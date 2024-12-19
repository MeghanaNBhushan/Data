# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	custom_help.py
# ----------------------------------------------------------------------------
"""Defines methods to interact with custom help"""

from os import path
from xml.dom import minidom
from swq.common.filesystem.filesystem_utils import open_t
from swq.common.logger import LOGGER
from xml.etree.ElementTree import parse as etree_parse
from swq.qac.constants import HELP_PAGES_CUSTOM_DIR, \
    HELP_PAGES_ORIGINAL_DIR, RULE_GROUP_DIR
from swq.qac.qac_utils import get_qac_installed_component_path


def set_help_path_in_rcf(rcf_filepath, help_pages_root_dir):
    """Sets help page path in rcf configuration file"""
    xml_tree = etree_parse(rcf_filepath)
    xml_root = xml_tree.getroot()

    for element in xml_root.iter():
        if element.tag == 'rule':
            _set_help_page_for_rule(element, help_pages_root_dir)

    xml_tree.write(rcf_filepath,
                   encoding='utf-8', xml_declaration=True)


def set_help_path_in_user_messages(user_messages_filepath,
                                   help_pages_root_dir):
    """Sets help page path in user messages configuration file"""
    xml_tree = etree_parse(user_messages_filepath)
    xml_root = xml_tree.getroot()

    for component_messages in xml_root.iter('messages'):
        _set_help_pages_for_component(component_messages,
                                      help_pages_root_dir)

    xml_tree.write(user_messages_filepath,
                   encoding='utf-8', xml_declaration=True)


def set_bosch_custom_help(in_filepath, custom_help_path):
    """Checks and enables Bosch Custom Help
    if configuration files support the feature"""

    if custom_help_path:
        out_filepath = in_filepath
        help_keyword = "__bosch_help__"
        LOGGER.info('Setting bosch custom help token in %s', in_filepath)

        replace_token_in_file(help_keyword, custom_help_path,
                              in_filepath, out_filepath)


def set_builtin_qac_help(in_filepath, qac_home_path):
    """Use Helix QAC Help pages from the local QAC installation
    if configuration files support the feature"""
    qa_help_keyword = "__qa_help__"
    out_filepath = in_filepath

    LOGGER.debug('Setting %s path in %s', qa_help_keyword, in_filepath)

    replace_token_in_file(qa_help_keyword, qac_home_path,
                          in_filepath, out_filepath)


def _set_help_pages_for_component(component_messages, root_dir):
    component_name = component_messages.attrib['component']
    for message in component_messages.iter('message'):
        message_id = message.attrib['id']
        help_page_path = _locate_user_messages_help_page(
            root_dir, component_name, message_id)
        if help_page_path is None:
            continue
        message.attrib['help'] = help_page_path


def _set_help_page_for_rule(rule, root_dir):
    rule_id = rule.attrib['id']
    help_page_path = _locate_rcf_help_page(rule_id, root_dir)
    if help_page_path:
        LOGGER.debug('Setting help page for the rule: %s', rule_id)
        rule.attrib['help'] = help_page_path


def _locate_user_messages_help_page(root_dir, component_name, message_id):
    custom_help_page = path.join(root_dir, HELP_PAGES_CUSTOM_DIR,
                                 component_name, '{}.html'.format(message_id))
    if path.exists(custom_help_page):
        return custom_help_page

    original_help_page = path.join(root_dir, HELP_PAGES_ORIGINAL_DIR,
                                   component_name,
                                   '{}.html'.format(message_id))

    if path.exists(original_help_page):
        return original_help_page

    LOGGER.debug('Help page is not found for the component:message: %s:%s',
                 component_name, message_id)
    return None


def _locate_rcf_help_page(rule_id, root_dir):
    custom_help_page = path.join(root_dir, HELP_PAGES_CUSTOM_DIR,
                                 RULE_GROUP_DIR, '{}.html'.format(rule_id))
    if path.exists(custom_help_page):
        return custom_help_page
    LOGGER.debug('Help page is not found for the rule: %s', rule_id)

    return None


def set_component_path_in_xml(user_messages_filepath: str, qac_home_path):
    """Checks and replaces components paths in user messages XML"""
    help_keyword = '__component_path__'

    with open_t(user_messages_filepath) as xml_in_file:
        xml_in_content = xml_in_file.read()
        if help_keyword not in xml_in_content:
            LOGGER.debug(
                'Not creating a new messages file due to absence of %s',
                help_keyword)
            return

        LOGGER.debug('Setting custom cpp help token in %s',
                     user_messages_filepath)
        dom_tree = minidom.parseString(xml_in_content)
        messages = dom_tree.getElementsByTagName('messages')
        for message in messages:
            component_name = message.getAttribute('component')
            component_filepath = get_qac_installed_component_path(
                qac_home_path, component_name, check_version=False)
            if component_filepath is not None:
                for component_message in message.getElementsByTagName(
                        'message'):
                    help_attribute = component_message.getAttribute('help')

                    if help_keyword in help_attribute:
                        component_message.setAttribute(
                            'help',
                            help_attribute.replace(help_keyword,
                                                   component_filepath))
            else:
                LOGGER.error('Component %s was not found', component_name)
        with open_t(user_messages_filepath, mode="w+") as output_file:
            xml_content = dom_tree.toprettyxml(newl='')
            output_file.write(xml_content)


def replace_token_in_file(token,
                          replace_value,
                          in_filepath,
                          out_filepath=None):
    """Replaces the token in the specified file with the specified value and
    returns new filepath. If the token is not used in the specified file then
    it returns original filename. If output filepath is not specified will
    overwrite and replace token in input file"""
    LOGGER.debug('Input filename: %s', in_filepath)
    LOGGER.debug('Looking for token: %s', token)

    if not out_filepath:
        out_filepath = in_filepath

    with open_t(in_filepath) as fin:
        fin_content = fin.read()
        if token not in fin_content:
            LOGGER.debug('Token %s was not found in %s', token, in_filepath)
            return

    with open_t(out_filepath, mode="wt") as fout:
        LOGGER.debug('Replacing token %s with %s', token, replace_value)
        modified_content = fin_content.replace(token, replace_value)
        fout.write(modified_content)
        LOGGER.debug('Output file: %s', out_filepath)
