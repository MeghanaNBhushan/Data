# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: analysis.py
# ----------------------------------------------------------------------------
"""This module contains methods to create analysis report"""

from numpy import vectorize
from swq.common.report.utils import \
    extend_dataframe_with_codeowners_information
from swq.qac.state.report.constants import ANALYSIS_REPORT_COLUMNS, \
    FILENAME_COLUMN_NAME, SUBDIAGNOSTICS_FULL_COLUMNS, \
    SUBDIAGNOSTICS_LIGHT_COLUMNS, STATE_MAPPED_COLUMNS
from swq.qac.state.utils import filter_out_subdiagnostics_if_present
from swq.qac.state.transformator import STATE_ANALYSIS_TRANSFORM_QUERY, \
    transform_state


def create_analysis_dataframe(config, state_content):
    """Creates analysis report dataframe"""
    analysis_dataframe = \
        transform_state(state_content, STATE_ANALYSIS_TRANSFORM_QUERY)

    append_producer_msgnum_column(analysis_dataframe)
    set_humanreadable_column_names(analysis_dataframe)
    analysis_dataframe = \
        select_subdiagnostics_data_for_report(config, analysis_dataframe)

    if config.codeowners_file:
        extend_dataframe_with_codeowners_information(config,
                                                     analysis_dataframe,
                                                     FILENAME_COLUMN_NAME)

    return analysis_dataframe


def set_humanreadable_column_names(analysis_dataframe):
    """Renames columns according to _STATE_MAPPED_COLUMNS"""
    analysis_dataframe.rename(columns=STATE_MAPPED_COLUMNS, inplace=True)


def select_subdiagnostics_data_for_report(config, analysis_dataframe):
    """Selects subdiagnostics data"""
    columns = ANALYSIS_REPORT_COLUMNS.copy()

    if config.with_full_subdiagnostics:
        columns.extend(SUBDIAGNOSTICS_FULL_COLUMNS)
    else:
        filter_out_subdiagnostics_if_present(analysis_dataframe)

    if config.with_subdiagnostics:
        columns.extend(SUBDIAGNOSTICS_LIGHT_COLUMNS)

    return analysis_dataframe[columns]


def append_producer_msgnum_column(analysis_dataframe):
    """Appends analysis report with producer_msgnum column"""
    def _get_producer_with_msg_num(producer, msgnum):
        return f'{producer}:{msgnum}'

    analysis_dataframe.loc[:, 'producer_msgnum'] = \
        vectorize(_get_producer_with_msg_num)(
            analysis_dataframe['producer'],
            analysis_dataframe['padmsgnum'].astype(str))
