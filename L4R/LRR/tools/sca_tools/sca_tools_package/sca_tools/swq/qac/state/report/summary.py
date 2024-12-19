# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: summary.py
# ----------------------------------------------------------------------------
"""This module contains methods to create summary report"""

import pandas as pd
from swq.common.logger import LOGGER
from swq.common.report.utils import append_row_to_dataframe, \
    group_report_by_columns, filter_report, append_string_to_report_column
from swq.qac.constants import BITMASK_ACTIVE, BITMASK_FOR_STATISTIC_CALCULATION
from swq.qac.state.report.constants import SUMMARY_REPORT_COLUMNS, \
    PRODUCER_COLUMN_NAME, RULE_TEXT_COLUMN_NAME, SEVERITY_COLUMN_NAME, \
    SUPPRESSION_BITMASK_COLUMN_NAME
from swq.qac.state.transformator import transform_state, \
    STATE_SUMMARY_TRANSFORM_QUERY
from swq.qac.state.utils import filter_out_subdiagnostics_if_present
from swq.qac.severity import ACTIVE_NUMBER_MESSAGE_PREFIX, \
    TOTAL_NUMBER_MESSAGE_PREFIX

SUMMARY_COLUMN = SUMMARY_REPORT_COLUMNS[0]
COUNT_COLUMN = SUMMARY_REPORT_COLUMNS[1]
SEVERITY_GROUP_COLUMNS = [
    SEVERITY_COLUMN_NAME, SUPPRESSION_BITMASK_COLUMN_NAME
]
COMPONENTS_GROUP_COLUMNS = [
    PRODUCER_COLUMN_NAME, SUPPRESSION_BITMASK_COLUMN_NAME
]
RULE_MSG_SEPARATOR = ','
RULE_TEXT_SEPARATED = 'RULE_TEXT_SEPARATED'
COMPONENT_COLUMN = 'COMPONENT'
ACTIVE_POSTFIX = ' active'
TOTAL_POSTFIX = ' total'
SUMMARY_FILENAME_COLUMN = 'filename'
MODULE_NAME_COLUMN = 'module_name'
MODULE_OUTPUTS_COLUMN = 'module_outputs'
MODULE_ERROR_COUNT_COLUMN = 'module_error_count'
MODULE_ANALISYS_CODE = 'analysis_code'
SUMMARY_COLUMNS_TO_SUM = [
    'analysis_error_count', 'severities_total', MODULE_ERROR_COUNT_COLUMN,
    'severity0', 'severity1', 'severity2', 'severity3', 'severity4',
    'severity5', 'severity6', 'severity7', 'severity8', 'severity9'
]


def create_summary_dataframe(analysis_dataframe):
    """Creates summary report dataframe"""
    summary_dataframe = pd.DataFrame(columns=SUMMARY_REPORT_COLUMNS)

    filter_out_subdiagnostics_if_present(analysis_dataframe)

    LOGGER.debug('Aggregating summary per severity')
    aggregated_summary_per_severity = _get_severity_summary(analysis_dataframe)

    LOGGER.debug('Aggregating summary per rule text')
    aggregated_summary_per_rule_text = _get_rule_text_summary(
        analysis_dataframe)

    LOGGER.debug('Aggregating summary per component')
    aggregated_summary_per_component = _get_components_summary(
        analysis_dataframe)

    summary_dataframe = (summary_dataframe
                            .append(aggregated_summary_per_severity)
                            .append(aggregated_summary_per_rule_text)
                            .append(aggregated_summary_per_component)
                         )  # yapf: disable

    return summary_dataframe


def create_summary_per_file_dataframe(state_content):
    """Creates summary per file report dataframe"""
    dataframe = \
        transform_state(state_content, STATE_SUMMARY_TRANSFORM_QUERY)

    _calculate_non_zero_codes_per_module(dataframe)

    severities_dataframe = _get_severities_per_file(dataframe)

    modules_dataframe = _aggregate_modules_per_file(dataframe)

    module_errors_dataframe = _calculate_error_count_per_module(dataframe)

    summary_per_file_dataframe = (severities_dataframe
                                    .join(modules_dataframe,
                                          on=SUMMARY_FILENAME_COLUMN,
                                          how='left')
                                    .join(module_errors_dataframe,
                                          on=SUMMARY_FILENAME_COLUMN,
                                          how='left')
                                  )  # yapf: disable

    summary_per_file_dataframe = _add_total_to_summary_per_file(
        summary_per_file_dataframe)

    return summary_per_file_dataframe


