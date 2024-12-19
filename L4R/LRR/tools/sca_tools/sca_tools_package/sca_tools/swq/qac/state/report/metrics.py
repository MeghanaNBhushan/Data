# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: metrics.py
# ----------------------------------------------------------------------------
"""This module contains methods to create metrics report"""

from swq.common.logger import LOGGER
from swq.common.report.utils import \
    extend_dataframe_with_codeowners_information
from swq.qac.state.transformator import STATE_METRICS_TRANSFORM_QUERY, \
    transform_state
from swq.qac.state.report.constants import METRIC_NAME_COLUMN_NAME, \
    PATH_COLUMN_NAME


def create_metrics_dataframe(config, state_content):
    """Creates metrics report dataframe"""
    metrics_dataframe = \
        transform_state(state_content, STATE_METRICS_TRANSFORM_QUERY)

    if not metrics_dataframe.empty:
        if config.metrics_filter_list:
            LOGGER.info('Applying metrics filter to the metrics report')
            metrics_dataframe = metrics_dataframe.query(
                f'{METRIC_NAME_COLUMN_NAME} in {config.metrics_filter_list}')

        if config.codeowners_file:
            extend_dataframe_with_codeowners_information(
                config, metrics_dataframe, PATH_COLUMN_NAME)

    return metrics_dataframe
