# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac_populate.py
# ----------------------------------------------------------------------------
"""Tests for qac/populate.py"""

from unittest import TestCase, mock
from unittest.mock import patch
from swq.common.return_codes import RC_BUILD_ERROR, RC_SYNC_ERROR
from swq.qac import populate as qac_populate_module
from swq.qac.constants import PROJECT_GENERATION_FAILED_MESSAGE, \
    PROJECT_SYNCHRONIZATION_FAILED_MESSAGE
from swq.qac.populate import apply_json_sync_filter, filter_build_log, \
    filter_build_log_populating_file, filter_compile_commands, \
    filter_json_populating_file, filter_project_populating_input_file, \
    fix_cl_specific_chars, generate_project_populating_input_file, \
    populate_files_to_qac_project, run_build_command, \
    suppress_files_in_compile_commands


class TestQacPopulate(TestCase):
    """Tests class for QAC Populate"""
    def setUp(self):
        self.config = mock.Mock(sync_type='JSON',
                                sync_build_log_file='some_build_log',
                                actual_sync_json='actual_sync_json',
                                actual_build_log='actual_build_log')

    def test_generate_project_populating_input_file(self):
        """Tests generate_project_populating_input_file()"""
        with patch.object(qac_populate_module, 'run_build_command') \
            as mocked_run_build_command, \
            patch.object(qac_populate_module,
                         'check_if_filepath_exists_and_exit_if_not') \
                as mocked_check_if_filepath_exists_and_exit_if_not, \
            patch.object(qac_populate_module,
                         'check_if_return_code_in_skip_list') \
                as mocked_check_if_return_code_in_skip_list:
            # sync_build_command was not defined, sync_type was set to MONITOR
            self.config.sync_build_command = ''
            self.config.sync_type = 'MONITOR'

            generate_project_populating_input_file(self.config)

            mocked_run_build_command.assert_not_called()
            mocked_check_if_return_code_in_skip_list.assert_not_called()
            mocked_check_if_filepath_exists_and_exit_if_not.assert_not_called()

            # sync_build_command was not defined, sync_type was set to JSON
            self.config.sync_build_command = ''
            self.config.sync_type = 'JSON'

            generate_project_populating_input_file(self.config)

            mocked_run_build_command.assert_not_called()
            mocked_check_if_return_code_in_skip_list.assert_not_called()
            mocked_check_if_filepath_exists_and_exit_if_not.assert_not_called()

            # sync_build_command was defined, sync_type was set to JSON
            return_code = 0

            self.config.sync_build_command = 'build.extension'
            self.config.sync_type = 'JSON'
            mocked_run_build_command.return_value = return_code

            generate_project_populating_input_file(self.config)

            mocked_run_build_command.assert_called_once_with(self.config)
            mocked_check_if_return_code_in_skip_list.assert_called_once_with(
                self.config, return_code, PROJECT_GENERATION_FAILED_MESSAGE,
                RC_BUILD_ERROR)
            mocked_check_if_filepath_exists_and_exit_if_not.\
                assert_called_once()

            # reset mocks
            mocked_run_build_command.reset_mock()
            mocked_check_if_return_code_in_skip_list.reset_mock()
            mocked_check_if_filepath_exists_and_exit_if_not.reset_mock()

            # sync_build_command was defined, sync_type was set to BUILD_LOG
            return_code = 0

            self.config.sync_type = 'BUILD_LOG'
            self.config.sync_build_command = 'build.extension'
            mocked_run_build_command.return_value = return_code

            generate_project_populating_input_file(self.config)

            mocked_run_build_command.assert_called_once_with(self.config)
            mocked_check_if_return_code_in_skip_list.assert_called_once_with(
                self.config, return_code, PROJECT_GENERATION_FAILED_MESSAGE,
                RC_BUILD_ERROR)
            mocked_check_if_filepath_exists_and_exit_if_not.\
                assert_called_once()

    def test_run_build_command(self):
        """Tests run_build_command()"""
        with patch.object(qac_populate_module, 'qac_commands') \
            as mocked_qac_commands:

            return_code = 0
            message = ''
            mocked_qac_commands.build_project_with_shell.return_value = \
                [message, return_code]
            mocked_qac_commands.build_project_without_shell.return_value = \
                [message, return_code]

            # use_python_build_shell was not set
            self.config.use_python_build_shell = False

            run_build_command(self.config)

            mocked_qac_commands.build_project_without_shell.\
                assert_called_once_with(
                    self.config)
            mocked_qac_commands.build_project_with_shell.assert_not_called()

            # reset mocks
            mocked_qac_commands.reset_mock()

            # use_python_build_shell was set
            self.config.use_python_build_shell = True

            run_build_command(self.config)
            mocked_qac_commands.build_project_without_shell.assert_not_called()
            mocked_qac_commands.build_project_with_shell.\
                assert_called_once_with(
                    self.config)

    def test_filter_project_populating_input_file(self):
        """Tests filter_project_populating_input_file()"""
        with patch.object(qac_populate_module, 'filter_json_populating_file') \
            as mocked_filter_json_populating_file, \
            patch.object(qac_populate_module,
                         'filter_build_log_populating_file') \
                as mocked_filter_build_log_populating_file:

            # sync_type was set to JSON
            self.config.sync_type = 'JSON'

            filter_project_populating_input_file(self.config)

            mocked_filter_json_populating_file.assert_called_once_with(
                self.config)
            mocked_filter_build_log_populating_file.assert_not_called()

            # reset_mocks
            mocked_filter_json_populating_file.reset_mock()
            mocked_filter_build_log_populating_file.reset_mock()

            # sync_type was set to BUILD_LOG
            self.config.sync_type = 'BUILD_LOG'

            filter_project_populating_input_file(self.config)

            mocked_filter_json_populating_file.assert_not_called()
            mocked_filter_build_log_populating_file.assert_called_once_with(
                self.config)

    def test_filter_json_populating_file(self):
        """Tests filter_json_populating_file()"""
        with patch.object(qac_populate_module, 'copy_file') \
            as mocked_copy_file, \
            patch.object(qac_populate_module, 'filter_compile_commands') \
                as mocked_filter_compile_commands:

            filter_json_populating_file(self.config)
            mocked_copy_file.assert_called_once_with(
                self.config.sync_build_log_file, self.config.actual_sync_json)
            mocked_filter_compile_commands.assert_called_once_with(self.config)

    def test_filter_build_log_populating_file(self):
        """Tests filter_build_log_populating_file()"""
        with patch.object(qac_populate_module, 'copy_file') \
            as mocked_copy_file, \
            patch.object(qac_populate_module, 'filter_build_log') \
                as mocked_filter_build_log:

            filter_build_log_populating_file(self.config)
            mocked_copy_file.assert_called_once_with(
                self.config.sync_build_log_file, self.config.actual_build_log)
            mocked_filter_build_log.assert_called_once_with(self.config)

    def test_filter_compile_commands(self):
        """Tests filter_compile_commands()"""
        with patch.object(qac_populate_module, 'fix_cl_specific_chars') \
            as mocked_fix_cl_specific_chars, \
            patch.object(qac_populate_module, 'apply_json_sync_filter') \
                as mocked_apply_json_sync_filter, \
            patch.object(qac_populate_module,
                         'suppress_files_in_compile_commands') \
                as mocked_suppress_files_in_compile_commands:

            filter_compile_commands(self.config)

            mocked_fix_cl_specific_chars.assert_called_once_with(self.config)
            mocked_apply_json_sync_filter.assert_called_once_with(self.config)
            mocked_suppress_files_in_compile_commands.assert_called_once_with(
                self.config)

    def test_filter_build_log(self):
        """Tests filter_build_log()"""
        with patch.object(qac_populate_module,
                          'suppress_file_in_static_list_s_build_log') \
            as mocked_suppress_file_in_static_list_s_build_log:

            # helper_suppress_file_list_s was not set
            self.config.helper_suppress_file_list_s = ''

            filter_build_log(self.config)

            mocked_suppress_file_in_static_list_s_build_log.assert_not_called()

            # helper_suppress_file_list_s was set
            helper_suppress_file_list_s = 'filepath'
            self.config.helper_suppress_file_list_s = \
                helper_suppress_file_list_s

            filter_build_log(self.config)

            mocked_suppress_file_in_static_list_s_build_log.\
                assert_called_once_with(
                    self.config.actual_build_log,
                    helper_suppress_file_list_s, self.config.actual_build_log
                )

    def test_apply_json_sync_filter(self):
        """Tests apply_json_sync_filter()"""
        with patch.object(qac_populate_module,
                          'use_json_sync_filter') \
            as mocked_use_json_sync_filter:

            # sync_type_json_path_pattern was not set
            self.config.sync_type_json_path_pattern = ''

            apply_json_sync_filter(self.config)

            mocked_use_json_sync_filter.assert_not_called()

            # sync_type_json_path_pattern was set
            sync_type_json_path_pattern = 'filepath'
            self.config.sync_type_json_path_pattern = \
                sync_type_json_path_pattern

            apply_json_sync_filter(self.config)

            mocked_use_json_sync_filter.\
                assert_called_once_with(
                    sync_type_json_path_pattern,
                    self.config.actual_sync_json,
                    self.config.actual_sync_json
                )

    def test_fix_cl_specific_chars(self):
        """Test fix_cl_specific_chars()"""
        with patch.object(qac_populate_module,
                          'file_contains_cl_specific_chars') \
            as mocked_file_contains_cl_specific_chars, \
            patch.object(qac_populate_module,
                          'apply_fix_to_cl_compile_commands') \
            as mocked_apply_fix_to_cl_compile_commands:
            # file does not contain cl specific chars
            mocked_file_contains_cl_specific_chars.return_value = False

            fix_cl_specific_chars(self.config)

            mocked_apply_fix_to_cl_compile_commands.assert_not_called()

            # file contains cl specific chars
            mocked_file_contains_cl_specific_chars.return_value = True

            fix_cl_specific_chars(self.config)

            mocked_apply_fix_to_cl_compile_commands.assert_called_once_with(
                self.config.actual_sync_json)

    def test_suppress_files_in_compile_commands(self):
        """Tests suppress_files_in_compile_commands()"""
        with patch.object(qac_populate_module,
                          'suppress_file_in_static_list_s') \
            as mocked_suppress_file_in_static_list_s:

            # helper_suppress_file_list_s was not set
            self.config.helper_suppress_file_list_s = ''

            suppress_files_in_compile_commands(self.config)

            mocked_suppress_file_in_static_list_s.assert_not_called()

            # helper_suppress_file_list_s was set
            helper_suppress_file_list_s = 'filepath'
            self.config.helper_suppress_file_list_s = \
                helper_suppress_file_list_s

            suppress_files_in_compile_commands(self.config)

            mocked_suppress_file_in_static_list_s.\
                assert_called_once_with(
                    self.config.actual_sync_json,
                    helper_suppress_file_list_s,
                    self.config.actual_sync_json
                )

    def test_populate_files_to_qac_project(self):
        """Test populate_files_to_qac_project()"""
        with patch.object(qac_populate_module, 'qac_commands') \
            as mocked_qac_commands, \
            patch.object(qac_populate_module, 'optimize_helix_project') \
                as mocked_optimize_helix_project, \
            patch.object(qac_populate_module,
                         'check_if_return_code_in_skip_list') \
                as mocked_check_if_return_code_in_skip_list:
            return_code = 0
            message = ''
            mocked_qac_commands.sync_project_json.return_value = [
                message, return_code
            ]
            mocked_qac_commands.sync_project_build_log.return_value = [
                message, return_code
            ]
            mocked_qac_commands.sync_project_monitor.return_value = [
                message, return_code
            ]

            # sync_type was set to JSON
            self.config.sync_type = 'JSON'
            populate_files_to_qac_project(self.config)

            mocked_qac_commands.sync_project_json.assert_called_once_with(
                self.config)
            mocked_check_if_return_code_in_skip_list.assert_called_once_with(
                self.config, return_code,
                PROJECT_SYNCHRONIZATION_FAILED_MESSAGE, RC_SYNC_ERROR)

            mocked_qac_commands.sync_project_build_log.assert_not_called()
            mocked_qac_commands.sync_project_monitor.assert_not_called()

            # reset mocks
            mocked_qac_commands.reset_mock()
            mocked_check_if_return_code_in_skip_list.reset_mock()

            # sync_type was set to BUILD_LOG
            self.config.sync_type = 'BUILD_LOG'
            populate_files_to_qac_project(self.config)

            mocked_qac_commands.sync_project_build_log.assert_called_once_with(
                self.config)
            mocked_check_if_return_code_in_skip_list.assert_called_once_with(
                self.config, return_code,
                PROJECT_SYNCHRONIZATION_FAILED_MESSAGE, RC_SYNC_ERROR)

            mocked_qac_commands.sync_project_json.assert_not_called()
            mocked_qac_commands.sync_project_monitor.assert_not_called()

            # reset mocks
            mocked_qac_commands.reset_mock()
            mocked_check_if_return_code_in_skip_list.reset_mock()

            # sync_type was set to MONITOR
            self.config.sync_type = 'MONITOR'
            populate_files_to_qac_project(self.config)

            mocked_qac_commands.sync_project_monitor.assert_called_once_with(
                self.config)
            mocked_check_if_return_code_in_skip_list.assert_called_once_with(
                self.config, return_code,
                PROJECT_SYNCHRONIZATION_FAILED_MESSAGE, RC_SYNC_ERROR)
            mocked_optimize_helix_project.assert_called_once_with(
                self.config
            )

            mocked_qac_commands.sync_project_json.assert_not_called()
            mocked_qac_commands.sync_project_build_log.assert_not_called()
