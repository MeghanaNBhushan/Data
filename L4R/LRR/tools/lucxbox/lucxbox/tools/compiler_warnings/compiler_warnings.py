""" Parser for compiler output """

import argparse
import importlib
import json
import os
import sys
import pathlib
import typing
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog, component_mapping, portal, finder

from lucxbox.tools.compiler_warnings import compiler_warnings_to_excel, compiler_warnings_to_csv, compiler_warnings_to_json,\
                                            compiler_warning
from lucxbox.tools.compiler_warnings.warning_type import load_warnings_db

LOGGER = lucxlog.get_logger()
def nonempty_str(value: str) -> typing.Optional[str]:
    if len(value) > 0:
        return value
    return None

def parse_args():
    """ Individual ArgumentParser adaptions regarding the script functionality

        Return value:
        ArgumentParser -- parsed arguments object to access given cli arguments
    """
    description = "A Compiler warnings parser with excel export possibilities."
    parser = argparse.ArgumentParser(description=description)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    parser.add_argument('--compiler-log', '-cl', dest='compiler_log', required=True,
                        help='Path to compiler log file to parse the warnings from (globbing is allowed).')
    parser.add_argument('--components-file', '-cf', dest='component_files', nargs='*', required=False,
                        help='Use COMPONENT files to map files to components/teams')
    parser.add_argument('--add-package-info', '-p', dest='add_package_info', required=False,
                        help='Add package and sw layer info when mapping components/teams')
    parser.add_argument('--to-excel', '-te', dest='to_excel',
                        required=False, help='Whether to export the results to excel')
    parser.add_argument('--to-csv', '-tc', dest='to_csv',
                        required=False, help='Whether to export the results to csv')
    parser.add_argument('--to-json', '-tj', dest='to_json',
                        required=False, help='Whether to export the results to json')
    parser.add_argument("--root-directory", "-rd", required=False,
                        help="Path to root of repository to get file list", dest="root_dir")
    parser.add_argument("--target-directory", "-td", required=False, nargs='+',
                        help="List of paths (seperated by space) to include warning only from specified locations", dest="target_dirs")
    parser.add_argument('--compiler', '-c', dest='compiler',
                        required=True, choices=['clang', 'greenhills', 'msvc', 'prqa_exceptions'], help='Compiler')
    parser.add_argument('--types-db', '-tdb', dest='types_db', required=False,
                        help='Compiler warning types database file (json).')
    parser.add_argument('--jobs', '-j', default=4,
                        type=int, help='Number of threads')
    parser.add_argument('--gitignore-mapping', '-g', action='store_true',
                        help='''Switch to enable of team mapping that implements gitignore specification -
                                within one level of precedence, the last matching pattern decides the outcome''')
    parser.add_argument('--changed-files', '-ch', required=False, nargs='+', help='Files containing a list of changed files')
    parser.add_argument('--output', '-o', required=False, help='Output file to log the warnings existing on the changed files')
    parser.add_argument('--use-relative-paths', help='Use relative file paths when mapping components', action='store_true')
    parser.add_argument('--black-list', '-bl', dest='black_list', required=False, nargs='+',
                        help='Mention the black list files for which warnings are not be considered')

    threshold_group = parser.add_mutually_exclusive_group(required=False)
    threshold_group.add_argument('--threshold', '-t', dest='threshold', type=int,
                                 help='Threshold of allowed overall warnings before script returns non-zero exit code')
    threshold_group.add_argument('--threshold-file', '-tf', dest='threshold_file',
                                 help='Threshold file which lists thresholds for each warning name. Threshold file is a json.')
    parser.add_argument('--ignore-type', required=False, type=nonempty_str, default=list(), nargs='+',
                        help='Remove specified warning type from comparison')

    return parser.parse_args()


def filter_warnings(warnings):
    counted_warnings = Counter(warnings)
    for warning, occurrence in zip(counted_warnings.keys(), counted_warnings.values()):
        warning.set_quantity(occurrence)
    return list(counted_warnings.keys())


def filter_warnings_for_directories(warnings, tokens):
    LOGGER.debug("Filtering warnings for directory: '%s'", ",".join(tokens))
    target_warnings = []
    for warning in warnings:
        for token in tokens:
            if token in warning.file_path.replace("\\", "/"):
                target_warnings.append(warning)
                break
    return target_warnings


