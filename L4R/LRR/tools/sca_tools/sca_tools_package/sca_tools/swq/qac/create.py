# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: create.py
# ----------------------------------------------------------------------------
"""Defines methods for qac create sumbcommand"""

from os import makedirs, path as os_path, walk as os_walk
from swq.common.constants import LOGS_PREFIX

from swq.common.filesystem.filesystem_utils import \
    clean_directory, copy_file, open_t, safe_delete_dirtree
from swq.common.logger import LOGGER
from swq.common.file.file_utils import \
    check_if_hashshum_file_exists_and_validate as validate_baseline_file
from swq.common.return_codes import \
    check_return_code_for_cmd_and_exit_if_failed
from swq.qac import qac_commands
from swq.qac.constants import BASELINE_FILE_NAME, EXPORT_DIR, SCA_TOOL_DIR
from swq.qac.custom_help import set_bosch_custom_help, set_builtin_qac_help, \
    set_component_path_in_xml, set_help_path_in_rcf, \
    set_help_path_in_user_messages
from swq.qac.file_transfer import \
    retrieve_file_from_remote_resource
from swq.qac.license_checker import ensure_license_servers_configured
from swq.qac.populate import filter_project_populating_input_file, \
    generate_project_populating_input_file, populate_files_to_qac_project
from swq.qac.qac_utils import get_module_toolchain, \
    verify_components_compatibility
from swq.qac.suppress import suppress_c_header, \
    suppress_file_in_static_list_a


def qac_create(config):
    """Entrypoint for `qac create` subcommand"""
    configure_qac_software(config)
    prepare_directory_tree(config)

    verify_components_compatibility(config)
    ensure_configuration_file_exists(config)
    link_help_pages_to_warnings(config)

    retrieve_validate_baseline_file(config)

    generate_project_populating_input_file(config)
    filter_project_populating_input_file(config)

    create_qac_project(config)
    run_post_create_qacli_commands(config)
    configure_qac_project(config)

    populate_files_to_qac_project(config)

    configure_files_suppression(config)
    remove_files_from_qac_project(config)


def run_post_create_qacli_commands(config):
    """Runs commands defined in QACLI_POST_CREATE_COMMANDS parameter"""
    if config.qacli_post_create_commands:
        LOGGER.info(
            'Configuring QAC project using commands from %s',
            config.get_parameter_name('QACLI_POST_CREATE_COMMANDS'))

        for command in config.qacli_post_create_commands:
            [_, return_code] = qac_commands.run_qacli_command(config, command)
            check_return_code_for_cmd_and_exit_if_failed(return_code)


def configure_qac_software(config):
    """Configures Helix QAC software according to provided settings
    in configuration file"""
    ensure_license_servers_configured(config)

    qac_commands.set_debug_level(config)

    if config.max_parallel_workers:
        LOGGER.info('Setting number of CPUs to be used in analysis to %s',
                    config.max_parallel_workers)

        qac_commands.set_maximum_cpu(config)
    else:
        LOGGER.info(
            'Number of CPU to use for QAC analysis left unchanged. '
            'Using pre-configured value')


def ensure_qac_project_directory_tree_created(config):
    """Ensures directory tree for QAC project created"""
    makedirs(config.qac_project_path, exist_ok=True)
    makedirs(os_path.join(config.qac_project_path, SCA_TOOL_DIR, EXPORT_DIR),
             exist_ok=True)
    makedirs(os_path.join(config.qac_project_path, SCA_TOOL_DIR,
                          'configuration'),
             exist_ok=True)
    makedirs(os_path.join(config.qac_project_path, SCA_TOOL_DIR, 'logs'),
             exist_ok=True)
    makedirs(os_path.join(config.qac_project_path, 's101'), exist_ok=True)
    makedirs(config.custom_config_path, exist_ok=True)
    makedirs(config.helper_logs_path, exist_ok=True)
    makedirs(os_path.join(config.helper_logs_path, 'analysis'), exist_ok=True)
    makedirs(os_path.join(config.helper_logs_path, 'qavupload'), exist_ok=True)
    makedirs(config.target_baseline_folder, exist_ok=True)
    makedirs(config.export_path, exist_ok=True)
    makedirs(config.via_path, exist_ok=True)
    makedirs(config.project_reports_path, exist_ok=True)
    makedirs(config.analysis_path, exist_ok=True)


