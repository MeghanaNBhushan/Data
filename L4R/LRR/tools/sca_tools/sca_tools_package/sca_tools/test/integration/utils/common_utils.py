# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: common_utils.py
# ----------------------------------------------------------------------------
"""Common utils"""

import os
import json
import subprocess

from datetime import datetime
from pathlib import Path
from test.integration.constants import MOCK_ENTRYPOINTS, BEHAVE_FOLDER_NAME, \
    BEHAVE_FOLDER_NAME, PARAMETER_VALUE_SEPARATOR, OS_FOLDER

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import create_dirs_if_necessary

_CURRENT_PATH = os.getcwd()
_INTEGRATION_TESTS_LOG_PATH = os.path.join(
    _CURRENT_PATH, BEHAVE_FOLDER_NAME, 'logs',
    'behave_integration_tests_{}.log'.format(
        datetime.today().strftime('%Y%m%d_%H%M%S.%f')[:-3]))


def initialize_logger_if_verbose_enabled(parsed_args):
    """ Initializes logger if verbose is enabled. """
    if parsed_args.verbose:
        LOGGER.initialize_once('BEHAVE TESTS')
        create_dirs_if_necessary(_INTEGRATION_TESTS_LOG_PATH)
        LOGGER.initialize_file_once(_INTEGRATION_TESTS_LOG_PATH)


def initialize_context(context):
    """ Initializes context with all variables
    to be used across various steps. """
    context.base_config = {}
    context.synctypes = {}
    context.compilers = {}
    context.configs = {}

    context.MOCK_ENTRYPOINTS = MOCK_ENTRYPOINTS
    context.current_path = _CURRENT_PATH
    context.test_root = os.path.normpath(_CURRENT_PATH)
    context.project_root = os.environ.get('BEHAVE_PROJECT_ROOT', '')
    context.minimal = os.environ.get('BEHAVE_MINIMAL', '')

    context.json_path = os.path.join(context.current_path, BEHAVE_FOLDER_NAME,
                                     'generated_config', OS_FOLDER, 'json')

    context.codeowners_filepath = os.path.join(context.current_path,
                                               BEHAVE_FOLDER_NAME,
                                               'generated_config',
                                               OS_FOLDER,
                                               'codeowners.txt')

    if not os.path.exists(context.json_path):
        try:
            os.makedirs(context.json_path)
        except OSError as error:
            LOGGER.error(error)

    context.logs_path = os.path.join(context.current_path, BEHAVE_FOLDER_NAME,
                                     'logs', OS_FOLDER)
    if not os.path.exists(context.logs_path):
        os.makedirs(context.logs_path)


def _get_utf8_decoded_message(bytes_array):
    return bytes_array.decode('utf8')


def execute_command(command, cwd=None):
    try:
        LOGGER.info('Executing %s, cwd=%s', ' '.join(arg for arg in command),
                    cwd)
        subprocess.check_output(command, stderr=subprocess.STDOUT, cwd=cwd)
    except subprocess.CalledProcessError as error:
        LOGGER.error("Command '{}' return with error (code {}): {}".format(
            error.cmd, error.returncode,
            _get_utf8_decoded_message(error.output)))
        return False
    return True


def replace_pattern(old_dict, new_dict, pattern):
    """ Replaces version information in the template json """
    LOGGER.debug('Pattern to be replaced: %s', pattern)
    for key, value in old_dict.items():
        LOGGER.debug('value to be inserted: %s', value)
        LOGGER.debug('in old dict found key: %s', key)
        LOGGER.debug('in new dict found keys: %s', new_dict.keys())
        LOGGER.debug('in new_dict search key: %s', key % pattern)
        if isinstance(value, dict):
            new_sub_dict = {}
            new_dict[key % pattern] = new_sub_dict
            replace_pattern(value, new_sub_dict, pattern)
        elif isinstance(value, list):
            new_dict[key % pattern] = [a % pattern for a in value]
        else:
            new_dict[key % pattern] = value % pattern


def save_json_config(context, config_key, config):
    """ Saves the json configuration """
    config_file_name = os.path.join(context.json_path,
                                    f'{config_key.lower()}.json')
    with open(config_file_name, 'w+') as json_file:
        LOGGER.debug('Save config file: %s', json_file)
        json_file.write(json.dumps(config, indent=4))


def map_target_options(context, target_options):
    """ Creates target options key value mapping """
    for row in context.table.rows:
        key = row['key']
        if PARAMETER_VALUE_SEPARATOR in row['value']:
            value = row['value'].split(PARAMETER_VALUE_SEPARATOR)
        else:
            value = row['value']
        target_options[key] = value
    return target_options


def read_configurations(context):
    """ Read the configurations """
    files = [
        read_json(f, context) for f in os.listdir(context.json_path)
        if os.path.isfile(os.path.join(context.json_path, f)) and (
            Path(f).suffix == '.json')
    ]

    LOGGER.info('Read in configurations for: %s', files)


def read_json(json_config_file, context):
    """ Loads the given json config into the context """
    config_key = json_config_file[0:-5]
    LOGGER.debug('config_key created: %s', config_key)
    json_path = os.path.join(context.json_path, json_config_file)
    with open(json_path) as json_file:
        context.configs[config_key] = json.load(json_file)
    return json_config_file


def _get_value_field_as_single_value_or_list(value):
    if value.startswith('['):
        _value = []
        _value.extend(f'{value[1:-1]}'.split(PARAMETER_VALUE_SEPARATOR))
        return _value

    return value


def generate_json_config_from_table(table):
    """ Converts a table into json format """
    json_config = {}
    for row in table.rows:
        key = row['key']
        value = row['value']
        value = _get_value_field_as_single_value_or_list(value)
        json_config[key] = value
    return json_config


def generate_codeowners_file(context):
    """ Generates codeowners file """
    with open(context.codeowners_filepath, 'w') as codeowners_file:
        for row in context.table.rows:
            team_mapping_row = "{} {}\n".format(row['component'], row['team'])
            codeowners_file.write(team_mapping_row)
    return context.codeowners_filepath


def extend_command_with_options(command, options):
    if options:
        if isinstance(options, list):
            command.extend(options)
        else:
            command.append(options)
