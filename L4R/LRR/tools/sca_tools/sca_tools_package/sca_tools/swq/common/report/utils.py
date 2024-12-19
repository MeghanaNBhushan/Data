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
"""Defines methods to interact with reports"""

from swq.common.logger import LOGGER
from swq.map_teams.map_teams import map_teams_components_in_dataframe, \
    COMPONENT_COLUMN_NAME, TEAM_COLUMN_NAME, SENSITIVE_INFO_WARNING_MESSAGE


def extend_dataframe_with_codeowners_information(config,
                                                 dataframe,
                                                 path_column_name=''):
    """Extends report with codeowners information"""
    LOGGER.warning(SENSITIVE_INFO_WARNING_MESSAGE)
    LOGGER.info('Adding Team/Component information to the report')
    map_teams_components_in_dataframe(dataframe, TEAM_COLUMN_NAME,
                                      COMPONENT_COLUMN_NAME, config,
                                      path_column_name)


def group_report_by_columns(report, columns, count_column_name):
    """Groups report by provided columns and create new column with count"""
    return report.groupby(columns).size().reset_index(name=count_column_name)


def filter_report(report, query_filter, columns=None):
    """Filters and optionally changes report columns"""
    if columns:
        return report.query(query_filter)[columns]

    return report.query(query_filter)


def append_string_to_report_column(report, original_column, new_column,
                                   string_to_append):
    """Appends string to rows from original column into new column"""
    kwargs = {new_column: report[original_column] + string_to_append}

    return report.assign(**kwargs)


def append_row_to_dataframe(dataframe, row):
    """Appends dataframe with row"""
    dataframe.loc[len(dataframe)] = row


def add_colon_to_column_names(columns):
    """Adds colon to column names"""
    return {key: f"{value}:" for key, value in columns.items()}
