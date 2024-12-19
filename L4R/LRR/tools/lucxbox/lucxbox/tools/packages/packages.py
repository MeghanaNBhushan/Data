"""
A script to create / check / update / checkout / compare software packages

software package in this context means a directory
without submodules

"""

import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs
from lucxbox.lib import lucxlog

from lucxbox.tools.packages.compare import api as compare_api
from lucxbox.tools.packages.status import api as status_api
from lucxbox.tools.packages.update import api as update_api
from lucxbox.tools.packages.checkout import api as checkout_api
from lucxbox.tools.packages.create import api as create_api
from lucxbox.tools.packages.remote import api as remote_api
from lucxbox.tools.packages.sync import api as sync_api


def parse_args():
    parser = argparse.ArgumentParser()
    parser = lucxargs.add_log_level(parser)
    parser.add_argument('-p', '--package-file-name', default='rb_package.json',
                        help="The packages file name that indicates a package. Default is 'rb_package.json'")
    parser.add_argument('-r', '--root', default=os.getcwd(),
                        help='Root path of searching for packages',
                        type=lucxargs.existing_directory)
    parser.add_argument('-f', '--filter', dest='packages_filter',
                        help='Restrict the packages by a wildcard for the package name, e.g. pf.if.*')
    parser.add_argument('-t', '--time-based', action='store_true',
                        help='Time based package versioning. Default is semantic')
    parser.add_argument('-y', '--filter-type', help='Filters the packages to only consider the ones with the given type')

    parser_sub = parser.add_subparsers(title='Package sub commands')

    compare_api(parser_sub)
    status_api(parser_sub)
    update_api(parser_sub)
    checkout_api(parser_sub)
    create_api(parser_sub)
    remote_api(parser_sub)
    sync_api(parser_sub)

    return parser.parse_args()


def main():
    args = parse_args()
    if not args.package_file_name.endswith('.json'):
        args.package_file_name += '.json'
    LOGGER.setLevel(args.log_level)
    if hasattr(args, 'func'):
        args.func(args)
    else:
        LOGGER.error(
            "Wrong usage. Please check tool usage with '--help' or '-h'")
        sys.exit(1)


if __name__ == "__main__":
    LOGGER = lucxlog.get_logger()
    main()
