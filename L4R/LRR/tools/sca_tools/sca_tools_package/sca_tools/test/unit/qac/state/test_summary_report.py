# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_summary_report.py
# ----------------------------------------------------------------------------
"""Tests for qac/state/report/summary.py"""

from unittest import TestCase, mock

import pandas as pd
from swq.qac.state.report import summary as summary_module
from swq.qac.state.report.summary import SUMMARY_COLUMN, COUNT_COLUMN
from swq.qac.state.report.constants import ANALYSIS_REPORT_COLUMNS, \
     SUBDIAGNOSTICS_FULL_COLUMNS


class TestQacSummaryReport(TestCase):
    """TestQacSummaryReport class"""
    def setUp(self):
        self.config = mock.Mock(codeowners_file=None, metrics_filter_list=[])
        self.state_content = mock.Mock()
        _columns = ANALYSIS_REPORT_COLUMNS + SUBDIAGNOSTICS_FULL_COLUMNS
        _data = [[
            'file1.c', '671', '1', 'qac-10.0.0:0882', 'Issue message', '9',
            '1', '', '', 'rb9', '1_25', 0
        ],
                 [
                     'file2.c', '673', '2', 'qac-10.0.0:0882', 'Issue message',
                     '8', '0', '', '', 'rb8', '1_26', 0
                 ]]
        self.analysis_df = pd.DataFrame(columns=_columns, data=_data)

    def test_create_summary_dataframe(self):
        """Tests create_summary_dataframe method"""
        _expected_values = {
            'active_severity_8': [1],
            'total_severity_8': [1],
            'suppressed_severity_9': [1],
            'project_active': [1],
            'project_total': [2],
            'rb9_active': [],
            'rb9_total': [1],
            'qac_component_active': [1],
            'qac_component_total': [2]
        }

        result_df = summary_module.create_summary_dataframe(self.analysis_df)

        count = result_df.query(f'`{SUMMARY_COLUMN}` ==\
                "active_number_of_warnings_of_Severity8"'
                                )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['active_severity_8'])

        count = result_df.query(f'`{SUMMARY_COLUMN}` ==\
                "total_number_of_warnings_of_Severity8"'
                                )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['total_severity_8'])

        count = result_df.query(f'`{SUMMARY_COLUMN}` ==\
                "total_number_of_warnings_of_Severity9_suppression_bitmask_1"'
                                )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['suppressed_severity_9'])

        count = result_df.query(
            f'`{SUMMARY_COLUMN}` == "project_active_warnings"'
        )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['project_active'])

        count = result_df.query(
            f'`{SUMMARY_COLUMN}` == "project_total_warnings"'
        )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['project_total'])

        count = result_df.query(f'`{SUMMARY_COLUMN}` == "rb9 active"'
                                )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['rb9_active'])

        count = result_df.query(f'`{SUMMARY_COLUMN}` == "rb9 total"'
                                )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['rb9_total'])

        count = result_df.query(
            f'`{SUMMARY_COLUMN}` == "qac-10.0.0:0882 active"'
        )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['qac_component_active'])

        count = result_df.query(
            f'`{SUMMARY_COLUMN}` == "qac-10.0.0:0882 total"'
        )[COUNT_COLUMN].values.tolist()
        self.assertEqual(count, _expected_values['qac_component_total'])
