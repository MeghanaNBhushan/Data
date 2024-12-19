""" Test for a mspdbsrv wrapper """

import os
import unittest
from unittest import mock
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import portal
from lucxbox.lib.lucxtest import TestCaseWithTempFile
from lucxbox.tools.dauerlaufw import dauerlaufw


class TestStringMethods(TestCaseWithTempFile):

    @mock.patch("lucxbox.tools.dauerlaufw.dauerlaufw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.dauerlaufw.dauerlaufw.lucxutils.execute")
    def test_build(self, mock_execute, _):
        with portal.In(self.test_dir):
            mock_execute.return_value = "", "Houston, we have a problem.", 1
            dauerlaufw.build(["echo"], "1")
            self.assertTrue(os.path.isfile("dauerlaufw_1.err"))
            self.assertTrue(os.path.isfile("dauerlaufw_1.out"))

    @mock.patch("lucxbox.tools.dauerlaufw.dauerlaufw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.dauerlaufw.dauerlaufw.lucxutils.execute")
    def test_loop(self, mock_execute, _):
        with portal.In(self.test_dir):
            mock_execute.side_effect = [["", "Houston, we have a problem.", 1], ["The eagle has landed!", "", 0]]
            dauerlaufw.loop(["echo"], "1")
            self.assertTrue(os.path.isfile("dauerlaufw_1.err"))
            self.assertTrue(os.path.isfile("dauerlaufw_1.out"))


if __name__ == "__main__":
    unittest.main()
