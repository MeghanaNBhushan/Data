# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: filter_qaview.py
# ----------------------------------------------------------------------------
"""
The purpose of this script is to parse the export of Helix QAC (via qaview
command from helper) for which severity levels are contained in the export
and then fail or pass the build on jenkins.

For example, if there are several severitylevel 8 warnings, 300 ID 4444,
9000 ID 1234 and 3000 ID 1239 in the export you could implement a jenkins
gate to fail the build if there are 301 warnings via:
python.exe sca_tools.py qac filter_qaview \
    --qaview_csv qacli-view.csv \
    --severity_level_fail_threshold_for_level_8 301 \
    --ignore_ids 1234,1239 \
    --datastore_path config.json \
    --datastore_target "target"
"""
from os import path as os_path, makedirs
from sys import exit as sys_exit
from pandas import read_csv
from swq.qac.constants import LEVELS, \
    QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX, \
    QAVIEW_TABLE_COLUMN_SUPPRESSION_JUSTIFICATION_INDEX, \
    CHECK_JUSTIFICATION_FOR_SUPPRESSION_BITMASK, BITMASK_ACTIVE
from swq.qac.state.report.constants import SUBDIAGNOSTICS_FULL_COLUMNS
from swq.qac.severity import calculate_aggregated_summary, \
    list_of_severitylevels_failed_quality_gate
from swq.qac.exporters.state_exporter import \
    _create_html_file_from_list_of_lists
from swq.common.component_mapping import no_regex_matches
from swq.common.logger import LOGGER
from swq.common.output_producer import create_output_producer
from swq.common.return_codes import \
    RC_FINDINGS_LARGER_THAN_THRESHOLD, RC_JUSTIFICATION_FAIL_CRITERIA, \
    RC_FINDINGS_AND_JUSTIFICATIONS_DO_NOT_MEET_CRITERIA


def justifications_for_suppressed_warnings_fail_requirements(
        csv_file_content, regular_expressions):
    """Check that proper Justification is provided for suppressed warning"""
    for row in csv_file_content:
        if not row:
            continue
        if row[QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX] in \
            CHECK_JUSTIFICATION_FOR_SUPPRESSION_BITMASK and \
            no_regex_matches(
                    regular_expressions,
                    row[QAVIEW_TABLE_COLUMN_SUPPRESSION_JUSTIFICATION_INDEX]):
            return True
    return False


def generate_threshold_exceeding_warnings_report(warning_records,
                                                 failed_severitylevels,
                                                 config):
    """Generates threshold exceeding warnings report"""
    active_warnings = f'`Suppression type bitmask` == "{BITMASK_ACTIVE}"'
    failed_severity_levels = f'Severity in {failed_severitylevels}'

    threshold_exceeding_warnings = warning_records.query(
        f'{failed_severity_levels} and {active_warnings}')

    threshold_warnings_report_dirname = \
        os_path.dirname(config.qac_threshold_warnings_report)

    if not os_path.exists(threshold_warnings_report_dirname):
        makedirs(threshold_warnings_report_dirname)
    threshold_exceeding_warnings_list = \
        [threshold_exceeding_warnings.columns.values.tolist()] + \
        threshold_exceeding_warnings.values.tolist()

    _create_html_file_from_list_of_lists(
        config, config.project_git_commit,
        '- Active/Unsuppressed issues from filter-qaview',
        config.qac_threshold_warnings_report,
        threshold_exceeding_warnings_list)


def filter_qaview_entrypoint(config):
    """Entrypoint for filter_qaview command"""
    arg_ids_to_ignore_tuple = config.ignore_ids.split(',') \
        if config.ignore_ids else ()
    LOGGER.info(f"IDs that were ignored: {arg_ids_to_ignore_tuple} \n")

    fail_thresholds = {}
    justification_check_failed = False

    for level in reversed(LEVELS):
        if not getattr(config, f"fail_{level}"):
            continue
        fail_thresholds.update(
            {f"fail{level}": int(getattr(config, f"fail_{level}"))})

    LOGGER.debug(f"Failure settings: {fail_thresholds} \n")

    warning_records = read_csv(config.qaview_csv,
                               delimiter=',',
                               quotechar='"',
                               keep_default_na=False,
                               dtype=str)
    csv_values_list = warning_records.values.tolist()

    if config.justification_message_regexp:
        justification_check_failed = \
            justifications_for_suppressed_warnings_fail_requirements(
                csv_values_list,
                config.justification_message_regexp)

    full_subdiagnostics_enabled = \
        all(header in warning_records.columns
            for header in SUBDIAGNOSTICS_FULL_COLUMNS)
    aggregated_summary = calculate_aggregated_summary(
        csv_values_list, full_subdiagnostics_enabled, arg_ids_to_ignore_tuple)

    output_producer = create_output_producer(config)
    output_producer(aggregated_summary)

    failed_severitylevels = list_of_severitylevels_failed_quality_gate(
        aggregated_summary, fail_thresholds)

    if failed_severitylevels and justification_check_failed:
        generate_threshold_exceeding_warnings_report(warning_records,
                                                     failed_severitylevels,
                                                     config)
        LOGGER.error('\nActive/Unsuppressed Issues of level(s) {} found!'
                     '\nProper justification for suppressed warning(s) not '
                     'provided!'.format(", ".join(failed_severitylevels)))
        sys_exit(RC_FINDINGS_AND_JUSTIFICATIONS_DO_NOT_MEET_CRITERIA)
    elif failed_severitylevels:
        generate_threshold_exceeding_warnings_report(warning_records,
                                                     failed_severitylevels,
                                                     config)
        LOGGER.error(
            "\nActive/Unsuppressed Issues of level(s) {} found!".format(
                ", ".join(failed_severitylevels)))
        sys_exit(RC_FINDINGS_LARGER_THAN_THRESHOLD)
    elif justification_check_failed:
        LOGGER.error(
            "\nProper justification for suppressed warning(s) not provided!")
        sys_exit(RC_JUSTIFICATION_FAIL_CRITERIA)
