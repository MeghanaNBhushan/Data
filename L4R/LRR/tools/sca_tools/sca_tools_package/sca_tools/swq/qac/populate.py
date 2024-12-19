# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: populate.py
# ----------------------------------------------------------------------------
"""Defines methods for Helix QAC project population"""

from swq.common.config.common_config import \
    check_if_filepath_exists_and_exit_if_not
from swq.common.file.file_utils import apply_fix_to_cl_compile_commands, \
    file_contains_cl_specific_chars, use_json_sync_filter
from swq.common.filesystem.filesystem_utils import copy_file
from swq.common.logger import LOGGER
from swq.common.return_codes import RC_BUILD_ERROR, RC_SYNC_ERROR
from swq.qac import qac_commands
from swq.qac.constants import PROJECT_GENERATION_FAILED_MESSAGE, \
    PROJECT_SYNCHRONIZATION_FAILED_MESSAGE
from swq.qac.qac_utils import check_if_return_code_in_skip_list, \
    optimize_helix_project
from swq.qac.suppress import suppress_file_in_static_list_s, \
    suppress_file_in_static_list_s_build_log


def generate_project_populating_input_file(config):
    """Generates input file for populating Helix QAC project

    If sync_type is JSON will generate compile_commands;
    If sync_type is BUILD_LOG the build log file will be generated"""
    if config.sync_type in ['JSON', 'BUILD_LOG']:
        LOGGER.info('%s is set to %s', config.get_parameter_name('SYNC_TYPE'),
                    config.sync_type)
        if config.sync_build_command:
            LOGGER.info(
                'Running %s to generate input file for project populating',
                config.get_parameter_name('SYNC_BUILD_COMMAND'))
            return_code = run_build_command(config)
            check_if_return_code_in_skip_list(
                config, return_code, PROJECT_GENERATION_FAILED_MESSAGE,
                RC_BUILD_ERROR)

            check_if_filepath_exists_and_exit_if_not(
                config.get_parameter_name('SYNC_BUILD_LOG_FILE'),
                config.sync_build_log_file)
        else:
            LOGGER.info(
                'Project populating input file will not be generated, '
                'because %s is unset',
                config.get_parameter_name('SYNC_BUILD_COMMAND'))


def run_build_command(config):
    """Runs build_command. If use_python_build_shell is True,
    shell will be used as the program to execute command"""
    return_code = 0

    if config.use_python_build_shell:
        LOGGER.info(
            'The command will be executed through the shell, '
            'because %s enabled',
            config.get_parameter_name('USE_PYTHON_BUILD_SHELL'))
        [_, return_code] = qac_commands.build_project_with_shell(config)
    else:
        LOGGER.info(
            'The command will not be executed through the shell, '
            'because %s disabled',
            config.get_parameter_name('USE_PYTHON_BUILD_SHELL'))
        [_, return_code] = qac_commands.build_project_without_shell(config)

    return return_code


def filter_project_populating_input_file(config):
    """Filters project populating input file based on sync_type"""
    if config.sync_type == 'JSON':
        filter_json_populating_file(config)

    if config.sync_type == 'BUILD_LOG':
        filter_build_log_populating_file(config)


def filter_compile_commands(config):
    """Filters compile_commands.json file"""
    fix_cl_specific_chars(config)
    apply_json_sync_filter(config)
    suppress_files_in_compile_commands(config)


def filter_build_log(config):
    """Filters build log file"""
    if config.helper_suppress_file_list_s:
        LOGGER.info('Removing files listed in %s from build log',
                    config.get_parameter_name('HELPER_SUPPRESS_FILE_LIST_S'))

        build_log_file = config.actual_build_log
        suppressed_build_log_file = build_log_file

        suppress_file_in_static_list_s_build_log(
            build_log_file, config.helper_suppress_file_list_s,
            suppressed_build_log_file)
    else:
        LOGGER.info('Leaving build log unchanged, because %s is unset',
                    config.get_parameter_name('HELPER_SUPPRESS_FILE_LIST_S'))


def filter_json_populating_file(config):
    """Copies compile_commands to SCA project folder and filters it"""
    copy_file(config.sync_build_log_file, config.actual_sync_json)

    LOGGER.info('Filtering compile_commands.json file %s',
                config.actual_sync_json)

    filter_compile_commands(config)


def filter_build_log_populating_file(config):
    """Copies build_log file to SCA project folder and filters it"""
    copy_file(config.sync_build_log_file, config.actual_build_log)

    LOGGER.info('Filtering build log file %s', config.actual_build_log)

    filter_build_log(config)


def apply_json_sync_filter(config):
    """Applies JSON sync filter if sync_type_json_path_pattern is specified."""
    if config.sync_type_json_path_pattern:
        LOGGER.info(
            'Removing files that are not matching patterns listed in %s '
            'from compile_commands.json',
            config.get_parameter_name('SYNC_TYPE_JSON_PATH_PATTERN_WHITELIST'))

        compile_commands_file = config.actual_sync_json
        filtered_compile_commands_file = compile_commands_file

        use_json_sync_filter(config.sync_type_json_path_pattern,
                             compile_commands_file,
                             filtered_compile_commands_file)
    else:
        LOGGER.info(
            'Leaving compile_commands.json unchanged, because %s is unset',
            config.get_parameter_name('SYNC_TYPE_JSON_PATH_PATTERN_WHITELIST'))


def fix_cl_specific_chars(config):
    """In case file contains CL specifid charachters ('@<<', '<<'),
    remove them"""
    compile_commands_file = config.actual_sync_json

    if file_contains_cl_specific_chars(compile_commands_file):
        LOGGER.info('CL specific characters were found in %s. '
                    'Applying fix', compile_commands_file)

        apply_fix_to_cl_compile_commands(compile_commands_file)
    else:
        LOGGER.info('CL specific characters were not found in %s',
                    compile_commands_file)


def suppress_files_in_compile_commands(config):
    """Suppresses files in compile_commands.json in case
    helper_suppress_file_list_s is specified"""
    if config.helper_suppress_file_list_s:
        LOGGER.info(
            'Removing files listed in %s from compile_commands.json',
            config.get_parameter_name('HELPER_SUPPRESS_FILE_LIST_S'))

        compile_commands_file = config.actual_sync_json
        suppressed_compile_commands_file = compile_commands_file

        suppress_file_in_static_list_s(compile_commands_file,
                                       config.helper_suppress_file_list_s,
                                       suppressed_compile_commands_file)
    else:
        LOGGER.info(
            'Leaving compile_commands.json unchanged, because %s is unset',
            config.get_parameter_name('HELPER_SUPPRESS_FILE_LIST_S'))


def populate_files_to_qac_project(config):
    """Populates files to Helix QAC project depending on sync_type
    and checks whether return_code is in skip_exit_on_build_return_codes"""
    return_code = 0

    LOGGER.info('Populating QAC Project. Sync type: %s', config.sync_type)

    if config.sync_type == 'JSON':
        [_, return_code] = qac_commands.sync_project_json(config)

    if config.sync_type == 'BUILD_LOG':
        [_, return_code] = qac_commands.sync_project_build_log(config)

    if config.sync_type == 'MONITOR':
        [_, return_code] = qac_commands.sync_project_monitor(config)
        optimize_helix_project(config)

    check_if_return_code_in_skip_list(config, return_code,
                                      PROJECT_SYNCHRONIZATION_FAILED_MESSAGE,
                                      RC_SYNC_ERROR)
