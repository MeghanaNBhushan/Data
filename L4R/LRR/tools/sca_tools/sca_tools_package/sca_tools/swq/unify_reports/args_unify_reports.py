# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: args_unify_reports.py
# -----------------------------------------------------------------------------
"""The argument subparser for the unify_reports subcommand of SCA tools"""
from swq.common.args.args_utils import add_common_config_args


def parse_args_unify_reports(helper_sub, params, entrypoints):
    """
    Parses unify_reports command arguments

    :param helper_sub: SWQ SCA Tools argument parser
    :param params: object of CommandParameters class
    :param entrypoints: dictionary with mapping of keyword to function
                        to be executed
    """

    unify_reports_parser = helper_sub.add_parser('unify_reports',
                                                 help=params.get_description())

    add_common_config_args(unify_reports_parser, params)

    unify_reports_parser.add_argument(
        params.UNIFY_REPORT_VARIANT_INPUT.flag_short,
        params.UNIFY_REPORT_VARIANT_INPUT.flag_long,
        type=str,
        help=params.UNIFY_REPORT_VARIANT_INPUT.description)

    unify_reports_parser.add_argument(
        params.UNIFY_REPORT_OUTPUT.flag_short,
        params.UNIFY_REPORT_OUTPUT.flag_long,
        type=str,
        help=params.UNIFY_REPORT_OUTPUT.description)

    unify_reports_parser.add_argument(
        params.UNIFY_REPORT_TYPE.flag_short,
        params.UNIFY_REPORT_TYPE.flag_long,
        type=str,
        help=params.UNIFY_REPORT_TYPE.description)
    unify_reports_parser.set_defaults(entrypoint='unify_reports',
                                      func=entrypoints['unify_reports'])
