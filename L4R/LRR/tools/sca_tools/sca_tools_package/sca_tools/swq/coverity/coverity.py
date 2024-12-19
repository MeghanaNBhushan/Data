# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: coverity.py
# ----------------------------------------------------------------------------
""" Main coverity helper functions """

import re
from math import trunc
from os import makedirs, path
from shutil import copy
from sys import executable as python_executable

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import create_dirs_if_necessary, \
    open_t
from swq.common.return_codes import log_and_exit, \
    check_return_code_for_cmd_and_exit_if_failed, \
    RC_ANALYZE_ERROR, RC_INVALID_FILEPATH, RC_MISSING_PARAMETER
from swq.common.config.common_config \
    import check_if_filepath_exists_and_exit_if_not
from swq.coverity.coverity_commands import cov_commit_defects, \
    run_coverity_analyze, create_coverity_config_for_compiler, \
    coverity_filter_translation_unit, run_coverity_build, git_rev_parse, \
    run_cov_run_desktop, run_generate_compile_commands
from swq.coverity.exporters.state_exporter import cov_format_errors_export,\
    cov_commit_defects_export, coverity_connect_webapi_export
from swq.coverity.coverity_utils import list_translation_units
from swq.coverity.project_state import ProjectState
from swq.coverity.constants import SCA_TOOL_DIR, EXPORT_DIR
from swq.common.file.file_utils import file_contains_cl_specific_chars, \
    apply_fix_to_cl_compile_commands, use_json_sync_filter


def _generate_compile_commands(config):
    [_, return_value] = run_generate_compile_commands(config)
    check_return_code_for_cmd_and_exit_if_failed(return_value)


def backup_compilation_file(filepath, backup_dir):
    """Saves file to a specified directory"""
    compilation_files_backup_dir = path.join(backup_dir, "build")
    makedirs(compilation_files_backup_dir, exist_ok=True)
    file_basename = path.basename(filepath)
    saved_filepath = path.join(compilation_files_backup_dir, file_basename)
    LOGGER.info("Saving file %s to: %s", filepath, saved_filepath)
    copy(filepath, saved_filepath)
    return saved_filepath


def get_build_command(config):
    """Returns build command according to defined configuration.
    BUILD_COMMAND will be used if no COMPILE_COMMANDS
    and USE_COMPILE_COMMANDS_JSON specified.
    In case if COMPILE_COMMANDS_JSON and USE_COMPILE_COMMANDS_JSON
    are specified will return build command that runs compilation
    using compile_commands.json"""

    build_command = config.build_command
    compile_commands_build_command = \
        config.compile_commands_build_command
    compile_commands_json = config.compile_commands_json
    use_compile_commands_json = config.use_compile_commands_json

    if use_compile_commands_json:
        LOGGER.info(
            '%s was set. compile_commands.json will be used for '
            'project compilation.',
            config.get_parameter_name('USE_COMPILE_COMMANDS_JSON'))

        if compile_commands_json is None:
            LOGGER.error('%s is not defined',
                         config.get_parameter_name('COMPILE_COMMANDS_JSON'))
            log_and_exit(RC_MISSING_PARAMETER)

        if compile_commands_build_command:
            LOGGER.info(
                '%s was set, running it to generate a compile_commands.json',
                config.get_parameter_name('COMPILE_COMMANDS_BUILD_COMMAND'))
            _generate_compile_commands(config)

        check_if_filepath_exists_and_exit_if_not(
            config.get_parameter_name('COMPILE_COMMANDS_JSON'),
            compile_commands_json)
        compile_commands_json = backup_compilation_file(
            compile_commands_json, config.helper_logs_path)

        if file_contains_cl_specific_chars(compile_commands_json):
            compile_commands_json = \
                apply_fix_to_cl_compile_commands(compile_commands_json)

        if config.merged_file_matching_patterns:
            compile_commands_json = \
                use_json_sync_filter(config.merged_file_matching_patterns,
                                     compile_commands_json)

        build_command = f'{python_executable} {config.script_location} '\
                        f'-f {compile_commands_json}'

        if config.max_parallel_workers:
            build_command += f' -t {config.max_parallel_workers}'

        return build_command

    if build_command is None:
        LOGGER.error('%s is not defined',
                     config.get_parameter_name('BUILD_COMMAND'))
        log_and_exit(RC_MISSING_PARAMETER)

    LOGGER.info('%s was set and will be used for project compilation',
                config.get_parameter_name('BUILD_COMMAND'))

    return build_command


