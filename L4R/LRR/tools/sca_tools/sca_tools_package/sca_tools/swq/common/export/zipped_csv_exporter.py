# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	zipped_csv_exporter.py
# ----------------------------------------------------------------------------
"""Defines a zipped csv exporter implementation"""

from os import path
from swq.common.export.zipped_csv_sheet import ZippedCsvSheet
from swq.common.export.spreadsheet_exporter import SpreadsheetExporter


class ZippedCsvExporter(SpreadsheetExporter):
    """Defines a csv format exporter"""
    def __init__(self, filepath):
        super().__init__(path.dirname(filepath), path.basename(filepath))
        self.__sheets = []
        self.__filepath = filepath

    def create_sheet(self, title: str):
        """Create a csv sheet"""
        result = ZippedCsvSheet(self.__filepath, title)
        self.__sheets.append(result)

        return result

    def save(self):
        """Saves the csv state"""
        for sheet in self.__sheets:
            sheet.save()
        return self.__filepath
