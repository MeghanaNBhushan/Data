""" Test for a warning type db """

import os
import unittest

from lucxbox.tools.compiler_warnings import warning_type


class TestWarningType(unittest.TestCase):

    def test_warning_type_db_armclang(self):
        file_path = os.path.join(os.path.dirname(__file__), 'test_warning_types_armclang.json')
        types_db = warning_type.load_warnings_db(file_path)

        self.assertEqual(len(types_db), 4)
        self.assertTrue("-W#pragma-messages" in types_db)
        self.assertTrue("-Waddress-of-temporary" in types_db)
        self.assertTrue("-Wconditional-uninitialized" in types_db)
        self.assertTrue("-Wzero-length-array" in types_db)
        self.assertEqual(types_db["-W#pragma-messages"].name, "-W#pragma-messages")
        self.assertEqual(types_db["-W#pragma-messages"].severity, "8")


if __name__ == "__main__":
    unittest.main()
