# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config_coverity.py
# ----------------------------------------------------------------------------
"""Shared coverity project variables"""

from os import path, environ
from swq.common.logger import LOGGER
from swq.common.config.common_config import CommonConfig, \
    check_if_filepath_exists_and_exit_if_not
from swq.common.constants import SWQ_MODULE_PATH
from swq.common.config.config_parser_utils import \
    merge_patterns_from_list_and_file, create_list_from_string_or_list
from swq.common.params.parameter_collector import ParameterCollector
from swq.coverity.coverity_commands import git_rev_parse
from swq.coverity.coverity_utils import get_filtered_report_name, \
    coverity_version
from swq.coverity.constants import SCA_TOOL_DIR, DEFAULT_EXPORT_FORMATS, \
    EXPORT_DIR


def create_coverity_config(params, args=None):
    """Parse configuration and creates config object"""
    parameter_collector = ParameterCollector(args, params)

    return CoverityConfig(parameter_collector)


class CoverityConfig(CommonConfig):
    """Class that abstracts the three hierarchical levels of configuration. \
    Read-only access to the variables themselves. \
    This is immutable by design"""
    def __init__(self, parameter_collector: object):
        self._load_environment_variables()
        super().__init__(parameter_collector)
        self._default_helper_logs_path = \
            path.join(self.coverity_project_path, SCA_TOOL_DIR, 'logs')
        self._cli_version_string = coverity_version(self)
        self.__coverity_export_dirpath = path.join(self.coverity_project_path,
                                                   SCA_TOOL_DIR, "export")

    def _load_environment_variables(self):
        LOGGER.info('Loading Environment Variables')
        self._verbose = bool(environ.get('VERBOSE'))
        LOGGER.info('VERBOSE is: %s', self._verbose)

    def _preview_report_csv_filepath(self):
        """Gets preview report csv filepath"""
        csv_report_basename = path.splitext(
            self.preview_report_json_filepath)[0]
        if self.translation_units_blacklist:
            csv_report_dirpath = path.dirname(
                self.preview_report_json_filepath)
            csv_report_filepath = path.join(
                csv_report_dirpath, "{}-export.csv".format(
                    get_filtered_report_name(csv_report_basename)))
        else:
            csv_report_filepath = "{}-export.csv".format(csv_report_basename)
        return csv_report_filepath

    @property
    def auth_key_filepath(self):
        """Gets the property auth_key_filepath"""
        auth_key_file_path = self._get_final_path_if_config_exists(
            'COVERITY_AUTH_KEY_FILEPATH')

        if auth_key_file_path:
            check_if_filepath_exists_and_exit_if_not(
                self.get_parameter_name('COVERITY_AUTH_KEY_FILEPATH'),
                auth_key_file_path)

        return auth_key_file_path

    @property
    def cov_build_option_list(self):
        """Gets the property cov_build_option_list"""
        return create_list_from_string_or_list(
            self._get_parameter_value('COV_BUILD_OPTION_LIST'))

    @property
    def cov_analyze_option_list(self):
        """Gets the property cov_analyze_option_list"""
        return create_list_from_string_or_list(
            self._get_parameter_value('COV_ANALYZE_OPTION_LIST'))

    @property
    def translation_units_blacklist(self):
        """Gets the property translation_units_blacklist"""
        return create_list_from_string_or_list(
            self._get_parameter_value('TRANSLATION_UNITS_BLACKLIST'))

    @property
    def cov_export_blacklist(self):
        """Gets the property cov_export_blacklist"""
        return self._get_parameter_value('COV_EXPORT_BLACKLIST')

    @property
    def cov_export_whitelist(self):
        """Gets the property cov_export_whitelist"""
        return self._get_parameter_value('COV_EXPORT_WHITELIST')

    @property
    def coverity_commit_url(self):
        """Gets the property coverity_commit_url"""
        return self._get_parameter_value('COVERITY_COMMIT_URL')

    @property
    def coverity_commit_host(self):
        """Gets the property coverity_commit_host"""
        return self._get_parameter_value('COVERITY_COMMIT_HOST')

    @property
    def coverity_commit_dataport(self):
        """Gets the property coverity_commit_dataport"""
        return self._get_parameter_value('COVERITY_COMMIT_DATAPORT')

    @property
    def coverity_commit_stream(self):
        """Gets the property coverity_commit_stream"""
        return self._get_parameter_value('COVERITY_COMMIT_STREAM')

    @property
    def coverity_auth_key_file(self):
        """Gets the property coverity_auth_key_file"""
        return self._get_parameter_value('COVERITY_AUTH_KEY_FILE')

    @property
    def build_command(self):
        """Gets the property build_command"""
        return self._get_parameter_value('BUILD_COMMAND')

    @property
    def compiler_list(self):
        """Gets the property compiler_list"""
        return create_list_from_string_or_list(
            self._get_parameter_value('COMPILER_LIST'))

    @property
    def datastore_target(self):
        """Gets the property datastore_target"""
        return self._get_parameter_value('DATASTORE_TARGET')

    @property
    def project_git_commit(self):
        """Gets the property project_git_commit"""
        def _get_git_hash():
            return_value = 'unknown'

            try:
                git_cmd_out, return_code = git_rev_parse(self)
                if return_code == 0:
                    return_value = git_cmd_out
            except FileNotFoundError as error:
                LOGGER.warning('Git operation failed. '
                               'No hash is available: \n%s',
                               str(error))

            return return_value

        return _get_git_hash()

    @property
    def verbose(self):
        """Gets the property verbose"""
        return self._verbose

    @property
    def coverity_project_path(self):
        """Gets the property coverity_project_path"""
        return self._get_final_path_if_config_exists('COVERITY_PROJECT_PATH')

    @property
    def coverity_bin_path(self):
        """Gets the property coverity_bin_path"""
        check_if_filepath_exists_and_exit_if_not(
            self.get_parameter_name('COVERITY_BIN_PATH'),
            self._get_final_path_if_config_exists('COVERITY_BIN_PATH'))
        return self._get_parameter_value('COVERITY_BIN_PATH')

    @property
    def skip_exit_on_error(self):
        """Gets the property skip_exit_on_error"""
        return self._get_parameter_value('SKIP_EXIT_ON_ERROR')

    @property
    def export_formats(self):
        """Gets the property export_formats.
        If 'all' is included it will be replaced
        with DEFAULT_EXPORT_FORMATS"""
        export_formats = create_list_from_string_or_list(
            self._get_parameter_value('EXPORT_FORMATS', default=['all']))

        if 'all' in export_formats:
            export_formats.remove('all')
            export_formats.extend(DEFAULT_EXPORT_FORMATS)

        return set(export_formats)

    @property
    def include_triage_history(self):
        """Gets the property include_triage_history"""
        return self._get_parameter_value('INCLUDE_TRIAGE_HISTORY')

    @property
    def triage_store(self):
        """Gets the property triage_store"""
        return self._get_parameter_value('TRIAGE_STORE')

    @property
    def webapi_url(self):
        """Gets the property webapi_url"""
        return self._get_parameter_value('WEBAPI_URL')

    @property
    def webapi_project_name(self):
        """Gets the property webapi_project_name"""
        return self._get_parameter_value('WEBAPI_PROJECT_NAME')

    @property
    def webapi_view_name(self):
        """Gets the property webapi_view_name"""
        return self._get_parameter_value('WEBAPI_VIEW_NAME')

    @property
    def webapi_coverity_user(self):
        """Gets the property webapi_coverity_user"""
        return self._get_parameter_value('COVERITY_USERNAME')

    @property
    def webapi_coverity_passcode(self):
        """Gets the property webapi_coverity_passcode"""
        return self._get_parameter_value('COVERITY_PASSWORD')

    @property
    def cov_errors_json_filepath(self):
        """Gets the property cov_errors_json_filepath"""
        return path.join(self.__coverity_export_dirpath, "cov-format-errors",
                         "json-output.json")

    @property
    def cov_errors_html_dirpath(self):
        """Gets the property cov_errors_html_dirpath"""
        return path.join(self.__coverity_export_dirpath, 'cov-format-errors',
                         'html')

    @property
    def preview_report_json_filepath(self):
        """Gets the property preview_report_json_filepath"""
        return path.join(self.__coverity_export_dirpath, "cov_commit_defects",
                         "preview-report.json")

    @property
    def state_filepath(self):
        """Gets the property state_filepath"""
        return path.join(self.coverity_project_path, SCA_TOOL_DIR,
                         'state.json.zip')

    @property
    def view_contents_export_filepath(self):
        """Gets the property view_contents_export_filepath"""
        return path.join(
            self.__coverity_export_dirpath, "viewContentsV1",
            "viewContentsV1_{}.json".format(self.webapi_view_name))

    @property
    def with_cid(self):
        """Gets the property with_cid"""
        return self._get_parameter_value('WITH_CID')

    @property
    def preview_report_csv(self):
        """Gets the property preview_report_csv"""
        default_value = self._preview_report_csv_filepath()
        return self._get_parameter_value('PREVIEW_REPORT_CSV',
                                         default=default_value)

    @property
    def filter_report_output_file(self):
        """Gets the property filter_report_output_file"""
        return self._get_parameter_value('FILTER_REPORT_OUTPUT_FILE')

    @property
    def compile_commands_json(self):
        """Gets the property compile_commands_json"""
        return self._get_final_path_if_config_exists('COMPILE_COMMANDS_JSON')

    @property
    def file_matching_patterns(self):
        """Gets the property file_matching_patterns"""
        return create_list_from_string_or_list(
            self._get_parameter_value('FILE_MATCHING_PATTERNS'))

    @property
    def input_file_matching_patterns(self):
        """Gets the property input_file_matching_patterns"""
        return self._get_parameter_value('INPUT_FILE_MATCHING_PATTERNS')

    @property
    def merged_file_matching_patterns(self):
        """Gets the list of file matching patterns generated in
        _merge_patterns_from_list_and_file method"""
        return merge_patterns_from_list_and_file(
            self.input_file_matching_patterns, self.file_matching_patterns)

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
    def only_last_team(self):
        """Gets the property only_last_team"""
        only_last_team = self._get_parameter_value('ONLY_LAST_TEAM')
        return only_last_team if only_last_team else \
            self._get_parameter_value('GITIGNORE_MAPPING')

    @property
    def compile_commands_build_command(self):
        """Gets the property compile_commands_build_command"""
        return self._get_parameter_value('COMPILE_COMMANDS_BUILD_COMMAND')

    @property
    def use_compile_commands_json(self):
        """Gets the property use_compile_commands_json"""
        return self._get_parameter_value('USE_COMPILE_COMMANDS_JSON')

    @property
    def script_location(self):
        """Gets the property script_location"""
        return path.normpath(
            '{}/common/compiler.py'.format(SWQ_MODULE_PATH.absolute()))

    @property
    def max_parallel_workers(self):
        """Gets the property max_parallel_workers"""
        return self._get_parameter_value('MAXIMUM_PARALLEL_WORKERS')

    @property
    def cli_version_string(self):
        """Gets the version string from Coverity CLI"""
        return self._cli_version_string

    @property
    def with_native_html_report(self):
        """Gets the property with_native_html_report"""
        return self._get_parameter_value(
            'COVERITY_WITH_NATIVE_HTML_REPORT', default=False)

    @property
    def reports_path(self):
        """Gets the property reports_path"""
        return path.join(self.coverity_project_path, SCA_TOOL_DIR, EXPORT_DIR)

    @property
    def coverity_config_filepath(self):
        """Gets the property coverity_config_filepath"""
        filepath = \
            self._get_parameter_value('COVERITY_CONFIG_FILEPATH', default='')

        return self.get_absolute_path_or_relative_to_project_root(
            filepath) if filepath else ''

    @property
    def run_desktop_extra_options(self):
        """Gets the property coverity_run_desktop_extra_options"""
        return self._get_parameter_value(
            'COVERITY_RUN_DESKTOP_EXTRA_OPTIONS', default=[])
