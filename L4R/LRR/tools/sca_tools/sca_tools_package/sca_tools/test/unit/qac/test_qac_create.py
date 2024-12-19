# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac_create.py
# ----------------------------------------------------------------------------
"""Tests for qac/create.py"""

from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac import create as qac_create_module
from swq.qac.constants import BASELINE_FILE_NAME
from swq.qac.create import \
    configure_exclude_filter_for_module, \
    configure_exclude_filter_for_modules, \
    configure_exclude_filter_for_sync, configure_files_suppression, \
    configure_qac_software, create_qac_project, \
    generate_analysis_filter_file, link_custom_help_pages, \
    link_help_pages_to_warnings, link_qac_builtin_help_pages, qac_create, \
    remove_files_from_qac_project, retrieve_validate_baseline_file, \
    run_post_create_qacli_commands, set_include_path_sync_setting, \
    set_baseline, prepare_directory_tree, configure_qac_project


class TestQacCreate(TestCase):
    """Tests class for QAC Create"""
    def setUp(self):
        self.config = mock.Mock(
            baseline_dirpath='path/to/baseline/dir',
            target_baseline_folder='path/to/target/baseline/dir',
            sync_type='JSON',
            max_parallel_workers=0,
            compiler_list=['gcc', 'msvc'],
            qac_home_path='qac/home',
            acf_file=mock.Mock(),
            vcf_file='vcf.file',
            ncf_file=mock.Mock(),
            rcf_file=mock.Mock(),
            user_messages=mock.Mock(),
            custom_help_path='custom_help')

    def test_configure_qac_software(self):
        """Tests configure_qac_software"""
        with patch.object(
            qac_create_module, 'ensure_license_servers_configured') \
                as mocked_ensure_license_servers_configured, \
                patch.object(qac_create_module, 'qac_commands') \
                as mocked_qac_commands:

            # max_parallel_workers is set to 0
            self.config.max_parallel_workers = 0

            configure_qac_software(self.config)

            mocked_ensure_license_servers_configured.assert_called_once_with(
                self.config)
            mocked_qac_commands.set_debug_level.assert_called_once_with(
                self.config)
            mocked_qac_commands.set_maximum_cpu.assert_not_called()

            # reset mock calls
            mocked_ensure_license_servers_configured.reset_mock()
            mocked_qac_commands.reset_mock()

            # max_parallel_workers is set to 8
            max_parallel_workers = 8
            self.config.max_parallel_workers = max_parallel_workers

            configure_qac_software(self.config)

            mocked_ensure_license_servers_configured.assert_called_once_with(
                self.config)
            mocked_qac_commands.set_debug_level.assert_called_once_with(
                self.config)
            mocked_qac_commands.set_maximum_cpu.assert_called_once_with(
                self.config)

    def test_qac_create_entypoint(self):
        """Tests qac_create()"""
        with patch.object(qac_create_module, 'configure_qac_software') \
                 as mocked_configure_qac_software, \
            patch.object(qac_create_module, 'prepare_directory_tree') \
                    as mocked_prepare_directory_tree, \
            patch.object(
                qac_create_module, 'verify_components_compatibility') \
                as mocked_verify_components_compatibility, \
            patch.object(
                qac_create_module, 'ensure_configuration_file_exists') \
                as mocked_ensure_configuration_file_exists, \
            patch.object(
                qac_create_module, 'link_help_pages_to_warnings') \
                as mocked_link_help_pages_to_warnings, \
            patch.object(qac_create_module,
                         'retrieve_validate_baseline_file') \
                as mocked_retrieve_validate_baseline_file, \
            patch.object(
                qac_create_module, 'generate_project_populating_input_file') \
                as mocked_generate_project_populating_input_file, \
            patch.object(
                qac_create_module, 'filter_project_populating_input_file') \
                as mocked_filter_project_populating_input_file, \
            patch.object(qac_create_module, 'create_qac_project') \
                as mocked_create_qac_project, \
            patch.object(qac_create_module, 'configure_qac_project') \
                as mocked_configure_qac_project, \
            patch.object(qac_create_module, 'populate_files_to_qac_project') \
                as mocked_populate_files_to_qac_project, \
            patch.object(qac_create_module, 'configure_files_suppression') \
                as mocked_configure_files_suppression, \
            patch.object(qac_create_module, 'run_post_create_qacli_commands') \
                as mocked_run_post_create_qacli_commands, \
            patch.object(qac_create_module, 'remove_files_from_qac_project') \
                as mocked_remove_files_from_qac_project:

            qac_create(self.config)

            mocked_configure_qac_software.assert_called_once_with(self.config)
            mocked_prepare_directory_tree.assert_called_once_with(self.config)
            mocked_verify_components_compatibility.assert_called_once_with(
                self.config)
            mocked_ensure_configuration_file_exists.assert_called_once_with(
                self.config)
            mocked_link_help_pages_to_warnings.\
                assert_called_once_with(self.config)
            mocked_retrieve_validate_baseline_file.\
                assert_called_once_with(self.config)
            mocked_generate_project_populating_input_file.\
                assert_called_once_with(self.config)
            mocked_filter_project_populating_input_file.\
                assert_called_once_with(self.config)
            mocked_create_qac_project.assert_called_once_with(self.config)
            mocked_configure_qac_project.assert_called_once_with(self.config)
            mocked_populate_files_to_qac_project.assert_called_once_with(
                self.config)
            mocked_configure_files_suppression.assert_called_once_with(
                self.config)
            mocked_remove_files_from_qac_project.assert_called_once_with(
                self.config)
            mocked_run_post_create_qacli_commands.assert_called_once_with(
                self.config)

    def test_retrieve_validate_baseline_file(self):
        """Tests retrieve_validate_baseline_file()"""
        with patch.object(
            qac_create_module,
            'retrieve_file_from_remote_resource') \
                as mocked_retrieve_file_from_remote_resource, \
            patch.object(
                qac_create_module,
                'validate_baseline_file') \
                    as mocked_validate_baseline_file, \
            patch.object(qac_create_module, 'os_path') as mocked_os_path, \
            patch.object(qac_create_module, 'copy_file') as mocked_copy_file:

            os_path_return_value = f'mocked/path/{BASELINE_FILE_NAME}'

            # baseline_dirpath is set, baseline will be retrieved
            # from remote resource with required validation
            mocked_os_path.join.return_value = os_path_return_value
            mocked_retrieve_file_from_remote_resource.return_value = (
                self.config.target_baseline_folder, True)

            retrieve_validate_baseline_file(self.config)

            mocked_retrieve_file_from_remote_resource.assert_called_once_with(
                self.config.baseline_dirpath,
                self.config.target_baseline_folder, BASELINE_FILE_NAME)
            mocked_os_path.join.assert_called_once_with(
                self.config.target_baseline_folder, BASELINE_FILE_NAME)
            mocked_validate_baseline_file.assert_called_once_with(
                os_path_return_value)
            mocked_copy_file.assert_not_called()

            # reset mocks
            mocked_retrieve_file_from_remote_resource.reset_mock()
            mocked_validate_baseline_file.reset_mock()
            mocked_os_path.reset_mock()

            # baseline_dirpath is set, baseline will be retrieved
            # from remote resource without required validation
            mocked_os_path.join.return_value = os_path_return_value
            mocked_retrieve_file_from_remote_resource.return_value = (
                self.config.target_baseline_folder, False)

            retrieve_validate_baseline_file(self.config)

            mocked_retrieve_file_from_remote_resource.assert_called_once_with(
                self.config.baseline_dirpath,
                self.config.target_baseline_folder, BASELINE_FILE_NAME)
            mocked_validate_baseline_file.assert_not_called()
            mocked_os_path.join.assert_not_called()
            mocked_copy_file.assert_not_called()

            # reset mocks
            mocked_retrieve_file_from_remote_resource.reset_mock()
            mocked_validate_baseline_file.reset_mock()
            mocked_os_path.reset_mock()

            # baseline_dirpath is set, baseline will not be retrieved
            # from remote resource with required validation
            mocked_os_path.join.return_value = os_path_return_value
            mocked_retrieve_file_from_remote_resource.return_value = (
                self.config.baseline_dirpath, True)

            retrieve_validate_baseline_file(self.config)

            mocked_retrieve_file_from_remote_resource.assert_called_once_with(
                self.config.baseline_dirpath,
                self.config.target_baseline_folder, BASELINE_FILE_NAME)
            mocked_validate_baseline_file.assert_called_once_with(
                os_path_return_value)
            mocked_os_path.join.assert_called_with(
                self.config.target_baseline_folder, BASELINE_FILE_NAME)
            mocked_copy_file.assert_called_once_with(os_path_return_value,
                                                     os_path_return_value)

            # reset mocks
            mocked_os_path.reset_mock()
            mocked_retrieve_file_from_remote_resource.reset_mock()
            mocked_validate_baseline_file.reset_mock()
            mocked_copy_file.reset_mock()

            # baseline_dirpath is not set
            self.config.baseline_dirpath = ''

            retrieve_validate_baseline_file(self.config)

            mocked_retrieve_file_from_remote_resource.assert_not_called()
            mocked_validate_baseline_file.assert_not_called()
            mocked_os_path.join.assert_not_called()
            mocked_copy_file.assert_not_called()

    def test_create_qac_project(self):
        """Tests create_qac_project()"""
        with patch.object(qac_create_module, 'qac_commands') \
            as mocked_qac_commands:

            expected_qacli_compiler_options = \
                ' '.join('--cct {}'.format(compiler)
                         for compiler in self.config.compiler_list)

            expected_config_files_pair = \
                [('acf', self.config.acf_file.get_result_filepath()),
                 ('rcf', self.config.rcf_file.get_result_filepath()),
                 ('vcf', self.config.vcf_file),
                 ('ncf', self.config.ncf_file.get_result_filepath()),
                 ('user-messages',
                  self.config.user_messages.get_result_filepath())]

            create_qac_project(self.config)

            mocked_qac_commands.create_qac_project.assert_called_once_with(
                self.config, expected_qacli_compiler_options,
                expected_config_files_pair)

    def test_set_include_path_sync_setting(self):
        """Tests set_include_path_sync_setting()"""
        with patch.object(qac_create_module, 'qac_commands') \
            as mocked_qac_commands:

            # qac_sync_settings_include_path is not set
            self.config.qac_sync_settings_include_path = []
            set_include_path_sync_setting(self.config)
            mocked_qac_commands.apply_sync_settings.assert_not_called()

            # qac_sync_settings_include_path is set
            qac_sync_settings_include_path = ['option1', 'option2']
            self.config.qac_sync_settings_include_path = \
                qac_sync_settings_include_path
            expected_apply_sync_settings_calls = [
                mock.call(self.config, 'INCLUDE_PATH',
                          qac_sync_settings_include_path[0]),
                mock.call(self.config, 'INCLUDE_PATH',
                          qac_sync_settings_include_path[1])
            ]

            set_include_path_sync_setting(self.config)
            mocked_qac_commands.apply_sync_settings.assert_has_calls(
                expected_apply_sync_settings_calls)

    def test_configure_qac_project(self):
        """Tests configure_qac_project()"""
        with patch.object(qac_create_module, 'qac_commands') \
            as mocked_qac_commands, \
            patch.object(qac_create_module, 'set_include_path_sync_setting') \
                as mocked_set_include_path_sync_setting, \
            patch.object(qac_create_module,
                         'configure_exclude_filter_for_modules') \
                as mocked_configure_exclude_filter_for_modules, \
            patch.object(qac_create_module,
                         'configure_exclude_filter_for_sync') \
                as mocked_configure_exclude_filter_for_sync:
            # c_files_analyzed_as_c is not set
            configure_qac_project(self.config)

            mocked_qac_commands.set_default_config.assert_called_once_with(
                self.config)
            mocked_qac_commands.setup_c_as_cpp_extensions.assert_not_called()
            mocked_configure_exclude_filter_for_sync.assert_called_once_with(
                self.config)
            mocked_configure_exclude_filter_for_modules.\
                assert_called_once_with(self.config)
            mocked_set_include_path_sync_setting.assert_called_once_with(
                self.config)

            # c_files_analyzed_as_c is set
            self.config.c_files_analyzed_as_c = False
            configure_qac_project(self.config)
            mocked_qac_commands.setup_c_as_cpp_extensions\
                .assert_called_once_with(
                    self.config)

    def test_configure_exclude_filter_for_sync(self):
        """ Test configure_exclude_filter_for_sync()"""
        with patch.object(qac_create_module, 'qac_commands') \
                as mocked_qac_commands:
            # project_sync_path_blacklist is set
            self.config.project_sync_path_blacklist = ['some/path']

            mocked_qac_commands.apply_sync_filter.return_value = \
                ['Command Output', 0]
            configure_exclude_filter_for_sync(self.config)
            mocked_qac_commands.apply_sync_filter.assert_called_with(
                self.config, self.config.project_sync_path_blacklist[0])

            # reset mocks
            mocked_qac_commands.reset_mock()

            # project_sync_path_blacklist is not set
            self.config.project_sync_path_blacklist = ''

            configure_exclude_filter_for_sync(self.config)
            mocked_qac_commands.apply_sync_filter.assert_not_called()

    def test_configure_files_suppression(self):
        """Tests configure_files_suppression()"""
        with patch.object(qac_create_module, 'suppress_c_header') \
            as mocked_suppress_c_header, \
            patch.object(qac_create_module, 'suppress_file_in_static_list_a') \
                as mocked_suppress_file_in_static_list_a:
            # helper_suppress_c_header and helper_suppress_file_list_a
            # are not set
            self.config.helper_suppress_c_header = ''
            self.config.helper_suppress_file_list_a = ''

            configure_files_suppression(self.config)

            mocked_suppress_c_header.assert_not_called()
            mocked_suppress_file_in_static_list_a.assert_not_called()

            # helper_suppress_c_header is set
            self.config.helper_suppress_c_header = 'file'

            configure_files_suppression(self.config)

            mocked_suppress_c_header.assert_called_once_with(self.config)
            mocked_suppress_file_in_static_list_a.assert_not_called()

            # reset mocks
            self.config.helper_suppress_c_header = ''
            mocked_suppress_c_header.reset_mock()

            # helper_suppress_file_list_a is set
            self.config.helper_suppress_file_list_a = 'file'

            configure_files_suppression(self.config)

            mocked_suppress_c_header.assert_not_called()
            mocked_suppress_file_in_static_list_a.assert_called_once_with(
                self.config, self.config.helper_suppress_file_list_a)

    def test_remove_files_from_qac_project(self):
        """Tests remove_files_from_qac_project()"""
        with patch.object(qac_create_module, 'qac_commands') \
            as mocked_qac_commands:
            # helper_remove_file_list is not set
            self.config.helper_remove_file_list = ''
            remove_files_from_qac_project(self.config)

            mocked_qac_commands.remove_files_from_project.assert_not_called()

            # helper_remove_file_list is set
            self.config.helper_remove_file_list = 'file'
            remove_files_from_qac_project(self.config)
            mocked_qac_commands.remove_files_from_project.\
                assert_called_once_with(
                    self.config)

    def test_set_baseline(self):
        """Tests set_baseline()"""
        with patch.object(qac_create_module, 'qac_commands') \
            as mocked_qac_commands, \
            patch.object(qac_create_module, 'os_path') as mocked_os_path:
            # baseline_filepath does not exist
            mocked_os_path.exists.return_value = False
            set_baseline(self.config)
            mocked_qac_commands.setup_baseline.assert_not_called()

            # baseline_filepath exists
            mocked_os_path.exists.return_value = True
            set_baseline(self.config)
            mocked_qac_commands.setup_baseline.assert_called_once_with(
                self.config, self.config.target_baseline_folder)

    def test_configure_exclude_filter_for_modules(self):
        """Tests configure_exclude_filter_for_modules()"""
        with patch.object(qac_create_module, 'generate_analysis_filter_file') \
            as mocked_generate_analysis_filter_file, \
            patch.object(qac_create_module,
                         'configure_exclude_filter_for_module') \
                as mocked_configure_exclude_filter_for_module:

            # qac_analysis_path_blacklist is not set
            self.config.qac_analysis_path_blacklist = []
            configure_exclude_filter_for_modules(self.config)

            mocked_generate_analysis_filter_file.assert_not_called()
            mocked_configure_exclude_filter_for_module.assert_not_called()

            # qac_analysis_path_blacklist is set with qac_modules
            blaclist_paths = ['path1', 'path2']
            qac_modules = ['qac', 'qacpp']

            self.config.qac_analysis_path_blacklist = blaclist_paths
            self.config.qac_modules = qac_modules

            configure_exclude_filter_for_modules(self.config)

            expected_configure_exclude_filter_for_module_calls = [
                mock.call(self.config, qac_modules[0]),
                mock.call(self.config, qac_modules[1])
            ]

            mocked_generate_analysis_filter_file.assert_called_once_with(
                self.config)
            mocked_configure_exclude_filter_for_module.assert_has_calls(
                expected_configure_exclude_filter_for_module_calls)

    def test_generate_analysis_filter_file(self):
        """Tests generate_analysis_filter_file()"""
        with patch.object(qac_create_module,
                          'open_t',
                          new_callable=mock.mock_open()) as mocked_open_t:
            blaclist_paths = ['path1', 'path2']
            analysis_filter_filepath = 'analysis_filter_filepath'

            self.config.analysis_filter_filepath = analysis_filter_filepath
            self.config.qac_analysis_path_blacklist = blaclist_paths

            generate_analysis_filter_file(self.config)

            expected_writeline_calls = \
                [mock.call(self.config.analysis_filter_filepath, mode='w'),
                 mock.call().__enter__(),
                 mock.call().__enter__().writelines(
                     ['-q {}\n'.format(blaclist_paths[0]),
                      '-q {}\n'.format(blaclist_paths[1])]),
                 mock.call().__exit__(None, None, None)]

            mocked_open_t.assert_has_calls(expected_writeline_calls)

    def test_configure_exclude_filter_for_module(self):
        """Tests configure_exclude_filter_for_module()"""
        with patch.object(qac_create_module, 'get_module_toolchain') \
            as mocked_get_module_toolchain, \
            patch.object(qac_create_module, 'qac_commands') \
                as mocked_qac_commands, \
            patch.object(qac_create_module,
                         'check_return_code_for_cmd_and_exit_if_failed') as \
                mocked_check_return_code_for_cmd_and_exit_if_failed:
            module = 'qacpp'
            toolchain = 'toolchain'
            return_code = 0
            message = ''

            mocked_get_module_toolchain.return_value = toolchain
            mocked_qac_commands.apply_path_blacklist.return_value = \
                [message, return_code]

            configure_exclude_filter_for_module(self.config, module)
            mocked_get_module_toolchain.assert_called_once_with(
                self.config, module)
            mocked_qac_commands.apply_path_blacklist(
                self.config, module, self.config.analysis_filter_filepath,
                toolchain)
            mocked_check_return_code_for_cmd_and_exit_if_failed.\
                assert_called_once_with(
                    return_code)

    def test_link_help_pages_to_warnings(self):
        """Tests link_help_pages_to_warnings()"""
        with patch.object(qac_create_module, 'link_custom_help_pages') \
            as mocked_link_custom_help_pages, \
            patch.object(qac_create_module, 'link_qac_builtin_help_pages') \
                as mocked_link_qac_builtin_help_pages:

            link_help_pages_to_warnings(self.config)
            mocked_link_custom_help_pages.assert_called_once_with(self.config)
            mocked_link_qac_builtin_help_pages.assert_called_once_with(
                self.config)

    def test_link_qac_builtin_help_pages(self):
        """Tests link_qac_builtin_help_pages()"""
        with patch.object(qac_create_module, 'set_builtin_qac_help') \
            as mocked_set_builtin_qac_help, \
            patch.object(qac_create_module, 'set_component_path_in_xml') \
                as mocked_set_component_path_in_xml:
            link_qac_builtin_help_pages(self.config)

            mocked_set_builtin_qac_help.assert_called_once_with(
                self.config.user_messages.get_result_filepath(),
                self.config.qac_home_path)

            mocked_set_component_path_in_xml.assert_called_once_with(
                self.config.user_messages.get_result_filepath(),
                self.config.qac_home_path)

    def test_link_custom_help_pages(self):
        """Tests link_custom_help_pages()"""
        with patch.object(qac_create_module, 'set_help_path_in_rcf') \
            as mocked_set_help_path_in_rcf, \
            patch.object(qac_create_module, 'set_help_path_in_user_messages') \
                as mocked_set_help_path_in_user_messages, \
            patch.object(qac_create_module, 'set_bosch_custom_help') \
                as mocked_set_bosch_custom_help:
            # help_pages_root_dir is not set
            self.config.help_pages_root_dir = ''

            expected_set_bosch_custom_help_calls = [
                mock.call(self.config.rcf_file.get_result_filepath(),
                          self.config.custom_help_path),
                mock.call(self.config.user_messages.get_result_filepath(),
                          self.config.custom_help_path)
            ]

            link_custom_help_pages(self.config)

            mocked_set_help_path_in_rcf.assert_not_called()
            mocked_set_help_path_in_user_messages.assert_not_called()

            mocked_set_bosch_custom_help.assert_has_calls(
                expected_set_bosch_custom_help_calls)

            # reset mocks
            mocked_set_bosch_custom_help.reset_mock()

            # help_pages_root_dir is set
            self.config.help_pages_root_dir = 'filepath'

            expected_set_bosch_custom_help_calls = [
                mock.call(self.config.rcf_file.get_result_filepath(),
                          self.config.custom_help_path),
                mock.call(self.config.user_messages.get_result_filepath(),
                          self.config.custom_help_path)
            ]

            link_custom_help_pages(self.config)

            mocked_set_help_path_in_rcf.assert_called_once_with(
                self.config.rcf_file.get_result_filepath(),
                self.config.help_pages_root_dir)
            mocked_set_help_path_in_user_messages.assert_called_once_with(
                self.config.user_messages.get_result_filepath(),
                self.config.help_pages_root_dir)
            mocked_set_bosch_custom_help.assert_has_calls(
                expected_set_bosch_custom_help_calls)

            # reset mocks
            mocked_set_bosch_custom_help.reset_mock()
            mocked_set_help_path_in_user_messages.reset_mock()
            mocked_set_help_path_in_rcf.reset_mock()

            # custom_help_path is not set
            # help_pages_root_dir is not set

            self.config.help_pages_root_dir = ''
            self.config.custom_help_path = ''

            link_custom_help_pages(self.config)

            mocked_set_help_path_in_rcf.assert_not_called()
            mocked_set_help_path_in_user_messages.assert_not_called()
            mocked_set_bosch_custom_help.assert_not_called()

    def test_prepare_directory_tree(self):
        """Tests prepare_directory_tree()"""

        with patch.object(qac_create_module, 'cleanup_qac_project_directory') \
            as mocked_cleanup_qac_project_directory, \
            patch.object(qac_create_module, 'remove_qac_export_directories') \
                as mocked_remove_qac_export_directories, \
            patch.object(qac_create_module,
                         'ensure_qac_project_directory_tree_created') \
                as mocked_ensure_qac_project_directory_tree_created, \
            patch.object(qac_create_module,
                         'ensure_qac_exports_directory_tree_created') \
                as mocked_ensure_qac_exports_directory_tree_created:

            # cleanup_on_create is set to False
            self.config.cleanup_on_create = False

            prepare_directory_tree(self.config)

            mocked_remove_qac_export_directories.assert_not_called()
            mocked_cleanup_qac_project_directory.assert_not_called()

            mocked_ensure_qac_project_directory_tree_created.\
                assert_called_once_with(self.config)

            mocked_ensure_qac_exports_directory_tree_created.\
                assert_called_once_with(self.config)

            # reset mocks
            mocked_ensure_qac_project_directory_tree_created.reset_mock()
            mocked_ensure_qac_exports_directory_tree_created.reset_mock()

            # cleanup_on_create is set to True

            self.config.cleanup_on_create = True

            prepare_directory_tree(self.config)

            mocked_remove_qac_export_directories.assert_called_once_with(
                self.config)
            mocked_cleanup_qac_project_directory.assert_called_once_with(
                self.config)

            mocked_ensure_qac_project_directory_tree_created.\
                assert_called_once_with(self.config)

            mocked_ensure_qac_exports_directory_tree_created.\
                assert_called_once_with(self.config)

    def test_run_post_create_qacli_commands(self):
        """Tests run_post_create_qacli_commands()"""
        with patch.object(qac_create_module, 'qac_commands') \
            as mocked_qac_commands:
            message = ''
            return_code = 0
            mocked_qac_commands.run_qacli_command.return_value = \
                [message, return_code]

            # qacli_post_create_commands is not defined
            self.config.qacli_post_create_commands = []

            run_post_create_qacli_commands(self.config)

            mocked_qac_commands.run_qacli_command.assert_not_called()

            # qacli_post_create_commands was defined with single command
            commands = ['foo bar']
            self.config.qacli_post_create_commands = commands

            run_post_create_qacli_commands(self.config)

            mocked_qac_commands.run_qacli_command.assert_called_once_with(
                self.config, commands[0])

            # reset mocks
            mocked_qac_commands.reset_mock()

            # qacli_post_create_commands was defined with multiple commands
            commands = ['foo bar', 'bar foo']
            self.config.qacli_post_create_commands = commands

            run_post_create_qacli_commands(self.config)

            expected_run_qacli_command_calls = [
                mock.call(self.config, commands[0]),
                mock.call(self.config, commands[1])
            ]

            mocked_qac_commands.run_qacli_command.assert_has_calls(
                expected_run_qacli_command_calls)
