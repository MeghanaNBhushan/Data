""" Test for coverityw """

import os
import unittest
from unittest import mock

from lucxbox.tools.coverityw.coverityw import Coverity
from lucxbox.tools.coverityw.parameters import Parameters


# obs: for tests to run correctly, parameters in test_configuration.ini must reflect the values here

def create_command(coverity_exe):
    command = os.path.join('C:\\TCC\\Tools\\coverity\\2018.03-1_WIN64\\bin', coverity_exe)
    return command


def add_temp_folder():
    return ' --dir "temp"'


def add_user_password(user, password):
    return ' --user "{user}" --password "{password}"'.format(user=user, password=password)


class TestCoverity(unittest.TestCase):
    """ test coveriy class """

    def setUp(self):
        self.mock_parameters_logger = mock.patch("lucxbox.tools.coverityw.parameters.LOGGER")
        self.mock_parameters_logger.start()
        self.mock_coverity_logger = mock.patch("lucxbox.tools.coverityw.coverityw.LOGGER")
        self.mock_coverity_logger.start()
        self.user_name = 'user_test'
        self.user_password = 'password'
        self.par = Parameters(
            os.path.join(os.path.dirname(__file__), 'test_configuration.ini'),
            output_dir='temp',
            build_command='echo test',
            user_name=self.user_name,
            user_password=self.user_password)
        self.cov = Coverity(self.par.coverity_configuration, self.par.compiler_configuration)
        self.addCleanup(self.mock_parameters_logger.stop)
        self.addCleanup(self.mock_coverity_logger.stop)

    def test_input_parameters(self):
        # the idea of this test is to go through all the configurations, read the ini file
        # and make sure nothing breaks until the end of it
        self.assertIsNotNone(self.cov)

    @mock.patch('subprocess.check_output')
    def test_coverity_configure(self, mock_check_output):
        self.cov.configure()

        command = create_command('cov-configure')
        command += ' --compiler=gcc --comptype gcc --template'
        mock_check_output.assert_called_with(command, shell=True)

    @mock.patch('subprocess.check_output')
    def test_converity_build(self, mock_check_output):
        self.cov.build()

        command = create_command('cov-build') + add_temp_folder()
        command += ' --emit-complementary-info echo test'
        mock_check_output.assert_called_with(command, shell=True)

    @mock.patch('subprocess.check_output')
    def test_converity_emit(self, mock_check_output):
        self.cov.emit('list')

        command = create_command('cov-manage-emit') + add_temp_folder()
        command += ' list'
        mock_check_output.assert_called_with(command, shell=True)

    @mock.patch('subprocess.check_output')
    def test_converity_analyse(self, mock_check_output):
        self.cov.analyze()

        command = create_command('cov-analyze') + add_temp_folder()
        command += ' --all'
        mock_check_output.assert_called_with(command, shell=True)

    @mock.patch('subprocess.check_output')
    def test_converity_commit(self, mock_check_output):
        self.cov.commit(self.user_name, self.user_password)

        command = create_command('cov-commit-defects') + add_temp_folder()
        command += ' --host "abts5364" --port "8080" --stream "coverity-example"'
        command += add_user_password(self.user_name, self.user_password)
        mock_check_output.assert_called_with(command, shell=True)


if __name__ == '__main__':
    unittest.main()
