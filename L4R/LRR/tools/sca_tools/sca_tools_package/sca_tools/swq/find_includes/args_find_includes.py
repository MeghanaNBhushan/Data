# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: args_find_includes.py
# -----------------------------------------------------------------------------
"""The argument subparser for the find_includes command of SWQ SCA Tools"""

from swq.common.args.args_utils import add_bool_arg_unified, \
    add_common_config_args


def parse_args_find_includes(helper_sub, params, entrypoints):
    """
    Parses find_includes command arguments

    :param helper_sub: SWQ SCA Tools argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """
    find_includes_parser = helper_sub.add_parser('find_includes',
                                                 help=params.get_description())

    add_common_config_args(find_includes_parser, params)

    find_includes_parser.add_argument(params.FROM_LIST.flag_short,
                                      params.FROM_LIST.flag_long,
                                      help=params.FROM_LIST.description)

    find_includes_parser.add_argument(params.OUTPUT_FILE.flag_short,
                                      params.OUTPUT_FILE.flag_long,
                                      help=params.OUTPUT_FILE.description)

    find_includes_parser.add_argument(
        params.FIND_INCLUDES_GIT_DIFF_FILTER.flag_short,
        params.FIND_INCLUDES_GIT_DIFF_FILTER.flag_long,
        help=params.FIND_INCLUDES_GIT_DIFF_FILTER.description)

    find_includes_parser.add_argument(
        params.FIND_INCLUDE_STRATEGY.flag_short,
        params.FIND_INCLUDE_STRATEGY.flag_long,
        help=params.FIND_INCLUDE_STRATEGY.description,
        choices=['all', 'minimal'])

    find_includes_parser.add_argument(params.MERGE_BASE.flag_short,
                                      params.MERGE_BASE.flag_long,
                                      help=params.MERGE_BASE.description)

    find_includes_parser.add_argument(params.CODE_DIRS_FILE.flag_short,
                                      params.CODE_DIRS_FILE.flag_long,
                                      help=params.CODE_DIRS_FILE.description)

    find_includes_parser.add_argument(
        params.THIRDPARTY_PREFIXES.flag_short,
        params.THIRDPARTY_PREFIXES.flag_long,
        help=params.THIRDPARTY_PREFIXES.description)

    find_includes_parser.add_argument(
        params.BLACKLIST_PATTERN.flag_short,
        params.BLACKLIST_PATTERN.flag_long,
        help=params.BLACKLIST_PATTERN.description)

    find_includes_parser.add_argument(
        params.WITH_MAPPING_REPORT.flag_short,
        params.WITH_MAPPING_REPORT.flag_long,
        help=params.WITH_MAPPING_REPORT.description)

    add_bool_arg_unified(find_includes_parser,
                         params.FROM_STDIN.flag_short,
                         params.FROM_STDIN.flag_long,
                         msg=params.FROM_STDIN.description)

    add_bool_arg_unified(find_includes_parser,
                         params.TO_STDOUT.flag_short,
                         params.TO_STDOUT.flag_long,
                         msg=params.TO_STDOUT.description)

    find_includes_parser.set_defaults(entrypoint='find_includes',
                                      func=entrypoints['find_includes'])
