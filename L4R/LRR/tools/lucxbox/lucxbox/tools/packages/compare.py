import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib.lucxprint import Printer, Status
from lucxbox.lib.color_string import Color
from lucxbox.tools.packages.package import get_packages


def api(parser):
    parser_compare = parser.add_parser('compare', help='Package comparing for different roots')
    parser_compare.add_argument('-r', '--root', dest='compare_root',
                                required=True, help='Root of the other packages to compare')
    parser_compare.set_defaults(func=compare)


def compare(args):
    packages = get_packages(args.root, args.package_file_name,
                            args.time_based, args.packages_filter)
    compare_packages = get_packages(args.compare_root, args.package_file_name, args.time_based,
                                    args.packages_filter, args.filter_type)
    packages_missing = get_missing_packages(packages, compare_packages)
    packages_additional = get_missing_packages(compare_packages, packages)  # pylint: disable=arguments-out-of-order
    packages_common = get_common_packages(packages, compare_packages)

    printer = Printer(box_color=Color.grey)
    printer.title('Status', color=Color.green)
    printer.print('Number of Packages')
    printer.print('Base:   ' + str(len(packages)), offset=4, color=Color.cyan)
    printer.print('Target: ' + str(len(compare_packages)),
                  offset=4, color=Color.magenta)
    printer.print('Common: ' + str(len(packages_common)),
                  offset=4, color=Color.blue)
    if packages_missing or packages_additional:
        printer.title('Missing/Additional Packages')
        for mpackage in packages_missing:
            printer.print(mpackage.get_name(), color=Color.red,
                          status=Status.error, status_content='MISSING')
        for mpackage in packages_additional:
            printer.print(mpackage.get_name(), color=Color.green,
                          status=Status.okay, status_content='ADDITIONAL')

    printer.title('Package Versions Comparison')
    for common_package in packages_common:
        base_package = common_package
        target_package = get_package_with_name(
            compare_packages, base_package.get_name())
        printer.print(common_package.get_name())
        if base_package.get_version() != target_package.get_version():
            printer.print('Version (Base):   ' +
                          base_package.get_version(), color=Color.green, offset=4)
            printer.print('Version (Target): ' +
                          target_package.get_version(), color=Color.red, offset=4)
        else:
            printer.print('Version (Base):   ' +
                          base_package.get_version(), color=Color.green, offset=4)
            printer.print('Version (Target): ' +
                          target_package.get_version(), color=Color.green, offset=4)

        if base_package.get_package_file_hash() != target_package.get_package_file_hash():
            printer.print('Checksum (Base):   ' +
                          base_package.get_package_file_hash(), color=Color.green, offset=4)
            printer.print('Checksum (Target): ' +
                          target_package.get_package_file_hash(), color=Color.red, offset=4)
        else:
            printer.print('Checksum (Base):   ' +
                          base_package.get_package_file_hash(), color=Color.green, offset=4)
            printer.print('Checksum (Target): ' +
                          target_package.get_package_file_hash(), color=Color.green, offset=4)

    printer.divider()


def get_missing_packages(packages, compare_packages):
    missing_packages = []
    for package in packages:
        missing = True
        for cpackage in compare_packages:
            if package.get_name() == cpackage.get_name():
                missing = False
        if missing:
            missing_packages.append(package)
    return missing_packages


def get_common_packages(packages, compare_packages):
    common_packages = []
    for package in packages:
        for cpackage in compare_packages:
            if package.get_name() == cpackage.get_name():
                common_packages.append(package)
    return common_packages


def get_package_with_name(packages, name):
    for package in packages:
        if package.get_name() == name:
            return package
    return None
