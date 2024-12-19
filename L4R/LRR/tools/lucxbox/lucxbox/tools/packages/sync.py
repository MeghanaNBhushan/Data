import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog

from lucxbox.tools.packages.helper import clone_repository
from lucxbox.tools.packages.helper import fetch_repository
from lucxbox.tools.packages.helper import clean_repository
from lucxbox.tools.packages.helper import archive_package_files
from lucxbox.tools.packages.helper import extract_archive
from lucxbox.tools.packages.helper import move_files

from lucxbox.tools.packages.package import get_packages
from lucxbox.tools.packages.package import add_hash_calc_version

LOGGER = lucxlog.get_logger()


def api(parser):
    parser_sync = parser.add_parser('sync', help='Sync package with remote')

    parser_input = parser_sync.add_mutually_exclusive_group(required=False)
    parser_input.add_argument('-c', '--commit', dest='ref',
                              help='The commit to checkout from remote repository')
    parser_input.add_argument('-t', '--tag', dest='ref',
                              help='The tag to checkout from remote repository')

    parser_sync.set_defaults(func=sync_with_remote)


def sync_with_remote(args):
    packages = get_packages(args.root, args.package_file_name,
                            args.time_based, args.packages_filter, args.filter_type, "update")
    if len(packages) > 1 and args.ref:
        LOGGER.warning(
            "Syncing more than one package with the same git reference. Is this really what you want?")

    for package in packages:
        last_ref = package.get_sync_git_ref()
        if args.ref:
            ref = args.ref
        elif last_ref:
            ref = last_ref
            LOGGER.info("Since no ref is given, the ref from the last sync will be taken.")
        else:
            LOGGER.error("No reference for sync available!")
            sys.exit(1)

        LOGGER.info("Syncing package with remote reference '%s'...", ref)
        url, clone, path, includes = package.get_remote_config()
        clone_abs_path = os.path.join(os.getcwd(), clone)
        package.erase()
        archive_name = os.path.basename(url).replace('.git', '')
        archive_path = os.path.join(clone_abs_path, archive_name + '.zip')
        extract_path = clone_abs_path
        if not os.path.isdir(clone_abs_path):
            clone_repository(clone_abs_path, url)

        fetch_repository(clone_abs_path, ref)
        clean_repository(clone_abs_path)
        extract_path = clone_abs_path
        for include in includes:
            archive_package_files(extract_path, archive_name, ref, os.path.join(path, include))
            extract_archive(archive_path, extract_path)
            move_files(extract_path, package.get_abs_path(), path)

        md5 = package.calculate_md5(only_tracked_files=False)
        md5 = add_hash_calc_version(md5, package.get_hash_calc_version())
        package.update_sync_status(ref, md5)
        LOGGER.info("The sync has been successful!")
