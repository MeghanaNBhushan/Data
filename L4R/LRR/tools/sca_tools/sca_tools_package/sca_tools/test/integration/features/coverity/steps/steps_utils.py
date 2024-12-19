# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: steps_utils.py
# ----------------------------------------------------------------------------

from os import path as os_path, environ as os_environ
from csv import DictReader
from json import loads as json_loads

from sys import executable as python_executable
from hamcrest import assert_that, equal_to
from test.integration.utils import common_utils
from test.integration.run_behave_tests import SWQ_MODULE_PATH
from swq.common.logger import LOGGER


def modify_coverity_config(context, old_config, new_config, config_key):
    """ Writes the new coverity json file """
    coverity_version_min = context.coverity_version.replace('coverity', '',
                                                            1).strip()

    mapping = {
        "coverity_version": context.coverity_version,
        "coverity_version_min": coverity_version_min,
        "project_root": context.project_root,
        "config_key": config_key,
        "test_root": context.test_root
    }

    common_utils.replace_pattern(old_config, new_config, mapping)

    return new_config


def read_parameter_table(context, config_key):
    """ Reads the parameter table given in a feature """
    LOGGER.debug(' read_parameter_table: %s', context.configs)
    target_options = context.configs[config_key][config_key]
    common_utils.map_target_options(context, target_options)
    common_utils.save_json_config(context, config_key,
                                  context.configs[config_key])
    modify_coverity_config(context, context.configs[config_key],
                           context.configs[config_key], config_key)


def get_command(context, config_key, session, options=None):
    json_filepath = os_path.join(context.json_path, f'{config_key}.json')
    project_root = os_path.join(context.project_root)
    coverity_bin_path = os_environ.get('COVERITY_BIN_PATH') or \
        context.configs[config_key]['COVERITY_BIN_PATH'] or \
        context.configs[config_key][config_key]['COVERITY_BIN_PATH']
    nox_file_path = os_path.join(project_root, 'noxfile.py')
    command = [
        python_executable, '-m', 'nox', '-f', nox_file_path, '-s', session,
        '--', '--coverity_json', json_filepath, '--coverity_bin_path',
        coverity_bin_path, '--project_root', project_root, '--variant',
        config_key, '--sca_tools',
        os_path.join(SWQ_MODULE_PATH.absolute(), 'sca_tools.py')
    ]

    common_utils.extend_command_with_options(command, options)

    return command


def get_amount_of_issues_from_csv_report(csv_filepath):
    with open(csv_filepath, newline='') as csv_file:
        csv_rows = DictReader(csv_file)
        return len(list(csv_rows))


def get_amount_of_issues_from_json_report(json_filepath):
    amount_of_issues = 0

    with open(json_filepath, 'r') as json_file:
        json_data = json_loads(json_file.read())
        for json_block in json_data['issues']:
            amount_of_issues += json_block['occurrenceNumberInMK'] == 1

    return amount_of_issues


def verify_reports(coverity_project_path):
    csv_filename = 'json-output-export.csv'
    csv_report_filepath = os_path.join(coverity_project_path, 'sca_tools',
                                       'export', 'cov-format-errors',
                                       csv_filename)

    json_filename = 'json-output.json'
    json_report_filepath = os_path.join(coverity_project_path, 'sca_tools',
                                        'export', 'cov-format-errors',
                                        json_filename)

    assert_that(os_path.exists(csv_report_filepath), equal_to(True),
                f'{csv_filename} was not created')

    amount_of_issues_from_csv_report = \
        get_amount_of_issues_from_csv_report(csv_report_filepath)
    amount_of_issues_from_json_report = \
        get_amount_of_issues_from_json_report(json_report_filepath)

    assert_that(
        amount_of_issues_from_csv_report,
        equal_to(amount_of_issues_from_json_report),
        f'Number of warnings in {csv_filename} not as in {json_filename}')
