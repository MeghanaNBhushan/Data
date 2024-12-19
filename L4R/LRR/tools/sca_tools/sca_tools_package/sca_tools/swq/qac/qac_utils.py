# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: qac_utils.py
# ----------------------------------------------------------------------------
"""Defines qac utils"""
from os import path
from datetime import datetime
from glob import glob
from xml.etree.ElementTree import parse as etree_parse
from swq.common.filesystem.filesystem_utils import open_t
from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, RC_SUCCESS, \
    RC_QAC_CONFIGURATION_INCONSISTENT, RC_QAC_MODULES_VERSION_MISMATCH
from swq.common.file.file_utils import \
    get_list_of_files_from_compile_commands, \
    get_list_of_files_from_file
from swq.qac import qac_commands
from swq.qac.qac_version import QacVersion


def _get_component_name(component):
    return component.rsplit('-')[0]


def _get_component_version(component):
    return component.rsplit('-')[1]


def has_summary_export(config):
    """Checks if QAC version supports summraty export"""
    qac_version = QacVersion(config.cli_version_string)
    (major, minor) = qac_version.major_minor()

    return qac_version.is_helix() and (major > 2019 or minor >= 2)


def resolve_filepath_list_from_path_or_pattern(filepath):
    """Resolves wildcards in a given file path and returns
    a list of all matching files"""
    if '*' in filepath:
        return glob(filepath, recursive=True)
    return [filepath]


def get_files_from_analyze_list(config):
    """Gets files from analyze list and makes filepaths absolute"""
    absolute_paths = [
        config.get_absolute_path_or_relative_to_project_root(filepath).replace(
            '\\', '/').strip()
        for filepath in get_list_of_files_from_file(config.analyze_list)
    ]
    return [
        f.replace('\\', '/').strip() for filepath in absolute_paths
        for f in resolve_filepath_list_from_path_or_pattern(filepath)
    ]


def get_relevant_files_for_analysis_and_exit_if_none(config):
    """Gets files from analyze list and that are present
    in compile_commands.json"""
    files_list = get_files_from_analyze_list(config)
    files_in_project = get_list_of_files_from_compile_commands(
        config.actual_sync_json)
    LOGGER.info("Filtering out the files not existing in QAC Project "
                "from the analyze list")
    relevant_files = set(files_in_project).intersection(set(files_list))
    irrelevant_files = set(files_list).difference(set(relevant_files))
    if not relevant_files:
        LOGGER.info("None of the files from {} exist "
                    "in QAC project".format(config.analyze_list))
        log_and_exit(RC_SUCCESS)
    if irrelevant_files:
        LOGGER.warning(
            "Files that are in analyze list and do not exist "
            "in the QAC project:\n%s", "\n".join(irrelevant_files))
    else:
        LOGGER.info("All files exist in QAC Project. No filtering needed")
    return relevant_files


def get_log_timestamp():
    """Returns timestamp"""
    return datetime.today().strftime('%Y%m%d_%H%M%S.%f')[:-3]


def get_qac_installed_component_path(qac_home_path,
                                     component_name,
                                     check_version=True):
    """Searchs and returns QAC component path if such exists.
    Search can be done with exact component version or with name only"""
    def get_component_path_if_exists_or_none(component_path, target_component):
        component_name = path.basename(component_path).lower()
        if not check_version:
            component_name = _get_component_name(component_name)

        return target_component.lower() == component_name

    qac_components_path = path.normpath(path.join(qac_home_path, 'components'))

    for component_filepath in glob('{}/**'.format(qac_components_path)):
        if get_component_path_if_exists_or_none(component_filepath,
                                                component_name):

            return component_filepath

    return None


def get_components_from_acf_file(acf_filepath):
    """Returns list of components from ACF file"""
    xml_tree = etree_parse(acf_filepath)
    xml_root = xml_tree.getroot()
    components = xml_root.find('components')

    return [
        "{}-{}".format(component.attrib['name'], component.attrib['version'])
        for component in components.findall('component')
        if component.attrib['name'] and component.attrib['version']
    ]


