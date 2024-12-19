# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: xml_config_merger.py
# ----------------------------------------------------------------------------
"""Defines an XML configuration files merger"""
import xml.etree.ElementTree as ET

from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, RC_FILE_PARSE_FAILED
from swq.qac.config.config_merger import ConfigMerger


class XMLConfigMerger(ConfigMerger):
    """Defines an XML configuration merger class"""
    def _write_output_file(self, xml_root_content: ET.Element):
        xml_tree = ET.ElementTree(xml_root_content)
        xml_tree.write(self._output_filepath,
                       encoding='utf-8',
                       xml_declaration=True)

        return self._output_filepath

    def _parse_content(self):
        parsed_content = []

        for xml_file in self._input_config_files:
            try:
                LOGGER.debug('Reading file from path %s', xml_file)
                xml_tree = ET.parse(xml_file)
                parsed_content.append(xml_tree.getroot())
            except ET.ParseError as parse_error:
                LOGGER.error('Parsing file %s failed due to %s', xml_file,
                             parse_error)
                log_and_exit(RC_FILE_PARSE_FAILED)

        return parsed_content
