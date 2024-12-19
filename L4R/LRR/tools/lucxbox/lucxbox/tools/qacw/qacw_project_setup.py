"""
QAC Project related functions
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxutils
from lucxbox.tools.qacw import prqa_installation

LOGGER = lucxlog.get_logger()


def setup_project(project_name, acf, cct_files, rcf, vcf, user_messages, file_filters, path_prqa, remap):
    """ The main function to create the prqa project.
    It gathers all input arguments and executes all underlying methods.

    :param project_name: The name of the project
    :param acf: The path to the acf configuration file
    :param cct_files: The path to the cct configuration file
    :param rcf: The path to the rcf configuration file
    :param vcf: The path to the vcf configuration file
    :param user_messages: The path to the user messages configuration file
    :param file_filters: List of file filters to be applied to the analysis
    :param path_prqa: The path to the PRQA executable
    :param remap: Option to map the c files as cpp for the analysis
    """
    prqa = prqa_installation.PrqaInstallation(path_prqa)

    # Clean project dir and generate anew
    if os.path.exists(project_name):
        os.rmdir(project_name)
    os.mkdir(project_name)

    # Create prqa project
    create_qaf_project(acf, cct_files, project_name, prqa, rcf, user_messages, vcf)

    # Set source root
    set_qaf_source_root(project_name, prqa)

    # remap target extensions
    if remap:
        remap_qaf_target_extensions(prqa, project_name)

    # List all config files and source extensions
    display_qaf_information(project_name, prqa)

    # Set file filters and list analyzers
    set_qaf_file_filters(prqa, project_name, file_filters)
    list_qaf_analyzers(prqa, project_name)


def create_qaf_project(acf, cct_files, project_name, prqa, rcf, user_messages, vcf):
    """ Create the QAF project folder based on the provided configuration files

    :param acf: The path to the acf configuration file
    :param cct_files: The path to the cct configuration file
    :param rcf: The path to the rcf configuration file
    :param project_name:  The name of the QAC project
    :param prqa: Information concerning the prqa installation
    :param user_messages: The path to the user messages configuration file
    :param vcf: The path to the vcf configuration file
    """
    cmd_create = prqa.cli + ' admin --qaf-project-config --qaf-project ' + project_name
    for cct in cct_files:
        cmd_create += ' --cct ' + cct
    cmd_create += ' --acf ' + acf
    cmd_create += ' --rcf ' + rcf
    if vcf:
        cmd_create += ' --vcf ' + vcf
    if user_messages:
        cmd_create += ' --user-messages ' + user_messages

    out, err, code = lucxutils.execute(cmd_create)
    if code != 0:
        LOGGER.critical("Command '%s' exited with code %s", cmd_create, code)
        LOGGER.critical("With error: '%s'", err)
        LOGGER.critical("with output: '%s'", out)
        sys.exit(-13.1)


def set_qaf_source_root(project_name, prqa):
    """ Set the QAF project source root

    :param project_name:  The name of the QAC project
    :param prqa: Information concerning the prqa installation
    """
    cmd_set_src_root = '{0} admin --qaf-project {1} --set-source-code-root {2}'.format(prqa.cli, project_name, os.getcwd())

    _, _, code = lucxutils.execute(cmd_set_src_root)
    if code != 0:
        LOGGER.critical("Command '%s' exited with code %s", cmd_set_src_root, code)
        sys.exit(-13.2)


def remap_qaf_target_extensions(prqa, project_name):
    """ Remap C Target extensions to CPP as C coding rule config is not yet available from EPG.
    Otherwise C files cannot be analyzed

    :param prqa: Information concerning the prqa installation
    :param project_name:  The name of the QAC project
    """
    cmd_lang_c_lowercase = "{0} admin --qaf-project {1} --target-language C --remove-source-extension .c".format(prqa.cli, project_name)
    cmd_lang_c_uppercase = "{0} admin --qaf-project {1} --target-language C --remove-source-extension .C".format(prqa.cli, project_name)
    cmd_lang_cpp_lowercase = "{0} admin --qaf-project {1} --target-language C++ --add-source-extension .c".format(prqa.cli, project_name)
    cmd_lang_cpp_uppercase = "{0} admin --qaf-project {1} --target-language C++ --add-source-extension .C".format(prqa.cli, project_name)

    for cmd in [cmd_lang_c_lowercase, cmd_lang_c_uppercase, cmd_lang_cpp_lowercase, cmd_lang_cpp_uppercase]:
        _, _, code = lucxutils.execute(cmd)
        if code != 0:
            LOGGER.critical("One of the qac admin commands  exited with code %s", code)
            sys.exit(-13.3)


def display_qaf_information(project_name, prqa):
    """ Display QAF relevant information such as config files and source extensions.

    :param project_name:  The name of the QAC project
    :param prqa: Information concerning the prqa installation
    """
    cmd_list_config_files = "{0} admin --qaf-project {1} --list-config-files".format(prqa.cli, project_name)
    cmd_list_source_extensions_c = "{0} admin --list-source-extensions --qaf-project {1} -T C".format(prqa.cli, project_name)
    cmd_list_source_extensions_cpp = "{0} admin --list-source-extensions --qaf-project {1} -T C++".format(prqa.cli, project_name)

    for cmd in [cmd_list_config_files, cmd_list_source_extensions_c, cmd_list_source_extensions_cpp]:
        _, _, code = lucxutils.execute(cmd)
        if code != 0:
            LOGGER.critical("One of the qac admin commands  exited with code %s", code)
            sys.exit(-13.4)


def set_qaf_file_filters(prqa, project_name, file_filters):
    """
    Executes a command that syncs the file filter settings

    :param prqa: Information concerning the prqa installation
    :param project_name: The name of the prqa project
    :param file_filters: List of file filters to be applied to the analysis
    """
    # Set file filter
    filters = []

    if os.name == 'nt':
        filters.append('C:/tools/')

    filters.extend(file_filters)

    for current_filter in filters:
        cmd_file_filter = "{0} pprops --qaf-project {1} --sync-setting FILE_FILTER --set {2}".format(prqa.cli, project_name, current_filter)
        LOGGER.info("Adding file filter: %s", current_filter)
        _, _, code = lucxutils.execute(cmd_file_filter)
        if code != 0:
            LOGGER.critical("Command '%s' exited with code %s", cmd_file_filter, code)
            sys.exit(-13.5)


def list_qaf_analyzers(prqa, project_name):
    """
    Function lists the analyzers

    :param prqa: Information concerning the prqa installation
    :param project_name: The name of the prqa project
    """
    # List out the used analyzers in the project
    cmd_analyzers = "{0} pprops --list-components --qaf-project {1}".format(prqa.cli, project_name)
    _, _, code = lucxutils.execute(cmd_analyzers)
    if code != 0:
        LOGGER.critical("Command '%s' exited with code %s", cmd_analyzers, code)
        sys.exit(-13.6)