def _build_project(config):
    build_command = get_build_command(config)
    [_, return_value] = run_coverity_build(config, build_command)
    check_return_code_for_cmd_and_exit_if_failed(return_value)


def _prepare_project(config):
    makedirs(path.join(config.coverity_project_path, SCA_TOOL_DIR, EXPORT_DIR),
             exist_ok=True)
    makedirs(path.join(config.coverity_project_path, SCA_TOOL_DIR,
                       'configuration'),
             exist_ok=True)
    makedirs(path.join(config.coverity_project_path, SCA_TOOL_DIR, 'logs'),
             exist_ok=True)


def coverity_create(config):
    """Creates coverity project by config"""
    LOGGER.debug("Create")
    LOGGER.info("GIT Commit is: '%s'", git_rev_parse(config))
    _prepare_project(config)

    for compiler in config.compiler_list:
        [_,
         return_value] = create_coverity_config_for_compiler(config, compiler)
        check_return_code_for_cmd_and_exit_if_failed(return_value)

    _build_project(config)

    # list all translation units after a build
    list_translation_units(config)


def filter_translation_units(config):
    "Filters translation units based on translation_units_blacklist"
    if config.translation_units_blacklist:
        LOGGER.info('Removing TUs listed in %s',
                    config.get_parameter_name('TRANSLATION_UNITS_BLACKLIST'))

        for filter_line in config.translation_units_blacklist:
            [_, return_value
             ] = coverity_filter_translation_unit(config, filter_line)
            if return_value not in (0, 2):
                log_and_exit(RC_ANALYZE_ERROR)
    else:
        LOGGER.info('Leaving TUs list unchanged, because %s is unset',
                    config.get_parameter_name('TRANSLATION_UNITS_BLACKLIST'))


def coverity_analyze(config):
    """Performs code analysis on a specified projects based on central
    analysis"""
    filter_translation_units(config)
    list_translation_units(config)
    [_, return_value] = run_coverity_analyze(config)
    check_return_code_for_cmd_and_exit_if_failed(return_value)


def coverity_run_desktop(config):
    """Generates analysis result based on desktop analysis"""
    filter_translation_units(config)
    list_translation_units(config)
    [_, return_code] = run_cov_run_desktop(config)
    check_return_code_for_cmd_and_exit_if_failed(return_code)


def coverity_export(config):
    """Generates analysis result report"""
    coverity_json_filepath = ProjectState(config).export_errors()
    cov_format_errors_export(config, coverity_json_filepath)


def coverity_preview_report(config):
    """Generates Coverity commit defects report based on preview report"""
    preview_report_json_export_file = ProjectState(
        config).export_preview_report()
    cov_commit_defects_export(config, preview_report_json_export_file)


def coverity_upload(config):
    """Uploads analysis report and source data to the coverity database \
    in a specified stream"""
    [_, return_value] = cov_commit_defects(config)
    check_return_code_for_cmd_and_exit_if_failed(return_value)


def coverity_webapi_export(config):
    """Exports specified view report from swq.coverity"""
    create_dirs_if_necessary(config.view_contents_export_filepath)
    coverity_connect_webapi_export(config)


