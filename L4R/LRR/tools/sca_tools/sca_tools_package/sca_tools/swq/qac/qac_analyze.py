# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: qac_analyze.py
# ----------------------------------------------------------------------------
"""The module contains all functions used to run QAC analysis and
   check its output"""
from os import path
from re import MULTILINE, finditer

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import copy_file, open_t, \
    clean_directory, copy_files
from swq.common.file.file_utils import write_lines_to_file
from swq.common.return_codes import log_and_exit, RC_ANALYZE_ERROR
from swq.qac import qac_commands
from swq.qac.project_state import REGEX_FOR_ANALYSIS_LOG_STRING
from swq.qac.qac_utils import \
    get_relevant_files_for_analysis_and_exit_if_none, \
    get_log_timestamp

__ANALYSIS_LOG_FILENAME_PREFIX = 'analyze_output'
__ANALYSIS_FAILURES_FILENAME_PREFIX = 'analyze_failures'


def qac_analyze(config):
    """Entrypoint function to run QAC Analysis"""
    analyze_project(config)
    if config.helper_create_baseline:
        qac_commands.create_baseline(config)
    if config.use_vscode_integration:
        qac_commands.vscode_output(config)


def analyze_project(config):
    """Runs QAC analysis and saves analysis log results"""
    clean_directory(config.qac_log_path)
    (return_value, _) = run_qac_analysis(config)
    __save_analysis_log_results_from_qac(config)

    return return_value


def compose_analyze_list_file(config):
    """Composes file with list of files used to be analyzed.
    Filters out files which are presented in original list, but
    do no exist in QAC project"""

    files_list = config.analyze_list

    if config.sync_type == 'JSON':
        files_list = get_relevant_files_for_analysis_and_exit_if_none(config)
        write_lines_to_file(config.actual_analyze_list, files_list)
    else:
        copy_file(config.analyze_list, config.actual_analyze_list)


def run_qac_analysis(config):
    """Runs QAC Analysis"""
    if config.analyze_list:
        compose_analyze_list_file(config)
        (return_value, analysis_failures) = analyze_list_and_check(config)
    elif config.use_flist:
        (return_value,
         analysis_failures) = analyze_file_and_check(config,
                                                     config.analyze_file)
    else:
        # empty files analyzes the whole project
        (return_value,
         analysis_failures) = analyze_file_and_check(config, None)
    return (return_value, analysis_failures)


def analyze_file_and_check(config, a_file):
    """Runs QAC analysis of the specified file"""
    output_log_filename = path.join(
        config.analysis_path,
        "{}_{}.log".format(__ANALYSIS_LOG_FILENAME_PREFIX,
                           get_log_timestamp()))
    [_, return_value] = qac_commands.analyze_file(config, a_file,
                                                  output_log_filename)
    analysis_failures = write_analysis_failures_to_file(
        config, output_log_filename, return_value)
    return (return_value, analysis_failures)


def analyze_list_and_check(config):
    """Runs QAC analysis of the files listed in the specified file"""
    if path.exists(config.actual_analyze_list):
        (return_value, analysis_failures) = analyze_file_and_check(
            config, '-F  {}'.format(config.actual_analyze_list))
    else:
        LOGGER.error("The file {} doesn't exist!".format(
            config.actual_analyze_list))
        log_and_exit(RC_ANALYZE_ERROR)
    return (return_value, analysis_failures)


def write_analysis_failures_to_file(config, output_log_filename, return_value):
    """Check QAC Analysis log for component return codes"""

    if not path.exists(output_log_filename):
        LOGGER.warning("Analysis log not found: %s", output_log_filename)
        return None

    analysis_failures = find_component_failures_in_analysis_output(
        output_log_filename)

    __write_analysis_failures_to_file(analysis_failures, output_log_filename)

    LOGGER.info('Checking qacli analysis output for potential failures '
                'because of sca_tools variable: '
                'SKIP_EXIT_ON_ANALYSIS_RETURN_CODES with value %s',
                config.skip_exit_on_analysis_return_codes)

    __check_return_code_and_exit_if_necessary(config, analysis_failures,
                                              return_value)
    return analysis_failures


def find_component_failures_in_analysis_output(log_filename):
    """Finds failures in analysis output and returns
    list of failures represented as string"""
    analysis_failures = []
    with open_t(log_filename) as analysis_log:
        analysis_log_content = analysis_log.read()
        for match in finditer(REGEX_FOR_ANALYSIS_LOG_STRING,
                              analysis_log_content, MULTILINE):
            component_return_code = match.group('return_code')
            if component_return_code != "0":
                analysis_failures.append(
                    __convert_failure_match_to_dict(match))
    return analysis_failures


def __save_analysis_log_results_from_qac(config):
    log_artifact_dir = config.analysis_path
    logs_dir = config.qac_log_path
    LOGGER.info("Saving logs from %s to %s", logs_dir, log_artifact_dir)
    copy_files(logs_dir, log_artifact_dir)


def __write_analysis_failures_to_file(analysis_failures, log_filename):
    if len(analysis_failures) > 0:
        LOGGER.error("Found %s with non-0 exit codes.", len(analysis_failures))

        with open_t(log_filename.replace(__ANALYSIS_LOG_FILENAME_PREFIX,
                                         __ANALYSIS_FAILURES_FILENAME_PREFIX),
                    mode="w+",
                    encoding='utf-8') as output_file:
            output_file.writelines(
                (__convert_failure_record_to_string(failure_record)
                 for failure_record in analysis_failures))


def __check_return_code_and_exit_if_necessary(config, analysis_failures,
                                              return_value):
    if return_value != 0:
        LOGGER.error("Analysis failed with return code %s. Failed files = %s",
                     return_value, analysis_failures)

        if config.skip_exit_on_analysis_return_codes and (return_value in (
                config.skip_exit_on_analysis_return_codes)):
            LOGGER.info("skip_exit_on_analysis_return_codes: {}".format(
                config.skip_exit_on_analysis_return_codes))
        else:
            __save_analysis_log_results_from_qac(config)
            log_and_exit(RC_ANALYZE_ERROR)


def __convert_failure_match_to_dict(failure_match):
    """Convert regexp match object with failure information to string"""
    failure_record = {
        'path': failure_match.group('path'),
        'module': failure_match.group('module'),
        'return_code': failure_match.group('return_code')
    }
    if failure_match.group('timestamp'):
        failure_record['timestamp'] = failure_match.group('timestamp')
    return failure_record


def __convert_failure_record_to_string(failure_record):
    """Convert regexp match object with failure information to string"""
    failure_description = 'path={}, module={}, return_code={}'.format(
        failure_record['path'], failure_record['module'],
        failure_record['return_code'])
    if 'timestamp' in failure_record:
        failure_description = '{}, timestamp={}'.format(
            failure_description, failure_record['timestamp'])
    failure_description += '\n'
    LOGGER.error(failure_description)
    return failure_description
