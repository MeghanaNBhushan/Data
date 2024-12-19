# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: layout.py
# ----------------------------------------------------------------------------
""" Handles columns related information and transformations
for QAC and Coverity unified reports"""
from swq.common.logger import LOGGER


def _get_reduced_columns(columns, ignore_cols):
    """ Remove all columns which can have different values while merging"""
    merge_columns = list(columns)
    for col in ignore_cols:
        if col in merge_columns:
            merge_columns.remove(col)
    return merge_columns


def _append_new_columns(ignore_columns, new_columns):
    for col in new_columns:
        ignore_columns.append(col)


def remove_duplicates(df_data, ignore_cols):
    """ Ignore some given columns when dropping the duplicates """
    df_data.drop_duplicates(subset=df_data.columns.difference(ignore_cols),
                            inplace=True)


class Column():
    """ Represents a column in the report, defined by name position
    and a methods needed for setting an initial value """
    def __init__(self, name, position, init_method):
        self._name = name
        self._position = position
        self._init_method = init_method

    @property
    def name(self):
        """ Column name """
        return self._name

    @property
    def position(self):
        """ Position of the column in the report table """
        return self._position

    @property
    def init_method(self):
        """ Method for setting an initial value to this column """
        return self._init_method


class Columns():
    """ Base class for unified report columns """
    COL_TEAM = 'Team'
    COL_SOURCES = 'Sources'
    COL_COMPONENTS = 'Components'
    COLS_SUMMARY = ['Alias', 'Filename']
    COL_WIDTHS_SUMMARY = {"Alias": 10, "Filename": 60}
    """ Holds all sort of columns needed for the unified report """
    def __init__(self, columns, merge_columns, new_columns):

        self._original_columns = columns
        self._merge_columns = merge_columns
        self._ignore_columns = _get_reduced_columns(self._original_columns,
                                                    self._merge_columns)
        self._new_columns = new_columns
        _append_new_columns(self._ignore_columns, self.new_columns)

        LOGGER.debug('_original_columns: %s', self._original_columns)
        LOGGER.debug('merge_columns: %s', self._merge_columns)
        LOGGER.debug('ignore_columns: %s', self._ignore_columns)
        LOGGER.debug('new_columns: %s', self._new_columns)

    def _init_source(self, report):
        LOGGER.debug('Initialize column %s', self.COL_SOURCES)
        return report.first_variant.short_name

    @property
    def new_columns(self):
        """ List of columns to be added and filled by aggregation """
        return self._new_columns

    @property
    def original_columns(self):
        """ List of columns from original qacli-view """
        return self._original_columns

    @property
    def merge_columns(self):
        """ List of columns which needs to be equal
        to aggregate two lines of different reports """
        return self._merge_columns

    @property
    def ignore_columns(self):
        """ List of columns which can differ in two warning lines,
        and the lines are aggregated anyway """
        return self._ignore_columns


class CovColumns(Columns):
    """ Contains all columns information for Coverity reports """

    COL_FILENAME = 'strippedMainEventFilePathname'
    COL_MERGEKEY = 'mergeKey'
    COL_COUNT = 'occurrenceCountForMK'
    COL_NUMBER = 'occurrenceNumberInMK'
    COL_CHECKNAME = 'checkerName'
    COL_SUBCATEGORY = 'subcategory'
    COL_TYPE = 'type'
    COL_SUBTYPE = 'subtype'
    COL_CODELANG = 'code-language'
    COL_EXTRA = 'extra'
    COL_DOMAIN = 'domain'
    COL_LANG = 'language'
    COL_LINE = 'mainEventLineNumber'
    COL_DISPNAME = 'functionDisplayName'
    COL_MANGNAME = 'functionMangledName'
    COL_CATEGORY = 'category'
    COL_DESCRIPT = 'categoryDescription'
    COL_CWECAT = 'cweCategory'
    COL_IMPACT = 'impact'
    COL_IMPACTDESC = 'impactDescription'
    COL_SUBCATEFFFECT = 'subcategoryLocalEffect'
    COL_SUBCATDESC = 'subcategoryShortDescription'
    COL_SUBCATDESCLONG = 'subcategoryLongDescription'
    COL_FILENAME_LONG = 'mainEventFilePathname'

    MERGE_COLUMNS = [COL_FILENAME, COL_MERGEKEY]

    NEW_COLUMNS = [Columns.COL_SOURCES]

    COL_WIDTHS_RESULT = {
        COL_FILENAME: 30,
        COL_MERGEKEY: 10,
        Columns.COL_SOURCES: 20,
        COL_COUNT: 10,
        COL_NUMBER: 10,
        COL_CHECKNAME: 30,
        COL_SUBCATEGORY: 20,
        COL_TYPE: 20,
        COL_SUBTYPE: 20,
        COL_CODELANG: 10,
        COL_EXTRA: 15,
        COL_DOMAIN: 10,
        COL_LANG: 10,
        COL_LINE: 10,
        COL_DISPNAME: 20,
        COL_MANGNAME: 20,
        COL_CATEGORY: 20,
        COL_DESCRIPT: 20,
        COL_CWECAT: 10,
        COL_IMPACT: 10,
        COL_IMPACTDESC: 10,
        COL_SUBCATEFFFECT: 20,
        COL_SUBCATDESC: 20,
        COL_SUBCATDESCLONG: 20,
        COL_FILENAME_LONG: 20,
        Columns.COL_TEAM: 20,
        Columns.COL_COMPONENTS: 20
    }

    SORT_COLUMNS = [COL_FILENAME, COL_LINE]

    def __init__(self, columns):
        super().__init__(columns, CovColumns.MERGE_COLUMNS,
                         CovColumns.NEW_COLUMNS)
        self._new_columns = [
            Column(self.COL_SOURCES, self._get_source_position,
                   super()._init_source)
        ]

    def _get_source_position(self):
        return list(self._original_columns).index(self.COL_MERGEKEY) + 1

    def fill_additional_columns(self, report):
        """ Fill additional columns """
        LOGGER.debug(
            'no additional columns except %s avaiable in Coverity report %s',
            self.COL_SOURCES, report.output_filename)


