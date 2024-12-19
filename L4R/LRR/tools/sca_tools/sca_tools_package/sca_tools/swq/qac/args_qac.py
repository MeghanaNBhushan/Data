# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: args_qac.py
# -----------------------------------------------------------------------------
"""The argument subparser for the qac command of the QAC"""

from swq.common.args.args_utils import add_bool_arg_unified, \
    add_common_config_args, map_teams_common_configurable_args


def parse_args_qac(helper_sub, params, entrypoints):
    """ Parses qac subcommand arguments """
    qac_parser = helper_sub.add_parser('qac', help=params.get_description())
    qac_subparser = qac_parser.add_subparsers(
        title=params.get_subparser_description())

    parse_args_qac_create(qac_subparser, params, entrypoints)
    parse_args_qac_create_baseline(qac_subparser, params, entrypoints)
    parse_args_qac_analyze(qac_subparser, params, entrypoints)
    parse_args_qac_report(qac_subparser, params, entrypoints)
    parse_args_qac_gui(qac_subparser, params, entrypoints)
    parse_args_qac_qavupload(qac_subparser, params, entrypoints)
    parse_args_qac_s101gen(qac_subparser, params, entrypoints)
    parse_args_qac_state(qac_subparser, params, entrypoints)
    parse_args_qac_export_state(qac_subparser, params, entrypoints)
    parse_args_qac_fix_cl_json(qac_subparser, params, entrypoints)
    parse_args_qac_filter_qaview(qac_subparser, params, entrypoints)
    parse_args_qac_export_analysis(qac_subparser, params, entrypoints)

    qac_parser.set_defaults(entrypoint='qac', parser=qac_parser)


def add_qac_common_args(subparser, params):
    """
    Parse swq.common arguments for helper subcommands

    :param subparser: argument parser
    """
    add_common_config_args(subparser, params)

    subparser.add_argument(params.QAC_BIN_PATH.flag_short,
                           params.QAC_BIN_PATH.flag_long,
                           help=params.QAC_BIN_PATH.description)

    subparser.add_argument(params.QAC_CONFIG_PATH.flag_short,
                           params.QAC_CONFIG_PATH.flag_long,
                           nargs='+',
                           help=params.QAC_CONFIG_PATH.description)

    subparser.add_argument(params.QAC_PROJECT_PATH.flag_short,
                           params.QAC_PROJECT_PATH.flag_long,
                           help=params.QAC_PROJECT_PATH.description)

    subparser.add_argument(params.QAC_LOGGING_LEVEL.flag_short,
                           params.QAC_LOGGING_LEVEL.flag_long,
                           help=params.QAC_LOGGING_LEVEL.description,
                           choices=['NONE', 'ERROR', 'INFO', 'DEBUG', 'TRACE'])


def qac_export_formats_args(subparser, params):
    """
    Parse export formats arguments in only export related helper subcommands

    :param subparser: argument parser
    """
    subparser.add_argument(params.EXPORT_FORMATS.flag_short,
                           params.EXPORT_FORMATS.flag_long,
                           help=params.EXPORT_FORMATS.description,
                           nargs='+',
                           choices=['xlsx', 'csv', 'csv_zip', 'html', 'all'])


