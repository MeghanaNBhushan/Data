""" Tests for coverity/coverity.py """

import os
import sys

from unittest import TestCase, mock
from unittest.mock import patch
from swq.common.return_codes import RC_ANALYZE_ERROR
from swq.coverity import coverity


class TestCoverity(TestCase):
    """ TestCoverity class """
    def setUp(self):
        self.config = mock.Mock(compiler_list=None,
                                translation_units_blacklist=None,
                                coverity_project_path='foo/bar',
                                helper_logs_path='logs/dir',
                                webapi_view_name='test',
                                build_command='build.sh',
                                merged_file_matching_patterns=None,
                                compile_commands_json=None,
                                max_parallel_workers=None)

    def test_coverity_create(self):
        """ Test coverity_create """
        with patch('swq.coverity.coverity.LOGGER'), \
                patch.object(coverity, 'makedirs'), \
                patch.object(coverity, 'git_rev_parse'), \
                patch.object(coverity, 'create_coverity_config_for_compiler') \
                as mock_create_coverity_config_for_compiler, \
                patch.object(
                        coverity,
                        'check_return_code_for_cmd_and_exit_if_failed')\
                as mock_check_return_code, \
                patch.object(coverity, 'run_coverity_build') \
                as mock_run_coverity_build, \
                patch.object(coverity, 'list_translation_units') \
                as mock_list_translation_units, \
                patch.object(coverity, 'run_generate_compile_commands') \
                as mock_run_generate_compile_commands, \
                patch.object(coverity, 'backup_compilation_file') \
                as mock_backup_compilation_file, \
                patch.object(coverity, 'get_build_command') \
                as mockget_build_command, \
                patch.object(coverity,
                             'check_if_filepath_exists_and_exit_if_not'):

            expected_build_command = 'some_build_command.sh'
            mockget_build_command.return_value = expected_build_command
            self.config.compiler_list = ["--gcc"]
            saved_compile_commands_json = 'path/to/saved/compile_commands.json'
            mock_backup_compilation_file.return_value = \
                saved_compile_commands_json
            mock_create_coverity_config_for_compiler.return_value = [
                'Output', 0
            ]
            mock_run_coverity_build.return_value = ['Output', 0]
            mock_run_generate_compile_commands.return_value = ['Output', 0]

            self.config.compile_commands_json = 'compile_commands.json'
            coverity.coverity_create(self.config)
            mock_run_generate_compile_commands.assert_not_called()
            mock_run_coverity_build.assert_called_once_with(
                self.config, expected_build_command)
            mock_list_translation_units.assert_called_with(self.config)
            mock_create_coverity_config_for_compiler.assert_called_with(
                self.config, self.config.compiler_list[0])
            mock_check_return_code.assert_called_with(0)

    def test_coverity_analyze(self):
        """ Test coverity_analyze """
        with patch.object(coverity, 'filter_translation_units') \
            as mock_filter_translation_units, \
            patch.object(coverity, 'run_coverity_analyze') \
            as mock_run_coverity_analyze, \
            patch.object(
                coverity,
                'check_return_code_for_cmd_and_exit_if_failed') \
            as mock_check_return_code, \
            patch.object(coverity, 'list_translation_units') \
            as mock_list_translation_units:

            return_code = 0
            mock_run_coverity_analyze.return_value = ['Output', return_code]

            coverity.coverity_analyze(self.config)

            mock_filter_translation_units.assert_called_once_with(self.config)
            mock_list_translation_units.assert_called_once_with(self.config)
            mock_run_coverity_analyze.assert_called_once_with(self.config)
            mock_check_return_code.assert_called_once_with(return_code)

    def test_coverity_export(self):
        """ Test coverity_export """
        with patch('swq.coverity.coverity.LOGGER'), \
                patch('swq.coverity.coverity.ProjectState') \
                as mock_project_state, \
                patch.object(coverity, 'cov_format_errors_export') \
                as mock_cov_format_errors_export:

            coverity_json_filepath = os.path.join(
                self.config.coverity_project_path, 'export',
                'cov-format-errors', 'json-output.json')
            instance = mock_project_state.return_value
            instance.export_errors.return_value = coverity_json_filepath

            coverity.coverity_export(self.config)
            mock_cov_format_errors_export.assert_called_with(
                self.config, coverity_json_filepath)

    def test_coverity_preview_report(self):
        """ Test coverity_preview_report """
        with patch('swq.coverity.coverity.LOGGER'), \
                patch('swq.coverity.coverity.ProjectState') as \
                mock_project_state, \
                patch.object(coverity, 'cov_commit_defects_export') \
                as mock_cov_commit_defects_export:

            export_file = os.path.join(self.config.coverity_project_path,
                                       'export', 'cov_commit_defects',
                                       'preview-report.json')
            instance = mock_project_state.return_value
            instance.export_preview_report.return_value = export_file

            coverity.coverity_preview_report(self.config)
            mock_cov_commit_defects_export.assert_called_with(
                self.config, export_file)

    def test_coverity_upload(self):
        """ Test coverity_upload """
        with patch.object(coverity, 'cov_commit_defects') \
                as mock_cov_commit_defects, \
                patch.object(coverity,
                             'check_return_code_for_cmd_and_exit_if_failed'):

            mock_cov_commit_defects.return_value = ['Output', 0]
            coverity.coverity_upload(self.config)
            mock_cov_commit_defects.assert_called_with(self.config)

    def test_coverity_webapi_export(self):
        """ Test coverity_webapi_export """
        with patch.object(coverity, 'create_dirs_if_necessary'), \
                patch.object(coverity, 'coverity_connect_webapi_export') \
                as mock_coverity_connect_webapi_export:

            coverity.coverity_webapi_export(self.config)
            mock_coverity_connect_webapi_export.assert_called_with(self.config)

    @patch('swq.coverity.coverity.LOGGER')
    @patch('os.path.exists')
    def test_coverity_show_build_log_metrics(self, mock_path_exists, logger):
        """ Test coverity_show_build_log_metrics """

        mock_path_exists.return_value = False
        build_log_content = ""
        with patch('swq.coverity.coverity.open',
                   new=mock.mock_open(read_data=build_log_content)) \
                as mocked_open:
            with self.assertRaises(SystemExit) as expected_exception:
                coverity.coverity_show_build_log_metrics(self.config)
                self.assertEqual(expected_exception.exception.code, 1)
                mocked_open.assert_not_called()

        mock_path_exists.return_value = True
        build_log_content = "foo\n"
        build_log_content += "Emit for file 'foo.cpp' complete.\n"
        build_log_content += "[WARNING] something went wrong\n"
        build_log_content += "[ERROR] boom\n"
        self.config.translation_units_blacklist = [".*/modules/.*"]
        with patch('swq.coverity.coverity.open_t',
                   new=mock.mock_open(read_data=build_log_content)) \
                as mocked_open:
            with self.assertRaises(SystemExit) as expected_exception:
                coverity.coverity_show_build_log_metrics(self.config)
                logger.error.assert_called()
                self.assertEqual(expected_exception.exception.code, 1)

    @patch('swq.coverity.coverity.LOGGER')
    def testget_build_command(self, logger):
        """ Test get_build_command() method """
        with patch.object(coverity, 'backup_compilation_file') \
            as mock_backup_compilation_file, \
            patch.object(coverity, 'check_if_filepath_exists_and_exit_if_not')\
            as mock_check_if_filepath_exists, \
            patch.object(coverity, 'file_contains_cl_specific_chars') \
            as mock_file_contains_cl_specific_chars, \
            patch.object(coverity, 'apply_fix_to_cl_compile_commands') \
            as mock_apply_fix_to_cl_compile_commands, \
            patch.object(coverity, 'use_json_sync_filter') \
            as mock_use_json_sync_filter, \
            patch.object(coverity, '_generate_compile_commands') \
            as mock_generate_compile_commands, \
            patch.object(coverity, 'log_and_exit') \
            as mock_log_and_exit:

            compile_commands_json = 'compile_commands.json'
            # Only build_command is defined

            expected_build_command = 'build_command.bat'
            self.config.build_command = expected_build_command
            self.config.use_compile_commands_json = False
            self.config.compile_commands_json = None

            result = coverity.get_build_command(self.config)
            self.assertEqual(result, expected_build_command)

            mock_use_json_sync_filter.assert_not_called()
            mock_file_contains_cl_specific_chars.assert_not_called()
            mock_backup_compilation_file.assert_not_called()
            mock_check_if_filepath_exists.assert_not_called()
            mock_generate_compile_commands.assert_not_called()

            # Only compile_commands_json and use_compile_commands_json
            # is defined

            python_executable = sys.executable
            backed_up_compiled_commands_json = compile_commands_json + '.back'
            fixed_cl_compiled_commands_json = compile_commands_json + '.fixed'
            script_location = os.path.normpath('some/path/script.py')

            mock_file_contains_cl_specific_chars.return_value = True
            mock_check_if_filepath_exists.return_value = True
            mock_apply_fix_to_cl_compile_commands.return_value = \
                fixed_cl_compiled_commands_json
            mock_backup_compilation_file.return_value = \
                backed_up_compiled_commands_json

            self.config.script_location = script_location
            self.config.build_command = None
            self.config.use_compile_commands_json = True
            self.config.compile_commands_json = compile_commands_json

            result = coverity.get_build_command(self.config)

            expected_build_command = '{} {} -f {}'.format(
                python_executable, script_location,
                fixed_cl_compiled_commands_json)

            mock_generate_compile_commands.assert_called_once_with(self.config)

            self.assertEqual(result, expected_build_command)

            mock_use_json_sync_filter.assert_not_called()
            mock_file_contains_cl_specific_chars.assert_called_once_with(
                backed_up_compiled_commands_json)
            mock_backup_compilation_file.assert_called_once_with(
                compile_commands_json, self.config.helper_logs_path)
            mock_check_if_filepath_exists.assert_called_once()
            mock_apply_fix_to_cl_compile_commands.assert_called_once_with(
                backed_up_compiled_commands_json)

            mock_use_json_sync_filter.reset_mock()
            mock_file_contains_cl_specific_chars.reset_mock()
            mock_backup_compilation_file.reset_mock()
            mock_check_if_filepath_exists.reset_mock()
            mock_apply_fix_to_cl_compile_commands.reset_mock()
            mock_generate_compile_commands.reset_mock()

            # Same but using use_json_sync_filter (with defined
            # merged_file_matching_patterns)

            self.config.merged_file_matching_patterns = 'pattern'
            filtered_compile_commands = 'compile_command.json.filtered'
            mock_use_json_sync_filter.return_value = \
                filtered_compile_commands

            result = coverity.get_build_command(self.config)
            mock_use_json_sync_filter.assert_called_once_with(
                self.config.merged_file_matching_patterns,
                fixed_cl_compiled_commands_json)

            expected_build_command = '{} {} -f {}'.format(
                python_executable, script_location, filtered_compile_commands)

            self.assertEqual(result, expected_build_command)
            mock_use_json_sync_filter.assert_called_once_with(
                self.config.merged_file_matching_patterns,
                fixed_cl_compiled_commands_json)
            mock_file_contains_cl_specific_chars.assert_called_once_with(
                backed_up_compiled_commands_json)
            mock_backup_compilation_file.assert_called_once_with(
                compile_commands_json, self.config.helper_logs_path)
            mock_check_if_filepath_exists.assert_called_once()
            mock_apply_fix_to_cl_compile_commands.assert_called_once_with(
                backed_up_compiled_commands_json)

            mock_use_json_sync_filter.reset_mock()
            mock_file_contains_cl_specific_chars.reset_mock()
            mock_backup_compilation_file.reset_mock()
            mock_check_if_filepath_exists.reset_mock()
            mock_apply_fix_to_cl_compile_commands.reset_mock()
            mock_generate_compile_commands.reset_mock()

            # Build command, compile_commands_json and
            # use_compile_commands_json are defined

            self.config.max_parallel_workers = 2

            result = coverity.get_build_command(self.config)

            expected_build_command = '{} {} -f {} -t {}'.format(
                python_executable, script_location, filtered_compile_commands,
                self.config.max_parallel_workers)

            mock_generate_compile_commands.assert_called_once_with(self.config)

            self.assertEqual(result, expected_build_command)

            mock_use_json_sync_filter.assert_called_once_with(
                self.config.merged_file_matching_patterns,
                fixed_cl_compiled_commands_json)
            mock_file_contains_cl_specific_chars.assert_called_once_with(
                backed_up_compiled_commands_json)
            mock_backup_compilation_file.assert_called_once_with(
                compile_commands_json, self.config.helper_logs_path)
            mock_check_if_filepath_exists.assert_called_once()
            mock_apply_fix_to_cl_compile_commands.assert_called_once_with(
                backed_up_compiled_commands_json)

            mock_use_json_sync_filter.reset_mock()
            mock_file_contains_cl_specific_chars.reset_mock()
            mock_backup_compilation_file.reset_mock()
            mock_check_if_filepath_exists.reset_mock()
            mock_apply_fix_to_cl_compile_commands.reset_mock()
            mock_generate_compile_commands.reset_mock()

            # Build command, compile_commands_json are defined
            # use_compile_commands_json are not provided

            expected_build_command = 'build_command.bat'
            self.config.build_command = expected_build_command
            self.config.use_compile_commands_json = False

            result = coverity.get_build_command(self.config)

            mock_generate_compile_commands.assert_not_called()

            self.assertEqual(result, expected_build_command)

            mock_use_json_sync_filter.assert_not_called()
            mock_file_contains_cl_specific_chars.assert_not_called()
            mock_backup_compilation_file.assert_not_called()
            mock_check_if_filepath_exists.assert_not_called()
            mock_apply_fix_to_cl_compile_commands.assert_not_called()

            # Nothing is defined

            self.config.build_command = None
            self.config.use_compile_commands_json = None
            self.config.compile_commands_json = None

            coverity.get_build_command(self.config)

            mock_generate_compile_commands.assert_not_called()

            logger.error.assert_called_once()
            mock_log_and_exit.assert_called_once()

            mock_use_json_sync_filter.assert_not_called()
            mock_file_contains_cl_specific_chars.assert_not_called()
            mock_backup_compilation_file.assert_not_called()
            mock_check_if_filepath_exists.assert_not_called()
            mock_apply_fix_to_cl_compile_commands.assert_not_called()

    def test_coverity_run_desktop(self):
        """ Test coverity_run_desktop """
        with patch.object(coverity, 'filter_translation_units') \
            as mock_filter_translation_units, \
            patch.object(coverity, 'run_cov_run_desktop') \
            as mock_run_cov_run_desktop, \
            patch.object(
                coverity,
                'check_return_code_for_cmd_and_exit_if_failed') \
            as mock_check_return_code, \
            patch.object(coverity, 'list_translation_units') \
            as mock_list_translation_units:

            return_code = 0
            mock_run_cov_run_desktop.return_value = ['Output', return_code]

            coverity.coverity_run_desktop(self.config)

            mock_filter_translation_units.assert_called_once_with(self.config)
            mock_list_translation_units.assert_called_once_with(self.config)
            mock_run_cov_run_desktop.assert_called_once_with(self.config)
            mock_check_return_code.assert_called_once_with(return_code)

    def test_filter_translation_units(self):
        """ Test filter_translation_units """
        with patch.object(coverity, 'coverity_filter_translation_unit') \
            as mock_coverity_filter_translation_unit, \
            patch.object(coverity, 'log_and_exit') as mock_log_and_exit:

            # translation_units_blacklist is specified
            blacklist_filter = ['app1.cpp', 'app2.cpp']
            self.config.translation_units_blacklist = blacklist_filter
            # command executed without error
            mock_coverity_filter_translation_unit.return_value = ['Output', 0]

            coverity.filter_translation_units(self.config)

            expected_calls = [mock.call(self.config, blacklist_filter[0]),
                              mock.call(self.config, blacklist_filter[1])]
            mock_coverity_filter_translation_unit.assert_has_calls(
                expected_calls)
            mock_log_and_exit.assert_not_called()

            # reset mocks
            mock_coverity_filter_translation_unit.reset_mock()

            # command executed with '2' return_code
            mock_coverity_filter_translation_unit.return_value = ['Output', 2]

            coverity.filter_translation_units(self.config)

            expected_calls = [mock.call(self.config, blacklist_filter[0]),
                              mock.call(self.config, blacklist_filter[1])]
            mock_coverity_filter_translation_unit.assert_has_calls(
                expected_calls)
            mock_log_and_exit.assert_not_called()

            # reset mocks
            mock_coverity_filter_translation_unit.reset_mock()

            # command executed with non-(0, 2) exitcode

            exception = Exception('sample')
            mock_coverity_filter_translation_unit.return_value = ['Output', 3]
            mock_log_and_exit.side_effect = exception

            with self.assertRaises(Exception) as expected_exception:
                coverity.filter_translation_units(self.config)
                expected_calls = [mock.call(self.config, blacklist_filter[0])]
                self.assertEqual(expected_exception, exception)
                mock_coverity_filter_translation_unit.assert_has_calls(
                    expected_calls)
                mock_log_and_exit.assert_called_once_with(RC_ANALYZE_ERROR)

            # reset mocks
            mock_coverity_filter_translation_unit.reset_mock()
            mock_log_and_exit.reset_mock()

            # translation_units_blacklist is not specified
            self.config.translation_units_blacklist = ''

            coverity.filter_translation_units(self.config)

            mock_coverity_filter_translation_unit.assert_not_called()
            mock_log_and_exit.assert_not_called()
