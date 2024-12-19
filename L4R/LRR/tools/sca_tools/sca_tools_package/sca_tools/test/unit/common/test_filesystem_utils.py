""" Tests for qac/filesystem/filesystem_utils.py """
from os import getcwd

from unittest import TestCase
from unittest.mock import patch
from swq.common.filesystem.filesystem_utils import check_if_project_exists
from swq.common.return_codes import RC_PROJECT_DOES_NOT_EXIST


class TestFilesystemUtils(TestCase):
    """Test filesystem utils"""
    @patch('swq.common.filesystem.filesystem_utils.LOGGER', create=True)
    def test_check_if_project_exists(self, logger):
        """ Test check_if_project_exists() with real path """
        self.assertIsNone(check_if_project_exists(getcwd()))
        logger.assert_not_called()

    @patch('swq.common.filesystem.filesystem_utils.LOGGER', create=True)
    def test_check_if_project_not_exists(self, logger):
        """ Test check_if_project_exists() with unexisting path """
        with self.assertRaises(SystemExit) as expected_exception:
            check_if_project_exists('directory/not/exist')
        self.assertEqual(expected_exception.exception.code,
                         RC_PROJECT_DOES_NOT_EXIST)
        logger.error.assert_called()
