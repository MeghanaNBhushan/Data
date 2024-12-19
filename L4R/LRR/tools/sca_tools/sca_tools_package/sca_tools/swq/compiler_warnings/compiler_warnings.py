# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: compiler_warnings.py
# ----------------------------------------------------------------------------
""" Creates compiler warnings report with the possibility to export in several
formats."""

import importlib
import json
import os
import pathlib

from collections import Counter
from sys import exit as sys_exit

import pandas as pd

from swq.common.config.common_config import \
    check_if_filepath_exists_and_exit_if_not
from swq.common.filesystem.filesystem_utils import open_t, \
    get_files_with_extensions, safe_delete_dirtree
from swq.common.logger import LOGGER
from swq.common.return_codes import RC_FINDINGS_LARGER_THAN_THRESHOLD, \
    RC_COMPILER_UNSUPPORTED
from swq.compiler_warnings import compiler_warning
from swq.compiler_warnings.warning_type import load_warnings_db
from swq.map_teams.map_teams import map_teams_components_in_dataframe, \
    TEAM_COLUMN_NAME, COMPONENT_COLUMN_NAME

_COMPILER_WARNINGS_CSV_HEADER = [
    'File path', 'File name', 'Row', 'Column', 'Components', 'Team', 'Message',
    'Severity', 'Type', 'Number of occurrences'
]
_COMPILER_WARNINGS_DF_COLUMNS = _COMPILER_WARNINGS_CSV_HEADER + ['Domain']
_COMPILER_WARNINGS_JSON_DF_COLUMNS = [
    'File path', 'Row', 'Column', 'Message', 'Components', 'Team', 'Severity',
    'Type', 'Number of occurrences', 'Domain'
]
_COMPILER_WARNINGS_JSON_KEYS = [
    'file_path', 'row', 'column', 'message', 'components', 'teams', 'severity',
    'type_name', 'quantity', 'domain'
]


def prepare_project(config):
    """
    Makes project directories preparation/cleanup
    """
    # Always creates the directory structure to avoid path problems
    safe_delete_dirtree(config.report_dir)
    os.makedirs(config.report_dir)


def filter_warnings(warnings):
    """
    Filter warnings
    """
    warnings_num = Counter(warnings)
    for warning, occurrence in zip(warnings_num.keys(), warnings_num.values()):
        warning.set_quantity(occurrence)
    return list(warnings_num.keys())


def filter_warnings_for_directories(warnings, tokens):
    """
    Filter warnings for directories
    """
    LOGGER.debug("Filtering warnings for directory: '%s'", ",".join(tokens))
    target_warnings = []
    for warning in warnings:
        for token in tokens:
            if token in warning.file_path.replace("\\", "/"):
                target_warnings.append(warning)
                break
    return target_warnings


def set_warning_info_from_types_db(warnings, db_file):
    """
    Set warning attributes based on warnings db
    """
    types_db = load_warnings_db(db_file)
    for warning in [w for w in warnings if w.has_type_name()]:
        if warning.type_name in types_db:
            warning.severity = types_db[warning.type_name].severity
        elif "-W" + warning.type_name in types_db:
            warning.severity = types_db["-W" + warning.type_name].severity
    return warnings


def print_all_warnings(warnings):
    """
    Prints the given warning list to the screen as a CSV representation
    """
    LOGGER.info('All Compiler warnings')
    for warning in warnings:
        components = ','.join(warning.teams)
        message = warning.message
        to_print = ';'.join([
            warning.file_path,
            str(warning.row), components,
            str(message),
            str(warning.type_name)
        ])
        if to_print != '.;;;;':
            LOGGER.info(to_print)


def get_file_name_path_mapping(root):
    """
    Return a directory with the file and file path mapping from the given root
    """
    source_files = get_files_with_extensions(root, ['.cpp', '.c'])
    mapping = {}
    for source_file in source_files:
        mapping[pathlib.Path(source_file).stem] = source_file
    return mapping


def warning_name_amount(warnings, name):
    """
    Counts warnings amount of a certain warning name in the given warnings list
    """
    amount = 0
    for warning in warnings:
        if warning.type_name == name:
            amount += 1
    return amount


