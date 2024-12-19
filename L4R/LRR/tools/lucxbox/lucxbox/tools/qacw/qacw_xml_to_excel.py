"""
QAC XML to XLSX Converter
"""
import sys
import os
import xlsxwriter

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.qacw import qacw_xml

LOGGER = lucxlog.get_logger()


def main(args):
    LOGGER.setLevel(args.log_level)

    args.output = os.path.abspath(args.output)

    if len(args.output.split('.')) == 1:
        LOGGER.info("No file extension found. Adding 'xlsx'.")
        args.output += '.xlsx'

    args.input = os.path.abspath(args.input)

    LOGGER.info("Reading QAC XML file '%s'", args.input)
    qac_severity_files = qacw_xml.get_severity_files_from_xml(args.input)

    if args.severity_levels:
        LOGGER.info("Severity levels to extract given.")
        qac_severity_files = qacw_xml.get_files_with_severity_levels(qac_severity_files, args.severity_levels)
        for qac_severity_file in qac_severity_files:
            qac_severity_file.filter_findings(args.severity_levels)

    LOGGER.info("Found '%s' files with given severity level violations", str(len(qac_severity_files)))

    LOGGER.info("Writing information to Excel file '%s'", args.output)

    if args.guess_component_name:
        LOGGER.info("Component name guessing activated.")

    write_excel(qac_severity_files, args.output, args.guess_component_name, args.excel_layout)


def write_excel(severity_files, excel_file, guess_component_name, layout):
    """ Writes a set of severity files to a given path of excel file

        WARNING: Target excel file will be overwritten if not locked!

        Keyword arguments:
        severity_files -- A list of SeverityFiles to export as an excel file
        excel_file -- ideally absolute path to the excel file to write results to.
        guess_component_name -- Whether to guess the component name out of the file path or not
        layout -- The layout to export the excel, either 'list' or 'matrix'
    """
    excel_workbook = xlsxwriter.Workbook(excel_file)
    excel_format_bold = excel_workbook.add_format({'bold': True})
    excel_worksheet = excel_workbook.add_worksheet('QAC++ Overview')

    if layout is not None and layout == 'matrix':
        set_matrix_layout(excel_worksheet, excel_format_bold)
        fill_matrix_layout(excel_worksheet, severity_files, guess_component_name)
    else:
        set_list_layout(excel_worksheet, excel_format_bold)
        fill_list_layout(excel_worksheet, severity_files, guess_component_name)

    excel_workbook.close()


def set_matrix_layout(excel_worksheet, bold_format):
    """ Setting the excel layout to be a matrix with columns for the number of severity level findings
        And columns containing file/component entries

        Keyword arguments:
        excel_worksheet -- The excel worksheet object to modify
        bold_format -- The workbook format for formatting something as bold
    """
    excel_worksheet.set_column('A:A', 30)
    excel_worksheet.set_column('B:B', 20)
    excel_worksheet.set_column('C:C', 20)
    excel_worksheet.set_column('D:D', 20)
    excel_worksheet.set_column('E:E', 20)
    excel_worksheet.set_column('F:F', 20)
    excel_worksheet.set_column('G:G', 20)
    excel_worksheet.set_column('H:H', 20)
    excel_worksheet.set_column('I:I', 20)
    excel_worksheet.set_column('J:J', 20)
    excel_worksheet.set_column('K:K', 20)
    excel_worksheet.write('A1', 'Component', bold_format)
    excel_worksheet.write('B1', 'Level 9', bold_format)
    excel_worksheet.write('C1', 'Level 8', bold_format)
    excel_worksheet.write('D1', 'Level 7', bold_format)
    excel_worksheet.write('E1', 'Level 6', bold_format)
    excel_worksheet.write('F1', 'Level 5', bold_format)
    excel_worksheet.write('G1', 'Level 4', bold_format)
    excel_worksheet.write('H1', 'Level 3', bold_format)
    excel_worksheet.write('I1', 'Level 2', bold_format)
    excel_worksheet.write('J1', 'Level 1', bold_format)
    excel_worksheet.write('K1', 'Level 0', bold_format)


def fill_matrix_layout(excel_worksheet, severity_files, guess_component_name):
    """ Filling the matrix excel layout with severity file findings

        Keyword arguments:
        excel_worksheet -- The worksheet object to be filled with context
        severity_files -- A list of SeverityFiles to export as an excel file
        excel_file -- ideally absolute path to the excel file to write results to.
        guess_component_name -- Whether to guess the component name out of the file path or not
    """
    excel_current_row = 1  # because 0 were the headings

    for severity_file in severity_files:
        component = severity_file.path
        if severity_file.component is not None and guess_component_name:
            component = severity_file.component

        excel_worksheet.write(excel_current_row, 0, component)

        for severity in range(1, 10):
            file_severities = severity_file.count_severity(10 - severity)
            excel_worksheet.write(excel_current_row, severity, file_severities)

        excel_current_row += 1


def set_list_layout(excel_worksheet, bold_format):
    """ Setting the list excel layout which where a row contains one finding for one file
        and columns are severity level, active, total and the message.
        Therefore a file can have several row entries -- for every finding one

        Keyword arguments:
        excel_worksheet -- The excel worksheet object to modify
        bold_format -- The workbook format for formatting something as bold
    """
    excel_worksheet.set_column('A:A', 40)
    excel_worksheet.set_column('B:B', 10)
    excel_worksheet.set_column('C:C', 20)
    excel_worksheet.set_column('D:D', 20)
    excel_worksheet.set_column('E:E', 100)
    excel_worksheet.write('A1', 'Component', bold_format)
    excel_worksheet.write('B1', 'Severity', bold_format)
    excel_worksheet.write('C1', 'Occurrences (active)', bold_format)
    excel_worksheet.write('D1', 'Occurrences (total)', bold_format)
    excel_worksheet.write('E1', 'Text', bold_format)


def fill_list_layout(excel_worksheet, severity_files, guess_component_name):
    """ Fills the list layout with severity files findings accordingly

        Keyword arguments:
        excel_worksheet -- The worksheet object to be filled with context
        severity_files -- A list of SeverityFiles to export as an excel file
        excel_file -- ideally absolute path to the excel file to write results to.
        guess_component_name -- Whether to guess the component name out of the file path or not
    """
    excel_current_row = 1  # because 0 were the headings

    for severity_file in severity_files:
        component = severity_file.path
        if severity_file.component is not None and guess_component_name:
            component = severity_file.component

        for finding in severity_file.get_all_findings():
            excel_worksheet.write(excel_current_row, 0, component)
            excel_worksheet.write(excel_current_row, 1, finding.severity)
            excel_worksheet.write(excel_current_row, 2, finding.active_occurrences)
            excel_worksheet.write(excel_current_row, 3, finding.occurrences)
            excel_worksheet.write(excel_current_row, 4, finding.message)
            excel_current_row += 1
