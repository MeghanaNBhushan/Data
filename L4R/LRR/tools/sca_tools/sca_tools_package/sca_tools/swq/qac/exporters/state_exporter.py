# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: state_exporter.py
# ----------------------------------------------------------------------------
"""Exports state information to csv and html"""

import json

from os import path
from zipfile import ZipFile
from datetime import datetime

from swq.qac.constants import BITMASK_ACTIVE, QAVIEW_TABLE_COLUMN_IDS_INDEX, \
    QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX, SCA_TOOL_DIR, EXPORT_DIR
from swq.qac.severity import _is_subdiagnostic, calculate_aggregated_summary
from swq.qac.exporters.html_exporter import create_html_from_list_of_lists, \
    LICENSE_WARNING
from swq.qac.state.utils import create_state_file
from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t, \
    check_if_project_exists
from swq.common.export.csv_exporter import CsvExporter
from swq.common.export.zipped_csv_exporter import ZippedCsvExporter
from swq.common.export.xlsx_exporter import XlsxExporter
from swq.common.return_codes import log_and_exit, RC_CONFIG_PARSING_ERROR
from swq.common.component_mapping import ComponentMapper
from swq.common.file.file_utils import calculate_sha256
from swq.map_teams.map_teams import add_team_components_to_row, \
    TEAM_REPORT_EXTRA_FIELDNAMES, SENSITIVE_INFO_WARNING_MESSAGE

QAVIEW_TABLE_COLUMN_FILENAME_INDEX = 0
QAVIEW_TABLE_COLUMN_SEVERITY_LEVEL_INFO_INDEX = 9

DIAG_XML_ELEMENTS = [
    'line', 'column', 'producer', 'padmsgnum', 'msgtext', 'severity',
    'suppmask', 'suppjust', 'rulegroup', 'rulenum'
]
SUBDIAG_XML_ELEMENTS = ['id', 'finding_origins']
SUBDIAG_XML_ELEMENTS_FULL = ['id', 'depth']

CSV_SUMMARY_HEADER = ['Name/Description', 'Count']

DEPRECATED_CSV_HEADER_WITH_FILENAME = [
    'Filename', 'Line number', 'Column number',
    'Producer component:Message number', 'Message text', 'Severity',
    'Suppression type bitmask', 'Suppression justification', 'Rule Group',
    'Rule text'
]

SUBDIAG_CSV_HEADER = [
    'SCA Tools Subdiagnostics ID', 'SCA Tools Subdiagnostics Origin'
]
SUBDIAG_CSV_HEADER_FULL = [
    'SCA Tools Subdiagnostics ID', 'SCA Tools Subdiagnostics Depth'
]


_METRICS_CSV_HEADER = [
    'path', 'entity_name', 'entity_line', 'entity_type', 'metric_name',
    'metric_value'
]

_STATE_COMMANDS_DEPRECATION_MSG = '!!! This subcommand is going to be \
deprecated in upcoming releases. Use `export_analysis` subcommand with \
neccessary flags instead !!!'


def qac_state(config):
    """Exports QAC project state reports"""
    _print_deprecation_message()
    create_state_file(config, generate_state=True)
    export_reports(config, summary_details=True)


def qac_export_state(config):
    """Exports reports from QAC project state file"""
    _print_deprecation_message()
    check_if_project_exists(config.qac_project_path)
    export_reports(config, summary_details=True)


def _print_deprecation_message():
    line_filler = '*' * len(_STATE_COMMANDS_DEPRECATION_MSG)
    LOGGER.warning(line_filler)
    LOGGER.warning(_STATE_COMMANDS_DEPRECATION_MSG.upper())
    LOGGER.warning(line_filler)


def _create_exporters(config, basename, default_sheet):
    def _xlsx_exporter_func():
        return XlsxExporter(
            _get_final_export_path(
                config, '{}-{}.xlsx'.format(basename, default_sheet)))

    def _csv_exporter_func():
        return CsvExporter(_get_final_export_path(config, basename))

    def _csv_zip_exporter_func():
        return ZippedCsvExporter(_get_final_export_path(config, basename))

    export_format_to_exporter = []
    for export_format in config.export_formats:
        if f"_{export_format}_exporter_func" in locals():
            export_format_to_exporter.append(
                locals()[f"_{export_format}_exporter_func"]())

    return export_format_to_exporter


def _get_final_export_path(config, filename):
    return path.join(config.qac_project_path, SCA_TOOL_DIR, EXPORT_DIR,
                     filename)


