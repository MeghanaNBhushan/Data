# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_config_merger.py
# ----------------------------------------------------------------------------
"""Test for qac/config/ncf_config_merger.py"""
from os import path

from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac.config.ncf_config_merger import NcfConfigMerger

_NCF_FILE1_CONTENT = ("rule={\'space\':\'TG\', \'type\':\'e::\',"
                      "\'pattern\':\'^E[A-Z][A-Z,a-z,0-9]+$\',"
                      "\'message\':4801}")
_NCF_FILE2_CONTENT = ("rule={\'space\':\'TG\', \'type\':\'u::\',"
                      "\'pattern\':\'^U[A-Z][A-Z,a-z,0-9]+$\',"
                      "\'message\':4801}")


def _my_mocked_open(filepath, *_args, **_kwargs):
    class FileMock:
        """ Class FileMock """
        def read(self):
            """ Method readlines """
            content = ''
            if 'file1.ncf' in filepath:
                content = _NCF_FILE1_CONTENT
            elif 'file2.ncf' in filepath:
                content = _NCF_FILE2_CONTENT
            return content

        def write(self, content: str):
            pass

        def __str__(self):
            return self.__class__.__name__

    magic_mock = mock.MagicMock()
    magic_mock.__enter__ = lambda x: FileMock()
    return magic_mock


class TestNcfConfigMerger(TestCase):
    """Test class for the qac.config.ncf_config_merger"""
    def setUp(self):
        self.merger = NcfConfigMerger('blibs', ['file1.ncf', 'file2.ncf'])
        self.expected_params = [_NCF_FILE1_CONTENT, _NCF_FILE2_CONTENT]

    def test_run(self):
        """Tests the merging of files and outputs"""

        with patch('swq.common.filesystem.filesystem_utils.open',
                   _my_mocked_open):
            return_value = self.merger.run()
            self.assertEqual(path.join('blibs', 'merged_ncf.ncf'),
                             return_value)
            with patch.object(self.merger,
                              'merge_contents') as merge_contents_mock:
                self.merger.run()
                merge_contents_mock.assert_called_with(self.expected_params)

    def test_merge_contents(self):
        """Tests the merging of files"""
        with patch('swq.common.filesystem.filesystem_utils.open',
                   _my_mocked_open),\
                patch.object(self.merger, 'merge_contents')\
                as merge_contents_mock:
            self.merger.run()
            merge_contents_mock.assert_called_with(self.expected_params)

    def test_write_output_files_input(self):
        """Tests the merging of files"""
        with patch('swq.common.filesystem.filesystem_utils.open',
                   _my_mocked_open),\
                patch.object(self.merger, '_write_output_file')\
                as write_output_file_mock:
            self.merger.run()
            expected_param = '\n'.join(self.expected_params)
            write_output_file_mock.assert_called_with(expected_param)
