#!/usr/bin/python
""" Script for checking the correct usage of the copyright header. """
import argparse
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog
from lucxbox.tools.copyright_checker.copyright_result import CopyrightResult

LOGGER = lucxlog.get_logger()

EXTENSION = (".cpp", ".c", ".hpp", ".h", ".s", ".inl")

REGEX_RB = r"(.*Copyright\s+\(c\)\s+\d{4}|.*\s+\@copyright\s+\(c\)\s+\d{4}\s+-\s+\d{4})\s+by\s+Robert\s+Bosch\s+GmbH"
REGEX_OTHER_RB = r"(\(C\)|COPYRIGHT).*ROBERT\s+BOSCH"
REGEX_OTHER = r".*Copyright|(\*|//)\s+\(C\)"
REGEX_BREAK = r".*\#include|.*\#define |// stringbitmap"

EXCLUDED_FILES = ["stringbitmap_coretest.hpp"]
EXCLUDED_FOLDERS = ["fv_if/tools", "fv_if/cubas/ext"]


def check_file(file_name, repo_name, root=""):
    """ Check a file for correctness if its copyright header and return a CopyrightResult object """
    copyright_result = CopyrightResult(root, file_name, repo_name, LOGGER)
    try:
        # Check if file has an extension, which should be checked
        if copyright_result.get_file_name().endswith(EXTENSION):
            # check if file should be ignored
            is_in_excluded_files = False
            for excluded_file_name in EXCLUDED_FILES:
                if excluded_file_name == copyright_result.get_file_name():
                    is_in_excluded_files = True
                    copyright_result.set_is_ignored(True)
                    break

            if not is_in_excluded_files:
                with open(copyright_result.get_full_path(), "r") as read_in_file:
                    for line in read_in_file:
                        if re.search(REGEX_RB, line, re.IGNORECASE):
                            copyright_result.set_has_rb_copyright(True)
                            return copyright_result
                        elif re.search(REGEX_OTHER_RB, line, re.IGNORECASE) and not re.search(REGEX_RB, line,
                                                                                              re.IGNORECASE):
                            copyright_result.set_has_other_rb_copyright(True)
                            return copyright_result
                        elif re.search(REGEX_OTHER, line, re.IGNORECASE) and not re.search(REGEX_RB, line,
                                                                                           re.IGNORECASE):
                            copyright_result.set_has_other_copyright(True)
                            return copyright_result
                        elif re.search(REGEX_BREAK, line, re.IGNORECASE):
                            break
                copyright_result.set_has_no_copyright(True)
        else:
            copyright_result.set_is_ignored(True)

        return copyright_result

    except IOError:
        copyright_result.set_is_ignored(True)
        return copyright_result


def check_folder(root_folder, repo_name, subdir_desired=False):
    """ Check the copyright header for all files inside a folder. Also include the sub folders if desired. """
    result_list = []

    total_folders = 0
    for root, _, files in os.walk(root_folder):
        total_folders += 1
        if not subdir_desired:
            break

    for root, _, files in os.walk(root_folder):
        for current_file in files:
            # check if folder should be ignored
            is_in_excluded_folder = False
            for folder in EXCLUDED_FOLDERS:
                if folder in root.replace("\\", "/"):
                    is_in_excluded_folder = True
                    result = CopyrightResult(root, current_file, repo_name, LOGGER)
                    result.set_is_ignored(True)
                    result_list.append(result)
                    break

            # if folder should not be ignored -> check file
            if not is_in_excluded_folder:
                result_list.append(check_file(current_file, repo_name, root))

        # stop after first iteration if no sub folders shall be included in the analysis
        if not subdir_desired:
            break

    return result_list


def check_list_of_files(input_file, repo_name):
    result_list = []

    total_files = 0
    with open(input_file) as file_handler:
        for line in file_handler:
            total_files += 1

    with open(input_file) as file_handler:
        for line in file_handler:
            path, file_name = os.path.split(line)
            if "/ext/" not in line:
                result = check_file(file_name, repo_name, path)
                result_list.append(result)

    return result_list


def parse_args():
    """
    Implementation of the argument parser with various options
    :return: The argument object containing all argument information.
    """
    parser = argparse.ArgumentParser(description="Process arguments.")
    parser.add_argument("--repo-name", dest="repo_name", default="fvg3",
                        help="The repository name of the project")
    parser.add_argument("--root-folder", dest="root_folder", default="../../../../fvg3",
                        help="the root folder of the directory to check.")
    parser.add_argument("-s", "--subdir", dest="subdir_desired", action="store_true", default=False,
                        help="Include sub directories in check? Default: False")
    parser.add_argument("-p, ""--print", action="store_true", default=False, dest="print_to_console",
                        help="Print results to console? Default: False")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check-single-file", default="", dest="check_single_file",
                       help="Set this if you wish to check a single file")
    group.add_argument("--check-file-of-files", default="", dest="check_file_of_files",
                       help="Path to file containing paths of files to check.")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args()


def print_result(result):
    LOGGER.info("----------------------------------------")
    LOGGER.info("Copyright Result Issues")
    LOGGER.info("----------------------------------------")
    if isinstance(result, list):
        counter = 1
        for item in result:
            if not item.get_has_rb_copyright() and not item.get_is_ignored():
                item.print_result(counter)
                counter += 1
    else:
        if not result.get_has_rb_copyright() and not result.get_is_ignored():
            result.print_result()


def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)
    root_folder = args.root_folder
    subdir_desired = args.subdir_desired
    check_single_file = args.check_single_file
    check_file_of_files = args.check_file_of_files
    print_to_console = args.print_to_console
    repo_name = args.repo_name

    if check_single_file != "":
        path, file_name = os.path.split(check_single_file)
        result = check_file(file_name, repo_name, path)
    elif check_file_of_files != "":
        result = check_list_of_files(check_file_of_files, repo_name)
    else:
        result = check_folder(root_folder, repo_name, subdir_desired)

    if print_to_console:
        print_result(result)


if __name__ == "__main__":
    main()
