# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_info_report.py
# ----------------------------------------------------------------------------
"""Tests for qac/state/report/info.py"""

from unittest import TestCase, mock
from unittest.mock import patch

import numpy as np
import pandas as pd
from swq.qac.state.report import info as info_module
from swq.qac.state.report.constants import INFO_MAPPED_COLUMNS
from swq.qac.state.transformator import STATE_INFO_TRANSFORM_QUERY

TRANSFORMED_INFO = '''
[
    {
        "license": "License Notice",
        "git_commit": "qwerty",
        "acf": null
    }
]
'''


class TestQacInfoReport(TestCase):
    """TestQacInfoReport class"""
    def setUp(self):
        self.state_content = mock.Mock()
        _columns = ['variable', 'value']
        _data = [[f"{INFO_MAPPED_COLUMNS['license']}:", 'License Notice'],
                 [f"{INFO_MAPPED_COLUMNS['git_commit']}:", 'qwerty'],
                 [f"{INFO_MAPPED_COLUMNS['acf']}:", np.nan]]
        self.expected_df = pd.DataFrame(columns=_columns, data=_data)

    @patch.object(info_module, 'transform_state')
    def test_create_info_dataframe(self, mocked_transform_state):
        """Tests create_info_dataframe method"""

        mocked_transform_state.return_value = pd.read_json(TRANSFORMED_INFO,
                                                           dtype=False)

        result_df = info_module.create_info_dataframe(self.state_content)

        mocked_transform_state.assert_called_once_with(
            self.state_content, STATE_INFO_TRANSFORM_QUERY)
        self.assertTrue(result_df.equals(self.expected_df))