def ensure_qac_exports_directory_tree_created(config):
    """Ensures directory tree for QAC exports created"""
    makedirs(config.export_path, exist_ok=True)
    makedirs(config.project_reports_path, exist_ok=True)
    makedirs(config.project_diagnostics_path, exist_ok=True)


def cleanup_qac_project_directory(config):
    """Cleans up qac_project_path directory"""
    # Temporary solution to keep sca log files during cleanup
    if config.qac_project_path in config.helper_logs_path:
        clean_directory(
            config.qac_project_path,
            exclude_regex=rf'{LOGS_PREFIX}.*\.log')

        for dir_path, _, _ in os_walk(config.qac_project_path):
            absolute_path = os_path.join(config.qac_project_path, dir_path)
            # Do not remove files under helper_logs_path
            if config.helper_logs_path in absolute_path:
                continue

            if absolute_path not in config.helper_logs_path:
                clean_directory(absolute_path)
                safe_delete_dirtree(absolute_path)
    else:
        safe_delete_dirtree(config.qac_project_path)


def remove_qac_export_directories(config):
    """Removes QAC export directories"""
    safe_delete_dirtree(config.export_path)
    safe_delete_dirtree(config.project_reports_path)
    safe_delete_dirtree(config.project_diagnostics_path)


def prepare_directory_tree(config):
    """Prepares directory tree for Helix QAC project creation and
    further SCA processing"""
    if config.cleanup_on_create:
        LOGGER.info(
            'Cleaning up project and exports directories, '
            'because %s enabled',
            config.get_parameter_name('CLEANUP_ON_CREATE'))

        remove_qac_export_directories(config)
        cleanup_qac_project_directory(config)
    else:
        LOGGER.info('Not performing cleanup, because %s disabled',
                    config.get_parameter_name('CLEANUP_ON_CREATE'))

    ensure_qac_project_directory_tree_created(config)
    ensure_qac_exports_directory_tree_created(config)


def ensure_configuration_file_exists(config):
    """Ensures configuration file for Helix QAC exists
    (ACF, VCF, RCF, NCF and USER_MESSAGES files) in case
    they are defined in configuration"""
    LOGGER.debug('Checking if ACF file exists')
    getattr(config, 'acf_file')
    LOGGER.debug('Checking if VCF file exists')
    getattr(config, 'vcf_file')
    LOGGER.debug('Checking if NCF file exists')
    getattr(config, 'ncf_file')
    LOGGER.debug('Checking if RCF file exists')
    getattr(config, 'rcf_file')
    LOGGER.debug('Checking if User Messages file exists')
    getattr(config, 'user_messages')
    LOGGER.debug('Checking if Custom help file exists')
    getattr(config, 'custom_help_path')


def link_custom_help_pages(config):
    """Links custom help page paths in configuration files"""
    rcf_filepath = config.rcf_file.get_result_filepath()
    user_messages_filepath = config.user_messages.get_result_filepath()

    if config.help_pages_root_dir:
        LOGGER.info(
            'Linking custom help pages from %s in RCF and user messages files',
            config.get_parameter_name('HELP_PAGES_ROOT_DIR'))
        set_help_path_in_rcf(rcf_filepath, config.help_pages_root_dir)
        set_help_path_in_user_messages(user_messages_filepath,
                                       config.help_pages_root_dir)

    if config.custom_help_path:
        LOGGER.info(
            'Linking custom help pages from %s in RCF and user messages files',
            config.get_parameter_name('CUSTOM_HELP_PATH'))
        set_bosch_custom_help(rcf_filepath, config.custom_help_path)
        set_bosch_custom_help(user_messages_filepath, config.custom_help_path)


