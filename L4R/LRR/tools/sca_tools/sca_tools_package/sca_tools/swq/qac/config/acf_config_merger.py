# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: acf_config_merger.py
# ----------------------------------------------------------------------------
"""Defines an Analysis Configuration File (ACF) merger"""

import xml.etree.ElementTree as ET

from swq.qac.config.xml_config_merger import XMLConfigMerger


def _merge_components(xml_root, merged_acf_root):
    for components in xml_root.iter('components'):
        components_xpath = 'components'
        if merged_acf_root.findall(components_xpath):
            merged_components = merged_acf_root.find(components_xpath)
            for component in components.iter('component'):
                name = component.attrib['name']
                version = component.attrib['version']
                xpath_attribs = f'[@name=\'{name}\'][@version=\'{version}\']'
                component_xpath = f'component{xpath_attribs}'
                if not merged_components.findall(component_xpath):
                    merged_components.append(component)
        else:
            merged_acf_root.append(xml_root.find('components'))


def _merge_component_settings(xml_root, merged_acf_root):
    for component_settings in xml_root.iter('component_settings'):
        component_settings_xpath = 'component_settings'
        if merged_acf_root.find(component_settings_xpath) is not None:
            for input_to in component_settings.iter('input_to'):
                component = input_to.attrib['component']
                tag_xpath = 'component_settings/input_to'
                component_xpath = f'{tag_xpath}[@component=\'{component}\']'
                component_node = merged_acf_root.find(component_xpath)
                if component_node is not None:
                    for option in input_to.iter('option'):
                        component_node.append(option)
                else:
                    merged_acf_root.find(component_settings_xpath).append(
                        input_to)
        else:
            merged_acf_root.append(component_settings)


def _append_acf_to_merged_acf_root(merged_acf_root, parsed_content):
    """Append rcf rulegroups to merged rcf file"""
    for xml_root in parsed_content:
        _merge_components(xml_root, merged_acf_root)
        _merge_component_settings(xml_root, merged_acf_root)


class AcfConfigMerger(XMLConfigMerger):
    """Defines a ACF configurations merger class"""

    _merged_filename = 'merged_analysis_configs.acf'
    __acf_attributes = {"xmlversion": "2.0.0"}

    def merge_contents(self, parsed_content: list):
        """Merges RCF files content"""

        merged_acf_root = ET.Element('acf', attrib=self.__acf_attributes)
        merged_acf_root.text = "\n\t"
        merged_acf_root.tail = "\n"

        _append_acf_to_merged_acf_root(merged_acf_root, parsed_content)

        return merged_acf_root
