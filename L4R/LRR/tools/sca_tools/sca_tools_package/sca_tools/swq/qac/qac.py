# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: qac.py
# ----------------------------------------------------------------------------

from os import path, makedirs
from shutil import copytree
from shutil import Error as shutilerror
from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t, \
    safe_delete_dirtree, check_if_project_exists
from swq.qac import qac_commands
from swq.qac.qac_utils import get_log_timestamp
from swq.qac.qac_version import QacVersion


def report(config, report_type, copy_to_reports: bool = True):
    """Generates native Helix QAC reports"""
    def _get_ignore_dependencies_flag():
        qac_version = QacVersion(config.cli_version_string)
        (major, minor) = qac_version.major_minor()
        return qac_version.is_helix() and major >= 2019 and minor >= 2

    def _get_parallel_flag():
        qac_version = QacVersion(config.cli_version_string)
        (major, _) = qac_version.major_minor()
        return qac_version.is_helix() and major >= 2020

    output_path = config.project_reports_path
    report_path = path.join(config.qac_project_path, "report")
    qac_commands.export_report(
        config,
        report_type,
        parallel=_get_parallel_flag(),
        ignore_dependencies=_get_ignore_dependencies_flag())
    if copy_to_reports:
        try:
            safe_delete_dirtree(report_path)
            copytree(output_path, report_path)
            LOGGER.info("Report folder copied to project root %s", report_path)
        except shutilerror as excp:
            LOGGER.error("Failed copying report folder: %s", excp)
    return report_path


def save_output(config, log_name, output):
    """Saves output log to a file"""
    save_build_path = path.join(config.helper_logs_path, "output")
    makedirs(save_build_path, exist_ok=True)
    output_log_file = path.join(save_build_path, log_name)
    LOGGER.info("Saving output log to file %s", output_log_file)
    with open_t(output_log_file, mode="w") as output_file:
        output_file.write(output)


def upload_to_qa_verify(config):
    """Uploads reports to QAVerify server"""
    LOGGER.info("### UPLOAD TO QAVERIFY ###")
    [output, return_value] = qac_commands.upload_qaf_project(config)
    save_output(config, "qavupload_output_{}.log".format(get_log_timestamp()),
                output)

    if return_value != 0:
        LOGGER.error("Dashboard \"qavupload\" failed with return code %s",
                     return_value)


def qac_report(config):
    """Entrypoint for QAC report"""
    check_if_project_exists(config.qac_project_path)
    report(config, 'RCR')


def qac_qavupload(config):
    """Entrypoint for QAC qavupload"""
    check_if_project_exists(config.qac_project_path)
    upload_to_qa_verify(config)


def qac_gui(config):
    """Entrypoint for QAC gui"""
    check_if_project_exists(config.qac_project_path)
    qac_commands.launch_gui(config)


def qac_s101gen(config):
    """Entrypoint for QAC s101gen"""
    check_if_project_exists(config.qac_project_path)
    qac_commands.s101_gen(config)