class QacColumns(Columns):
    """ Contains all columns information for QAC reports """

    COL_FILENAME = 'Filename'
    COL_LINE = 'Line number'
    COL_COLUMN = 'Column number'
    COL_PRODUCER = 'Producer component:Message number'
    COL_MSG = 'Message text'
    COL_SEVERITY = 'Severity'
    COL_RULEGROUP = 'Rule Group'
    COL_RULETEXT = 'Rule text'
    COL_DEPTH = 'Depth'
    COL_TEAM = 'Team'
    COL_COMPONENTS = 'Components'
    COL_SUPPRESSION_BITMASK = 'Suppression type bitmask'
    COL_SUPPRESSION_JUSTIFICATION = 'Suppression justification'
    COL_SUPPRESSION_SET = 'Suppression Bitmask Set'
    COL_SOURCES = 'Sources'
    COL_ID = 'Id'

    MERGE_COLUMNS = [
        COL_FILENAME, COL_LINE, COL_COLUMN, COL_PRODUCER, COL_MSG,
        COL_SEVERITY, COL_RULEGROUP, COL_RULETEXT
    ]

    NEW_COLUMNS = [COL_SOURCES, COL_SUPPRESSION_SET]

    COL_WIDTHS_RESULT = {
        COL_FILENAME: 30,
        COL_LINE: 10,
        COL_COLUMN: 10,
        COL_SOURCES: 10,
        COL_PRODUCER: 20,
        COL_MSG: 60,
        COL_SEVERITY: 10,
        COL_RULEGROUP: 20,
        COL_RULETEXT: 30,
        COL_DEPTH: 10,
        COL_TEAM: 30,
        COL_COMPONENTS: 20,
        COL_SUPPRESSION_BITMASK: 10,
        COL_SUPPRESSION_JUSTIFICATION: 10,
        COL_ID: 8,
        COL_SUPPRESSION_SET: 8
    }

    SORT_COLUMNS = [COL_FILENAME, COL_LINE]

    def __init__(self, columns):
        super().__init__(columns, QacColumns.MERGE_COLUMNS,
                         QacColumns.NEW_COLUMNS)
        self._new_columns = [
            Column(self.COL_SOURCES, self._get_source_position,
                   super()._init_source),
            Column(self.COL_SUPPRESSION_SET, self._get_suppression_position,
                   self._init_suppressions)
        ]

    def _get_source_position(self):
        return list(self._original_columns).index(self.COL_COLUMN) + 2

    def _get_suppression_position(self):
        """ Place the supression set (summary of suppressions of all variants)
        right after the column 'Suppression type bitmask' """
        return list(self._original_columns).index(
            self.COL_SUPPRESSION_BITMASK) + 1

    def _init_suppressions(self, report):
        return report.data[self.COL_SUPPRESSION_BITMASK]

    def _fill_suppression_bitmask_set(self, report):
        def _convert(value):
            if isinstance(value, int):
                result = str(value)
            elif isinstance(value, float):
                result = str(value)
            elif ',' in value:
                result = value.replace(' ', '')
                result = result.split(',')
                result = list(set(result))
                result = ', '.join(result)
            else:
                LOGGER.debug(f'value is a other format {value}')
                result = str(value)
            return result

        col1 = self.COL_SUPPRESSION_SET
        col2 = self.COL_SUPPRESSION_BITMASK
        report.data[col1] = report.data[col2].apply(_convert)

    def fill_additional_columns(self, report):
        """ Fill additional columns """
        LOGGER.info('fill suppression bitmask set')
        self._fill_suppression_bitmask_set(report)
