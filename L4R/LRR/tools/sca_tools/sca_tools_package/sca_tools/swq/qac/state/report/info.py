# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: info.py
# ----------------------------------------------------------------------------
"""This module contains methods to create info report"""

from swq.common.report.utils import add_colon_to_column_names
from swq.qac.state.report.constants import INFO_MAPPED_COLUMNS
from swq.qac.state.transformator import STATE_INFO_TRANSFORM_QUERY, \
    transform_state


def create_info_dataframe(state_content):
    """Creates info report dataframe"""
    info_dataframe = transform_state(state_content, STATE_INFO_TRANSFORM_QUERY)
    info_dataframe.rename(
        columns=add_colon_to_column_names(INFO_MAPPED_COLUMNS), inplace=True)
    info_dataframe = info_dataframe.melt()

    return info_dataframe
