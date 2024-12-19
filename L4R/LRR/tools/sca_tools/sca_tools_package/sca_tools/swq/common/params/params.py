# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	params.py
# ----------------------------------------------------------------------------
"""Defines SCA tools parameters class"""

from swq.common.file.file_utils import load_json_file
from swq.common.params.params_utils import merge_dicts
from swq.common.logger import LOGGER
from swq.common.constants import COMMON_PARAMS_JSON, \
    COMPILER_WARNINGS_PARAMS_JSON, COVERITY_PARAMS_JSON, \
    FIND_INCLUDES_PARAMS_JSON, MAP_TEAMS_PARAMS_JSON, QAC_PARAMS_JSON, \
    UNIFY_REPORTS_PARAMS_JSON
from swq.common.params.parameter_properties import ParameterProperties


def _load_common_parameters():
    return load_json_file(COMMON_PARAMS_JSON)


class SCAParameters:
    """Class that holds parameters of SCA_tools commands"""
    def __init__(self):
        self.__common_parameters = _load_common_parameters()
        self.__compiler_warnings = self.__load_compiler_warnings_parameters()
        self.__coverity = self.__load_coverity_parameters()
        self.__find_includes = self.__load_find_includes_parameters()
        self.__map_teams = self.__load_map_teams_parameters()
        self.__qac = self.__load_qac_parameters()
        self.__unify_reports = self.__load_unify_reports_parameters()

    def __load_compiler_warnings_parameters(self):
        command_parameters = self.__get_all_parameters_for_command(
            COMPILER_WARNINGS_PARAMS_JSON)
        return CommandParameters(command_parameters)

    def __load_coverity_parameters(self):
        command_parameters = self.__get_all_parameters_for_command(
            COVERITY_PARAMS_JSON)
        return CommandParameters(command_parameters)

    def __load_find_includes_parameters(self):
        command_parameters = self.__get_all_parameters_for_command(
            FIND_INCLUDES_PARAMS_JSON)
        return CommandParameters(command_parameters)

    def __load_map_teams_parameters(self):
        command_parameters = self.__get_all_parameters_for_command(
            MAP_TEAMS_PARAMS_JSON)
        return CommandParameters(command_parameters)

    def __load_qac_parameters(self):
        command_parameters = self.__get_all_parameters_for_command(
            QAC_PARAMS_JSON)
        return CommandParameters(command_parameters)

    def __load_unify_reports_parameters(self):
        command_parameters = self.__get_all_parameters_for_command(
            UNIFY_REPORTS_PARAMS_JSON)
        return CommandParameters(command_parameters)

    def __merge_with_common_parameters(self, loaded_json_data):
        common_parameters = self.__common_parameters['parameters']
        loaded_parameters = loaded_json_data['parameters']
        merged_json_data = loaded_json_data.copy()
        for parameter in common_parameters.keys():
            if parameter in loaded_parameters.keys():
                merged_json_data['parameters'][parameter] = merge_dicts(
                    common_parameters[parameter], loaded_parameters[parameter])
            else:
                merged_json_data['parameters'][parameter] = common_parameters[
                    parameter]

        return merged_json_data

    def __get_all_parameters_for_command(self, json_file):
        """Parses parameters JSON file and merges with common parameters"""
        LOGGER.debug("Reading parameters from config %s", json_file)
        loaded_json_data = load_json_file(json_file)

        return self.__merge_with_common_parameters(loaded_json_data)

    @property
    def compiler_warnings(self):
        """Gets the property compiler_warnings"""
        return self.__compiler_warnings

    @property
    def coverity(self):
        """Gets the property coverity"""
        return self.__coverity

    @property
    def find_includes(self):
        """Gets the property find_includes"""
        return self.__find_includes

    @property
    def map_teams(self):
        """Gets the property map_teams"""
        return self.__map_teams

    @property
    def qac(self):
        """Gets the property qac"""
        return self.__qac

    @property
    def unify_reports(self):
        """Gets the property unify_reports"""
        return self.__unify_reports


class CommandParameters:
    """Defines SCA tools command parameters class"""
    def __init__(self, data: dict):
        self._data = data
        self.__subcommand = None

    def __getattr__(self, key):
        try:
            return ParameterProperties(key, self._data['parameters'][key])
        except KeyError as ex:
            raise AttributeError("Undefined parameter: {}".format(key)) from ex

    def __is_parameter_mandatory(self, mandatory_value):
        try:
            return self.__subcommand in mandatory_value
        except TypeError:
            return mandatory_value

    def get_all_params(self):
        """Returns all parameters"""
        return [getattr(self, key) for key in self._data['parameters']]

    def get_cli_params(self):
        """Returns only cli parameters"""
        return [param for param in self.get_all_params() if param.cli]

    def get_env_params(self):
        """Returns only env parameters"""
        return [param for param in self.get_all_params() if param.env]

    def get_json_params(self):
        """Returns only json parameters"""
        return [param for param in self.get_all_params() if param.json]

    def get_mandatory_params(self):
        """Returns only mandatory parameters"""
        return [
            param for param in self.get_all_params()
            if self.__is_parameter_mandatory(param.mandatory)
        ]

    def get_deprecated_params(self):
        """Returns only deprecated parameters"""
        return [param for param in self.get_all_params() if param.deprecated]

    def get_description(self, subparser='root'):
        """Returns command description"""
        return self._data['argparser'][subparser].get('description', '')

    def get_subparser_description(self):
        """Returns subparser description"""
        return self._data['argparser']['root'].get('subparser_description', '')

    def is_datastore_config_required(self):
        """Returns datastore_config"""
        return self.__is_parameter_mandatory(self.DATASTORE_PATH.mandatory)

    def set_subcommand(self, subcommand):
        """Sets subcommand"""
        self.__subcommand = subcommand

    def get_subcommand(self):
        """Returns subcommand"""
        return self.__subcommand

    def is_subcommand_deprecated(self):
        """Returns subcommand deprecation"""
        subcommand = 'root' if self.__subcommand is None else self.__subcommand
        return (self._data['argparser'][subcommand].get('deprecated', False),
                self._data['argparser'][subcommand].get(
                    'deprecation_message', None))
