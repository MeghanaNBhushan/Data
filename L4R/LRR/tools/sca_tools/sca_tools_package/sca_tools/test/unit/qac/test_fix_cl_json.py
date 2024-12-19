# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_fix_cl_json.py
# ----------------------------------------------------------------------------
""" Tests for qac/fix_cl_json.py """

import json

from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac import fix_cl_json


class TestFixJinjaJson(TestCase):
    """ TestFixJinjaJson class """
    def setUp(self):
        self.config = mock.Mock(input_cl_json=None)

    def test_fix_cl_json_entrypoint(self):
        """ Test fix_cl_json_entrypoint """

        self.config.input_cl_json = 'foo.json'
        modified_file = self.config.input_cl_json + '.fixed.json'
        json_data = '[{\
"directory": "foo/bar",\
"command": "gcc -o fileA.c.obj -c fileA.c",\
"file": "fileA.c"\
}]'

        with patch('swq.common.file.file_utils.LOGGER'), \
                patch('swq.common.file.file_utils.load_json_file') \
                as mock_load_json_file, \
                patch('swq.common.filesystem.filesystem_utils.open',
                      new_callable=mock.mock_open,) \
                as mocked_open, \
                patch('json.dump') as mocked_json_dump:

            mock_load_json_file.return_value = json.loads(json_data)
            fix_cl_json.fix_cl_json_entrypoint(self.config)
            mocked_open.assert_called_with(modified_file,
                                           mode='wt',
                                           buffering=mock.ANY,
                                           encoding='utf-8',
                                           errors=mock.ANY,
                                           newline=mock.ANY,
                                           closefd=mock.ANY,
                                           opener=mock.ANY)
            mocked_json_dump.assert_called_with(json.loads(json_data),
                                                mocked_open.return_value,
                                                sort_keys=True,
                                                indent=4,
                                                ensure_ascii=False)
            mocked_open.reset_mock()
            mocked_json_dump.reset_mock()
            mock_load_json_file.reset_mock()

        json_data = '[{\
"directory": "foo/bar",\
"command": "gcc -o fileA.c.obj -c fileA.c @<< \\r\\n <<",\
"file": "fileA.c"\
}]'

        expected_json_data = '[{\
"directory": "foo/bar",\
"command": "gcc -o fileA.c.obj -c fileA.c   ",\
"file": "fileA.c"\
}]'

        with patch('swq.common.file.file_utils.LOGGER'), \
                patch('swq.common.file.file_utils.load_json_file') \
                as mock_load_json_file, \
                patch('swq.common.filesystem.filesystem_utils.open',
                      new_callable=mock.mock_open,) \
                as mocked_open, \
                patch('json.dump') as mocked_json_dump:

            mock_load_json_file.return_value = json.loads(json_data)
            fix_cl_json.fix_cl_json_entrypoint(self.config)
            mocked_open.assert_called_with(modified_file,
                                           mode='wt',
                                           buffering=mock.ANY,
                                           encoding='utf-8',
                                           errors=mock.ANY,
                                           newline=mock.ANY,
                                           closefd=mock.ANY,
                                           opener=mock.ANY)
            mocked_json_dump.assert_called_with(json.loads(expected_json_data),
                                                mocked_open.return_value,
                                                sort_keys=True,
                                                indent=4,
                                                ensure_ascii=False)
