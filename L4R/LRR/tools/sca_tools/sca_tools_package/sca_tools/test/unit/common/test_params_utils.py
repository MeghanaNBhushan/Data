# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_params_utils.py
# ----------------------------------------------------------------------------
"""Tests for swq.common.params/params_utils.py"""

from unittest import TestCase, mock

from swq.common.params.params_utils import collect_cli_parameters


class TestParamsUtils(TestCase):
    """TestParamsUtils class"""
    def setUp(self):
        pass

    def test_collect_cli_parameters(self):
        """Test test_collect_cli_parameters()"""
        param1_alias = 'parameter1'
        param1_value = 'value1'
        param2_alias = 'parameter2'
        param2_cli_option = 'parameter2_cli'
        param2_value = 'value2'
        param3_alias = 'parameter3'
        cli_args = {
            param1_alias: param1_value,
            param2_cli_option: param2_value,
            'not_expected_option': 'c'
        }
        param1_properties = mock.Mock(alias=param1_alias,
                                      cli_option=param1_alias)
        param2_properties = mock.Mock(alias=param2_alias,
                                      cli_option=param2_cli_option)
        param3_properties = mock.Mock(alias=param3_alias,
                                      cli_option=param3_alias)
        cli_parameters = [
            param1_properties, param2_properties, param3_properties
        ]
        expected_result = {
            param1_alias: param1_value,
            param2_alias: param2_value
        }

        actual_result = collect_cli_parameters(cli_args, cli_parameters)

        self.assertEqual(actual_result, expected_result)
