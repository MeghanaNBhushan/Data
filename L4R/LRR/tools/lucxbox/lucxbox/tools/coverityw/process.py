#!/usr/bin/python
""" common function for running commands with logging information """

import subprocess
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()


def run_command(full_command, exit_on_error=True, remove_password=None):
    if remove_password is not None:
        LOGGER.debug('Command: %s', full_command.replace(
            remove_password, '********'))
    else:
        LOGGER.debug('Command: %s', full_command)
    output = None
    try:
        output = subprocess.check_output(full_command, shell=True)
        LOGGER.debug('Output: %s', output)
    except subprocess.CalledProcessError as error:
        output = error.output
        error_message = 'Command returned error: %s'
        if exit_on_error:
            LOGGER.error(error_message, error.output)
            sys.exit(error.returncode)
        else:
            LOGGER.warning(error_message, error.output)
    return output
