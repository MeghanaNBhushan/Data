# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: export_analysis.py
# ----------------------------------------------------------------------------
"""Export analysis results and generate project state"""

from swq.common.report.report import Report, ReportExporter
from swq.qac.state.utils import create_state_file, read_state
from swq.qac.state.report.analysis import create_analysis_dataframe
from swq.qac.state.report.metrics import create_metrics_dataframe
from swq.qac.state.report.summary import create_summary_dataframe, \
    create_summary_per_file_dataframe
from swq.qac.state.report.info import create_info_dataframe


def qac_export_analysis(config):
    """Entrypoint for export_analysis command"""
    if config.from_state_file:
        state_content = read_state(config.from_state_file)
    else:
        state_content = create_state_file(config)

    if config.with_metrics:
        report_name = 'metrics'
        metrics_report = Report(report_name)
        metrics_report.dataframe = create_metrics_dataframe(
            config, state_content)

        metrics_exporter = _create_report_exporter(config, report_name)
        metrics_exporter.add_report(metrics_report)
        metrics_exporter.save()

    report_name = 'qacli-view'
    analysis_exporter = _create_report_exporter(config, report_name)
    if config.with_analysis or config.with_summary:
        info_report = _create_info_report(state_content)
        analysis_exporter.add_report(info_report)
        analysis_report = _create_analysis_report(config, state_content)

    if config.with_analysis:
        analysis_exporter.add_report(analysis_report)

    if config.with_summary:
        summary_report = _create_summary_report(analysis_report)
        analysis_exporter.add_report(summary_report)

        report_name = 'report-summary'
        summary_exporter = _create_report_exporter(config, report_name)
        summary_per_file_report = _create_summary_per_file_report(
            state_content)
        summary_exporter.add_report(summary_per_file_report)
        summary_exporter.save()

    analysis_exporter.save()


def _create_info_report(state_content):
    info_report = Report('info')
    info_report.with_header = False
    info_report.css_classes = ['info']
    info_report.dataframe = create_info_dataframe(state_content)

    return info_report


def _create_analysis_report(config, state_content):
    analysis_report = Report('analysis')
    analysis_report.dataframe = create_analysis_dataframe(
        config, state_content)

    return analysis_report


def _create_summary_report(analysis_report):
    summary_report = Report('summary')
    summary_report.dataframe = create_summary_dataframe(
        analysis_report.dataframe)

    return summary_report


def _create_summary_per_file_report(state_content):
    summary_per_file_report = Report('report-summary')
    summary_per_file_report.dataframe = create_summary_per_file_dataframe(
        state_content)

    return summary_per_file_report


def _create_report_exporter(config, name):
    report_exporter = ReportExporter(name)
    report_exporter.set_export_dir(config.reports_path)
    report_exporter.set_export_formats(config.export_formats)

    return report_exporter
