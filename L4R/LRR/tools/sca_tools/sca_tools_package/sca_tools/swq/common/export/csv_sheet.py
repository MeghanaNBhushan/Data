# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	csv_sheet.py
# ----------------------------------------------------------------------------
"""Csv sheet implementation"""

import csv

from swq.common.logger import LOGGER
from swq.common.export.sheet import Sheet
from swq.common.filesystem.filesystem_utils import open_t


def _create_csv_writer(csv_file):
    return csv.writer(csv_file,
                      delimiter=',',
                      quotechar='"',
                      quoting=csv.QUOTE_NONNUMERIC)


class CsvSheet(Sheet):
    """Defines a single csv sheet instance"""
    def __init__(self, basepath, title: str):
        super().__init__(title)
        if title:
            self.__csv_filepath = '{}-{}.csv'.format(basepath, title)
        else:
            self.__csv_filepath = '{}.csv'.format(basepath)
        self.__csv_file = open_t(self.__csv_filepath, mode='w+', newline='')
        self.__csv_writer = _create_csv_writer(self.__csv_file)
        LOGGER.info('Creating csv sheet in path %s', self.__csv_filepath)

    def append(self, row: list):
        """Appends a row to the csv"""
        self.__csv_writer.writerow(row)

    def append_rows(self, rows: list):
        """Appends rows to the csv"""
        self.__csv_writer.writerows(rows)

    def save(self):
        """Saves the csv state"""
        self.__csv_file.close()
