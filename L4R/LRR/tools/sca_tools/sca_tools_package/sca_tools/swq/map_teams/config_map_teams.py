# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config_map_teams.py
# ----------------------------------------------------------------------------
"""Shared map_teams project variables"""

from swq.common.config.common_config import CommonConfig, \
    check_if_filepath_exists_and_exit_if_not
from swq.common.config.config_parser_utils import \
    create_list_from_string_or_list
from swq.common.params.parameter_collector import ParameterCollector


def create_map_teams_config(params, args=None):
    """Parse configuration and creates config object"""
    parameter_collector = ParameterCollector(args, params)

    return MapTeamsConfig(parameter_collector)


class MapTeamsConfig(CommonConfig):
    """Class that abstracts the three hierarchical levels of configuration. \
    Read-only access to the variables themselves. \
    This is immutable by design"""
    def __init__(self, parameter_collector: object):
        super().__init__(parameter_collector)
        check_if_filepath_exists_and_exit_if_not(
            self.get_parameter_name('INPUT_WARNINGS_REPORT'),
            self.input_warnings_report)

    @property
    def codeowners_file(self):
        """Gets the property codeowners_file"""
        filepaths = create_list_from_string_or_list(
            self._get_parameter_value('CODEOWNERS_FILE'))

        return [
            self.get_path_relative_to_project_root(filepath)
            for filepath in filepaths
        ] if filepaths else None

    @property
    def datastore_target(self):
        """Gets the property datastore_target"""
        return self._get_parameter_value('DATASTORE_TARGET')

    @property
    def field_delimiter(self):
        """Gets the property field_delimiter"""
        return self._get_parameter_value('FIELD_DELIMITER', default=',')

    @property
    def only_last_team(self):
        """Gets the property only_last_team"""
        only_last_team = self._get_parameter_value('ONLY_LAST_TEAM')
        return only_last_team if only_last_team else \
            self._get_parameter_value('GITIGNORE_MAPPING')

    @property
    def input_warnings_report(self):
        """Gets the property input_warnings_report"""
        filepath = self._get_parameter_value('INPUT_WARNINGS_REPORT')

        return self.get_path_relative_to_project_root(filepath)

    @property
    def mapping_column(self):
        """Gets the property mapping_column"""
        return self._get_parameter_value('MAPPING_COLUMN', default='Filename')

    @property
    def teams_report(self):
        """Gets the property teams_report"""
        filepath = self._get_parameter_value('TEAMS_REPORT')

        return self.get_path_relative_to_project_root(filepath)
