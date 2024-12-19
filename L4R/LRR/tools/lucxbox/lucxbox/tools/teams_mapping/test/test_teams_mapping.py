""" Test for a python project """

import os
import unittest
from unittest import mock
from lucxbox.tools.teams_mapping import teams_mapping

class TestTeamsMapping(unittest.TestCase):

    def setUp(self):
        self.mock_logger = mock.patch(
            "lucxbox.tools.teams_mapping.teams_mapping.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_get_delimeter(self):
        report_name = os.path.dirname(
            os.path.realpath(__file__)) + "/test_report.csv"
        delimiter = teams_mapping.get_csv_dialect(report_name).delimiter
        self.assertEqual(delimiter, ',')

    def test_skip_rows(self):
        report_name = os.path.dirname(
            os.path.realpath(__file__)) + "/test_report.csv"
        skip_rows = teams_mapping.get_rows_before_header(report_name, ',')
        self.assertEqual(skip_rows, 2)

    def test_add_fieldnames(self):
        fieldnames = teams_mapping.add_fieldnames(
            ['Team', 'Components'], ['File', 'Messages', 'Line number', 'Column number'])
        self.assertIn('Team', fieldnames)
        self.assertIn('Components', fieldnames)
        fieldnames = teams_mapping.add_fieldnames(
            ['Team', 'Components'], ['Team', 'File', 'Line number'])
        self.assertIn('Team', fieldnames)
        self.assertIn('Components', fieldnames)
        self.assertCountEqual(
            ['Team', 'File', 'Line number', 'Components'], fieldnames)

    def test_main_usage(self):
        with self.assertRaises(SystemExit):
            teams_mapping.main()


if __name__ == "__main__":
    unittest.main()
