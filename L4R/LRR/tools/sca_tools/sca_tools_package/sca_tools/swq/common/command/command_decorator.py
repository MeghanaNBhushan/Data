# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: command_decorator.py
# ----------------------------------------------------------------------------
""" External commands decorator """

import codecs
import sys

from subprocess import CalledProcessError, PIPE, Popen, STDOUT
from shlex import split as shlex_split
from time import time
from os import getcwd as os_getcwd, chdir as os_chdir
from typing import TextIO

from swq.common.return_codes import log_and_exit, RC_CMD_FAILED
from swq.common.filesystem.filesystem_utils import open_t
from swq.common.constants import IS_WINDOWS
from swq.common.logger import LOGGER


def _ensure_utf8_in_output(a_output):
    if a_output.encoding.upper() != 'UTF-8':
        return codecs.getwriter('utf-8')(a_output.buffer, 'strict')
    return a_output

def ensure_utf8_stdout_call_once():
    """Forces output in utf-8 encoding. Must only be called once \
    during initialization"""
    def _can_be_utf8_patched(a_output):
        return hasattr(a_output, 'encoding')

    if _can_be_utf8_patched(sys.stdout):
        sys.stdout = _ensure_utf8_in_output(sys.stdout)

    if _can_be_utf8_patched(sys.stderr):
        sys.stderr = _ensure_utf8_in_output(sys.stderr)


def _decode_and_redirect_to_outputs(line, use_logger: bool, silent: bool,
                                    output_file: TextIO):
    line_utf8 = line.decode('utf-8', errors='ignore').rstrip()
    if not silent:
        if use_logger:
            LOGGER.info_noformat('%s', line_utf8)
        else:
            print('{}\n'.format(line_utf8))
    if output_file:
        output_file.write('{}\n'.format(line_utf8))

    return line_utf8


def _needs_to_set_path(build_shell, working_dir):
    return not build_shell and working_dir


def _run_command(command_list: str, build_shell: bool, use_logger: bool,
                 silent: bool, output_filepath: str,
                 working_dir: str) -> (str, int):
    output = ''
    output_file = None
    if output_filepath:
        output_file = open_t(output_filepath, mode='w')
    command_string_or_list = adapt_command_to_list_or_string_according_to_os(
        command_list)
    # if build shell is native forces changing directory to avoid
    # on depending on the proper Python version before running the
    # command. Later restores it
    if _needs_to_set_path(build_shell, working_dir):
        previous_working_dir = os_getcwd()
        os_chdir(working_dir)
    LOGGER.debug('Arguments to Popen: %s', command_string_or_list)
    command_process = Popen(command_string_or_list,
                            stdout=PIPE,
                            stderr=STDOUT,
                            shell=build_shell,
                            cwd=working_dir)
    subprocess_output = (_decode_and_redirect_to_outputs(
        line, use_logger, silent,
        output_file) for line in iter(command_process.stdout.readline, b''))
    output = '\n'.join(list(subprocess_output))
    command_process.stdout.close()
    command_process.wait()
    if output_file:
        output_file.close()
    # Restores the previous working directory if necessary
    if _needs_to_set_path(build_shell, working_dir):
        os_chdir(previous_working_dir)

    return (output, command_process.returncode)


def adapt_command_to_list_or_string_according_to_os(command_list: str):
    """Performs a transformation to the commandline to the OS it
    is running into"""
    # In an Unix system the commandline string needs to be split for
    # proper parameter forwarding and also it will break if parameters
    # are bound directly to the command string
    return command_list if IS_WINDOWS else shlex_split(command_list)


# Make it private, this should not be called directly (use decorator)
# And then remove default parameters values
def run_command(command_string: str,
                fast_fail: bool = True,
                build_shell: bool = False,
                use_logger: bool = True,
                silent: bool = False,
                output_filepath: str = None,
                cwd: str = None) -> (str, int):
    """Runs commandline in a shell and gets it's output result"""
    return_code = 0
    output = ""
    start = time()
    LOGGER.info(
        "Command: %s\n Command Args: current_dir=%s, "
        "fast_fail=%s, build_shell=%s, use_logger=%s, silent=%s, "
        "output_filepath=%s, cwd=%s", command_string, os_getcwd(), fast_fail,
        build_shell, use_logger, silent, output_filepath, cwd)

    try:
        (output, return_code) = _run_command(command_string, build_shell,
                                             use_logger, silent,
                                             output_filepath, cwd)
    except CalledProcessError as command_error:
        LOGGER.warning("Exception: %s", command_error)
        LOGGER.warning(command_error.output)
        if fast_fail:
            log_and_exit(RC_CMD_FAILED)
        return_code = command_error.returncode

    end = time()
    LOGGER.info("Running command finished in %s with return code %s",
                end - start, return_code)
    return [output, return_code]


def command(fail_fast: bool = True,
            build_shell: bool = False,
            use_logger: bool = True,
            silent: bool = False,
            output_filepath: str = None,
            cwd: str = None) -> (str, int):
    """Decorator for the 'command' function
    """
    def command_decorator(function):
        def function_wrapper(*args, **kwargs):
            command_list = function(*args, **kwargs)
            command_string = " ".join(
                [str(command_part) for command_part in command_list])
            return run_command(command_string,
                               fast_fail=fail_fast,
                               build_shell=build_shell,
                               use_logger=use_logger,
                               silent=silent,
                               output_filepath=output_filepath,
                               cwd=cwd)

        return function_wrapper

    return command_decorator
