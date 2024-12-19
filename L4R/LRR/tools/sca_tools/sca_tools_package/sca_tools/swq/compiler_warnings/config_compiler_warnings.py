# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config_compiler_warnings.py
# ----------------------------------------------------------------------------
"""Shared compiler_warnings project variables"""

from swq.common.logger import LOGGER
from swq.common.config.common_config import CommonConfig, \
    check_if_filepath_exists_and_exit_if_not
from swq.common.config.config_parser_utils \
    import create_list_from_string_or_list
from swq.common.params.parameter_collector import ParameterCollector

from swq.common.return_codes import log_and_exit, RC_INVALID_PARAMETER

CW_COMPILER_VALUES = ['clang', 'greenhills', 'msvc']
CW_EXPORT_FORMATS = ['xlsx', 'csv', 'json']


def create_compiler_warnings_config(params, args=None):
    """Parse configuration and creates config object"""
    parameter_collector = ParameterCollector(args, params)

    return CompilerWarningsConfig(parameter_collector)


class CompilerWarningsConfig(CommonConfig):
    """Class that abstracts the three hierarchical levels of configuration. \
    Read-only access to the variables themselves. \
    This is immutable by design"""
    def __init__(self, parameter_collector: object):
        super().__init__(parameter_collector)
        self.__check_acceptance_of_cw_compiler_value()

    def __check_acceptance_of_cw_compiler_value(self):
        if self.compiler not in CW_COMPILER_VALUES:
            LOGGER.error('%s has invalid value: %s',
                         self.get_parameter_name('COMPILER'), self.compiler)
            LOGGER.error('Available options are: %s', CW_COMPILER_VALUES)
            log_and_exit(RC_INVALID_PARAMETER)

    @property
    def black_list(self):
        """Gets the property black_list"""
        black_lists = create_list_from_string_or_list(
            self._get_parameter_value('BLACK_LIST'))
        if black_lists:
            for file in black_lists:
                check_if_filepath_exists_and_exit_if_not(
                    self.get_parameter_name('BLACK_LIST'), file)
        return black_lists

    @property
    def changed_files(self):
        """Gets the property changed_files"""
        changed_files = create_list_from_string_or_list(
            self._get_parameter_value('CHANGED_FILES'))

        if changed_files:
            for file in changed_files:
                check_if_filepath_exists_and_exit_if_not(
                    self.get_parameter_name('CHANGED_FILES'), file)
        return changed_files

    @property
    def codeowners_file(self):
        """Gets the property codeowners_file"""
        filepaths = create_list_from_string_or_list(
            self._get_parameter_value('CODEOWNERS_FILE'))

        return [
            self.get_path_relative_to_project_root(filepath)
            for filepath in filepaths
        ] if filepaths else None

    @property
    def compiler(self):
        """Gets the property compiler"""
        return self._get_parameter_value('COMPILER')

    @property
    def compiler_log(self):
        """Gets the property compiler_log"""
        compiler_log = self._get_parameter_value('COMPILER_LOG')
        check_if_filepath_exists_and_exit_if_not(
            self.get_parameter_name('COMPILER_LOG'), compiler_log)
        return compiler_log

    @property
    def export_formats(self):
        """Gets the property export_formats.
        If 'all' is included it will be replaced
        with CW_EXPORT_FORMATS"""
        export_formats = create_list_from_string_or_list(
            self._get_parameter_value('EXPORT_FORMATS', default=['all']))

        if 'all' in export_formats:
            export_formats.remove('all')
            export_formats.extend(CW_EXPORT_FORMATS)

        return set(export_formats)

    @property
    def gitignore_mapping(self):
        """Gets the property gitignore_mapping"""
        return self._get_parameter_value('GITIGNORE_MAPPING')

    @property
    def jobs(self):
        """Gets the property jobs"""
        return self._get_parameter_value('JOBS', default=4)

    @property
    def mapping_column(self):
        """Gets the property mapping_column"""
        return self._get_parameter_value('COMPILER_WARNINGS_MAPPING_COLUMN',
                                         default='File path')

    @property
    def only_last_team(self):
        """Gets the property only_last_team"""
        only_last_team = self._get_parameter_value('ONLY_LAST_TEAM')
        return only_last_team if only_last_team else \
            self._get_parameter_value('GITIGNORE_MAPPING')

    @property
    def output(self):
        """Gets the property output"""
        return self._get_parameter_value('OUTPUT')

    @property
    def quiet(self):
        """Gets the property output"""
        return self._get_parameter_value('QUIET')

    @property
    def report_basename(self):
        """Gets the property report_basename"""
        return self._get_parameter_value(
            'COMPILER_WARNINGS_REPORT_BASENAME',
            default=f'compiler_warnings_{self.compiler}')

    @property
    def report_dir(self):
        """Gets the property report_dir"""
        return self.get_absolute_path_or_relative_to_project_root(
            self._get_parameter_value('COMPILER_WARNINGS_REPORT_DIR',
                                      default='reports/compiler_warnings'))

    @property
    def target_directory(self):
        """Gets the property target_directory"""
        return create_list_from_string_or_list(
            self._get_parameter_value('TARGET_DIRECTORY'))

    @property
    def threshold(self):
        """Gets the property threshold"""
        return self._get_parameter_value('THRESHOLD')

    @property
    def threshold_file(self):
        """Gets the property threshold_file"""
        threshold_file = self._get_parameter_value('THRESHOLD_FILE')
        if threshold_file:
            check_if_filepath_exists_and_exit_if_not(
                self.get_parameter_name('THRESHOLD_FILE'), threshold_file)
        return threshold_file

    @property
    def types_db(self):
        """Gets the property types_db"""
        types_db_file = self._get_parameter_value('TYPES_DB')
        if types_db_file:
            check_if_filepath_exists_and_exit_if_not(
                self.get_parameter_name('TYPES_DB'), types_db_file)
        return types_db_file

    @property
    def use_relative_paths(self):
        """Gets the property use_relative_paths"""
        return self._get_parameter_value('USE_RELATIVE_PATHS', default=False)
