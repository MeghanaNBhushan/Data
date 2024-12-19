# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	finder.py
# ----------------------------------------------------------------------------
"""Provides file finding capabilities"""

from os import path
from typing import List
import os


class SearchablePath:
    """Defines a path that can be used for searching"""
    def __init__(self, search_filepath: str, recursive: bool):
        self._search_filepath = path.normpath(search_filepath)
        self._recursive = recursive

    @property
    def search_filepath(self) -> str:
        """A base search filepath"""
        return self._search_filepath

    @property
    def is_recursive(self) -> bool:
        """Defines wether the search from a given path should be recursive or
        not"""
        return self._recursive


def _file_exists_in_searchable_path(filename: str,
                                    searchable_path: SearchablePath):
    search_final_path = path.join(searchable_path.search_filepath, filename)
    if path.exists(search_final_path):
        return (True, search_final_path)

    if searchable_path.is_recursive:
        subdirs = [
            path.join(searchable_path.search_filepath, file_in_dir)
            for file_in_dir in os.listdir(searchable_path.search_filepath)
            if path.isdir(
                path.join(searchable_path.search_filepath, file_in_dir))
        ]

        subdirs_scan = [
            _file_exists_in_searchable_path(
                filename, SearchablePath(subdir, recursive=True))
            for subdir in subdirs
        ]

        for found, subdir_search_final_path in subdirs_scan:
            if found:
                return (True, subdir_search_final_path)

    return (False, None)


def find_file_in_search_paths(
        search_filepath: str,
        searchable_paths: List[SearchablePath]) -> (bool, str):
    """Finds a given file in the given searchable paths"""
    normalized_search_filepath = path.normpath(search_filepath)
    for searchable_path in searchable_paths:
        (found, filepath) = _file_exists_in_searchable_path(
            normalized_search_filepath, searchable_path)
        if found:
            return (True, filepath)

    return (False, None)


def find_files_in_search_paths(
        search_filepaths: List[str],
        searchable_paths: List[SearchablePath]) -> (bool, str):
    """Finds a given files in the given searchable paths"""
    searched_files = [
        find_file_in_search_paths(search_filepath, searchable_paths)
        for search_filepath in search_filepaths
    ]

    for found, filepath in searched_files:
        if found:
            return (True, filepath)

    return (False, None)
