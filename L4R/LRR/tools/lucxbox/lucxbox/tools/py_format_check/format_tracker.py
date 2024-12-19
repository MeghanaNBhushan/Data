# pylint: disable=logging-fstring-interpolation, bad-continuation
from typing import Union, List
import inspect
from pathlib import Path
import sys
import subprocess
import logging
import pandas as pd


def dump_args(func):
    """
    Decorator to log function call details.

    This includes parameters names and effective values.
    """

    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ", ".join(
            "{} = {!r}".format(*item) for item in func_args.items()
        )
        logging.debug(
            f"Calling function {func.__module__}.{func.__qualname__}"
            f" with args\n     ( {func_args_str} )\n"
        )
        return func(*args, **kwargs)

    return wrapper


@dump_args
def call_subprocess(cmd_args: List[str], dir_path: Union[Path, str]) -> str:
    """
    Call cmd_args to run subprocess.run() from some dir_path.

    Args:
        cmd_args (List[str]): Full command to run
        dir_path (Union[Path, str]): Directory where the command should be run

    Returns:
        str: Decoded stdout without leading and trailing characters
    """
    try:
        process = subprocess.run(
            cmd_args, capture_output=True, cwd=dir_path, text=True, check=True
        )
    except subprocess.CalledProcessError:
        logging.exception(
            f"Something went wrong when calling {cmd_args}. \
              Check if the command can be run in the command line."
        )
        sys.exit(1)
    return process.stdout.strip()


def get_common_ancestor(
    root_dir: Union[Path, str], target_branch: str, commit: str
) -> str:
    """
    Get the merge-base (a.k.a. common parent/ancestor) from
    a specific commit to the head of a certain branch

    Args:
        root_dir (Union[Path, str]): Path to repository root dir_path
        target_branch (str): Branch name
        commit (str): Commit ID

    Returns:
        str: Commit ID of latest common parent
    """
    # Find the newest common ancestor
    common_ancestor_cmd = ["git", "merge-base", target_branch, commit]
    common_ancestor = call_subprocess(common_ancestor_cmd, dir_path=root_dir)
    logging.debug(
        f"""Found merge-base commit {common_ancestor}
            with branch {target_branch}"""
    )
    return common_ancestor


def get_git_diff_files(
    root_dir: Union[Path, str], target_branch: str, commit: str
) -> List[str]:
    """
    Get list of files that are different from a specific commit
    to the head of a target branch

    Args:
        root_dir (Union[Path, str]): Path to git project root
        target_branch (str): Name of branch to compare against
        commit (str): Commit ID as comparison baseline

    Returns:
        List[str]: Files that have changed in the current commit
                   w.r.t. the target branch
    """
    # Get file names of the PR diff (ala Bitbucket)
    common_ancestor = get_common_ancestor(root_dir, target_branch, commit)
    git_diff_cmd = [
        "git",
        "diff",
        "--diff-filter=ACMR",
        "--name-only",
        common_ancestor,
    ]
    diff_list = call_subprocess(git_diff_cmd, dir_path=root_dir).split()
    logging.debug(f"Found diff against branch {target_branch}: {*diff_list,}")
    return diff_list


def get_repo_root(
    file_dir: Union[str, Path] = Path(__file__).resolve().parent
):
    """
    Get the repository root level of a certain dir_path.
    This returns the "parent repo" dir_path and not the submodule's root.

    Args:
        file_dir (Union[str, Path], optional): Path to some file.
                                               Defaults to dir of this file.

    Returns:
        [Path]: Path to the parent repo root
    """
    git_root_cmd = [
        "git",
        "rev-parse",
        "--show-superproject-working-tree",
        "--show-toplevel",
    ]
    repository_root = call_subprocess(git_root_cmd, dir_path=file_dir).split()[
        0
    ]
    logging.info(f"Found repo root {repository_root} for {file_dir}")
    return Path(repository_root)


def get_branch_head(repo_root_dir: Union[str, Path]) -> str:
    """
    Get the latest commit of the current git branch

    Args:
        repo_root_dir (Union[str, Path]): Path to the repo

    Returns:
        str: Commit ID of HEAD
    """
    git_head_cmd = ["git", "rev-parse", "HEAD"]
    head_commit = call_subprocess(git_head_cmd, dir_path=repo_root_dir).strip()
    logging.info(f"Found head commit: {head_commit}")
    return head_commit


def is_flake8_config(file: Path):
    """
    Check if a file is a valid flake8 configuration file
    See https://flake8.pycqa.org/en/latest/user/configuration.htm

    Args:
        file (Path): Path to a candidate flake8 configuration file

    Returns:
        bool: True if it's a valid if flake8 configuration
              False otherwise
    """
    try:
        with file.open() as config_file:
            for line in config_file:
                if line.strip().startswith("[flake8]"):
                    return True
            return False
    except FileNotFoundError:
        logging.debug(f"Could not find config file {file}")
        return False
    except (PermissionError, IsADirectoryError):
        logging.warning(f"{file} is not a file!!")
        return False