def link_qac_builtin_help_pages(config):
    """Links QAC builtin help page paths in configuration files"""
    user_messages_filepath = config.user_messages.get_result_filepath()

    LOGGER.info('Linking QAC built-in help pages in user messages file')

    set_builtin_qac_help(user_messages_filepath, config.qac_home_path)
    set_component_path_in_xml(user_messages_filepath, config.qac_home_path)


def link_help_pages_to_warnings(config):
    """Links custom and builtin help page paths to warnings
    in configuration files"""
    link_custom_help_pages(config)
    link_qac_builtin_help_pages(config)


def retrieve_validate_baseline_file(config):
    """Retrieves and validates (if .sha file exists) baseline file"""
    if config.baseline_dirpath:
        LOGGER.info('Retrieving baseline file from %s',
                    config.get_parameter_name('LOCAL_BASELINE_PATH'))

        (baseline_directory, validation_required) = \
            retrieve_file_from_remote_resource(
                config.baseline_dirpath,
                config.target_baseline_folder,
                BASELINE_FILE_NAME)

        if validation_required:
            validate_baseline_file(
                os_path.join(baseline_directory, BASELINE_FILE_NAME))

        if baseline_directory == config.baseline_dirpath:
            source_baseline_filepath = os_path.join(config.baseline_dirpath,
                                                    BASELINE_FILE_NAME)
            target_baseline_filepath = os_path.join(
                config.target_baseline_folder, BASELINE_FILE_NAME)

            copy_file(source_baseline_filepath, target_baseline_filepath)


def create_qac_project(config):
    """Creates Helix QAC project"""
    LOGGER.info('Creating Helix QAC project')

    qacli_compiler_options = ' '.join('--cct {}'.format(compiler)
                                      for compiler in config.compiler_list)

    config_files_pair = [('acf', config.acf_file.get_result_filepath()),
                         ('rcf', config.rcf_file.get_result_filepath()),
                         ('vcf', config.vcf_file),
                         ('ncf', config.ncf_file.get_result_filepath()),
                         ('user-messages',
                          config.user_messages.get_result_filepath())]

    qac_commands.create_qac_project(config, qacli_compiler_options,
                                    config_files_pair)


def set_include_path_sync_setting(config):
    """Sets INCLUDE_PATH sync setting in case they are defined
    in qac_sync_settings_include_path"""
    if config.qac_sync_settings_include_path:
        LOGGER.info(
            'Setting the symbols used to extract Include Paths from the '
            'compiler command line, as %s is set',
            config.get_parameter_name('QAC_SYNC_SETTINGS_INCLUDE_PATH'))
        for option in config.qac_sync_settings_include_path:
            qac_commands.apply_sync_settings(config, 'INCLUDE_PATH', option)
    else:
        LOGGER.info(
            'Using QAC default symbols to extract Include Paths from the '
            'compiler command line, as %s is unset',
            config.get_parameter_name('QAC_SYNC_SETTINGS_INCLUDE_PATH'))


def generate_analysis_filter_file(config):
    """Generates options for exclude filter configuration
    from qac_analysis_path_blacklist"""
    LOGGER.info(
        'Generating options file %s for exclude filter configuration from %s',
        config.analysis_filter_filepath,
        config.get_parameter_name('QAC_ANALYSIS_PATH_BLACKLIST'))
    with open_t(config.analysis_filter_filepath,
                mode="w") as analysis_filter_file:
        analysis_filter_file.writelines([
            '-q {}\n'.format(path_filter)
            for path_filter in config.qac_analysis_path_blacklist
        ])


