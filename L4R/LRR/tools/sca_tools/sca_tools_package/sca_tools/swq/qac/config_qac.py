# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config_qac.py
# ----------------------------------------------------------------------------
"""Shared sca_tools QAC project variables"""

from os import path, environ

from swq.common.logger import LOGGER
from swq.common.config.common_config import CommonConfig, \
    check_if_filepath_exists_and_exit_if_not
from swq.common.config.config_parser_utils import \
    create_list_from_string_or_list
from swq.common.return_codes import RC_QAC_MODULES_NOT_DEFINED, \
    RC_CONFIG_NOT_FOUND, RC_INVALID_FILEPATH, RC_INVALID_PARAMETER, \
    log_and_exit
from swq.common.params.parameter_collector import ParameterCollector

from swq.qac.config.qac_project_creation_config import QACProjectCreationConfig
from swq.qac.config.acf_config_merger import AcfConfigMerger
from swq.qac.config.ncf_config_merger import NcfConfigMerger
from swq.qac.config.rcf_config_merger import RcfConfigMerger
from swq.qac.config.user_messages_config_merger import UserMessagesConfigMerger
from swq.qac.constants import LEVELS, DEFAULT_EXPORT_FORMATS, \
    SYNC_TYPE_VALUES, SCA_TOOL_DIR, EXPORT_DIR
from swq.qac.qac_version import QacVersion
from swq.qac.qac_commands import cli_version, cli_config_folder, \
    git_rev_parse
from swq.qac import finder
from swq.qac.finder import SearchablePath


def create_qac_config(params, args=None):
    """Parse configuration and creates config object"""
    parameter_collector = ParameterCollector(args, params)

    return QACConfig(parameter_collector)


