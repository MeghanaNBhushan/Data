""" Finder is a library for helping you get files and folders you need. """
import os

from lucxbox.lib.lucxutils import execute


def get_files_with_ending(endings, excludes=None):
    """ Recursive get all files with ending. """
    if isinstance(endings, list) is False:
        raise TypeError("Parameter 'endings' is not a list.")
    if excludes is None:
        excludes = []

    matches = []

    for root, _, files in os.walk("."):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            ending_matches = any(file_name.endswith(ending) for ending in endings)
            excluded = any(os.path.normpath(exclude) in file_path for exclude in excludes)
            if ending_matches and not excluded:
                matches.append(file_path)
    return matches


def get_git_root(path=None):
    if path:
        cwd = path
    else:
        cwd = os.getcwd()
    out, err, returncode = execute(["git", "rev-parse", "--show-toplevel"], cwd=cwd)
    if returncode != 0:
        raise ValueError("Getting git root failed with error: " + err.strip())
    lines = out.split("\n")
    root = lines[0].strip()
    if os.path.isdir(root):
        return root
    else:
        raise ValueError("Getting git root failed. Can not understand output:" + out.strip())


def get_git_topmost_root(path=None):
    if path:
        cur_path = path
    else:
        cur_path = os.getcwd()
    last_path = cur_path
    try:
        ret_val = get_git_root(cur_path)
    except ValueError as error:
        raise error
    while os.path.exists(ret_val):
        last_path = cur_path
        cur_path = os.path.dirname(cur_path)
        try:
            ret_val = get_git_root(cur_path)
        except ValueError:
            # Found toplevel git folder
            break
    # Get top level
    repo_root_dir = last_path
    return repo_root_dir