def check_warnings_thresholds(threshold_file, warnings):
    """
    Method to cross-check the given warning list against a warnings threshold
    file, which can specify thresholds for every warning type.
    Note that this is only supported if the warning type can be extracted from
    the compiler log and is supported by the compiler regex

    Arguments:
    threshold_file - the threshold file, which is a JSON
    warnings - the warnings list with entries of the type CompilerWarning
    """
    overflow_amount = 0

    LOGGER.debug("Reading thresholds JSON file '%s'", threshold_file)
    with open_t(threshold_file) as tfile:
        thresholds = json.load(tfile)
    LOGGER.debug(thresholds)

    specified_warning_thresholds = []

    for threshold in thresholds:
        warning_name = threshold['warning_name']
        specified_warning_thresholds.append(warning_name)
        threshold_value = threshold['threshold']
        if threshold_value == -1:
            LOGGER.warning(
                "Warning '%s' has unlimited threshold and appears '%d' times",
                warning_name, warning_name_amount(warnings, warning_name))
            continue
        overflow = warning_name_amount(warnings,
                                       warning_name) - threshold_value
        if overflow > 0:
            LOGGER.error(
                "Threshold of warning '%s' is exceeded by '%d' warnings.",
                warning_name, overflow)
            overflow_amount += overflow
        else:
            LOGGER.debug(
                "Warning '%s' has a threshold buffer of '%d' warnings.",
                warning_name, abs(overflow))

    printed_warning = []
    for warning in warnings:
        if warning.type_name and warning.type_name not in printed_warning \
            and warning.type_name not in specified_warning_thresholds:
            LOGGER.warning(
                "Warning '%s' was not specified in threshold but appears"
                "'%d' times", warning.type_name,
                warning_name_amount(warnings, warning.type_name))
            printed_warning.append(warning.type_name)

    if overflow_amount > 0:
        LOGGER.error(
            "Accumulated warning threshold was exceeded by '%d' warnings.",
            overflow_amount)
        sys_exit(RC_FINDINGS_LARGER_THAN_THRESHOLD)


def read_changed_files(changed_files_files):
    """
    Read changed files and define if the warnings relate to changes
    """
    changed_files = {}
    for changed_files_file in changed_files_files:
        LOGGER.debug("Reading changed files from '%s'",
                     os.path.abspath(changed_files_file))
        with open_t(changed_files_file) as cff:
            lines = cff.read().splitlines()

        for line in lines:
            if ',' in line:
                splitted = line.split(',')
                filename = splitted[0]
                warning_lines = []
                for warning_line in splitted[1:]:
                    if warning_line:
                        warning_lines.append(int(warning_line))
                if warning_lines:
                    changed_files[filename] = warning_lines
                else:
                    LOGGER.warning(
                        "The file '%s' does only contain removed lines",
                        filename)
                    changed_files[filename] = [-1]
            else:
                changed_files[line.strip()] = []

    LOGGER.info("Extracted '%d' changed files", len(changed_files))
    return changed_files


def check_changed_files_warnings(changed_files, warnings, output_file):
    """
    Filter warnings basing on changed files list passed
    """
    relevant_warnings = []
    for warning in warnings:
        if warning.file_path in changed_files:
            LOGGER.debug("Found file '%s' with warnings in the changed files",
                         warning.file_path)
            if not changed_files[warning.file_path]:
                LOGGER.debug("Changed file has no changed line infos -> ADD")
                relevant_warnings.append(warning)
            elif int(warning.row) in changed_files[warning.file_path]:
                LOGGER.debug(
                    "Line '%d' was changed and contains a warning -> ADD",
                    warning.row)
                relevant_warnings.append(warning)
            else:
                LOGGER.debug("Warning not introduced by changes -> SKIP")

    report = ('\n' + 20 * '-' + '\n').join(map(str, relevant_warnings))
    if output_file:
        with open_t(output_file, 'w') as output:
            output.write(report)
    else:
        LOGGER.info(report)

    if relevant_warnings:
        LOGGER.warning("The changed files introduced new warnings!")

    return relevant_warnings


