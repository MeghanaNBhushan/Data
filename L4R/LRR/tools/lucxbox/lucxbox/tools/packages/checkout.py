import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog
from lucxbox.tools.packages.package import get_packages

LOGGER = lucxlog.get_logger()


def api(parser):
    parser_checkout = parser.add_parser(
        'checkout-helper', help='Package Checkout Helper')
    parser_checkout_type = parser_checkout.add_mutually_exclusive_group(
        required=True)
    parser_checkout_type.add_argument(
        '-l', '--list', action='store_true', help='Lists available versions of the package. Exits afterwards')
    parser_checkout_type.add_argument(
        '-v', '--version', help='Version to be searched and checked out')
    parser_checkout.add_argument('-r', '--reference', default='HEAD',
                                 help='The branch to fetch and start parsing the package history and finding the version.'
                                 + 'The default is "HEAD" which does not fetch from origin.')
    parser_checkout.add_argument('-n', '--no-fetch', action='store_true', dest='local', help='Do not fetch reference from origin')
    parser_checkout.set_defaults(func=checkout_helper)


def checkout_helper(args):
    packages = get_packages(args.root, args.package_file_name,
                            args.time_based, args.packages_filter, args.filter_type)
    if len(packages) > 1:
        LOGGER.error("Checkout feature is limited to a single package chosen")
        LOGGER.error("Current selected packages (%d):", len(packages))
        for package in packages:
            LOGGER.error(package.get_name())
        sys.exit(1)
    package = packages[0]
    package.scan_versions_from_ref(args.local, args.reference)
    if args.list:
        LOGGER.info("Available versions of package '%s':", package.get_name())
        for version in package.get_versions():
            LOGGER.info(version)
        sys.exit(0)

    package.print_checkout_commands(args.version)
