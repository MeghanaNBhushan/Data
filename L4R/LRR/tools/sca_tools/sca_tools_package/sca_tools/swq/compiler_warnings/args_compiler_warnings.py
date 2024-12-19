# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: args_compiler_warnings.py
# -----------------------------------------------------------------------------
"""The argument subparser for the compiler_warnings command of SWQ SCA Tools"""

from swq.common.args.args_utils import add_bool_arg_unified, \
    add_common_config_args, map_teams_common_configurable_args
from swq.compiler_warnings.config_compiler_warnings \
    import CW_COMPILER_VALUES, CW_EXPORT_FORMATS


def parse_args_compiler_warnings(helper_sub, params, entrypoints):
    """
    Parses compiler_warnings command arguments

    :param helper_sub: SWQ SCA Tools argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    compiler_warns_parser = helper_sub.add_parser(
        'compiler_warnings', help=params.get_description())

    add_common_config_args(compiler_warns_parser, params)
    map_teams_common_configurable_args(compiler_warns_parser, params)

    compiler_warns_parser.add_argument(params.BLACK_LIST.flag_short,
                                       params.BLACK_LIST.flag_long,
                                       help=params.BLACK_LIST.description,
                                       nargs='+')

    compiler_warns_parser.add_argument(params.CHANGED_FILES.flag_short,
                                       params.CHANGED_FILES.flag_long,
                                       help=params.CHANGED_FILES.description)

    compiler_warns_parser.add_argument(params.COMPILER.flag_short,
                                       params.COMPILER.flag_long,
                                       help=params.COMPILER.description,
                                       choices=CW_COMPILER_VALUES)

    compiler_warns_parser.add_argument(params.COMPILER_LOG.flag_short,
                                       params.COMPILER_LOG.flag_long,
                                       help=params.COMPILER_LOG.description)

    compiler_warns_parser.add_argument(
        params.COMPILER_WARNINGS_MAPPING_COLUMN.flag_short,
        params.COMPILER_WARNINGS_MAPPING_COLUMN.flag_long,
        type=str,
        help=params.COMPILER_WARNINGS_MAPPING_COLUMN.description)

    compiler_warns_parser.add_argument(
        params.COMPILER_WARNINGS_REPORT_BASENAME.flag_short,
        params.COMPILER_WARNINGS_REPORT_BASENAME.flag_long,
        help=params.COMPILER_WARNINGS_REPORT_BASENAME.description)

    compiler_warns_parser.add_argument(
        params.COMPILER_WARNINGS_REPORT_DIR.flag_short,
        params.COMPILER_WARNINGS_REPORT_DIR.flag_long,
        help=params.COMPILER_WARNINGS_REPORT_DIR.description)

    compiler_warns_parser.add_argument(params.EXPORT_FORMATS.flag_short,
                                       params.EXPORT_FORMATS.flag_long,
                                       help=params.EXPORT_FORMATS.description,
                                       nargs='+',
                                       choices=CW_EXPORT_FORMATS + ['all'])

    compiler_warns_parser.add_argument(params.JOBS.flag_short,
                                       params.JOBS.flag_long,
                                       help=params.JOBS.description)

    compiler_warns_parser.add_argument(params.OUTPUT.flag_short,
                                       params.OUTPUT.flag_long,
                                       help=params.OUTPUT.description)

    add_bool_arg_unified(compiler_warns_parser,
                         params.QUIET.flag_short,
                         params.QUIET.flag_long,
                         msg=params.QUIET.description)

    compiler_warns_parser.add_argument(
        params.TARGET_DIRECTORY.flag_short,
        params.TARGET_DIRECTORY.flag_long,
        help=params.TARGET_DIRECTORY.description,
        nargs='+')

    compiler_warns_parser.add_argument(params.THRESHOLD.flag_short,
                                       params.THRESHOLD.flag_long,
                                       help=params.THRESHOLD.description)

    compiler_warns_parser.add_argument(params.THRESHOLD_FILE.flag_short,
                                       params.THRESHOLD_FILE.flag_long,
                                       help=params.THRESHOLD_FILE.description)

    compiler_warns_parser.add_argument(params.TYPES_DB.flag_short,
                                       params.TYPES_DB.flag_long,
                                       help=params.TYPES_DB.description)

    add_bool_arg_unified(compiler_warns_parser,
                         params.USE_RELATIVE_PATHS.flag_short,
                         params.USE_RELATIVE_PATHS.flag_long,
                         msg=params.USE_RELATIVE_PATHS.description)

    compiler_warns_parser.set_defaults(entrypoint='compiler_warnings',
                                       func=entrypoints['compiler_warnings'])
