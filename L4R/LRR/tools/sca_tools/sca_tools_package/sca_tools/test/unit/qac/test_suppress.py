# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_suppress.py
# ----------------------------------------------------------------------------
""" Tests for qac/suppress.py """

import os

from json import loads
from unittest import TestCase, mock
from unittest.mock import patch, call
from subprocess import CalledProcessError
from swq.qac import suppress


class TestSuppress(TestCase):
    """ TestSuppress class """
    def setUp(self):
        self.config = mock.Mock(project_root='project/root',
                                via_path=None,
                                qac_modules=None)

    def test_suppress_file_in_static_list_s(self):
        """ Test suppress_file_in_static_list_s """

        modified_buildlog = 'foo.txt'
        modified_buildlog_filtered = modified_buildlog + '.fil'
        original_json = '[{\
"directory": "src/build_commands",\
"command": "gcc -o foo/fileA.obj -c src/fileA.cpp",\
"file": "src/fileA.cpp"\
}]'

        with patch('swq.qac.suppress.LOGGER'), \
                patch('swq.qac.suppress.dump') as mocked_dump:
            with patch('swq.common.filesystem.filesystem_utils.open',
                       new_callable=mock.mock_open,
                       read_data=original_json) as mocked_open:
                handlers = (mocked_open.return_value,
                            mock.mock_open().return_value)
                mocked_open.side_effect = handlers
                result = suppress.suppress_file_in_static_list_s(
                    modified_buildlog, [])
                self.assertEqual(result, modified_buildlog_filtered)
                mocked_open.assert_called_with(modified_buildlog_filtered,
                                               mode='wt',
                                               buffering=mock.ANY,
                                               encoding='utf-8',
                                               errors=mock.ANY,
                                               newline=mock.ANY,
                                               closefd=mock.ANY,
                                               opener=mock.ANY)
                mocked_dump.assert_called_with(loads(original_json),
                                               handlers[1],
                                               sort_keys=True,
                                               indent=4,
                                               ensure_ascii=False)
                mocked_open.reset_mock()
            with patch('swq.common.filesystem.filesystem_utils.open',
                       new_callable=mock.mock_open,
                       read_data=original_json) as mocked_open:
                handlers = (mocked_open.return_value,
                            mock.mock_open().return_value)
                mocked_open.side_effect = handlers
                result = suppress.suppress_file_in_static_list_s(
                    modified_buildlog, [])
                self.assertEqual(result, modified_buildlog_filtered)
                mocked_open.assert_called_with(modified_buildlog_filtered,
                                               mode='wt',
                                               buffering=mock.ANY,
                                               encoding='utf-8',
                                               errors=mock.ANY,
                                               newline=mock.ANY,
                                               closefd=mock.ANY,
                                               opener=mock.ANY)
                mocked_dump.assert_called_with(loads(original_json),
                                               handlers[1],
                                               sort_keys=True,
                                               indent=4,
                                               ensure_ascii=False)

    def test_suppress_file_in_static_list_s_build_log(self):
        """ Test suppress_file_in_static_list_s_build_log """

        file_list_path = 'foo'
        modified_buildlog = 'bar'
        modified_buildlog_filtered = modified_buildlog + '.fil'

        with patch('swq.qac.suppress.LOGGER'), \
                patch('swq.common.filesystem.filesystem_utils.open',
                      new_callable=mock.mock_open) as mocked_open:
            handlers = (mocked_open.return_value,
                        mock.mock_open().return_value,
                        mock.mock_open().return_value)
            mocked_open.side_effect = handlers
            result = suppress.suppress_file_in_static_list_s_build_log(
                modified_buildlog, file_list_path)
            self.assertEqual(result, modified_buildlog_filtered)
            mocked_open.assert_called()
            self.assertEqual(mocked_open.call_count, 2)
            expected_calls = [
                call(os.path.abspath(modified_buildlog),
                     mode='rt',
                     buffering=1,
                     encoding='utf-8',
                     errors='replace',
                     newline=None,
                     closefd=True,
                     opener=None),
                call('bar.fil',
                     mode='wt',
                     buffering=1,
                     encoding='utf-8',
                     errors='replace',
                     newline=None,
                     closefd=True,
                     opener=None)
            ]
            self.assertIn(expected_calls, mocked_open.call_args_list)

    def test_suppress_c_header(self):
        """ Test suppress_c_header """

        self.config.via_path = 'foo/bar'
        via_file = os.path.join(self.config.via_path, 'suppress_h.via')
        with patch('swq.qac.suppress.LOGGER'), \
                patch.object(suppress, '_get_analysis_excluded_header_paths')\
                as mock_get_analysis_excluded_header_paths, \
                patch.object(suppress, '_create_opt_file'), \
                patch.object(suppress, 'qac_suppress') as mock_qac_suppress:

            mock_get_analysis_excluded_header_paths.return_value = 'header.h'
            expected_result = (
                via_file, mock_get_analysis_excluded_header_paths.return_value)
            result = suppress.suppress_c_header(self.config)
            self.assertEqual(result, expected_result)

            self.config.qac_modules = ['module1', 'module2']
            result = suppress.suppress_c_header(self.config)
            self.assertEqual(result, expected_result)
            mock_qac_suppress.assert_called_with(self.config,
                                                 self.config.qac_modules[1],
                                                 via_file)
            self.assertEqual(mock_qac_suppress.call_count, 2)

    def test_suppress_file_in_static_list_a(self):
        """ Test suppress_file_in_static_list_a """

        self.config.via_path = 'foo/bar'
        via_file = os.path.join(self.config.via_path, 'suppress_file_list.via')
        with patch('swq.qac.suppress.LOGGER') as logger, \
                patch.object(suppress, 'makedirs'), \
                patch.object(suppress, '_create_opt_file'), \
                patch.object(suppress, 'qac_suppress') as mock_qac_suppress:

            result = suppress.suppress_file_in_static_list_a(
                self.config, 'filelist.txt')
            self.assertEqual(result, via_file)

            self.config.qac_modules = ['module1', 'module2']
            result = suppress.suppress_file_in_static_list_a(
                self.config, 'filelist.txt')
            self.assertEqual(result, via_file)
            mock_qac_suppress.assert_called_with(self.config,
                                                 self.config.qac_modules[1],
                                                 via_file)
            self.assertEqual(mock_qac_suppress.call_count, 2)
            mock_qac_suppress.reset_mock()

            mock_qac_suppress.side_effect = CalledProcessError(1, 'bad cmd')
            result = suppress.suppress_file_in_static_list_a(
                self.config, 'filelist.txt')
            logger.warning.assert_called()
            self.assertEqual(result, via_file)

    def test_get_analysis_excluded_header_paths(self):
        """ Test _get_analysis_excluded_header_paths """

        self.config.via_path = 'foo/bar'
        with patch('swq.qac.suppress.LOGGER'), \
                patch.object(suppress, '_create_opt_file'), \
                patch.object(suppress, '_get_all_header_files_in_directory') \
                as mock_get_all_header_files_in_directory:

            mock_get_all_header_files_in_directory.return_value = [
                'mixed/file1.hpp', 'mixed/file2.h', 'only_c/file3.h',
                'another_only_c/file4.h', 'only_cpp/file5.hpp'
            ]
            result = suppress.suppress_c_header(self.config)
            result_headers = result[1]
            result_headers.sort()
            self.assertEqual(result_headers,
                             ['another_only_c', 'mixed/file2.h', 'only_c'])
