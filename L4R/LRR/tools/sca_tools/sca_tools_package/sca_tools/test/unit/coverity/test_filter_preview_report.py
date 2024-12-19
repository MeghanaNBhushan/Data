# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_filter_preview_report.py
# ----------------------------------------------------------------------------
"""Tests for coverity/filter_preview_report.py"""

from unittest import TestCase, mock
from unittest.mock import patch

from pandas import DataFrame
from swq.coverity.filter_preview_report import coverity_filter_report
from swq.common.return_codes import RC_TRIAGE_CLASSIFICATION_ISSUE_FOUND


class TestFilterPreviewReport(TestCase):
    """TestFilterPreviewReport class"""
    def setUp(self):
        self.config = mock.Mock(preview_report_csv='foo.csv')
        self.columns = [
            "cid", "mergeKey", "presentInComparisonSnapshot",
            "firstDetectedDateTime", "severity", "triage_owner",
            "triage_externalReference", "triage_legacy", "triage_fixTarget",
            "triage_action", "triage_classification",
            "customTriage_SeverityLevel", "first_occurence_checker",
            "first_occurence_file", "first_occurence_function",
            "first_occurence_extra", "first_occurence_mergeWithLowercaseFile",
            "first_occurence_subcategory",
            "first_occurence_mainEventLineNumber",
            "first_occurence_mainEventDescription",
            "first_occurence_componentName",
            "first_occurence_componentDefaultOwner"
        ]
        self.csv_data = [[
            3226753, "8ecaf", False, "2020-10-23T14:34:07.502Z", "Unspecified",
            "", "", "False", "Untargeted", "Undecided", "Classified",
            "Unspecified", "PARSE_ERROR", "/path/to/file/foo.cpp", "unknown",
            "opencl_kernels_objdetect.hpp", True, "none", 47, "opencl.hpp",
            "mod", ""
        ],
                         [
                             1937213, "5c3cd85d", True, "2018-09-04T",
                             "Unspecified", "", "", "False", "Untargeted",
                             "Undecided", "Classified", "Unspecified",
                             "FORWARD_NULL", "/Program 14.0/VC/include/vector",
                             "_ZNSt22_e", "_Ptr,this", True, "none", 113,
                             "Incrementing"
                         ]]

    def test_coverity_filter_report_without_exceptions(self):
        """Test coverity_filter_report without exceptions"""

        with patch('swq.coverity.filter_preview_report.LOGGER') \
                as mocked_logger,\
                patch('swq.coverity.filter_preview_report.read_csv') \
                as mocked_read, \
                patch('swq.coverity.filter_preview_report.isfile') \
                as mocked_check, \
                patch(
                'swq.coverity.filter_preview_report.create_output_producer') \
                as mocked_producer:

            mocked_check.return_value = 1
            mocked_producer.return_value = mock.Mock()
            mocked_read.return_value = DataFrame(data=self.csv_data,
                                                 columns=self.columns,
                                                 dtype='str')

            coverity_filter_report(self.config)

            mocked_producer.assert_called_with(self.config)
            mocked_check.assert_called_with(self.config.preview_report_csv)
            mocked_logger.error.assert_not_called()

    def test_coverity_filter_report_with_file_not_found_exception(self):
        """Test coverity_filter_report with file not found exceptions"""

        with patch('swq.coverity.filter_preview_report.LOGGER') \
                as mocked_logger, \
                patch('swq.coverity.filter_preview_report.read_csv') \
                as mocked_read, \
                patch('swq.coverity.filter_preview_report.isfile') \
                as mocked_check, \
                self.assertRaises(SystemExit):

            mocked_check.return_value = 0

            mocked_read.return_value = DataFrame(data=self.csv_data,
                                                 columns=self.columns,
                                                 dtype='str')

            coverity_filter_report(self.config)

        mocked_check.assert_called_with(self.config.preview_report_csv)
        mocked_logger.error.assert_called()

    def test_coverity_filter_report_with_new_issues(self):
        """Test coverity_filter_report with new triage classification issues"""

        with patch('swq.coverity.filter_preview_report.LOGGER') \
                as mocked_logger,\
                patch('swq.coverity.filter_preview_report.isfile') \
                as mocked_check, \
                patch('swq.coverity.filter_preview_report.read_csv') \
                as mocked_read, \
                patch(
                'swq.coverity.filter_preview_report.create_output_producer') \
                as mocked_producer, \
                patch('swq.coverity.filter_preview_report.log_and_exit') \
                as mocked_log_exit, \
                patch('swq.coverity.filter_preview_report.sys_exit') \
                as mocked_sys_exit:

            mocked_producer.return_value = mock.Mock()
            mocked_log_exit.return_value = 0
            mocked_check.return_value = 0
            mocked_logger.return_value = 0
            csv_data = [[
                3226753, "8ecaf", False, "2020-10-23T14:34:07.502Z",
                "Unspecified", "", "", "False", "Untargeted", "Undecided",
                "Unclassified", "Unspecified", "PARSE_ERROR",
                "/path/to/file/foo.cpp", "unknown",
                "opencl_kernels_objdetect.hpp", True, "none", 47, "opencl.hpp",
                "mod", ""
            ]]

            mocked_read.return_value = DataFrame(data=csv_data,
                                                 columns=self.columns,
                                                 dtype='str')

            coverity_filter_report(self.config)

            mocked_read.assert_called_with('foo.csv',
                                           delimiter=',',
                                           quotechar='"',
                                           keep_default_na=False,
                                           dtype=str)
            mocked_producer.assert_called_with(self.config)
            mocked_check.assert_called_with(self.config.preview_report_csv)
            mocked_log_exit.assert_called()
            mocked_sys_exit.assert_called_with(
                RC_TRIAGE_CLASSIFICATION_ISSUE_FOUND)
