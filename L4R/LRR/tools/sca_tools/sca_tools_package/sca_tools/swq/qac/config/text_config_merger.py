# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: text_config_merger.py
# ----------------------------------------------------------------------------
"""Defines a plain text configuration files merger"""
from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t
from swq.qac.config.config_merger import ConfigMerger


class TextConfigMerger(ConfigMerger):
    """Defines a plain text configuration files merger class"""
    def _write_output_file(self, output_file_content: str):
        with open_t(self._output_filepath, mode='w') as output_file:
            output_file.write(output_file_content)

    def _parse_content(self):
        parsed_content = []

        for input_filepath in self._input_config_files:
            LOGGER.debug('Reading file from path %s', input_filepath)
            with open_t(input_filepath) as input_file:
                parsed_content.append(input_file.read())
        return parsed_content
