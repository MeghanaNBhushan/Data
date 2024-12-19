# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: report.py
# ----------------------------------------------------------------------------
"""Defines report and report exporter classes"""

from os import path
import pandas as pd
from jinja2 import FileSystemLoader, Environment

from swq.common.filesystem.filesystem_utils import open_t
from swq.common.logger import LOGGER
from swq.common.report.constants import REPORT_HTML_TEMPLATES_PATH, \
    REPORT_HTML_TEMPLATE_FILENAME


class Report:
    """Class that holds information of a generated report"""
    def __init__(self, name):
        self._title = name
        self._dataframe = None
        self._with_header = True
        self._css_classes = ['report']

    @property
    def title(self):
        """Gets the property title"""
        return self._title

    @property
    def dataframe(self):
        """Gets the property dataframe"""
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        """Sets the property dataframe"""
        self._dataframe = value

    @property
    def with_header(self):
        """Gets the property with_header"""
        return self._with_header

    @with_header.setter
    def with_header(self, value: bool):
        """Sets the property with_header"""
        self._with_header = value

    @property
    def css_classes(self):
        """Gets the property css_classes"""
        return self._css_classes

    @css_classes.setter
    def css_classes(self, value: list):
        """Sets the property css_classes"""
        self._css_classes = value


class ReportExporter:
    """Class that holds methods for a report export"""
    def __init__(self, name):
        """Initializes ReportExporter class"""
        self._name = name
        self._export_dir = None
        self._export_formats = None
        self._reports = []

    def add_report(self, report):
        """Adds report to the exporter"""
        self._reports.append(report)

    def to_csv(self, zipped=False):
        """Exports report in CSV ot ZIPPED CSV format.
        Each report added to exporter creates separate file"""
        for report in self._reports:
            self._export_csv(report, zipped)

    def to_xlsx(self):
        """Exports report in XLSX format.
        Each report added to exporter creates separate sheet respectively"""
        file_format = '.xlsx'
        export_filename = self._name + file_format
        export_filepath = path.join(self._export_dir, export_filename)
        # https://github.com/PyCQA/pylint/issues/3060
        # pylint: disable=abstract-class-instantiated
        writer = pd.ExcelWriter(export_filepath, engine='openpyxl')
        self._add_reports_as_xlsx_sheets(writer)
        writer.save()
        _print_export_success_message(self._name, file_format, export_filepath)

    def to_html(self):
        """Exports report in HTML format.
        Each report added to exporter creates separate HTML file"""
        for report in self._reports:
            file_format = '.html'
            html_filepath = self._get_export_filepath(report, file_format)
            html_table = _get_html_table(report)
            html_template = _load_html_template(REPORT_HTML_TEMPLATE_FILENAME,
                                                REPORT_HTML_TEMPLATES_PATH)
            rendered_html = html_template.render(title=report.title,
                                                 tables=[html_table])
            _write_to_file(html_filepath, rendered_html)
            _print_export_success_message(self._name, file_format,
                                          html_filepath)

    def _export_csv(self, report, zipped=False):
        file_format = '.zip' if zipped else '.csv'
        csv_filename = self._get_export_filename(report, '.csv')
        filepath = self._get_export_filepath(report, file_format)
        report.dataframe.to_csv(filepath,
                                index=False,
                                header=report.with_header,
                                compression=_get_compression_options(
                                    csv_filename, zipped))
        _print_export_success_message(report.title, file_format, filepath)

    def _get_export_filename(self, report, file_format):
        if len(self._reports) > 1:
            return f'{self._name}-{report.title}{file_format}'

        return f'{report.title}{file_format}'

    def _get_export_filepath(self, report, file_format):
        filename = self._get_export_filename(report, file_format)

        return path.join(self._export_dir, filename)

    def _add_reports_as_xlsx_sheets(self, xlsx_writer):
        for report in self._reports:
            _add_xlsx_sheet(report, xlsx_writer)

    def _export(self):
        """Exports report"""
        for export_format in self._export_formats:
            if export_format == 'csv':
                self.to_csv()

            if export_format == 'csv_zip':
                self.to_csv(zipped=True)

            if export_format == 'xlsx':
                self.to_xlsx()

            if export_format == 'html':
                self.to_html()

    def set_export_dir(self, value):
        """Sets the export directory"""
        self._export_dir = value

    def set_export_formats(self, value):
        """Sets the export formats"""
        self._export_formats = value

    def save(self):
        """Saves report"""
        if self._reports:
            self._export()


def _get_html_table(report):
    return report.dataframe.to_html(index=False,
                                    header=report.with_header,
                                    classes=report.css_classes)


def _load_html_template(template_filename, templates_dir):
    template_loader = FileSystemLoader(searchpath=templates_dir)
    template_env = Environment(loader=template_loader)

    return template_env.get_template(template_filename)


def _write_to_file(filepath, content):
    with open_t(filepath, mode='w') as open_file:
        open_file.write(content)


def _add_xlsx_sheet(report, writer):
    report.dataframe.to_excel(writer,
                              sheet_name=report.title,
                              index=False,
                              header=report.with_header)
    # Enables auto filtering
    writer.sheets[report.title].auto_filter.ref = \
        writer.sheets[report.title].dimensions


def _get_compression_options(csv_file, zipped):
    return dict(method='zip', archive_name=csv_file) if zipped else None


def _print_export_success_message(title, file_format, filepath):
    LOGGER.info('Created successfully a %s report in %s format '
                'at %s', title, file_format, filepath)
