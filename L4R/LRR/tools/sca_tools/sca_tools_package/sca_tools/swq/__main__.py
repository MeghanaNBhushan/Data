# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	__main__.py
# ----------------------------------------------------------------------------
"""Entrypoint for all subcommands in SWQ"""
from sys import version_info
from swq import swq

# python version check
assert version_info >= swq.PYTHON_MINIMUM_VERSION


def run():
    """Deferred run from __main__ to swq"""
    swq.run()


if __name__ == "__main__":
    run()