def configure_exclude_filter_for_module(config, module):
    """Configures blacklist filter specified in qac_analysis_path_blacklist
    to separated QAC module"""
    LOGGER.info('Configuring exclude filter for %s module', module)
    toolchain = get_module_toolchain(config, module)
    [_, return_code] = \
        qac_commands.apply_path_blacklist(config, module,
                                          config.analysis_filter_filepath,
                                          toolchain)
    check_return_code_for_cmd_and_exit_if_failed(return_code)


def configure_exclude_filter_for_modules(config):
    """Configures blacklist filter specified in qac_analysis_path_blacklist
    to QAC modules listed in qac_modules"""
    if config.qac_analysis_path_blacklist:
        generate_analysis_filter_file(config)
        for module in config.qac_modules:
            configure_exclude_filter_for_module(config, module)
    else:
        LOGGER.info(
            'Exclude filter configuration for modules will not be performed, '
            'because %s is unset',
            config.get_parameter_name('QAC_ANALYSIS_PATH_BLACKLIST'))


def set_baseline(config):
    """Sets baseline in case baseline file exists"""
    baseline_filepath = \
        os_path.join(config.target_baseline_folder, BASELINE_FILE_NAME)
    if os_path.exists(baseline_filepath):
        LOGGER.info('Baseline file exists. Setting up baseline in QAC project')
        qac_commands.setup_baseline(config, config.target_baseline_folder)


def configure_exclude_filter_for_sync(config):
    """Configures blacklist filter specified in qac_sync_path_blacklist
    for QAC project synchronization"""
    if config.project_sync_path_blacklist:
        for path in config.project_sync_path_blacklist:
            LOGGER.info(
                'Configuring %s path to be excluded from '
                'project synchronization',
                path)
            [_, return_value] = qac_commands.apply_sync_filter(config, path)
            check_return_code_for_cmd_and_exit_if_failed(return_value)
    else:
        LOGGER.info(
            'Exclude filter configuration for sync will not be performed, '
            'because %s is unset',
            config.get_parameter_name('QAC_SYNC_PATH_BLACKLIST'))


def configure_qac_project(config):
    """Configures Helix QAC project"""
    qac_commands.set_default_config(config)

    LOGGER.info('Setting the root directory of source code to %s',
                config.project_root)
    qac_commands.set_source_code_root(config)

    if not config.c_files_analyzed_as_c:
        LOGGER.info(
            'Removing C extensions from C language and '
            'associating it with C++ language, because %s disabled',
            config.get_parameter_name('C_FILES_ANALYZED_AS_C'))

        qac_commands.setup_c_as_cpp_extensions(config)
    else:
        LOGGER.info(
            'C extension associated with C language, '
            'because %s enabled',
            config.get_parameter_name('C_FILES_ANALYZED_AS_C'))

    set_include_path_sync_setting(config)
    configure_exclude_filter_for_sync(config)
    configure_exclude_filter_for_modules(config)
    set_baseline(config)


def configure_files_suppression(config):
    """Configures suppression for QAC project

    If helper_suppress_c_header is specified C headers will be excluded
    from analysis
    If helper_suppress_file_list_a is specified, files from
    helper_suppress_file_list_a will be excluded from analysis"""
    if config.helper_suppress_c_header:
        LOGGER.info(
            'Header files (.h, .hpp) will be excluded from analysis, '
            'because %s enabled',
            config.get_parameter_name('HELPER_SUPPRESS_C_HEADER'))
        suppress_c_header(config)

    if config.helper_suppress_file_list_a:
        LOGGER.info('Files listed in %s will be excluded from analysis',
                    config.get_parameter_name('HELPER_SUPPRESS_FILE_LIST_A'))
        suppress_file_in_static_list_a(config,
                                       config.helper_suppress_file_list_a)


def remove_files_from_qac_project(config):
    """Removes files from helper_remove_file_list from QAC project"""
    if config.helper_remove_file_list:
        LOGGER.info('Removing files listed in %s from Helix QAC project',
                    config.get_parameter_name('HELPER_REMOVE_FILE_LIST'))
        qac_commands.remove_files_from_project(config)
