# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_project_state.py
# ----------------------------------------------------------------------------
""" Tests for coverity/project_state.py """
from unittest import TestCase, mock
from unittest.mock import patch
from swq.coverity import project_state
from swq.coverity.project_state import ProjectState


class TestCovProjectState(TestCase):
    """ TestCovProjectState class """
    def setUp(self):
        self.config = mock.Mock(project_git_commit='123',
                                project_root='project/root',
                                coverity_project_path='project/path',
                                cli_version_string=None,
                                compiler_list=["--gcc"],
                                project_reports_path='project/reports',
                                with_cid=None,
                                cov_errors_json_filepath='cov_errors.json')
        self.project_state = ProjectState(self.config)
        self.mock_logger = patch("swq.coverity.project_state.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_generate_consolidated_json(self):
        """ Test _generate_consolidated_json() """
        json_data = '{}'
        found_tus = {
            'total_numberof_tus': 6,
            'numberof_failed_tus': 1,
            'percentage_of_successful_tus': 83
        }

        with patch.object(project_state, 'list_translation_units') \
                as mock_list_translation_units, \
                patch.object(ProjectState, 'export_errors'), \
                patch('swq.common.filesystem.filesystem_utils.open',
                      new=mock.mock_open(read_data=json_data)):

            mock_list_translation_units.return_value = found_tus
            result_state = self.project_state.create()
            expected_analysis = {}
            self.assertEqual(result_state['analysis'], expected_analysis)
            self.assertEqual(result_state['number_of_found_tus'],
                             found_tus['total_numberof_tus'])
            self.assertEqual(result_state['number_of_failed_tus'],
                             found_tus['numberof_failed_tus'])

        json_data = '{\
"issues" : [\
    {\
    "mergeKey" : "123456abc",\
    "checkerName" : "PW.INCLUDE_RECURSION",\
    "subcategory" : "none",\
    "extra" : "#include <opencv2/core/base.hpp>",\
    "domain" : "STATIC_C",\
    "language" : "C++",\
    "mainEventFilePathname" : "/opencv2/core/check.hpp",\
    "strippedMainEventFilePathname" : "opencv2/core/check.hpp",\
    "mainEventLineNumber" : 8,\
    "checkerProperties" : {\
        "category" : "Build system issues",\
        "cweCategory" : "none",\
        "issueKinds" : [\
          "QUALITY"\
        ],\
        "impact" : "Low",\
        "subcategoryLocalEffect" : "Compilation errors.",\
        "subcategoryLongDescription" : "Recursion in included header files"\
      }\
    }\
    ]\
}'

        expected_analysis['analyzed_file'] = 'opencv2/core/check.hpp'
        expected_analysis['cid'] = ''
        expected_analysis['merge_key'] = '123456abc'
        expected_analysis['line'] = 8
        expected_analysis['issue_kinds'] = ['QUALITY']
        with patch.object(project_state, 'list_translation_units') \
                as mock_list_translation_units, \
                patch.object(ProjectState, 'export_errors'), \
                patch('swq.common.filesystem.filesystem_utils.open',
                      new=mock.mock_open(read_data=json_data)):

            mock_list_translation_units.return_value = found_tus
            result_state = self.project_state.create()
            result_analysis_data = result_state['analysis']
            self.assertIn(expected_analysis['analyzed_file'],
                          result_analysis_data.keys())
            result_findings = result_analysis_data[
                expected_analysis['analyzed_file']]['findings'][0]
            self.assertEqual(result_findings['cid'], expected_analysis['cid'])
            self.assertEqual(result_findings['merge_key'],
                             expected_analysis['merge_key'])
            self.assertEqual(result_findings['line'],
                             expected_analysis['line'])
            self.assertEqual(result_findings['issue_kinds'],
                             expected_analysis['issue_kinds'])

        preview_report_json = '{\
"issueInfo" : [{\
    "cid" : 1234,\
    "mergeKey" : "123456abc"\
    }]\
}'

        self.config.with_cid = True
        expected_analysis['cid'] = 1234
        with patch.object(project_state, 'list_translation_units') \
                as mock_list_translation_units, \
                patch.object(ProjectState, 'export_errors'), \
                patch.object(ProjectState, 'export_preview_report'), \
                patch('swq.common.filesystem.filesystem_utils.open',
                      new=mock.mock_open(read_data=json_data)) \
                as mock_file_open:

            handlers = (
                mock_file_open.return_value,
                mock.mock_open(read_data=preview_report_json).return_value,
            )
            mock_file_open.side_effect = handlers

            mock_list_translation_units.return_value = found_tus
            result_state = self.project_state.create()
            result_analysis_data = result_state['analysis']
            result_findings = result_analysis_data[
                expected_analysis['analyzed_file']]['findings'][0]
            self.assertEqual(result_findings['cid'], expected_analysis['cid'])

    def test_export_preview_report(self):
        """Tests export_preview_report()"""
        with patch.object(project_state, 'create_dirs_if_necessary') \
                as mock_create_dirs_if_necessary, \
                patch.object(project_state, 'cov_commit_defects') \
                as mock_cov_commit_defects, \
                patch.object(
                    project_state,
                    'check_return_code_for_cmd_and_exit_if_failed') \
                as mock_check_return_code:

            preview_report_json = '/foo/bar/json_output.json'
            return_code = 0
            mock_create_dirs_if_necessary.return_value = preview_report_json
            mock_cov_commit_defects.return_value = [
                'Command Output', return_code
            ]
            self.project_state.export_preview_report()
            mock_cov_commit_defects.assert_called_once_with(
                self.config, preview_report_json)
            mock_check_return_code.assert_called_once_with(return_code)

    def test_export_errors(self):
        """Tests export_errors()"""
        with patch.object(project_state, 'create_dirs_if_necessary') \
                as mock_create_dirs_if_necessary, \
                patch.object(project_state, 'coverity_export_errors_json') \
                as mock_coverity_export_errors_json, \
                patch.object(project_state, 'coverity_export_errors_html') \
                as mock_coverity_export_errors_html, \
                patch.object(
                        project_state,
                        'check_return_code_for_cmd_and_exit_if_failed') \
                as mock_check_return_code:

            # with_native_html_report is False
            self.config.with_native_html_report = False
            return_code = 0
            mock_create_dirs_if_necessary.return_value = \
                self.config.cov_errors_json_filepath
            mock_coverity_export_errors_json.return_value = [
                'Command Output', return_code
            ]
            self.project_state.export_errors()
            mock_coverity_export_errors_json.assert_called_once_with(
                self.config, self.config.cov_errors_json_filepath)
            mock_check_return_code.assert_called_once_with(return_code)
            mock_coverity_export_errors_html.assert_not_called()

            # reset mocks
            mock_coverity_export_errors_json.reset_mock()
            mock_coverity_export_errors_html.reset_mock()

            # with_native_html_report is True
            self.config.with_native_html_report = True
            return_code = 0
            mock_create_dirs_if_necessary.return_value = \
                self.config.cov_errors_json_filepath
            mock_coverity_export_errors_json.return_value = [
                'Command Output', return_code
            ]
            mock_coverity_export_errors_html.return_value = [
                'Command Output', return_code
            ]
            self.project_state.export_errors()
            mock_coverity_export_errors_json.assert_called_once_with(
                self.config, self.config.cov_errors_json_filepath)
            mock_coverity_export_errors_html.assert_called_once_with(
                self.config)
