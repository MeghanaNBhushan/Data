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
"""Defines constants for the coverity scripts"""

MERGE_KEY_COLUMN_INDEX = 1
CHECKER_INDEX_COLUMN_INDEX = 4
PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX = 13
MAIN_EVENT_LINE_NUMBER_COLUMN_INDEX = 12
IMPACT_COLUMN_INDEX = 18
SUBCATEGORY_LONG_DESCRIPTION_COLUMN_INDEX = 22
ERROR_EXPORT_TABLE_MAIN_EVENT_FILEPATH_INDEX = 23

UNCLASSIFIED_TRIAGE_CLASSIFICATION = 'Unclassified'
TRIAGE_CLASSIFICATION_COLUMN_NAME = 'triage_classification'

BUILD_SCRIPT_LINUX = 'generated_build.sh'
BUILD_SCRIPT_WINDOWS = 'generated_build.bat'
FILTERED_REPORT_SUFFIX = 'filtered'
SCA_TOOL_DIR = 'sca_tools'
EXPORT_DIR = 'export'

DEFAULT_EXPORT_FORMATS = ['csv', 'xlsx']