def _get_severity_summary(analysis_dataframe):
    """Aggregates summary per severity from Analysis report"""
    total_warnings_per_severity = _get_total_warnings_per_severity(
        analysis_dataframe)

    active_warnings_per_severity = _get_active_warnings_per_severity(
        analysis_dataframe)

    warnings_per_bitmask = _get_suppressed_warnings_per_bitmask(
        analysis_dataframe)

    sort_columns = [SEVERITY_COLUMN_NAME, SUMMARY_COLUMN]
    select_columns = [SUMMARY_COLUMN, COUNT_COLUMN]
    severity_summary = (total_warnings_per_severity
                            .append(active_warnings_per_severity)
                            .append(warnings_per_bitmask)
                            .sort_values(by=sort_columns)
                        )[select_columns]  # yapf: disable

    _append_project_totals_to_report(severity_summary,
                                     active_warnings_per_severity,
                                     total_warnings_per_severity)

    return severity_summary


def _get_rule_text_summary(analysis_dataframe):
    """Aggregates summary per rule text from Analysis report"""
    separated_rules_report = _get_separated_rule_text_report(
        analysis_dataframe)

    rules_total = group_report_by_columns(separated_rules_report,
                                          RULE_TEXT_SEPARATED, COUNT_COLUMN)

    rules_total = append_string_to_report_column(rules_total,
                                                 RULE_TEXT_SEPARATED,
                                                 RULE_TEXT_SEPARATED,
                                                 TOTAL_POSTFIX)

    active_rules_query = \
        f'`{SUPPRESSION_BITMASK_COLUMN_NAME}` == "{BITMASK_ACTIVE}"'

    rules_active = group_report_by_columns(
        filter_report(separated_rules_report, active_rules_query),
        RULE_TEXT_SEPARATED, COUNT_COLUMN)

    rules_active = append_string_to_report_column(rules_active,
                                                  RULE_TEXT_SEPARATED,
                                                  RULE_TEXT_SEPARATED,
                                                  ACTIVE_POSTFIX)

    rename_columns = {RULE_TEXT_SEPARATED: SUMMARY_COLUMN}
    rules_summary = (rules_total
                        .append(rules_active)
                        .sort_values(RULE_TEXT_SEPARATED)
                        .rename(columns=rename_columns)
                     )  # yapf: disable

    return rules_summary


def _get_components_summary(analysis_dataframe):
    """Aggregates summary per component from Analysis report"""
    total_warnings_per_component = _get_total_warnings_per_component(
        analysis_dataframe)

    active_warnings_per_component = _get_active_warnings_per_component(
        analysis_dataframe)

    rename_columns = {COMPONENT_COLUMN: SUMMARY_COLUMN}
    select_columns = [SUMMARY_COLUMN, COUNT_COLUMN]
    component_summary = (total_warnings_per_component
                            .append(active_warnings_per_component)
                            .sort_values(COMPONENT_COLUMN)
                            .rename(columns=rename_columns)
                         )[select_columns]  # yapf: disable

    return component_summary


def _group_report_by_severity(report, query=None):
    """Generates groupped report by severity.
    Optionally filters using provided query"""
    if query:
        return group_report_by_columns(
            filter_report(report, query, SEVERITY_GROUP_COLUMNS),
            SEVERITY_GROUP_COLUMNS, COUNT_COLUMN)

    return group_report_by_columns(report, SEVERITY_COLUMN_NAME, COUNT_COLUMN)


def _get_total_warnings_per_severity(analysis_dataframe):
    """Generates total per severity dataframe and appends
    summary column with proper naming"""
    total_warnings = _group_report_by_severity(analysis_dataframe)
    total_warnings[SUMMARY_COLUMN] = \
        TOTAL_NUMBER_MESSAGE_PREFIX + total_warnings[SEVERITY_COLUMN_NAME]

    return total_warnings


def _get_active_warnings_per_severity(analysis_dataframe):
    """Generates active per severity dataframe and appends
    summary column with proper naming"""
    active_warnings_query = \
        f'`{SUPPRESSION_BITMASK_COLUMN_NAME}` == "{BITMASK_ACTIVE}"'

    active_warnings = _group_report_by_severity(analysis_dataframe,
                                                active_warnings_query)

    active_warnings[SUMMARY_COLUMN] =\
        ACTIVE_NUMBER_MESSAGE_PREFIX + active_warnings[SEVERITY_COLUMN_NAME]

    return active_warnings


