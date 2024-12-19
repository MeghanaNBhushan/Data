import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog

from lucxbox.tools.packages.package import get_packages

LOGGER = lucxlog.get_logger()


def api(parser):
    parser_remote = parser.add_parser('remote', help='Add remote configuration')

    parser_remote.add_argument('-u', '--url', dest='url', required=True,
                               help='The url of the remote repository')
    parser_remote.add_argument('-c', '--clone', dest='clone', required=True,
                               help='The clone directory of the remote repository')
    parser_remote.add_argument('-p', '--path', dest='path', default='.',
                               help='The path in the remote repository from where to include files')
    parser_remote.add_argument('-i', '--includes', dest='includes', default=['**'], nargs='+',
                               help='The wildcard patterns to include files from remote repository')

    parser_remote.set_defaults(func=add_remote)


def add_remote(args):
    packages = get_packages(args.root, args.package_file_name,
                            args.time_based, args.packages_filter, args.filter_type, "status")
    if len(packages) > 1:
        LOGGER.warning(
            "Adding the same remote configuration for more than one package. Is this really what you want?")

    path = args.path.replace('\\', '/')
    includes = []
    for include in args.includes:
        includes.append(include.replace('\\', '/'))

    clone_abs = os.path.abspath(args.clone)
    clone_rel = os.path.relpath(clone_abs, os.getcwd()).replace('\\', '/')
    for package in packages:
        LOGGER.info("Adding remote config for '%s'...", package.get_name())
        package.update_remote_config(args.url, clone_rel, path, includes)
        LOGGER.info("URL: '%s'", args.url)
        LOGGER.info("CLONE: '%s'", clone_rel)
        LOGGER.info("PATH: '%s'", path)
        LOGGER.info("INCLUDES: '%s'", ', '.join(includes))
        LOGGER.info("The remote config has been successfully added!")
