# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	constants.py
# ----------------------------------------------------------------------------
"""Defines constants for the qac scripts"""

LEVELS = range(10)

QAVIEW_TABLE_COLUMN_IDS_INDEX = 3
QAVIEW_TABLE_COLUMN_SEVERITY_INDEX = 5
QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX = 6
QAVIEW_TABLE_COLUMN_SUPPRESSION_JUSTIFICATION_INDEX = 7
QAVIEW_TABLE_COLUMN_DEPTH_INDEX = 11

BITMASK_ACTIVE = "0"
BITMASK_FOR_STATISTIC_CALCULATION = ["1", "4", "5"]

DIAG_FILES_ROOT_DIR = '_SOURCE_ROOT'
SCA_TOOL_DIR = 'sca_tools'
EXPORT_DIR = 'export'

CHECK_JUSTIFICATION_FOR_SUPPRESSION_BITMASK = ["1", "5"]

DEFAULT_EXPORT_FORMATS = ['csv', 'xlsx', 'html']

SYNC_TYPE_VALUES = ['JSON', 'BUILD_LOG', 'MONITOR']

HELP_PAGES_CUSTOM_DIR = 'custom'
HELP_PAGES_ORIGINAL_DIR = 'original'
RULE_GROUP_DIR = 'rule_group'

BASELINE_FILE_NAME = 'files.sup'

PROJECT_GENERATION_FAILED_MESSAGE = 'Project generation failed'
PROJECT_SYNCHRONIZATION_FAILED_MESSAGE = 'Project synchronization failed'
