""" Test for a warnings parser """

import os
import unittest
from unittest import mock

from lucxbox.tools.compiler_warnings import compiler_clang, compiler_greenhills, compiler_msvc
from lucxbox.tools.compiler_warnings.compiler_warnings import set_warning_info_from_types_db


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.mock_logger = mock.patch("lucxbox.tools.compiler_warnings.compiler.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_get_warnings_armclang(self):
        compiler = compiler_clang.Compiler()
        file_path = os.path.join(os.path.dirname(__file__), 'test_warnings_armclang.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})
        self.assertEqual(len(warnings), 3)

    def test_get_warnings_greenhills(self):
        compiler = compiler_greenhills.Compiler()
        file_path = os.path.join(os.path.dirname(__file__), 'test_warnings_greenhills.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})
        self.assertEqual(len(warnings), 12)

    def test_get_warnings_msvc(self):
        compiler = compiler_msvc.Compiler()
        file_path = os.path.join(os.path.dirname(__file__), 'test_warnings_msvc.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})
        self.assertEqual(len(warnings), 6)

    def test_warning_info_from_types_db(self):
        compiler = compiler_clang.Compiler()
        file_path = os.path.join(os.path.dirname(__file__), 'test_warnings_armclang.txt')
        warnings = compiler.get_warnings_from_file(file_path, 1, {})
        db_path = os.path.join(os.path.dirname(__file__), 'test_warning_types_armclang.json')
        warnings = set_warning_info_from_types_db(warnings, db_path)
        self.assertEqual(warnings[0].type_name, "#pragma-messages")
        self.assertEqual(warnings[0].severity, "8")


if __name__ == "__main__":
    unittest.main()
