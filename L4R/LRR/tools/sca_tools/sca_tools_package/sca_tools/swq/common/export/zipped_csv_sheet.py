# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	zipped_csv_sheet.py
# ----------------------------------------------------------------------------
"""Zipped csv sheet implementation"""

from os import path
from io import StringIO
from zipfile import ZipFile, ZIP_DEFLATED
from swq.common.logger import LOGGER
from swq.common.export.sheet import Sheet
from swq.common.export.csv_sheet import _create_csv_writer


class ZippedCsvSheet(Sheet):
    """Defines a single csv sheet instance"""
    def __init__(self, basepath, title: str):
        super().__init__(title)
        if title:
            self.__csv_filepath = '{}-{}.zip'.format(basepath, title)
        else:
            self.__csv_filepath = '{}.zip'.format(basepath)
        self.__csv_file = ZipFile(self.__csv_filepath,
                                  mode='w',
                                  compression=ZIP_DEFLATED)
        self.__csv_string_buffer = StringIO()
        self.__csv_writer = _create_csv_writer(self.__csv_string_buffer)
        LOGGER.info('Creating zipped csv sheet in path %s',
                    self.__csv_filepath)

    def append(self, row: list):
        """Appends a row to the csv"""
        self.__csv_writer.writerow(row)

    def append_rows(self, rows: list):
        """Appends rows to the csv"""
        self.__csv_writer.writerows(rows)

    def save(self):
        """Saves the csv state"""
        csv_filename = \
            path.basename(self.__csv_filepath).replace('.zip', '.csv')
        self.__csv_file.writestr(csv_filename,
                                 self.__csv_string_buffer.getvalue())
        self.__csv_string_buffer.close()
        self.__csv_file.close()
