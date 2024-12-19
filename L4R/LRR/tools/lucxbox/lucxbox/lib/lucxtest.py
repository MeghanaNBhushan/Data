""" Library for lucxbox related test helper """

import shutil
import tempfile
import unittest


class TestCaseWithTempFile(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
