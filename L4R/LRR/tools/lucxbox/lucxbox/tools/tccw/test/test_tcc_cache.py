""" Test for tccw """

import os
import sys
import unittest
from unittest import mock

from lucxbox.tools.tccw import tcc_cache, tcc_config

USER_HOME = os.path.expanduser("~")
TCCW_FILE = os.path.join(USER_HOME, ".tccw")
TEST_DATA = {"TCC_PYTHON": "C:\\affe\\affe"}
TEST_CONFIG = os.path.normcase(os.path.join(os.path.dirname(__file__), "test_config.xml"))
TEST_CONFIG_MIRROR = os.path.normcase(os.path.join(os.path.dirname(__file__), "test_config_mirror.xml"))
EXPECTED_HASH = "0bdeb69cf8b9a94bffdf3ff3462fb4eb"
MOCKNODE = "mock_host"
MOCKSYSTEM = "Windows"
MOCKVERSION = "10.0.17763"


class TestTccwCache(unittest.TestCase):
    """ Test class for tcc wrapper """

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def setUp(self):
        self.mock_node = mock.patch('lucxbox.tools.tccw.tcc_cache.platform.node').start()
        self.mock_version = mock.patch('lucxbox.tools.tccw.tcc_cache.platform.system').start()
        self.mock_system = mock.patch('lucxbox.tools.tccw.tcc_cache.platform.version').start()
        self.mock_node.return_value = MOCKNODE
        self.mock_system.return_value = MOCKVERSION
        self.mock_version.return_value = MOCKSYSTEM


    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def tearDown(self):
        self.mock_node.stop()
        self.mock_version.stop()
        self.mock_system.stop()


    @mock.patch("lucxbox.tools.tccw.tcc_cache.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_cache.load_data")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.os.path.isfile")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.atomicwrites.atomic_write")
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_store_data_mirror(self, mock_atomic, mock_isfile, mock_load, _):
        mock_isfile.return_value = True
        mock_load.return_value = None
        config = tcc_config.TccConfig()
        config.set_local_file(TEST_CONFIG_MIRROR)
        tcc_cache.store_data(TEST_DATA, config)
        self.assertEqual(len(mock_atomic.mock_calls), 0)


    @mock.patch("lucxbox.tools.tccw.tcc_cache.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_cache.load_data")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.os.path.isfile")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.atomicwrites.atomic_write")
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_store_data(self, mock_atomic, mock_isfile, mock_load, _):
        mock_isfile.return_value = True
        mock_load.return_value = None
        config = tcc_config.TccConfig()
        config.set_local_file(TEST_CONFIG)
        tcc_cache.store_data(TEST_DATA, config)
        expected_call = mock.call(TCCW_FILE, overwrite=True)
        self.assertEqual(mock_atomic.mock_calls[0], expected_call)
        expected_data = {EXPECTED_HASH: TEST_DATA}
        expected_call = mock.call().__enter__().write(str(expected_data).replace("'", "\""))
        self.assertEqual(mock_atomic.mock_calls[2], expected_call)


    @mock.patch("lucxbox.tools.tccw.tcc_cache.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_cache.load_data")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.os.path.isfile")
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_get_env_from_cache(self, mock_isfile, mock_load, _):
        mock_isfile.return_value = True
        mock_load.return_value = {EXPECTED_HASH: TEST_DATA}
        config = tcc_config.TccConfig()
        config.set_local_file(TEST_CONFIG)
        data = tcc_cache.get_env_from_cache(config)
        self.assertEqual(TEST_DATA, data)


    @mock.patch("lucxbox.tools.tccw.tcc_cache.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_cache.load_data")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.os.path.isfile")
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_get_env_first_run(self, mock_isfile, mock_load, _):
        mock_isfile.return_value = True
        mock_load.return_value = {"affeaffeaffeaffeaffeaffeaffeaffe": TEST_DATA}
        config = tcc_config.TccConfig()
        config.set_local_file(os.path.join(os.path.dirname(__file__), "test_config.xml"))
        data = tcc_cache.get_env_from_cache(config)
        self.assertEqual(None, data)


    @mock.patch("lucxbox.tools.tccw.tcc_cache.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_cache.load_data")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.os.path.isfile")
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_get_env_read_error(self, mock_isfile, mock_load, _):
        mock_isfile.return_value = True
        mock_load.return_value = None
        config = tcc_config.TccConfig()
        config.set_local_file(os.path.join(os.path.dirname(__file__), "test_config.xml"))
        data = tcc_cache.get_env_from_cache(config)
        self.assertEqual(None, data)


    @mock.patch("lucxbox.tools.tccw.tcc_cache.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_cache.load_data")
    @mock.patch("lucxbox.tools.tccw.tcc_cache.os.path.isfile")
    def test_get_hash(self, mock_isfile, mock_load, _):
        mock_isfile.return_value = True
        mock_load.return_value = None
        additional_data = MOCKNODE + MOCKSYSTEM + MOCKVERSION
        actual_hash = tcc_cache.get_file_hash(TEST_CONFIG, additional_data)
        self.assertEqual(actual_hash, EXPECTED_HASH)


if __name__ == "__main__":
    unittest.main()
