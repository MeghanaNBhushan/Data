# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: unify_reports.py
# ----------------------------------------------------------------------------
""" Creates an unified report for the given qacli-view reports """

from time import time
from os.path import splitext
from pandas import concat, read_csv, DataFrame, ExcelFile

from swq.unify_reports.layout import QacColumns, CovColumns, remove_duplicates
from swq.common.export.dataframe_exporter import DataframeExporter
from swq.common.config.common_config \
    import check_if_filepath_exists_and_exit_if_not
from swq.common.logger import LOGGER


def _print_input_information(config):
    LOGGER.info("Input of unified report file is %s",
                config.unify_report_variant_input)
    LOGGER.info("Result of unified report file is %s",
                config.unify_report_output)
    LOGGER.info("Type of unified report is %s", config.unify_report_type)


def _get_intersection(input_report1, input_report2, merge_cols, ignore_cols):
    def _get_col(row, col):
        """ Convert int to str but preent it from getting 'nan' """
        return str(row[col]).replace('nan', '')

    def _concate(row, col):
        col_x = _get_col(row, col + '_x')
        col_y = _get_col(row, col + '_y')
        result = ''
        if len(col_x) > 0 and len(col_y) > 0:
            result = col_x + '#' + col_y
        elif len(col_x) == 0:
            result = str(col_y)
        elif len(col_y) == 0:
            result = str(col_x)
        return result

    def _condense(df_data):
        """ Find columns which existed in both dataframes
        and are now duplicated.
        Merge there values into a new column with the original name """
        duplicated_columns = set([
            col.replace('_x', '') for col in df_data.columns
            if col.endswith('_x')
        ])

        for col in duplicated_columns:
            df_data[col + '_x'] = df_data[col + '_x'].astype(str)
            df_data[col + '_y'] = df_data[col + '_y'].astype(str)
            df_data[col] = df_data.apply(
                lambda x, column=col: _concate(x, column), axis=1)
            df_data.drop(col + '_x', inplace=True, axis=1)
            df_data.drop(col + '_y', inplace=True, axis=1)
            df_data[col] = df_data[col].astype(str)
        return df_data

    LOGGER.info('warnings in common %s', input_report1.shape[0])
    LOGGER.info('warnings in input  %s', input_report2.shape[0])

    df_common = input_report1.merge(input_report2,
                                    how='inner',
                                    on=merge_cols,
                                    indicator=False)
    if not df_common.empty:
        df_common = _condense(df_common)
    else:
        df_common = DataFrame(columns=merge_cols + ignore_cols)

    remove_duplicates(df_common, ignore_cols)

    rows = df_common.shape[0]
    LOGGER.info('warnings in intersection: %s', rows)

    return df_common


def _get_diff(df_common, df_input_report, variant_name, ignore_cols):
    df_diff = concat([df_common, df_input_report])
    df_diff.drop_duplicates(subset=df_common.columns.difference(ignore_cols),
                            keep=False,
                            inplace=True)
    rows = df_diff.shape[0]
    LOGGER.info(f'warnings only in {variant_name}: {rows}')
    return df_diff


def _get_union(df_common, df_diff, ignore_cols):
    df_union = concat([df_common, df_diff])
    # ignoring the Sources when dropping the duplicates
    df_union.drop_duplicates(subset=df_union.columns.difference(ignore_cols),
                             inplace=True,
                             keep='first')
    rows = df_union.shape[0]
    LOGGER.info('warnings in union: %s', rows)
    return df_union


def _check_consistency(df_all, df_common, df_only_in_common, df_only_in_input):
    rows_common = df_common.shape[0]
    rows_diff1 = df_only_in_common.shape[0]
    rows_diff2 = df_only_in_input.shape[0]
    rows_all = df_all.shape[0]

    rows_all_sum = rows_common + rows_diff1 + rows_diff2
    LOGGER.info('--- check consistency ---')
    LOGGER.info('warnings in common:    %s', rows_common)
    LOGGER.info('warnings in diff1:     %s', rows_diff1)
    LOGGER.info('warnings in diff2:     %s', rows_diff2)
    LOGGER.info('                    _____')
    LOGGER.info('warnings in all:       %s', rows_all)
    LOGGER.info('-------------------------\n')
    assert rows_all == rows_all_sum, 'Merge was not successful'


