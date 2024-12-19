# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	config_merger.py
# ----------------------------------------------------------------------------
"""Defines QAC project configuration files merger"""
from os import path
from abc import ABC, abstractmethod

from swq.common.logger import LOGGER


class ConfigMerger(ABC):
    """Defines a configuration merger abstract base class"""

    _merged_filename = ''

    def __init__(self, output_folder_path: str, input_config_files: list):
        self._output_folder_path = output_folder_path
        self._input_config_files = input_config_files
        self._output_filepath = path.join(self._output_folder_path,
                                          self._merged_filename)

    @abstractmethod
    def _write_output_file(self, output_file_content: str):
        """Writes merged content to an output file"""

    def run(self):
        """Merges content of configuration files and writes into new file"""
        LOGGER.info('Merge the following files: %s', self._input_config_files)
        parsed_content = self._parse_content()
        output_file_content = self.merge_contents(parsed_content)
        self._write_output_file(output_file_content)

        return self._output_filepath

    @abstractmethod
    def _parse_content(self):
        """Parses content of input files"""

    @abstractmethod
    def merge_contents(self, parsed_content: list):
        """Method for merging functionality"""
