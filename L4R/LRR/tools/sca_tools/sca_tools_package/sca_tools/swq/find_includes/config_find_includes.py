# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config_find_includes.py
# ----------------------------------------------------------------------------
"""Shared find_includes project variables"""

from swq.common.logger import LOGGER
from swq.common.config.common_config import CommonConfig
from swq.common.config.config_parser_utils import \
    create_list_from_string_or_list
from swq.common.params.parameter_collector import ParameterCollector
from swq.common.return_codes import log_and_exit, RC_INVALID_PARAMETER

_FIND_INCLUDE_STRATEGY_VALUES = ['all', 'minimal']


def create_find_includes_config(params, args=None):
    """Parse configuration and creates config object"""
    parameter_collector = ParameterCollector(args, params)

    return FIConfig(parameter_collector)


class FIConfig(CommonConfig):
    """Class that abstracts the three hierarchical levels of configuration. \
    Read-only access to the variables themselves. \
    This is immutable by design"""
    def __init__(self, parameter_collector: object):
        super().__init__(parameter_collector)
        self.__check_acceptance_of_find_include_strategy_value()

    def __check_acceptance_of_find_include_strategy_value(self):
        if self.find_include_strategy not in _FIND_INCLUDE_STRATEGY_VALUES:
            LOGGER.error('%s has invalid value: %s',
                         self.get_parameter_name('FIND_INCLUDE_STRATEGY'),
                         self.find_include_strategy)
            LOGGER.error('Available options are: %s',
                         _FIND_INCLUDE_STRATEGY_VALUES)
            log_and_exit(RC_INVALID_PARAMETER)

    @property
    def datastore_target(self):
        """Gets the property datastore_target"""
        return self._get_parameter_value('DATASTORE_TARGET')

    @property
    def from_list(self):
        """Gets the property from_list"""
        return self._get_or_read_list_of_paths('FROM_LIST')

    @property
    def output_file(self):
        """Gets the property output_file"""
        return self._get_parameter_value('OUTPUT_FILE')

    @property
    def find_include_strategy(self):
        """Gets the property find_include_strategy"""
        return self._get_parameter_value('FIND_INCLUDE_STRATEGY',
                                         default='all')

    @property
    def git_diff_filter(self):
        """Gets the property git_diff_filter"""
        return self._get_parameter_value('FIND_INCLUDES_GIT_DIFF_FILTER',
                                         default='rd')

    @property
    def merge_base(self):
        """Gets the property merge_base"""
        return self._get_parameter_value('MERGE_BASE',
                                         default="origin/develop")

    @property
    def code_dirs_file(self):
        """Gets the property code_dirs_file"""
        return self._get_or_read_list_of_paths('CODE_DIRS_FILE')

    @property
    def thirdparty_prefixes(self):
        """Gets the property thirdparty_prefixes"""
        thirdparty_prefixes = self._get_or_read_list_of_paths(
            'THIRDPARTY_PREFIXES')

        return thirdparty_prefixes if thirdparty_prefixes else []

    @property
    def blacklist_pattern(self):
        """Gets the property blacklist_pattern"""
        return self._get_or_read_list_of_paths('BLACKLIST_PATTERN')

    @property
    def header_extensions(self):
        """Gets the property header_extensions"""
        return create_list_from_string_or_list(
            self._get_parameter_value('HEADER_EXTENSIONS',
                                      default=[".hpp", ".h", ".inl"]))

    @property
    def source_extensions(self):
        """Gets the property source_extensions"""
        return create_list_from_string_or_list(
            self._get_parameter_value('SOURCE_EXTENSIONS',
                                      default=[".cpp", ".c", ".inl"]))

    @property
    def source_output_extensions(self):
        """Gets the property source_output_extensions"""
        output_extensions = create_list_from_string_or_list(
            self._get_parameter_value('SOURCE_OUTPUT_EXTENSIONS',
                                      default=(".cpp", ".c")))

        return output_extensions if output_extensions is tuple else tuple(
            output_extensions)

    @property
    def with_mapping_report(self):
        """Gets the property with_mapping_report"""
        filepath = self._get_parameter_value('WITH_MAPPING_REPORT')

        return self.get_path_relative_to_project_root(
            filepath) if filepath else None

    @property
    def from_stdin(self):
        """Gets the property from_stdin"""
        return self._get_parameter_value('FROM_STDIN')

    @property
    def to_stdout(self):
        """Gets the property to_stdout"""
        return self._get_parameter_value('TO_STDOUT', default=True) \
            if not self.output_file else False
