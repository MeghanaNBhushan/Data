# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	file_utils.py
# ----------------------------------------------------------------------------
"""Defines file utils"""

import json

from hashlib import sha256
from datetime import datetime
from shutil import copyfile
from os import path, remove, replace
from re import compile as re_compile
from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import \
    check_if_file_exist_and_exit_if_not, open_t, open_b, \
    create_dirs_if_necessary
from swq.common.return_codes import log_and_exit, RC_INVALID_FILEPATH, \
    RC_FILE_PARSE_FAILED, RC_HASHSUM_MISMATCH

CL_SPECIFIC_CHARS = ['@<<', '<<']
CHARS_TO_REMOVE = CL_SPECIFIC_CHARS + ['\n', '\r']
READLINES_BUFFER_SIZE = 10240
SHA_EXTENSION = 'sha'


def _copy_metadata_if_exists(source_filepath, target_filepath):
    if path.exists(f'{source_filepath}.{SHA_EXTENSION}'):
        LOGGER.debug('SHA file %s found. Downloading',
                     f'{source_filepath}.{SHA_EXTENSION}')
        copyfile(f'{source_filepath}.{SHA_EXTENSION}',
                 f'{target_filepath}.{SHA_EXTENSION}')


def _remove_local_metadata_if_exists(target_filepath):
    if path.exists(f'{target_filepath}.{SHA_EXTENSION}'):
        LOGGER.debug('Local SHA file found. Removing %s',
                     f'{target_filepath}.{SHA_EXTENSION}')
        remove(f'{target_filepath}.{SHA_EXTENSION}')


def copyfile_with_metadata(source_filepath, target_filepath):
    """Copies file with its metadata"""
    delta_time = datetime.now()

    create_dirs_if_necessary(target_filepath)
    copyfile(source_filepath, target_filepath)
    _remove_local_metadata_if_exists(target_filepath)
    _copy_metadata_if_exists(source_filepath, target_filepath)

    delta_time = datetime.now() - delta_time
    LOGGER.info('Copied %s to %s in %s', source_filepath, target_filepath,
                delta_time)


def remove_empty_strings_from_list(lines):
    """Remove all empty lines from a given list.

    :param lines: List of the lines.
    """

    lines_without_empty_lines = [
        line for line in lines if not line.strip() == ''
    ]

    return lines_without_empty_lines


def remove_empty_lines_from_file(file_path):
    """Remove all empty lines from a given file.

    :param file_path: Path to the file.
    """
    with open_t(file_path) as file_in:
        lines = file_in.readlines()

    lines_without_empty_lines = remove_empty_strings_from_list(lines)

    if lines != lines_without_empty_lines:
        with open_t(file_path, mode='w') as file_out:
            file_out.writelines(lines_without_empty_lines)

        LOGGER.debug('Removed empty lines from file %s', file_path)


def strings_contain_cl_specific_chars(strings):
    """ Checks list of string on special characters """
    for line in strings:
        if any(chars in line.rstrip() for chars in CL_SPECIFIC_CHARS):
            return True

    return False


def file_contains_cl_specific_chars(json_filepath):
    """ Checks JSON file content on special characters """
    with open_t(json_filepath, 'r') as input_file:
        return strings_contain_cl_specific_chars(
            input_file.readlines(READLINES_BUFFER_SIZE))


def load_json_file(json_file, strict=True):
    """ Loads JSON file """
    if not path.exists(json_file):
        LOGGER.error('JSON file could not be found at path %s', json_file)
        log_and_exit(RC_INVALID_FILEPATH)
    with open_t(json_file) as input_file:
        try:
            data = json.load(input_file, strict=strict)
        except ValueError as error:
            LOGGER.error("Failed to load JSON file due to %s", error)
            log_and_exit(RC_FILE_PARSE_FAILED)
    return data


def apply_fix_to_cl_compile_commands(json_filepath):
    """ Fixes cl JSON file """
    LOGGER.info("input_cl_json: %s", str(json_filepath))

    modified_json = []
    json_data = load_json_file(json_filepath, strict=False)
    LOGGER.info("Original JSON length: " + str(len(json_data)))
    for json_item in json_data:
        fixed_command = _remove_cl_specific_chars(json_item['command'])
        fixed_item = _create_compile_commands_json_object(
            json_item['directory'], fixed_command, json_item['file'])
        modified_json.append(fixed_item)

    LOGGER.info("Fixed JSON length: " + str(len(modified_json)))
    return _write_output_fixed_cl_json(json_filepath, modified_json)


def _remove_cl_specific_chars(compile_command):
    fixed_command = compile_command
    for chars in CHARS_TO_REMOVE:
        fixed_command = fixed_command.replace(chars, '')
    return fixed_command


def _create_compile_commands_json_object(directory, compile_command, filepath):
    return {
        "directory": directory,
        "command": compile_command,
        "file": filepath
    }


def _write_output_fixed_cl_json(json_filepath, json_content):
    fixed_cl_json_filepath = "{}.{}".format(json_filepath, "fixed.json")
    with open_t(fixed_cl_json_filepath, mode="wt") as output_file:
        json.dump(json_content,
                  output_file,
                  sort_keys=True,
                  indent=4,
                  ensure_ascii=False)
    LOGGER.info("- done -")
    return fixed_cl_json_filepath