def set_components_from_file(warnings, component_files, use_relative_paths=False):
    """ Method to do a component mapping of found warnings based on a component file
        and the path of the file where a warning was found.
        Return value:
        A new list of warnings with adapted component attributes if there was a match

        Arguments:
        warnings - The list of compiler warnings with entries of the type CompilerWarning
        component_files - The component files mapper which follows the GitHub CODEOWNERS style,
                          which is basically a wildcard to name mapper
        use_relative_paths - Use relative file paths while mapping components
    """
    LOGGER.debug("Trying to set components from file '%s'", component_files)
    component_mapper = component_mapping.ComponentMapper(component_files, use_relative_paths)
    changed_warnings = []
    for warning in warnings:
        warning.components = component_mapper.get_component_names_for_path(warning.file_path)
        warning.teams = component_mapper.get_teams_for_path(warning.file_path)
        changed_warnings.append(warning)
    return changed_warnings


def set_warning_info_from_types_db(warnings, db_file):
    types_db = load_warnings_db(db_file)
    for warning in [w for w in warnings if w.has_type_name()]:
        if warning.type_name in types_db:
            warning.severity = types_db[warning.type_name].severity
        elif "-W" + warning.type_name in types_db:
            warning.severity = types_db["-W" + warning.type_name].severity
    return warnings


def print_all_warnings(warnings):
    """ Prints the given warning list to the screen as a CSV representation """
    LOGGER.info('All Compiler warnings')
    for warning in warnings:
        components = ','.join(warning.teams)
        message = warning.message
        to_print = ';'.join([warning.file_path, str(warning.row), components, str(message),
                             str(warning.type_name)])
        if to_print != '.;;;;':
            LOGGER.info(to_print)


def get_file_name_path_mapping(root):
    """ Return a directory with the file and file path mapping from the given root """
    with portal.In(root):
        source_files = finder.get_files_with_ending(['.cpp', '.c'])
    mapping = {}
    for source_file in source_files:
        mapping[pathlib.Path(source_file).stem] = source_file
    return mapping


def warning_name_amount(warnings, name):
    """ Counts the warning amount of a certain warning name in the given warnings list """
    amount = 0
    for warning in warnings:
        if warning.type_name == name:
            amount += 1
    return amount


def check_warnings_thresholds(threshold_file, warnings):
    """ Method to cross-check the given warning list against a warnings threshold file,
        which can specify thresholds for every warning type.
        Note that this is only supported if the warning type can be extracted from the compiler
        log and is supported by the compiler regex

        Arguments:
        threshold_file - the threshold file, which is a JSON
        warnings - the warnings list with entries of the type CompilerWarning
    """
    overflow_amount = 0
    if not os.path.exists(threshold_file):
        LOGGER.critical(
            "Given threshold file '%s' does not exist", threshold_file)
        sys.exit(1)

    LOGGER.debug("Reading thresholds JSON file '%s'", threshold_file)
    with open(threshold_file, 'r') as tfile:
        thresholds = json.load(tfile)
    LOGGER.debug(thresholds)

    specified_warning_thresholds = []

    for threshold in thresholds:
        warning_name = threshold['warning_name']
        specified_warning_thresholds.append(warning_name)
        threshold_value = threshold['threshold']
        if threshold_value == -1:
            LOGGER.warning("Warning '%s' is chosen to have an unlimited threshold and appears '%d' times",
                           warning_name, warning_name_amount(warnings, warning_name))
            continue
        overflow = warning_name_amount(
            warnings, warning_name) - threshold_value
        if overflow > 0:
            LOGGER.error(
                "Threshold of warning '%s' is exceeded by '%d' warnings.", warning_name, overflow)
            overflow_amount += overflow
        else:
            LOGGER.debug(
                "Warning '%s' has a threshold buffer of '%d' warnings.", warning_name, abs(overflow))

    printed_warning = []
    for warning in warnings:
        if warning.type_name not in printed_warning:
            if warning.type_name and warning.type_name not in specified_warning_thresholds:
                LOGGER.warning("Warning '%s' was not specified in threshold but appears '%d' times",
                               warning.type_name, warning_name_amount(warnings, warning.type_name))
                printed_warning.append(warning.type_name)

    if overflow_amount > 0:
        LOGGER.error(
            "Accumulated warning threshold was exceeded by '%d' warnings.", overflow_amount)

    sys.exit(overflow_amount)


def read_changed_files(changed_files_files):
    changed_files = {}
    for changed_files_file in changed_files_files:
        LOGGER.debug("Reading changed files from '%s'", os.path.abspath(changed_files_file))
        with open(changed_files_file, 'r') as cff:
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
                    LOGGER.warning("The file '%s' does only contain removed lines", filename)
                    changed_files[filename] = [-1]
            else:
                changed_files[line.strip()] = []

    LOGGER.info("Extracted '%d' changed files", len(changed_files))
    return changed_files


