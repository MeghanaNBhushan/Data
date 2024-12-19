# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config_parser_utils.py
# ----------------------------------------------------------------------------
"""Helper functions for the configuration parsers of the SCA helper"""

from os import path
from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t
from swq.common.return_codes import log_and_exit, RC_INVALID_FILEPATH


def _flatten(list_of_lists):
    """Converts a list of lists into a list leaving the empty strings out"""
    return [item for a_list in list_of_lists for item in a_list if item]


def _create_list_of_strings_from_string_or_list(string_or_list_of_strings):
    """Transforms an input string or list of string lines into a single list"""
    result = None

    if isinstance(string_or_list_of_strings, list):
        result = string_or_list_of_strings
    else:
        result = [string_or_list_of_strings]

    return _flatten([a_string.rstrip("\'\"\n").split() for a_string in result])


def _read_list_from_file(filepath):
    """Reads a list from a given filepath"""
    LOGGER.debug('Reading list from file %s', filepath)
    if path.exists(filepath):
        filepaths = open_t(filepath).readlines()
        return _create_list_of_strings_from_string_or_list(filepaths)

    LOGGER.error('Could not read file %s', filepath)
    log_and_exit(RC_INVALID_FILEPATH)

    return None


def create_list_of_elements_from_file_or_list(value):
    """Creates a list of elements from file of list"""
    if value is None:
        return None

    if isinstance(value, list):
        return _create_list_of_strings_from_string_or_list(value)

    if not path.exists(value):
        LOGGER.error('Invalid filepath provided %s', value)

    return _read_list_from_file(value)


def create_list_from_string_or_list(value):
    """Creates a list from string or list"""
    if value is None:
        return None

    if isinstance(value, str):
        return [value]

    return value


def merge_patterns_from_list_and_file(input_file_matching_patterns,
                                      file_matching_patterns):
    """Gets a list of patterns from file (if provided) and a list
    with file matching patterns"""
    merged_file_matching_patterns = []

    if input_file_matching_patterns:
        file_data = create_list_of_elements_from_file_or_list(
            input_file_matching_patterns)
        merged_file_matching_patterns.extend(file_data)

    if file_matching_patterns:
        merged_file_matching_patterns.extend(file_matching_patterns)

    return merged_file_matching_patterns
