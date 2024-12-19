"""
QAC Project report
"""

import os
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxutils
from lucxbox.tools.qacw import prqa_installation

LOGGER = lucxlog.get_logger()


def report(project_name, report_types, file_list, archive_target_dir, path_prqa):
    """ The main function to create, archive, and upload reports.
    It gathers all input arguments and executes all underlying methods.

    :param project_name: The name of the project
    :param report_types: List of report type to generate
    :param archive_target_dir: The path where the report shall be archived
    :param path_prqa: The path to the PRQA executable
    """
    create_reports(project_name, report_types, file_list, path_prqa)

    archive_src_dir = project_name + "/prqa/configs/Initial"
    archive_report(archive_src_dir, archive_target_dir)


def create_reports(project_name, report_types, file_list, path_prqa):
    """ Generate different report types

    :param project_name: The name of the project
    :param report_types: 'CRR', 'HMR', 'MDR', 'RCR', 'SSR', 'SUR'
    :param path_prqa: The path to the PRQA executable
    """
    prqa = prqa_installation.PrqaInstallation(path_prqa)

    for idx, report_type in enumerate(report_types):
        LOGGER.info("Creating report %s of %s - %s", idx + 1, str(len(report_types)), report_type)
        cmd_report = "{0} report -P {1} -t {2}".format(prqa.cli, project_name, report_type)

        # Create report only for selected files, while ignoring unanalyzed dependencies
        if file_list:
            cmd_report += " --files " + file_list + " --ignore"

        out, err, code = lucxutils.execute(cmd_report)
        if code != 0:
            LOGGER.critical("Command '%s' exited with code %s", cmd_report, code)
            LOGGER.critical("With error: '%s'", err)
            LOGGER.critical("with output: '%s'", out)
            sys.exit(-16.1)


def archive_report(archive_src_dir, archive_target_dir):
    """ Zip and archive the project to a location defined in the command parameters.

    :param archive_src_dir: The path to the prior created report
    :param archive_target_dir: The path where the report shall be archived
    """
    if archive_target_dir:
        LOGGER.info("Archiving the report to %s", archive_target_dir)
        if not os.path.exists(archive_target_dir):
            os.makedirs(archive_target_dir)

        base_name = archive_target_dir + "/reports"
        try:
            shutil.make_archive(base_name=base_name, root_dir=archive_src_dir, format="zip")
        except ValueError as value_error:
            LOGGER.critical("Archiving of report failed with message %s", str(value_error.message))
            sys.exit(-16.2)
