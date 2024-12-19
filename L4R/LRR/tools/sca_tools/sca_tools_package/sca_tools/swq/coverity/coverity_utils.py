# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: coverity_utils.py
# ----------------------------------------------------------------------------
"""Defines helper methods for interaction with Coverity"""
from os import path
from math import trunc

from swq.common.logger import LOGGER
from swq.common.return_codes import \
    check_return_code_for_cmd_and_exit_if_failed
from swq.common.constants import IS_WINDOWS
from swq.coverity.coverity_commands import list_coverity_translation_units, \
    get_coverity_analysis_version
from swq.coverity.constants import BUILD_SCRIPT_LINUX, BUILD_SCRIPT_WINDOWS, \
    FILTERED_REPORT_SUFFIX


def list_translation_units(config):
    """Returns list of translation units"""
    LOGGER.info("LISTING TRANSLATION UNITS")
    [output, return_value] = list_coverity_translation_units(config)
    check_return_code_for_cmd_and_exit_if_failed(return_value)

    total_numberof_tus = output.count("Translation unit:")
    numberof_failed_tus = output.count(" (failure)")
    coverity_failures = []

    for line in output.splitlines():
        if line.endswith('(failure)'):
            coverity_failures.append(line)

    numberof_successful_tus = total_numberof_tus - numberof_failed_tus
    percentage_of_successful_tus = 0
    try:
        percentage_of_successful_tus = trunc(
            (numberof_successful_tus / total_numberof_tus) * 100)
    except ZeroDivisionError:
        LOGGER.error("Couldnt calculate %, assuming 0")
    LOGGER.info("TOTAL NUMBER OF FOUND TRANSLATION UNITS: %s",
                total_numberof_tus)
    LOGGER.info("# OF FAILED TUs: %s", numberof_failed_tus)
    for fail in coverity_failures:
        LOGGER.info(" FAILED TUs: %s", fail)
    LOGGER.info("# OF SUCCESSFULL TUs: %s", numberof_successful_tus)
    LOGGER.info("%% OF TUs READY FOR ANALYSIS: %s %%",
                percentage_of_successful_tus)

    return {
        'total_numberof_tus': total_numberof_tus,
        'numberof_failed_tus': numberof_failed_tus,
        'numberof_successful_tus': numberof_successful_tus,
        'percentage_of_successful_tus': percentage_of_successful_tus
    }


def coverity_version(config):
    """Gets Coverity Analysis version and build number"""
    version_string, return_code = get_coverity_analysis_version(config)
    check_return_code_for_cmd_and_exit_if_failed(return_code)

    return version_string


def compose_build_script_filepath(compile_commands_json):
    """Composes build script filepath using compile_commands.json filepath"""
    return path.join(
        path.dirname(compile_commands_json), BUILD_SCRIPT_WINDOWS) \
        if IS_WINDOWS else path.join(path.dirname(
            compile_commands_json), BUILD_SCRIPT_LINUX)


def get_filtered_report_name(csv_report_filepath):
    """Gets filtered report name from report filepath"""
    return '{}-{}'.format(
        path.splitext(path.basename(csv_report_filepath))[0],
        FILTERED_REPORT_SUFFIX)
