# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_config_qac.py
# ----------------------------------------------------------------------------
"""Tests for qac/config_qac.py"""
import inspect
from unittest import TestCase
from unittest.mock import patch

from swq.common.params.params import SCAParameters
from swq.qac.config_qac import create_qac_config


class TestQacConfig(TestCase):
    """ TestQacConfig class """
    def setUp(self):
        self.params = SCAParameters()
        self.qac_params = [
            param.alias.upper() for param in self.params.qac.get_all_params()
        ]
        self.exception_list = [
            'target_config', 'commandline_config', 'env_config',
            'general_config', 'merged_config', 'project_root',
            'platform_command_extension'
        ]
        self.args = {
            'project_root': 'foo/bar',
            'datastore_path': 'qac.json',
            'datastore_target': 'test'
        }
        self.general_config = {
            'qac_bin_path': '/opt/qac',
            'qac_project_path': 'qac_project'
        }
        self.target_config = {}

    @patch('swq.common.params.parameter_collector.parse_configuration_files')
    def test_qac_config_parameters(self, parse_configuration_files):
        """Test config_qac"""
        with patch('swq.common.params.params_utils.LOGGER'), \
            patch('swq.qac.config_qac.LOGGER'), \
            patch('swq.qac.config_qac.'
                  'check_if_filepath_exists_and_exit_if_not') \
                as check_filepath,\
            patch('swq.common.config.common_config.'
                  'check_if_filepath_exists_and_exit_if_not') \
                as common_check_filepath,\
            patch('swq.qac.config_qac.QacVersion') \
                as qac_version,\
            patch('swq.qac.config_qac.cli_version'),\
            patch('swq.qac.config_qac.QACConfig.'
                  '_check_for_helix_installation'),\
            patch('swq.qac.config_qac.cli_config_folder')\
                as cli_config_folder:
            cli_config_folder.return_value = 'helix/config/path'
            check_filepath.return_value = True
            common_check_filepath.return_value = True
            qac_version.return_value.major_minor.return_value = (2020, 2)
            parse_configuration_files.return_value = (self.general_config,
                                                      self.target_config)
            config = create_qac_config(self.params.qac, self.args)

        with patch('swq.common.config.common_config.'
                   'CommonConfig._get_parameter_value') \
                as get_parameter_value,\
            patch('swq.qac.config_qac.'
                  'check_if_filepath_exists_and_exit_if_not') \
                as check_filepath,\
            patch('swq.qac.config_qac.QACConfig._find_config_path'),\
            patch('swq.qac.config_qac.QacVersion'),\
            patch('swq.qac.config_qac.QACConfig.'
                  'helix_config_project_xml_path'),\
            patch('swq.common.config.common_config.'
                  'create_list_of_elements_from_file_or_list'),\
            patch('swq.qac.config_qac.QACConfig.project_git_commit'), \
            patch('swq.qac.config_qac.cli_config_folder')\
                as cli_config_folder:
            check_filepath.return_value = True
            cli_config_folder.return_value = 'helix/config/path'
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
                    self.assertIn(args[0], self.qac_params)

                get_parameter_value.reset_mock()
