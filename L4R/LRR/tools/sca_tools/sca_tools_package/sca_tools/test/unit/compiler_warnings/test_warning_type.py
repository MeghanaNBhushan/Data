# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_warning_type.py
# ----------------------------------------------------------------------------
"""Test for compiler_warnings/warning_type.py"""
import os
import unittest

from swq.compiler_warnings.warning_type import load_warnings_db


class TestWarningType(unittest.TestCase):
    """ TestWarningType class """

    def test_warning_type_db_armclang(self):
        """ Test load_warnings_db() method """
        file_path = os.path.join(os.path.dirname(__file__), 'testdata',
                                 'test_warning_types_armclang.json')
        types_db = load_warnings_db(file_path)

        self.assertEqual(len(types_db), 4)
        self.assertTrue("-W#pragma-messages" in types_db)
        self.assertTrue("-Waddress-of-temporary" in types_db)
        self.assertTrue("-Wconditional-uninitialized" in types_db)
        self.assertTrue("-Wzero-length-array" in types_db)
        self.assertEqual(types_db["-W#pragma-messages"].name,
                         "-W#pragma-messages")
        self.assertEqual(types_db["-W#pragma-messages"].severity, "8")
