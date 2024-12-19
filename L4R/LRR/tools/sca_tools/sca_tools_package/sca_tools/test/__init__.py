# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: __init__.py
# ----------------------------------------------------------------------------
"""INIT for all tests"""
import logging
from swq.common.logger import LOGGER

logging.disable()
LOGGER.initialize_once('SCA_TOOLS_TEST')
