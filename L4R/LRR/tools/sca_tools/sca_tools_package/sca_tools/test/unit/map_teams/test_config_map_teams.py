# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_config_map_teams.py
# ----------------------------------------------------------------------------
"""Tests for map_teams/config_map_teams.py"""
import inspect
from unittest import TestCase
from unittest.mock import patch

from swq.common.params.params import SCAParameters
from swq.map_teams.config_map_teams import create_map_teams_config


class TestMapTeamsConfig(TestCase):
    """ TestMapTeamsConfig class """
    def setUp(self):
        self.params = SCAParameters()
        self.map_teams_params = [
            param.alias.upper()
            for param in self.params.map_teams.get_all_params()
        ]

        self.args = {
            'project_root': 'foo/bar',
            'codeowners_file': 'foo.txt',
            'input_warnings_report': 'input.csv'
        }
        self.general_config = {}
        self.target_config = {}
        self.exception_list = [
            'target_config', 'commandline_config', 'env_config',
            'general_config', 'merged_config', 'project_root',
            'platform_command_extension'
        ]

    @patch('swq.common.params.parameter_collector.parse_configuration_files')
    def test_map_teams_config_parameters(self, parse_configuration_files):
        """Test map_teams parameters"""
        with patch('swq.common.params.parameter_collector.LOGGER'), \
            patch('swq.common.params.params_utils.LOGGER'), \
            patch('swq.map_teams.config_map_teams.' +
                  'check_if_filepath_exists_and_exit_if_not') \
                as check_filepath,\
            patch('swq.common.config.common_config.' +
                  'check_if_filepath_exists_and_exit_if_not') \
                as common_check_filepath:
            check_filepath.return_value = True
            common_check_filepath.return_value = True
            parse_configuration_files.return_value = (self.general_config,
                                                      self.target_config)
            config = create_map_teams_config(self.params.map_teams, self.args)

        with patch('swq.common.config.common_config.CommonConfig.' +
                   '_get_parameter_value') \
                as get_parameter_value:
            members = inspect.getmembers(config)
            attributes = [
                member[0] for member in members
                if not (member[0].startswith('_') or inspect.ismethod(
                    member[1]) or member[0] in self.exception_list)
            ]
            get_parameter_value.reset_mock()
            for attrib in attributes:
                getattr(config, attrib)
                for call in get_parameter_value.call_args_list:
                    args, _ = call
                    self.assertIn(args[0], self.map_teams_params)

                get_parameter_value.reset_mock()
