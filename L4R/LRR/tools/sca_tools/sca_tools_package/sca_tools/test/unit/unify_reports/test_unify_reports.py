"""Test for a the unify_reports/unify_reports.py"""
from unittest import mock, TestCase
from unittest.mock import patch, call
import test.unit.unify_reports.qac_test_data as qac_test_data
import test.unit.unify_reports.cov_test_data as cov_test_data
from pandas.testing import assert_frame_equal

from pandas import DataFrame
from swq.unify_reports import unify_reports
from swq.unify_reports.layout import Columns, CovColumns


def _replace_get_qac_data(report_filename):
    return DataFrame(data=qac_test_data.INPUTS_TXT[report_filename],
                     columns=qac_test_data.GIVEN_COLUMNS)


def _replace_get_qac_disjunct_data(report_filename):
    return DataFrame(data=qac_test_data.INPUTS_TXT_DISJUNCT[report_filename],
                     columns=qac_test_data.GIVEN_COLUMNS)


def _replace_get_cov_data(report_filename):
    return DataFrame(data=cov_test_data.INPUTS_TXT[report_filename],
                     columns=cov_test_data.GIVEN_COLUMNS)


def _return_filename(filename):
    return filename


class TestUnifyReports(TestCase):
    """Test class for the unify_reports/unify_reports.py"""
    def setUp(self):
        self.config_qac = mock.Mock(
            unify_report_variant_input=qac_test_data.INPUTS_TXT_FILENAMES,
            unify_report_output='output.csv',
            unify_report_type='qac',
            get_absolute_path_or_relative_to_project_root=_return_filename)
        self.config_qac_disjunct = mock.Mock(
            unify_report_variant_input=qac_test_data.
            INPUTS_TXT_FILENAMES_DISJUNCT,
            unify_report_output='output.csv',
            unify_report_type='qac',
            get_absolute_path_or_relative_to_project_root=_return_filename)
        self.config_cov = mock.Mock(
            unify_report_variant_input=cov_test_data.INPUTS_TXT_FILENAMES,
            unify_report_output='output_cov.xlsx',
            unify_report_type='cov',
            get_absolute_path_or_relative_to_project_root=_return_filename)
        self.mock_logger = patch("swq.unify_reports.unify_reports.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @patch.object(unify_reports, '_get_dataframe', new=_replace_get_qac_data)
    def test_qac_reports(self):
        """Test unify_reports() for qac reports"""
        path_exists_name = \
            'check_if_filepath_exists_and_exit_if_not'
        with patch.object(unify_reports, path_exists_name),\
            patch('builtins.open'):

            # Test case merge the given reports and check the accumulated
            # sources
            actual_unified_report = unify_reports.unify_reports(
                self.config_qac)
            expected_report_data = DataFrame(
                data=qac_test_data.MERGED_REPORT,
                columns=qac_test_data.EXPECTED_COLUMNS)
            expected_summary_data = DataFrame(
                data=qac_test_data.INPUTS_SUM,
                columns=qac_test_data.SUMMARY_COLUMNS)
            actual_columns = list(
                actual_unified_report.data.columns.sort_values())
            expected_columns = list(expected_report_data.columns.sort_values())
            self.assertListEqual(actual_columns, expected_columns)

            reorder_cols = expected_report_data.columns
            actual_report_data = actual_unified_report.data[reorder_cols]
            assert_frame_equal(actual_report_data.reset_index(drop=True),
                               expected_report_data.reset_index(drop=True))

            actual_summary_data = actual_unified_report.summary
            assert_frame_equal(actual_summary_data.reset_index(drop=True),
                               expected_summary_data.reset_index(drop=True))

    @patch.object(unify_reports, "_save_worksheet")
    @patch.object(unify_reports, '_get_dataframe', new=_replace_get_cov_data)
    def test_coverity_reports(self, save_mock):
        """Test unify_reports() for coverity reports"""
        path_exists_name = \
            'check_if_filepath_exists_and_exit_if_not'
        with patch.object(unify_reports, path_exists_name):

            actual_unified_report = unify_reports.unify_reports(
                self.config_cov)

            actual_report_data = actual_unified_report.data
            actual_summary_data = actual_unified_report.summary

            expected_report_data = DataFrame(
                data=cov_test_data.MERGED_REPORT,
                columns=cov_test_data.EXPECTED_COLUMNS)
            expected_summary_data = DataFrame(
                data=cov_test_data.INPUTS_SUM,
                columns=cov_test_data.SUMMARY_COLUMNS)

            calls = [
                call(actual_unified_report.frame_exporter, 'summary',
                     actual_summary_data, Columns.COL_WIDTHS_SUMMARY),
                call(actual_unified_report.frame_exporter, 'combined',
                     actual_report_data, CovColumns.COL_WIDTHS_RESULT)
            ]
            save_mock.assert_has_calls(calls, any_order=True)

            # sort the actual report to make it compareable
            actual_columns = list(
                actual_unified_report.data.columns.sort_values())
            expected_columns = list(expected_report_data.columns.sort_values())

            self.assertListEqual(actual_columns, expected_columns)
            reorder_cols = expected_report_data.columns
            actual_report_data = actual_unified_report.data[reorder_cols]
            assert_frame_equal(actual_report_data.reset_index(drop=True),
                               expected_report_data.reset_index(drop=True))

            assert_frame_equal(actual_summary_data.reset_index(drop=True),
                               expected_summary_data.reset_index(drop=True))

    @patch.object(unify_reports,
                  '_get_dataframe',
                  new=_replace_get_qac_disjunct_data)
    def test_disjunctive_reports(self):
        """Test non overlapping reports"""
        path_exists_name = \
            'check_if_filepath_exists_and_exit_if_not'
        with patch.object(unify_reports, path_exists_name), \
            patch('builtins.open'):

            # Test case merge the given reports and check the accumulated
            # sources
            actual_unified_report = unify_reports.unify_reports(
                self.config_qac_disjunct)
            expected_report_data = DataFrame(
                data=qac_test_data.MERGED_REPORT_DISJUNCT,
                columns=qac_test_data.EXPECTED_COLUMNS)
            expected_summary_data = DataFrame(
                data=qac_test_data.INPUTS_SUM_DISJUNCT,
                columns=qac_test_data.SUMMARY_COLUMNS)
            actual_columns = list(
                actual_unified_report.data.columns.sort_values())
            expected_columns = list(expected_report_data.columns.sort_values())
            self.assertListEqual(actual_columns, expected_columns)

            reorder_cols = expected_report_data.columns
            actual_report_data = actual_unified_report.data[reorder_cols]

            assert_frame_equal(actual_report_data.reset_index(drop=True),
                               expected_report_data.reset_index(drop=True))

            actual_summary_data = actual_unified_report.summary
            assert_frame_equal(actual_summary_data.reset_index(drop=True),
                               expected_summary_data.reset_index(drop=True))
