# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: constants.py
# ----------------------------------------------------------------------------
""" Constants for behave tests in sca_tools_package """
from swq.qac.exporters.state_exporter import qac_export_state, qac_state
from swq.qac.fix_cl_json import fix_cl_json_entrypoint
from swq.qac.qac import qac_report, \
    qac_qavupload, qac_gui, qac_s101gen
from swq.qac.create import qac_create
from swq.qac.qac_analyze import qac_analyze
from swq.qac.export_analysis import qac_export_analysis
from swq.qac.filter_qaview import filter_qaview_entrypoint
from swq.find_includes.find_includes import find_includes_entrypoint
from swq.coverity.coverity import coverity_create, \
    coverity_show_build_log_metrics, coverity_analyze, \
    coverity_export, coverity_preview_report, coverity_upload, \
    coverity_webapi_export
from swq.coverity.filter_preview_report import coverity_filter_report
from swq.coverity.export_analysis import coverity_export_analysis
from swq.map_teams.map_teams import map_teams
from swq.unify_reports.unify_reports import unify_reports
from swq.common.constants import IS_WINDOWS

FEATURES_QAC = {
    'create_config':
    '01_qac_create_config.feature',
    'full_analysis':
    '02_qac_full_analysis.feature',
    'delta_analysis':
    '03_qac_delta_analysis.feature',
    'compile_commands_full_analysis':
    '04_qac_full_compile_commands_anaylsis.feature'
}

FEATURES_COVERITY = {
    'create_config':
    '01_coverity_create_config.feature',
    'full_analysis':
    '02_coverity_full_analysis.feature',
    'delta_analysis':
    '03_coverity_delta_analysis.feature',
    'compile_commands_full_analysis':
    '04_coverity_full_compile_commands_anaylsis.feature'
}

MOCK_ENTRYPOINTS = {
    'coverity_create': coverity_create,
    'coverity_check_buildlog': coverity_show_build_log_metrics,
    'coverity_analyze': coverity_analyze,
    'coverity_export': coverity_export,
    'coverity_export_analysis': coverity_export_analysis,
    'coverity_preview_report': coverity_preview_report,
    'coverity_upload': coverity_upload,
    'coverity_webapi_export': coverity_webapi_export,
    'coverity_filter_report': coverity_filter_report,
    'find_includes': find_includes_entrypoint,
    'map_teams': map_teams,
    'unify_reports': unify_reports,
    'qac_create': qac_create,
    'qac_analyze': qac_analyze,
    'qac_report': qac_report,
    'qac_qavupload': qac_qavupload,
    'qac_gui': qac_gui,
    'qac_s101gen': qac_s101gen,
    'qac_state': qac_state,
    'qac_qaview': qac_export_state,
    'qac_fix_cl_json': fix_cl_json_entrypoint,
    'qac_filter_qaview': filter_qaview_entrypoint,
    'qac_export_analysis': qac_export_analysis
}

TABLE_PROVIDED_MESSAGE = 'ERROR: table is not provided'
BEHAVE_FOLDER_NAME = 'test/integration'
PARAMETER_VALUE_SEPARATOR = ','
OS_FOLDER = 'windows' if IS_WINDOWS else 'linux'
