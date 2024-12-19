import sys
import os
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog
from lucxbox.tools.packages.helper import write_json


LOGGER = lucxlog.get_logger()


def api(parser):
    parser_init = parser.add_parser('create', help='Package creation')
    parser_init.add_argument('-n', '--name', help='The name of the component. When not given, path from cwd will be used')
    parser_init.add_argument('-d', '--directories', nargs='+',
                             help='Directories to include in the package. Default is ".". Paths are relative to the root of the package!')
    parser_init.add_argument('-e', '--exclude-directories', nargs='+',
                             help='Directories to exclude from the package checksum. Paths are relative to the root of the package!')
    parser_init.add_argument('-f', '--exclude-file-extensions', nargs='+',
                             help='File extensions to be excluded from checksum (e.g. ".txt .md")')
    parser_init.add_argument('-t', '--types', nargs='+',
                             help='Types to assign to this package')
    parser_init.add_argument('-s', '--files', nargs='+',
                             help='Additional files to include in the package. Paths are relative to the root of the package!')

    parser_init.set_defaults(func=create)


def create(args):
    package_file_location = os.path.join(args.root, args.package_file_name)
    LOGGER.info("Creating new package file '%s' in '%s'", args.package_file_name, os.path.abspath(args.root))
    if args.name:
        name = args.name
    else:
        rel_path = Path(args.root).absolute().relative_to(os.getcwd())
        name = str(rel_path).replace(os.sep, '.')
    LOGGER.info("Package name is '%s'", name)
    package_file = {}
    package_file['name'] = name
    package_file['version'] = {'semantic_name': '0.0.0', 'semantic_md5': '0'}
    package_file['version']['time_based_name'] = '1999'
    package_file['version']['time_based_md5'] = '0'
    if args.directories:
        package_file['directories'] = args.directories
    if args.exclude_directories:
        package_file['directories_exclude'] = args.exclude_directories
    if args.exclude_file_extensions:
        package_file['file_extensions_exclude'] = args.exclude_file_extensions
        LOGGER.debug("Adding file extension excludes: '%s'", tuple(args.exclude_file_extensions))
    if args.files:
        package_file['files'] = args.files
        LOGGER.debug("Adding files: '%s'", tuple(args.files))
    if args.types:
        package_file['types'] = args.types
        LOGGER.debug("Adding types: '%s'", tuple(args.types))

    write_json(package_file_location, package_file)
    LOGGER.info("Successfully created new package")
    LOGGER.warning("New Package includes dummy versions and checksums")
    LOGGER.warning("Calling 'update' on this package is recommended before checking in.")