def parse_args_qac_create(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'create' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'create'
    parser_qac_create = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_qac_common_args(parser_qac_create, params)

    add_bool_arg_unified(parser_qac_create,
                         params.QAC_DISABLE_OPTIMIZATION.flag_short,
                         params.QAC_DISABLE_OPTIMIZATION.flag_long,
                         msg=params.QAC_DISABLE_OPTIMIZATION.description)

    parser_qac_create.add_argument(params.HELP_PAGES_ROOT_DIR.flag_short,
                                   params.HELP_PAGES_ROOT_DIR.flag_long,
                                   help=params.HELP_PAGES_ROOT_DIR.description)

    parser_qac_create.add_argument(params.LOCAL_BASELINE_PATH.flag_short,
                                   params.LOCAL_BASELINE_PATH.flag_long,
                                   help=params.LOCAL_BASELINE_PATH.description)

    parser_qac_create.add_argument(
        params.HELPER_REMOVE_FILE_LIST.flag_short,
        params.HELPER_REMOVE_FILE_LIST.flag_long,
        help=params.HELPER_REMOVE_FILE_LIST.description)

    add_bool_arg_unified(parser_qac_create,
                         params.HELPER_SUPPRESS_C_HEADER.flag_short,
                         params.HELPER_SUPPRESS_C_HEADER.flag_long,
                         msg=params.HELPER_SUPPRESS_C_HEADER.description)

    parser_qac_create.add_argument(
        params.HELPER_SUPPRESS_FILE_LIST_A.flag_short,
        params.HELPER_SUPPRESS_FILE_LIST_A.flag_long,
        help=params.HELPER_SUPPRESS_FILE_LIST_A.description)

    parser_qac_create.add_argument(
        params.HELPER_SUPPRESS_FILE_LIST_S.flag_short,
        params.HELPER_SUPPRESS_FILE_LIST_S.flag_long,
        help=params.HELPER_SUPPRESS_FILE_LIST_S.description)

    add_bool_arg_unified(parser_qac_create,
                         params.USE_PYTHON_BUILD_SHELL.flag_short,
                         params.USE_PYTHON_BUILD_SHELL.flag_long,
                         msg=params.USE_PYTHON_BUILD_SHELL.description)

    parser_qac_create.add_argument(params.SYNC_BUILD_COMMAND.flag_short,
                                   params.SYNC_BUILD_COMMAND.flag_long,
                                   help=params.SYNC_BUILD_COMMAND.description)

    parser_qac_create.add_argument(params.SYNC_BUILD_LOG_FILE.flag_short,
                                   params.SYNC_BUILD_LOG_FILE.flag_long,
                                   help=params.SYNC_BUILD_LOG_FILE.description)

    add_bool_arg_unified(parser_qac_create,
                         params.CLEANUP_ON_CREATE.flag_short,
                         params.CLEANUP_ON_CREATE.flag_long,
                         msg=params.CLEANUP_ON_CREATE.description)

    parser_qac_create.add_argument(
        params.SKIP_EXIT_ON_BUILD_RETURN_CODES.flag_short,
        params.SKIP_EXIT_ON_BUILD_RETURN_CODES.flag_long,
        help=params.SKIP_EXIT_ON_BUILD_RETURN_CODES.description,
        nargs='+',
        type=int)

    add_bool_arg_unified(parser_qac_create,
                         params.C_FILES_ANALYZED_AS_C.flag_short,
                         params.C_FILES_ANALYZED_AS_C.flag_long,
                         msg=params.C_FILES_ANALYZED_AS_C.description)

    add_bool_arg_unified(parser_qac_create,
                         params.IGNORE_VALIDATION.flag_short,
                         params.IGNORE_VALIDATION.flag_long,
                         msg=params.IGNORE_VALIDATION.description)

    parser_qac_create.add_argument(
        params.MAXIMUM_PARALLEL_WORKERS.flag_short,
        params.MAXIMUM_PARALLEL_WORKERS.flag_long,
        help=params.MAXIMUM_PARALLEL_WORKERS.description)

    parser_qac_create.set_defaults(func=entrypoints['qac_create'],
                                   subcommand=command_name)


def parse_args_qac_analyze(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'analyze' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'analyze'
    parser_qac_analyze = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))

    add_qac_common_args(parser_qac_analyze, params)

    parser_qac_analyze.add_argument(params.ANALYZE_FILE.flag_short,
                                    params.ANALYZE_FILE.flag_long,
                                    help=params.ANALYZE_FILE.description)

    parser_qac_analyze.add_argument(params.ANALYZE_LIST.flag_short,
                                    params.ANALYZE_LIST.flag_long,
                                    help=params.ANALYZE_LIST.description)

    add_bool_arg_unified(parser_qac_analyze,
                         params.HELPER_CREATE_BASELINE.flag_short,
                         params.HELPER_CREATE_BASELINE.flag_long,
                         msg=params.HELPER_CREATE_BASELINE.description)

    parser_qac_analyze.add_argument(
        params.SKIP_EXIT_ON_ANALYSIS_RETURN_CODES.flag_short,
        params.SKIP_EXIT_ON_ANALYSIS_RETURN_CODES.flag_long,
        help=params.SKIP_EXIT_ON_ANALYSIS_RETURN_CODES.description,
        nargs='+',
        type=int)

    add_bool_arg_unified(parser_qac_analyze,
                         params.USE_VSCODE_INTEGRATION.flag_short,
                         params.USE_VSCODE_INTEGRATION.flag_long,
                         msg=params.USE_VSCODE_INTEGRATION.description)

    parser_qac_analyze.set_defaults(func=entrypoints['qac_analyze'],
                                    subcommand=command_name)


