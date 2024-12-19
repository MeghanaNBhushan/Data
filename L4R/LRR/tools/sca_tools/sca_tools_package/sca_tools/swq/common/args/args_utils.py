# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: args_utils.py
# -----------------------------------------------------------------------------
"""Helper functions for the argument parser of the SWQ SCA Tools"""

import argparse


def add_bool_arg_unified(parser, short, name, msg):
    """ Add boolean argument to an argument parser """
    def _str2bool(value):
        if isinstance(value, bool):
            return value
        if value.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        if value.lower() in ('no', 'false', 'f', 'n', '0', ''):
            return False

        raise argparse.ArgumentTypeError('Incorrect boolean value specified.')

    parser.add_argument(short,
                        name,
                        type=_str2bool,
                        nargs='?',
                        const=True,
                        help=msg)


def add_common_config_args(parser, params):
    """
    Add swq.common arguments to a helper parser

    :param parser: argument parser
    """
    parser.add_argument(params.DATASTORE_PATH.flag_short,
                        params.DATASTORE_PATH.flag_long,
                        nargs='+',
                        help=params.DATASTORE_PATH.description)

    parser.add_argument(params.DATASTORE_TARGET.flag_short,
                        params.DATASTORE_TARGET.flag_long,
                        help=params.DATASTORE_TARGET.description)

    parser.add_argument(params.PROJECT_ROOT.flag_short,
                        params.PROJECT_ROOT.flag_long,
                        help=params.PROJECT_ROOT.description)

    parser.add_argument(params.HELPER_LOGS_PATH.flag_short,
                        params.HELPER_LOGS_PATH.flag_long,
                        help=params.HELPER_LOGS_PATH.description)


def map_teams_common_configurable_args(parser, params):
    """
    Add swq.common map teams arguments to a parser

    :param parser: argument parser
    """
    parser.add_argument(params.CODEOWNERS_FILE.flag_short,
                        params.CODEOWNERS_FILE.flag_long,
                        nargs='+',
                        type=str,
                        help=params.CODEOWNERS_FILE.description)

    add_bool_arg_unified(parser,
                         params.ONLY_LAST_TEAM.flag_short,
                         params.ONLY_LAST_TEAM.flag_long,
                         msg=params.ONLY_LAST_TEAM.description)

    add_bool_arg_unified(parser,
                         params.GITIGNORE_MAPPING.flag_short,
                         params.GITIGNORE_MAPPING.flag_long,
                         msg=params.GITIGNORE_MAPPING.description)
