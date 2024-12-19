# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	return_codes.py
# ----------------------------------------------------------------------------
"""Defines swq.common return codes for the scripts"""

import platform

from getpass import getuser as getpass_getuser
from json import dumps as json_dumps
from inspect import stack as inspect_stack
from os import getcwd as os_getcwd
from os import environ as os_environ
from sys import exit as sys_exit
from sys import version as sys_version
from re import findall as re_findall
from socket import gethostname as socket_gethostname
from socket import gethostbyname as socket_gethostbyname
from uuid import getnode as uuid_getnode
from psutil import virtual_memory as psutil_virtual_memory

from swq.common.constants import filter_sensitive_keys_from_dict
from swq.common.logger import LOGGER

RC_SUCCESS = 0
RC_INVALID_CMD_PARAMETERS = 1
RC_CMD_FAILED = 2
RC_CONFIG_NOT_FOUND = 3
RC_CONFIG_PARSING_ERROR = 4
RC_ANALYZE_ERROR = 5
RC_SYNC_ERROR = 6
RC_PROJECT_DOES_NOT_EXIST = 7
RC_EXPORT_FAILED = 8
RC_INVALID_FILEPATH = 9
RC_MISSING_PARAMETER = 10
RC_WEB_API_CALL_FAILED = 11
RC_FINDINGS_LARGER_THAN_THRESHOLD = 12
RC_BUILD_ERROR = 13
RC_JUSTIFICATION_FAIL_CRITERIA = 14
RC_FINDINGS_AND_JUSTIFICATIONS_DO_NOT_MEET_CRITERIA = 15
RC_FILE_PARSE_FAILED = 16
RC_MESSAGE_ID_NOT_UNIQUE = 17
RC_RCF_RULE_GROUP_NOT_UNIQUE = 18
RC_TRIAGE_CLASSIFICATION_ISSUE_FOUND = 19
RC_INVALID_PARAMETER = 20
RC_FILES_NOT_EXIST_IN_PROJECT = 21
RC_QAC_MODULES_NOT_DEFINED = 22
RC_QAC_CONFIGURATION_INCONSISTENT = 23
RC_QAC_MODULES_VERSION_MISMATCH = 24
RC_HASHSUM_MISMATCH = 25
RC_INVALID_OR_CORRUPTED_COMPRESSED_FILE = 26
RC_COMPILER_UNSUPPORTED = 27

_TRANSLATION_DICT = {
    RC_SUCCESS: "SUCCESS",
    RC_INVALID_CMD_PARAMETERS: "INVALID_CMD_PARAMETERS",
    RC_CMD_FAILED: "CMD_FAILED",
    RC_CONFIG_NOT_FOUND: "CONFIG_NOT_FOUND",
    RC_CONFIG_PARSING_ERROR: "CONFIG_PARSING_ERROR",
    RC_ANALYZE_ERROR: "ANALYZE_ERROR",
    RC_SYNC_ERROR: "SYNC_ERROR",
    RC_PROJECT_DOES_NOT_EXIST: "PROJECT_DOES_NOT_EXIST",
    RC_EXPORT_FAILED: "EXPORT_FAILED",
    RC_INVALID_FILEPATH: "INVALID_FILEPATH",
    RC_MISSING_PARAMETER: "MISSING_PARAMETER",
    RC_WEB_API_CALL_FAILED: "WEB_API_CALL_FAILED",
    RC_FINDINGS_LARGER_THAN_THRESHOLD: "FINDINGS_LARGER_THAN_THRESHOLD",
    RC_BUILD_ERROR: "BUILD_ERROR",
    RC_FILES_NOT_EXIST_IN_PROJECT: "FILES_NOT_EXIST_IN_PROJECT",
    RC_INVALID_PARAMETER: "INVALID_PARAMETER",
    RC_QAC_MODULES_NOT_DEFINED: "QAC_MODULES_NOT_DEFINED",
    RC_QAC_CONFIGURATION_INCONSISTENT: "QAC_CONFIGURATION_INCONSISTENT",
    RC_QAC_MODULES_VERSION_MISMATCH: "QAC_MODULES_VERSION_MISMATCH",
    RC_FILE_PARSE_FAILED: "FILE_PARSE_FAILED",
    RC_HASHSUM_MISMATCH: "HASHSUM_MISMATCH",
    RC_INVALID_OR_CORRUPTED_COMPRESSED_FILE:
    "INVALID_OR_CORRUPTED_COMPRESSED_FILE",
    RC_COMPILER_UNSUPPORTED: "COMPILER_UNSUPPORTED"
}


def _get_system_info():
    try:
        info = {}
        info['platform_system'] = platform.system()
        info['platform_release'] = platform.release()
        info['platform_version'] = platform.version()
        info['platform_architecture'] = platform.machine()
        info['python_version'] = sys_version
        info['hostname'] = socket_gethostname()
        info['username'] = getpass_getuser()
        info['cwd'] = os_getcwd()
        info['ip_address'] = socket_gethostbyname(socket_gethostname())
        info['mac_address'] = ':'.join(
            re_findall('..', '%012x' % uuid_getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil_virtual_memory().total /
                                (1024.0**3))) + " GB"
        env_dict = {k: os_environ[k] for k in os_environ}
        info['env'] = filter_sensitive_keys_from_dict(env_dict)

        return info
    except Exception as exception:
        LOGGER.error(exception)
        return {}


def _lookup_return_code_from_value(return_code):
    rc_message = _TRANSLATION_DICT.get(return_code)
    if rc_message:
        return f'{rc_message}({return_code})'

    return f'UNKNOWN({return_code})'


def log_and_exit(error_code):
    """Logs error code and exits"""
    rc_message = _lookup_return_code_from_value(error_code)
    if error_code == RC_SUCCESS:
        LOGGER.info('Exiting with exit code %s', rc_message)
    else:
        LOGGER.debug('System info:\n%s\n', json_dumps(_get_system_info()))

        stacktrace = list([
            '\tFile {}, line {} in {} called from {}'.format(
                stack.filename, stack.lineno,
                ''.join(stack.code_context[0].split()), stack.function)
            for stack in inspect_stack()
        ])
        stacktrace = stacktrace[::-1]
        stacktrace.insert(0, 'Traceback (most recent call last):')

        LOGGER.error('\n'.join(stacktrace))

        LOGGER.error('Exiting with error code %s', rc_message)
    sys_exit(error_code)


def check_return_code_for_cmd_and_exit_if_failed(return_code):
    """Checks for return code not equal to zero"""
    if return_code != 0:
        LOGGER.error(f'Detected error code = {return_code}')
        log_and_exit(RC_CMD_FAILED)
