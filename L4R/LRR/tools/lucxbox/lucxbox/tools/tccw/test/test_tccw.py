""" Test for tccw """

import os
import sys
import tempfile
import unittest
from unittest import mock

from lucxbox.tools.tccw import tcc_config, tcc_wrapper, tccw

MOCK_MAKE = """TCC_7ZIP = c:/TCC/Tools/7zip/18.05_WIN64
TCC_A2LMERGER = c:/TCC/Tools/a2lmerger/3.9.3"""


class TestTccw(unittest.TestCase):
    """ Test class for tcc wrapper """

    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.os.environ", {})
    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.subprocess.check_call")
    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.lucxutils.which")
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_execute_windows(self, mock_which, mock_call, _):
        mock_which.return_value = True
        cmd = ["%TCC_TEST_PATH%", "--version"]
        env = {"TCC_TEST_PATH": "C:\\AFFEAFFE"}
        tcc_wrapper.execute(cmd, env)
        ref_call = mock.call(["C:\\AFFEAFFE", "--version"], env={"TCC_TEST_PATH": "C:\\AFFEAFFE"}, shell=True)
        self.assertEqual(ref_call, mock_call.mock_calls[0])

    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.LOGGER", create=True)
    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.os.environ", {})
    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.subprocess.check_call")
    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.lucxutils.which")
    def test_execute_linux(self, mock_which, mock_call, _):
        mock_which.return_value = True
        cmd = ["$TCC_TEST_PATH", "--version"]
        env = {"TCC_TEST_PATH": "/c/AFFEAFFE"}
        tcc_wrapper.execute(cmd, env)
        ref_call = mock.call(["/c/AFFEAFFE", "--version"], env={"TCC_TEST_PATH": "/c/AFFEAFFE"}, shell=True)
        self.assertEqual(ref_call, mock_call.mock_calls[0])

    @mock.patch("lucxbox.tools.tccw.tcc_config.LOGGER", create=True)
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_set_by_value(self, _):
        config = tcc_config.TccConfig()
        config.set_by_value("TCC_FVG3_Windows_DevLatest")
        self.assertEqual(config.get("tccxmlconfigpath"),
                         "ITO\\TCC\\Base\\FVG3\\Windows\\TCC_FVG3_Windows_DevLatest.xml")

    @mock.patch("lucxbox.tools.tccw.tcc_config.LOGGER", create=True)
    def test_set_by_file(self, _):
        config = tcc_config.TccConfig()
        config.set_by_file(os.path.join(os.path.dirname(__file__), "test_config.ini"))
        self.assertEqual(config.get("tccxmlconfigpath"), "ITO\\TCC\\Base\\FVG3\\Windows\\AFFEAFFE.xml")
        self.assertEqual(config.get("tccscriptpath"), "C:\\TCC\\Base\\InstallToolCollection\\AFFEAFFE.ps1")
        self.assertEqual(config.get("tccinvoker"), "AFFEAFFE.exe")
        self.assertEqual(config.get("tccinstall"), False)

    @mock.patch("lucxbox.tools.tccw.tcc_config.LOGGER", create=True)
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_set_by_empty_file(self, _):
        config = tcc_config.TccConfig()
        config.set_by_file(os.path.join(os.path.dirname(__file__), "empty.ini"))
        self.assertEqual(config.get("tccxmlconfigpath"), "ITO\\TCC\\Base\\FVG3\\Windows\\AFFEAFFE.xml")
        self.assertEqual(config.get("tccscriptpath"), "C:\\TCC\\Base\\InstallToolCollection\\InstallToolCollection.ps1")
        self.assertEqual(config.get("tccinstall"), True)

    @mock.patch("lucxbox.tools.tccw.tcc_wrapper.setenv")
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    # pylint: disable=no-self-use
    def test_tcc_init_func(self, mock_popen):
        cfg = tcc_config.TccConfig()
        cfg.set_by_value("TCC_IF_Windows_BTC-0.23.0")
        tcc_wrapper.init_tcc(cfg, True)
        exec_env = {}
        exec_env['BUILD_DIR'] = tempfile.gettempdir()
        tcc_command = cfg.get_invoker() + ' -file ' + cfg.get_script_path()
        exec_env["TCC_COMMAND"] = tcc_command
        exec_env["TOOLCOLLECTION"] = cfg.get_version()
        exec_env["TOOLCOLLECTION_XML"] = cfg.get_xml()
        mock_popen.assert_called_with(exec_env, r'C:\TCC\Tools\tcc_init\TCC_IF_Windows_BTC-0.23.0\init.bat')

    @mock.patch.dict(os.environ, {'PATH': 'SOMETHING'})
    def test_extend_env_path(self):
        env = {'TCC_TEST': 'SOMETHING/ELSE'}
        extend_path = ['TEST/bin']
        expected = {'PATH': 'SOMETHING/ELSE{}bin{}SOMETHING'.format(os.sep, os.pathsep), 'TCC_TEST': 'SOMETHING/ELSE'}
        self.assertDictEqual(expected, tccw.extend_env_path(env, extend_path))


if __name__ == "__main__":
    unittest.main()
