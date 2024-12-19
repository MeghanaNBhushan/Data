# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	constants.py
# ----------------------------------------------------------------------------
"""Defines constants for the swq.common scripts"""

from os import path
from pathlib import Path as pathlib_Path
from sys import platform as sys_platform

from swq.common.logger import LOGGER

SWQ_MODULE_PATH = pathlib_Path(__file__).parent.parent
IS_WINDOWS = sys_platform == 'win32'
SECURITY_SENSITIVE_ENVS = [
    'COVERITY_PASSPHRASE', 'COVERITY_PASSWORD', 'COV_USER',
    'COVERITY_USERNAME', 'QAV_PASSWORD', 'QAV_USERNAME'
]
COMMON_PARAMS_JSON = path.join(SWQ_MODULE_PATH, 'common', 'params',
                               'common_params.json')
COMPILER_WARNINGS_PARAMS_JSON = path.join(SWQ_MODULE_PATH, 'compiler_warnings',
                                          'params',
                                          'compiler_warnings_params.json')
COVERITY_PARAMS_JSON = path.join(SWQ_MODULE_PATH, 'coverity', 'params',
                                 'coverity_params.json')
FIND_INCLUDES_PARAMS_JSON = path.join(SWQ_MODULE_PATH, 'find_includes',
                                      'params', 'find_includes_params.json')
MAP_TEAMS_PARAMS_JSON = path.join(SWQ_MODULE_PATH, 'map_teams', 'params',
                                  'map_teams_params.json')
QAC_PARAMS_JSON = path.join(SWQ_MODULE_PATH, 'qac', 'params',
                            'qac_params.json')
UNIFY_REPORTS_PARAMS_JSON = path.join(SWQ_MODULE_PATH, 'unify_reports',
                                      'params', 'unify_reports_params.json')
LOGS_PREFIX = 'sca_tools'


def filter_sensitive_keys_from_dict(possible_dict_with_security_keys: dict,
                                    warn=False):
    """Filters out security sensitive keys from dictionary, if any"""
    filtered_dict = {}
    for key, value in possible_dict_with_security_keys.items():
        filtered_dict[key] = value
        if key.upper() in SECURITY_SENSITIVE_ENVS:
            if warn:
                LOGGER.warning(
                    "'%s' should not be used "
                    "from configuration file. Please, use environment "
                    "variables instead.", key.upper())
            filtered_dict[key] = '***'

    return filtered_dict
