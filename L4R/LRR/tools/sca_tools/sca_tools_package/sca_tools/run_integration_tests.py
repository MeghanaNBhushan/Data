# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2020 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
# Filename: 	run_integration_tests.py
# Author(s): 	Andre Silva (CC-AD/ESW4)
# ----------------------------------------------------------------------------

import unittest
import integration_test.all_tests

testSuite = integration_test.all_tests.create_test_suite()
text_runner = unittest.TextTestRunner().run(testSuite)
