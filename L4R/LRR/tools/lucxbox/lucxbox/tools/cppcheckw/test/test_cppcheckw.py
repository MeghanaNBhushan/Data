"""Test for cppcheckw.py"""

import os
import tempfile
import shutil
import unittest

from unittest.mock import patch
from lucxbox.lib import lucxlog
from lucxbox.tools.cppcheckw.cppcheckw import CppCheck
from lucxbox.tools.cppcheckw.htmlreport import convert_to_html

LOGGER = lucxlog.get_logger()


class TestCppCheck(unittest.TestCase):
    """ test CppCheck class """
    file_path = os.path.dirname(__file__)
    cppcheck_path = r"C:\some\valid\local path\Cppcheck\cppcheck.exe"
    test_config = os.path.join(file_path, "test_configuration.ini")
    test_src = os.path.join(file_path, "cppExample.c")

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @patch('os.path.exists')
    @patch('lucxbox.tools.cppcheckw.cppcheckw.lucxutils.execute')
    @patch('lucxbox.tools.cppcheckw.cppcheckw.convert_to_html')
    def test_read_config(self, mock_exists, mock_execute, _):
        mock_execute.return_value = ("test stdout", "test stderr", 0)
        mock_exists.return_value = True

        expected_strings = {'txt': "--enable=all -v --inline-suppr",
                            'xml': "--xml -q --xml-version=2 --suppress=Path\\to\\file.one "
                                   "--suppress=Path\\to\\file.two --suppress=Path/to/file.three",
                            'html': "--xml --verbose --report-progress --suppress=Path\\to\\file.one "
                                    "--suppress=Path\\to\\file.two --suppress=Path/to/file.three"}

        for format_ in expected_strings:
            # invoke CppCheck class with test_configuration.ini
            args = CppCheckTestArgs(output_file=os.path.join(self.temp_dir, "test.txt"),
                                    format=format_,
                                    config_file=self.test_config,
                                    sources=[self.test_src],
                                    install_path=self.cppcheck_path,)
            cc_obj = CppCheck(args)
            cc_obj.analyze()

            # Build the expected command
            command = "{} ".format(self.cppcheck_path)
            for path in args.sources:
                command += '"{}" '.format(path)
            command += "{}".format(expected_strings[format_])
            # Assert, that CppCheck.exe is called with the expected command
            mock_execute.assert_called_with(command)

    def test_htmlreport(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(self.file_path, "test_xml.xml"), "r") as file:
                xml_string = file.read()
            convert_to_html(xml_string, tmpdir, source_dir=self.file_path)

    def test_cppcheck_iec(self):
        LOGGER.debug("Test invalid ECs")
        test_values = {
            'Wrong cppcheck path': {'install_path': r"C:\wrong\path",
                                    "sources": [self.test_src]},
        }

        for _, arguments in test_values.items():
            LOGGER.debug("Test with following arguments: %s", arguments)
            with tempfile.TemporaryDirectory() as tmpdir:
                args = CppCheckTestArgs(os.path.join(tmpdir, 'temp_file'),
                                        **arguments)

                with self.assertRaises(SystemExit):
                    cc_obj = CppCheck(args)
                    cc_obj.analyze()


class CppCheckTestArgs:

    def __init__(self, output_file, **kwargs):
        self.output_file = output_file
        self.sources = []
        self.list_files = []
        self.config_file = os.path.join(CppCheck.script_dir, "standard_config.ini")
        self.format = "xml"
        self.tcc_var = None
        self.install_path = None
        self.tcc_server_config = None
        self.tcc_var = "TCC_CPPCHECK"
        self.tcc_local_config = None

        for key in kwargs:
            assert key in self.__dict__
        self.__dict__.update(kwargs)


if __name__ == '__main__':
    unittest.main()
