#!/bin/env python3
""" Sanity check for git lfs """

import argparse
import fnmatch
import os
import subprocess
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog, portal

LOGGER = lucxlog.get_logger()


def parse_args(arguments):
    desc = "Sanity Check for git lfs extension which verifies that all " + \
           "fils are properly check into git lfs."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--root", "-r", help="Path to the root of the repository." +
                        " Optional argument.")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args(arguments)


def get_lfs_attributes():
    for line in subprocess.check_output(["git", "lfs", "track"]).splitlines():
        line = line.decode("utf-8")
        yield line.strip().split(' ')[0]


def get_all_files():
    for line in subprocess.check_output(["git", "ls-files"]).splitlines():
        line = line.decode("utf-8")
        yield line.strip()


def get_lfs_files():
    for line in subprocess.check_output(["git", "lfs", "ls-files"]).splitlines():
        line = line.decode("utf-8")
        yield line.split(' ', 2)[2].strip()


def get_new_staged_files():
    # --diff-filter=[(A|C|D|M|R|T|U|X|B)...[*]]
    # Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), ...
    for line in subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=AR"]).splitlines():
        line = line.decode("utf-8")
        yield line.strip()


def get_wrong_files(git_all_files, git_lfs_files, git_lfs_attributes):
    git_files_should_be_in_lfs = set()
    for attribute in git_lfs_attributes:
        git_files_should_be_in_lfs |= {
            x for x in git_all_files if fnmatch.fnmatch(x, attribute)}
    for move_candidate in git_files_should_be_in_lfs - git_lfs_files:
        # Additional check if file is not excluded in some .gitattribute file.
        # As far as `git lfs track` for git-lfs version < 2.6.0 is not showing explicitly excluded patterns.
        if subprocess.check_output(["git", "check-attr", "filter", move_candidate],
                                   universal_newlines=True).strip().split(": ")[2] == "lfs":
            yield move_candidate
        else:
            LOGGER.debug("File: %s is excluded by .gitattributes", str(move_candidate))

def sanity_check(git_all_files, git_lfs_files, git_lfs_attributes):
    error = "Sanity check failed, %s."
    if not git_all_files:
        LOGGER.error(error, "no file tracked by git at all")
        sys.exit(1)
    if not git_lfs_files:
        LOGGER.error(error, "no file tracked by git lfs")
        sys.exit(1)
    if not git_lfs_attributes:
        LOGGER.error(error, "no attributes found for git lfs")
        sys.exit(1)


def handle_error(wrong_files):
    files = ", ".join(wrong_files)
    LOGGER.error("Following files should be under git-lfs control: %s", files)
    sys.exit(len(wrong_files))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv[1:])
    LOGGER.setLevel(args.log_level)

    from_path = os.path.abspath(os.getcwd())
    if args.root:
        from_path = os.path.abspath(args.root)
        LOGGER.info("Changing into '%s'.", args.root)
        if not os.path.isdir(args.root):
            LOGGER.error("Given path '%s' is not a directory.", args.root)
            sys.exit(1)

    with portal.In(from_path):
        git_all_files = set(get_all_files())
        LOGGER.debug("all tracked files: %s", str(git_all_files))
        git_lfs_files = set(get_lfs_files())
        LOGGER.debug("all tracked lfs files: %s", str(git_lfs_files))
        git_lfs_attributes = set(get_lfs_attributes())
        LOGGER.debug("git lfs attributes: %s", str(git_lfs_attributes))

        # INFO(fub2lr) In the lucxbau we merge the pull request with "git merge --squash --no-commit --no-ff".
        # Files that are now in the staging area and are added have to be ignored.
        git_new_staged_files = set(get_new_staged_files())
        LOGGER.debug("git staged files: %s", str(git_new_staged_files))
        git_all_files = git_all_files - git_new_staged_files

    sanity_check(git_all_files, git_lfs_files, git_lfs_attributes)

    wrong_files = set(get_wrong_files(git_all_files, git_lfs_files, git_lfs_attributes))
    LOGGER.debug("wrong files: %s", str(wrong_files))

    if wrong_files:
        handle_error(wrong_files)


if __name__ == "__main__":
    sys.exit(main())
