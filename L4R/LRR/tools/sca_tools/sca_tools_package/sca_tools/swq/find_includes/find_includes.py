# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: find_includes.py
# ----------------------------------------------------------------------------
"""This script finds all source files which include given hpp/inl files,
directly or indirectly.

The main use case for this script is to support local QAC analysis using the
sca_tools script[*], which is able to produce a lightweight PRQA/QAC
solution based only on the files which were modified in a pull request.

However, at the time of writing this script, the prqa_helper (sca_tools)
script had the following limitation: QAC can not analyze header files
by themselves. It always needs a source file. If a PR only modified a header
file, but not a corresponding source file, the prqa_helper (sca_tools) script
produces a PRQA/QAC solution which does not contain the corresponding source
files. Hence, the changes to the header files might not be analyzed.

The script offers a solution for this problem by taking a list of
file paths relative to a given project root and producing a list of
corresponding source files. This list can then be supplied to the prqa_helper
(sca_tools) script to produce a suitable PRQA/QAC solution.

In detail, this means:
- every source file in the input list is also written to the output list
- for every hpp/inl file in the input list, either
    * _all_ source files which (directly or indirectly) include that header
      file are written to the output list (option "all"), or
    * _one_ such source file is written to the output list (option "minimal").

A "minimal" output list leads to the smallest possible PRQA/QAC solution
where all modified files appear. However, it is currently not 100% certain
whether this would produce all QAC warnings that would have been produced
when analyzing the complete repository (in particular when the header files
contain C++ template code).

A "complete" output list removes these uncertainties at the cost of a slightly
longer PRQA/QAC analysis time. However, in most cases, the analysis time will
still be significantly less than analyzing the whole repository.

By default, the target:
- Assumes that it is called from somewhere within a git repository to
  be analyzed.
- Generates the input file list by producing the name-only git diff between
  the current git branch and its merge-base with origin/develop (like it
  would be done by the prqa_helper script). Note: local modifications which
  have not yet been committed to git are not considered in this list!

The script can be customized to:
- Consider an explicitly specified path to a repository.
- Take the file list from stdin instead of the git diff.


[*] For more information see
https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/prqa_helper/browse.
"""

import itertools
import os
import re
import sys

from os import path
from collections import defaultdict

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t, \
    create_dirs_if_necessary
from swq.common.command.command_decorator import command
from swq.common.return_codes import log_and_exit, RC_CMD_FAILED
from swq.common.file.file_utils import remove_empty_lines_from_file
from swq.find_includes.exporters.reports_exporter import export_mapping_report

ACCEPTED_GIT_RETURN_CODES = [0]


