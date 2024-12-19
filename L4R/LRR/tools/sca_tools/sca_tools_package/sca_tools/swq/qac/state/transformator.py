# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: transformator.py
# ----------------------------------------------------------------------------
"""Defines methods for state file transformation

.. data:: STATE_SUMMARY_TRANSFORM_QUERY

    JQ query to flatten 'summary' object per file from 'analysis'
    in state.json.
    Below is an example of original 'summary' object from state.json and
    tranformed JSON with the `STATE_SUMMARY_TRANSFORM_QUERY` JQ query:

    Original:

    "fileA.cpp": {
        "summary": {
            "severities": {
                "0": "0",
                "1": "0",
                "2": "0",
                "3": "0",
                "4": "8",
                "5": "0",
                "6": "1",
                "7": "0",
                "8": "15",
                "9": "1"
            },
            "severities_total": "25",
            "analysis_error_count": "0",
            "analysis_exit_status": "0",
            "analysis_log": [
                {
                    "analysis_code": "0",
                    "module": "qac",
                    "timestamp": "(00:00:02)"
                }
            ]
        }
    }

    Transformed:

    {
        "filename": "fileA.cpp",
        "severities_total": "25",
        "analysis_error_count": "0",
        "analysis_exit_status": "0",
        "module_name": "qac",
        "analysis_code": "0",
        "severity0": "0",
        "severity1": "0",
        "severity2": "0",
        "severity3": "0",
        "severity4": "8",
        "severity5": "0",
        "severity6": "1",
        "severity7": "0",
        "severity8": "15",
        "severity9": "1"
    }
"""

import pandas as pd

from swq.common.jq import get_jq
from swq.qac.state.report.constants import PATH_COLUMN_NAME, \
    ENTITY_NAME_COLUMN_NAME, ENTITY_LINE_COLUMN_NAME, \
    ENTITY_TYPE_COLUMN_NAME, METRIC_NAME_COLUMN_NAME, \
    METRIC_VALUE_COLUMN_NAME

MAPPED_METRIC_COLUMNS = '{' + f'''
        "{PATH_COLUMN_NAME}": $path,
        "{ENTITY_NAME_COLUMN_NAME}": $entity_name,
        "{ENTITY_LINE_COLUMN_NAME}": $entity_line,
        "{ENTITY_TYPE_COLUMN_NAME}": $entity_type,
        "{METRIC_NAME_COLUMN_NAME}": $metric_name,
        "{METRIC_VALUE_COLUMN_NAME}": $metric_value
''' + '}'

STATE_METRICS_TRANSFORM_QUERY = f'''
    [
        .analysis |
        to_entries[] |
        .key as $path |
        .value.submetrics[]? |
        .line as $entity_line |
        .type as $entity_type |
        .name as $entity_name |
        .metrics | to_entries[] |
        .key as $metric_name |
        .value as $metric_value |
        {MAPPED_METRIC_COLUMNS}
    ]
'''

STATE_ANALYSIS_TRANSFORM_QUERY = '''
    [
        .analysis |
        to_entries[] |
        .value.findings[]? |
        .sub_findings as $sub_findings |
        del(.sub_findings) |
        [.] + $sub_findings |
        .[]
    ]
'''

STATE_INFO_TRANSFORM_QUERY = '''
    [
        . | del(.analysis)
    ]
'''

STATE_SUMMARY_TRANSFORM_QUERY = '''
[
    .analysis | to_entries[] |
    .key as $filename |
    select(.value.summary != null) |  .value.summary |
    .severities_total as $severities_total |
    .analysis_error_count as $analysis_error_count |
    .analysis_exit_status as $analysis_exit_status |
    .severities_total as $severities_total |
    [.severities[]] as $severities |
    .analysis_log[]? |
    .module as $module_name |
    .analysis_code as $analysis_code |
    $severities[0] as $severity0 |
    $severities[1] as $severity1 |
    $severities[2] as $severity2 |
    $severities[3] as $severity3 |
    $severities[4] as $severity4 |
    $severities[5] as $severity5 |
    $severities[6] as $severity6 |
    $severities[7] as $severity7 |
    $severities[8] as $severity8 |
    $severities[9] as $severity9 |
    {
        $filename,
        $severities_total,
        $analysis_error_count,
        $analysis_exit_status,
        $module_name,
        $analysis_code,
        $severity0,
        $severity1,
        $severity2,
        $severity3,
        $severity4,
        $severity5,
        $severity6,
        $severity7,
        $severity8,
        $severity9
    }
]
'''


def transform_state(state_content, query):
    """Transforms metrics state file content"""
    jq_instance = get_jq()
    transformed_state = \
        (jq_instance[query] << state_content)()

    return pd.read_json(transformed_state, dtype=False)
