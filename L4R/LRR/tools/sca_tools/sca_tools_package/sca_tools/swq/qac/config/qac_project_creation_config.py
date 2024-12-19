# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: qac_project_creation_config.py
# ----------------------------------------------------------------------------
"""Defines QAC project creation configuration"""
from os.path import basename


class QACProjectCreationConfig:
    """Defines QAC project creation configuration class"""
    def __init__(self, input_filepaths, output_folder_path, merger_class):
        if isinstance(input_filepaths, str):
            self.__init_fields(input_filepaths)
        elif isinstance(input_filepaths, list):
            if len(input_filepaths) == 1:
                self.__init_fields(input_filepaths[0])
            else:
                self.__input_filepaths = input_filepaths
                self.__input_filenames_as_string = ",".join(
                    [basename(input_file) for input_file in input_filepaths])
                self.__result_filepath = merger_class(output_folder_path,
                                                      input_filepaths).run()
        else:
            self.__input_filepaths = self.__input_filenames_as_string = \
                self.__result_filepath = None

    def __init_fields(self, input_filepath):
        self.__input_filepaths = input_filepath
        self.__input_filenames_as_string = basename(input_filepath)
        self.__result_filepath = input_filepath

    def get_input_filepaths(self):
        """Gets input configuration files"""
        return self.__input_filepaths

    def get_input_filenames_as_string(self):
        """Gets input configuration files and represents as string"""
        return self.__input_filenames_as_string

    def get_result_filepath(self):
        """Gets merge result configuration files"""
        return self.__result_filepath
