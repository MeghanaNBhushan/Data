# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	stdout_exporter.py
# ----------------------------------------------------------------------------
"""Defines a stdout exporter"""

from swq.common.export.stdout_sheet import StdOutSheet


def default_row_formatter(row: list):
    """stdout default row formatter"""
    return ','.join(
        ['"' + str(item).replace('\"', '\'') + '"' for item in row])


class StdOutExporter:
    """Defines a stdout exporter"""
    def __init__(self, row_formatter=default_row_formatter):
        self._sheets = []
        self._row_formatter = row_formatter

    def set_formatter(self, row_formatter):
        """Setter for row_formatter field"""
        self._row_formatter = row_formatter

    def create_sheet(self, title: str):
        """Creates a sheet to be exported"""
        sheet = StdOutSheet(title, self._row_formatter)
        self._sheets.append(sheet)

        return sheet

    def save(self):
        """Saves the exporting state"""
        for sheet in self._sheets:
            sheet.print()
