# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: sessions.py
# ----------------------------------------------------------------------------

from steps_utils import get_command, verify_reports

from os import path as os_path
from behave import then
from hamcrest import assert_that, equal_to
from test.integration.utils.common_utils import execute_command
from test.integration.constants import BEHAVE_FOLDER_NAME

from swq.common.logger import LOGGER


@then(u'create, analyze and export a report for config {config_key} \
using full project analysis')
def perform_coverity_steps_with_full_project_analysis(context, config_key):
    LOGGER.info('Create report for the projects given by the config_key %s',
                config_key)

    command = get_command(context, config_key, 'coverity_analyze_export')
    return_value = execute_command(command)
    assert_that(return_value, equal_to(True), 'command failed')

    coverity_project_path = os_path.join(
        context.test_root, BEHAVE_FOLDER_NAME, 'bin',
        context.configs[config_key][config_key]['COVERITY_PROJECT_PATH'])
    verify_reports(coverity_project_path)


@then(u'create, analyze and export a report for config {config_key} \
using delta project analysis')
def perform_coverity_steps_with_delta_project_analysis(context, config_key):
    LOGGER.info('Create report for the projects given by the config_key %s',
                config_key)

    command = get_command(context, config_key, 'coverity_analyze_delta_export')

    return_value = execute_command(command)
    assert_that(return_value, equal_to(True), 'command failed')

    coverity_project_path = os_path.join(
        context.test_root, BEHAVE_FOLDER_NAME, 'bin',
        context.configs[config_key][config_key]['COVERITY_PROJECT_PATH'])
    verify_reports(coverity_project_path)


@then(u'create, analyze and export a report for config {config_key} \
using compile_commands full project analysis')
def perform_coverity_steps_with_full_project_analysis_using_compile_commands(
        context, config_key):
    LOGGER.info('Create report for the projects given by the config_key %s',
                config_key)

    command = get_command(context, config_key, 'coverity_json_analyze_export')

    return_value = execute_command(command)
    assert_that(return_value, equal_to(True), 'command failed')

    coverity_project_path = os_path.join(
        context.test_root, BEHAVE_FOLDER_NAME, 'bin',
        context.configs[config_key][config_key]['COVERITY_PROJECT_PATH'])
    verify_reports(coverity_project_path)
