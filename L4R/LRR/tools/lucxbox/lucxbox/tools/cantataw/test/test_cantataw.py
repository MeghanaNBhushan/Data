""" Testing the Cantata wrapper """

import os
import sys
import unittest
from unittest import mock

import lucxbox.tools.cantataw.cantataw as cantataw


class TestCLI(unittest.TestCase):
    """Test class for the command line interface"""

    def test_non_existent_step(self):
        with self.assertRaises(SystemExit):
            cantataw.main(['cantataw.py', os.path.join('e2e', 'windows.json'), 'foo'])

    def test_non_existent_config(self):
        with self.assertRaises(IOError):
            cantataw.main(['cantataw.py', 'non-existent.json', 'build'])


class TestSchema(unittest.TestCase):
    """Test class for validation against schema"""

    def setUp(self):
        self.valid_configuration = {
            'env_script': 'setenv.bat',
            'build': 'build.bat build_args',
            'test': 'build.bat test_args',
            'report': {
                'cov_file': 'coverage_input.cov',
                'output': 'coverage_output',
                'report_types': ['stmt', 'func', 'call', 'decn']
            }
        }
        self.schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema/v0.1.json')
        self.mock_logger = mock.patch('lucxbox.tools.cantataw.cantataw.LOGGER')
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_valid_configuration(self):
        cantataw.validate(self.valid_configuration, self.schema_path)

    def test_missing_required_property(self):
        configuration = self.valid_configuration
        del configuration['build']
        with self.assertRaises(SystemExit):
            cantataw.validate(configuration, self.schema_path)

    def test_no_additional_properties(self):
        configuration = self.valid_configuration
        configuration['additionalProperty'] = 'test'
        with self.assertRaises(SystemExit):
            cantataw.validate(configuration, self.schema_path)

    def test_invalid_report_type(self):
        configuration = self.valid_configuration
        configuration['report']['report_types'] = [42]
        with self.assertRaises(SystemExit):
            cantataw.validate(configuration, self.schema_path)


class TestBuild(unittest.TestCase):
    """Test class for build step functionality"""

    def setUp(self):
        self.env = {}
        self.arg1 = 'arg1'
        self.arg2 = 'arg2'
        self.arguments = '{} {}'.format(self.arg1, self.arg2)
        self.build_script = 'build.bat' if os.name == 'nt' else 'build.sh'
        self.mock_logger = mock.patch('lucxbox.tools.cantataw.cantataw.LOGGER')
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @mock.patch('lucxbox.tools.cantataw.cantataw.subprocess.check_call')
    def test_ignore_cwd_if_abs_path(self, mock_check_call):
        absolute_path_program = os.path.abspath(os.path.join(os.path.sep, 'Program', self.build_script))
        cwd = os.path.abspath(os.path.join(os.path.sep, 'Temp'))

        cantataw.build('{} {}'.format(absolute_path_program, self.arguments), cwd, self.env)

        mock_check_call.assert_called_with(args=[absolute_path_program, self.arg1, self.arg2], cwd=cwd, env=self.env, shell=True)

    @mock.patch('lucxbox.tools.cantataw.cantataw.subprocess.check_call')
    def test_cwd_used_if_rel_path(self, mock_check_call):
        relative_path_program = os.path.join('..', 'test', self.build_script)
        cwd = os.path.abspath(os.path.join(os.path.sep, 'Program Files'))

        cantataw.build('{} {}'.format(relative_path_program, self.arguments), cwd, self.env)

        expected_path = os.path.join(cwd, relative_path_program)
        mock_check_call.assert_called_with(args=[expected_path, self.arg1, self.arg2], cwd=cwd, env=self.env, shell=True)


