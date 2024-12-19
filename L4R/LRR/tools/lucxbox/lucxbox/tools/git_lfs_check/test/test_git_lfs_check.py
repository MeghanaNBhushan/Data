""" Test for git lfs check """

import unittest
from unittest import mock

from lucxbox.tools.git_lfs_check import git_lfs_check


class TestStringMethods(unittest.TestCase):
    """ Test class for git lfs module """

    def test_get_wrong_files(self):
        git_all_files = set(["big.bin", "another.bin"])
        git_lfs_files = set(["big.bin", "another.bin"])
        git_lfs_attributes = set(["*.bin"])
        result = set(git_lfs_check.get_wrong_files(git_all_files, git_lfs_files, git_lfs_attributes))
        self.assertEqual(set([]), result)

    @mock.patch("subprocess.check_output")
    def test_get_wrong_files_missing(self, mock_check_output):
        mock_check_output.return_value = 'another.bin: filter: lfs\n'
        git_all_files = set(["big.bin", "another.bin"])
        git_lfs_files = set(["big.bin"])
        git_lfs_attributes = set(["*.bin"])
        result = set(git_lfs_check.get_wrong_files(git_all_files, git_lfs_files, git_lfs_attributes))
        self.assertEqual(set(["another.bin"]), result)

    @mock.patch("subprocess.check_output")
    def test_get_wrong_files_excludes(self, mock_check_output):
        mock_check_output.return_value = 'excluded.bin: filter: unspecified\n'
        git_all_files = set(["big.bin", "excluded.bin"])
        git_lfs_files = set(["big.bin"])
        git_lfs_attributes = set(["*.bin"])
        result = set(git_lfs_check.get_wrong_files(git_all_files, git_lfs_files, git_lfs_attributes))
        self.assertEqual(set([]), result)

    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.LOGGER", create=True)
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.get_lfs_attributes")
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.get_all_files")
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.get_lfs_files")
    def test_main_failing_sanity_check(self, mock_get_lfs_files, mock_get_all_files, \
            mock_get_lfs_attributes, mock_logger):
        mock_get_lfs_files.return_value = []
        mock_get_all_files.return_value = []
        mock_get_lfs_attributes.return_value = []
        with self.assertRaises(SystemExit) as exception:
            git_lfs_check.main(["git_lfs_check.py"])
        self.assertEqual(exception.exception.code, 1)
        expected_call = mock.call('Sanity check failed, %s.', 'no file tracked by git at all')
        self.assertEqual(1, len(mock_logger.error.mock_calls))
        self.assertEqual(expected_call, mock_logger.error.mock_calls[0])

    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.LOGGER", create=True)
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.sanity_check")
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.get_wrong_files")
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.get_lfs_attributes")
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.get_all_files")
    @mock.patch("lucxbox.tools.git_lfs_check.git_lfs_check.get_lfs_files")
    def test_main_fake_sanity_check(self, mock_get_lfs_files, mock_get_all_files, \
            mock_get_lfs_attributes, mock_get_wrong_files, mock_sanity_check, mock_logger):
        mock_get_lfs_files.return_value = []
        mock_get_all_files.return_value = []
        mock_get_lfs_attributes.return_value = []
        mock_get_wrong_files.return_value = set(["another.bin"])
        mock_sanity_check.return_value = True
        with self.assertRaises(SystemExit) as exception:
            git_lfs_check.main(["git_lfs_check.py"])
        self.assertEqual(exception.exception.code, 1)
        expected_call = mock.call('Following files should be under git-lfs control: %s', 'another.bin')
        self.assertEqual(1, len(mock_logger.error.mock_calls))
        self.assertEqual(expected_call, mock_logger.error.mock_calls[0])

if __name__ == "__main__":
    unittest.main()
