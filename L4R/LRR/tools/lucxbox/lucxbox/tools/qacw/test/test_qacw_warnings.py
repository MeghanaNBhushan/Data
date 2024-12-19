""" Testing the qacw_warnings """
import os
import unittest
from unittest import mock

import lucxbox.tools.qacw.qacw_warnings as qac_warnings


class TestQacWarnings(unittest.TestCase):
    """All test cases for qacw_warnings"""

    def setUp(self):
        self.mock_logger = mock.patch("lucxbox.tools.qacw.qacw_warnings.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_process_results_file(self):
        components_files = os.path.dirname(os.path.realpath(__file__)) + "/test_components"
        file_name = os.path.dirname(os.path.realpath(__file__)) + "/test_report.log"
        exceptions_wildcards = ["C:/tools/**"]

        qac_results = qac_warnings.process_results_file(file_name=file_name, exception_wildcards=exceptions_wildcards,
                                                        components_files=components_files, min_severity=2)

        self.assertTrue(len(qac_results) == 2)

    def test_check_if_analyze_line(self):
        line1 = "// ======= Results for C:/Tools/compiler/ARM_6_06_01/include/libcxx/atomic"
        line2 = "C:/Tools/compiler/ARM_6_06_01/include/libcxx/atomic - was analyzed resulting in 1 harderror(s)"
        line3 = ""
        line4 = "path - zero diagnostics found"
        line5 = "C:/Tools/compiler/ARM_6_06_01/include/libcxx/type_traits; 4524; 9;  Critical Parsing error, parser failures for:"

        self.assertFalse(qac_warnings.check_if_analyze_line(exception_wildcards=[], line=line1))
        self.assertFalse(qac_warnings.check_if_analyze_line(exception_wildcards=[], line=line2))
        self.assertFalse(qac_warnings.check_if_analyze_line(exception_wildcards=[], line=line3))
        self.assertFalse(qac_warnings.check_if_analyze_line(exception_wildcards=[], line=line4))
        self.assertFalse(qac_warnings.check_if_analyze_line(exception_wildcards=["C:/Tools/**"], line=line5))
        self.assertFalse(qac_warnings.check_if_analyze_line(exception_wildcards=["C:/tools/**"], line=line5))
        self.assertTrue(qac_warnings.check_if_analyze_line(exception_wildcards=[], line=line5))

    def test_xlsx_creation(self):
        components_files = os.path.dirname(os.path.realpath(__file__)) + "/test_components"
        file_name = os.path.dirname(os.path.realpath(__file__)) + "/test_report.log"
        exceptions_wildcards = ["C:/tools/**"]

        qac_results = qac_warnings.process_results_file(file_name=file_name, exception_wildcards=exceptions_wildcards,
                                                        components_files=components_files, min_severity=0)

        qac_warnings.create_xlsx_report(qac_results=qac_results, team_warnings_file="output.xlsx")
        self.assertTrue(os.path.isfile("output.xlsx"), msg="xlsx file could not be created")
        os.remove("output.xlsx")
        self.assertFalse(os.path.isfile("output.xlsx"))

    def test_csv_creation(self):
        components_files = os.path.dirname(os.path.realpath(__file__)) + "/test_components"
        file_name = os.path.dirname(os.path.realpath(__file__)) + "/test_report.log"
        exceptions_wildcards = ["C:/tools/**"]

        qac_results = qac_warnings.process_results_file(file_name=file_name, exception_wildcards=exceptions_wildcards,
                                                        components_files=components_files, min_severity=0)

        qac_warnings.create_xlsx_report(qac_results=qac_results, team_warnings_file="output.csv")
        self.assertTrue(os.path.isfile("output.csv"), msg="csv file could not be created")
        os.remove("output.csv")
        self.assertFalse(os.path.isfile("output.csv"))


if __name__ == "__main__":
    unittest.main()