def _get_dataframe(report_filename):
    _, file_extension = splitext(report_filename)
    LOGGER.info('File extension of output file is %s', file_extension)
    if file_extension == '.zip':
        df_report = read_csv(report_filename,
                             compression='zip',
                             sep=',',
                             quotechar='"')
    elif file_extension == '.csv':
        df_report = read_csv(report_filename, sep=',', quotechar='"')
    elif file_extension == '.xlsx':
        df_report = ExcelFile(report_filename).parse('export')
    else:
        LOGGER.error('Unknown file format, can not read from: %s',
                     report_filename)
        raise ValueError(
            f'Unknown file format, can not read from {report_filename}, \
                supported input file formats are csv and xlsx')
    return df_report


def _save_worksheet(frame_exporter, sheet_name, data, columns_format):
    LOGGER.info('_save_worksheet called')
    frame_exporter.append_dataframe(sheet_name, data)
    frame_exporter.format_columns(sheet_name, columns_format)


class UnifiedReport():
    """ Wrapper object for the unified reports.
    Holds a list of variants, creates a merge of all variants
    based on MERGE_COLUMNS.
    Handles the relevant columns and their formatting. """

    COMBINED_SHEET = 'combined'
    SUMMARY_SHEET = 'summary'

    def __init__(self, variant, variants, output_filename, columns):
        self._output_filename = output_filename

        # take the first dataframe as merge start
        self._first_variant = variant
        self._variants = variants
        self._df_data = self._first_variant.data
        LOGGER.info('Unified report initialized with report %s (%s)',
                    self._first_variant.filename,
                    self._first_variant.short_name)

        self._columns = columns
        self._insert_new_columns_and_init()
        self._df_summary = self._get_variantnames_summary()
        self._frame_exporter = DataframeExporter(self._output_filename)

    def _insert_new_columns_and_init(self):
        """ insert new column with given name at a given
         position and fill it with the given initial value """
        for col in self._columns.new_columns:
            new_column = col.name
            position = col.position()
            initial_value = col.init_method(report=self)
            self._df_data.insert(loc=position,
                                 column=new_column,
                                 value=initial_value)
            self._end_columns = self._df_data.columns

    def _aggregate_sources(self, df_data, variant_name):
        """ all common warnings in intersection append
                the variant_name of df_input_report """
        df_data.Sources = df_data[self._columns.COL_SOURCES].apply(
            lambda x, vn=variant_name:
            (str(x) + ',' + vn).replace('nan,', '').replace('"', ''))

    def create(self, sort_columns):
        """ Creates a unified report by merging all warnings of the same type,
         in the same file and for the same line and column
         having the same message text.
         For all attribute relevant for merging (if similiar than merge)
         see MERGE_COLUMNS"""
        for variant in self._variants:
            LOGGER.info('Input report %s (%s) will be added now',
                        variant.filename, variant.short_name)
            df_input_report = variant.data
            variant_name = variant.short_name

            df_intersect = _get_intersection(self._df_data, df_input_report,
                                             self._columns.merge_columns,
                                             self._columns.ignore_columns)

            self._aggregate_sources(df_intersect, variant_name)

            df_only_in_common = _get_diff(df_intersect, self._df_data,
                                          'common',
                                          self._columns.ignore_columns)
            df_only_in_input = _get_diff(df_intersect, df_input_report,
                                         variant_name,
                                         self._columns.ignore_columns)

            self._aggregate_sources(df_only_in_input, variant_name)

            self._df_data = _get_union(df_intersect, df_only_in_common,
                                       self._columns.ignore_columns)
            self._df_data = _get_union(self._df_data, df_only_in_input,
                                       self._columns.ignore_columns)

            self._df_data = self._df_data.sort_values(by=sort_columns)

            _check_consistency(self._df_data, df_intersect, df_only_in_common,
                               df_only_in_input)
        self._columns.fill_additional_columns(self)
        self._remove_duplicate_entries_from_lists()
        self._reorder_columns(self._end_columns)
        self._df_data.reset_index(inplace=True, drop=True)
        return self._df_data

    def _remove_duplicate_entries_from_lists(self):
        def _remove_duplicates(value):
            if not isinstance(value, str):
                return value
            if '#' in value:
                parts = value.split('#')
                if len(set(parts)) == 1:
                    value = parts[0]
                else:
                    value = value.replace('#', ', ')
            return value

        self._df_data = self._df_data.applymap(_remove_duplicates)

    def _reorder_columns(self, columns):
        self._df_data = self._df_data[columns]

    def _get_variantnames_summary(self):
        df_variantnames = DataFrame(columns=self._columns.COLS_SUMMARY)
        df_variantnames = df_variantnames.append(
            {
                'Alias': self._first_variant.short_name,
                'Filename': self._first_variant.filename
            },
            ignore_index=True)
        for variant in self._variants:
            df_variantnames = df_variantnames.append(
                {
                    'Alias': variant.short_name,
                    'Filename': variant.filename
                },
                ignore_index=True)
        return df_variantnames

    def save(self):
        """ Saves the unified report as csv or xlsx
        depending on the given output filename """
        LOGGER.info('unified report saved')
        if self._output_filename.endswith('csv'):
            self._df_data.to_csv(self._output_filename, index=False)
        elif self._output_filename.endswith('xlsx'):

            # add summary sheet here
            _save_worksheet(self._frame_exporter, self.SUMMARY_SHEET,
                            self._df_summary, self._columns.COL_WIDTHS_SUMMARY)

            LOGGER.debug('Columns of combined sheet: %s',
                         self._df_data.columns)
            _save_worksheet(self._frame_exporter, self.COMBINED_SHEET,
                            self._df_data, self._columns.COL_WIDTHS_RESULT)

    @property
    def summary(self):
        """ Summary dataframe of unified report """
        return self._df_summary

    @property
    def data(self):
        """ Aggergated warnings dataframe of unified report """
        return self._df_data

    @property
    def first_variant(self):
        """ First variant (report) of unified report """
        return self._first_variant

    @property
    def output_filename(self):
        """ Output filename of unified report """
        return self._output_filename

    @property
    def frame_exporter(self):
        """ frame_exporter """
        return self._frame_exporter


