"""
QAC Project analysis
"""
import os
from os.path import exists
from os import mkdir
import sys
import fnmatch

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxutils
from lucxbox.tools.qacw import prqa_installation

LOGGER = lucxlog.get_logger()


def sync_and_analyze(project_name, build_command, file_list, path_prqa, clean_build, output_path, output_format, inter_tu_dataflow,
                     suppress_h):
    """ The main function to analyze the prqa project. It checks the licenses,
    synchronizes the project - derive source files, Include paths and
    Definitions from an existing C or C++ project -, and finally analyzes the
    source code.

    :param build_command: The build command
    :param file_list: List of files to be analyzed
    :param path_prqa: The path to the PRQA executable
    :param project_name: The name of the project
    :param clean_build: If true, cleans all analysis data from the specified qaf-project before performing analysis.
    :param output_path: Path where the messages report shall be exported.
    :param output_format: Format the messages should be stored in.
    :param inter_tu_dataflow: Perform Inter TU Dataflow analysis.
    :param suppress_h: Ignore h include files in the qacpp analysis.
    """
    prqa = prqa_installation.PrqaInstallation(path_prqa)

    sync_build(prqa, project_name, build_command)

    # exclude h files from the analysis
    if suppress_h:
        qacw_suppress_h(project_name, prqa)

    analyze(prqa, project_name, file_list, clean_build, inter_tu_dataflow)
    if output_path is not None:
        export_messages(prqa, project_name, output_path, output_format)


def sync_build(prqa, project_name, build_command):
    """Sync the build command with the project.

    :param prqa: Information concerning the prqa installation
    :param project_name: The name of the prqa project
    :param build_command The build command
    """
    # Synchronize (Build)
    cmd_sync = ("{0} sync -t " +
                ("JSON" if build_command.lower().endswith(".json") else "MONITOR") +
                " -P {1} \"{2}\"").format(prqa.cli, project_name, build_command)

    LOGGER.info("Executing \"sync\" with \"%s\"", build_command)
    out, err, code = lucxutils.execute(cmd_sync)
    if code != 0:
        LOGGER.critical("Command '%s' exited with code %s", cmd_sync, code)
        LOGGER.critical("With error: '%s'", err)
        LOGGER.critical("with output: '%s'", out)
        sys.exit(-14)


def analyze(prqa, project_name, file_list, clean_build, inter_tu_dataflow):
    """
    Analyze the qac project.

    :param prqa: Information concerning the prqa installation
    :param project_name: The name of the prqa project
    :param file_list: List of files to be analyzed
    :param clean_build: If true, cleans all analysis data from the specified qaf-project before performing analysis.
    :param inter_tu_dataflow: Perform Inter TU Dataflow analysis.
    """
    # Analyze
    cmd_analyze = "{0} analyze -P {1} -f --force-complete".format(prqa.cli, project_name)

    if clean_build:
        cmd_analyze += " --clean"

    if inter_tu_dataflow:
        cmd_analyze += " --inter-tu-dataflow"

    # Analyze only the selected files and nothing else from the project
    if file_list:
        cmd_analyze += " --files " + file_list

    LOGGER.info("Executing \"analyze\"")
    out, err, code = lucxutils.execute(cmd_analyze)
    if code != 0:
        if code == 2:
            LOGGER.error("Command '%s' exited with code 2, 'Command Processing Failure'. Continuing.", cmd_analyze)
        elif code == 3:
            LOGGER.info("Command '%s' exited with code 3, 'Command Success, with some warnings'. Continuing.", cmd_analyze)
        elif code == 9:
            LOGGER.info("Command '%s' exited with code 9, 'Command Success, with some parsing errors'. Continuing.", cmd_analyze)
        else:
            LOGGER.critical("Command '%s' exited with code %s", cmd_analyze, code)
            LOGGER.critical("With error: '%s'", err)
            LOGGER.critical("with output: '%s'", out)
            sys.exit(-15)
    elif "Missing component" in out:
        LOGGER.error("Command '%s' exited with code 0 but there were missing components reported.\n"
                     "Please open the project in the QA GUI to see which components are missing, "
                     "because there could be essential ones among them!", cmd_analyze)
        LOGGER.error("with output: '%s'", out)


def export_messages(prqa, project_name, output_path, output_format):
    """
    Runs qacli view and returns the results.

    :param prqa: Information concerning the prqa installation
    :param project_name: Name of the PRQA project.
    :param output_path: Path where to store messages report output.
    :param output_format: Format the messages should be stored in.
    """
    if exists(output_path):
        LOGGER.critical('Output path already exists')
        sys.exit(-16)

    if output_format == 'xml':
        cmd = '{0} view --qaf-project "{1}" --medium XML -s -x all -o "{2}"'.format(prqa.cli, project_name, output_path)

        mkdir(output_path)
        out, err, code = lucxutils.execute(cmd, shell=True)
    else:
        cmd = '{0} view --qaf-project "{1}" --medium STDOUT --rules'.format(prqa.cli, project_name)

        with open(output_path, 'w') as output_file:
            out, err, code = lucxutils.execute(cmd, shell=True, stdout=output_file)

    if code != 0:
        if code == 2:
            LOGGER.error("Command '%s' exited with code 2, 'Command Processing Failure'. Continuing.", cmd)
        elif code == 3:
            LOGGER.info("Command '%s' exited with code 3, 'Command Success, with some warnings'. Continuing.", cmd)
        elif code == 9:
            LOGGER.info("Command '%s' exited with code 9, 'Command Success, with some parsing errors'. Continuing.", cmd)
        else:
            LOGGER.critical("Command '%s' exited with code %s", cmd, code)
            LOGGER.critical("With error: '%s'", err)
            LOGGER.critical("with output: '%s'", out)


def qacw_suppress_h(project_name, prqa):
    """
    Identify all .h files for c++ analysis suppression.

    :param project_name: Name of the PRQA project.
    :param prqa: Information concerning the prqa installation
    """

    dir_path = os.getcwd()
    h_files = get_h_files(dir_path)

    files = open("suppress_h.via", "w+")
    for h_header in h_files:
        files.write("-q " + h_header + "\n")
    files.close()

    LOGGER.info("Executing \"excluding h files\"")

    if "helix" in prqa.cli:
        qacpp_comp = 'qacpp-4.5.0'
    else:
        qacpp_comp = 'qacpp-4.3.0'

    cmd_exclude_h = '{0} pprops -P "{1}" -c {2} -O suppress_h.via --set-options'.format(prqa.cli, project_name, qacpp_comp)
    out, err, code = lucxutils.execute(cmd_exclude_h)

    if code != 0:
        if code == 3:
            LOGGER.error("Command '%s' exited with code 3, 'Skipping command. h files already available'. Continuing.", cmd_exclude_h)
        else:
            LOGGER.critical("Command '%s' exited with code %s", cmd_exclude_h, code)
            LOGGER.critical("With error: '%s'", err)
            LOGGER.critical("with output: '%s'", out)
            sys.exit(-16)


def get_h_files(directory_path):
    """
    Get a list with all h files

    :param directory_path: repo root.
    """
    h_files = []
    for dir_paths, _, filenames in os.walk(directory_path):
        for filename in fnmatch.filter(filenames, '*.h'):
            full_n = os.path.join(dir_paths, filename)
            full_d = os.path.dirname(os.path.abspath(full_n))
            hpp_found = False
            for files in os.listdir(full_d):
                if files.endswith('.hpp'):
                    hpp_found = True

            if not hpp_found:
                h_files.append(full_d)
                break

            h_files.append(full_n)
    return h_files
