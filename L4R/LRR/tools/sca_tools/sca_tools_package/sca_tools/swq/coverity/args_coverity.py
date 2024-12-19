# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: args_coverity.py
# ----------------------------------------------------------------------------
"""The argument parser for the coverity helper"""

from swq.common.args.args_utils import add_bool_arg_unified, \
    add_common_config_args, map_teams_common_configurable_args


def parse_args_coverity(helper_sub, params, entrypoints):
    """
    Parses coverity subcommand arguments

    :param helper_sub: SWQ SCA Tools argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    coverity_parser = helper_sub.add_parser('coverity',
                                            help=params.get_description())
    coverity_subparser = coverity_parser.add_subparsers(
        title=params.get_subparser_description())

    parse_args_coverity_create(coverity_subparser, params, entrypoints)
    parse_args_coverity_check_buildlog(coverity_subparser, params, entrypoints)
    parse_args_coverity_analyze(coverity_subparser, params, entrypoints)
    parse_args_coverity_run_desktop(coverity_subparser, params, entrypoints)
    parse_args_coverity_export(coverity_subparser, params, entrypoints)
    parse_args_coverity_export_analysis(coverity_subparser, params,
                                        entrypoints)
    parse_args_coverity_preview_report(coverity_subparser, params, entrypoints)
    parse_args_coverity_upload(coverity_subparser, params, entrypoints)
    parse_args_coverity_webapi_export(coverity_subparser, params, entrypoints)
    parse_args_coverity_filter_report(coverity_subparser, params, entrypoints)

    coverity_parser.set_defaults(entrypoint='coverity', parser=coverity_parser)


def add_coverity_common_args(subparser, params):
    """
    Parse swq.common arguments for helper subcommands

    :param subparser: argument parser
    :param params: object of CommandParameters class
    """
    add_common_config_args(subparser, params)

    subparser.add_argument(params.COVERITY_BIN_PATH.flag_short,
                           params.COVERITY_BIN_PATH.flag_long,
                           help=params.COVERITY_BIN_PATH.description)

    subparser.add_argument(params.COVERITY_PROJECT_PATH.flag_short,
                           params.COVERITY_PROJECT_PATH.flag_long,
                           help=params.COVERITY_PROJECT_PATH.description)


def parse_args_coverity_create(coverity_subparser, params, entrypoints):
    """
    Parse arguments for coverity 'create' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'create'
    parser_coverity_create = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_coverity_common_args(parser_coverity_create, params)

    parser_coverity_create.add_argument(
        params.COMPILE_COMMANDS_JSON.flag_short,
        params.COMPILE_COMMANDS_JSON.flag_long,
        help=params.COMPILE_COMMANDS_JSON.description)

    parser_coverity_create.add_argument(
        params.FILE_MATCHING_PATTERNS.flag_short,
        params.FILE_MATCHING_PATTERNS.flag_long,
        nargs='+',
        help=params.FILE_MATCHING_PATTERNS.description)

    parser_coverity_create.add_argument(params.BUILD_COMMAND.flag_short,
                                        params.BUILD_COMMAND.flag_long,
                                        help=params.BUILD_COMMAND.description)

    parser_coverity_create.add_argument(
        params.COMPILE_COMMANDS_BUILD_COMMAND.flag_short,
        params.COMPILE_COMMANDS_BUILD_COMMAND.flag_long,
        help=params.COMPILE_COMMANDS_BUILD_COMMAND.description)

    parser_coverity_create.add_argument(
        params.INPUT_FILE_MATCHING_PATTERNS.flag_short,
        params.INPUT_FILE_MATCHING_PATTERNS.flag_long,
        help=params.INPUT_FILE_MATCHING_PATTERNS.description)

    add_bool_arg_unified(parser_coverity_create,
                         params.SKIP_EXIT_ON_ERROR.flag_short,
                         params.SKIP_EXIT_ON_ERROR.flag_long,
                         msg=params.SKIP_EXIT_ON_ERROR.description)

    add_bool_arg_unified(parser_coverity_create,
                         params.USE_COMPILE_COMMANDS_JSON.flag_short,
                         params.USE_COMPILE_COMMANDS_JSON.flag_long,
                         msg=params.USE_COMPILE_COMMANDS_JSON.description)

    parser_coverity_create.add_argument(
        params.MAXIMUM_PARALLEL_WORKERS.flag_short,
        params.MAXIMUM_PARALLEL_WORKERS.flag_long,
        help=params.MAXIMUM_PARALLEL_WORKERS.description)

    parser_coverity_create.set_defaults(func=entrypoints['coverity_create'],
                                        subcommand=command_name)


def parse_args_coverity_check_buildlog(coverity_subparser, params,
                                       entrypoints):
    """
    Parse arguments for coverity 'check_buildlog' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'check_buildlog'
    parser_coverity_check_buildlog = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_coverity_common_args(parser_coverity_check_buildlog, params)

    parser_coverity_check_buildlog.set_defaults(
        func=entrypoints['coverity_check_buildlog'], subcommand=command_name)


def parse_args_coverity_analyze(coverity_subparser, params, entrypoints):
    """
    Parse arguments for coverity 'analyze' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'analyze'
    parser_coverity_analyze = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_coverity_common_args(parser_coverity_analyze, params)

    parser_coverity_analyze.set_defaults(func=entrypoints['coverity_analyze'],
                                         subcommand=command_name)