def _create_html_file_from_list_of_lists(
        config,
        git_commit,
        title_basename,
        html_filepath,
        list_of_lists,
        report_description: str = LICENSE_WARNING):
    title = '{} for {}'.format(title_basename,
                               path.basename(config.project_root))
    with open_t(html_filepath, mode='w+', newline='') as html_file:
        acf_file = config.acf_file.get_input_filenames_as_string()
        cct_files = ','.join(
            [path.basename(cct) for cct in config.compiler_list])
        rcf_file = config.rcf_file.get_input_filenames_as_string()
        user_messages = config.user_messages.get_input_filenames_as_string()
        html_file.write(
            create_html_from_list_of_lists(title, config.project_root,
                                           git_commit,
                                           config.cli_version_string, acf_file,
                                           rcf_file, cct_files, user_messages,
                                           list_of_lists, report_description))
        LOGGER.info('State html summary written to %s', html_filepath)


def _get_open_closed_issues_from_all(values, with_full_subdiagnostics):
    aggregated_summary = calculate_aggregated_summary(
        values, with_full_subdiagnostics)
    return [[key, value] for key, value in aggregated_summary.items()]


def get_warning_summary_per_rule_text(values, with_full_subdiagnostics):
    """Get warnings summary per rule text column"""
    column = QAVIEW_TABLE_COLUMN_SEVERITY_LEVEL_INFO_INDEX
    resulted_dict = aggregate_warnings_summary_per_entity(
        values, column, with_full_subdiagnostics)
    return [[key, value] for key, value in resulted_dict.items()]


def get_warning_summary_per_producer_component(values,
                                               with_full_subdiagnostics):
    """Get warning summary per producer component column"""
    column = QAVIEW_TABLE_COLUMN_IDS_INDEX
    resulted_dict = aggregate_warnings_summary_per_entity(
        values, column, with_full_subdiagnostics)
    return [[key, value] for key, value in resulted_dict.items()]


