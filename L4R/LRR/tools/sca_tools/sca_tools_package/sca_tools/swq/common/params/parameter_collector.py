# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: parameter_collector.py
# ----------------------------------------------------------------------------
"""Defines SCA tools parameters collector class"""

from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, RC_MISSING_PARAMETER
from swq.common.params.params_utils import collect_environment_parameters, \
    collect_cli_parameters, parse_configuration_files, merge_dicts, \
    check_if_parameter_set_and_exit_if_not, print_configuration_dicts


class ParameterCollector:
    """Class that collects and handles parameters"""
    def __init__(self, args, parameters):
        self._args = args
        self._parameters = parameters
        self._commandline_config = collect_cli_parameters(
            self._args, self._parameters.get_cli_params())
        self._env_config = collect_environment_parameters(
            self._parameters.get_env_params())
        self._target_config = {}
        self._general_config = {}
        self._check_and_collect_datastore_parameters()
        self._merged_config = merge_dicts(self._general_config,
                                          self._target_config,
                                          self._env_config,
                                          self._commandline_config)
        print_configuration_dicts(self._commandline_config, self._env_config,
                                  self._target_config, self._general_config,
                                  self._merged_config)
        self._check_for_deprecated_subcommand()
        self._check_for_mandatory_parameters()
        self._check_for_deprecated_parameters()

    def _check_and_collect_datastore_parameters(self):
        merged_input_parameters = merge_dicts(self._env_config,
                                              self._commandline_config)
        datastore_paths = merged_input_parameters.get(
            self._parameters.DATASTORE_PATH.alias)

        if self._parameters.is_datastore_config_required():
            check_if_parameter_set_and_exit_if_not(
                self._parameters.DATASTORE_PATH.alias, datastore_paths)

        if datastore_paths:
            json_parameters = [
                parameter.alias
                for parameter in self._parameters.get_json_params()
            ]
            (self._general_config, self._target_config) = \
                parse_configuration_files(
                    merged_input_parameters, datastore_paths,
                    json_parameters,
                    self._parameters.DATASTORE_TARGET.alias)
        else:
            LOGGER.info("%s either is not specified or path does not exist",
                        self._parameters.DATASTORE_PATH.alias)
            LOGGER.info('Proceeding without configuration file')

    def _check_for_deprecated_subcommand(self):
        (subcommand_deprecated,
         deprecation_message) = self._parameters.is_subcommand_deprecated()
        if subcommand_deprecated:
            LOGGER.warning(deprecation_message)

    def _check_for_mandatory_parameters(self):
        missing_variables = {
            parameter.alias
            for parameter in self._parameters.get_mandatory_params()
            if parameter.alias not in self._merged_config.keys()
        }
        if missing_variables:
            for variable in missing_variables:
                LOGGER.error('Please define mandatory variable: %s',
                             variable.upper())
            log_and_exit(RC_MISSING_PARAMETER)

    def _check_for_deprecated_parameters(self):
        deprecated_parameters = [
            parameter
            for parameter in self._parameters.get_deprecated_params()
            if parameter.alias in self._merged_config.keys()
        ]
        if deprecated_parameters:
            for parameter in deprecated_parameters:
                LOGGER.warning(parameter.deprecation_message)

    def __getattr__(self, property_name):
        parameter_name = getattr(self._parameters, property_name).alias
        try:
            return self._merged_config[parameter_name]
        except KeyError as ex:
            raise AttributeError from ex

    def get_parameter_name(self, property_name):
        """Gets parameter name"""
        parameter_name = getattr(self._parameters, property_name).alias

        return parameter_name if parameter_name else None

    def get_commandline_config(self):
        """Gets commandline config"""
        return self._commandline_config

    def get_env_config(self):
        """Gets env config"""
        return self._env_config

    def get_target_config(self):
        """Gets target config"""
        return self._target_config

    def get_general_config(self):
        """Gets general config"""
        return self._general_config

    def get_merged_config(self):
        """Gets merged config"""
        return self._merged_config

    def get_subcommand(self):
        """Returns subcommand"""
        return self._parameters.get_subcommand()
