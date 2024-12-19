# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: common_config.py
# ----------------------------------------------------------------------------
"""Shared SCA project variables"""

from os import path, getcwd

from swq.common.constants import IS_WINDOWS
from swq.common.config.config_parser_utils import \
    create_list_of_elements_from_file_or_list, \
    create_list_from_string_or_list
from swq.common.return_codes import log_and_exit, RC_INVALID_FILEPATH
from swq.common.logger import LOGGER


def check_if_filepath_exists_and_exit_if_not(parameter_name, file_path):
    """Checks filepath exists and exit if not"""
    if not path.exists(file_path):
        LOGGER.error(
            'Path %s does not exist. Please provide'
            ' correct value for %s. Exiting', file_path,
            parameter_name.upper())
        log_and_exit(RC_INVALID_FILEPATH)


def _capitalize_path_if_windows(file_path):
    if IS_WINDOWS and path.isabs(file_path):
        drive, tail = path.splitdrive(file_path)

        if drive.islower():
            capitalized_path = drive.upper() + tail
            return capitalized_path

    return file_path


class CommonConfig:
    """Class that abstracts the three hierarchical levels of configuration. \
    Read-only access to the variables themselves. \
    This is immutable by design"""
    def __init__(self, parameter_collector):
        self._parameter_collector = parameter_collector
        self._subcommand = self._parameter_collector.get_subcommand()
        self.__project_root = _capitalize_path_if_windows(
            path.normpath(
                self._get_parameter_value('PROJECT_ROOT', default=getcwd())))
        self._default_helper_logs_path = getcwd()
        self._check_for_project_root()

    def get_parameter_name(self, parameter):
        """Gets config name in upper case"""
        return self._parameter_collector.get_parameter_name(parameter).upper()

    def _get_parameter_value(self, parameter_name, default=None):
        return getattr(self._parameter_collector, parameter_name, default)

    def _check_for_project_root(self):
        check_if_filepath_exists_and_exit_if_not(
            self.get_parameter_name('PROJECT_ROOT'), self.__project_root)

    def get_absolute_path_or_relative_to_project_root(self, config_path):
        """Gets an absolute path from a relative or just return
        the original path if the input is already absolute"""
        config_path = path.normpath(config_path)

        return config_path if path.isabs(config_path) else path.join(
            self.project_root, config_path)

    def _get_final_path_if_single_value_or_list_if_list(self, config_name):
        config_value = self._get_parameter_value(config_name)

        if isinstance(config_value, list):
            return config_value

        return self.get_absolute_path_or_relative_to_project_root(
            config_value) if config_value else None

    def _get_final_path_if_config_exists(self, path_config_name):
        config_path = self._get_parameter_value(path_config_name)
        return self.get_absolute_path_or_relative_to_project_root(
            config_path) if config_path else None

    def _get_or_read_list_of_paths(self, config_name):
        config_value = self._get_final_path_if_single_value_or_list_if_list(
            config_name)
        return create_list_of_elements_from_file_or_list(config_value)

    def get_path_relative_to_project_root(self, filepath):
        """Gets relative path to the project_root"""
        resolved_filepath = \
            self.get_absolute_path_or_relative_to_project_root(
                path.normpath(filepath)
            )
        LOGGER.debug(
            'Getting relative path to the project root for '
            'filepath = %s resolved_filepath = %s', filepath,
            resolved_filepath)

        return resolved_filepath

    @property
    def platform_command_extension(self):
        """Gets the property platform_command_extension"""
        return '.exe' if IS_WINDOWS else ''

    @property
    def datastore_path(self):
        """Gets the property datastore_path"""
        filepaths = create_list_from_string_or_list(
            self._get_parameter_value('DATASTORE_PATH'))

        return [
            self.get_path_relative_to_project_root(filepath)
            for filepath in filepaths
        ]

    @property
    def project_root(self):
        """Gets the property project_root and checks that path exists"""
        return self.__project_root

    @property
    def helper_logs_path(self):
        """Gets the property helper_logs_path"""
        filepath = self._get_parameter_value(
            'HELPER_LOGS_PATH', default=self._default_helper_logs_path)

        return self.get_path_relative_to_project_root(filepath)

    @property
    def commandline_config(self):
        """Gets the property commandline_config"""
        return self._parameter_collector.get_commandline_config()

    @property
    def env_config(self):
        """Gets the property env_config"""
        return self._parameter_collector.get_env_config()

    @property
    def general_config(self):
        """Gets the property general_config"""
        return self._parameter_collector.get_general_config()

    @property
    def target_config(self):
        """Gets the property target_config"""
        return self._parameter_collector.get_target_config()

    @property
    def merged_config(self):
        """Gets the property merged_config"""
        return self._parameter_collector.get_merged_config()
