""" Helper component for warnings parser. """

import sys
import os
import xlsxwriter

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.compiler_warnings import compiler_warnings_info

LOGGER = lucxlog.get_logger()


def write_excel(excel_file, warnings, count=False, gitignore_mapping=False):
    LOGGER.debug("Preparing to write new excel file '%s'", excel_file)
    excel_workbook = xlsxwriter.Workbook(excel_file)
    excel_format_bold = excel_workbook.add_format({'bold': True})
    warnings_worksheet = excel_workbook.add_worksheet('Warnings')
    set_warnings(warnings_worksheet, excel_format_bold)
    fill_warnings(warnings_worksheet, warnings, gitignore_mapping)
    if count:
        add_count(warnings_worksheet, warnings, excel_format_bold)

    add_info(excel_workbook, excel_format_bold)

    excel_workbook.close()

def add_info(excel_workbook, bold_format):
    date_format = excel_workbook.add_format({'num_format': 'mmm d yyyy hh:mm AM/PM'})
    info_worksheet = excel_workbook.add_worksheet('Info')
    info_worksheet.set_column('A:A', 10)
    info_worksheet.set_column('B:B', 80)
    info_worksheet.write('A1', 'Date', bold_format)
    info_worksheet.write('A2', 'Branch', bold_format)
    info_worksheet.write('A3', 'Commit', bold_format)
    info_worksheet.write('A4', 'Dirty', bold_format)
    info_worksheet.write('A5', 'Arguments', bold_format)
    info_worksheet.write('B1', compiler_warnings_info.get_date(), date_format)
    info_worksheet.write('B2', compiler_warnings_info.get_branch())
    info_worksheet.write('B3', compiler_warnings_info.get_commit())
    info_worksheet.write('B4', compiler_warnings_info.get_dirty())
    info_worksheet.write('B5', compiler_warnings_info.get_call())

def set_warnings(excel_worksheet, bold_format):
    LOGGER.debug("Setting excel sheet layout.")
    excel_worksheet.set_column('A:A', 80)
    excel_worksheet.set_column('B:B', 10)
    excel_worksheet.set_column('C:C', 30)
    excel_worksheet.set_column('D:D', 100)
    excel_worksheet.set_column('E:E', 100)
    excel_worksheet.set_column('F:F', 12)
    excel_worksheet.set_column('G:G', 50)
    excel_worksheet.set_column('H:H', 30)
    excel_worksheet.write('A1', 'File path', bold_format)
    excel_worksheet.write('B1', 'File name', bold_format)
    excel_worksheet.write('C1', 'Row', bold_format)
    excel_worksheet.write('D1', 'Column', bold_format)
    excel_worksheet.write('E1', 'Components', bold_format)
    excel_worksheet.write('F1', 'Team', bold_format)
    excel_worksheet.write('G1', 'Message', bold_format)
    excel_worksheet.write('H1', 'Severity', bold_format)
    excel_worksheet.write('I1', 'Type', bold_format)
    excel_worksheet.write('J1', 'Number of occurrences', bold_format)


def fill_warnings(excel_worksheet, warnings, gitignore_mapping=False):
    excel_current_row = 1  # because 0 were the headings
    LOGGER.debug("Filling excel sheet with warnings.")
    for warning in warnings:
        excel_worksheet.write(excel_current_row, 0, warning.file_path)  # Path
        excel_worksheet.write(excel_current_row, 1, os.path.basename(warning.file_path))  # Name
        excel_worksheet.write(excel_current_row, 2, warning.row)  # Row
        excel_worksheet.write(excel_current_row, 3, warning.column)  # Column

        if warning.has_components:
            if gitignore_mapping:
                excel_worksheet.write(excel_current_row, 4, warning.components[-1] if warning.components else '')
                excel_worksheet.write(excel_current_row, 5, warning.teams[-1] if warning.teams else '')
            else:
                excel_worksheet.write(excel_current_row, 4, ','.join(warning.components))
                excel_worksheet.write(excel_current_row, 5, ','.join(warning.teams))

        excel_worksheet.write(excel_current_row, 6, warning.message)  # Message

        if warning.has_severity():
            excel_worksheet.write(excel_current_row, 7, warning.severity)

        if warning.has_type_name():
            excel_worksheet.write(excel_current_row, 8, warning.type_name)

        if warning.has_quantity():
            excel_worksheet.write(excel_current_row, 9, warning.quantity)

        excel_current_row += 1


def add_count(excel_worksheet, matches, bold_format):
    count = len(matches)
    # because 0 were the headings and we already have one line per warning
    excel_current_row = 1 + count + 2
    excel_worksheet.write(excel_current_row, 0,
                          "Warnings count:", bold_format)  # File
    excel_worksheet.write(excel_current_row, 1,
                          str(count), bold_format)  # File
