#!/usr/bin/env python
# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	sca_tools.py
# ----------------------------------------------------------------------------
"""Entrypoint for all subcommands in SWQ. sca_tools backwards compatible"""
# pylint: disable=C0413
from pathlib import Path as pathlib_Path
from sys import version_info, path as sys_path

# Ensures sys.path is correctly setup
_HERE = pathlib_Path(__file__).parent
sys_path.insert(0, f'{_HERE}')
from swq import swq    # noqa

# python version check
assert version_info >= swq.PYTHON_MINIMUM_VERSION


def run():
    """Deferred run from sca_tools to swq"""
    swq.run()


if __name__ == "__main__":
    run()