def get_list_of_files_from_compile_commands(json_filepath):
    """ Returns list of files from swq.compile_commands.json """
    json_data = load_json_file(json_filepath, strict=False)

    return [command_json_content['file'] for command_json_content in json_data]


def read_lines_from_file(filepath):
    """Reads file from files without trailing new line"""
    with open_t(filepath, 'r') as file_in:
        return file_in.read().splitlines()


def write_lines_to_file(filepath, content, mode='w'):
    """Writes content to file line by line with trailing new line.
    Creates destination directory if it does not exist"""
    create_dirs_if_necessary(filepath)
    with open_t(filepath, mode) as out_file:
        out_file.writelines("%s\n" % line for line in content)


def get_list_of_files_from_file(filepath):
    """Reads file and returns list of files with forward slashes"""
    return [
        a_file.replace('\\', '/') for a_file in read_lines_from_file(filepath)
    ]


def use_json_sync_filter(sync_type_json_path_pattern,
                         compile_commands_file,
                         output_file=None):
    """Applies filter specified in sync_type_json_path_pattern
    and returns new filepath with filtered commands"""
    _output_file = \
        output_file if output_file else compile_commands_file + ".tmp"
    filtered_json = []

    with open_t(compile_commands_file) as fin:
        data = json.load(fin)
        LOGGER.info("Original JSON length: %s", len(data))

        for pattern_string in sync_type_json_path_pattern:
            LOGGER.info("# using JSON filter: " + pattern_string)
            pattern_regex = re_compile(pattern_string)
            for item in data:
                if pattern_regex.search(item['file']):
                    filtered_json.append(item)
        LOGGER.info("Filtered JSON length: %s", len(filtered_json))
        with open_t(_output_file, mode="wt") as fout:
            json.dump(filtered_json,
                      fout,
                      sort_keys=True,
                      indent=4,
                      ensure_ascii=False)

    return _output_file


def escape_line_breaks_in_string(a_string: str):
    """Escapes all line breaks with double backslash"""
    return a_string.replace('\r', '\\r').replace('\n', '\\n')


def calculate_sha256(filepath):
    """Returns SHA256 hashsum of a given file"""
    check_if_file_exist_and_exit_if_not(filepath)
    sha256_hash = sha256()
    block_size = sha256_hash.block_size
    with open_b(filepath, 'r') as fin:
        block = fin.read(block_size)
        while len(block) > 0:
            sha256_hash.update(block)
            block = fin.read(block_size)

    return sha256_hash.hexdigest()


def write_sha256_to_metadata(filepath):
    """Creates file with SHA_EXTENSION extension with source file's hashsum"""
    LOGGER.info('Calculating hashsum for %s', filepath)
    hashsum = calculate_sha256(filepath)
    write_lines_to_file(f'{filepath}.{SHA_EXTENSION}', [hashsum])


def read_sha256_from_metadata(filepath):
    """Reads hashsum for filepath with SHA_EXTENSION extension"""
    hashsum = None
    if check_if_hashshum_file_exists(filepath):
        with open_t(f'{filepath}.{SHA_EXTENSION}') as fin:
            hashsum = fin.readline().rstrip()
    return hashsum


def hashsum_is_valid_for_file(filepath):
    """Checks whether hashsum is same as in filepath.{SHA_EXTENSION} file"""
    calculated_hashsum = calculate_sha256(filepath)
    LOGGER.debug('Calculated hashsum for %s is %s', filepath,
                 calculated_hashsum)
    hashsum_from_metadata = read_sha256_from_metadata(filepath)
    LOGGER.debug('Hashsum from file %s is %s', f'{filepath}.{SHA_EXTENSION}',
                 hashsum_from_metadata)
    hashsums_equal = calculated_hashsum == hashsum_from_metadata

    if not hashsums_equal:
        LOGGER.warning('Calculated %s and read %s hashsums are different',
                       calculated_hashsum, hashsum_from_metadata)

    return hashsums_equal


def check_if_hashshum_file_exists(filepath):
    """Checks if hashsum file exists"""
    return path.exists(f'{filepath}.{SHA_EXTENSION}')


def check_if_hashshum_file_exists_and_validate(filepath):
    """Runs hashsum validation if hashsum file exists"""
    if check_if_hashshum_file_exists(filepath):
        LOGGER.info('Hashsum file found %s. Baseline validation is enabled',
                    f'{filepath}.{SHA_EXTENSION}')
        check_if_hashsum_is_valid_and_exit_if_not(filepath)
    else:
        LOGGER.info('Hashsum file %s is not found',
                    f'{filepath}.{SHA_EXTENSION}')
        LOGGER.warning(
            'Validation disabled. Baseline consistency cannot be ensured')


def check_if_hashsum_is_valid_and_exit_if_not(filepath):
    """Validates file by its hashsum with additional SHA_EXTENSION extension"""
    if not hashsum_is_valid_for_file(filepath):
        LOGGER.error('Hashsum validation failed for %s', filepath)
        log_and_exit(RC_HASHSUM_MISMATCH)

    LOGGER.info('Hashsum validation succeeded')


def move_file_to_target_folder(source_filepath, target_filepath):
    """Moves source_filepath to target_filepath"""
    LOGGER.info('Moving %s to %s', source_filepath, target_filepath)
    replace(source_filepath, target_filepath)
