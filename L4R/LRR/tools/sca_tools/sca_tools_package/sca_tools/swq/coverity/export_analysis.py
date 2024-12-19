# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: export_analysis.py
# ----------------------------------------------------------------------------
"""Generates project state based on analysis results and generates reports"""
from os import path
from zipfile import ZipFile, ZIP_DEFLATED
from json import dumps

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import safe_delete_dirtree
from swq.coverity.project_state import ProjectState


def _cleanup_exports(config):
    safe_delete_dirtree(path.dirname(config.cov_errors_json_filepath))
    if config.with_cid:
        safe_delete_dirtree(path.dirname(config.preview_report_json_filepath))


def coverity_export_analysis(config):
    """Entrypoint for export_analysis command"""
    project_state = ProjectState(config).create()
    with ZipFile(config.state_filepath, 'w',
                 compression=ZIP_DEFLATED) as state_file:
        state_file.writestr('state.json', dumps(project_state))
        LOGGER.info('Created successfully a state dump of the project at %s',
                    config.state_filepath)
    _cleanup_exports(config)