def find_config_file(repo_root: Path) -> Path:
    """
    Searches for flake8 config files in the repo root.
    See https://flake8.pycqa.org/en/latest/user/configuration.html

    Args:
        repo_root (str, Path): Root of project repository

    Raises:
        FileNotFoundError: No flake8 config file is found in the project root

    Returns:
        Path: Name of root's flake8 configuration file
    """
    candidates = (".flake8", "setup.cfg", "tox.ini")
    candidate_paths = {
        repo_root.joinpath(config_file) for config_file in candidates
    }
    cfg_files = list(filter(is_flake8_config, candidate_paths))

    if not cfg_files:
        raise FileNotFoundError(
            f"No flake8 configuration files found in {repo_root}"
        )

    if len(cfg_files) != 1:
        raise ValueError(
            f"Multiple flake8 configuration files found: {cfg_files}"
        )
    [cfg_file] = cfg_files
    logging.info(f"Found config file: {str(cfg_file)}")
    return cfg_file


def lint_all(dir_path: str, output: str, pickle: str = "") -> int:
    """
    Use flake8 to lint the whole repository and save results to its root.
    Optional: Write a DataFrame pickle to the repository root

    Args:
        dir_path (str): Path to a dir_pathectory inside the repository
        output (str): Name of output file for flake8 run
        pickle (str, optional): Name of DataFrame pickle to save.
                                Defaults to ''.
    Returns:
        int: 0 if flake8 could analyse the repo.
             1 if run was unsuccesful
    """
    # Set up paths
    repo_root = get_repo_root(dir_path)
    baseline_file = repo_root.joinpath(output)

    config_file = find_config_file(repo_root)

    # Run flake8 for the whole the repository
    err = lint_and_pickle(
        output=baseline_file,
        config_file=config_file,
        files_to_lint=["."],
        root=repo_root,
        pickle=pickle,
    )

    return err


def run_flake8(
    output_file: Path,
    config: Union[str, Path],
    files: List[str],
    dir_path: Union[str, Path],
) -> int:
    """
    Use a configuration file to run flake 8as a subprocess to lint a project.
    This overwrites the format pattern in the configuration file and
    use separator (_-_) for the output before saving it in the working dir.

    Args:
        output_file (Path): File path where the log is saved
        config (str): Flake8 configuration file on same level as "dir_path"
        files (Union[str, List[str]]): Python file(s) to lint
        dir_path (Union[str, Path]): Path where flake8 will be run from

    Returns:
        int: 0 if flake8 run successfully (despite linting errors found)
             1 otherwise
    """
    # Prepare flake8 command
    format_pattern = "%(path)s_-_%(row)d_-_%(col)d_-_%(code)s_-_%(text)s"
    flake8_args = [
        "flake8",
        f"--format={format_pattern}",
        f"--config={config}",
    ]

    # Extend files with string cast since pathlib objects are not correctly
    # handled by subprocess in python 3.7. This bug is fixed in python 3.8
    flake8_args.extend(str(py_file) for py_file in files)
    logging.info(
        f"Running {flake8_args} from {dir_path} and saving to {output_file}"
    )
    # Run flake8 and write to file
    with output_file.open(mode="w") as log_file:
        try:
            subprocess.run(
                flake8_args, stdout=log_file, cwd=dir_path, check=False
            )
            # Do not use return code of flake8
            err = 0
            logging.info("Flake8 run successful")
        except FileNotFoundError:
            logging.exception(
                f"Could not run {flake8_args}. Check if flake8 is installed."
            )
            err = 1
    return err


def create_flake8_pickle(
    flake8_log: Union[str, Path], path: Path, filename: Union[Path, str]
) -> int:
    """
    Read a flake8 logfile and create a Pandas DataFrame pickle out of it
    This uses a separator (_-_) for the flake8 logfile.

    Args:
        path (Path): Location where the pickle will be saved
        flake8_log (Path): Path to Flake8 logfile
        filename (str): Name of the pickle

    Returns:
        int: 0 if pickle was created.
             1 if unsuccesful
    """
    baseline_pickle = path.joinpath(filename)
    dataframe = read_flake8_log(flake8_log)

    try:
        dataframe.to_pickle(baseline_pickle)
        err = 0
        logging.info(f"Saved pickle {baseline_pickle} from {flake8_log}")
    except AttributeError:
        logging.exception(f"{dataframe} not a valid DataFrame")
        err = 1
    except ValueError:
        logging.exception(f"{baseline_pickle} not a valid path")
        err = 1
    return err


