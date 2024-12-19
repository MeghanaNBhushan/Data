""" Testing the qacw_project """
import os
import shutil
import unittest
from unittest import mock

import lucxbox.tools.qacw.qacw_project_report as qac_report


class TestQacProject(unittest.TestCase):

    def setUp(self):
        self.mock_logger = mock.patch("lucxbox.tools.qacw.qacw_project_report.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_archive_report(self):
        src = os.path.dirname(os.path.realpath(__file__))
        target = os.path.dirname(os.path.realpath(__file__)) + "/yet_another_folder"

        qac_report.archive_report(src, target)

        target_archive = target + "/reports.zip"
        self.assertTrue(os.path.isfile(target_archive))

        shutil.rmtree(target)


if __name__ == "__main__":
    unittest.main()
