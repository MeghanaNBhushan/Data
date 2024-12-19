""" Test for a cashew """

import argparse
import os
import unittest
from unittest import mock

from lucxbox.tools.cashew import cashew

TEST_PATH = "C:\\foo@123\\"
TEST_PATH_2 = "C:\\fooXXX\\"
REF_HASH = "49d57ce"
REF_HASH_2 = "1dc742b"
BASE_PATH = os.path.join("C", "ccache")
ARGS = argparse.Namespace(basedir=None, path=None)

class TestStringMethods(unittest.TestCase):
    """ Test class for cashew module. """

    @mock.patch("lucxbox.tools.cashew.cashew.LOGGER", create=True)
    @mock.patch("lucxbox.tools.cashew.cashew.os.environ", {"CCACHE_DIR": BASE_PATH})
    @mock.patch("lucxbox.tools.cashew.cashew.os.getcwd")
    @mock.patch("lucxbox.tools.cashew.cashew.os.path.exists")
    def test_setup_ccache_env(self, mock_exists, mock_getcwd, _):
        mock_exists.return_value = True
        mock_getcwd.return_value = TEST_PATH
        cashew.set_compiler_cache_env(ARGS, ["AFFEAFFE"], "CCACHE_DIR")
        ref_path = os.path.join(BASE_PATH, REF_HASH)
        self.assertEqual(ref_path, cashew.os.environ["CCACHE_DIR"])

    @mock.patch("lucxbox.tools.cashew.cashew.LOGGER", create=True)
    @mock.patch("lucxbox.tools.cashew.cashew.os.environ", {"CLCACHE_DIR": BASE_PATH})
    @mock.patch("lucxbox.tools.cashew.cashew.os.getcwd")
    @mock.patch("lucxbox.tools.cashew.cashew.os.path.exists")
    def test_setup_clcache_env(self, mock_exists, mock_getcwd, _):
        mock_exists.return_value = True
        mock_getcwd.return_value = TEST_PATH
        cashew.set_compiler_cache_env(ARGS, ["AFFEAFFE"], "CLCACHE_DIR")
        ref_path = os.path.join(BASE_PATH, REF_HASH)
        self.assertEqual(ref_path, cashew.os.environ["CLCACHE_DIR"])

    @mock.patch("lucxbox.tools.cashew.cashew.LOGGER", create=True)
    def test_setup_w_exception(self, mock_logger):
        with self.assertRaises(SystemExit):
            cashew.set_compiler_cache_env(ARGS, ["AFFEAFFE"], "DEADBEEF")
        self.assertEqual(1, len(mock_logger.mock_calls))
        ref_call = mock.call.error("Environment variable '%s' not set.", 'DEADBEEF')
        self.assertEqual(ref_call, mock_logger.mock_calls[0])

    @mock.patch("lucxbox.tools.cashew.cashew.LOGGER", create=True)
    @mock.patch("lucxbox.tools.cashew.cashew.os.environ", {"CCACHE_DIR": BASE_PATH})
    @mock.patch("lucxbox.tools.cashew.cashew.os.getcwd")
    @mock.patch("lucxbox.tools.cashew.cashew.os.path.exists")
    def test_setup_with_path(self, mock_exists, mock_getcwd, _):
        mock_exists.return_value = True
        mock_getcwd.return_value = TEST_PATH
        args = argparse.Namespace(basedir=None, path="DEADBEEF")
        cashew.set_compiler_cache_env(args, ["AFFEAFFE"], "CCACHE_DIR")
        ref_path = os.path.join("DEADBEEF", REF_HASH)
        self.assertEqual(ref_path, cashew.os.environ["CCACHE_DIR"])

    @mock.patch("lucxbox.tools.cashew.cashew.LOGGER", create=True)
    @mock.patch("lucxbox.tools.cashew.cashew.os.environ", {"CCACHE_DIR": BASE_PATH})
    @mock.patch("lucxbox.tools.cashew.cashew.os.getcwd")
    @mock.patch("lucxbox.tools.cashew.cashew.os.path.exists")
    def test_setup_with_different_path(self, mock_exists, mock_getcwd, _):
        mock_exists.return_value = True
        mock_getcwd.return_value = TEST_PATH_2
        args = argparse.Namespace(basedir=None, path="DEADBEEF")
        cashew.set_compiler_cache_env(args, ["AFFEAFFE"], "CCACHE_DIR")
        ref_path = os.path.join("DEADBEEF", REF_HASH_2)
        self.assertEqual(ref_path, cashew.os.environ["CCACHE_DIR"])

    @mock.patch("lucxbox.tools.cashew.cashew.subprocess.check_call")
    @mock.patch("lucxbox.tools.cashew.cashew.LOGGER", create=True)
    @mock.patch("lucxbox.tools.cashew.cashew.os.environ", {"CCACHE_DIR": BASE_PATH, "JENKINS_HOME": "DEADBEEF"})
    @mock.patch("lucxbox.tools.cashew.cashew.os.getcwd")
    @mock.patch("lucxbox.tools.cashew.cashew.os.path.exists")
    def test_main_error(self, mock_exists, mock_getcwd, mock_logger, _):
        mock_exists.return_value = True
        mock_getcwd.return_value = TEST_PATH
        with self.assertRaises(SystemExit):
            cashew.main(["cashew.py", "--stats", "--", "echo"])
        ref_call = mock.call("Parameter 'size' and 'stats' require either 'clcache' or 'ccache'.")
        self.assertEqual(ref_call, mock_logger.error.mock_calls[0])


if __name__ == "__main__":
    unittest.main()