class Variants():
    """ Holds a list of variants and creates the variant names,
    inits the unified reports and adds the other variants """
    def __init__(self, config):
        self._list = []
        for line in config.unify_report_variant_input:
            if '=' in line:
                short_name, variant_report_filename = line.split('=')
            else:
                short_name = str(len(self._list))
                variant_report_filename = line
            variant = Variant(variant_report_filename, short_name, config)
            self._list.append(variant)

    def get_unified_report(self, ouput_filename, report_type):
        """ Gets the unified report """
        first_variant = self._list[0]
        variants_to_be_added = self._list[1:]    # all except the first one
        if report_type == 'qac':
            qac_columns = QacColumns(first_variant.data.columns)
            unified_report = UnifiedReport(first_variant, variants_to_be_added,
                                           ouput_filename, qac_columns)
            unified_report.create(QacColumns.SORT_COLUMNS)
        elif report_type == 'cov':
            cov_columns = CovColumns(first_variant.data.columns)
            unified_report = UnifiedReport(first_variant, variants_to_be_added,
                                           ouput_filename, cov_columns)
            unified_report.create(CovColumns.SORT_COLUMNS)

        return unified_report

    @property
    def list(self):
        """ List of variants """
        return self._list


class Variant():
    """ Variant hold a filename of an qacli-view.csv
    and creates the dataframe from it """
    def __init__(self, filename, short_name: str, config):
        self._filename = filename
        assert isinstance(short_name, str), 'Shortname must be a string'
        self._short_name = short_name
        input_param = config.get_parameter_name('UNIFY_REPORT_VARIANT_INPUT')
        LOGGER.info('input_param: %s', input_param)
        input_path = config.get_absolute_path_or_relative_to_project_root(
            filename)
        LOGGER.info('input_path: %s', input_path)
        check_if_filepath_exists_and_exit_if_not(input_param, input_path)
        self._data = _get_dataframe(input_path)

    @property
    def filename(self):
        """ Filename of given qacli_view.csv """
        return self._filename

    @property
    def data(self):
        """ Dataframe derived from qacli_view.csv """
        return self._data

    @property
    def short_name(self):
        """ Variant name used in the Sources column of uified report.
        If given in the input file it is an variant alias,
        otherwise it is the position of the variant in the list """
        return self._short_name


def unify_reports(config):
    """ Entrypoint function for unify_reports functionality """

    start = time()
    _print_input_information(config)

    variants = Variants(config)
    unified_report = variants.get_unified_report(config.unify_report_output,
                                                 config.unify_report_type)
    unified_report.save()

    end = time() - start
    LOGGER.info('report merging took so long: %s', end)

    return unified_report
