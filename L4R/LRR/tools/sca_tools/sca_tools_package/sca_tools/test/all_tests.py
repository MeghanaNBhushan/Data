# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2020 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
# Filename: 	all_tests.py
# Author(s): 	Andre Silva (CC-AD/ESW4)
# ----------------------------------------------------------------------------

from unittest import defaultTestLoader, TestSuite
from pathlib import Path


def create_test_suite():
    test_filepaths = Path('.').glob('test/**/test_*.py')
    modules = [
        '{}.{}'.format('.'.join(filename.parts[:-1]),
                       filename.stem)
        for filename in test_filepaths
    ]
    tests_to_load = [
        defaultTestLoader.loadTestsFromName(name) for name in modules
    ]

    return TestSuite(tests_to_load)
