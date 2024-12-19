""" See https://docs.python.org/3/library/argparse.html for usage. """
import argparse
import os

from lucxbox.__pkginfo__ import VERSION

def add_version(parser):
    """ Add default logger argument. """
    parser.add_argument('--version', action='version',
                        version='lucxbox version {version}'.format(version=VERSION))
    return parser


def add_log_level(parser):
    """ Add default logger argument. """
    parser.add_argument('-d', '--debug', dest='log_level',
                        action='store_const', const='DEBUG', default='INFO',
                        help='Print debug information')
    parser.add_argument('-q', '--quiet', dest='log_level',
                        action='store_const', const='ERROR', default='INFO',
                        help='Print only errors')
    return parser


def add_cfg(parser):
    """ Add default config argument. """
    parser.add_argument('--config', default='CONFIG')
    return parser


def split_argv(argv):
    if argv.count("--") > 0:
        main_argv = argv[1:argv.index("--")]
        build_argv = argv[argv.index("--") + 1:]
        return main_argv, build_argv
    else:
        main_argv = argv[1:]
        return main_argv, None


def existing_file(file_path):
    """
    Argparse 'type' method to check whether a given file on command line exists
    """
    if os.path.isfile(file_path):
        return file_path
    else:
        raise argparse.ArgumentTypeError(
            "Given file '{}' does not exist".format(file_path))


def existing_directory(dir_path):
    """
    Argparse 'type' method to check whether a given file on command line exists
    """
    if os.path.isdir(dir_path):
        return dir_path
    else:
        raise argparse.ArgumentTypeError(
            "Given file '{}' does not exist".format(dir_path))