class TestTest(unittest.TestCase):
    """Test class for test step functionality"""

    def setUp(self):
        self.env = {}
        self.arg1 = 'arg1'
        self.arg2 = 'arg2'
        self.arguments = '{} {}'.format(self.arg1, self.arg2)
        self.test_executable = 'test.exe' if os.name == 'nt' else 'test'
        self.mock_logger = mock.patch('lucxbox.tools.cantataw.cantataw.LOGGER')
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @mock.patch('lucxbox.tools.cantataw.cantataw.subprocess.check_call')
    def test_ignore_cwd_if_abs_path(self, mock_check_call):
        absolute_path_program = os.path.abspath(os.path.join(os.path.sep, 'Program', self.test_executable))
        cwd = os.path.abspath(os.path.join(os.path.sep, 'Temp'))

        cantataw.test('{} {}'.format(absolute_path_program, self.arguments), cwd, self.env)

        mock_check_call.assert_called_with(args=[absolute_path_program, self.arg1, self.arg2], cwd=cwd, env=self.env, shell=True)

    @mock.patch('lucxbox.tools.cantataw.cantataw.subprocess.check_call')
    def test_cwd_used_if_rel_path(self, mock_check_call):
        relative_path_program = os.path.join('..', 'test', self.test_executable)
        cwd = os.path.abspath(os.path.join(os.path.sep, 'Program Files'))

        cantataw.test('{} {}'.format(relative_path_program, self.arguments), cwd, self.env)

        expected_path = os.path.join(cwd, relative_path_program)
        mock_check_call.assert_called_with(args=[expected_path, self.arg1, self.arg2], cwd=cwd, env=self.env, shell=True)


class TestEnvironmentFromScriptWindows(unittest.TestCase):
    """Test class for integration test of calling a script which sets environment variables"""

    def setUp(self):
        self.mock_logger = mock.patch('lucxbox.tools.cantataw.cantataw.LOGGER')
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @unittest.skipUnless(sys.platform.startswith('win'), 'requires Windows')
    def test_set_environment_via_script(self):
        cwd = os.path.join(os.path.dirname(__file__), 'int')
        script = 'setenv.bat'

        actual = cantataw.environment_from_script(script, cwd)

        expected = {
            'CANTATA_DIR': 'C:\\TCC\\Tools\\cantata\\8.0.0-2_WIN64',
            'A': 'B=C='
        }
        for key, value in expected.items():
            self.assertEqual(value, actual[key])
        self.assertIn('C:\\TCC\\Tools\\cantata\\8.0.0-2_WIN64\\bin', actual['Path'].split(os.pathsep))

    @unittest.skipUnless(sys.platform.startswith('win'), 'requires Windows')
    def test_set_environment_encoding(self):
        cwd = os.path.join(os.path.dirname(__file__), 'int')
        script = 'setenv.bat'

        env = cantataw.environment_from_script(script, cwd)

        for key, value in env.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(value, str))


class TestEnvironmentFromScriptLinux(unittest.TestCase):
    """Test class for integration test of calling a script which sets environment variables"""

    def setUp(self):
        self.mock_logger = mock.patch('lucxbox.tools.cantataw.cantataw.LOGGER')
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @unittest.skipUnless(not sys.platform.startswith('win'), 'requires Linux')
    def test_set_environment_via_script(self):
        cwd = os.path.join(os.path.dirname(__file__), 'int')
        script = 'setenv.sh'

        actual = cantataw.environment_from_script(script, cwd)

        expected = {
            'CANTATA_DIR': '/opt/TCC/Tools/cantata/8.0.0-2_LINUX',
            'A': 'B=C='
        }
        for key, value in expected.items():
            self.assertEqual(value, actual[key])
        self.assertIn('/opt/TCC/Tools/cantata/8.0.0-2_LINUX/bin', actual['PATH'].split(os.pathsep))

    @unittest.skipUnless(not sys.platform.startswith('win'), 'requires Linux')
    def test_set_environment_encoding(self):
        cwd = os.path.join(os.path.dirname(__file__), 'int')
        script = 'setenv.sh'

        env = cantataw.environment_from_script(script, cwd)

        for key, value in env.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(value, str))


if __name__ == '__main__':
    unittest.main()
