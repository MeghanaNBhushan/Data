import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog
from lucxbox.tools.packages.package import get_packages

LOGGER = lucxlog.get_logger()


def api(parser):
    parser_update = parser.add_parser(
        'update', help='Updating package information')

    parser_update.add_argument(
        '-v', '--version', help='Version name. E.g. a semantic one like "1.0.0"')
    parser_update.set_defaults(func=update_version)


def update_version(args):
    packages = get_packages(args.root, args.package_file_name,
                            args.time_based, args.packages_filter, args.filter_type, "update")
    if len(packages) > 1:
        LOGGER.warning(
            "Updating more than one package with a version name. Is this really what you want?")
    for package in packages:
        if args.time_based:
            if args.version:
                LOGGER.warning(
                    "-v / --version given for updating a time based version. Given version will be ignored")
            new_version = package.get_next_time_based_version()
        else:
            if not args.version:
                LOGGER.error(
                    "-v / --version is required for semantic version update.")
                sys.exit(1)
            new_version = args.version

        package_file_hash = package.get_package_file_hash()
        package_disk_hash = package.get_disk_hash()

        if package_file_hash == package_disk_hash:
            LOGGER.info("HASH :: %s [LEAVING AS IS]", package.get_name())
            LOGGER.info("VERSION :: %s :: %s [LEAVING AS IS]", package.get_name(), package.get_version())
        else:
            package.update_package_file_hash()
            LOGGER.info(
                "HASH :: %s :: %s -> %s [UPDATED]", package.get_name(), package_file_hash, package_disk_hash)
            package.update_version(new_version)
