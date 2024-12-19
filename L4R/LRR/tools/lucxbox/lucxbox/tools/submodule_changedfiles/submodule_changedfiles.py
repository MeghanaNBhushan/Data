#!/usr/bin/env python3
""" Script to add changed files from submodule into changed files file
"""
import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.gitw import gitw

LOGGER = lucxlog.get_logger()


def nonempty_str(value: str):
    if len(value) > 0:
        return value
    raise argparse.ArgumentTypeError("Must not be empty string")


def parse_args() -> argparse.Namespace:
    """Adds and parses command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-cf', '--changed-files-file', required=True, type=nonempty_str,
                        help='Name of the file containing list of changed files')
    parser.add_argument('-sub', '--submodule-relative-path', required=True, type=nonempty_str,
                        help='Relative path of submodule in main repository')
    parser.add_argument('-dci', '--dest-commit-id', required=True, type=nonempty_str,
                        help='Main repository commit id. Ex: ^ENV:LUCX_TARGET_BRANCH_COMMIT;')
    return parser.parse_args()


def get_submodule_changed_revision(dest_commit_id, submodule_relative_path):
    """Get changed revision of updated submodule in PR
    """
    LOGGER.info("Getting submodule changed revision")
    repo = gitw.Repo(os.getcwd())
    old_rev, new_rev = repo.get_submodule_changed_revision(dest_commit_id, submodule_relative_path)
    return old_rev, new_rev


def get_submodule_changed_files(submodule_relative_path, old_rev, new_rev):
    """Get changed files of updated submodule in PR
    """
    LOGGER.info("Getting submodule changed files list")
    submodule_repo = gitw.Repo(os.path.abspath(submodule_relative_path))
    diff_files = submodule_repo.get_changed_files_of_commits(old_rev, new_rev)
    return diff_files


def get_changed_files_from_file(changed_files_file):
    """Get list of changed files from changed files file
    """
    LOGGER.info("Getting existing changed files list")
    try:
        with open(changed_files_file, 'r') as file:
            return file.read().splitlines()
    except IOError as error:
        LOGGER.warning('Could not read file: %s', error)
        raise Exception('Could not read changed files file')


def append_submodule_changed_files(changed_files, submodule_changed_files, submodule_relative_path):
    """Append changed files of updated submodule into changed files list
    """
    LOGGER.info("Append submodule changed files list into existing changed files list")
    # Remove submodule path
    submodule_full_path = os.path.abspath(submodule_relative_path)
    changed_files.remove(submodule_full_path)

    # Append submodule changed files
    for changed_file in submodule_changed_files:
        changed_file_path = os.path.abspath(os.path.join(submodule_full_path, changed_file))
        changed_files.append(changed_file_path)
    return sorted(changed_files)


def update_changed_files_file(changed_files_file, changed_files):
    LOGGER.info("Updating changed files file")
    try:
        with open(changed_files_file, 'w') as file:
            file.writelines("\n".join(changed_files))
    except IOError as error:
        LOGGER.warning('Could not write file: %s', error)
        raise Exception('Could not write changed files file')


def update_submodule_changed_files(changed_files_file, submodule_relative_path, dest_commit_id):
    """Update changed files file to include list of changed files from submodule in Pull Request
    """
    # Get changed revision
    old_rev, new_rev = get_submodule_changed_revision(dest_commit_id, submodule_relative_path)
    if old_rev is None or new_rev is None:
        LOGGER.info("Not found changed revision")
        return

    # Get submodule changed files
    submodule_changed_files = get_submodule_changed_files(submodule_relative_path, old_rev, new_rev)
    if len(submodule_changed_files) == 0:
        LOGGER.info("Not found submodule changed files")
        return

    # Append submodule changed files
    current_changed_files = get_changed_files_from_file(changed_files_file)
    all_changed_files = append_submodule_changed_files(current_changed_files, submodule_changed_files,
                                                       submodule_relative_path)

    # Update changed files file
    update_changed_files_file(changed_files_file, all_changed_files)


if __name__ == '__main__':
    args = parse_args()

    LOGGER.debug("Arguments:")
    LOGGER.debug("Changed files file: %s", args.changed_files_file)
    LOGGER.debug("Submodule relative path: %s", args.submodule_relative_path)
    LOGGER.debug("Destination commit id: %s", args.dest_commit_id)
    LOGGER.debug("-----------------------")

    update_submodule_changed_files(args.changed_files_file, args.submodule_relative_path, args.dest_commit_id)

    LOGGER.info("Completed")
