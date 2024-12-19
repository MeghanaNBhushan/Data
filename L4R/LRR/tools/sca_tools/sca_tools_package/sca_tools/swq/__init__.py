# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	__init__.py
# ----------------------------------------------------------------------------
""" INIT for swq"""
import os

__all__ = []
_EXCLUSION_LIST = ['__init__.py', '__main__.py']

for module in os.listdir(os.path.dirname(__file__)):
    if module not in _EXCLUSION_LIST and module[-3:] == '.py':
        __all__.append(module[:-3])
