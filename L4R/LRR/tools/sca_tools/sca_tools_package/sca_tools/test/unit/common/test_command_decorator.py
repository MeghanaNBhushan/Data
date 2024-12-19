# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_command_decorator.py
# ----------------------------------------------------------------------------
""" Tests for external commands decorator """

import os
import tempfile
from unittest import TestCase, mock
from unittest.mock import patch
from subprocess import CalledProcessError
from swq.common.command import command_decorator
from swq.common.return_codes import RC_CMD_FAILED
from swq.common.constants import IS_WINDOWS


@patch('swq.common.command.command_decorator.LOGGER', create=True)
@patch('swq.common.command.command_decorator.Popen')
@patch('swq.common.command.command_decorator.PIPE')
@patch('swq.common.command.command_decorator.STDOUT')
class TestCommandDecorator(TestCase):
    """ TestCommandDecorator class """
    def setUp(self):
        self.config = mock.Mock(qacli='qacli.exe')
        self.stdout_mock = None

    def mocked_stdout(self):
        """ Mock Popen stdout """
        self.stdout_mock = tempfile.NamedTemporaryFile(delete=False)
        self.stdout_mock.write(b'STDOUT (mocked)')
        self.stdout_mock.seek(0)
        return self.stdout_mock

    def test_run_command(self, mock_stdout, mock_pipe, mock_popen, logger):
        """ Test run_command() """

        instance = mock_popen.return_value
        instance.stdout = self.mocked_stdout()
        instance.returncode = 0

        command_string = 'external_command'
        fast_fail = False
        build_shell = False
        use_logger = False
        silent = False

        with patch('swq.common.command.command_decorator.print') \
                as mock_print, \
                patch('swq.common.return_codes.sys_exit') as mock_sys_exit:

            expected_result = ['STDOUT (mocked)', 0]
            expected_command_string = command_string if IS_WINDOWS else (
                [command_string])
            result = command_decorator.run_command(command_string, fast_fail,
                                                   build_shell, use_logger,
                                                   silent)
            self.assertEqual(result, expected_result)
            mock_popen.assert_called_with(expected_command_string,
                                          stdout=mock_pipe,
                                          stderr=mock_stdout,
                                          shell=build_shell,
                                          cwd=mock.ANY)
            mock_sys_exit.assert_not_called()
            mock_print.assert_called()
            mock_print.reset_mock()

            use_logger = True
            instance.stdout = self.mocked_stdout()
            result = command_decorator.run_command(command_string, fast_fail,
                                                   build_shell, use_logger,
                                                   silent)
            self.assertEqual(result, expected_result)
            mock_print.assert_not_called()
            logger.info.assert_called()
            logger.reset_mock()

            silent = True
            instance.stdout = self.mocked_stdout()
            result = command_decorator.run_command(command_string, fast_fail,
                                                   build_shell, use_logger,
                                                   silent)
            self.assertEqual(result, expected_result)
            mock_print.assert_not_called()

            instance.stdout = self.mocked_stdout()
            instance.returncode = 1
            mock_popen.side_effect = CalledProcessError(1, 'bad cmd')
            expected_result = ['', 1]
            result = command_decorator.run_command(command_string, fast_fail,
                                                   build_shell, use_logger,
                                                   silent)
            self.assertEqual(result, expected_result)
            mock_sys_exit.assert_not_called()

            fast_fail = True
            result = command_decorator.run_command(command_string, fast_fail,
                                                   build_shell, use_logger,
                                                   silent)
            self.assertEqual(result, expected_result)
            logger.info.assert_called()
            mock_sys_exit.assert_called_once_with(RC_CMD_FAILED)
            self.stdout_mock.close()
            os.remove(self.stdout_mock.name)
