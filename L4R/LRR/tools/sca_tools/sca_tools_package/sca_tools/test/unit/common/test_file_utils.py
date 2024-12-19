""" Tests for qac/file/file_utils.py """

from unittest import TestCase
from unittest.mock import patch, mock_open, call
from swq.common.file.file_utils import SHA_EXTENSION, \
    check_if_hashshum_file_exists_and_validate, \
    check_if_hashsum_is_valid_and_exit_if_not, move_file_to_target_folder, \
    read_sha256_from_metadata, remove_empty_lines_from_file, \
    write_sha256_to_metadata, hashsum_is_valid_for_file, copyfile_with_metadata


class TestFileUtils(TestCase):
    """Test file utils"""
    @patch('builtins.open', new_callable=mock_open, read_data="      \ndata")
    def test_remove_empty_lines_from_file(self, mock_file):
        """Test remove_empty_lines_from_file()"""
        remove_empty_lines_from_file('not/exist')

        calls = [
            call('not/exist',
                 mode='rt',
                 buffering=1,
                 encoding='utf-8',
                 errors='replace',
                 newline=None,
                 closefd=True,
                 opener=None),
            call().__enter__(),
            call().readlines(),
            call().__exit__(None, None, None),
            call('not/exist',
                 mode='wt',
                 buffering=1,
                 encoding='utf-8',
                 errors='replace',
                 newline=None,
                 closefd=True,
                 opener=None),
            call().__enter__(),
            call().writelines(['data']),
            call().__exit__(None, None, None)
        ]

        mock_file.assert_has_calls(calls)

    @patch('swq.common.file.file_utils.LOGGER', create=True)
    def test_write_sha256_to_metadata(self, logger):
        """Test write_sha256_to_metadata() method"""
        with patch('swq.common.file.file_utils.calculate_sha256') \
            as mock_get_sha, \
            patch('swq.common.file.file_utils.write_lines_to_file') \
            as mock_write_lines:
            expected_hash = 'expected_hash'
            filepath = 'some/path'
            mock_get_sha.return_value = expected_hash
            write_sha256_to_metadata(filepath)
            mock_get_sha.assert_called_once_with(filepath)
            logger.info.assert_called_once()
            mock_write_lines.assert_called_once_with(
                f'{filepath}.{SHA_EXTENSION}', [expected_hash])

    @patch('builtins.open', new_callable=mock_open, read_data='some_hash')
    def test_read_sha256_from_metadata(self, file_open):
        """Test read_sha256_from_metadata() method"""
        with patch('swq.common.file.file_utils.check_if_hashshum_file_exists')\
            as mock_check_if_exists:
            mock_check_if_exists.return_value = False
            filepath = 'some_file'
            actual_result = read_sha256_from_metadata(filepath)
            file_open.assert_not_called()
            self.assertEqual(actual_result, None)

            mock_check_if_exists.return_value = True
            actual_result = read_sha256_from_metadata(filepath)
            file_open.assert_called_once_with(f'{filepath}.{SHA_EXTENSION}',
                                              mode='rt',
                                              buffering=1,
                                              encoding='utf-8',
                                              errors='replace',
                                              newline=None,
                                              closefd=True,
                                              opener=None)
            self.assertEqual(actual_result, 'some_hash')

    @patch('swq.common.file.file_utils.LOGGER', create=True)
    def test_hashsum_is_valid_for_file(self, logger):
        """Test hashsum_is_valid_for_file() method"""
        with patch('swq.common.file.file_utils.calculate_sha256') \
            as mock_get_sha, \
            patch('swq.common.file.file_utils.read_sha256_from_metadata')\
            as mock_read:
            logger.reset_mock()
            mock_get_sha.return_value = 'some_hash'
            mock_read.return_value = 'some_hash'
            filepath = 'some/path'

            actual_result = hashsum_is_valid_for_file(filepath)
            self.assertEqual(actual_result, True)

            mock_get_sha.return_value = 'fake_hash'
            actual_result = hashsum_is_valid_for_file(filepath)
            self.assertEqual(actual_result, False)

    @patch('swq.common.file.file_utils.LOGGER', create=True)
    def test_check_if_hashsum_is_valid_and_exit_if_not(self, logger):
        """Test check_if_hashsum_is_valid_and_exit_if_not() method"""
        with patch('swq.common.file.file_utils.hashsum_is_valid_for_file') \
            as mock_check_hashsum, \
            patch('swq.common.file.file_utils.log_and_exit') \
            as mock_log_and_exit:
            mock_check_hashsum.return_value = False
            filepath = 'some/path'
            check_if_hashsum_is_valid_and_exit_if_not(filepath)
            logger.error.assert_called_once()
            mock_log_and_exit.assert_called_once()

            mock_log_and_exit.reset_mock()
            logger.reset_mock()
            mock_check_hashsum.return_value = True
            check_if_hashsum_is_valid_and_exit_if_not(filepath)
            mock_log_and_exit.assert_not_called()
            logger.error.asser_not_called()

    @patch('swq.common.file.file_utils.LOGGER', create=True)
    def test_copyfile_with_metadata(self, logger):
        """Test copyfile_with_metadata() method"""
        with patch('swq.common.file.file_utils.copyfile') as mock_copyfile, \
            patch('swq.common.file.file_utils.path') as mock_path, \
            patch('swq.common.file.file_utils.remove') as mock_remove, \
            patch('swq.common.file.file_utils.create_dirs_if_necessary') \
            as mock_create_dirs:
            logger.reset_mock()
            source_filepath = 'source/filepath'
            target_filepath = 'target/filepath'
            mock_path.exists.return_value = True
            copyfile_with_metadata(source_filepath, target_filepath)
            mock_copyfile.assert_has_calls([
                call(source_filepath, target_filepath),
                call(f'{source_filepath}.{SHA_EXTENSION}',
                     f'{target_filepath}.{SHA_EXTENSION}')
            ])
            mock_remove.assert_called_once_with(
                f'{target_filepath}.{SHA_EXTENSION}')
            mock_path.exists.assert_has_calls([
                call(f'{target_filepath}.{SHA_EXTENSION}'),
                call(f'{source_filepath}.{SHA_EXTENSION}')
            ])
            mock_create_dirs.assert_called_once_with(target_filepath)

            mock_remove.reset_mock()
            mock_copyfile.reset_mock()
            mock_path.reset_mock()
            mock_create_dirs.reset_mock()

            mock_path.exists.return_value = False
            copyfile_with_metadata(source_filepath, target_filepath)
            mock_copyfile.assert_has_calls([
                call(source_filepath, target_filepath),
            ])
            mock_remove.assert_not_called()
            mock_path.exists.assert_has_calls([
                call(f'{target_filepath}.{SHA_EXTENSION}'),
                call(f'{source_filepath}.{SHA_EXTENSION}')
            ])
            mock_create_dirs.assert_called_once_with(target_filepath)

    @patch('swq.common.file.file_utils.LOGGER', create=True)
    def test_check_if_hashshum_file_exists_and_validate(self, logger):
        """ Test check_if_hashshum_file_exists_and_validate() method """
        with patch('swq.common.file.file_utils.check_if_hashshum_file_exists')\
            as mock_check_if_exists, \
            patch('swq.common.file.file_utils.'
                  'check_if_hashsum_is_valid_and_exit_if_not') \
            as mock_check_if_valid:
            logger.reset_mock()
            mock_check_if_exists.return_value = False
            filepath = 'some/file'
            check_if_hashshum_file_exists_and_validate(filepath)
            mock_check_if_valid.assert_not_called()

            mock_check_if_exists.return_value = True
            check_if_hashshum_file_exists_and_validate(filepath)
            mock_check_if_valid.assert_called_once_with(filepath)

    @patch('swq.common.file.file_utils.LOGGER', create=True)
    def test_move_file_to_target_folder(self, logger):
        """ Test move_file_to_target_folder() method """
        with patch('swq.common.file.file_utils.replace') as mock_replace:
            logger.reset_mock()
            source_filepath = 'source'
            target_filepath = 'target'
            move_file_to_target_folder(source_filepath, target_filepath)
            mock_replace.assert_called_once_with(source_filepath,
                                                 target_filepath)
