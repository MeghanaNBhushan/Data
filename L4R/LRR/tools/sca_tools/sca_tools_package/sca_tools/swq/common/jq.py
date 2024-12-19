# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: jq.py
# ----------------------------------------------------------------------------
"""JQ module"""

from plumbum import local
from swq.common.logger import LOGGER
from swq.common.return_codes import RC_CMD_FAILED, log_and_exit


POSSIBLE_JQ_BIN_NAMES = ['jq', 'jq-win32', 'jq-win64', 'jq-linux32',
                         'jq-linux64', 'jq-linux-x86_64', 'jq-linux-x86']


def get_jq():
    """Gets JQ as a plumbum instance"""
    for jq_bin_name in POSSIBLE_JQ_BIN_NAMES:
        if jq_bin_name in local:
            return local[jq_bin_name]

    LOGGER.error('JQ binary was not found in PATH. Scanned binary names: '
                 f'{POSSIBLE_JQ_BIN_NAMES}')
    log_and_exit(RC_CMD_FAILED)