class FindIncludes:
    """Class for the find_includes functionalities"""
    def __init__(self, config):
        """Initializes FindIncludes class using main QAC-helper \
        config file. Should provide following arguments in config:

        :find_include_strategy:
        :code_dirs_file:
        :thirdparty_prefixes:
        :project_root:
        :from_stdin:
        :merge_base:
        :to_stdout:
        :header_extensions:
        :source_extensions:
        :source_output_extensions:
        :unit_test_file_pattern:
        :blacklist_pattern:
        :from_list:
        :output_file:
        """
        self.__config = config
        self.__config.code_extensions = config.source_extensions + \
            config.header_extensions
        self.__config.include_search_pattern = \
            r'^\s*#\s*include\s+["<](.*)[>"]'

    def _exit_on_error_code(self, return_code):
        if return_code not in ACCEPTED_GIT_RETURN_CODES:
            log_and_exit(RC_CMD_FAILED)

    def __get_diff_using_merge_base_hash(self, merge_base_hash):
        return [
            "git", "diff", merge_base_hash, "HEAD", "--name-only",
            f"--diff-filter={self.__config.git_diff_filter}"
        ]

    def _get_diff_using_merge_base_hash(self, merge_base_hash) -> [str, int]:
        command_decorator = command(fail_fast=True,
                                    use_logger=True,
                                    silent=False,
                                    cwd=self.__config.project_root)(
                                        self.__get_diff_using_merge_base_hash)

        return command_decorator(merge_base_hash)

    def __get_merge_base_hash(self):
        return ["git", "merge-base", "HEAD", self.__config.merge_base]

    def _get_merge_base_hash(self) -> [str, int]:
        command_decorator = command(fail_fast=True,
                                    use_logger=True,
                                    silent=False,
                                    cwd=self.__config.project_root)(
                                        self.__get_merge_base_hash)

        return command_decorator()

    def get_file_diff_from_head_to_merge_base(self):
        """The function get_file_diff_from_head_to_merge_base gets the name \
        of the files which were changed or added
        Output:
        normed_diff_as_list... Struct of a List with changed files name"""
        [merge_base_hash, merge_base_rc] = self._get_merge_base_hash()
        self._exit_on_error_code(merge_base_rc)
        [diff,
         git_diff_rc] = self._get_diff_using_merge_base_hash(merge_base_hash)
        self._exit_on_error_code(git_diff_rc)
        normed_diff_as_list = [
            path.normpath(filepath.strip())
            for filepath in diff.strip().split()
        ]
        LOGGER.debug(
            'File diff from HEAD to merge-base with %s:\n%s',
            self.__config.merge_base,
            '\n'.join('    {}'.format(path) for path in normed_diff_as_list))
        return self.read_filepaths_from_lines(normed_diff_as_list)

    def read_filepaths_from_lines(self, line_or_lines):
        """Read filepaths one or several lines. These filepaths must be \
        whitespace separated"""
        lines = None

        if isinstance(line_or_lines, list):
            lines = line_or_lines
        else:
            lines = [line_or_lines]

        # Converts a list of lists into a list leaving the empty strings out
        def flatten(list_of_lists):
            return [
                item for a_list in list_of_lists for item in a_list if item
            ]

        return flatten([
            filepaths_line.rstrip("\'\"\n").split() for filepaths_line in lines
        ])

    def convert_to_repo_relative_path(self, filepath):
        """Convert a given path (as specified in an #include) to a path \
        relative to the top level of a repository.

        :param filepath: Path to convert.
        :return: Path relative to top level of repository.
        """
        relpath = path.normpath(filepath)
        try:
            common_relative_path = path.commonpath(
                [self.__config.project_root, relpath])
        except ValueError:
            common_relative_path = ''

        try:
            relpath = path.relpath(filepath, common_relative_path)
        except ValueError as error:
            # this can happen if for example replath is used on files
            # on different harddrives
            LOGGER.error('Normalizing file %s with root %s failed due to %s',
                         filepath, common_relative_path, error)

        return relpath

    def parse_included_files_in_file_content(self,
                                             file_content_as_list_of_lines):
        """Return all paths occurring in #include statements \
        in the given file content.

        :param file_content_as_list_of_lines: Content of a file, \
        given as a list of lines.
        :return: A sequence of paths included in the given file content.
        """
        for line in file_content_as_list_of_lines:
            match = re.search(self.__config.include_search_pattern, line)
            if match:
                yield match.group(1).strip()

    def is_3rd_party_include(self, include_path, thirdparty_prefixes):
        """Check whether an include path points to a 3rd party component \
        (vfc, Daddy, VMC).

        :param include_path: Include path string to check.
        :return: True if the path points to a 3rd party component, False else.
        """
        return_value = any(prefix in include_path
                           for prefix in thirdparty_prefixes)
        LOGGER.debug(
            "is_3rd_party_include include_path: {}  result: {}".format(
                include_path, return_value))
        return return_value

    def is_file_blacklisted(self, file_path, blacklist_pattern=""):
        """Check whether a given path denotes a black listed file.

        :param file_path: Path to be checked.
        :param blacklist_pattern: optional, to provide a custom filter string.
        :return: True if the file is blacklisted file (according to naming \
        conventions), False else.
        """
        return_value = False    # default is False
        pattern = ""
        if self.__config.file_blacklist_pattern:
            pattern = self.__config.file_blacklist_pattern
        if blacklist_pattern:
            pattern = blacklist_pattern
        if pattern:
            return_value = re.match(pattern, file_path)
        LOGGER.debug("is_file_blacklisted: checking file: {} \
            with pattern: {} result: {}".format(file_path, pattern,
                                                return_value))
        return return_value

    def is_code_file(self, file_path):
        """Check whether a given path denotes a C++ code file \
        (not a unit test file).

        :param file_path: Path to be checked.
        :return: True if the file is a cpp, hpp, h or inl file \
        and not a unit test file, False else.
        """
        LOGGER.debug("is_code_file: {}".format(file_path))
        has_code_extension = path.splitext(
            file_path)[1] in self.__config.code_extensions
        return has_code_extension and not self.is_file_blacklisted(file_path)

    def is_header_code_file(self, file_path):
        """Check whether a given path denotes a C/C++ header file \
        (not a unit test file).

        :param file_path: Path to be checked.
        :return: True if the file is a hpp/h/inl file and not \
        a unit test file, False else.
        """
        has_header_extension = path.splitext(
            file_path)[1] in self.__config.header_extensions
        return has_header_extension and not self.is_file_blacklisted(file_path)

    def is_source_code_file(self, file_path):
        """Check whether a given path denotes a source file.

        :param file_path: Path to be checked.
        :return: True if the file is a source file and not a unit test file, \
        False else.
        """
        has_source_extension = path.splitext(
            file_path)[1] in self.__config.source_extensions
        return has_source_extension and not self.is_file_blacklisted(file_path)

    def is_output_filter_satisfied(self, file_path):
        """Check whether a given path denotes a source file.

        :param file_path: Path to be checked.
        :return: True if the file is a source file and not a unit test file, \
        False else.
        """
        is_satisfied = path.splitext(
            file_path)[1] in self.__config.source_output_extensions
        return is_satisfied

    def get_fileid_from_path(self, header_filepath):
        """Returns base name of the filepath provided"""
        return path.basename(header_filepath)

    def _get_all_code_file_paths(self, search_directories, comparator):
        # Gets all paths from the file
        code_file_paths = []
        for code_dir in search_directories:
            for parent_directory, _, file_names in os.walk(
                    path.join(self.__config.project_root, code_dir)):
                # Filters the filenames if it is a code
                LOGGER.debug(
                    "_get_all_code_file_paths in parent_directory {}".format(
                        parent_directory))
                resolved_file_names = (path.join(parent_directory, f)
                                       for f in file_names)
                code_file_names = filter(comparator, resolved_file_names)
                code_file_paths.extend(f for f in code_file_names)
        return code_file_paths

    def create_mapping_of_file_to_all_direct_includers(self,
                                                       search_directories,
                                                       third_party_includes):
        """Create a mapping which takes a file and returns a set of \
        all direct includers of that given file.

        A direct includer of a given file is a C++ code file which contains \
        an #include statement referring to the given file.

        :search_directories: All directories to be in the search for the files.
        :return: A function which takes a PJ-DC repo-relative file path and
        returns a set of PJ-DC repo-relative
        file paths which denote direct includers of the specified file.
        """

        dict_mapping_file_to_all_direct_includers = defaultdict(set)

        for code_file_path in self._get_all_code_file_paths(
                search_directories, self.is_code_file):
            LOGGER.debug("_get_all_code_file_paths  {}".format(code_file_path))
            code_file_path_relative_to_repo = \
                self.convert_to_repo_relative_path(code_file_path)

            # looks if the path not in the find_cpp_3rd_party_prefixes.txt data
            with open_t(code_file_path) as code_file:
                # Read the content of the *.c/*.cpp/*.h/*.hpp files
                code_file_content = code_file.readlines()
                include_paths = self.parse_included_files_in_file_content(
                    code_file_content)
                # Filters the includes files and checks if
                # their are third party path
                relevant_include_paths_relative_to_repo = [
                    self.convert_to_repo_relative_path(include_path)
                    for include_path in include_paths
                    if not self.is_3rd_party_include(include_path,
                                                     third_party_includes)
                ]

            # Saves the abs. path of the h/hpp and c/cpp
            # which are included in the c/cpp files
            for relevant_include_path \
                    in relevant_include_paths_relative_to_repo:
                dict_mapping_file_to_all_direct_includers[
                    self.get_fileid_from_path(relevant_include_path)].add(
                        code_file_path_relative_to_repo)
        # Sort and save the included path in a with the argument file_path and
        # the expression dict_mapping_file_to_all_direct_includers
        return lambda file_path: dict_mapping_file_to_all_direct_includers[
            self.get_fileid_from_path(file_path)]

    def find_sources_which_include_header_file(
            self, header_file_path, map_file_to_all_direct_includers):
        """Get a sequence of source files which include a given header file \
        directly or indirectly.

        :param header_file_path: A repo-relative path to a C++ header \
        file (hpp/h/inl).
        :param map_file_to_all_direct_includers: A function which takes \
        a file path and returns a sequence of all code
        files in the repository which include the specified file directly via \
        an #include statement.
        :return: A generator object which produces a new source file \
        including the given header file (directly or indirectly) with \
        each iteration.
        """
        if not self.is_header_code_file(header_file_path):
            raise ValueError(
                '`header_file_path` is not a supported header file format.')

        # 'files_which_include_given_header_file' will be filled iteratively,
        # starting with all direct includers
        files_which_include_given_header_file =  \
            map_file_to_all_direct_includers(
                header_file_path
            )

        found_sources = set()
        while True:
            # Filters the found included filenames if they are source codes
            source_files_which_include_given_header_file = filter(
                self.is_source_code_file,
                files_which_include_given_header_file)
            # Saves the source filenames
            for source_file in source_files_which_include_given_header_file:
                if source_file not in found_sources:
                    found_sources.add(source_file)
                    yield source_file

            files_which_include_given_file_indirectly = set(
                itertools.chain.from_iterable(
                    map_file_to_all_direct_includers(f)
                    for f in files_which_include_given_header_file))
            # Number of items and return None if no change or nothing was found
            old_number_of_includers = len(
                files_which_include_given_header_file)
            files_which_include_given_header_file.update(
                files_which_include_given_file_indirectly)
            new_number_of_includers = len(
                files_which_include_given_header_file)
            if new_number_of_includers == old_number_of_includers:
                return None

    def _source_paths_generators(self, header_files,
                                 map_file_to_all_direct_includers):
        return [
            self.find_sources_which_include_header_file(
                header_file, map_file_to_all_direct_includers)
            for header_file in header_files
        ]

    def find_sources_for_header_files(self, header_files, search_directories,
                                      third_party_includes):
        """ The function find_sources_for_header_files calls the functions \
            which are responsible to find the files and to create the generator
                Input:
                    header_files... Struct of Paths which has been changed \
                    from the user
                    find_include_strategy... String of the Setting which \
                    have been to use
                Output:
                    found_source_files... Struct of a list which contains \
                    the filenames/path which header influenced sources """
        # Detect all included files and writes the abs. path in that var.
        map_file_to_all_direct_includers = \
            self.create_mapping_of_file_to_all_direct_includers(
                search_directories, third_party_includes
            )
        source_paths_generators = self._source_paths_generators(
            header_files, map_file_to_all_direct_includers)

        if self.__config.find_include_strategy == 'all':
            return set(itertools.chain.from_iterable(source_paths_generators))

        # find_include_strategy == 'minimal'
        return set(
            next(source_paths_generator, '')
            for source_paths_generator in source_paths_generators)

    def map_source_files_with_headers(self, header_files, search_directories,
                                      third_party_includes):
        """ Finds source files that include given header files \
            and returns mapping as dictionary  """
        map_file_to_all_direct_includers = \
            self.create_mapping_of_file_to_all_direct_includers(
                search_directories, third_party_includes
            )
        mapping_source_paths_dict = {
            self.convert_to_repo_relative_path(header_file): set(
                filter(
                    self.is_output_filter_satisfied,
                    self.find_sources_which_include_header_file(
                        header_file, map_file_to_all_direct_includers)))
            for header_file in header_files
        }

        return mapping_source_paths_dict

    def check_config_parameters(self):
        """Verify correctness and consistency of parsed \
        command line arguments."""
        assert self.__config.find_include_strategy in ('all', 'minimal')

    def norm_filepaths(self, filepaths):
        """Normalized a list of filepaths by applying \
        convert_to_repo_relative_path to each line"""
        normalized_lines = []
        for line in filepaths:
            norm_path = self.convert_to_repo_relative_path(line)
            normalized_lines.append(norm_path)
        return normalized_lines

    def get_input_files(self):
        """Return the list of input files, depending on the parsed \
        command line arguments."""
        if self.__config.from_stdin:
            filepath_lines = sys.stdin.readlines()
            return self.read_filepaths_from_lines(
                self.norm_filepaths(filepath_lines))

        if self.__config.from_list:
            return self.norm_filepaths(self.__config.from_list)

        return self.get_file_diff_from_head_to_merge_base()

    def create_output_producer(self):
        """Create a function to produce the computed output list, depending \
        on the parsed command line arguments.

        If config.to_stdout is True, the created function will print \
        the output to stdout.
        Otherwise, it will write result list of source files to specified \
        output file.

        :return: A function which takes a list of source file paths, \
        and writes them to the defined output.
        """
        def _output_producer_to_stdout(source_paths):
            for source_path in source_paths:
                print(source_path)

        def _output_producer_to_file(source_paths):
            LOGGER.info('project_root = %s', self.__config.project_root)
            list_file_path = path.normpath(
                path.join(self.__config.project_root,
                          self.__config.output_file))
            create_dirs_if_necessary(list_file_path)
            with open_t(list_file_path, mode='w') as list_file:
                list_file.write('\n'.join(source_paths).replace('\\', '/'))
            LOGGER.info('source paths have been written to %s', list_file_path)

            remove_empty_lines_from_file(list_file_path)
            LOGGER.debug('Removed empty lines from output file.')

        return _output_producer_to_stdout if self.__config.to_stdout else (
            _output_producer_to_file)

    def initialize_search_directories(self):
        """Initializes search directories according to the \
        provided script parameters"""
        search_directories = self.__config.code_dirs_file

        if not self.__config.code_dirs_file:
            search_directories = [
                dirs for dirs in next(os.walk(self.__config.project_root))[1]
                if ".git" not in dirs
            ]

        return {path.normpath(search_dir) for search_dir in search_directories}

    def _map_compilation_units_with_headers(self, search_directories,
                                            produce_output):
        LOGGER.info("### MAP COMPILATION UNITS WITH HEADERS ### ")
        input_files = self._get_all_code_file_paths(search_directories,
                                                    self.is_header_code_file)
        mapped_files_dict = self.map_source_files_with_headers(
            input_files, search_directories, self.__config.thirdparty_prefixes)

        export_mapping_report(self.__config.with_mapping_report,
                              mapped_files_dict)

        if self.__config.to_stdout:
            mapped_files_list = []
            for header, compilation_units in mapped_files_dict.items():
                for compilation_unit in compilation_units:
                    mapped_files_list.append("{}, {}".format(
                        header, compilation_unit))
            produce_output(mapped_files_list)

    def _find_compilation_units_for_headers(self, search_directories,
                                            produce_output):
        def _is_in_search_directories(search_dirs):
            def is_in_search_directories(filepath):
                return len([
                    sd_filepath
                    for sd_filepath in search_dirs if sd_filepath in filepath
                ]) > 0

            return is_in_search_directories

        input_files = self.get_input_files()
        LOGGER.info('input files = %s', input_files)
        input_files = set(
            filter(_is_in_search_directories(search_directories), input_files))
        LOGGER.info('input valid files = %s', input_files)

        # Filtering and finding relevant filenames
        input_source_files = set(filter(self.is_source_code_file, input_files))
        input_header_files = list(filter(self.is_header_code_file,
                                         input_files))

        LOGGER.info("### FINDING COMPILATION UNITS FOR HEADERS ### ")
        found_source_files = self.find_sources_for_header_files(
            input_header_files, search_directories,
            self.__config.thirdparty_prefixes)

        LOGGER.info('input source files = %s', input_source_files)
        LOGGER.info('found source files = %s', found_source_files)

        output_source_files = input_source_files | found_source_files
        filtered_output_source_files = [
            source_path for source_path in output_source_files
            if source_path.endswith(self.__config.source_output_extensions)
        ]

        LOGGER.info('output paths = %s', filtered_output_source_files)

        produce_output(filtered_output_source_files)

    def run_find_includes(self):
        """Entrypoint method for FindIncludes class. It does initial \
        configuration and performs actual search"""

        # Precheck and gets data
        self.check_config_parameters()

        if self.__config.blacklist_pattern:
            LOGGER.debug("file_blacklist_pattern set")
            pattern_string = self.__config.blacklist_pattern[0]
            self.__config.file_blacklist_pattern = r"{}".format(pattern_string)
            LOGGER.info("file_blacklist_pattern: {}".format(pattern_string))
        else:
            LOGGER.info("No file_blacklist_pattern specified")
            self.__config.file_blacklist_pattern = ""

        LOGGER.info('third party includes = %s',
                    self.__config.thirdparty_prefixes)

        LOGGER.info('project_root path = %s', self.__config.project_root)

        # By default search the repo dir for folder to search,
        # otherwise use "whitelist"
        search_directories = self.initialize_search_directories()
        LOGGER.info('search directories = %s', search_directories)

        produce_output = self.create_output_producer()

        if self.__config.with_mapping_report:
            self._map_compilation_units_with_headers(search_directories,
                                                     produce_output)
        else:
            self._find_compilation_units_for_headers(search_directories,
                                                     produce_output)


def find_includes_entrypoint(config):
    """
    find_includes entrypoint function

    :param config: configuration represented as an object
    """
    find_includes = FindIncludes(config)
    find_includes.run_find_includes()
