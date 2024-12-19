# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	xlsx_sheet.py
# ----------------------------------------------------------------------------
"""Xslx sheet implementation"""

from swq.common.export.sheet import Sheet


class XlsxSheet(Sheet):
    """Defines a single xslx sheet instance"""
    def __init__(self, worksheet, title: str):
        super().__init__(title)
        self.__worksheet = worksheet
        self.__worksheet.title = title

    def append(self, row: list):
        """Appends a row to the sheet"""
        self.__worksheet.append(row)

    def enable_filters(self):
        """Enables filters for this sheet"""
        self.__worksheet.auto_filter.ref = self.__worksheet.dimensions