def _get_info_sheet_rows(config, git_commit):
    baseline_sha256 = "" if not path.exists(
        config.local_baseline_cache_filepath) else calculate_sha256(
            config.local_baseline_cache_filepath)

    return [['License', LICENSE_WARNING],
            ['Date', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
            ['Git Commit', git_commit],
            ['QAC version', config.cli_version_string],
            ['Project root', config.project_root],
            ['ACF', config.acf_file.get_input_filenames_as_string()],
            ['RCF', config.rcf_file.get_input_filenames_as_string()],
            [
                'CCT',
                ','.join([path.basename(cct) for cct in config.compiler_list])
            ],
            [
                'User Messages',
                config.user_messages.get_input_filenames_as_string()
            ], ["Cache Baseline path", config.local_baseline_cache_dir_path],
            ["Local Baseline path", config.local_baseline_path],
            ["Local Baseline sha", baseline_sha256]]


def generate_sheet(exporter, sheet_name, values, enable_filters: bool = False):
    """Creates sheet and appends it rows with provided values"""
    sheet = exporter.create_sheet(sheet_name)
    for rows in values:
        sheet.append_rows(rows)

    if enable_filters:
        sheet.enable_filters()


def export_view_summary(config, csv_values):
    """Converts a qacli view report to a summary of \
    open and total severities"""
    open_closed_issues_from_all = \
        _get_open_closed_issues_from_all(csv_values,
                                         config.with_full_subdiagnostics)
    warning_summary_per_rule_text = \
        get_warning_summary_per_rule_text(csv_values,
                                          config.with_full_subdiagnostics)
    warning_summary_per_producer_component = \
        get_warning_summary_per_producer_component(
            csv_values, config.with_full_subdiagnostics)

    summary_sheet_values = [[CSV_SUMMARY_HEADER], open_closed_issues_from_all,
                            warning_summary_per_rule_text,
                            warning_summary_per_producer_component]
    exporters = _create_exporters(config, 'qacli-view', 'summary')
    for exporter in exporters:
        generate_sheet(exporter,
                       'summary',
                       summary_sheet_values,
                       enable_filters=True)

        exporter.save()

    if config.generate_html:
        csv_values = [CSV_SUMMARY_HEADER]
        csv_values.extend(open_closed_issues_from_all)
        csv_values.extend(warning_summary_per_rule_text)
        csv_values.extend(warning_summary_per_producer_component)

        export_view_html_summary(config, csv_values)


def export_view_html_summary(config, csv_values):
    """Exports qacli-view-summary in HTML format"""
    check_qaview_html_filepath = path.join(config.qac_project_path,
                                           SCA_TOOL_DIR, EXPORT_DIR,
                                           'qacli-view-summary.html')

    with open_t(check_qaview_html_filepath, mode='w+',
                newline='') as check_qaview_html_file:
        acf_file = config.acf_file.get_input_filenames_as_string()
        cct_files = ','.join(
            [path.basename(cct) for cct in config.compiler_list])
        rcf_file = config.rcf_file.get_input_filenames_as_string()
        user_messages = config.user_messages.get_input_filenames_as_string()
        check_qaview_html_file.write(
            create_html_from_list_of_lists("qacli-view-summary",
                                           config.project_root,
                                           config.project_git_commit,
                                           config.cli_version_string,
                                           acf_file,
                                           rcf_file,
                                           cct_files,
                                           user_messages,
                                           csv_values,
                                           report_description=""))
        LOGGER.info('Writing qacli-view-summary html file to %s',
                    check_qaview_html_filepath)


def _convert_state_to_severity_summary(config, git_commit, state_analysis,
                                       summary_details: bool):
    def _get_row_csv_values(files_with_summary, total_sums):
        filepath, file_state = files_with_summary
        row = [
            filepath,
            file_state.get('analysis_error_count'),
            file_state.get('analysis_exit_status'),
            file_state.get('severities_total')
        ]
        # Fills in the analysis_log parts of the file if present
        if file_state.get('analysis_log'):
            analysis_log = file_state.get('analysis_log')
            row.append(','.join([
                '{}:{}'.format(analysis['module'], analysis['analysis_code'])
                for analysis in analysis_log
            ]))
            module_errors = len([
                analysis for analysis in analysis_log
                if analysis['analysis_code'] != '0'
            ])
            row.append(module_errors)
            # Module errors sum
            total_sums[5] += module_errors
        else:
            row.extend(['-', 0])
        row.extend(
            [file_state['severities'][(str(id))] for id in range(0, 10)])
        indices_to_sum = [1, 3]
        indices_to_sum.extend(list(range(6, 16)))
        for i in indices_to_sum:
            total_sums[i] = total_sums[i] + int(row[i])

        return row

    headers = [
        'filename', 'analysis_error_count', 'analysis_exit_status',
        'severities_total', 'module_outputs', 'module_error_count'
    ]
    headers.extend(['severity{}'.format(id) for id in range(0, 10)])
    files_with_summary = [(filepath, file_state['summary'])
                          for filepath, file_state in state_analysis.items()
                          if file_state.get('summary')]

    csv_values = [headers]
    total_sums = ['Total', 0, '-', 0, '-', 0]
    total_sums.extend([0] * 10)
    csv_values.extend([
        row for row in map(lambda x: _get_row_csv_values(x, total_sums),
                           files_with_summary) if row
    ])

    # Printing details will require a QAC License and therefore
    # should be avoided in some specific use cases
    report_description = ""
    if summary_details:
        csv_values.insert(1, total_sums)
        report_description = LICENSE_WARNING
    else:
        csv_values = [headers, total_sums]

    summary_sheet_values = [[CSV_SUMMARY_HEADER], csv_values]

    exporters = _create_exporters(config, 'report', 'summary')
    for exporter in exporters:
        generate_sheet(exporter,
                       'summary',
                       summary_sheet_values,
                       enable_filters=True)

        exporter.save()

    if config.generate_html:
        _create_html_file_from_list_of_lists(
            config, git_commit, 'Static Code Analysis Summary Report',
            path.join(config.qac_project_path, SCA_TOOL_DIR, EXPORT_DIR,
                      'report-summary.html'), csv_values, report_description)


def _convert_state_to_file_metrics(config, state_analysis):
    def _get_metrics_data():
        metrics_data = []
        for filepath, file_stats in state_analysis.items():
            if not file_stats.get('submetrics'):
                continue
            metrics_data.extend(
                _get_metrics_data_per_file(filepath,
                                           file_stats.get('submetrics')))

        return metrics_data

    def _get_metrics_data_per_file(filepath, file_submetrics):
        metrics_per_file = []
        for entity in file_submetrics:
            if entity.get('type') and entity.get('metrics'):
                metrics_per_file.extend(
                    _get_metrics_data_per_entity(
                        _get_entity_columns(filepath, entity), entity))

        return metrics_per_file

    def _get_entity_columns(filepath, entity):
        return [
            filepath,
            entity.get('name'),
            entity.get('line'),
            entity.get('type')
        ]

    def _get_metrics_data_per_entity(entity_columns, entity):
        metrics_per_enitity = []
        for metric_name, metric_value in entity['metrics'].items():
            if config.metrics_filter_list and (
                    metric_name not in config.metrics_filter_list):
                continue
            metrics_per_enitity.append(entity_columns +
                                       [metric_name, metric_value])

        return metrics_per_enitity

    def _export_metrics_report(csv_values):
        metrics_sheet_values = [csv_values]
        exporters = _create_exporters(config, 'report', 'metrics')
        for exporter in exporters:
            generate_sheet(exporter,
                           'metrics',
                           metrics_sheet_values,
                           enable_filters=True)

            exporter.save()

    if config.metrics_filter_list:
        LOGGER.info('Applying metrics filter to the metrics report')

    csv_values = [_METRICS_CSV_HEADER]
    if config.codeowners_file:
        LOGGER.info('Adding Team/Component information to the metrics report')
        component_mapper = ComponentMapper(config.codeowners_file)
        csv_values[0].extend(TEAM_REPORT_EXTRA_FIELDNAMES)
        csv_values.extend(
            add_team_components_to_row(metric_row,
                                       _METRICS_CSV_HEADER.index('path'),
                                       component_mapper, config.only_last_team)
            for metric_row in _get_metrics_data() if metric_row)
    else:
        csv_values.extend(_get_metrics_data())

    if len(csv_values) > 1:
        _export_metrics_report(csv_values)
    else:
        LOGGER.warning('State report does not contain metrics information. '
                       'Generate state report using "-wm"/"--with_metrics" '
                       'flag or "WITH_METRICS" parameter to include metrics')


def _convert_state_to_file_analysis(config, git_commit, state_analysis):
    def _get_formatted_source_root(source_root):
        filepath = source_root['filepath']
        line = source_root['line']
        column = source_root['column']
        producer = source_root['producer']
        msgnum = source_root['padmsgnum']

        return f'{filepath}:{line}:{column}:{producer}:{msgnum}'

    def _get_subdiagnostic_origins_for_finding(finding):
        sub_findings = finding['sub_findings'].copy()
        source_roots = []

        source_root = sub_findings.pop(0)

        while sub_findings:
            if source_root['id'] not in sub_findings[0]['id']:
                source_roots.append(
                    _get_formatted_source_root(source_root))
            source_root = sub_findings.pop(0)

        source_roots.append(_get_formatted_source_root(source_root))

        return source_roots

    def _get_list_of_findings(findings):
        result_findings = []

        for finding in findings:
            current_findings = [finding]

            if config.with_full_subdiagnostics:
                for sub_finding in finding['sub_findings']:
                    current_findings.append(sub_finding)
            elif config.with_subdiagnostics:
                current_findings = []
                subdiagnostic_origins = []
                if finding['sub_findings']:
                    subdiagnostic_origins = \
                        _get_subdiagnostic_origins_for_finding(finding)
                _finding = finding
                _finding['origins'] = ' '.join(subdiagnostic_origins)
                current_findings.append(_finding)

            result_findings.extend(current_findings)

        return result_findings

    def _get_row_csv_values(file_with_findings):
        findings = file_with_findings

        def _convert_finding_to_rows(finding):
            def _compose_producer_with_msgnum(finding):
                return [
                    finding.get('producer') + ':' + finding.get('padmsgnum')
                ]

            if not finding:
                return None

            row = [finding['filepath']]
            for element in diagnostic_xml_elements:
                if element == 'producer':
                    row.extend(_compose_producer_with_msgnum(finding))
                elif element == 'padmsgnum':
                    pass
                else:
                    row.extend([finding.get(element)])

            return row

        return [
            finding for finding in map(_convert_finding_to_rows, findings)
            if finding
        ]

    diagnostic_xml_elements = DIAG_XML_ELEMENTS
    if config.with_full_subdiagnostics:
        diagnostic_xml_elements.extend(SUBDIAG_XML_ELEMENTS_FULL)
    elif config.with_subdiagnostics:
        diagnostic_xml_elements.extend(SUBDIAG_XML_ELEMENTS)

    files_with_findings = [
        _get_list_of_findings(state_analysis[key]['findings'])
        for key in state_analysis if state_analysis[key].get('findings')
    ]
    csv_values = [DEPRECATED_CSV_HEADER_WITH_FILENAME]
    if config.with_full_subdiagnostics:
        csv_values[0].extend(SUBDIAG_CSV_HEADER_FULL)
    elif config.with_subdiagnostics:
        csv_values[0].extend(SUBDIAG_CSV_HEADER)

    if config.codeowners_file:
        LOGGER.info('Adding Team/Component information to the qacli-view '
                    'report')
        component_mapper = ComponentMapper(config.codeowners_file)
        csv_values[0].extend(TEAM_REPORT_EXTRA_FIELDNAMES)
        csv_values.extend([
            add_team_components_to_row(subrow,
                                       QAVIEW_TABLE_COLUMN_FILENAME_INDEX,
                                       component_mapper, config.only_last_team)
            for row in map(_get_row_csv_values, files_with_findings) if row
            for subrow in row if subrow
        ])
    else:
        for row in map(_get_row_csv_values, files_with_findings):
            csv_values.extend(row)

    export_analysis_report(config, git_commit, csv_values)
    export_view_summary(config, csv_values)


def export_analysis_report(config, git_commit, csv_values):
    """Creates analysis files for qacli-view"""
    info_sheet_rows = _get_info_sheet_rows(config, git_commit)
    open_closed_issues_from_all = \
        _get_open_closed_issues_from_all(csv_values,
                                         config.with_full_subdiagnostics)
    warning_summary_per_rule_text = \
        get_warning_summary_per_rule_text(csv_values,
                                          config.with_full_subdiagnostics)
    warning_summary_per_producer_component = \
        get_warning_summary_per_producer_component(
            csv_values, config.with_full_subdiagnostics)

    info_sheet_values = [info_sheet_rows]
    summary_sheet_values = [[CSV_SUMMARY_HEADER], open_closed_issues_from_all,
                            warning_summary_per_rule_text,
                            warning_summary_per_producer_component]
    view_sheet_values = [csv_values]

    exporters = _create_exporters(config, 'qacli', 'view')
    for exporter in exporters:
        # Info sheet
        generate_sheet(exporter, 'info', info_sheet_values)

        # Summary sheet
        generate_sheet(exporter,
                       'summary',
                       summary_sheet_values,
                       enable_filters=True)

        # View sheet
        generate_sheet(exporter,
                       'view',
                       view_sheet_values,
                       enable_filters=True)

        exporter.save()


def export_reports(config, summary_details: bool = True):
    """Export State information to CSV and HTML"""
    LOGGER.info('Reading state file with path %s', config.state_filepath)
    with ZipFile(config.state_filepath) as state_zip_file:
        with state_zip_file.open('state.json') as state_file:
            state = json.loads(state_file.read())
            state_analysis = state.get('analysis')

            if not state_analysis:
                LOGGER.error('No analysis in state file found. Exiting')
                log_and_exit(RC_CONFIG_PARSING_ERROR)

            git_commit = state.get('git_commit')
            _convert_state_to_severity_summary(config, git_commit,
                                               state_analysis, summary_details)
            if config.codeowners_file:
                LOGGER.warning(SENSITIVE_INFO_WARNING_MESSAGE)
            if config.with_metrics:
                _convert_state_to_file_metrics(config, state_analysis)
            _convert_state_to_file_analysis(config, git_commit, state_analysis)


def aggregate_warnings_summary_per_entity(values, entity,
                                          with_full_subdiagnostics):
    """Aggregate warnings summary per entity"""
    def _get_value_or_zero_in_dict_from_name(a_dict: dict, lookup_name: str):
        value = a_dict.get(lookup_name)
        return value if value else 0

    warning_active_dict = {}
    warning_total_dict = {}
    warning_dict = {}

    for row in values[1:]:
        if with_full_subdiagnostics and _is_subdiagnostic(row):
            continue

        for warning in row[entity].split(','):
            warning_total_dict[warning] = \
                warning_total_dict.get(warning, 0) + 1
            if row[QAVIEW_TABLE_COLUMN_SUPPRESSION_FLAG_INDEX] == \
                BITMASK_ACTIVE:
                warning_active_dict[warning] = \
                    warning_active_dict.get(warning, 0) + 1

    for warning_name in warning_total_dict:
        total_number_of_warning_names = f"{warning_name} total"
        active_number_of_warning_names = f"{warning_name} active"

        warning_active_dict_number = _get_value_or_zero_in_dict_from_name(
            warning_active_dict, warning_name)
        warning_total_dict_number = _get_value_or_zero_in_dict_from_name(
            warning_total_dict, warning_name)

        LOGGER.debug("%s: %s", "total_number_of_warning_names",
                     f"{total_number_of_warning_names}")
        LOGGER.debug("%s: %s", f"warning_total_dict[{warning_name}]",
                     f"{warning_total_dict_number}")
        LOGGER.debug("%s: %s", "active_number_of_warning_names",
                     f"{active_number_of_warning_names}")
        LOGGER.debug("%s: %s", f"warning_active_dict[{warning_name}]",
                     f"{warning_active_dict_number}")

        warning_dict.update(
            {f"{active_number_of_warning_names}": warning_active_dict_number})
        warning_dict.update(
            {f"{total_number_of_warning_names}": warning_total_dict_number})
    return warning_dict
