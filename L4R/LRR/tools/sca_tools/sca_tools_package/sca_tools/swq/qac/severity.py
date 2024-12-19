# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: severity.py
# ----------------------------------------------------------------------------
"""Defines qac severity util methods"""

import re
from contextlib import suppress

from swq.qac.constants import QAVIEW_TABLE_COLUMN_IDS_INDEX, \
    QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX, LEVELS, \
    QAVIEW_TABLE_COLUMN_SEVERITY_INDEX, QAVIEW_TABLE_COLUMN_DEPTH_INDEX, \
    BITMASK_ACTIVE, BITMASK_FOR_STATISTIC_CALCULATION

TOTAL_NUMBER_MESSAGE_PREFIX = "total_number_of_warnings_of_Severity"
ACTIVE_NUMBER_MESSAGE_PREFIX = "active_number_of_warnings_of_Severity"


def _is_subdiagnostic(row):
    return int(row[QAVIEW_TABLE_COLUMN_DEPTH_INDEX]) != 0


def list_of_severitylevels_failed_quality_gate(aggregated_summary,
                                               fail_threshold):
    """Gets all the active issues from provided issues and fail dicts"""
    failed_severitylevels = []
    for level in reversed(LEVELS):
        if f"fail{level}" not in fail_threshold:
            continue
        if aggregated_summary.get(f"{ACTIVE_NUMBER_MESSAGE_PREFIX}{level}"
                                  ) > int(fail_threshold.get(f"fail{level}")):
            failed_severitylevels.append(str(level))
    return failed_severitylevels


def match_severity_level(item: str):
    """Returns a match or None"""
    return re.search(r"severitylevel(?P<level>\d)", item)


def get_severity_level(item):
    """Get the severity level of the warning
    Args:
        item (str): row item with severity level info
    Returns:
        int: severity level. If no level is found, return None
    """
    match = match_severity_level(item)
    if match:
        return int(match.group("level"))
    return None


def create_list():
    """Create a list with 10 values equal to 0"""
    return [0] * 10


def calculate_aggregated_summary(csv_list,
                                 with_full_subdiagnostics,
                                 ids_to_ignore_tuple=()):
    """Counts and gets dict with its issues from csv_list"""

    # Containers for number of warnings
    number_of_warnings_of_severitylevel = create_list()
    project_active_warnings = create_list()
    project_total_warnings = 0

    number_of_warnings_per_bitmask_per_severitylevel = \
        {i: create_list() for i in BITMASK_FOR_STATISTIC_CALCULATION}

    aggregated_summary = {}
    for row in csv_list:
        # Suppress rows that don't correspond to warnings
        with suppress(IndexError):
            try:
                level = int(row[QAVIEW_TABLE_COLUMN_SEVERITY_INDEX])
            except ValueError:
                continue

            if with_full_subdiagnostics and _is_subdiagnostic(row):
                continue

            number_of_warnings_of_severitylevel[level] += 1
            project_total_warnings += 1
            if not any(s in row[QAVIEW_TABLE_COLUMN_IDS_INDEX]
                       for s in ids_to_ignore_tuple):
                if row[QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX] == \
                    BITMASK_ACTIVE:
                    project_active_warnings[level] += 1
                # check bitmask types and count accordingly,
                # at this point, we ignore dashboard types
                if row[QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX] in \
                    BITMASK_FOR_STATISTIC_CALCULATION:
                    number_of_warnings_per_bitmask_per_severitylevel[
                        row[QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX]][
                            level] += 1

    for level in LEVELS:
        total_number_message = \
            f"{TOTAL_NUMBER_MESSAGE_PREFIX}{level}"
        aggregated_summary.update({
            f"{total_number_message}":
            number_of_warnings_of_severitylevel[level]
        })
        aggregated_summary.update({
            f"{ACTIVE_NUMBER_MESSAGE_PREFIX}{level}":
            project_active_warnings[level]
        })

        for bitmask in BITMASK_FOR_STATISTIC_CALCULATION:
            aggregated_summary.update({
                f"{total_number_message}_suppression_bitmask_{bitmask}":
                number_of_warnings_per_bitmask_per_severitylevel[bitmask]
                [level]
            })

    aggregated_summary.update(
        {"project_total_warnings": project_total_warnings})
    aggregated_summary.update(
        {"project_active_warnings": sum(project_active_warnings)})
    return aggregated_summary
