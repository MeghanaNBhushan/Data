# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_compiler_warnings.py
# ----------------------------------------------------------------------------
"""Test for compiler_warnings/compiler_warnings.py"""
import os

from unittest import TestCase
from unittest.mock import patch, Mock, call, ANY as mock_any, mock_open

from swq.compiler_warnings.compilers.clang import Compiler \
    as clang_compiler
from swq.compiler_warnings.compilers.greenhills import Compiler \
    as greenhills_compiler
from swq.compiler_warnings.compilers.msvc import Compiler as msvc_compiler
from swq.compiler_warnings.compiler_warnings import \
    check_changed_files_warnings, compiler_warnings, read_changed_files, \
    set_warning_info_from_types_db, export_to_file, \
    warning_name_amount, check_warnings_thresholds, \
    filter_warnings_for_directories
from swq.compiler_warnings.compiler_warning import CompilerWarning


class TestCompilerWarnings(TestCase):
    """ TestCompilerWarnings class """
    def setUp(self):
        self.testdata_folder = os.path.join(os.path.dirname(__file__),
                                            'testdata')
        self.config = Mock(codeowners_file='',
                           export_formats=['xlsx'],
                           report_dir='report_dir',
                           report_basename='basename.txt',
                           compiler='clang',
                           compiler_log='log.txt',
                           jobs=1,
                           types_db='',
                           changed_files='',
                           black_list='',
                           threshold='',
                           threshold_file='',
                           target_directory='',
                           project_root='')

    def test_get_warnings_armclang(self):
        """ Test Clang compiler class """
        compiler = clang_compiler()
        file_path = os.path.join(self.testdata_folder,
                                 'test_warnings_armclang.txt')
        actual_amount_of_warnings = \
            len(compiler.get_warnings_from_file(file_path, 1, {}))
        expected_amount_of_warnings = 3
        self.assertEqual(actual_amount_of_warnings,
                         expected_amount_of_warnings)

    def test_get_warnings_greenhills(self):
        """ Test Greenhills compiler class """
        compiler = greenhills_compiler()
        file_path = os.path.join(self.testdata_folder,
                                 'test_warnings_greenhills.txt')
        actual_amount_of_warnings = \
            len(compiler.get_warnings_from_file(file_path, 1, {}))
        expected_amount_of_warnings = 12
        self.assertEqual(actual_amount_of_warnings,
                         expected_amount_of_warnings)

    def test_get_warnings_msvc(self):
        """ Test MSVC compiler class """
        compiler = msvc_compiler()
        file_path = os.path.join(self.testdata_folder,
                                 'test_warnings_msvc.txt')
        actual_amount_of_warnings = \
            len(compiler.get_warnings_from_file(file_path, 1, {}))
        expected_amount_of_warnings = 6
        self.assertEqual(actual_amount_of_warnings,
                         expected_amount_of_warnings)

    def test_warning_info_from_types_db(self):
        """ Test set_warning_info_from_types_db() method """
        compiler = clang_compiler()
        file_path = os.path.join(self.testdata_folder,
                                 'test_warnings_armclang.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})
        db_path = os.path.join(self.testdata_folder,
                               'test_warning_types_armclang.json')
        warnings = set_warning_info_from_types_db(warnings, db_path)
        self.assertEqual(warnings[0].type_name, "#pragma-messages")
        self.assertEqual(warnings[0].severity, "8")

    def test_export_to_file(self):
        """ Test export_to_file() method """
        compiler = clang_compiler()
        file_path = os.path.join(self.testdata_folder,
                                 'test_warnings_armclang.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})
        with patch('swq.compiler_warnings.compiler_warnings.pd') as mocked_pd,\
            patch('swq.compiler_warnings.compiler_warnings.'
                  'map_teams_components_in_dataframe') as mocked_map_teams:
            # test xlsx export
            self.config.export_formats = ['xlsx']
            export_to_file(self.config, warnings)
            mocked_pd.assert_has_calls([
                call.DataFrame.from_records().to_excel(
                    os.path.abspath(
                        os.path.join(self.config.report_dir,
                                     'basename.txt.xlsx')),
                    index=False,
                    columns=[
                        'File path', 'File name', 'Row', 'Column',
                        'Components', 'Team', 'Message', 'Severity', 'Type',
                        'Number of occurrences'
                    ])
            ])
            mocked_pd.reset_mock()

            # test csv export
            self.config.export_formats = ['csv']
            export_to_file(self.config, warnings)
            mocked_pd.assert_has_calls([
                call.DataFrame.from_records().to_csv(
                    os.path.abspath(
                        os.path.join(self.config.report_dir,
                                     'basename.txt.csv')),
                    mode='w',
                    index=False,
                    columns=[
                        'File path', 'File name', 'Row', 'Column',
                        'Components', 'Team', 'Message', 'Severity', 'Type',
                        'Number of occurrences'
                    ])
            ])
            mocked_pd.reset_mock()

            # test json export
            self.config.export_formats = ['json']
            export_to_file(self.config, warnings)
            mocked_pd.assert_has_calls([
                call.DataFrame.from_records().reindex().to_json(
                    os.path.abspath(
                        os.path.join(self.config.report_dir,
                                     'basename.txt.json')),
                    orient='records')
            ])
            mocked_map_teams.assert_not_called()
            mocked_pd.reset_mock()
            mocked_map_teams.reset_mock()

            # test codeowners
            self.config.export_formats = []
            self.config.codeowners_file = 'codeowners.txt'
            export_to_file(self.config, warnings)
            mocked_map_teams.assert_called_once_with(mock_any, 'Team',
                                                     'Components', self.config)
            mocked_pd.reset_mock()

    def test_warning_name_amount(self):
        """ Test warning_name_amount() method """
        compiler = clang_compiler()
        file_path = os.path.join(self.testdata_folder,
                                 'test_warnings_armclang.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})

        warnings_type_name = '#pragma-messages'
        actual_amount = warning_name_amount(warnings, warnings_type_name)
        expected_amount = 2

        self.assertEqual(expected_amount, actual_amount)

    def test_check_warnings_thresholds(self):
        """ Test check_warnings_thresholds() method """
        compiler = clang_compiler()
        file_path = os.path.join(self.testdata_folder,
                                 'test_warnings_armclang.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})

        threshold_file = 'some_file'
        threshold_file_data = '''
        [{"warning_name":"none","threshold":1},{"warning_name":"none1","threshold":0}]
        '''
        # success check
        with patch('swq.compiler_warnings.compiler_warnings.open_t',
                   new=mock_open(read_data=threshold_file_data)) \
                as mocked_open_t, \
            patch('swq.compiler_warnings.compiler_warnings.sys_exit') \
                as mocked_sys_exit:
            check_warnings_thresholds(threshold_file, warnings)
            mocked_open_t.assert_called_with(threshold_file)
            mocked_sys_exit.assert_not_called()
            mocked_open_t.reset_mock()

        # failed check
        threshold_file_data = '''
        [{"warning_name":"#pragma-messages","threshold":1}]
        '''
        with patch('swq.compiler_warnings.compiler_warnings.open_t',
                   new=mock_open(read_data=threshold_file_data)) \
                as mocked_open_t, \
            patch('swq.compiler_warnings.compiler_warnings.sys_exit') \
                as mocked_sys_exit:
            check_warnings_thresholds(threshold_file, warnings)
            mocked_open_t.assert_called_with(threshold_file)
            mocked_sys_exit.assert_called_once_with(12)
            mocked_open_t.reset_mock()

        # infinity check
        threshold_file_data = '''
        [{"warning_name":"#pragma-messages","threshold":-1}]
        '''
        with patch('swq.compiler_warnings.compiler_warnings.open_t',
                   new=mock_open(read_data=threshold_file_data)) \
                as mocked_open_t, \
            patch('swq.compiler_warnings.compiler_warnings.sys_exit') \
                as mocked_sys_exit:
            check_warnings_thresholds(threshold_file, warnings)
            mocked_open_t.assert_called_with(threshold_file)
            mocked_sys_exit.assert_not_called()
            mocked_open_t.reset_mock()

    def test_read_changed_files(self):
        """ Test read_changed_files() method """

        # Has warnings lines
        changed_files_files = ['file1.txt']
        changed_files_data = 'filename,123,456,789'
        with patch('swq.compiler_warnings.compiler_warnings.open_t',
                   new=mock_open(read_data=changed_files_data)) \
                as mocked_open_t:
            actual_changed_files = read_changed_files(changed_files_files)
            expected_changed_files = {}
            expected_changed_files['filename'] = [123, 456, 789]
            self.assertEqual(expected_changed_files, actual_changed_files)
            mocked_open_t.assert_called_with(changed_files_files[0])

        # Has no warnings lines
        changed_files_files = ['file1.txt']
        changed_files_data = 'filename,'
        with patch('swq.compiler_warnings.compiler_warnings.open_t',
                   new=mock_open(read_data=changed_files_data)) \
                as mocked_open_t:
            actual_changed_files = read_changed_files(changed_files_files)
            expected_changed_files = {}
            expected_changed_files['filename'] = [-1]
            self.assertEqual(expected_changed_files, actual_changed_files)
            mocked_open_t.assert_called_with(changed_files_files[0])

        # Has no lines
        changed_files_files = ['file1.txt']
        changed_files_data = ''
        with patch('swq.compiler_warnings.compiler_warnings.open_t',
                   new=mock_open(read_data=changed_files_data)) \
                as mocked_open_t:
            actual_changed_files = read_changed_files(changed_files_files)
            expected_changed_files = {}
            self.assertEqual(expected_changed_files, actual_changed_files)
            mocked_open_t.assert_called_with(changed_files_files[0])

        # Has no comma-separated values
        changed_files_files = ['file1.txt']
        changed_files_data = 'filename'
        with patch('swq.compiler_warnings.compiler_warnings.open_t',
                   new=mock_open(read_data=changed_files_data)) \
                as mocked_open_t:
            actual_changed_files = read_changed_files(changed_files_files)
            expected_changed_files = {}
            expected_changed_files['filename'] = []
            self.assertEqual(expected_changed_files, actual_changed_files)
            mocked_open_t.assert_called_with(changed_files_files[0])

    def test_check_changed_files_warnings(self):
        """ Test check_changed_files_warnings() method """
        changed_files = {'some_path': ''}
        warnings = [CompilerWarning('some_path', 2, 3, 'msg')]
        output_file = ''

        # has no changes
        with patch('swq.compiler_warnings.compiler_warnings.open_t') \
                as mocked_open_t:
            expected_relevant_warnings = [
                CompilerWarning('some_path', 2, 3, 'msg')
            ]
            actural_relevant_warnings = check_changed_files_warnings(
                changed_files, warnings, output_file)

            self.assertEqual(expected_relevant_warnings,
                             actural_relevant_warnings)
            mocked_open_t.assert_not_called()

        changed_files = {'some_path': [2]}
        warnings = [CompilerWarning('some_path', 2, 3, 'msg')]
        output_file = ''

        # has changed row
        with patch('swq.compiler_warnings.compiler_warnings.open_t') \
                as mocked_open_t:
            expected_relevant_warnings = [
                CompilerWarning('some_path', 2, 3, 'msg')
            ]
            actural_relevant_warnings = check_changed_files_warnings(
                changed_files, warnings, output_file)

            self.assertEqual(expected_relevant_warnings,
                             actural_relevant_warnings)
            mocked_open_t.assert_not_called()

        changed_files = {'some_path': [3]}
        warnings = [CompilerWarning('some_path', 2, 3, 'msg')]
        output_file = ''

        # skip
        with patch('swq.compiler_warnings.compiler_warnings.open_t') \
                as mocked_open_t:
            expected_relevant_warnings = []
            actural_relevant_warnings = check_changed_files_warnings(
                changed_files, warnings, output_file)

            self.assertEqual(expected_relevant_warnings,
                             actural_relevant_warnings)
            mocked_open_t.assert_not_called()

        changed_files = {'some_path_new': [3]}
        warnings = [CompilerWarning('some_path', 2, 3, 'msg')]
        output_file = ''

        # no warnings-file_path in changed_files
        with patch('swq.compiler_warnings.compiler_warnings.open_t') \
                as mocked_open_t:
            expected_relevant_warnings = []
            actural_relevant_warnings = check_changed_files_warnings(
                changed_files, warnings, output_file)

            self.assertEqual(expected_relevant_warnings,
                             actural_relevant_warnings)
            mocked_open_t.assert_not_called()

        changed_files = {'some_path': [2]}
        warnings = [CompilerWarning('some_path', 2, 3, 'msg')]
        output_file = 'output.txt'

        # write to output file
        with patch('swq.compiler_warnings.compiler_warnings.open_t') \
                as mocked_open_t:
            expected_relevant_warnings = [
                CompilerWarning('some_path', 2, 3, 'msg')
            ]
            actural_relevant_warnings = check_changed_files_warnings(
                changed_files, warnings, output_file)

            self.assertEqual(expected_relevant_warnings,
                             actural_relevant_warnings)
            mocked_open_t.assert_has_calls([
                call(output_file, 'w'),
                call().__enter__(),
                call().__enter__().write('some_path:2\n\tmsg'),
                call().__exit__(None, None, None)
            ])

    def test_filter_warnings_for_directories(self):
        """ Test filter_warnings_for_directories() method """
        main_warning = CompilerWarning(os.path.normpath('repo_root/main.cpp'),
                                       2, 3, 'msg')
        sample_warning = CompilerWarning(
            os.path.normpath('repo_root/sample.cpp'), 2, 3, 'msg')
        tokens = ['main.cpp']
        warnings = [main_warning, sample_warning]
        expected_result = [main_warning]
        actual_result = filter_warnings_for_directories(warnings, tokens)

        self.assertEqual(expected_result, actual_result)

    def test_compiler_warnings(self):
        """ Test compiler_warnings() method """
        # Test without parameters
        with patch('swq.compiler_warnings.compiler_warnings.prepare_project'
                   ) as mock_prepare_project, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'get_file_name_path_mapping') as mock_mapping, \
                patch('swq.compiler_warnings.compiler_warnings.importlib') \
                    as mock_importlib, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'filter_warnings') as mock_filter_warnings, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'filter_warnings_for_directories') \
                          as mock_fw_for_directories, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'set_warning_info_from_types_db') as mock_set_warning, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'print_all_warnings') as mock_print_all_warnings, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'export_to_file') as mock_export_to_file:
            mocked_compiler = Mock()
            mock_mapping.return_value = {}
            mock_importlib.import_module.return_value = mocked_compiler
            mock_fw_for_directories.return_value = ['fw_directories']
            mock_filter_warnings.return_value = ['filtered']
            mock_set_warning.return_value = ['set']
            compiler_warnings(self.config)
            mock_prepare_project.assert_called_once_with(self.config)
            mock_filter_warnings.assert_called_once_with(
                mocked_compiler.Compiler().get_warnings_from_file())
            mock_fw_for_directories.assert_not_called()
            mock_set_warning.assert_not_called()
            mock_print_all_warnings.assert_has_calls([call(['filtered'])])
            mock_export_to_file.assert_called_once_with(
                self.config, ['filtered'])

        # Test with parameters
        self.config.types_db = os.path.normpath('types_db_filepath')
        self.config.changed_files = os.path.normpath('changed_files.txt')
        self.config.black_list = ['black', 'list']
        self.config.threshold = 5
        self.config.threshold_file = os.path.normpath('threshold_file.txt')
        self.config.output = 'file.txt'

        project_root_folder = os.path.normpath('project_root')
        self.config.project_root = os.path.normpath(project_root_folder)
        self.config.target_directory = [
            os.path.normpath(os.path.join(project_root_folder, 'target1')),
            os.path.normpath(os.path.join(project_root_folder, 'target2'))
        ]

        blacklist_read_data = 'black_list_read_data'

        with patch('swq.compiler_warnings.compiler_warnings.prepare_project'
                   ) as mock_prepare_project, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'get_file_name_path_mapping') as mock_mapping, \
                patch('swq.compiler_warnings.compiler_warnings.importlib') \
                    as mock_importlib, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'filter_warnings') as mock_filter_warnings, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'filter_warnings_for_directories') \
                          as mock_fw_for_directories, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'set_warning_info_from_types_db') as mock_set_warning, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'print_all_warnings') as mock_print_all_warnings, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'export_to_file') as mock_export_to_file, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'check_warnings_thresholds') as mock_check_threshold, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'read_changed_files') as mock_read_changed_files, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'check_changed_files_warnings') \
                           as mock_changed_files_warnings, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'check_if_filepath_exists_and_exit_if_not') \
                          as mock_check_filepath, \
                patch('swq.compiler_warnings.compiler_warnings.open',
                      new=mock_open(read_data=blacklist_read_data)), \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'black_list_filter') as mock_black_list, \
                patch('swq.compiler_warnings.compiler_warnings.'
                      'sys_exit') as mock_sys_exit:
            mocked_compiler = Mock()
            mock_mapping.return_value = {}
            mock_importlib.import_module.return_value = mocked_compiler
            mock_fw_for_directories.return_value = ['fw_directories']
            mock_check_filepath.return_value = True
            mock_filter_warnings.return_value = ['filtered']
            mock_set_warning.return_value = ['set_warnings']
            mock_read_changed_files.return_value = ['changed_files']
            mock_black_list.return_value = ['filtered_with_black_list']
            mock_changed_files_warnings.return_value = [
                'checked_changed_files_warnings'
            ]
            compiler_warnings(self.config)

            mock_mapping.assert_called_once_with(self.config.project_root)
            mock_filter_warnings.assert_called_once_with(
                mocked_compiler.Compiler().get_warnings_from_file())
            mock_fw_for_directories.assert_called_once_with(
                ['filtered'], ['/target1', '/target2'])
            mock_black_list.assert_has_calls([
                call(['black_list_read_data'],
                     ['checked_changed_files_warnings']),
                call(['black_list_read_data'], ['filtered_with_black_list'])
            ])
            mock_set_warning.assert_called_once_with(['fw_directories'],
                                                     os.path.abspath(
                                                         self.config.types_db))
            mock_read_changed_files.assert_called_once_with(
                self.config.changed_files)
            mock_changed_files_warnings.assert_called_once_with(
                ['changed_files'], ['set_warnings'], self.config.output)
            mock_check_filepath.assert_has_calls([
                call(self.config.get_parameter_name(),
                     self.config.black_list[0]),
                call(self.config.get_parameter_name(),
                     self.config.black_list[1])
            ])
            mock_print_all_warnings.assert_called_once_with(
                ['filtered_with_black_list'])
            mock_export_to_file.assert_called_once_with(
                self.config, ['filtered_with_black_list'])
            mock_check_threshold.assert_called_once_with(
                os.path.abspath(self.config.threshold_file),
                ['filtered_with_black_list'])
            mock_sys_exit.assert_not_called()

            # Reset mocks
            mock_mapping.reset_mock()
            mock_filter_warnings.reset_mock()
            mock_fw_for_directories.reset_mock()
            mock_set_warning.reset_mock()
            mock_read_changed_files.reset_mock()
            mock_changed_files_warnings.reset_mock()
            mock_check_filepath.reset_mock()
            mock_print_all_warnings.reset_mock()
            mock_export_to_file.reset_mock()
            mock_check_threshold.reset_mock()
            mock_black_list.reset_mock()
            mock_sys_exit.reset_mock()

            # Test threshold exceeding warnings > 0
            self.config.threshold = 1

            mocked_compiler = Mock()
            mock_mapping.return_value = {}
            mock_importlib.import_module.return_value = mocked_compiler
            mock_fw_for_directories.return_value = ['fw_directories']
            mock_check_filepath.return_value = True
            mock_filter_warnings.return_value = ['filtered']
            mock_set_warning.return_value = ['set_warnings']
            mock_read_changed_files.return_value = ['changed_files']
            mock_black_list.return_value = [
                'filtered_with_black_list1', 'filtered_with_black_list2'
            ]
            mock_changed_files_warnings.return_value = [
                'checked_changed_files_warnings'
            ]
            compiler_warnings(self.config)
            mock_sys_exit.assert_called_once_with(12)

            # Reset mocks
            mock_mapping.reset_mock()
            mock_filter_warnings.reset_mock()
            mock_fw_for_directories.reset_mock()
            mock_set_warning.reset_mock()
            mock_read_changed_files.reset_mock()
            mock_changed_files_warnings.reset_mock()
            mock_check_filepath.reset_mock()
            mock_print_all_warnings.reset_mock()
            mock_export_to_file.reset_mock()
            mock_check_threshold.reset_mock()
            mock_black_list.reset_mock()
            mock_sys_exit.reset_mock()
            mock_importlib.reset_mock()

            # Test raise ImportError
            mock_sys_exit.side_effect = SystemExit
            with self.assertRaises(SystemExit) as se:
                mock_importlib.import_module.side_effect = ImportError
                self.assertRaises(compiler_warnings(self.config), ImportError)
                self.assertEqual(se.exception.code, -1)