def read_flake8_log(flake8_log: Union[Path, str]) -> pd.DataFrame:
    """
    Read a flake8 log and return it as a Pandas DataFrame
    This assumes a separator (_-_) for the flake8 logfile.

    Args:
        flake8_log (Path): Path to Flake8 logfile
    Raises:
        ValueError: Invalid DataFrame created (NaN values or empty)
        SystemExit: Return code 1 if exception occurs

    Returns:
        pd.DataFrame: Flake8 log as DataFrame

    """
    column_names = ["filename", "lineNo", "columnNo", "errorNo", "comment"]
    try:
        logging.info(f"Reading {flake8_log} with column names {column_names}")
        baseline_df = pd.read_csv(
            flake8_log, sep="_-_", engine="python", names=column_names
        )
    except FileNotFoundError:
        logging.exception(f"Flake8 logfile not found {flake8_log}")
        sys.exit(1)
    except OSError:
        logging.exception(f"{flake8_log} is not a readable file!")
        sys.exit(1)
    except pd.errors.ParserError:
        logging.exception(f"{flake8_log} is not a 'comma' separated file!")
        sys.exit(1)
    else:
        if baseline_df.isnull().values.any():
            raise ValueError(
                f"""{flake8_log} is not a valid flake8 log.
                    Check that the separators are '_-_'
                 """
            )
        # Transform file names to Path for OS-consistency
        baseline_df["filename"] = baseline_df["filename"].apply(
            lambda x: str(Path(x))
        )
        return baseline_df


def lint_diff(
    dir_path: str,
    output: Union[Path, str],
    target_branch: str,
    pickle: str = "",
) -> int:
    """
    Lint modified, addded, renamed or moved *.py files listed
    in "diff" against a target branch.

    Args:
        dir_path (str): Path to a directory inside the repository
        output (str): Name of output file for flake8 run
        pickle (str, optional): Name of DataFrame pickle to save.
                                Defaults to ''.
        target_branch (str): Parent or branch to run the diff against.

    Returns:
        [int]: 0 if flake8 could analyse the diff (even if empty).
               1 if run was unsuccesful
    """
    # Run styleChecker for this branch
    repo_root = get_repo_root(dir_path)
    output_path = repo_root.joinpath(output)

    config_file = find_config_file(repo_root)

    head = get_branch_head(repo_root)
    diff_files = get_git_diff_files(
        repo_root, target_branch=target_branch, commit=head
    )
    py_files = [f for f in diff_files if f.endswith(".py")]
    logging.info(f"Found {len(py_files)} *.py files in diff: {py_files}")

    err = 0
    if py_files:
        err = lint_and_pickle(
            output=output_path,
            config_file=config_file,
            files_to_lint=py_files,
            root=repo_root,
            pickle=pickle,
        )
    return err


def lint_and_pickle(
    output: Path,
    config_file: Union[Path, str],
    files_to_lint: List[str],
    root: Path,
    pickle: str,
) -> int:
    """
    Lint python files of a project and optionally pickle the results.

    Args:
        output (Path): Name of the output file for linting run
        config_file (str): A configuration file for flake8
        files_to_lint (Union[str, List[str]]): File(s) *.py to be linted
        root (Path): Working directory where the linting will be executed
        pickle (str): Name of the pickle file

    Returns:
        int: 0 if linting (and pickle if requested) succeeded
             1 otherwise
    """

    err = run_flake8(
        output_file=output,
        config=config_file,
        files=files_to_lint,
        dir_path=root,
    )

    if err == 0 and pickle:
        err = create_flake8_pickle(
            path=root, flake8_log=output, filename=pickle
        )
    return err


def read_pandas_pickle(file_path: Path) -> pd.DataFrame:
    """
    Wrapper to read a Pandas DataFrame saved as pickle

    Args:
        file_path (Path): Path to Pandas pickle

    Returns:
        pd.DataFrame: Pandas DataFrame from pickle
    """
    try:
        logging.info(f"Reading pickle {file_path}")
        dataframe = pd.read_pickle(file_path)
    except FileNotFoundError:
        logging.exception(f"Could not find {file_path}")
        sys.exit(1)
    except (PermissionError, IsADirectoryError):
        logging.exception(f"{file_path} is not a file!!")
        sys.exit(1)
    except KeyError:
        logging.exception(f"{file_path} is not a pickle!!")
        sys.exit(1)
    return dataframe


def compare_linting(
    dir_path: str, baseline: Union[str, Path], local_changes: Union[str, Path]
) -> int:
    """
    Compare the linting results of a branch against a baseline.

    Args:
        dir_path (str): Path to some folder inside a repository.
                   Not necessarily the root.
        baseline (Union[str, Path]): DataFrame pickle with flake8 result
                                     that serves as the max. amount of allowed
                                     errors
        local_changes (Union[str, Path]): DataFrame pickle with
                                          flake8 branch linting

    Returns:
        int: [description]
    """
    # Set up paths
    repo_root = get_repo_root(dir_path)
    baseline_path = repo_root.joinpath(baseline)
    local_changes_path = repo_root.joinpath(local_changes)

    # Get linting results
    baseline_df = read_pandas_pickle(baseline_path)
    branch_df = read_pandas_pickle(local_changes_path)

    # Compare both DFs
    merged = branch_df.merge(baseline_df, indicator=True, how="outer")

    # Get only newly added linting errors
    logging.info("Comparing local lint against baseline..")
    new_errors = merged[merged["_merge"] == "left_only"]
    number_of_errors = len(new_errors)
    if number_of_errors:
        del new_errors["_merge"]
        new_errors.to_csv(
            repo_root.joinpath("new_errors.csv"), index=False, header=False
        )
        new_errors.to_json(
            repo_root.joinpath("new_errors.json"), orient="records"
        )
    logging.info(f"{number_of_errors} new errors found.")
    return number_of_errors