def coverity_show_build_log_metrics(config):
    """Shows build log metrics"""
    coverity_build_log_path = path.join(config.coverity_project_path,
                                        "build-log.txt")
    translation_units_blacklist = config.translation_units_blacklist
    LOGGER.info("CHECKING COVERITY {}".format(coverity_build_log_path))
    coverity_non_compilation_unit_errors = []
    coverity_compilation_unit_errors_in_scope = []
    coverity_non_compilation_unit_warnings = []
    coverity_compilation_unit_warnings_in_scope = []
    relevant_tus = 0
    total_tus = 0
    if not translation_units_blacklist:
        translation_units_blacklist = []
    if not path.exists(coverity_build_log_path):
        LOGGER.error("%s does not exist.", coverity_build_log_path)
        log_and_exit(RC_INVALID_FILEPATH)
    else:
        with open_t(coverity_build_log_path) as build_log:
            data = build_log.read()
            # get the relevant and total numbers of compilation units
            for matches in re.findall("Emit for file '(.*?)' complete.", data):
                total_tus = total_tus + 1
                try:
                    if not any(
                            re.match(regex, matches)
                            for regex in translation_units_blacklist):
                        relevant_tus = relevant_tus + 1
                except ValueError:
                    LOGGER.error('Failure in parsing regex in .json: '
                                 'TRANSLATION_UNITS_BLACKLIST')
            all_coverity_errors = re.findall("[ERROR](.*)", data)
            for errors in all_coverity_errors:
                compilation_unit = re.search("compilation of \"(.*?)\"",
                                             errors)
                if compilation_unit:
                    # check if the comilation unit is relevant
                    if not any(
                            re.match(regex, compilation_unit.group(1))
                            for regex in translation_units_blacklist):
                        coverity_compilation_unit_errors_in_scope.append(
                            errors)
                else:
                    coverity_non_compilation_unit_errors.append(errors)

            all_coverity_warnings = re.findall("[WARNING](.*)", data)
            for warnings in all_coverity_warnings:
                compilation_unit = re.search("compilation of \"(.*?)\"",
                                             warnings)
                if compilation_unit:
                    # check if the comilation unit is relevant
                    if not any(
                            re.match(regex, compilation_unit.group(1))
                            for regex in translation_units_blacklist):
                        coverity_compilation_unit_warnings_in_scope.append(
                            warnings)
                else:
                    coverity_non_compilation_unit_warnings.append(warnings)

    numberof_successful_tus_in_scope = relevant_tus - len(
        coverity_compilation_unit_errors_in_scope)
    percentage_of_successful_tus_in_scope = 0
    try:
        percentage_of_successful_tus_in_scope = trunc(
            (numberof_successful_tus_in_scope / relevant_tus) * 100)
    except ZeroDivisionError:
        LOGGER.error("Couldnt calculate %%, asuming 0")
    LOGGER.info("------------ Project file scope ------------")
    for item in translation_units_blacklist:
        LOGGER.info("blacklist regex: %s", item)

    coverity_warnings = coverity_non_compilation_unit_warnings +\
        coverity_compilation_unit_warnings_in_scope
    unique_coverity_warnings = set(coverity_warnings)
    if len(coverity_warnings) != 0:
        LOGGER.warning(
            "------------ Unique Coverity [WARNING] in scope ------------")
        for warning in unique_coverity_warnings:
            LOGGER.warning("Coverity [WARNING]%s", warning.rstrip())
    coverity_errors = coverity_non_compilation_unit_errors +\
        coverity_compilation_unit_errors_in_scope
    unique_coverity_errors = set(coverity_errors)
    if len(coverity_errors) != 0:
        LOGGER.warning(
            "------------ Unique Coverity [ERROR] in scope ------------")
        for error in unique_coverity_errors:
            LOGGER.warning("Coverity [ERROR]%s", error)

    LOGGER.info("------------------------")
    LOGGER.info("Total [WARNING] found: %d in %s", len(all_coverity_warnings),
                coverity_build_log_path)
    LOGGER.info("[WARNING] in scope: %d in %s. Please have a look.",
                len(unique_coverity_warnings), coverity_build_log_path)
    LOGGER.info("Total [ERROR] found: %d in %s", len(all_coverity_errors),
                coverity_build_log_path)
    LOGGER.info("[ERROR] in scope: %d in %s. Please have a look.",
                len(unique_coverity_errors), coverity_build_log_path)
    LOGGER.info("Total [Compilation Units] found: %d in %s", total_tus,
                coverity_build_log_path)
    LOGGER.info(
        "[Compilation Units] in scope: %d. (%s%%) are ready for analysis.",
        relevant_tus, percentage_of_successful_tus_in_scope)
    if len(unique_coverity_errors) != 0:
        LOGGER.error("Coverity [ERROR] in file scope, Analysis failed.")
        log_and_exit(RC_ANALYZE_ERROR)
