# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_severity.py
# ----------------------------------------------------------------------------
"""Tests for qac/filter_qaview.py"""

from csv import reader
from unittest import TestCase

from swq.qac.severity import list_of_severitylevels_failed_quality_gate, \
    calculate_aggregated_summary


class TestSeverity(TestCase):
    """TestSeverity class"""
    def setUp(self):
        self.csv_data = 'Filename,Line number,Column number,\
Producer component:Message number,Message text,Severity,\
Suppression type bitmask,Suppression justification,Rule Group,\
Rule text\npath/to/header,1,1,producer,Message text,9,0,,\
"Rules,severitylevels","R1,severitylevel9"\npath/to/cpp,1,1,producer,\
Message text,6,0,,"Rule 01,severitylevels","DCL51-CPP,severitylevel6"'

        self.aggregated_summary = {
            "total_number_of_warnings_of_Severity0": 0,
            "active_number_of_warnings_of_Severity0": 0,
            "total_number_of_warnings_of_Severity1": 0,
            "active_number_of_warnings_of_Severity1": 0,
            "total_number_of_warnings_of_Severity2": 0,
            "active_number_of_warnings_of_Severity2": 0,
            "total_number_of_warnings_of_Severity3": 0,
            "active_number_of_warnings_of_Severity3": 0,
            "total_number_of_warnings_of_Severity4": 0,
            "active_number_of_warnings_of_Severity4": 0,
            "total_number_of_warnings_of_Severity5": 0,
            "active_number_of_warnings_of_Severity5": 0,
            "total_number_of_warnings_of_Severity6": 1,
            "active_number_of_warnings_of_Severity6": 1,
            "total_number_of_warnings_of_Severity7": 0,
            "active_number_of_warnings_of_Severity7": 0,
            "total_number_of_warnings_of_Severity8": 0,
            "active_number_of_warnings_of_Severity8": 0,
            "total_number_of_warnings_of_Severity9": 2,
            "active_number_of_warnings_of_Severity9": 2,
            "project_total_warnings": 2,
            "project_active_warnings": 2
        }

    def test_list_of_severitylevels_failed_quality_gate_without_fails(self):
        """ Tests list_of_severitylevels_failed_quality_gate method
        with empty fail_threshold """
        fail_threshold = {}
        actual_severitylevels_failed_quality_gate = \
            list_of_severitylevels_failed_quality_gate(
                self.aggregated_summary,
                fail_threshold
            )

        expected_severitylevels_failed_quality_gate = []

        self.assertEqual(actual_severitylevels_failed_quality_gate,
                         expected_severitylevels_failed_quality_gate)

    def test_list_of_severitylevels_failed_quality_gate_with_fails(self):
        """ Tests list_of_severitylevels_failed_quality_gate method
        with defined fail_threshold that should fail """
        fail_threshold = {"fail9": 0}
        actual_severitylevels_failed_quality_gate = \
            list_of_severitylevels_failed_quality_gate(
                self.aggregated_summary,
                fail_threshold
            )

        expected_severitylevels_failed_quality_gate = ["9"]

        self.assertEqual(actual_severitylevels_failed_quality_gate,
                         expected_severitylevels_failed_quality_gate)

    def test_list_of_severitylevels_failed_quality_gate_with_defined_fails(
            self):
        """ Tests list_of_severitylevels_failed_quality_gate method
        with defined fail_threshold that should not fail """
        fail_threshold = {"fail9": 3}
        actual_severitylevels_failed_quality_gate = \
            list_of_severitylevels_failed_quality_gate(
                self.aggregated_summary,
                fail_threshold
            )

        expected_severitylevels_failed_quality_gate = []

        self.assertEqual(actual_severitylevels_failed_quality_gate,
                         expected_severitylevels_failed_quality_gate)

    def test_calculate_aggregated_summary(self):
        csv_data = reader(self.csv_data.split('\n'),
                          delimiter=',',
                          quotechar='"')
        with_subdiagnostics = False
        actual_aggregated_summary = calculate_aggregated_summary(
            csv_data, with_subdiagnostics)
        expected_aggregated_summary = {
            'total_number_of_warnings_of_Severity0': 0,
            'active_number_of_warnings_of_Severity0': 0,
            'total_number_of_warnings_of_Severity0_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity0_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity0_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity1': 0,
            'active_number_of_warnings_of_Severity1': 0,
            'total_number_of_warnings_of_Severity1_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity1_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity1_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity2': 0,
            'active_number_of_warnings_of_Severity2': 0,
            'total_number_of_warnings_of_Severity2_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity2_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity2_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity3': 0,
            'active_number_of_warnings_of_Severity3': 0,
            'total_number_of_warnings_of_Severity3_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity3_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity3_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity4': 0,
            'active_number_of_warnings_of_Severity4': 0,
            'total_number_of_warnings_of_Severity4_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity4_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity4_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity5': 0,
            'active_number_of_warnings_of_Severity5': 0,
            'total_number_of_warnings_of_Severity5_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity5_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity5_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity6': 1,
            'active_number_of_warnings_of_Severity6': 1,
            'total_number_of_warnings_of_Severity6_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity6_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity6_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity7': 0,
            'active_number_of_warnings_of_Severity7': 0,
            'total_number_of_warnings_of_Severity7_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity7_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity7_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity8': 0,
            'active_number_of_warnings_of_Severity8': 0,
            'total_number_of_warnings_of_Severity8_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity8_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity8_suppression_\
bitmask_5': 0,
            'total_number_of_warnings_of_Severity9': 1,
            'active_number_of_warnings_of_Severity9': 1,
            'total_number_of_warnings_of_Severity9_suppression_\
bitmask_1': 0,
            'total_number_of_warnings_of_Severity9_suppression_\
bitmask_4': 0,
            'total_number_of_warnings_of_Severity9_suppression_\
bitmask_5': 0,
            'project_total_warnings': 2,
            'project_active_warnings': 2
        }
        self.assertEqual(actual_aggregated_summary,
                         expected_aggregated_summary)
