# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_metrics_report.py
# ----------------------------------------------------------------------------
"""Tests for qac/state/report/metrics.py"""

from unittest import TestCase, mock
from unittest.mock import patch

import pandas as pd
from swq.qac.state.report import metrics as metrics_module
from swq.qac.state.report.constants import PATH_COLUMN_NAME
from swq.qac.state.transformator import STATE_METRICS_TRANSFORM_QUERY

TRANSFORMED_METRICS = '''
[
    {
    "path": "file1.cpp",
    "entity_name": "main",
    "entity_line": 671,
    "entity_type": "function",
    "metric_name": "STUNR",
    "metric_value": "0"
    },
    {
    "path": "file2.cpp",
    "entity_name": "main",
    "entity_line": 673,
    "entity_type": "function",
    "metric_name": "STXLN",
    "metric_value": "7"
    }
]
'''
METRICS_FILTER_LIST = ['STXLN']


class TestQacMetricsReport(TestCase):
    """TestQacMetricsReport class"""
    def setUp(self):
        self.config = mock.Mock(codeowners_file=None, metrics_filter_list=[])
        self.state_content = mock.Mock()

    @patch.object(metrics_module, 'transform_state')
    @patch.object(metrics_module,
                  'extend_dataframe_with_codeowners_information')
    def test_create_metrics_dataframe(self, mocked_extend_codeowners,
                                      mocked_transform_state):
        """Tests create_metrics_dataframe method"""

        # Test case with no metrics in state
        mocked_transform_state.return_value = pd.DataFrame([])

        result_df = metrics_module.create_metrics_dataframe(
            self.config, self.state_content)

        mocked_transform_state.assert_called_once_with(
            self.state_content, STATE_METRICS_TRANSFORM_QUERY)
        self.assertTrue(result_df.empty)
        mocked_transform_state.reset_mock()

        # Test case with metrics and no metrics filter
        _expected_values = {
            'df_rows_count': 2,
            'metric_name': ['STUNR', 'STXLN']
        }

        mocked_transform_state.return_value = pd.read_json(TRANSFORMED_METRICS,
                                                           dtype=False)

        result_df = metrics_module.create_metrics_dataframe(
            self.config, self.state_content)

        self.assertEqual(result_df.shape[0], _expected_values['df_rows_count'])
        self.assertListEqual(result_df['metric_name'].tolist(),
                             _expected_values['metric_name'])
        mocked_extend_codeowners.assert_not_called()

        # Test case when metricts filter is set
        self.config.metrics_filter_list = METRICS_FILTER_LIST.copy()
        _expected_rows_count = 1

        result_df = metrics_module.create_metrics_dataframe(
            self.config, self.state_content)

        self.assertEqual(result_df.shape[0], _expected_rows_count)
        self.assertListEqual(result_df['metric_name'].tolist(),
                             self.config.metrics_filter_list)

        # Test case when codeowners_file is set
        self.config.codeowners_file = 'CODEOWNERS.txt'

        result_df = metrics_module.create_metrics_dataframe(
            self.config, self.state_content)

        mocked_extend_codeowners.assert_called_once_with(
            self.config, result_df, PATH_COLUMN_NAME)
