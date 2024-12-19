# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_output_producer.py
# ----------------------------------------------------------------------------
"""Tests for swq.common/output_producer.py"""

from unittest import TestCase, mock
from unittest.mock import patch

from swq.common.output_producer import create_output_producer


class TestOutputProducer(TestCase):
    """TestOutputProducer class"""
    def setUp(self):
        self.config = mock.Mock(filter_report_output_file=None, to_stdout=True)

    @patch('swq.common.output_producer.LOGGER', create=True)
    @patch('builtins.print')
    @patch('os.path.join')
    def test_create_output_producer(self, join, mocked_print, logger):
        """Test create_output_producer()"""
        mocked_print.return_value = 0

        return_data = {'key1': 'value1', 'key2': 'value2'}
        return_method = create_output_producer(self.config)
        return_method(return_data)

        expected_calls = [
            mock.call(f'{k}: {v}') for k, v in return_data.items()
        ]
        logger.info.assert_has_calls(expected_calls)

        self.config.to_stdout = False
        self.config.project_root = "foo"
        self.config.output_file = "bar"
        self.config.filter_report_output_file = 'foo/bar'

        join.return_value = 'foo/bar'

        with patch('swq.common.filesystem.filesystem_utils.open',
                   new=mock.mock_open(read_data=""),
                   create=True) as _file:
            return_method = create_output_producer(self.config)
            return_method({'field': 'value'})
            logger.info.assert_called()
            _file.assert_called_with('foo/bar',
                                     mode='wt',
                                     buffering=mock.ANY,
                                     encoding='utf-8',
                                     errors=mock.ANY,
                                     newline=mock.ANY,
                                     closefd=mock.ANY,
                                     opener=mock.ANY)