def parse_args_coverity_run_desktop(coverity_subparser, params, entrypoints):
    """
    Parse arguments for coverity 'run_desktop' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'run_desktop'
    parser_coverity_run_desktop = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_coverity_common_args(parser_coverity_run_desktop, params)

    parser_coverity_run_desktop.add_argument(
        params.COVERITY_AUTH_KEY_FILEPATH.flag_short,
        params.COVERITY_AUTH_KEY_FILEPATH.flag_long,
        help=params.COVERITY_AUTH_KEY_FILEPATH.description)

    parser_coverity_run_desktop.add_argument(
        params.COVERITY_CONFIG_FILEPATH.flag_short,
        params.COVERITY_CONFIG_FILEPATH.flag_long,
        help=params.COVERITY_CONFIG_FILEPATH.description)

    parser_coverity_run_desktop.set_defaults(
        func=entrypoints['coverity_run_desktop'],
        subcommand=command_name)


def parse_args_coverity_export(coverity_subparser, params, entrypoints):
    """
    Parse arguments for coverity 'export' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'export'
    parser_coverity_export = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_coverity_common_args(parser_coverity_export, params)
    coverity_export_formats_args(parser_coverity_export, params)

    add_bool_arg_unified(
        parser_coverity_export,
        params.COVERITY_WITH_NATIVE_HTML_REPORT.flag_short,
        params.COVERITY_WITH_NATIVE_HTML_REPORT.flag_long,
        msg=params.COVERITY_WITH_NATIVE_HTML_REPORT.description)

    map_teams_common_configurable_args(parser_coverity_export, params)

    parser_coverity_export.set_defaults(func=entrypoints['coverity_export'],
                                        subcommand=command_name)


def parse_args_coverity_export_analysis(coverity_subparser, params,
                                        entrypoints):
    """
    Parse arguments for coverity 'export_analysis' helper subcommand
    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'export_analysis'
    parser_coverity_export_analysis = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_coverity_common_args(parser_coverity_export_analysis, params)

    add_bool_arg_unified(parser_coverity_export_analysis,
                         params.WITH_CID.flag_short,
                         params.WITH_CID.flag_long,
                         msg=params.WITH_CID.description)

    parser_coverity_export_analysis.set_defaults(
        func=entrypoints['coverity_export_analysis'], subcommand=command_name)


def parse_args_coverity_preview_report(coverity_subparser, params,
                                       entrypoints):
    """
    Parse arguments for coverity 'preview_report' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'preview_report'
    parser_coverity_preview_report = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_coverity_common_args(parser_coverity_preview_report, params)
    parser_coverity_preview_report.add_argument(
        params.COVERITY_AUTH_KEY_FILEPATH.flag_short,
        params.COVERITY_AUTH_KEY_FILEPATH.flag_long,
        help=params.COVERITY_AUTH_KEY_FILEPATH.description)

    coverity_export_formats_args(parser_coverity_preview_report, params)

    map_teams_common_configurable_args(parser_coverity_preview_report, params)

    parser_coverity_preview_report.set_defaults(
        func=entrypoints['coverity_preview_report'], subcommand=command_name)


def parse_args_coverity_upload(coverity_subparser, params, entrypoints):
    """
    Parse arguments for coverity 'upload' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'upload'
    parser_coverity_upload = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_coverity_common_args(parser_coverity_upload, params)
    parser_coverity_upload.add_argument(
        params.COVERITY_AUTH_KEY_FILEPATH.flag_short,
        params.COVERITY_AUTH_KEY_FILEPATH.flag_long,
        help=params.COVERITY_AUTH_KEY_FILEPATH.description)

    parser_coverity_upload.set_defaults(func=entrypoints['coverity_upload'],
                                        subcommand=command_name)


def parse_args_coverity_webapi_export(coverity_subparser, params, entrypoints):
    """
    Parse arguments for coverity 'webapi_export' helper subcommand

    :param coverity_subparser: subparser for coverity argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'webapi_export'
    parser_coverity_webapi_export = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_coverity_common_args(parser_coverity_webapi_export, params)
    coverity_export_formats_args(parser_coverity_webapi_export, params)

    add_bool_arg_unified(parser_coverity_webapi_export,
                         params.INCLUDE_TRIAGE_HISTORY.flag_short,
                         params.INCLUDE_TRIAGE_HISTORY.flag_long,
                         msg=params.INCLUDE_TRIAGE_HISTORY.description)

    parser_coverity_webapi_export.set_defaults(
        func=entrypoints['coverity_webapi_export'], subcommand=command_name)


def parse_args_coverity_filter_report(coverity_subparser, params, entrypoints):
    """
    Parse arguments for qac 'filter_report' helper subcommand

    :param preview_report_csv: path to qaview export
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    command_name = 'filter_report'
    parser_coverity_filter_report = coverity_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_coverity_common_args(parser_coverity_filter_report, params)

    parser_coverity_filter_report.add_argument(
        params.PREVIEW_REPORT_CSV.flag_short,
        params.PREVIEW_REPORT_CSV.flag_long,
        help=params.PREVIEW_REPORT_CSV.description)

    parser_coverity_filter_report.add_argument(
        params.FILTER_REPORT_OUTPUT_FILE.flag_short,
        params.FILTER_REPORT_OUTPUT_FILE.flag_long,
        help=params.FILTER_REPORT_OUTPUT_FILE.description)

    parser_coverity_filter_report.set_defaults(
        func=entrypoints['coverity_filter_report'], subcommand=command_name)


def coverity_export_formats_args(subparser, params):
    """
    Parse export format arguments in only export related helper subcommands

    :param subparser: argument parser
    :param params: object of CommandParameters class
    """
    subparser.add_argument(
        params.EXPORT_FORMATS.flag_short,
        params.EXPORT_FORMATS.flag_long,
        help=params.EXPORT_FORMATS.description,
        nargs='+',
        choices=['xlsx', 'csv', 'csv_zip', 'stdout', 'vscode', 'all'])
