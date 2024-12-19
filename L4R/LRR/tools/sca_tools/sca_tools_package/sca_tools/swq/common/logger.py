# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: logger.py
# ----------------------------------------------------------------------------
"""Logger that on all levels to console"""

import logging
from sys import stdout


class Logger:
    """Wrapper class for Logging facilities"""

    _formatter = None
    _formatter_message_only = None
    _stdout_handler = None
    _file_handler = None
    _current_log_level = logging.INFO
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger()
        self._formatter_message_only = logging.Formatter('%(message)s')

    def debug(self, message: str, *args, **kwargs):
        """Logs debug message"""
        self._logger.debug(message, *args, **kwargs)

    def initialize_once(self, module_name):
        """Initializes the logger mechanism given the module name"""
        self._stdout_handler = logging.StreamHandler(stdout)
        self._formatter = logging.Formatter(
            '%(asctime)s [{}] [%(levelname)s] %(message)s'.format(module_name))
        self._stdout_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._stdout_handler)
        self._update_logger()

    def error(self, message: str, *args, **kwargs):
        """Logs error message"""
        self._logger.error(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Logs info message"""
        self._logger.info(message, *args, **kwargs)

    def info_noformat(self, message: str, *args, **kwargs):
        """Logs info message without formatting"""
        self._set_message_only_format()
        self._logger.info(message, *args, **kwargs)
        self._set_full_format()

    def initialize_file_once(self, log_filepath):
        """Initializes the file logging into a given filepath"""
        self._file_handler = logging.FileHandler(log_filepath)
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)
        self._update_logger()

    def _update_logger(self):
        if self._file_handler:
            self._file_handler.setLevel(self._current_log_level)
        if self._stdout_handler:
            self._stdout_handler.setLevel(self._current_log_level)
        self._logger.setLevel(self._current_log_level)

    def _set_message_only_format(self):
        if self._stdout_handler:
            self._stdout_handler.setFormatter(self._formatter_message_only)
        if self._file_handler:
            self._file_handler.setFormatter(self._formatter_message_only)

    def _set_full_format(self):
        if self._stdout_handler:
            self._stdout_handler.setFormatter(self._formatter)
        if self._file_handler:
            self._file_handler.setFormatter(self._formatter)

    def set_verbose(self):
        """Sets the verbose logging level"""
        self._current_log_level = logging.DEBUG
        self._update_logger()

    def warning(self, message: str, *args, **kwargs):
        """Logs warning message"""
        self._logger.warning(message, *args, **kwargs)


LOGGER = Logger()