def export_to_file(config, warnings):
    """
    Export analysis results to the requested formats
    """
    warnings_data = [[
        warning.file_path,
        os.path.basename(warning.file_path), warning.row, warning.column,
        warning.components if warning.components else '',
        warning.teams if warning.teams else '', warning.message,
        warning.severity, warning.type_name, warning.quantity, warning.domain
    ] for warning in warnings]
    warnings_dataframe = pd.DataFrame.from_records(
        warnings_data, columns=_COMPILER_WARNINGS_DF_COLUMNS)
    if config.codeowners_file:
        LOGGER.debug("Trying to set components from file '%s'",
                     config.codeowners_file)
        map_teams_components_in_dataframe(warnings_dataframe,
                                          TEAM_COLUMN_NAME,
                                          COMPONENT_COLUMN_NAME, config)

    if 'xlsx' in config.export_formats:
        xlsx_report = os.path.abspath(
            os.path.join(config.report_dir,
                         f'{config.report_basename}.xlsx'))
        LOGGER.info('Writing Compiler Warnings XLSX report to %s', xlsx_report)
        warnings_dataframe.to_excel(xlsx_report,
                                    index=False,
                                    columns=_COMPILER_WARNINGS_CSV_HEADER)

    if 'csv' in config.export_formats:
        csv_report = os.path.abspath(
            os.path.join(config.report_dir,
                         f'{config.report_basename}.csv'))
        LOGGER.info('Writing Compiler Warnings CSV report to %s', csv_report)
        warnings_dataframe.to_csv(csv_report,
                                  mode='w',
                                  index=False,
                                  columns=_COMPILER_WARNINGS_CSV_HEADER)

    if 'json' in config.export_formats:
        json_report = os.path.abspath(
            os.path.join(config.report_dir,
                         f'{config.report_basename}.json'))
        warnings_dataframe = warnings_dataframe.reindex(
            columns=_COMPILER_WARNINGS_JSON_DF_COLUMNS)
        warnings_dataframe.columns = _COMPILER_WARNINGS_JSON_KEYS
        LOGGER.info('Writing Compiler Warnings JSON report to %s', json_report)
        warnings_dataframe.to_json(json_report, orient="records")


def black_list_filter(black_list, warnings):
    """
    Filter warnings by black list
    """
    for path in black_list:
        for loc, warning in enumerate(warnings):
            if path in str(warning):
                warnings[loc] = (compiler_warning.CompilerWarning(
                    "", "", None, "", "", ''))

    return warnings


def compiler_warnings(config):
    """
    Produces compiler warnings reports based on compiler log
    """
    prepare_project(config)
    try:
        compiler_lib_name = '.' + config.compiler
        LOGGER.debug("Trying to load compiler implementation file '%s.py'",
                     config.compiler)
        compiler_lib = importlib.import_module(
            compiler_lib_name, package='swq.compiler_warnings.compilers')
    except ImportError:
        LOGGER.error(
            "Compiler '%s' is not supported yet (Cannot include '%s.py')",
            config.compiler, config.compiler)
        sys_exit(RC_COMPILER_UNSUPPORTED)

    compiler = compiler_lib.Compiler()

    filemapping = get_file_name_path_mapping(config.project_root)
    warnings = compiler.get_warnings_from_file(config.compiler_log,
                                               config.jobs, filemapping)
    warnings = filter_warnings(warnings)

    if config.target_directory and config.project_root:
        tokens = [config.target_directory]
        if isinstance(config.target_directory, list):
            tokens = config.target_directory
        for i, element in enumerate(tokens):
            tokens[i] = element.replace(config.project_root,
                                        "").replace("\\", "/")
        warnings = filter_warnings_for_directories(warnings, tokens)

    if config.types_db:
        warnings = set_warning_info_from_types_db(
            warnings, os.path.abspath(config.types_db))

    if config.changed_files:
        changed_files = read_changed_files(config.changed_files)
        warnings = check_changed_files_warnings(changed_files, warnings,
                                                config.output)

    if config.black_list:
        for black_list_file in config.black_list:
            check_if_filepath_exists_and_exit_if_not(
                config.get_parameter_name('BLACK_LIST'), black_list_file)
            with open(black_list_file) as blist:
                path_list = blist.read()
                path_list = path_list.split('\n')
            warnings = black_list_filter(path_list, warnings)

    print_all_warnings(warnings)

    export_to_file(config, warnings)

    if config.threshold:
        threshold = int(config.threshold)
        LOGGER.debug("Using overall threshold value of '%d'", threshold)
        if threshold < len(warnings):
            exceed_warnings = len(warnings) - threshold
            if exceed_warnings > 0:
                LOGGER.error(
                    "Threshold of '%d' was exceeded by '%d' warnings.",
                    threshold, exceed_warnings)
                sys_exit(RC_FINDINGS_LARGER_THAN_THRESHOLD)

    if config.threshold_file:
        check_warnings_thresholds(os.path.abspath(config.threshold_file),
                                  warnings)