def _get_suppressed_warnings_per_bitmask(analysis_dataframe):
    """Generates suppressed warnings dataframe and appends
    summary column with proper naming"""
    def _assemble_suppression_summary_name(row):
        return TOTAL_NUMBER_MESSAGE_PREFIX + row[SEVERITY_COLUMN_NAME] +\
            '_suppression_bitmask_' + str(row[SUPPRESSION_BITMASK_COLUMN_NAME])

    suppressed_warnings_query = \
        f'`{SUPPRESSION_BITMASK_COLUMN_NAME}` \
            in {BITMASK_FOR_STATISTIC_CALCULATION}'

    warnings_per_bitmask = _group_report_by_severity(
        analysis_dataframe, suppressed_warnings_query)

    warnings_per_bitmask[SUMMARY_COLUMN] = ""
    if not warnings_per_bitmask.empty:
        warnings_per_bitmask[SUMMARY_COLUMN] = warnings_per_bitmask.apply(
            _assemble_suppression_summary_name, axis=1)

    return warnings_per_bitmask[[
        SEVERITY_COLUMN_NAME, SUMMARY_COLUMN, COUNT_COLUMN
    ]]


def _append_project_totals_to_report(report, active_warnings, total_warnings):
    """Appends project active and project total summary to report"""
    append_row_to_dataframe(
        report,
        ['project_active_warnings', active_warnings[COUNT_COLUMN].sum()])

    append_row_to_dataframe(
        report, ['project_total_warnings', total_warnings[COUNT_COLUMN].sum()])


def _get_separated_rule_text_report(analysis_dataframe):
    """Generates dataframe with separated rule text"""
    kwargs = {
        RULE_TEXT_SEPARATED:
        analysis_dataframe[RULE_TEXT_COLUMN_NAME].str.split(RULE_MSG_SEPARATOR)
    }

    return analysis_dataframe.assign(**kwargs).explode(RULE_TEXT_SEPARATED)


def _get_total_warnings_per_component(analysis_dataframe):
    """Generates total per component dataframe and appends
    summary column with proper naming"""
    total_warnings = group_report_by_columns(analysis_dataframe,
                                             PRODUCER_COLUMN_NAME,
                                             COUNT_COLUMN)

    total_warnings = append_string_to_report_column(total_warnings,
                                                    PRODUCER_COLUMN_NAME,
                                                    COMPONENT_COLUMN,
                                                    TOTAL_POSTFIX)

    return total_warnings


def _get_active_warnings_per_component(analysis_dataframe):
    """Generates active per component dataframe and appends
    summary column with proper naming"""
    _query_filter = \
        f'`{SUPPRESSION_BITMASK_COLUMN_NAME}` == "{BITMASK_ACTIVE}"'

    _component_summary_column = [PRODUCER_COLUMN_NAME, COUNT_COLUMN]

    active_warnings = group_report_by_columns(analysis_dataframe,
                                              COMPONENTS_GROUP_COLUMNS,
                                              COUNT_COLUMN)

    active_warnings = filter_report(active_warnings, _query_filter,
                                    _component_summary_column)

    active_warnings = append_string_to_report_column(active_warnings,
                                                     PRODUCER_COLUMN_NAME,
                                                     COMPONENT_COLUMN,
                                                     ACTIVE_POSTFIX)

    return active_warnings


def _calculate_non_zero_codes_per_module(dataframe):
    dataframe[MODULE_ERROR_COUNT_COLUMN] = dataframe[[
        MODULE_ANALISYS_CODE
    ]].astype(int).gt(0).sum(axis=1)


def _get_severities_per_file(dataframe):
    return dataframe.drop(columns=[
        MODULE_NAME_COLUMN, MODULE_ERROR_COUNT_COLUMN, MODULE_ANALISYS_CODE
    ],
                          inplace=False).drop_duplicates()


def _aggregate_modules_per_file(dataframe):
    _assemble_module_outputs(dataframe)

    return dataframe.drop_duplicates().groupby(
        SUMMARY_FILENAME_COLUMN)[MODULE_OUTPUTS_COLUMN].apply(list)


def _assemble_module_outputs(dataframe):
    dataframe[MODULE_OUTPUTS_COLUMN] = \
        dataframe[MODULE_NAME_COLUMN].str.cat(
            dataframe[MODULE_ANALISYS_CODE], sep=':')


def _calculate_error_count_per_module(dataframe):
    return dataframe[[SUMMARY_FILENAME_COLUMN, MODULE_ERROR_COUNT_COLUMN
                      ]].groupby(SUMMARY_FILENAME_COLUMN).sum()


def _add_total_to_summary_per_file(dataframe):
    total = dataframe.loc[:, SUMMARY_COLUMNS_TO_SUM].astype(int).sum(axis=0)
    total[SUMMARY_FILENAME_COLUMN] = 'Total'

    return dataframe.append(total, ignore_index=True)
