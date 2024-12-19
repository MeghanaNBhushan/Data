import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib.lucxprint import Printer, Status
from lucxbox.lib.color_string import Color
from lucxbox.lib import lucxlog, lucxargs
from lucxbox.tools.packages.package import get_packages

LOGGER = lucxlog.get_logger()


def api(parser):
    parser_status = parser.add_parser('status', help='Packages status')
    parser_status.add_argument('--fail-on-diff', '-f', action='store_true',
                               help='Fail the script when packages were changed')
    parser_status.add_argument(
        '-l', '--long', action='store_true', help='Long status - every package detail')
    parser_status.add_argument('-r', '--reference', type=lucxargs.existing_directory,
                               help='Reference root to check against trusted package file checksums')
    parser_status.add_argument('-o', '--output', help='Status output to file in an easier parseable format')
    parser_status.set_defaults(func=status)


def status(args):
    packages = get_packages(args.root, args.package_file_name,
                            args.time_based, args.packages_filter, args.filter_type)
    reference_packages = []
    if args.reference:
        reference_packages = get_packages(
            args.reference, args.package_file_name, args.time_based, args.packages_filter, args.filter_type)
    modified_packages = []
    clean_packages = []
    for package in packages:
        if args.long:
            package.pretty_print()
        if package.needs_hash_update():
            modified_packages.append(package)
        else:
            package_clean = True
            if args.reference and not package_clean_against_ref(package, reference_packages):
                package_clean = False
            if package_clean:
                clean_packages.append(package)
            else:
                modified_packages.append(package)

    print_status_summary(modified_packages, clean_packages)

    if args.output:
        status_to_file(modified_packages, clean_packages, args.output, args.long)

    if args.fail_on_diff:
        sys.exit(len(modified_packages))


def get_package_status_file_line(package, clean, details):
    name = package.get_name()
    version = package.get_version()
    clean_indicator = 'dirty'
    checksum = package.get_disk_hash()
    if clean:
        clean_indicator = 'clean'
    line = "{} {} {}\n".format(name, clean_indicator, version)
    if details:
        line = "{} {} {} {}\n".format(name, clean_indicator, version, checksum)
    return line


def status_to_file(modified_packages, clean_packages, output_file, details):
    with open(output_file, 'w') as out:
        for clean_package in clean_packages:
            out.write(get_package_status_file_line(clean_package, True, details))
        for modified_package in modified_packages:
            out.write(get_package_status_file_line(modified_package, False, details))


def print_status_summary(modified_packages, clean_packages):
    printer = Printer(box_color=Color.grey)
    printer.title('Status', color=Color.green)

    if modified_packages:
        printer.print(content='Modified', color=Color.yellow,
                      status=Status.warning, status_content=str(len(modified_packages)))
        for modified_package in modified_packages:
            printer.print(content=modified_package.get_name(),
                          status_content=modified_package.get_version() + '*',
                          status=Status.warning, offset=4)

    if clean_packages:
        printer.print(content='Clean', color=Color.green,
                      status=Status.okay, status_content=str(len(clean_packages)))
        for modified_package in clean_packages:
            printer.print(content=modified_package.get_name(),
                          status_content=modified_package.get_version(),
                          status=Status.okay, offset=4)
    printer.divider()


def package_clean_against_ref(package, reference_packages):
    clean = True
    for ref_package in reference_packages:
        if package.get_name() == ref_package.get_name():
            if package.get_version() == ref_package.get_version():
                if package.get_package_file_hash() != ref_package.get_package_file_hash():
                    LOGGER.error("Hash of '%s' for version '%s' != reference hash",
                                 package.get_name(), package.get_version())
                    clean = False
            else:
                LOGGER.warning(
                    "Version of package and reference is not the same")
            break
    return clean
