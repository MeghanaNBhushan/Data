# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_config_compiler_warnings.py
# ----------------------------------------------------------------------------
"""Tests for compiler_warnings/config_compiler_warnings.py"""
import inspect
from unittest import TestCase
from unittest.mock import patch

from swq.common.params.params import SCAParameters
from swq.compiler_warnings.config_compiler_warnings \
    import create_compiler_warnings_config


class TestCompilerWarningsConfig(TestCase):
    """ TestCompilerWarningsConfig class """
    def setUp(self):
        self.params = SCAParameters()
        self.compiler_warnings_params = [
            param.alias.upper()
            for param in self.params.compiler_warnings.get_all_params()
        ]

        self.args = {
            'compiler': 'clang',
            'compiler_log': 'foo/bar',
            'black_list': 'bl1 bl2 bl3',
            'export_format': 'csv json',
            'changed_files': 'foo/path1 bar/path2',
            'codeowners_file': 'cp/file/path',
            'gitignore_mapping': True,
            'jobs': 5,
            'output': 'output/path',
            'quiet': False,
            'target_directory': 'foo/bar/target',
            'threshold': 105,
            'types_db': 'foo',
            'use_relative_paths': False
        }
        self.general_config = {}
        self.target_config = {}
        self.exception_list = [
            'target_config', 'commandline_config', 'env_config',
            'general_config', 'merged_config', 'project_root'
        ]

    @patch('swq.common.params.parameter_collector.parse_configuration_files')
    def test_compiler_warnings_config_parameters(self,
                                                 parse_configuration_files):
        """ Test compiler_warnings parameters """
        with patch('swq.common.params.parameter_collector.LOGGER'), \
            patch('swq.common.params.params_utils.LOGGER') \
                as check_filepath:
            check_filepath.return_value = True
            parse_configuration_files.return_value = (self.general_config,
                                                      self.target_config)
            config = create_compiler_warnings_config(
                self.params.compiler_warnings, self.args)

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
                    self.assertIn(args[0], self.compiler_warnings_params)

                get_parameter_value.reset_mock()
