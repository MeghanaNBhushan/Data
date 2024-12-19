""" Test for a the mapping of components """
import os
import unittest
from unittest import mock

from lucxbox.tools.cpp_macro_reader import cpp_macro_reader

TEST_SYSCONFIG_OUT = """ONE=1
TWO=2
THREE=3
ONE_ONE=17
ONE_TWO=18
ONE_TWO_ONE=289
MAX=4294967295
MEM_VAS_DRAM_SIZE=1073741824
MEM_VAS_RTRAM_BASE=3944742912
MEM_VAS_BOOTMGR_MAXSIZE=194560
MEM_VAS_RPU_MAXSIZE=9437184
MEM_VAS_APU_MAXSIZE=1064304640
MEM_VAS_HSMRPUEX_BASE=3944988672
MEM_VAS_HSMRPUEX_MAXSIZE=8192
MEM_VAS_BOOTMGR_BASE=3944753152

"""

TEST_SYSCONFIG_MAX_OUT = """OVERFLOW=4294967296

"""


class TestSysConfig(unittest.TestCase):
    """Test class for the component mapper"""

    def setUp(self):
        self.mock_logger = mock.patch("lucxbox.tools.cpp_macro_reader.cpp_macro_reader.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @mock.patch("lucxbox.tools.cpp_macro_reader.cpp_macro_reader.lucxutils.execute")
    def test_get_addresses(self, mock_execute):
        mock_execute.return_value = TEST_SYSCONFIG_OUT, "", 0
        sysconfig_file = os.path.dirname(os.path.realpath(__file__)) + "/test_sysconfig.hpp"
        addresses = cpp_macro_reader.get_macros(sysconfig_file, "dummy")
        self.assertEqual(addresses["ONE"], "0x00000001")
        self.assertEqual(addresses["TWO"], "0x00000002")
        self.assertEqual(addresses["THREE"], "0x00000003")
        self.assertEqual(addresses["ONE_ONE"], "0x00000011")
        self.assertEqual(addresses["ONE_TWO"], "0x00000012")
        self.assertEqual(addresses["ONE_TWO_ONE"], "0x00000121")
        self.assertEqual(addresses["MAX"], "0xFFFFFFFF")

        self.assertEqual(addresses["MEM_VAS_DRAM_SIZE"], "0x40000000")
        self.assertEqual(addresses["MEM_VAS_BOOTMGR_MAXSIZE"], "0x0002F800")
        self.assertEqual(addresses["MEM_VAS_APU_MAXSIZE"], "0x3F700000")
        self.assertEqual(addresses["MEM_VAS_BOOTMGR_BASE"], "0xEB202800")

    @mock.patch("lucxbox.tools.cpp_macro_reader.cpp_macro_reader.lucxutils.execute")
    def test_get_addresses_max(self, mock_execute):
        mock_execute.return_value = TEST_SYSCONFIG_MAX_OUT, "", 0
        sysconfig_file = os.path.dirname(os.path.realpath(__file__)) + "/test_sysconfig_max.hpp"
        with self.assertRaises(ValueError):
            cpp_macro_reader.get_macros(sysconfig_file, "dummy")

    @mock.patch("lucxbox.tools.cpp_macro_reader.cpp_macro_reader.lucxutils.execute")
    def test_compile_error(self, mock_execute):
        mock_execute.return_value = "", "error", 1
        sysconfig_file = os.path.dirname(os.path.realpath(__file__)) + "/test_sysconfig_max.hpp"
        with self.assertRaises(SystemExit):
            cpp_macro_reader.get_macros(sysconfig_file, "dummy")


if __name__ == "__main__":
    unittest.main()
