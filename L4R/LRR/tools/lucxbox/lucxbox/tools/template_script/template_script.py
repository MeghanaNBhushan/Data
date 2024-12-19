""" Template for a python project """

import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog


def parse_args():
    desc = "Please add some description."
    parser = argparse.ArgumentParser(description=desc)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    parser.add_argument('--config', default='CONFIG')
    return parser.parse_args()


def upper(in_var):
    """ Just a dummy function to show the unittest framework. """
    return in_var.upper()


def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)
    lucxlog.demo(LOGGER)


if __name__ == "__main__":
    LOGGER = lucxlog.get_logger()
    main()
