# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	license_checker.py
# ----------------------------------------------------------------------------
"""Defines a license checker implementation"""

from os import path

from swq.common.filesystem.filesystem_utils import open_t
from swq.common.logger import LOGGER
from swq.qac.qac_commands import set_license_server, \
    list_license_server, check_license_server

from swq.common.return_codes import \
    check_return_code_for_cmd_and_exit_if_failed


def _transform_license_string(license_string):
    """
    transforms a license string like 5065@rb-lic-rlm-prqa2.de.bosch.com
    into port="5065" host="rb-lic-rlm-prqa2.de.bosch.com"
    """
    license_url = license_string.split('@')[1]
    license_port = license_string.split('@')[0]
    xml_search_string = 'port="{}" host="{}"'.format(license_port, license_url)
    return xml_search_string


def _license_already_set_in_global_config_xml(project_xml_path,
                                              license_string):
    """  checks if a PRQA xml exists and if its contains a licensestring
    """
    if path.exists(project_xml_path):
        LOGGER.debug(
            "_license_already_set_in_global_config_xml project exists")
        with open_t(project_xml_path) as xml_file:
            project_xml_file_content = xml_file.read()
            return _transform_license_string(
                license_string) in project_xml_file_content
    return False


def validate_license_settings(config):
    LOGGER.info("### VALIDATING LICENSE CONFIGURATION ###")
    for license_string in config.license_servers:
        if not _license_already_set_in_global_config_xml(
                config.helix_config_project_xml_path, license_string):
            LOGGER.info("license {} missing in {}".format(
                license_string, config.helix_config_project_xml_path))
            set_license_server(config, license_string)
        else:
            LOGGER.info("license {} already set in {}".format(
                license_string, config.helix_config_project_xml_path))
    if config.verbose:
        LOGGER.info("### LISTING SERVERS ###")
        [_, return_value] = list_license_server(config)
        check_return_code_for_cmd_and_exit_if_failed(return_value)

        LOGGER.info("### CHECKING LICENSE ###")
        [_, return_value] = check_license_server(config)
        check_return_code_for_cmd_and_exit_if_failed(return_value)


def ensure_license_servers_configured(config):
    LOGGER.info('Validating license configuration')
    for license_string in config.license_servers:
        if not _license_already_set_in_global_config_xml(
                config.helix_config_project_xml_path, license_string):
            LOGGER.info('License server {} is missing '
                        'in {} configuration file'.format(
                            license_string,
                            config.helix_config_project_xml_path))
            set_license_server(config, license_string)
        else:
            LOGGER.info('License server {} already set '
                        'in {} configuration file'.format(
                            license_string,
                            config.helix_config_project_xml_path))
    if config.verbose:
        LOGGER.info('Listing license servers')
        [_, return_value] = list_license_server(config)
        check_return_code_for_cmd_and_exit_if_failed(return_value)

        LOGGER.info('Checking license servers')
        [_, return_value] = check_license_server(config)
        check_return_code_for_cmd_and_exit_if_failed(return_value)