def parse_args_qac_report(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'report' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'report'
    parser_qac_report = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_report, params)
    parser_qac_report.set_defaults(func=entrypoints['qac_report'],
                                   subcommand=command_name)


def parse_args_qac_gui(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'gui' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'gui'
    parser_qac_gui = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_gui, params)
    parser_qac_gui.set_defaults(func=entrypoints['qac_gui'],
                                subcommand=command_name)


def parse_args_qac_qavupload(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'qavupload' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'qavupload'
    parser_qac_qavupload = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_qavupload, params)

    parser_qac_qavupload.add_argument(params.QAV_PROJECT_NAME.flag_short,
                                      params.QAV_PROJECT_NAME.flag_long,
                                      help=params.QAV_PROJECT_NAME.description)

    parser_qac_qavupload.add_argument(
        params.QAV_PROJECT_SNAPSHOT.flag_short,
        params.QAV_PROJECT_SNAPSHOT.flag_long,
        help=params.QAV_PROJECT_SNAPSHOT.description)

    parser_qac_qavupload.add_argument(params.QAV_SERVER_URL.flag_short,
                                      params.QAV_SERVER_URL.flag_long,
                                      help=params.QAV_SERVER_URL.description)

    parser_qac_qavupload.add_argument(
        params.QAV_UPLOAD_SOURCE.flag_short,
        params.QAV_UPLOAD_SOURCE.flag_long,
        help=params.QAV_UPLOAD_SOURCE.description)

    parser_qac_qavupload.set_defaults(func=entrypoints['qac_qavupload'],
                                      subcommand=command_name)


def parse_args_qac_s101gen(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 's101gen' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 's101gen'
    parser_qac_s101gen = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_s101gen, params)
    parser_qac_s101gen.set_defaults(func=entrypoints['qac_s101gen'],
                                    subcommand=command_name)


def parse_args_qac_state(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'state' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'state'
    parser_qac_state = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_state, params)
    add_bool_arg_unified(parser_qac_state,
                         params.QAC_WITH_SUBDIAGNOSTICS.flag_short,
                         params.QAC_WITH_SUBDIAGNOSTICS.flag_long,
                         msg=params.QAC_WITH_SUBDIAGNOSTICS.description)
    add_bool_arg_unified(parser_qac_state,
                         params.QAC_WITH_FULL_SUBDIAGNOSTICS.flag_short,
                         params.QAC_WITH_FULL_SUBDIAGNOSTICS.flag_long,
                         msg=params.QAC_WITH_FULL_SUBDIAGNOSTICS.description)
    add_bool_arg_unified(parser_qac_state,
                         params.QAC_WITH_METRICS.flag_short,
                         params.QAC_WITH_METRICS.flag_long,
                         msg=params.QAC_WITH_METRICS.description)
    parser_qac_state.add_argument(params.METRICS_FILTER_LIST.flag_short,
                                  params.METRICS_FILTER_LIST.flag_long,
                                  help=params.METRICS_FILTER_LIST.description,
                                  nargs='+')
    add_bool_arg_unified(parser_qac_state,
                         params.QAC_CLEANUP_DIAGNOSTICS_OUTPUT.flag_short,
                         params.QAC_CLEANUP_DIAGNOSTICS_OUTPUT.flag_long,
                         msg=params.QAC_CLEANUP_DIAGNOSTICS_OUTPUT.description)
    map_teams_common_configurable_args(parser_qac_state, params)
    qac_export_formats_args(parser_qac_state, params)
    parser_qac_state.set_defaults(func=entrypoints['qac_state'],
                                  subcommand=command_name)


