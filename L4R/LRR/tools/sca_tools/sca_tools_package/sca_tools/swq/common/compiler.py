# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: compiler.py
# ----------------------------------------------------------------------------
"""Compiler module for multithreading compile_commands execution"""

import logging
import sys
import json
import os
import argparse

from subprocess import Popen
from threading import Thread, Event
from queue import Queue
from time import time
from shlex import split as shlex_split

MODULE_NAME = 'compiler'
IS_WINDOWS = sys.platform == 'win32'

RC_INVALID_FILEPATH = 9
RC_MISSING_PARAMETER = 10

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [{}] [%(levelname)s] '
                    '%(message)s'.format(MODULE_NAME.upper()))
logger = logging.getLogger(__name__)

exit_event = Event()


def adapt_command_to_list_or_string_according_to_os(command_list: str):
    """Performs a transformation to the commandline to the OS it
    is running into"""
    # In an Unix system the commandline string needs to be split for
    # proper parameter forwarding and also it will break if parameters
    # are bound directly to the command string
    return command_list if IS_WINDOWS else shlex_split(command_list)


def check_if_filepath_exists_and_exit_if_not(file_path):
    """Checks filepath exists and exit if not"""
    if not os.path.exists(file_path):
        logger.error(
            'Path %s does not exist. Please provide'
            ' correct path. Exiting', file_path)
        sys.exit(RC_INVALID_FILEPATH)


class CommandRunner(Thread):
    """Command runner class"""
    def __init__(self, queue, commands_count, thread_number):
        Thread.__init__(self)
        self.queue = queue
        self.thread_number = thread_number
        self.commands_count = commands_count
        self._return_code = 0

    def _get_logger_prefix(self):
        return '[Thread {}] ({} of {})'.format(
            self.thread_number + 1, self.commands_count - self.queue.qsize(),
            self.commands_count)

    def _log_build_started(self, filename, command, directory):
        logger.info('%s Started: %s', self._get_logger_prefix(), filename)
        logger.info('%s Command: %s, cwd=%s', self._get_logger_prefix(),
                    command, directory)

    def _log_build_finished(self, filename, start_time, return_code):
        logger.info('%s Finished: %s took %.2fs', self._get_logger_prefix(),
                    filename,
                    time() - start_time)
        if return_code != 0:
            logger.error('%s Failed to compile %s! '
                         'Return code: %d', self._get_logger_prefix(),
                         filename, return_code)
            self._return_code = return_code
            exit_event.set()

    def run(self):
        while True:
            if exit_event.is_set() or self.queue.empty():
                break
            directory, command, filepath = self.queue.get()
            filename = os.path.basename(filepath)
            try:
                start_time = time()
                self._log_build_started(filename, command, directory)
                process = run_command(directory, command)
                process.wait()
                self._log_build_finished(filename, start_time,
                                         process.returncode)
            finally:
                self.queue.task_done()

    def join(self, timeout=None):
        Thread.join(self, timeout)
        return self._return_code


def run_command(directory, command):
    """Runs commandline from specified directory in
    a shell and returns the process"""
    command = adapt_command_to_list_or_string_according_to_os(command)
    process = Popen(cwd=os.path.normpath(directory), args=command, shell=False)
    return process


def get_list_of_compile_commands_data(compile_commands_filepath):
    """Returns list containing folders, commands and filenames
    from specified compile_commands.json"""
    list_of_compile_commands_data = []
    with open(compile_commands_filepath, mode='r') as compile_commands_content:
        json_content = json.load(compile_commands_content)
        for obj in json_content:
            list_of_compile_commands_data.append(
                [obj['directory'], obj['command'], obj['file']])
    return list_of_compile_commands_data


def create_multithread_parser():
    """Creates argument parser and then returns it"""
    parser = argparse.ArgumentParser(
        description='Helper for the paralleled compile commands execution')

    parser.add_argument('-f',
                        '--filepath',
                        help='Path to the compile_commands.json')
    parser.add_argument('-t',
                        '--threads',
                        type=int,
                        default=os.cpu_count(),
                        help='Specifies amount of threads')

    return parser


def get_filled_queue_from_list(list_of_compile_commands_data):
    """Creates and fills a queue with the data from compile_commands.json"""
    queue = Queue()

    for folder, command, filepath in list_of_compile_commands_data:
        queue.put((folder, command, filepath))

    return queue


def create_command_runners(threads_count, filled_queue, filled_queue_size):
    """Creates command runner threads"""
    runners = []

    for i in range(threads_count):
        runner = CommandRunner(filled_queue, filled_queue_size, i)
        runner.daemon = True
        runner.start()
        runners.append(runner)

    return runners


def get_return_code_from_runners(runners):
    """Returns the exit code from threads"""
    return_code = 0

    for runner in runners:
        return_code = runner.join()
        if return_code != 0:
            break

    return return_code


def run_compilation():
    """Entrypoint for compiler script"""
    multithread_parser = create_multithread_parser()
    parsed_args = multithread_parser.parse_args()

    if parsed_args.filepath is None:
        logger.error('Please provide file path to compile_commands.json')
        multithread_parser.print_help()
        sys.exit(RC_MISSING_PARAMETER)

    check_if_filepath_exists_and_exit_if_not(parsed_args.filepath)

    list_of_compile_commands_data = \
        get_list_of_compile_commands_data(parsed_args.filepath)
    filled_queue = \
        get_filled_queue_from_list(list_of_compile_commands_data)

    filled_queue_size = filled_queue.qsize()

    logger.info('Running compilation commands in %d threads',
                parsed_args.threads)
    command_runners = create_command_runners(parsed_args.threads, filled_queue,
                                             filled_queue_size)
    return_code = get_return_code_from_runners(command_runners)

    sys.exit(return_code)


if __name__ == '__main__':
    run_compilation()
