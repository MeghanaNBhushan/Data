# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: reports_exporter.py
# ----------------------------------------------------------------------------
"""Find_includes reports exporter"""

from swq.common.export.xlsx_exporter import XlsxExporter


def _get_mapping_report(mapped_files_dict):
    return [[header, '\n'.join(compilation_units)]
            for header, compilation_units in mapped_files_dict.items()]


def export_mapping_report(report_file, mapped_files_dict):
    """Generated xlsx report with mapping of
    header and compilation unit files"""
    exporter = XlsxExporter(report_file)
    summary_sheet = exporter.create_sheet('summary')
    summary_sheet.append_rows([['header', 'compilation unit']])
    summary_sheet.append_rows(_get_mapping_report(mapped_files_dict))
    summary_sheet.enable_filters()
    exporter.wrap_text_in_cells()
    return exporter.save()
