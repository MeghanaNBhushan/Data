# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	spreadsheet_exporter.py
# ----------------------------------------------------------------------------
"""Defines a spreadsheet exporter interface"""


class SpreadsheetExporter:
    """Defines a spreadsheet exporter interface"""

    _dirpath = None
    _filename = None

    def __init__(self, dirpath, filename):
        self._dirpath = dirpath
        self._filename = filename

    def create_sheet(self, title: str):
        """Creates a sheet to be exported"""

    def save(self):
        """Saves the exporting state"""
