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
"""Defines constants for report module"""

FILENAME_COLUMN_NAME = 'Filename'
LINE_NUMBER_COLUMN_NAME = 'Line number'
COLUMN_NUMBER_COLUMN_NAME = 'Column number'
PRODUCER_COLUMN_NAME = 'Producer component:Message number'
MSG_TEXT_COLUMN_NAME = 'Message text'
SEVERITY_COLUMN_NAME = 'Severity'
SUPPRESSION_BITMASK_COLUMN_NAME = 'Suppression type bitmask'
SUPPRESSION_JUSTIFICATION_COLUMN_NAME = 'Suppression justification'
RULE_GROUP_COLUMN_NAME = 'Rule Group'
RULE_TEXT_COLUMN_NAME = 'Rule Text'
SUBDIAGNOSTICS_ID_COLUMN_NAME = 'SCA Tools Subdiagnostics ID'
SUBDIAGNOSTICS_ORIGIN_COLUMN_NAME = 'SCA Tools Subdiagnostics Origin'
SUBDIAGNOSTICS_DEPTH_COLUMN_NAME = 'SCA Tools Subdiagnostics Depth'

ANALYSIS_REPORT_COLUMNS = [
    FILENAME_COLUMN_NAME, LINE_NUMBER_COLUMN_NAME, COLUMN_NUMBER_COLUMN_NAME,
    PRODUCER_COLUMN_NAME, MSG_TEXT_COLUMN_NAME, SEVERITY_COLUMN_NAME,
    SUPPRESSION_BITMASK_COLUMN_NAME, SUPPRESSION_JUSTIFICATION_COLUMN_NAME,
    RULE_GROUP_COLUMN_NAME, RULE_TEXT_COLUMN_NAME
]

PATH_COLUMN_NAME = 'path'
ENTITY_NAME_COLUMN_NAME = 'entity_name'
ENTITY_LINE_COLUMN_NAME = 'entity_line'
ENTITY_TYPE_COLUMN_NAME = 'entity_type'
METRIC_NAME_COLUMN_NAME = 'metric_name'
METRIC_VALUE_COLUMN_NAME = 'metric_value'

METRICS_REPORT_COLUMNS = [
    PATH_COLUMN_NAME, ENTITY_NAME_COLUMN_NAME, ENTITY_LINE_COLUMN_NAME,
    ENTITY_TYPE_COLUMN_NAME, METRIC_NAME_COLUMN_NAME, METRIC_VALUE_COLUMN_NAME
]

SUMMARY_REPORT_COLUMNS = ['Name/Description', 'Count']

SUBDIAGNOSTICS_LIGHT_COLUMNS = [
    SUBDIAGNOSTICS_ID_COLUMN_NAME, SUBDIAGNOSTICS_ORIGIN_COLUMN_NAME
]
SUBDIAGNOSTICS_FULL_COLUMNS = [
    SUBDIAGNOSTICS_ID_COLUMN_NAME, SUBDIAGNOSTICS_DEPTH_COLUMN_NAME
]

STATE_MAPPED_COLUMNS = {
    'filepath': FILENAME_COLUMN_NAME,
    'line': LINE_NUMBER_COLUMN_NAME,
    'column': COLUMN_NUMBER_COLUMN_NAME,
    'producer_msgnum': PRODUCER_COLUMN_NAME,
    'msgtext': MSG_TEXT_COLUMN_NAME,
    'severity': SEVERITY_COLUMN_NAME,
    'suppmask': SUPPRESSION_BITMASK_COLUMN_NAME,
    'suppjust': SUPPRESSION_JUSTIFICATION_COLUMN_NAME,
    'rulegroup': RULE_GROUP_COLUMN_NAME,
    'rulenum': RULE_TEXT_COLUMN_NAME,
    'depth': SUBDIAGNOSTICS_DEPTH_COLUMN_NAME,
    'id': SUBDIAGNOSTICS_ID_COLUMN_NAME,
    'finding_origins': SUBDIAGNOSTICS_ORIGIN_COLUMN_NAME
}

INFO_MAPPED_COLUMNS = {
    'license': 'License',
    'git_commit': 'Git Commit',
    'project_root': 'Project Root',
    'prqa_project_relative_path': 'Project Relative Path',
    'cli_version': 'QAC Version',
    'timestamp': 'Date',
    'acf': 'ACF',
    'cct': 'CCT',
    'ncf': 'NCF',
    'rcf': 'RCF',
    'vcf': 'VCF',
    'user_messages': 'User Messages',
    'cache_baseline_path': 'Cache Baseline Path',
    'local_baseline_path': 'Local Baseline Path',
    'local_baseline_sha': 'Local Baseline SHA'
}
