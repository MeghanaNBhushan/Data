# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	stdout_sheet.py
# ----------------------------------------------------------------------------
"""StdOut sheet implementation"""

from swq.common.export.sheet import Sheet


class StdOutSheet(Sheet):
    """Defines a stdout_sheet instance"""
    def __init__(self, title: str, row_formatter):
        super().__init__(title)
        self._sheet = []
        self._row_formatter = row_formatter

    def append(self, row: list):
        """Appends a row to the sheet"""
        self._sheet.append(row)

    def print(self):
        """Prints all the information from sheet"""
        for row in self._sheet[1:]:
            formatted_string = self._row_formatter(row)
            print(formatted_string)
