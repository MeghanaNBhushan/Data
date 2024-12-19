# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: filter_preview_report.py
# ----------------------------------------------------------------------------
"""
The purpose of this script is to parse the export of SCA tools coverity
preview_report subcommand for which new triage classifications found
and then fail or pass the build on jenkins.

Example of usage:
python.exe sca_tools.py coverity filter_report \
    --preview_report_csv preview-report.csv \
    --datastore_path config.json \
    --datastore_target "target"
"""

from os.path import isfile
from sys import exit as sys_exit
from pandas import read_csv

from swq.common.logger import LOGGER
from swq.common.output_producer import create_output_producer
from swq.common.return_codes import log_and_exit, RC_INVALID_FILEPATH, \
    RC_TRIAGE_CLASSIFICATION_ISSUE_FOUND
from swq.coverity.constants import UNCLASSIFIED_TRIAGE_CLASSIFICATION, \
    TRIAGE_CLASSIFICATION_COLUMN_NAME


def __calculate_unclassified_issues(csv_file_content):
    total_issues = 0
    unclassified_issues = 0
    for _, row in csv_file_content:
        total_issues += 1
        if row[TRIAGE_CLASSIFICATION_COLUMN_NAME] == \
            UNCLASSIFIED_TRIAGE_CLASSIFICATION:
            unclassified_issues += 1

    return (total_issues, unclassified_issues)


def __aggregate_summary(total_issues, unclassified_issues):
    return {
        "unclassified_issues": unclassified_issues,
        "total_issues": total_issues
    }


def coverity_filter_report(config):
    """Entrypoint for filter_report command"""
    if not isfile(config.preview_report_csv):
        LOGGER.error("File \"" + str(config.preview_report_csv) +
                     "\" is not readable")
        log_and_exit(RC_INVALID_FILEPATH)

    file_content = read_csv(config.preview_report_csv,
                            delimiter=',',
                            quotechar='"',
                            keep_default_na=False,
                            dtype=str)
    csv_from_output_iter = file_content.iterrows()

    (total_issues, unclassified_issues
     ) = __calculate_unclassified_issues(csv_from_output_iter)

    aggregated_summary = __aggregate_summary(total_issues, unclassified_issues)

    output_producer = create_output_producer(config)
    output_producer(aggregated_summary)

    if unclassified_issues:
        LOGGER.error("\nUnclassified issue(s) found!")
        sys_exit(RC_TRIAGE_CLASSIFICATION_ISSUE_FOUND)
