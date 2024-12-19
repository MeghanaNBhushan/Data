# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: filesystem_utils.py
# ----------------------------------------------------------------------------
"""Defines filesystem utils"""
import stat
import re

from os import chmod, listdir, makedirs, path, remove, walk, \
    stat as os_stat

from shutil import copy, rmtree
from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, RC_CONFIG_PARSING_ERROR, \
    RC_PROJECT_DOES_NOT_EXIST, RC_INVALID_FILEPATH


def open_t(filepath,
           mode='r',
           buffering=1,
           encoding='utf-8',
           errors='replace',
           newline=None,
           closefd=True,
           opener=None):
    """Builtin open text decorator that specifies some defaults"""
    valid_opening_modes = {
        'a': 'at',
        'at': 'at',
        'a+': 'a+t',
        'r': 'rt',
        'rt': 'rt',
        'r+': 'r+t',
        'r+t': 'r+t',
        'rw': 'r+t',
        'w': 'wt',
        'wt': 'wt',
        'w+': 'w+t',
        'w+t': 'w+t'
    }

    if mode not in valid_opening_modes:
        LOGGER.error('Invalid opening mode provided: %s', mode)
        log_and_exit(RC_CONFIG_PARSING_ERROR)

    return open(filepath,
                mode=valid_opening_modes[mode],
                buffering=buffering,
                encoding=encoding,
                errors=errors,
                newline=newline,
                closefd=closefd,
                opener=opener)


def open_b(filepath, mode='r', newline=None, closefd=True, opener=None):
    """Builtin open binary decorator that specifies safe defaults"""
    valid_opening_modes = {
        'a': 'ab',
        'ab': 'ab',
        'a+': 'a+b',
        'rb': 'rb',
        'r': 'rb',
        'r+': 'r+b',
        'r+b': 'r+b',
        'rw': 'r+b',
        'w': 'wb',
        'wb': 'wb',
        'w+': 'w+b',
        'w+b': 'w+b'
    }

    if mode not in valid_opening_modes:
        LOGGER.error('Invalid opening mode provided: %s', mode)
        log_and_exit(RC_CONFIG_PARSING_ERROR)

    return open(filepath,
                mode=valid_opening_modes[mode],
                newline=newline,
                closefd=closefd,
                opener=opener)


def safe_delete_dirtree(directory):
    """ Avoids problems as this can be a rather dangerous operation one should
    check if this is not a system file or root of
    user home folder for instance
    """
    filepath_tree_depth = len(directory.split(path.sep))
    system_tree_depth_threshold = 3
    if path.exists(
            directory) and filepath_tree_depth >= system_tree_depth_threshold:
        LOGGER.info('Deleting directory = %s', directory)
        rmtree(directory, ignore_errors=True, onerror=None)
        # Avoids async deletion problems
        max_retries = 32768
        retries = 0
        while path.exists(directory) and retries < max_retries:
            retries += 1


def create_dirs_if_necessary(filepath):
    """ Creates dir by path """
    directory = path.dirname(filepath)
    if not path.exists(directory):
        makedirs(directory)
    return filepath


def normalize_path(project_root, filepath):
    """Workaround for problematic paths"""
    if len(filepath) < 3 or filepath == "C:\\Program":
        return None

    last_three_chars = filepath[-3:]
    if last_three_chars == 'cma':
        return 'cma'
    relpath = filepath
    try:
        relpath = path.relpath(filepath, project_root)
    except ValueError as error:
        LOGGER.error('Normalizing file %s with root %s failed due to %s',
                     filepath, project_root, error)

    return relpath


def check_if_project_exists(project_path):
    """Checks project by path and exists if not exists"""
    if not path.exists(project_path):
        LOGGER.error("Project not found on path %s. Can't continue",
                     project_path)
        log_and_exit(RC_PROJECT_DOES_NOT_EXIST)


def copy_file(src_file, dest_file):
    """Copies file. Creates destination directory if it does not exist"""
    if path.exists(src_file):
        create_dirs_if_necessary(dest_file)
        LOGGER.info("Copying file %s to %s", src_file, dest_file)
        copy(src_file, dest_file)
    else:
        LOGGER.warning("File %s does not exist", src_file)


def copy_files(src_dir, dest_dir):
    """Copies files from src_dir to dest_dir.
       Creates dest_dir if it does not exist"""
    if path.exists(src_dir):
        makedirs(dest_dir, exist_ok=True)
        filelist = listdir(src_dir)
        for filepath in filelist:
            LOGGER.info("Copying file %s", filepath)
            copy(path.join(src_dir, filepath), dest_dir)
    else:
        LOGGER.info("Nothing to copy from %s", src_dir)


def clean_directory(directory, exclude_regex=''):
    """Safely removes files from specified directory"""
    LOGGER.info("Cleaning files in directory %s", directory)
    if path.exists(directory):
        dir_entries = listdir(directory)

        if exclude_regex:
            compiled_regex = re.compile(exclude_regex)
            dir_entries_matched = filter(compiled_regex.match, dir_entries)
            dir_entries = set(dir_entries) - set(dir_entries_matched)

        for entry in dir_entries:
            absolute_path = path.join(directory, entry)
            __safe_remove_file(absolute_path)
    else:
        LOGGER.info("Nothing to clean in the directory %s", directory)


def __safe_remove_file(filepath):
    """Safely removes file"""
    try:
        remove(filepath)
        LOGGER.info('File removed: %s', filepath)
    except IsADirectoryError:
        LOGGER.debug('Skipping %s removal as it is a directory', filepath)
    except (PermissionError, OSError) as error:
        # Windows raises PermissionError on folders removal
        LOGGER.debug('Could not remove file %s due to %s', filepath, error)


def set_executable_permission(filepath):
    """Makes file executable"""
    mode = os_stat(filepath)
    chmod(filepath, mode.st_mode | stat.S_IEXEC)


def check_if_file_exist_and_exit_if_not(filepath):
    """Checks if file exist and exits if not"""
    if not path.exists(filepath):
        LOGGER.error('%s path does not exist', filepath)
        log_and_exit(RC_INVALID_FILEPATH)


def get_files_with_extensions(search_directory, extensions, excludes=None):
    """ Recursive get all files with ending. """
    if isinstance(extensions, list) is False:
        raise TypeError("Parameter 'extensions' is not a list.")

    if excludes is None:
        excludes = []

    matches = []

    for dirpath, _, file_names in walk(search_directory):
        LOGGER.debug(
            'Looking for files with %s extensions in %s', extensions, dirpath)

        for file_name in file_names:
            file_path = path.join(dirpath, file_name)
            extension_matched = any(
                file_name.endswith(ending) for ending in extensions)
            file_excluded = any(
                path.normpath(exclude) in file_path for exclude in excludes)
            if extension_matched and not file_excluded:
                matches.append(file_path)

    return matches