def check_changed_files_warnings(changed_files, warnings, output_file):
    relevant_warnings = []
    for warning in warnings:
        if warning.file_path in changed_files:
            LOGGER.debug("Found file '%s' with warnings in the changed files", warning.file_path)
            if not changed_files[warning.file_path]:
                LOGGER.debug("Changed file has no changed line infos -> ADD")
                relevant_warnings.append(warning)
            elif int(warning.row) in changed_files[warning.file_path]:
                LOGGER.debug("Line '%d' was changed and contains a warning -> ADD", warning.row)
                relevant_warnings.append(warning)
            else:
                LOGGER.debug("Warning not introduced by changes -> SKIP")

    report = ('\n' + 20 * '-' + '\n').join(map(str, relevant_warnings))
    if output_file:
        with open(output_file, 'w') as output:
            output.write(report)
    else:
        print(report)

    if relevant_warnings:
        LOGGER.warning("The changed files introduced new warnings!")

    return relevant_warnings



def export_to_file(args, warnings):
    if args.to_excel:
        compiler_warnings_to_excel.write_excel(os.path.abspath(args.to_excel), warnings,
                                               gitignore_mapping=args.gitignore_mapping)

    if args.to_csv:
        compiler_warnings_to_csv.write_csv(os.path.abspath(args.to_csv), warnings, args.gitignore_mapping, args.add_package_info)

    if args.to_json:
        compiler_warnings_to_json.write_json(os.path.abspath(args.to_json), warnings)


def black_list_filter(black_list, warnings):
    for path in black_list:
        for loc, warning in enumerate(warnings):
            if path in str(warning):
                warnings[loc] = (compiler_warning.CompilerWarning
                                 ("",
                                  "",
                                  None,
                                  "",
                                  "",
                                  ''
                                 )
                                )

    return warnings

def filter_by_types(ignore_type, warnings):
        """ Filter out specific warning types

        Args:
          types: list of type strings to filter out
        """
        result=[]
        types_upper = [t.upper() for t in ignore_type]
        for warning in warnings:
            if (warning.type_name is None) or (warning.type_name.upper() not in types_upper):
                result.append(warning)
        return result

# pylint: disable=too-many-branches
def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)

    try:
        compiler_lib_name = '.compiler_' + args.compiler
        LOGGER.debug("Trying to load compiler implementation file '%s.py'", compiler_lib_name)
        compiler_lib = importlib.import_module(compiler_lib_name, package='lucxbox.tools.compiler_warnings')
    except ImportError:
        LOGGER.critical(
            "Compiler '%s' not supported yet (Cannot include 'compiler_%s.py')", args.compiler, args.compiler)
        sys.exit(-1)

    compiler = compiler_lib.Compiler()
    if args.root_dir:
        filemapping = get_file_name_path_mapping(args.root_dir)
    else:
        filemapping = {}
    warnings = compiler.get_warnings_from_file(args.compiler_log, args.jobs, filemapping)
    warnings = filter_warnings(warnings)

    if args.target_dirs and args.root_dir:
        tokens = [args.target_dirs]
        if isinstance(args.target_dirs, list):
            tokens = args.target_dirs
        for i, element in enumerate(tokens):
            tokens[i] = element.replace(args.root_dir, "").replace("\\", "/")
        warnings = filter_warnings_for_directories(warnings, tokens)

    if args.component_files is not None:
        warnings = set_components_from_file(warnings, args.component_files, args.use_relative_paths)

    if args.types_db:
        warnings = set_warning_info_from_types_db(warnings, os.path.abspath(args.types_db))

    if args.black_list:
        for black_list_file in args.black_list:
            with open(black_list_file) as blist:
                path_list = blist.read()
                path_list = path_list.split('\n')
            warnings = black_list_filter(path_list, warnings)

    if args.changed_files:
        changed_files = read_changed_files(args.changed_files)
        warnings = check_changed_files_warnings(changed_files, warnings, args.output)
    
    if args.ignore_type:
        warnings = filter_by_types(args.ignore_type, warnings)

    print_all_warnings(warnings)

    export_to_file(args, warnings)

    if (args.threshold or args.threshold == 0):
        LOGGER.debug("Using overall threshold value of '%d'", args.threshold)
        if args.threshold < len(warnings):
            exceed_warnings = len(warnings) - args.threshold
            if exceed_warnings > 0:
                LOGGER.error("Threshold of '%s' was ecxeeded by '%s' warnings.",
                             str(args.threshold), str(exceed_warnings))
                sys.exit(1)

    if args.threshold_file:
        check_warnings_thresholds(
            os.path.abspath(args.threshold_file), warnings)


if __name__ == "__main__":
    main()
