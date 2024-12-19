# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: rcf_config_merger.py
# ----------------------------------------------------------------------------
"""Defines a RCF configuration merger"""

import xml.etree.ElementTree as ET

from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, RC_RCF_RULE_GROUP_NOT_UNIQUE
from swq.qac.config.xml_config_merger import XMLConfigMerger


def _check_for_duplication_and_exit_if_found(merged_rcf_root, rule_group_name):
    """Checks for duplication in rcf files and exit if found"""
    if merged_rcf_root.findall(rule_group_name):
        LOGGER.error(
            "Merging failed due to overlapping "
            "rule_group with name %s", rule_group_name)
        log_and_exit(RC_RCF_RULE_GROUP_NOT_UNIQUE)


def _remove_mapped_no(rule_group):
    for rule in rule_group.iter('rule'):
        enforcements = rule.findall('enforcement')
        for enforcement in enforcements:
            messages = enforcement.findall('message')
            for message in messages:
                if message.attrib['mapped'] == 'no':
                    LOGGER.debug('Remove message: %s', ET.tostring(message))
                    enforcement.remove(message)


def _append_rcf_to_merged_rcf_root(merged_rcf_root, parsed_content):
    """Append rcf rulegroups to merged rcf file"""
    for rcf_root in parsed_content:
        for rule_group in rcf_root.iter('rulegroup'):
            rule_group_name_xpath = "rulegroup[@name='%s']" % \
                rule_group.attrib['name']
            _remove_mapped_no(rule_group)
            _check_for_duplication_and_exit_if_found(merged_rcf_root,
                                                     rule_group_name_xpath)
            merged_rcf_root.append(rule_group)


class RcfConfigMerger(XMLConfigMerger):
    """Defines a RCF configuration merger class"""

    _merged_filename = 'merged_coding_rules.rcf'

    _rcf_attributes = {"name": "generated_coding_rules", "version": "1.0"}

    def merge_contents(self, parsed_content: list):
        """Merges RCF files content"""

        merged_rcf_root = ET.Element('rcf', attrib=self._rcf_attributes)
        merged_rcf_root.text = "\n\t"
        merged_rcf_root.tail = "\n"

        _append_rcf_to_merged_rcf_root(merged_rcf_root, parsed_content)

        return merged_rcf_root
