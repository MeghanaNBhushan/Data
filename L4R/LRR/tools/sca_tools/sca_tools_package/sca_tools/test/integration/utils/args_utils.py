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
# ----------------------------------------------------------------------------
"""Argument parser utils"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter, \
    ArgumentTypeError


def add_bool_arg_unified(parser, short, full, msg):
    """ Add boolean argument to an argument parser """
    def _str2bool(value):
        if isinstance(value, bool):
            return value
        if value.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        if value.lower() in ('no', 'false', 'f', 'n', '0', ''):
            return False

        raise ArgumentTypeError('Incorrect boolean value specified.')

    parser.add_argument(short,
                        full,
                        type=_str2bool,
                        nargs='?',
                        const=True,
                        help=msg)


def add_coverity_args(subparser):
    coverity_parser = subparser.add_parser('coverity')
    add_common_args(coverity_parser)
    coverity_parser.add_argument(
        '--version',
        help='Select Coverity version, e.g. 2020.03, 2020.06, ...')
    coverity_parser.set_defaults(test_type='coverity')


def add_qac_args(subparser):
    qac_parser = subparser.add_parser('qac')
    add_common_args(qac_parser)
    qac_parser.add_argument(
        '--version', help='Select QAC version, e.g. 2019.2, 2020.1, ...')
    qac_parser.set_defaults(test_type='qac')


def add_common_args(parser):
    parser.add_argument('-f',
                        '--features',
                        nargs='+',
                        help='Select feature as config, create or analyze')

    parser.add_argument('-pr',
                        '--project_root',
                        help='Path to the project root folder')

    parser.add_argument('-rp',
                        '--reports_dir',
                        help='Absolute path to Junit reports directory')


def add_behave_args(parser):
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Prints the behave tests log to stdout')


def setup_argument_parser():
    """Set up argparse command line argument parser."""
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawDescriptionHelpFormatter)
    subparser = parser.add_subparsers(title='Behave sub-commands')

    add_behave_args(parser)
    add_qac_args(subparser)
    add_coverity_args(subparser)

    return parser
