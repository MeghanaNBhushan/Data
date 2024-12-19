#!/usr/bin/python
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Unittest for copyright_checker class

Author: Michael Engeroff
Department: CC-DA/ESI1
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import unittest
from unittest import mock

from lucxbox.tools.copyright_checker import copyright_checker
from lucxbox.tools.copyright_checker.copyright_result import CopyrightResult

REPO_NAME = "fvg3"


class TestCopyrightChecker(unittest.TestCase):
    """ Test class for copyright checker """

    def __init__(self, *args, **kwargs):
        super(TestCopyrightChecker, self).__init__(*args, **kwargs)
        self.pwd = os.path.dirname(os.path.realpath(__file__))
        self.root = os.path.join(self.pwd, "resources")

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_check_file_rb_copyright(self, _):
        """ Check file with correct RB header """
        file_name = "rb_header.hpp"
        result = copyright_checker.check_file(file_name, REPO_NAME, self.root)
        self.assertTrue(result.get_has_rb_copyright())

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_check_file_no_copyright(self, _):
        """ Check file with out any copyright header """
        file_name = "no_header.hpp"
        result = copyright_checker.check_file(file_name, REPO_NAME, self.root)
        self.assertTrue(result.get_has_no_copyright())

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_check_file_ignored(self, _):
        """ Check a file, which should be ignored from the copyright check """
        file_name = "ignore.flux"
        result = copyright_checker.check_file(file_name, REPO_NAME, self.root)
        self.assertTrue(result.get_is_ignored())

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_check_other_rb_copyright(self, _):
        """ Check file with some other RB copyright header """
        file_name = "other_rb_header_v1.hpp"
        result = copyright_checker.check_file(file_name, REPO_NAME, self.root)
        self.assertTrue(result.get_has_other_rb_copyright())

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_check_file_other_copyright(self, _):
        """ Check file with some copyright header """
        file_name = "other_header.hpp"
        result = copyright_checker.check_file(file_name, REPO_NAME, self.root)
        self.assertTrue(result.get_has_other_copyright())

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_print_result_list(self, mock_logger):
        result_list = []
        copyright_result1 = CopyrightResult("resources", "test1.cpp", REPO_NAME, mock_logger)
        copyright_result2 = CopyrightResult("resources", "test2.cpp", REPO_NAME, mock_logger)
        copyright_result3 = CopyrightResult("resources", "test3.cpp", REPO_NAME, mock_logger)
        copyright_result4 = CopyrightResult("resources", "test4.cpp", REPO_NAME, mock_logger)
        copyright_result5 = CopyrightResult("resources", "test5.cpp", REPO_NAME, mock_logger)

        copyright_result1.set_has_rb_copyright(True)
        copyright_result2.set_has_other_rb_copyright(True)
        copyright_result3.set_has_no_copyright(True)
        copyright_result4.set_has_other_copyright(True)
        copyright_result5.set_is_ignored(True)

        result_list.append(copyright_result1)
        result_list.append(copyright_result2)
        result_list.append(copyright_result3)
        result_list.append(copyright_result4)
        result_list.append(copyright_result5)

        copyright_checker.print_result(result_list)

        info_calls = str(mock_logger.info.mock_calls)
        self.assertTrue("test1.cpp" not in info_calls)
        self.assertTrue("test2.cpp" in info_calls)
        self.assertTrue("test3.cpp" in info_calls)
        self.assertTrue("test4.cpp" in info_calls)
        self.assertTrue("test5.cpp" not in info_calls)

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_ignored_has_correct_header(self, mock_logger):
        copyright_result = CopyrightResult(self.root, "test1.cpp", REPO_NAME, mock_logger)
        copyright_result.set_has_rb_copyright(True)
        copyright_checker.print_result(copyright_result)

        output = str(mock_logger.info.mock_calls)
        self.assertTrue("test1.cpp" not in output)

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_result_ignored(self, mock_logger):
        copyright_result = CopyrightResult(self.root, "test1.cpp", REPO_NAME, mock_logger)
        copyright_result.set_is_ignored(True)
        copyright_checker.print_result(copyright_result)

        output = str(mock_logger.info.mock_calls)
        self.assertTrue("test1.cpp" not in output)

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_result_not_ignored_1(self, mock_logger):
        copyright_result = CopyrightResult(self.root, "test1.cpp", REPO_NAME, mock_logger)
        copyright_result.set_has_other_rb_copyright(True)
        copyright_checker.print_result(copyright_result)

        output = str(mock_logger.info.mock_calls)
        self.assertTrue("test1.cpp" in output)

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_result_not_ignored_2(self, mock_logger):
        copyright_result = CopyrightResult(self.root, "test1.cpp", REPO_NAME, mock_logger)
        copyright_result.set_has_no_copyright(True)
        copyright_checker.print_result(copyright_result)

        output = str(mock_logger.info.mock_calls)
        self.assertTrue("test1.cpp" in output)

    @mock.patch("lucxbox.tools.copyright_checker.copyright_checker.LOGGER", create=True)
    def test_result_not_ignored_3(self, mock_logger):
        copyright_result = CopyrightResult(self.root, "test1.cpp", REPO_NAME, mock_logger)
        copyright_result.set_has_other_copyright(True)
        copyright_checker.print_result(copyright_result)

        output = str(mock_logger.info.mock_calls)
        self.assertTrue("test1.cpp" in output)


if __name__ == '__main__':
    unittest.main(exit=False)