def parse_args_qac_export_state(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'export_state' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'export_state'
    parser_qac_export_state = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_export_state, params)
    add_bool_arg_unified(parser_qac_export_state,
                         params.QAC_WITH_METRICS.flag_short,
                         params.QAC_WITH_METRICS.flag_long,
                         msg=params.QAC_WITH_METRICS.description)
    parser_qac_export_state.add_argument(
        params.METRICS_FILTER_LIST.flag_short,
        params.METRICS_FILTER_LIST.flag_long,
        help=params.METRICS_FILTER_LIST.description,
        nargs='+')
    map_teams_common_configurable_args(parser_qac_export_state, params)
    qac_export_formats_args(parser_qac_export_state, params)
    parser_qac_export_state.set_defaults(func=entrypoints['qac_export_state'],
                                         subcommand=command_name)


def parse_args_qac_fix_cl_json(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'fix_cl_json' helper subcommand

    :param qac_subparser: subparser for qac argument parser
    """
    command_name = 'fix_cl_json'
    parser_qac_fix_cl_json = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_fix_cl_json, params)

    parser_qac_fix_cl_json.add_argument(params.INPUT_CL_JSON.flag_short,
                                        params.INPUT_CL_JSON.flag_long,
                                        help=params.INPUT_CL_JSON.description)

    parser_qac_fix_cl_json.set_defaults(func=entrypoints['qac_fix_cl_json'],
                                        subcommand=command_name)


def parse_args_qac_filter_qaview(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'filter_qaview' helper subcommand

    :param qaview-csv: path to qaview export
    :param fail-threshold-severity-{level}: amount of maximum warnings
    :param ignore: error ids that can be ignored
    """
    command_name = 'filter_qaview'
    parser_qac_filter_qaview = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_filter_qaview, params)

    parser_qac_filter_qaview.add_argument(params.QAVIEW_CSV.flag_short,
                                          params.QAVIEW_CSV.flag_long,
                                          help=params.QAVIEW_CSV.description)

    parser_qac_filter_qaview.add_argument(params.IGNORE_IDS.flag_short,
                                          params.IGNORE_IDS.flag_long,
                                          help=params.IGNORE_IDS.description)

    parser_qac_filter_qaview.add_argument(
        params.JUSTIFICATION_MESSAGE_REGEXP.flag_short,
        params.JUSTIFICATION_MESSAGE_REGEXP.flag_long,
        help=params.JUSTIFICATION_MESSAGE_REGEXP.description,
        nargs='+')

    parser_qac_filter_qaview.add_argument(
        params.FILTER_REPORT_OUTPUT_FILE.flag_short,
        params.FILTER_REPORT_OUTPUT_FILE.flag_long,
        help=params.FILTER_REPORT_OUTPUT_FILE.description)

    add_bool_arg_unified(parser_qac_filter_qaview,
                         params.TO_STDOUT.flag_short,
                         params.TO_STDOUT.flag_long,
                         msg=params.TO_STDOUT.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_0.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_0.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_0.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_1.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_1.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_1.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_2.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_2.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_2.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_3.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_3.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_3.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_4.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_4.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_4.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_5.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_5.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_5.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_6.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_6.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_6.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_7.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_7.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_7.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_8.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_8.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_8.description)

    parser_qac_filter_qaview.add_argument(
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_9.flag_short,
        params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_9.flag_long,
        help=params.SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_9.description)

    parser_qac_filter_qaview.add_argument(
        params.QAC_THRESHOLD_WARNINGS_REPORT.flag_short,
        params.QAC_THRESHOLD_WARNINGS_REPORT.flag_long,
        help=params.QAC_THRESHOLD_WARNINGS_REPORT.description)

    parser_qac_filter_qaview.set_defaults(
        func=entrypoints['qac_filter_qaview'], subcommand=command_name)


