# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename:	test_analysis_report.py
# ----------------------------------------------------------------------------
"""Tests for qac/state/report/analysis.py"""

from unittest import TestCase, mock
from unittest.mock import patch

import pandas as pd
from swq.qac.state.report import analysis as analysis_module
from swq.qac.state.report.constants import ANALYSIS_REPORT_COLUMNS, \
    SUBDIAGNOSTICS_LIGHT_COLUMNS, SUBDIAGNOSTICS_FULL_COLUMNS, \
    FILENAME_COLUMN_NAME
from swq.qac.state.transformator import STATE_ANALYSIS_TRANSFORM_QUERY

TRANSFORMED_ANALYSIS_FINDINGS = '''
[
    {
        "filepath": "file1.c",
        "line": "671",
        "column": "1",
        "producer": "qac-10.0.0",
        "padmsgnum": "0882",
        "msgtext": "Issue message",
        "severity": "9",
        "suppmask": "0",
        "suppjust": "",
        "rulegroup": "",
        "rulenum": "rb9",
        "depth": 0,
        "id": "1_25",
        "finding_origins": ""
    },
    {
        "filepath": "file2.c",
        "line": "673",
        "column": "2",
        "producer": "qac-10.0.0",
        "padmsgnum": "0882",
        "msgtext": "Issue message",
        "severity": "8",
        "suppmask": "0",
        "suppjust": "",
        "rulegroup": "",
        "rulenum": "rb8",
        "depth": 0,
        "id": "1_26",
        "finding_origins": ""
    }
]
'''


def _get_transformed_analysis():
    return pd.read_json(TRANSFORMED_ANALYSIS_FINDINGS, dtype=False)


class TestQacAnalysisReport(TestCase):
    """TestQacAnalysisReport class"""
    def setUp(self):
        self.config = mock.Mock(codeowners_file=None,
                                with_full_subdiagnostics=False,
                                with_subdiagnostics=False)
        self.state_content = mock.Mock()

    @patch.object(analysis_module, 'transform_state')
    @patch.object(analysis_module,
                  'extend_dataframe_with_codeowners_information')
    def test_create_analysis_dataframe(self, mocked_extend_codeowners,
                                       mocked_transform_state):
        """Tests create_analysis_dataframe method"""

        _expected_values = {
            'df_rows_count': 2,
            'component_msgnum': 'qac-10.0.0:0882'
        }
        mocked_transform_state.return_value = _get_transformed_analysis()

        result_df = analysis_module.create_analysis_dataframe(
            self.config, self.state_content)

        mocked_transform_state.assert_called_once_with(
            self.state_content, STATE_ANALYSIS_TRANSFORM_QUERY)
        self.assertListEqual(list(result_df.columns), ANALYSIS_REPORT_COLUMNS)
        self.assertEqual(result_df.shape[0], _expected_values['df_rows_count'])
        self.assertEqual(
            result_df['Producer component:Message number'].values.all(),
            _expected_values['component_msgnum'])
        mocked_extend_codeowners.assert_not_called()

        # Test case when 'with_full_subdiagnostics' is set
        self.config.with_full_subdiagnostics = True
        mocked_transform_state.return_value = _get_transformed_analysis()
        _expected_columns = \
            ANALYSIS_REPORT_COLUMNS + SUBDIAGNOSTICS_FULL_COLUMNS

        result_df = analysis_module.create_analysis_dataframe(
            self.config, self.state_content)

        self.assertListEqual(list(result_df.columns), _expected_columns)

        # Test case when 'with_subdiagnostics' is set
        self.config.with_subdiagnostics = True
        self.config.with_full_subdiagnostics = False
        mocked_transform_state.return_value = _get_transformed_analysis()
        _expected_columns = ANALYSIS_REPORT_COLUMNS +\
            SUBDIAGNOSTICS_LIGHT_COLUMNS

        result_df = analysis_module.create_analysis_dataframe(
            self.config, self.state_content)

        self.assertListEqual(list(result_df.columns), _expected_columns)

        # Test case when 'codeowners_file' is set
        self.config.codeowners_file = 'CODEOWNERS.txt'
        mocked_transform_state.return_value = _get_transformed_analysis()

        result_df = analysis_module.create_analysis_dataframe(
            self.config, self.state_content)

        mocked_extend_codeowners.assert_called_once_with(
            self.config, result_df, FILENAME_COLUMN_NAME)
