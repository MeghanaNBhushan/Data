# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: user_messages_config_merger.py
# ----------------------------------------------------------------------------
"""Defines a User Messages configuration merger"""
import xml.etree.ElementTree as ET

from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, RC_MESSAGE_ID_NOT_UNIQUE
from swq.qac.config.xml_config_merger import XMLConfigMerger


class UserMessagesConfigMerger(XMLConfigMerger):
    """Defines a User Messages configuration merger class"""

    _merged_filename = 'merged_user_messages.xml'

    def _append_messages_to_merged_xml_root(self, merged_xml_root,
                                            parsed_content):
        for xml_root in parsed_content:
            for component_messages in xml_root.iter('messages'):
                component_xpath = "messages[@component='%s']" % \
                    component_messages.attrib['component']
                if merged_xml_root.findall(component_xpath):
                    matched_messages_node = merged_xml_root.find(
                        component_xpath)
                    for message in component_messages.iter('message'):
                        message_id = message.attrib['id']
                        message_xpath = "message[@id='%s']" % message_id
                        if matched_messages_node.findall(message_xpath):
                            LOGGER.error(
                                "Merging failed due to overlapping "
                                "message with id %s", message_id)
                            log_and_exit(RC_MESSAGE_ID_NOT_UNIQUE)
                        else:
                            matched_messages_node.append(message)
                else:
                    merged_xml_root.append(component_messages)

    def merge_contents(self, parsed_content: list):
        """Merges user messages XML files content"""
        merged_xml_root = ET.Element('user_messages')
        merged_xml_root.text = "\n\t"
        merged_xml_root.tail = "\n"

        self._append_messages_to_merged_xml_root(merged_xml_root,
                                                 parsed_content)

        return merged_xml_root
