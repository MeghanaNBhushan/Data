# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	sheet.py
# ----------------------------------------------------------------------------
"""Defines a single sheet container interface"""


class Sheet:
    """Defines a single sheet interface"""
    def __init__(self, title):
        self._title = title

    def append(self, row: list):
        """Appends a row to the sheet"""

    def append_rows(self, rows: list):
        """Appends a set of rows to the sheet"""
        for row in rows:
            self.append(row)

    def enable_filters(self):
        """Enables filters for this sheet if supported by the implementation"""

    @property
    def title(self):
        """Gets the sheet title"""
        return self._title

    def save(self):
        """Saves the sheet state"""
