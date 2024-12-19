# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac_version.py
# ----------------------------------------------------------------------------
""" Test qac/qac_version.py """

from unittest import TestCase, mock
from swq.qac.qac_version import QacVersion


@mock.patch('swq.qac.qac_version.LOGGER', create=True)
class TestQacVersion(TestCase):
    """ Test QacVersion class """
    def test_helix_qac_version_2019_1(self, logger):
        """ Test Helix QAC version 2019.1 """
        qac_version = QacVersion('Helix QAC 2019.1')
        self.assertTrue(qac_version.is_helix())
        self.assertFalse(qac_version.is_prqa())
        self.assertEqual((2019, 1), qac_version.major_minor())
        logger.warning.assert_not_called()

    def test_helix_prqa_2_3(self, logger):
        """ Test PRQA Framework version 2.3 """
        qac_version = QacVersion('PRQA Framework version 2.3.0.9377-qax')
        self.assertTrue(qac_version.is_prqa())
        self.assertFalse(qac_version.is_helix())
        self.assertEqual((2, 3), qac_version.major_minor())
        logger.warning.assert_not_called()

    def test_invalid_version(self, logger):
        """ Test invalid version """
        qac_version = QacVersion('NotQAC 128213')
        self.assertFalse(qac_version.is_prqa())
        self.assertFalse(qac_version.is_helix())
        self.assertEqual((0, 0), qac_version.major_minor())
        logger.warning.assert_called()
