# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: utils.py
# ----------------------------------------------------------------------------
"""Utils for interacting with state.json"""

from os import makedirs, path

from json import dumps
from zipfile import ZipFile, ZIP_DEFLATED

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import check_if_project_exists, \
    safe_delete_dirtree, check_if_file_exist_and_exit_if_not, open_t
from swq.qac import qac_utils, qac_commands
from swq.qac.qac import report
from swq.qac.create import remove_qac_export_directories, \
    ensure_qac_exports_directory_tree_created
from swq.qac.state.report.constants import SUBDIAGNOSTICS_DEPTH_COLUMN_NAME
from swq.qac.project_state import ProjectState


def _cleanup_diagnostics(diagnostics_path):
    LOGGER.info("Cleaning up diagnostics output")
    safe_delete_dirtree(diagnostics_path)
    makedirs(diagnostics_path, exist_ok=True)


def create_state_file(config, generate_state=False):
    """Creates state file"""
    check_if_project_exists(config.qac_project_path)

    remove_qac_export_directories(config)
    ensure_qac_exports_directory_tree_created(config)

    if config.with_metrics:
        report(config, 'HMR', copy_to_reports=False)

    if qac_utils.has_summary_export(config):
        qac_commands.export_project_summary(config)

    _generate_state = config.with_state_file or generate_state

    if _generate_state:
        project_state = ProjectState(config).create()
        dumped_project_state = dumps(project_state)
        with ZipFile(config.state_filepath, 'w',
                     compression=ZIP_DEFLATED) as state_file:
            state_file.writestr('state.json', dumped_project_state)
            LOGGER.info(
                'Created successfully a state dump of '
                'the project at %s', config.state_filepath)

        if config.qac_cleanup_diagnostic_output:
            _cleanup_diagnostics(config.project_diagnostics_path)

        return dumped_project_state


def read_state(state_filepath):
    """Reads state file"""
    check_if_file_exist_and_exit_if_not(state_filepath)
    LOGGER.debug('Reading state file from %s', state_filepath)

    state = {}
    _, state_extension = path.splitext(state_filepath)

    if state_extension == '.zip':
        with ZipFile(state_filepath) as state_zip_file:
            with state_zip_file.open('state.json') as state_file:
                state = state_file.read()

    if state_extension == '.json':
        with open_t(state_filepath) as state_file:
            state = state_file.read()

    return state


def filter_out_subdiagnostics_if_present(analysis_report):
    """Filters out subdiagnostics from analysis report if present"""
    if SUBDIAGNOSTICS_DEPTH_COLUMN_NAME in analysis_report.columns:
        analysis_report.query(f'`{SUBDIAGNOSTICS_DEPTH_COLUMN_NAME}` == 0',
                              inplace=True)