def parse_args_qac_export_analysis(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'export_analysis' helper subcommand
    """
    command_name = 'export_analysis'
    parser_qac_export_analysis = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_export_analysis, params)
    qac_export_formats_args(parser_qac_export_analysis, params)
    map_teams_common_configurable_args(parser_qac_export_analysis, params)
    parser_qac_export_analysis.add_argument(
        params.METRICS_FILTER_LIST.flag_short,
        params.METRICS_FILTER_LIST.flag_long,
        help=params.METRICS_FILTER_LIST.description,
        nargs='+')
    add_bool_arg_unified(parser_qac_export_analysis,
                         params.QAC_WITH_SUBDIAGNOSTICS.flag_short,
                         params.QAC_WITH_SUBDIAGNOSTICS.flag_long,
                         msg=params.QAC_WITH_SUBDIAGNOSTICS.description)
    add_bool_arg_unified(parser_qac_export_analysis,
                         params.QAC_WITH_FULL_SUBDIAGNOSTICS.flag_short,
                         params.QAC_WITH_FULL_SUBDIAGNOSTICS.flag_long,
                         msg=params.QAC_WITH_FULL_SUBDIAGNOSTICS.description)
    add_bool_arg_unified(parser_qac_export_analysis,
                         params.QAC_CLEANUP_DIAGNOSTICS_OUTPUT.flag_short,
                         params.QAC_CLEANUP_DIAGNOSTICS_OUTPUT.flag_long,
                         msg=params.QAC_CLEANUP_DIAGNOSTICS_OUTPUT.description)
    add_bool_arg_unified(parser_qac_export_analysis,
                         params.QAC_WITH_ANALYSIS.flag_short,
                         params.QAC_WITH_ANALYSIS.flag_long,
                         msg=params.QAC_WITH_ANALYSIS.description)
    add_bool_arg_unified(parser_qac_export_analysis,
                         params.QAC_WITH_METRICS.flag_short,
                         params.QAC_WITH_METRICS.flag_long,
                         msg=params.QAC_WITH_METRICS.description)
    add_bool_arg_unified(parser_qac_export_analysis,
                         params.QAC_WITH_SUMMARY.flag_short,
                         params.QAC_WITH_SUMMARY.flag_long,
                         msg=params.QAC_WITH_SUMMARY.description)
    add_bool_arg_unified(parser_qac_export_analysis,
                         params.QAC_WITH_STATE_FILE.flag_short,
                         params.QAC_WITH_STATE_FILE.flag_long,
                         msg=params.QAC_WITH_STATE_FILE.description)
    parser_qac_export_analysis.add_argument(
        params.QAC_FROM_STATE_FILE.flag_short,
        params.QAC_FROM_STATE_FILE.flag_long,
        help=params.QAC_FROM_STATE_FILE.description,
        nargs='?',
        const=True)

    parser_qac_export_analysis.set_defaults(
        func=entrypoints['qac_export_analysis'], subcommand=command_name)


def parse_args_qac_create_baseline(qac_subparser, params, entrypoints):
    """
    Parse arguments for qac 'create_baseline' helper subcommand
    """
    command_name = 'create_baseline'
    parser_qac_create_baseline = qac_subparser.add_parser(
        command_name, help=params.get_description(subparser=command_name))
    add_qac_common_args(parser_qac_create_baseline, params)

    parser_qac_create_baseline.set_defaults(
        func=entrypoints['qac_create_baseline'], subcommand=command_name)
