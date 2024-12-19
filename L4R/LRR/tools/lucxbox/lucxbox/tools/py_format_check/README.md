# Python Format Checker

The Python Format Checker is a portable tool to introduce format linting for Python files with CI in mind.
It provides an easy-to-use yet robust flake8 wrapper interface for any git project.

By first defining a baseline instead of directly formatting the whole repository, we can define clear constraints without slowing down the development process.
Furthermore, adopting new project-wide options is limited only to the discussion and edition of the project's flake8 configuration file.

## Installation

This requires at least Python 3.7 with `flake8` and `pandas` installations in your environment.
A valid flake8 configuration file on the root level is also needed.

Refer to this repository's requirements.

See https://flake8.pycqa.org/en/latest/user/configuration.html

## Usage

Check first the CLI help by running
```python pyFormatCheck.py -h```

Now that you got a feel for what's intended, you will know that this aims to be robust and the cwd is irrelevant, thus you can also run it from this repository's root
```python lucxbox/tools/py_format_check/pyFormatCheck.py command --any arguments``` or from any other dir you want. 

This is important because you can run the Python Format Checker from your
repository's dir without having to explicitly add this script to your project
```python /path/to/this/repo/pyFormatCheck.py -d . command --any arguments```

In order to integrate this checker into your project, consider the following steps:

1. Create a baseline for your current repository. This can be updated either on the nightly or for each merge-commit to your trunk, depending on your repo size.
```python pyFormatCheck.py -d /path/to/your/repo/ lintAll --output nightly_run.log --pickle nightly_baseline.pkl```

2. Check for each Pull Request if there's any linting errors in the files in the diff against a target branch (usually `origin/develop`) 
```python pyFormatCheck.py -d /path/to/your/repo/ lintDiff --output local_run.log --pickle local_changes.pkl --target_branch origin/develop```

3. Compare the linting results of the previous step against some baseline defined in the first step. This will yield a nonzero exit code if errors were added.
```python pyFormatCheck.py -d /path/to/your/repo/ compareLint -baseline nightly_baseline.pkl --localchanges local_changes.pkl```

Furthermore, two files `new_errors.csv` and `new_errors.json` with information about the newly added errors will be saved in the repository's root directory for further usage.


You can now fail Pull Requests that make code reviews harder!

## Argparse help

usage: py_format_check.py [-h] [-v] [-d DIR_PATH]
                          {lintAll,lintDiff,compareLint} ...

positional arguments:
  {lintAll,lintDiff,compareLint}
                        Command to run
    lintAll             Lint all *.py files from a whole project repository.
                        Returns zero exit code iff flake8 ran successfully or
                        if the output could be saved. See https://flake8.pycqa
                        .org/en/latest/user/configuration.html
    lintDiff            Lint only the *.py files found in the diff from the
                        current checked out branch against some target branch.
                        Returns zero exit code iff flake8 ran successfully or
                        if the output could be saved.
    compareLint         Compare two linting results from flake8 runs. Requires
                        a valid baseline pickle (see lint_repo) and newly
                        added changes (see lint_diff). Returns zero exit code
                        iff no new linting errors were added w.r.t. the
                        baseline.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Select verbosity level. Default is 0. Values above -vv
                        are casted to DEBUG
  -d DIR_PATH, --dir_path DIR_PATH
                        Directory path in a repository. Not necessarily the
                        root. A single valid flake8 configuration file in the
                        project's root dir is required. This defaults to the
                        current script's dir

The current script's dir = lucxbox/tools/py_format_check/

## Contributing

Pull requests are welcome. For major changes, please open first an issue to discuss what you would like to change.

## Authors
Franco Camborda (CC-DA/EAS2) <FrancoPaul.CambordaLaCruz@bosch.com>