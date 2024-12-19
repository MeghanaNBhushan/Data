# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	file_transfer.py
# ----------------------------------------------------------------------------
"""File transfer mechanism that checks on the file hash before copying"""

from os import path

from swq.common.logger import LOGGER
from swq.common.file.file_utils import SHA_EXTENSION, copyfile_with_metadata, \
    hashsum_is_valid_for_file, read_sha256_from_metadata


def _copy_files_if_hashes_are_different(source_folder, target_folder,
                                        filename):
    source_filepath = path.join(source_folder, filename)
    target_filepath = path.join(target_folder, filename)

    source_sha256 = read_sha256_from_metadata(source_filepath)
    target_sha256 = read_sha256_from_metadata(target_filepath)

    if source_sha256 is None:
        LOGGER.info('Source hashsum file %s is not found',
                    f'{source_filepath}.{SHA_EXTENSION}')
    elif target_sha256 is None:
        LOGGER.info('Target hashsum file %s is not found',
                    f'{target_filepath}.{SHA_EXTENSION}')
    elif source_sha256 != target_sha256:
        LOGGER.info('Source %s and target %s hashsums are different',
                    source_sha256, target_sha256)
    elif hashsum_is_valid_for_file(target_filepath):
        LOGGER.info('Source and target files are the same. '
                    'Local validation enabled and succeeded')
        return (target_folder, False)

    LOGGER.info('Downloading baseline file')
    copyfile_with_metadata(source_filepath, target_filepath)
    return (target_folder, True)


_NETWORK_WARNING_STR = '''Configured LOCAL_BASELINE_PATH is a network share.
Because of QAC performance reasons this file will be copied from %s to %s.

To avoid this mechanism either make sure LOCAL_BASELINE_PATH is not a network \
share. (Normally in the xxx.json)'''


def retrieve_file_from_remote_resource(
        source_folder, target_folder, filename):
    """If the source folder is a network folder then copy \
    the baseline locally if necessary"""
    def is_network_folder(filepath):
        return filepath.startswith('//') or filepath.startswith('\\\\')

    if is_network_folder(source_folder):
        LOGGER.info(_NETWORK_WARNING_STR, source_folder, target_folder)
        return _copy_files_if_hashes_are_different(source_folder,
                                                   target_folder, filename)

    return (source_folder, True)