# pylint: disable=too-many-public-methods
class QACConfig(CommonConfig):
    """Class that abstracts the three hierarchical levels of configuration. \
    Read-only access to the variables themselves. \
    This is immutable by design"""
    def __init__(self, parameter_collector: object):
        self._cli_version_string = None
        self._helix_config_path = None
        self._verbose = False
        self._load_environment_variables()
        super().__init__(parameter_collector)
        self._determine_helix_configuration_path()
        self._create_failure_threshold_properties()
        self.__user_messages = None
        self.__acf_file = None
        self.__ncf_file = None
        self.__rcf_file = None
        self._default_helper_logs_path = \
            path.join(self.qac_project_path, SCA_TOOL_DIR, 'logs')
        if self.sync_type and self._subcommand == 'create':
            self.__check_acceptance_of_sync_type_value()
            self.__check_sync_build_log_value()

    def __check_acceptance_of_sync_type_value(self):
        if self.sync_type not in SYNC_TYPE_VALUES:
            LOGGER.error('%s has invalid value: %s',
                         self.get_parameter_name('SYNC_TYPE'), self.sync_type)
            LOGGER.error('Available options are: %s', SYNC_TYPE_VALUES)
            log_and_exit(RC_INVALID_PARAMETER)

    def __check_sync_build_log_value(self):
        if self.sync_type in ['JSON', 'BUILD_LOG']:
            if self.sync_build_log_file is None:
                LOGGER.error('%s is unset',
                             self.get_parameter_name('SYNC_BUILD_LOG_FILE'))
                log_and_exit(RC_INVALID_PARAMETER)

    def _load_environment_variables(self):
        LOGGER.info('Loading Environment Variables')
        self._verbose = bool(environ.get('VERBOSE'))
        LOGGER.info('VERBOSE is: %s', self._verbose)

    def _create_failure_threshold_properties(self):
        """Creates """
        for level in reversed(LEVELS):
            setattr(
                self, f'fail_{str(level)}',
                self._get_parameter_value(
                    f'SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_{str(level)}'))

    def _check_for_helix_installation(self):
        if not path.exists(self.qacli):
            LOGGER.error('QAC executable could not be found in path %s. %s',
                         self.qacli,
                         'Please install it with TCC, iSM or manually.')
            log_and_exit(RC_INVALID_FILEPATH)

    def _determine_helix_configuration_path(self):
        """Determines the helix configuration path based on the QAC version and
        the OS. e.g
            If PRQA and Linux           -> /home/my_username/.config/PRQA.
            If QAC 2019.1 and Windows ->
                    C:\\Users\\my_username_\\AppData\\Local\\Perforce\\2019.1_WIN64
        """
        self._check_for_helix_installation()
        self._cli_version_string = cli_version(self)[0]
        helix_base_path = path.dirname(
            path.dirname(path.normpath(self.qac_bin_path)))
        helix_config_basename = path.basename(helix_base_path)
        LOGGER.debug('helix_base_path = %s\nhelix_config_basename = %s',
                     helix_base_path, helix_config_basename)

        qac_version = QacVersion(self.cli_version_string)
        (major, _) = qac_version.major_minor()
        if qac_version.is_helix() and major >= 2020:
            os_config_folder = path.normpath(
                cli_config_folder(self)[0].split('\n')[-1])
        else:
            os_config_folder = path.normpath(
                cli_config_folder(self)[0].split('=')[1].strip())

        self._helix_config_path = path.join(os_config_folder,
                                            helix_config_basename)

        LOGGER.info('QAC configuration path is %s', self._helix_config_path)

    def _create_searchable_paths(self):
        searchable_filepaths = []
        if self.qac_config_path:
            paths_to_append = self.qac_config_path
            if isinstance(self.qac_config_path, str):
                paths_to_append = [self.qac_config_path]

            searchable_filepaths.extend([
                path.normpath(config_path) for config_path in paths_to_append
                if config_path
            ])

        qac_default_config = path.normpath(
            path.join(self.qac_bin_path, '..', '..', 'config'))
        searchable_filepaths.extend(
            [self._helix_config_path, self.project_root, qac_default_config])

        LOGGER.debug('Searchable filepaths = %s', searchable_filepaths)

        return [
            SearchablePath(searchable_filepath, recursive=False)
            for searchable_filepath in searchable_filepaths
        ]

    def _find_in_searchable_paths(self, filepath, default_relative_path):
        if filepath:
            normalized_filepath = path.normpath(filepath)
            filepaths = [normalized_filepath]
            if default_relative_path:
                filepaths.append(
                    path.join(path.normpath(default_relative_path),
                              normalized_filepath))
            (found, result_filepath) = finder.find_files_in_search_paths(
                filepaths, self._create_searchable_paths())
            LOGGER.debug('Filepath %s found? %s with result %s', filepath,
                         found, result_filepath)
            return result_filepath

        return None

    def _find_config_path(self, filepath, default_relative_path,
                          path_config_name, exit_on_not_found):
        found_filepath = self._find_in_searchable_paths(
            filepath, default_relative_path)

        if filepath is not None and found_filepath is None:
            LOGGER.error('Config %s with filepath %s not found',
                         path_config_name, filepath)
            if exit_on_not_found:
                log_and_exit(RC_CONFIG_NOT_FOUND)

        return found_filepath

    def _find_config_paths(self,
                           path_config_name,
                           default_relative_path,
                           exit_on_not_found=True):
        """Finds a path based on the current configs"""
        def _get_list_of_found_configs(paths_list: list):
            return [
                self._find_config_path(filepath, default_relative_path,
                                       path_config_name, exit_on_not_found)
                for filepath in paths_list
            ]

        filepath_or_list = self._get_parameter_value(path_config_name)

        if isinstance(filepath_or_list, list):
            return _get_list_of_found_configs(filepath_or_list)

        return self._find_config_path(filepath_or_list, default_relative_path,
                                      path_config_name, exit_on_not_found)

    def _qacli_view_csv_filepath(self):
        return path.join(self.qac_project_path, SCA_TOOL_DIR, 'export',
                         'qacli-view.csv')

    def _threshold_html_report_filepath(self):
        return path.join(self.qac_project_path, SCA_TOOL_DIR, 'export',
                         'threshold_warnings_report.html')

    @property
    def acf_file(self):
        """Gets the property acf_file"""
        if not isinstance(self.__acf_file, QACProjectCreationConfig):
            self.__acf_file = QACProjectCreationConfig(
                self._find_config_paths('ACF_FILE', path.join('config',
                                                              'acf')),
                self.custom_config_path, AcfConfigMerger)

        return self.__acf_file

    @property
    def analysis_path(self):
        """Gets the property analysis_path"""
        return path.join(self.helper_logs_path, "analysis")

    @property
    def analyze_file(self):
        """Gets the property analyze_file"""
        return self._get_parameter_value('ANALYZE_FILE')

    @property
    def analysis_filter_filepath(self):
        """Gets the property analysis_filter_filepath"""
        return path.join(self.via_path, 'analysis_filter.via')

    @property
    def analyze_list(self):
        """Gets the property analyze_list"""
        return self._get_final_path_if_config_exists('ANALYZE_LIST')

    @property
    def analyze_params(self):
        """Gets the property analyze_params"""
        return self._get_parameter_value('ANALYZE_PARAMS')

    @property
    def sync_build_command(self):
        """Gets the property sync_build_command"""
        return self._get_parameter_value('SYNC_BUILD_COMMAND')

    @property
    def sync_build_log_file(self):
        """Gets the property sync_build_log_file"""
        return self._get_final_path_if_config_exists('SYNC_BUILD_LOG_FILE')

    @property
    def c_files_analyzed_as_c(self):
        """Gets the property c_files_analyzed_as_c"""
        return self._get_parameter_value('C_FILES_ANALYZED_AS_C', default=True)

    @property
    def cleanup_on_create(self):
        """Gets the property cleanup_on_create"""
        return self._get_parameter_value('CLEANUP_ON_CREATE', default=False)

    @property
    def cli_version_string(self):
        """Gets the property cli_version_string"""
        return self._cli_version_string

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
    def compiler_list(self):
        """Gets the property compiler_list"""
        compiler_list = create_list_from_string_or_list(
            self._get_parameter_value('COMPILER_LIST', default=[]))

        compiler_ccts = [
            (compiler,
             self._find_in_searchable_paths(compiler,
                                            path.join('config', 'cct')))
            for compiler in compiler_list
        ]

        if not all(compiler_ccts):
            LOGGER.error('%s: \n%s\n\n',
                         'CCT list contains invalid configurations',
                         compiler_list)
            log_and_exit(RC_CONFIG_NOT_FOUND)

        return [cct_filepath for _, cct_filepath in compiler_ccts]

    @property
    def custom_config_path(self):
        """Gets the property custom_config_path"""
        return path.join(self.qac_project_path, SCA_TOOL_DIR, 'configuration')

    @property
    def custom_help_path(self):
        """Gets the property custom_help_path"""
        return self._get_final_path_if_config_exists('CUSTOM_HELP_PATH')

    @property
    def datastore_target(self):
        """Gets the property datastore_target"""
        return self._get_parameter_value('DATASTORE_TARGET')

    @property
    def disable_optimization(self):
        """Gets the property datastore_target"""
        return self._get_parameter_value('QAC_DISABLE_OPTIMIZATION',
                                         default=False)

    @property
    def export_path(self):
        """Gets the property export_path"""
        return path.join(self.helper_logs_path, 'export')

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
    def generate_html(self):
        """Gets the property generate_html
        If export_formats contains 'html'
        will enable html generation"""

        return 'html' in self.export_formats

    @property
    def only_last_team(self):
        """Gets the property only_last_team"""
        only_last_team = self._get_parameter_value('ONLY_LAST_TEAM')

        return only_last_team if only_last_team else \
            self._get_parameter_value('GITIGNORE_MAPPING')

    @property
    def help_pages_root_dir(self):
        """Gets the property help_pages_root_dir"""
        return self._get_final_path_if_config_exists('HELP_PAGES_ROOT_DIR')

    @property
    def helper_create_baseline(self):
        """Gets the property helper_create_baseline"""
        return self._get_parameter_value('HELPER_CREATE_BASELINE')

    @property
    def helper_remove_file_list(self):
        """Gets the property helper_remove_file_list"""
        return self._get_final_path_if_config_exists('HELPER_REMOVE_FILE_LIST')

    @property
    def helper_suppress_c_header(self):
        """Gets the property helper_suppress_c_header"""
        return self._get_parameter_value('HELPER_SUPPRESS_C_HEADER')

    @property
    def helper_suppress_file_list_a(self):
        """Gets the property helper_suppress_file_list_a"""
        filepath_or_none = self._get_or_read_list_of_paths(
            'HELPER_SUPPRESS_FILE_LIST_A')
        return filepath_or_none if filepath_or_none else ""

    @property
    def helper_suppress_file_list_s(self):
        """Gets the property helper_suppress_file_list_s"""
        filepath_or_none = self._get_or_read_list_of_paths(
            'HELPER_SUPPRESS_FILE_LIST_S')
        return filepath_or_none if filepath_or_none else ""

    @property
    def input_cl_json(self):
        """Gets the property input_cl_json"""
        return self._get_parameter_value('INPUT_CL_JSON')

    @property
    def license_servers(self):
        """Gets the property license_servers"""
        default_servers = [
            "5065@rb-lic-rlm-prqa2.de.bosch.com",    # >= QAC 9.7
            "5065@rb-lic-rlm-prqa-gl.de.bosch.com",    # <= QAC 9.6
            "5065@rb-lic-rlm-prqa-cc.de.bosch.com"    # QAC++
        ]
        return create_list_from_string_or_list(
            self._get_parameter_value('LICENSE_SERVERS',
                                      default=default_servers))

    @property
    def local_baseline_path(self):
        """Gets the property local_baseline_path"""
        return self._get_final_path_if_config_exists('LOCAL_BASELINE_PATH')

    @property
    def baseline_dirpath(self):
        """Gets the property baseline_dir_path"""
        return self._get_final_path_if_config_exists('LOCAL_BASELINE_PATH')

    @property
    def local_baseline_cache_dir_path(self):
        """Gets the property local_baseline_cache_dir_path"""
        return path.join(self.qac_project_path, "prqa", "configs", "Initial",
                         "output")

    @property
    def local_baseline_cache_filepath(self):
        """Gets the property local_baseline_cache_filepath"""
        return path.join(self.local_baseline_cache_dir_path, 'files.sup')

    @property
    def target_baseline_folder(self):
        """Gets the property target_baseline_folder"""
        return path.join(self.qac_project_path, SCA_TOOL_DIR, EXPORT_DIR,
                         'baseline')

    @property
    def target_baseline_filepath(self):
        """Gets the property target_baseline_filepath"""
        return path.join(self.target_baseline_folder, 'files.sup')

    @property
    def qac_sync_settings_include_path(self):
        """Gets the property qac_sync_settings_include_path """
        return create_list_from_string_or_list(
            self._get_parameter_value('QAC_SYNC_SETTINGS_INCLUDE_PATH',
                                      default=[]))

    @property
    def qac_logging_level(self):
        """Gets the property logging_level"""
        return self._get_parameter_value('QAC_LOGGING_LEVEL', default="ERROR")

    @property
    def qacli(self):
        """Gets the property qacli"""
        return path.join(
            self.qac_bin_path, '{}{}'.format('qacli',
                                             self.platform_command_extension))

    @property
    def qagui(self):
        """Gets the property qagui"""
        return path.join(
            self.qac_bin_path, '{}{}'.format('qagui',
                                             self.platform_command_extension))

    @property
    def qac_home_path(self):
        """Gets qac_home_path - the directory 2 levels up from qac_bin_path)"""
        return path.dirname(path.dirname(self.qac_bin_path))

    @property
    def ncf_file(self):
        """Gets the property ncf_file"""
        if not isinstance(self.__ncf_file, QACProjectCreationConfig):
            self.__ncf_file = QACProjectCreationConfig(
                self._find_config_paths('NCF_FILE', path.join('config',
                                                              'ncf')),
                self.custom_config_path, NcfConfigMerger)

        return self.__ncf_file

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
                LOGGER.warning(
                    'Git operation failed. '
                    'No hash is available: \n%s', str(error))

            return return_value

        return _get_git_hash()

    @property
    def verbose(self):
        """Gets the property verbose"""
        return self._verbose

    @property
    def qac_analysis_path_blacklist(self):
        """Gets the property qac_analysis_path_blacklist"""
        if not self.qac_modules:
            LOGGER.error('QAC modules must be defined to apply analysis '
                         'file filters')
            log_and_exit(RC_QAC_MODULES_NOT_DEFINED)

        path_blacklist = create_list_from_string_or_list(
            self._get_parameter_value('QAC_ANALYSIS_PATH_BLACKLIST',
                                      default=[]))

        return [
            self.get_absolute_path_or_relative_to_project_root(analysis_filter)
            for analysis_filter in path_blacklist
        ]

    @property
    def qac_modules(self):
        """Gets the property qac_modules"""
        return create_list_from_string_or_list(
            self._get_parameter_value('QAC_MODULES', default=[]))

    @property
    def qac_bin_path(self):
        """Gets the property qac_bin_path"""
        check_if_filepath_exists_and_exit_if_not(
            self.get_parameter_name('QAC_BIN_PATH'),
            self._get_final_path_if_config_exists('QAC_BIN_PATH'))
        return self._get_final_path_if_config_exists('QAC_BIN_PATH')

    @property
    def qac_config_path(self):
        """Gets the property qac_config_path"""
        qac_config_paths = create_list_from_string_or_list(
            self._get_parameter_value('QAC_CONFIG_PATH'))

        return [
            self.get_path_relative_to_project_root(qac_config_path)
            for qac_config_path in qac_config_paths
        ] if qac_config_paths else None

    @property
    def qac_log_path(self):
        """Gets the property qac_log_path"""
        return path.join(self._helix_config_path, 'app', 'logs')

    @property
    def qac_project_path(self):
        """Gets the property qac_project_path"""
        return self._get_final_path_if_config_exists('QAC_PROJECT_PATH')

    @property
    def qav_password(self):
        """Gets the property qav_password"""
        return self._get_parameter_value('QAV_PASSWORD')

    @property
    def qav_username(self):
        """Gets the property qav_username"""
        return self._get_parameter_value('QAV_USERNAME')

    @property
    def qav_project_name(self):
        """Gets the property qav_project_name"""
        return self._get_parameter_value('QAV_PROJECT_NAME')

    @property
    def qav_project_snapshot(self):
        """Gets the property qav_project_snapshot"""
        return self._get_parameter_value('QAV_PROJECT_SNAPSHOT')

    @property
    def qav_server_url(self):
        """Gets the property qav_server_url"""
        return self._get_parameter_value('QAV_SERVER_URL')

    @property
    def qav_upload_source(self):
        """Gets the property qav_upload_source"""
        return self._get_parameter_value('QAV_UPLOAD_SOURCE')

    @property
    def helix_config_project_xml_path(self):
        """Gets the property helix_config_project_xml_path"""
        return path.join(self._helix_config_path, 'app',
                         'qa-framework-app.xml')

    @property
    def project_reports_path(self):
        """Gets the property project_reports_path"""
        return path.join(self.qac_project_path, "prqa", "configs", "Initial",
                         "reports")

    @property
    def project_diagnostics_path(self):
        """Gets the property project_diagnostics_path"""
        return path.join(self.qac_project_path, SCA_TOOL_DIR, EXPORT_DIR,
                         'diagnostics_output')

    @property
    def project_sync_path_blacklist(self):
        """Gets the property project_sync_path_blacklist"""
        return create_list_from_string_or_list(
            self._get_parameter_value('QAC_SYNC_PATH_BLACKLIST', default=[]))

    @property
    def reports_path(self):
        """Gets the property reports_path"""
        return path.join(self.qac_project_path, SCA_TOOL_DIR, EXPORT_DIR)

    @property
    def sync_type(self):
        """Gets the property sync_type"""
        return self._get_parameter_value('SYNC_TYPE')

    @property
    def rcf_file(self):
        """Gets the property rcf_file"""
        if not isinstance(self.__rcf_file, QACProjectCreationConfig):
            self.__rcf_file = QACProjectCreationConfig(
                self._find_config_paths('RCF_FILE', path.join('config',
                                                              'rcf')),
                self.custom_config_path, RcfConfigMerger)

        return self.__rcf_file

    @property
    def skip_exit_on_analysis_return_codes(self):
        """Gets the property skip_exit_on_analysis_return_codes"""
        return self._get_parameter_value('SKIP_EXIT_ON_ANALYSIS_RETURN_CODES')

    @property
    def skip_exit_on_build_return_codes(self):
        """Gets the property skip_exit_on_build_return_codes"""
        return create_list_from_string_or_list(
            self._get_parameter_value('SKIP_EXIT_ON_BUILD_RETURN_CODES',
                                      default=[0]))

    @property
    def state_filepath(self):
        """Gets the property state_filepath"""
        return path.join(self.qac_project_path, SCA_TOOL_DIR, EXPORT_DIR,
                         'state.json.zip')

    @property
    def sync_type_json_path_pattern(self):
        """Gets the property sync_type_json_path_pattern"""
        return create_list_from_string_or_list(
            self._get_parameter_value('SYNC_TYPE_JSON_PATH_PATTERN_WHITELIST'))

    @property
    def use_flist(self):
        """Gets the property use_flist"""
        return self.analyze_file != 'no'

    @property
    def use_python_build_shell(self):
        """Gets the property use_python_build_shell"""
        return self._get_parameter_value('USE_PYTHON_BUILD_SHELL')

    @property
    def use_vscode_integration(self):
        """Gets the property use_vscode_integration"""
        return self._get_parameter_value('USE_VSCODE_INTEGRATION')

    @property
    def user_messages(self):
        """Gets the property user_messages"""
        if not isinstance(self.__user_messages, QACProjectCreationConfig):
            self.__user_messages = QACProjectCreationConfig(
                self._find_config_paths(
                    'USER_MESSAGES', path.join('user_library',
                                               'user_messages')),
                self.custom_config_path, UserMessagesConfigMerger)

        return self.__user_messages

    @property
    def vcf_file(self):
        """Gets the property vcf_file"""
        return self._find_config_paths('VCF_FILE', path.join('config', 'vcf'))

    @property
    def via_path(self):
        """Gets the property via_path"""
        return path.join(self.helper_logs_path, 'suppressions')

    @property
    def optimization(self):
        """Gets the property string if an optimization flag is possible"""
        return "--optimize" if QacVersion(
            self._cli_version_string).is_helix() else None

    @property
    def qaview_csv(self):
        """Gets the property qaview_csv"""
        default_value = self._qacli_view_csv_filepath()
        qaview_csv = self._get_parameter_value('QAVIEW_CSV',
                                               default=default_value)
        check_if_filepath_exists_and_exit_if_not(
            self.get_parameter_name('QAVIEW_CSV'), qaview_csv)

        return qaview_csv

    @property
    def ignore_ids(self):
        """Gets ids of specified errors to ignore"""
        return self._get_parameter_value('IGNORE_IDS')

    @property
    def justification_message_regexp(self):
        """Gets regular expression for suppressed justification"""
        return create_list_from_string_or_list(
            self._get_parameter_value('JUSTIFICATION_MESSAGE_REGEXP'))

    @property
    def to_stdout(self):
        """Gets the property to_stdout"""
        return self._get_parameter_value('TO_STDOUT')

    @property
    def filter_report_output_file(self):
        """Gets the property filter_report_output_file"""
        return self._get_parameter_value('FILTER_REPORT_OUTPUT_FILE')

    @property
    def metrics_filter_list(self):
        """Gets the property metrics_filter_list"""
        return create_list_from_string_or_list(
            self._get_parameter_value('METRICS_FILTER_LIST'))

    @property
    def actual_build_log(self):
        """Gets the property actual_build_log. The property is an actual
        build log which is used to sync project. It is obtained from
        SYNC_BUILD_LOG_FILE after applying all specified sync filters"""
        return path.join(self.helper_logs_path, 'build', 'build.log')

    @property
    def actual_sync_json(self):
        """Gets the property actual_sync_json. The property is an actual
        compile_commands.json which is used to sync project.
        It is obtained from SYNC_BUILD_LOG_FILE after applying all specified
        sync filters and/or fix_cl_json"""
        return path.join(self.helper_logs_path, 'build',
                         'compile_commands.json')

    @property
    def actual_analyze_list(self):
        """Gets the property actual_analyze_list. The property is an actual
        analyze list which is used in file based analysis.
        It is obtained from ANALYZE_LIST by removing all the files not existing
        in QAC project"""
        return path.join(self.analysis_path, 'analyze_list.txt')

    @property
    def ignore_validation(self):
        """Gets the property ignore_validation"""
        return self._get_parameter_value('IGNORE_VALIDATION', default=False)

    @property
    def with_analysis(self):
        """Gets the property with_analysis"""
        return self._get_parameter_value('QAC_WITH_ANALYSIS', default=False)

    @property
    def with_metrics(self):
        """Gets the property with_metrics"""
        return self._get_parameter_value('QAC_WITH_METRICS', default=False)

    @property
    def with_summary(self):
        """Gets the property with_summary"""
        return self._get_parameter_value('QAC_WITH_SUMMARY', default=False)

    @property
    def from_state_file(self):
        """Gets the property from_state_file"""
        _from_state_file = self._get_parameter_value('QAC_FROM_STATE_FILE',
                                                     default=False)
        if _from_state_file:
            if type(_from_state_file) is str:
                return _from_state_file

            return self.state_filepath

        return None

    @property
    def with_state_file(self):
        """Gets the property with_state_file"""
        flags_enable_state_generation = [
            self._get_parameter_value('QAC_WITH_STATE_FILE', default=False),
            self.with_analysis, self.with_metrics, self.with_summary
        ]

        return any(flags_enable_state_generation) and not self.from_state_file

    @property
    def with_subdiagnostics(self):
        """Gets the property qac_with_subdiagnostics
        Enables light version of subdiagnostics
        (only origins will be present in analysis report)

        If both flags are provided (with_subdiagnostics and
        with_full_subdiagnostics) with_full_subdiagnostics
        will take precedence"""
        return not self.with_full_subdiagnostics \
            and self._get_parameter_value('QAC_WITH_SUBDIAGNOSTICS',
                                          default=False)

    @property
    def with_full_subdiagnostics(self):
        """Gets the property qac_with_full_subdiagnostics"""
        return self._get_parameter_value('QAC_WITH_FULL_SUBDIAGNOSTICS',
                                         default=False)

    @property
    def max_parallel_workers(self):
        """Gets the property max_parallel_workers"""
        return self._get_parameter_value('MAXIMUM_PARALLEL_WORKERS')

    @property
    def qac_cleanup_diagnostic_output(self):
        """Gets the property qac_cleanup_diagnostic_output"""
        return self._get_parameter_value('QAC_CLEANUP_DIAGNOSTICS_OUTPUT',
                                         default=False)

    @property
    def qac_threshold_warnings_report(self):
        """Gets the property qac_threshold_warnings_report"""
        default_threshold_warnings_report_filepath = \
            self._threshold_html_report_filepath()
        return self._get_parameter_value(
            'QAC_THRESHOLD_WARNINGS_REPORT',
            default=default_threshold_warnings_report_filepath)

    @property
    def qacli_view_extra_args(self):
        """Gets the property qacli_view_extra_args"""
        return self._get_parameter_value(
            'QACLI_VIEW_EXTRA_ARGS', default=[])

    @property
    def qacli_post_create_commands(self):
        """Gets the property qacli_post_create_commands"""
        return self._get_parameter_value(
            'QACLI_POST_CREATE_COMMANDS', default=[])
