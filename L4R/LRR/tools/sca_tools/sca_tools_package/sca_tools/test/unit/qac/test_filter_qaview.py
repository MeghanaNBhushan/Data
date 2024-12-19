# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_filter_qaview.py
# ----------------------------------------------------------------------------
"""Tests for qac/filter_qaview.py"""

from unittest import TestCase, mock
from unittest.mock import patch

from pandas import DataFrame
from swq.qac.filter_qaview import filter_qaview_entrypoint, \
    justifications_for_suppressed_warnings_fail_requirements
from swq.common.return_codes import RC_FINDINGS_LARGER_THAN_THRESHOLD, \
    RC_JUSTIFICATION_FAIL_CRITERIA, \
    RC_FINDINGS_AND_JUSTIFICATIONS_DO_NOT_MEET_CRITERIA


class TestFilterQAVIEW(TestCase):
    """TestFilterQAVIEW class"""
    def setUp(self):
        self.config = mock.Mock(qaview_csv='foo.csv',
                                ignore_ids=None,
                                justification_message_regexp='',
                                fail_0=0,
                                fail_1=0,
                                fail_2=0,
                                fail_3=0,
                                fail_4=0,
                                fail_5=0,
                                fail_6=0,
                                fail_7=0,
                                fail_8=0,
                                fail_9=0)

        self.csv_data = 'Filename,Line number,Column number,\
Producer component:Message number,Message text,Severity,\
Suppression type bitmask,Suppression justification,Rule Group,\
Rule text\npath/to/header,1,1,producer,Message text,9,0,,\
"Rules,severitylevels","R1,severitylevel9"\npath/to/cpp,1,1,producer,\
Message text,6,0,,"Rule 01,severitylevels","DCL51-CPP,severitylevel6"'

        self.issues_list = {
            "total_number_of_warnings_of_severitylevel0": 0,
            "active_number_of_warnings_of_severitylevel0": 0,
            "total_number_of_warnings_of_severitylevel1": 0,
            "active_number_of_warnings_of_severitylevel1": 0,
            "total_number_of_warnings_of_severitylevel2": 0,
            "active_number_of_warnings_of_severitylevel2": 0,
            "total_number_of_warnings_of_severitylevel3": 0,
            "active_number_of_warnings_of_severitylevel3": 0,
            "total_number_of_warnings_of_severitylevel4": 0,
            "active_number_of_warnings_of_severitylevel4": 0,
            "total_number_of_warnings_of_severitylevel5": 0,
            "active_number_of_warnings_of_severitylevel5": 0,
            "total_number_of_warnings_of_severitylevel6": 1,
            "active_number_of_warnings_of_severitylevel6": 1,
            "total_number_of_warnings_of_severitylevel7": 0,
            "active_number_of_warnings_of_severitylevel7": 0,
            "total_number_of_warnings_of_severitylevel8": 0,
            "active_number_of_warnings_of_severitylevel8": 0,
            "total_number_of_warnings_of_severitylevel9": 2,
            "active_number_of_warnings_of_severitylevel9": 2,
            "project_total_warnings": 2,
            "project_active_warnings": 2
        }

    def test_filter_qaview_entrypoint_without_exceptions(self):
        """Test filter_qaview_entrypoint without exceptions"""

        with patch('swq.qac.filter_qaview.LOGGER') as mocked_logger, \
                patch('swq.qac.filter_qaview.read_csv') as mocked_read, \
                patch('swq.qac.filter_qaview.'
                      'list_of_severitylevels_failed_quality_gate') \
                as mocked_list,\
                patch('swq.qac.filter_qaview.calculate_aggregated_summary') \
                as mocked_count,\
                patch('swq.qac.filter_qaview.create_output_producer') \
                as mocked_producer:

            mocked_list.return_value = 0
            mocked_count.return_value = self.issues_list
            mocked_producer.return_value = mock.Mock()
            mocked_read.return_value = \
                DataFrame(data=self.csv_data.split('\n'),
                          dtype='str')
            filter_qaview_entrypoint(self.config)
            mocked_read.assert_called_with('foo.csv',
                                           delimiter=',',
                                           quotechar='"',
                                           keep_default_na=False,
                                           dtype=str)
            mocked_list.assert_called_with(self.issues_list, {})
            mocked_producer.assert_called_with(self.config)
            mocked_logger.error.assert_not_called()

    def test_filter_qaview_entrypoint_with_faildict(self):
        """Test filter_qaview_entrypoint with fail dict"""

        self.config.fail_9 = 2

        with patch('swq.qac.filter_qaview.LOGGER') as mocked_logger, \
                patch('swq.qac.filter_qaview.read_csv') as mocked_read, \
                patch('swq.qac.filter_qaview.'
                      'list_of_severitylevels_failed_quality_gate') \
                as mocked_list,\
                patch('swq.qac.filter_qaview.calculate_aggregated_summary') \
                as mocked_count,\
                patch('swq.qac.filter_qaview.create_output_producer') \
                as mocked_producer,\
                patch('swq.qac.filter_qaview.sys_exit') as mocked_sys_exit, \
                patch('swq.qac.filter_qaview.'
                      'generate_threshold_exceeding_warnings_report') \
                as mock_generate_threshold_report:

            mocked_list.return_value = ['foo', 'bar']
            mocked_count.return_value = self.issues_list
            mocked_producer.return_value = mock.Mock()
            mocked_logger.return_value = 0
            mocked_read.return_value = \
                DataFrame(data=self.csv_data.split('\n'), dtype='str')

            filter_qaview_entrypoint(self.config)

            mocked_read.assert_called_with('foo.csv',
                                           delimiter=',',
                                           quotechar='"',
                                           keep_default_na=False,
                                           dtype=str)

            mocked_producer.assert_called_with(self.config)
            mocked_sys_exit.assert_called()
            mock_generate_threshold_report.assert_called()

    @patch('swq.qac.filter_qaview.'
           'justifications_for_suppressed_warnings_fail_requirements')
    def test_filter_qaview_entrypoint_with_failjustification(
            self, mocked_justification):
        """Test filter_qaview_entrypoint with fail justification"""

        self.config.justification_message_regexp = ["[0-9]+"]

        with patch('swq.qac.filter_qaview.LOGGER') as mocked_logger, \
                patch('swq.qac.filter_qaview.read_csv') as mocked_read, \
                patch('swq.qac.filter_qaview.'
                      'list_of_severitylevels_failed_quality_gate') \
                as mocked_list, \
                patch('swq.qac.filter_qaview.create_output_producer') \
                as mocked_producer, \
                patch('swq.qac.filter_qaview.sys_exit') as mocked_sys_exit, \
                patch('swq.qac.filter_qaview.'
                      'generate_threshold_exceeding_warnings_report') \
                as mock_generate_threshold_report:

            mocked_list.return_value = []
            mocked_producer.return_value = mock.Mock()
            mocked_logger.return_value = 0
            mocked_justification.return_value = True
            mocked_read.return_value = \
                DataFrame(data=self.csv_data.split('\n'), dtype='str')

            filter_qaview_entrypoint(self.config)

            mocked_read.assert_called_with('foo.csv',
                                           delimiter=',',
                                           quotechar='"',
                                           keep_default_na=False,
                                           dtype=str)
            mocked_sys_exit.assert_called_with(RC_JUSTIFICATION_FAIL_CRITERIA)
            mock_generate_threshold_report.assert_not_called()

    @patch('swq.qac.filter_qaview.'
           'justifications_for_suppressed_warnings_fail_requirements')
    def test_filter_qaview_entrypoint_with_failseverityleveljustification(
            self, mocked_justification):
        """Test filter_qaview_entrypoint with fail justification"""

        self.config.justification_message_regexp = ["[0-9]+"]

        with patch('swq.qac.filter_qaview.LOGGER') as mocked_logger, \
                patch('swq.qac.filter_qaview.read_csv') as mocked_read, \
                patch('swq.qac.filter_qaview.'
                      'list_of_severitylevels_failed_quality_gate') \
                as mocked_list, \
                patch('swq.qac.filter_qaview.create_output_producer') \
                as mocked_producer, \
                patch('swq.qac.filter_qaview.sys_exit') as mocked_sys_exit, \
                patch('swq.qac.filter_qaview.'
                      'generate_threshold_exceeding_warnings_report') \
                as mock_generate_threshold_report:

            mocked_list.return_value = ['foo']
            mocked_producer.return_value = mock.Mock()
            mocked_logger.return_value = 0
            mocked_justification.return_value = True

            mocked_read.return_value = \
                DataFrame(data=self.csv_data.split('\n'), dtype='str')

            filter_qaview_entrypoint(self.config)
            mocked_read.assert_called_with('foo.csv',
                                           delimiter=',',
                                           quotechar='"',
                                           keep_default_na=False,
                                           dtype=str)
            mocked_sys_exit.assert_called_with(
                RC_FINDINGS_AND_JUSTIFICATIONS_DO_NOT_MEET_CRITERIA)
            mock_generate_threshold_report.assert_called_once()

    @patch('swq.qac.filter_qaview.'
           'justifications_for_suppressed_warnings_fail_requirements')
    def test_filter_qaview_entrypoint_with_failseveritylevel(
            self, mocked_justification):
        """Test filter_qaview_entrypoint with fail severitylevel"""

        self.config.justification_message_regexp = ["[0-9]+"]

        with patch('swq.qac.filter_qaview.LOGGER') as mocked_logger, \
                patch('swq.qac.filter_qaview.read_csv') as mocked_read, \
                patch('swq.qac.filter_qaview.'
                      'list_of_severitylevels_failed_quality_gate') \
                as mocked_list, \
                patch('swq.qac.filter_qaview.create_output_producer') \
                as mocked_producer, \
                patch('swq.qac.filter_qaview.sys_exit') as mocked_sys_exit, \
                patch('swq.qac.filter_qaview.'
                      'generate_threshold_exceeding_warnings_report') \
                as mock_generate_threshold_report:

            mocked_list.return_value = ['foo']
            mocked_producer.return_value = mock.Mock()
            mocked_logger.return_value = 0
            mocked_justification.return_value = False
            mocked_read.return_value = \
                DataFrame(data=self.csv_data.split('\n'), dtype='str')

            filter_qaview_entrypoint(self.config)
            mocked_read.assert_called_with('foo.csv',
                                           delimiter=',',
                                           quotechar='"',
                                           keep_default_na=False,
                                           dtype=str)

            mocked_sys_exit.assert_called_with(
                RC_FINDINGS_LARGER_THAN_THRESHOLD)
            mock_generate_threshold_report.assert_called_once()

    @patch('swq.qac.filter_qaview.no_regex_matches')
    def test_justifications_for_suppressed_warnings_fail_requirements(
            self, mocked_no_regex_matches):
        """Test justifications_for_suppressed_warnings_fail_requirements"""
        csv_file_content = [[],
                            [
                                'object_writer.cc', '4', '6', 'qacpp-4.5.0',
                                "Message", '9', '0', '', 'Rule', 'R1'
                            ]]

        regexp = ['[0-9]']
        mocked_no_regex_matches.return_value = True
        result = justifications_for_suppressed_warnings_fail_requirements(
            csv_file_content, regexp)
        self.assertFalse(result)

        mocked_no_regex_matches.return_value = False
        result = justifications_for_suppressed_warnings_fail_requirements(
            csv_file_content, regexp)
        self.assertFalse(result)

        csv_file_content = [[
            'object_writer.cc', '4', '6', 'qacpp-4.5.0', "Message", '9', '1',
            '', 'Rule', 'R1'
        ]]

        result = justifications_for_suppressed_warnings_fail_requirements(
            csv_file_content, regexp)
        self.assertFalse(result)
        mocked_no_regex_matches.assert_called()
        result = justifications_for_suppressed_warnings_fail_requirements(
            csv_file_content, regexp)
        self.assertFalse(result)

        mocked_no_regex_matches.return_value = True
        result = justifications_for_suppressed_warnings_fail_requirements(
            csv_file_content, regexp)
        self.assertTrue(result)