def check_if_component_version_matches_and_exit_otherwise(
        first_component, second_component):
    """Checks if provided component version matches and exit
    if not with RC_QAC_MODULES_VERSION_MISMATCH code"""

    if _get_component_version(first_component) != \
        _get_component_version(second_component):
        LOGGER.error(
            "Component version specified in ACF and available "
            "in components folder are different. "
            "Please check %s component's version",
            _get_component_name(first_component))
        log_and_exit(RC_QAC_MODULES_VERSION_MISMATCH)


def verify_components_compatibility(config):
    """Checks components defined in ACF and QAC_MODULES"""
    components_from_acf = get_components_from_acf_file(
        config.acf_file.get_result_filepath())

    for component in config.qac_modules:
        if component not in components_from_acf:
            LOGGER.error("QAC component %s is not present in ACF file",
                         component)
            log_and_exit(RC_QAC_CONFIGURATION_INCONSISTENT)

    for component in components_from_acf:
        component_name = _get_component_name(component)
        qac_installed_component_path = get_qac_installed_component_path(
            config.qac_home_path, component_name, check_version=False)

        if not qac_installed_component_path:
            LOGGER.warning("Component %s cannot be found in components path",
                           component)
            continue

        qac_installed_component = path.basename(qac_installed_component_path)
        check_if_component_version_matches_and_exit_otherwise(
            component, qac_installed_component)


def get_module_toolchain(config, module):
    """Returns module toolchain specified in 'target' field
    by its name and version"""
    def _get_qacli_supported_toolchain(target):
        if target == 'C_CPP':
            return 'C/C++'
        return target

    xml_tree = etree_parse(config.acf_file.get_result_filepath())
    xml_root = xml_tree.getroot()
    components = xml_root.find('components')
    module_name = module.split('-')[0]
    module_version = module.split('-')[1]

    for component in components.findall('component'):
        if component.attrib['name'] == module_name and \
            component.attrib['version'] == module_version:
            return _get_qacli_supported_toolchain(component.attrib['target'])

    return None


def check_if_return_code_in_skip_list(config, return_code, message, exit_code):
    """Checks if return_code is in skip_exit_on_build_return_codes and
    exit otherwise"""
    parameter_name = \
        config.get_parameter_name('SKIP_EXIT_ON_BUILD_RETURN_CODES')
    if return_code != 0:
        if return_code not in config.skip_exit_on_build_return_codes:
            LOGGER.error(
                '%s. Return code %s is not in %s list', message, return_code,
                parameter_name)
            log_and_exit(exit_code)
        else:
            LOGGER.info(
                'Return code %s is in %s list', return_code, parameter_name)


def optimize_helix_project(config):
    """
    Starting with QAC2019.1 an "optimize" flag was introduced to remove
    duplicates in the project.xml. This increases the performance in
    projects with a lot of files in it. Currently we pass this flag for json
    and buildlogs directly, but for monitor builds we need this workaround.
    """
    LOGGER.info('%s is set to %s',
                config.get_parameter_name('QAC_DISABLE_OPTIMIZATION'),
                config.disable_optimization)

    if not config.disable_optimization and QacVersion(
            config.cli_version_string).is_helix():

        LOGGER.info('Deduplicating dependencies in prqaproject.xml')

        optimization_workaround_path = path.join(config.custom_config_path,
                                                 'helix_optimization.txt')
        with open_t(optimization_workaround_path,
                    mode="w") as optimization_workaround_file:
            # \n is placed to indicate EOL (End of Line)
            optimization_workaround_file.write(
                "helix_optimization_workaround_file.cpp\n")
        qac_commands.delete_file_to_optimize_project(
            config, optimization_workaround_path)
        LOGGER.info('Project optimization done. '
                    'Non-zero exit status 2 is okay')
    else:
        LOGGER.info('Skipping project optimization')
