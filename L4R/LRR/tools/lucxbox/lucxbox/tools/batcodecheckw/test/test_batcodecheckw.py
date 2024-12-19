"""Test for batcodecheckw.py"""

import os
import tempfile
import shutil
import sys
import subprocess
import unittest

from unittest.mock import patch
from lucxbox.lib import lucxlog
from lucxbox.tools.batcodecheckw import batcodecheckw

LOGGER = lucxlog.get_logger()


@patch('lucxbox.tools.batcodecheckw.batcodecheckw.subprocess.Popen')
class TestBatCodeCheck(unittest.TestCase):
    """ test BatCodeCheck class """
    file_path = os.path.dirname(__file__)
    batcodecheck_path = r"C:\some\valid\local\path\batcodecheck\batcodecheck.exe"
    test_src = os.path.join(file_path, "bccExample.bat")
    bcc_default_var = "TCC_BATCODECHECK"
    tccw_python_path = os.path.join(batcodecheckw.BatCodeCheck.file_path, '..', 'tccw', 'tccw.py')

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.out_path = os.path.join(self.temp_dir, "valid_out_path")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @patch('lucxbox.tools.batcodecheckw.batcodecheckw.check_installation')
    def test_valid_list_file(self, mock_check_installation, mock_popen):
        process = unittest.mock.Mock()
        process.communicate.return_value = ("stdout", "stderr")
        process.returncode = 0
        mock_popen.return_value = process
        mock_check_installation.return_value = self.batcodecheck_path
        list_file_path = os.path.join(self.temp_dir, "some_file_name.tmp")
        with open(list_file_path, 'w') as list_file:
            list_file.write(self.test_src)
        batcodecheckw.main([
            "",
            "-l", list_file_path,
            "-o", self.out_path,
            "-i", self.batcodecheck_path,
        ])
        expected_cmd = "{} {} /H:{}".format(self.batcodecheck_path, self.test_src, os.path.join(self.out_path, "bccExample.html"))
        mock_popen.assert_called_with(expected_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    @patch('lucxbox.tools.batcodecheckw.batcodecheckw.check_installation')
    def test_empty_list_file(self, mock_check_installation, mock_popen):
        mock_check_installation.return_value = self.batcodecheck_path
        list_file_path = os.path.join(self.temp_dir, "some_file_name.tmp")
        open(list_file_path, "w").close()
        batcodecheckw.main([
            "",
            "-l", list_file_path,
            "-o", self.out_path,
            "-i", self.batcodecheck_path,
        ])
        mock_popen.assert_not_called()

    @patch('lucxbox.tools.batcodecheckw.batcodecheckw.check_installation')
    def test_deleted_src_in_list_file(self, mock_check_installation, mock_popen):
        mock_check_installation.return_value = self.batcodecheck_path
        list_file_path = os.path.join(self.temp_dir, "some_file_name.tmp")
        with open(list_file_path, 'w') as list_file:
            list_file.write(os.path.join(self.temp_dir, "non_existing_file.bat"))
        batcodecheckw.main([
            "",
            "-l", list_file_path,
            "-o", self.out_path,
            "-i", self.batcodecheck_path,
        ])
        mock_popen.assert_not_called()

    @patch('lucxbox.tools.batcodecheckw.batcodecheckw.check_installation')
    def test_non_existing_list_file(self, mock_check_installation, mock_popen):
        mock_check_installation.return_value = self.batcodecheck_path
        list_file_path = os.path.join(self.temp_dir, "non_existing_list_file.tmp")
        batcodecheckw.main([
            "",
            "-l", list_file_path,
            "-o", self.out_path,
            "-i", self.batcodecheck_path,
        ])
        mock_popen.assert_not_called()

    @patch('lucxbox.tools.batcodecheckw.batcodecheckw.check_installation')
    def test_valid_source(self, mock_check_installation, mock_popen):
        process = unittest.mock.Mock()
        process.communicate.return_value = ("stdout", "stderr")
        process.returncode = 0
        mock_popen.return_value = process
        mock_check_installation.return_value = self.batcodecheck_path

        batcodecheckw.main([
            "",
            "-s", self.test_src,
            "-o", self.out_path,
            "-i", self.batcodecheck_path,
        ])
        expected_cmd = "{} {} /H:{}".format(self.batcodecheck_path, self.test_src, os.path.join(self.out_path, "bccExample.html"))
        mock_popen.assert_called_with(expected_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    @patch('lucxbox.tools.batcodecheckw.batcodecheckw.check_installation')
    def test_non_existing_source(self, mock_check_installation, mock_popen):
        mock_check_installation.return_value = self.batcodecheck_path
        source_file = os.path.join(self.file_path, "non_existing_file.bat")
        batcodecheckw.main([
            "",
            "-s", source_file,
            "-o", self.out_path,
            "-i", self.batcodecheck_path,
        ])
        mock_popen.assert_not_called()

    def test_local_tcc(self, mock_popen):
        process = unittest.mock.Mock()
        process.communicate.return_value = ("stdout", "stderr")
        process.returncode = 0
        mock_popen.return_value = process
        # create temporary config file
        test_config_path = os.path.join(self.temp_dir, "valid_config.xml")
        open(test_config_path, "w").close()
        # execute bccw with local config
        batcodecheckw.main([
            "",
            "-s", self.test_src,
            "-o", self.out_path,
            "-tl", test_config_path,
        ])
        # create tool path
        tool_path = "{} {} -l {}  -- %{}%/BatCodeCheck.exe".format(sys.executable,
                                                                   self.tccw_python_path,
                                                                   test_config_path,
                                                                   self.bcc_default_var)
        # assert that bccw was called with correct local config in command
        expected_cmd = "{} {} /H:{}".format(tool_path, self.test_src, os.path.join(self.out_path, "bccExample.html"))
        mock_popen.assert_called_with(expected_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    def test_invalid_local_tcc(self, mock_popen):
        with self.assertRaises(SystemExit):
            batcodecheckw.main([
                "",
                "-s", self.test_src,
                "-o", self.out_path,
                "-tl", r"C:\invalid\local\tcc\path.xml",
            ])
        mock_popen.assert_not_called()

    def test_server_tcc(self, mock_popen):
        process = unittest.mock.Mock()
        process.communicate.return_value = ("stdout", "stderr")
        process.returncode = 0
        mock_popen.return_value = process
        # create variable for test tcc server config
        test_config = "TCC_Test_Server_Config"
        # execute bccw with test server config
        batcodecheckw.main([
            "",
            "-s", self.test_src,
            "-o", self.out_path,
            "-tc", test_config,
        ])
        # create tool path
        tool_path = "{} {} -c {}  -- %{}%/BatCodeCheck.exe".format(sys.executable,
                                                                   self.tccw_python_path,
                                                                   test_config,
                                                                   self.bcc_default_var)
        # assert that bccw was called with correct server config in command
        expected_cmd = "{} {} /H:{}".format(tool_path, self.test_src, os.path.join(self.out_path, "bccExample.html"))
        mock_popen.assert_called_with(expected_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    def test_invalid_batcodecheck_path(self, mock_popen):
        invalid_path = "C:/invalid/path/Batcodecheck.exe"
        with self.assertRaises(SystemExit):
            batcodecheckw.main([
                "",
                "-s", self.test_src,
                "-o", self.out_path,
                "-i", invalid_path,
            ])
        mock_popen.assert_not_called()


if __name__ == '__main__':
    unittest.main()
