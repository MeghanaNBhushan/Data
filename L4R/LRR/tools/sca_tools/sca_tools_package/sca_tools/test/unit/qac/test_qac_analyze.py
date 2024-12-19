# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac_analyze.py
# ----------------------------------------------------------------------------
""" Tests for qac/qac_analyze.py """

from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac import qac_analyze
from swq.common.return_codes import RC_ANALYZE_ERROR


class TestQacAnalyze(TestCase):
    """ TestQacAnalyze class """
    def setUp(self):
        self.config = mock.Mock(
            c_files_analyzed_as_c=False,
            sync_type=None,
            sync_type_json_path_pattern=None,
            sync_build_log_file='swq.compile_commands.json',
            sync_build_command=None,
            use_python_build_shell=None,
            helper_suppress_c_header=None,
            helper_suppress_file_list_a=None,
            helper_suppress_file_list_s=None,
            project_root='not/existing/path',
            qacli='qacli.exe',
            qac_log_path="non/existing/path",
            qac_project_path='qac/project/path',
            qac_modules=None,
            qac_analysis_path_blacklist=None,
            qac_sync_settings_include_path=[],
            project_reports_path='qac/reports/path',
            custom_config_path="non/existing/custom_config_path",
            custom_help_path="non/existing/path",
            local_baseline_cache_filepath='another/path/files.sup',
            local_baseline_cache_dir_path='another/path',
            local_baseline_path="non/existing/local/path",
            qac_home_path="",
            qac_bin_path="non/existing/path",
            use_flist="",
            optimization='',
            verbose=None,
            rcf_file=mock.MagicMock(),
            acf_file='helix2019.2_1.5.1_ccda_cpp.acf',
            vcf_file='prqa_ccda_config_git_1.0.xml',
            ncf_file=mock.MagicMock(),
            user_messages=mock.MagicMock(),
            compiler_list=[],
            generate_html=None,
            project_git_commit=None,
            via_path=None,
            skip_exit_on_analysis_return_codes=None,
            skip_exit_on_build_return_codes=[0],
            actual_analyze_list=None)
        self.build_log = self.config.sync_build_log_file
        self.build_log_modified = self.build_log + '.tmp'
        self.build_log_with_suppress = self.build_log + '.fil'

        self.config.user_messages.get_result_filepath.return_value = \
            'user_messages.xml'
        self.config.ncf_file.get_result_filepath.return_value = 'ncf_file.ncf'
        self.config.ncf_file.get_result_filepath.return_value = 'rcf_file.rcf'

    @patch('swq.qac.qac_analyze.LOGGER', create=True)
    @patch('swq.common.return_codes.sys_exit')
    @patch('os.path.exists')
    @patch.object(qac_analyze, 'copy_files')
    def test_write_analysis_failures_to_file(self, mock_copy_files,
                                             path_exists, sysexit, logger):
        """ Test  write_analysis_failures_to_file() """

        output_log_file = 'analyze_output.log'
        return_value = 0
        path_exists.return_value = False
        self.assertEqual(
            qac_analyze.write_analysis_failures_to_file(
                self.config, output_log_file, return_value), None)

        path_exists.return_value = True
        with patch.object(qac_analyze,
                          'find_component_failures_in_analysis_output'
                          ) as mock_find_component_failures_in_analysis_output:
            expected_failures = []
            mock_find_component_failures_in_analysis_output.return_value = \
                expected_failures
            self.assertEqual(
                qac_analyze.write_analysis_failures_to_file(
                    self.config, output_log_file, return_value),
                expected_failures)
            mock_copy_files.assert_not_called()
            sysexit.assert_not_called()
            logger.error.assert_not_called()

            expected_failures = [{
                "path": "/fileA.cpp",
                "module": "qacpp",
                "return_code": "1"
            }]
            mock_find_component_failures_in_analysis_output.return_value = \
                expected_failures
            self.assertEqual(
                qac_analyze.write_analysis_failures_to_file(
                    self.config, output_log_file, return_value),
                expected_failures)
            mock_copy_files.assert_not_called()
            sysexit.assert_not_called()
            logger.error.assert_called()

            return_value = 3
            self.config.skip_exit_on_analysis_return_codes = (2, 3)
            expected_failures = [{
                "path": "/fileA.cpp",
                "module": "qacpp",
                "return_code": "1",
                "timestamp": "(123456.789)"
            }]
            mock_find_component_failures_in_analysis_output.return_value = \
                expected_failures
            self.assertEqual(
                qac_analyze.write_analysis_failures_to_file(
                    self.config, output_log_file, return_value),
                expected_failures)
            mock_copy_files.assert_not_called()
            sysexit.assert_not_called()

            return_value = 4
            expected_return_value = RC_ANALYZE_ERROR
            self.assertEqual(
                qac_analyze.write_analysis_failures_to_file(
                    self.config, output_log_file, return_value),
                expected_failures)
            mock_copy_files.assert_called_once_with(self.config.qac_log_path,
                                                    self.config.analysis_path)
            sysexit.assert_called_once_with(expected_return_value)

    @patch('swq.qac.qac_analyze.LOGGER')
    def test_find_component_failures_in_analysis_output(self, _):
        """Test find_component_failures_in_analysis_output function"""
        output_log_file = 'analyze_output.log'
        file_content_mock = 'src/fileA.cpp:qacpp:0:1:1\n'
        expected_failures = []
        with patch('swq.common.filesystem.filesystem_utils.open',
                   new=mock.mock_open(read_data=file_content_mock)):
            self.assertEqual(
                qac_analyze.find_component_failures_in_analysis_output(
                    output_log_file), expected_failures)

        file_content_mock = 'src/fileA.cpp:qacpp:1:1:1\n'
        expected_failures = [{
            "path": "/fileA.cpp",
            "module": "qacpp",
            "return_code": "1"
        }]
        with patch('swq.common.filesystem.filesystem_utils.open',
                   new=mock.mock_open(read_data=file_content_mock)):
            self.assertEqual(
                qac_analyze.find_component_failures_in_analysis_output(
                    output_log_file), expected_failures)

        file_content_mock = 'src/fileA.cpp:qacpp:-1:1:1\n'
        expected_failures = [{
            "path": "/fileA.cpp",
            "module": "qacpp",
            "return_code": "-1"
        }]
        with patch('swq.common.filesystem.filesystem_utils.open',
                   new=mock.mock_open(read_data=file_content_mock)):
            self.assertEqual(
                qac_analyze.find_component_failures_in_analysis_output(
                    output_log_file), expected_failures)

        file_content_mock = 'src/fileA.cpp:qacpp:1:1:1 (123456.789)\n'
        expected_failures = [{
            "path": "/fileA.cpp",
            "module": "qacpp",
            "return_code": "1",
            "timestamp": "(123456.789)"
        }]
        with patch('swq.common.filesystem.filesystem_utils.open',
                   new=mock.mock_open(read_data=file_content_mock)):
            self.assertEqual(
                qac_analyze.find_component_failures_in_analysis_output(
                    output_log_file), expected_failures)

    @patch('os.path.join')
    @patch.object(qac_analyze.qac_commands, 'analyze_file')
    @patch.object(qac_analyze, 'write_analysis_failures_to_file')
    def test_analyze_file_and_check(self,
                                    mock_qac_write_analysis_failures_to_file,
                                    mock_qac_commands_analyze_file,
                                    mock_qac_path_join):
        """Test analyze_file_and_check"""
        mock_qac_path_join.return_value = 'some//path'
        expected_return_value = 0
        expected_failures = ['first_file', 'second_file']
        expected_analyze_file = "some_file"
        mock_qac_commands_analyze_file.return_value = [
            'Commands Outputs', expected_return_value
        ]
        mock_qac_write_analysis_failures_to_file.return_value = \
            expected_failures

        self.assertEqual(
            qac_analyze.analyze_file_and_check(self.config,
                                               expected_analyze_file),
            (expected_return_value, expected_failures))

        mock_qac_commands_analyze_file.assert_called_with(
            self.config, expected_analyze_file,
            mock_qac_path_join.return_value)

    @patch('swq.qac.qac_analyze.LOGGER', create=True)
    @patch('os.path.exists')
    @patch.object(qac_analyze, 'analyze_file_and_check')
    def test_analyze_list_and_check(self, mock_analyze_file_and_check,
                                    mock_exists, mock_logger):
        """Test analyze_list_and_check"""
        self.config.actual_analyze_list = 'file/with/list.of.files'
        expected_argument = '-F  {}'.format(self.config.actual_analyze_list)
        expected_return_value = (0, ['file1', 'file2'])
        mock_analyze_file_and_check.return_value = expected_return_value

        mock_exists.return_value = True
        self.assertEqual(qac_analyze.analyze_list_and_check(self.config),
                         expected_return_value)
        mock_analyze_file_and_check.assert_called_once_with(
            self.config, expected_argument)
        mock_logger.error.assert_not_called()
        mock_analyze_file_and_check.reset_mock()

        mock_exists.return_value = False
        with self.assertRaises(SystemExit) as expected_exception:
            qac_analyze.analyze_list_and_check(self.config)
        self.assertEqual(expected_exception.exception.code, RC_ANALYZE_ERROR)
        mock_analyze_file_and_check.assert_not_called()
        mock_logger.error.assert_called()

    @patch('os.path.exists')
    @patch('os.path.join')
    @patch.object(qac_analyze, 'analyze_file_and_check')
    def test_analyze_project(self, mock_analyze_file, mock_qac_path_join,
                             mock_qac_path_exists):
        """ Test analyze_project() """
        mock_qac_path_join.return_value = 'some//path'
        mock_qac_path_exists.return_value = False
        self.config.analyze_list = False
        with patch.object(qac_analyze, 'copy_files')\
            as mock_copy_files,\
            patch.object(qac_analyze, 'clean_directory')\
            as mock_qac_clean_directory,\
            patch.object(qac_analyze, 'analyze_list_and_check')\
            as mock_analyze_list,\
            patch.object(qac_analyze, 'compose_analyze_list_file')\
            as mock_compose_analyze_list_file,\
            patch.object(qac_analyze, 'LOGGER'):

            expected_analyze_file_return = (0, ['file1'])
            mock_qac_clean_directory.return_value = None
            mock_analyze_file.return_value = expected_analyze_file_return
            self.assertIs(qac_analyze.analyze_project(self.config),
                          expected_analyze_file_return[0])
            mock_qac_clean_directory.assert_called_once_with(
                self.config.qac_log_path)
            mock_analyze_file.assert_called_once_with(self.config, None)
            mock_copy_files.assert_called_once_with(self.config.qac_log_path,
                                                    self.config.analysis_path)
            mock_analyze_file.reset_mock()

            self.config.use_flist = "True"
            self.config.analyze_file = "some_file"
            self.assertIs(qac_analyze.analyze_project(self.config),
                          expected_analyze_file_return[0])
            mock_analyze_file.assert_called_once_with(self.config,
                                                      self.config.analyze_file)

            expected_analyze_list_return = (0, ['file1'])
            mock_analyze_list.return_value = expected_analyze_list_return
            self.config.analyze_list = "some_file_with_list"
            mock_qac_path_exists.return_value = True
            self.assertIs(qac_analyze.analyze_project(self.config),
                          expected_analyze_file_return[0])
            mock_analyze_list.assert_called_once_with(self.config)
            mock_compose_analyze_list_file.assert_called_once_with(self.config)

            # with patch.object(qac_analyze, '_safe_remove_file')\
            #         as mock_qac_safe_remove_file:
            #     mock_qac_commands_analyze_file.return_value = [
            #         'Commands Outputs', 1
            #     ]
            #     self.assertIs(qac_analyze.analyze_project(self.config),
            #                   mock_qac_commands_analyze_file.return_value[1])
            #     mock_qac_write_analysis_failures_to_file.assert_called_with(
            #         self.config, mock_qac_path_join.return_value,
            #         mock_qac_commands_analyze_file.return_value[1])
            #     mock_qac_safe_remove_file.assert_not_called()

    def test_compose_analyze_list_file(self):
        """Tests compose_analyze_list_file method"""
        with patch.object(qac_analyze, 'copy_file') as mocked_copy_file, \
            patch.object(
                qac_analyze,
                'get_relevant_files_for_analysis_and_exit_if_none') \
                as mocked_get_relevant_files, \
                patch.object(qac_analyze, 'write_lines_to_file') \
                as mocked_write_lines_to_file:

            self.config.analyze_list = 'list.txt'
            relevant_files = ['foo', 'bar']
            mocked_get_relevant_files.return_value = relevant_files

            # sync_type is JSON
            self.config.sync_type = 'JSON'
            qac_analyze.compose_analyze_list_file(self.config)

            mocked_copy_file.assert_not_called()
            mocked_get_relevant_files.assert_called_once_with(self.config)
            mocked_write_lines_to_file.assert_called_once_with(
                self.config.actual_analyze_list, relevant_files)

            # reset mocks
            mocked_get_relevant_files.reset_mock()
            mocked_write_lines_to_file.reset_mock()

            # sync_type is MONITOR
            self.config.sync_type = 'MONITOR'

            qac_analyze.compose_analyze_list_file(self.config)

            mocked_copy_file.assert_called_once_with(
                self.config.analyze_list, self.config.actual_analyze_list)
            mocked_get_relevant_files.assert_not_called()
            mocked_write_lines_to_file.assert_not_called()

            # reset mocks
            mocked_copy_file.reset_mock()

            # sync_type is BUILD_LOG
            self.config.sync_type = 'BUILD_LOG'

            qac_analyze.compose_analyze_list_file(self.config)

            mocked_copy_file.assert_called_once_with(
                self.config.analyze_list, self.config.actual_analyze_list)
            mocked_get_relevant_files.assert_not_called()
            mocked_write_lines_to_file.assert_not_called()
