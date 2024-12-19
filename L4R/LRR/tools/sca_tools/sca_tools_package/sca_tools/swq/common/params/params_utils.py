# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: params_utils.py
# ----------------------------------------------------------------------------
"""Helper functions for the parameters handler classes of the SCA helper"""

import re

from os import path, environ
from json import loads
from functools import reduce

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t
from swq.common.constants import filter_sensitive_keys_from_dict
from swq.common.return_codes import log_and_exit, RC_INVALID_FILEPATH, \
    RC_CONFIG_PARSING_ERROR, RC_INVALID_PARAMETER, RC_MISSING_PARAMETER

_ENV_CONFIG_FIELD_SEPARATOR = ';'


def _get_args_or_none(arg, config_name: str):
    LOGGER.debug('%s = %s', config_name, arg)

    if arg is None:
        return None

    return (config_name, arg)


def _parse_env_string_to_list(config_value):
    return config_value.split(_ENV_CONFIG_FIELD_SEPARATOR) if len(
        config_value.split(_ENV_CONFIG_FIELD_SEPARATOR)) > 1 else config_value


def get_env_var_or_none(param):
    """Gets variable from environnement variables"""
    return _parse_env_string_to_list(
        environ.get(param.upper()).replace('\"', '')) if environ.get(
            param.upper()) else None


def create_validated_parameters_dict(target_parameters, validator_func):
    """Creates dict from list using validation function"""
    return {
        k: validator_func(k)
        for k in target_parameters if validator_func(k)
    }


def collect_cli_parameters(args, cli_parameters):
    """Collects parameters defined in CLI"""
    return {
        pair[0]: pair[1]
        for pair in [
            _get_args_or_none(args.get(key.cli_option), key.alias)
            for key in cli_parameters
        ] if pair
    }


def collect_environment_parameters(env_parameters):
    """Collects parameters defined in environment"""
    env_parameters = [parameter.alias for parameter in env_parameters]
    return create_validated_parameters_dict(env_parameters,
                                            get_env_var_or_none)


def load_json_with_comments(filepath):
    """Loads a JSON file from a given filepath and loads it. \
        It can contain // based comments"""
    if not path.exists(filepath):
        LOGGER.error(
            "load_json_with_comments: {} does not exist".format(filepath))
        log_and_exit(RC_INVALID_FILEPATH)

    with open_t(filepath) as file_with_comments:
        config_file_without_comments = re.sub(r'^\s*//.*\n', '',
                                              file_with_comments.read(), 0,
                                              re.MULTILINE)
        try:
            return_values = with_keys_in_lowercase(
                loads(config_file_without_comments))
        except ValueError:
            LOGGER.error("Parsing error when loading: {}".format(filepath))
            log_and_exit(RC_CONFIG_PARSING_ERROR)
        return return_values


def is_datastore_target_variable(possible_dt_variable):
    """Check if the variable is a datastore_target"""
    return isinstance(possible_dt_variable, dict)


def is_configured_key(key, config_args):
    """Check if key in configuration arguments"""
    return key.lower() in config_args


def only_unused_keys_not_in_configuration(parameters: dict, config_args):
    """Returns unused keys that are not in configuration"""
    def _only_unused_keys_not_in_configuration(key: str):
        return not is_datastore_target_variable(parameters.get(key)) and \
            not is_configured_key(key, config_args)

    return filter(_only_unused_keys_not_in_configuration, parameters.keys())


def print_unused_parameters(parameters: dict, config_args):
    """Compare parameters with configuration arguments """
    for key in only_unused_keys_not_in_configuration(parameters, config_args):
        LOGGER.debug('Unused parameter from configuration - %s', key.upper())


def merge_dicts(*dict_args):
    """Given any number of dictionaries, shallow copy and merge into
    a new dict, precedence goes to key-value pairs in latter
    dictionaries."""
    merged_dict = {}
    for dictionary in dict_args:
        merged_dict.update(dictionary)
    return merged_dict


def _merge_datastore_json(json_a: dict,
                          json_b: dict,
                          datastore_target: str = None):
    intersection_keys = json_a.keys() & json_b.keys()
    merged_config = merge_dicts(json_a, json_b)
    config_level_msg = 'base level'
    if datastore_target:
        config_level_msg = f'\'{datastore_target}\' datastore target level'
    LOGGER.warning(
        f'Overwriting {config_level_msg} parameters: {intersection_keys}')
    for key in intersection_keys:
        if isinstance(json_a[key], dict) and isinstance(json_b[key], dict):
            merged_config[key] = _merge_datastore_json(json_a[key],
                                                       json_b[key], key)

    return merged_config


def _get_target_config_from_datastore_config(datastore_target, json_config,
                                             general_config_level):
    target_config = {}
    if datastore_target:
        datastore_target = datastore_target.lower()
        LOGGER.debug("datastore_target = %s", datastore_target)
        if datastore_target in json_config:
            LOGGER.debug('Unused parameters from %s config level',
                         datastore_target)
            print_unused_parameters(json_config[datastore_target],
                                    general_config_level)
            target_config = with_keys_in_lowercase(
                json_config[datastore_target])
            target_config = filter_parameters_dict(target_config,
                                                   general_config_level)
        else:
            LOGGER.error("Specified datastore target does not exist: %s",
                         datastore_target)
            log_and_exit(RC_INVALID_PARAMETER)

    return target_config


def filter_parameters_dict(parameters_dict, target_parameters):
    """Filters parameters dict"""
    return {
        k: parameters_dict[k]
        for k in parameters_dict if k in target_parameters
    }


def parse_configuration_files(merged_input_parameters, datastore_paths,
                              general_config_level, datastore_target_config):
    """Parses JSON configuration file and returns configutration dicts"""
    datastore_config = {}

    for datastore_path in datastore_paths:
        datastore_config = \
            _merge_datastore_json(
                datastore_config,
                load_json_with_comments(path.normpath(datastore_path)))

    LOGGER.debug('Unused parameters from base config level')
    print_unused_parameters(datastore_config, general_config_level)

    datastore_target = merge_dicts(
        datastore_config, merged_input_parameters).get(datastore_target_config)

    target_config = _get_target_config_from_datastore_config(
        datastore_target, datastore_config, general_config_level)

    general_config = filter_parameters_dict(datastore_config,
                                            general_config_level)
    return (general_config, target_config)


def with_keys_in_lowercase(to_convert: dict):
    """Returns dict keys in lower case"""
    return {key.lower(): to_convert[key] for key in to_convert}


def check_if_parameter_set_and_exit_if_not(variable_name, value):
    """Checks that parameter set or exit if not"""
    if not value:
        LOGGER.error('The parameter is not set: %s', variable_name.upper())
        log_and_exit(RC_MISSING_PARAMETER)


def print_configuration_dicts(commandline_config, env_config, target_config,
                              general_config, merged_config):
    """Print parsed configuration parameters"""
    LOGGER.info(
        "\n\ncommandline config = %s\n\nenv_config = %s\n\n"
        "target_config = %s\n\ngeneral_config = %s\n\n"
        "merged_config = %s\n\n", commandline_config,
        filter_sensitive_keys_from_dict(env_config),
        filter_sensitive_keys_from_dict(target_config, warn=True),
        filter_sensitive_keys_from_dict(general_config, warn=True),
        filter_sensitive_keys_from_dict(merged_config))
