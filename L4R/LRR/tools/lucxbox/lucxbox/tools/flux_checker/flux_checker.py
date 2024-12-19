#!/bin/env python3
""" Wrapper for FQM tool to check if all flux files have no errors and can be opened in the flux GUI """

import argparse
import getpass
import os
import sys
import tempfile
from pathlib import Path
import requests


sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog, finder, lucxutils, lucxio
from lucxbox.lib.wildcards import matches_wildcard_pattern

LOGGER = lucxlog.get_logger()

ARTIFACTORY_URL = 'https://rb-artifactory.bosch.com/artifactory'
FLUX_REPOSITORY = 'flux-local/flux'


def parse_args():
    description = "Wrapper for FQM tool to check if all flux files have no " + \
                  "errors and can be opened in the flux GUI. " + \
                  "Unless specified explicitly, the tool will look in all subfolders for '.flux' files."
    parser = argparse.ArgumentParser(description=description)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    default_fqmdir = Path(tempfile.gettempdir()) / 'fqm'
    parser.add_argument('--fqm-version',
                        dest='fqmversion',
                        required=False,
                        help='Flux Quality Metrics version. Minimum 1.1. (e.g. "1.1.0.19", required)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fqm-dir',
                       dest='fqmdir',
                       default=default_fqmdir,
                       help='Flux Quality Metrics directory (default: user TEMP directory)')
    group.add_argument('--fqm-exe',
                       dest='fqmexe',
                       help='Flux Quality Metrics executable')
    subparsers = parser.add_subparsers(title='Flux checker sub-commands')
    parse_install(subparsers)
    parser_check(subparsers)

    return parser.parse_args()


def parse_install(subparsers):
    installer = subparsers.add_parser('install', help='Install FQM from Artifactory.')
    installer.add_argument('--user',
                           default=getpass.getuser(),
                           help='User for accessing Artifactory (default: current user)')
    installer.add_argument('--password',
                           help='Password for accessing Artifactory (prompt if not provided)')
    installer.set_defaults(func=install)


def install(args):
    version = args.fqmversion
    directory = args.fqmdir
    version_path = _version_path(directory, version)
    if not version_path.exists():
        LOGGER.info('FQM version %s was not found on local system. Try to download it from Artifactory.', version)
        user = args.user
        password = args.password or _prompt_password(args.user)
        download_from_artifactory(user, password, version, directory, version_path)
    if version_path.exists():
        fqm_executable = _find_fqm_executable(version_path)
        LOGGER.info('FQM installed at "%s".', fqm_executable)


def _prompt_password(user):
    return getpass.getpass(prompt='Enter the Artifactory password for user "{}": '.format(user))


def version_exists_in_artifactory(session, version):
    response_version = session.get(ARTIFACTORY_URL + '/api/storage/{}'.format(FLUX_REPOSITORY))
    response_version.raise_for_status()
    folders = [child['uri'].lstrip('/') for child in response_version.json()['children']]
    versions = [folder for folder in folders if not folder == 'jenkins' and not folder.startswith(('0', '1.0'))]
    if version in versions:
        LOGGER.debug('FQM version %s does exist', version)
        return True
    else:
        LOGGER.error('FQM version %s does not exist or is not supported. Minimum supported version: 1.1. Available versions: %s',
                     version,
                     ', '.join(versions))
        return False


def download_from_artifactory(user, password, version, directory, version_path):
    with _login(user, password) as session:
        if version_exists_in_artifactory(session, version):
            filename = 'Flux.QualityMetrics-{}-unsupported-{}.zip'.format(_platform(), version)
            url = '{}/list/{}/{}/standalone_tools/{}/{}'.format(ARTIFACTORY_URL, FLUX_REPOSITORY, version, _platform(), filename)
            zipfile_path = lucxio.download(url=url,
                                           filename=filename,
                                           directory=directory,
                                           session=session)
            LOGGER.info('Extract FQM zip file %s to %s', zipfile_path, version_path)
            directory_prefix = 'Publish/Flux.QualityMetrics/{}/'.format(_platform().capitalize())
            lucxutils.zipfile_extractall_subdirectory(zipfile_path, version_path, directory_prefix)


def _platform():
    return 'windows' if sys.platform == 'win32' else 'linux'


def _login(user, password):
    session = requests.Session()
    session.auth = user, password
    return session


def _version_path(directory, version):
    return Path(directory) / 'FQM' / version


def _find_fqm_executable(version_path):
    binary = 'FQM.exe' if sys.platform == 'win32' else 'FQM'
    executable_path = Path(version_path, binary).absolute()
    if not executable_path.exists():
        LOGGER.error('FQM does not exist at "%s". Please install it. For details, see "python flux_checker.py --help".', executable_path)
        sys.exit(1)
    if not lucxutils.is_exe(str(executable_path)):
        LOGGER.error('FQM installed at "%s" is not an executable', executable_path)
        sys.exit(1)
    return str(executable_path)


def parser_check(subparsers):
    checker = subparsers.add_parser('check', help='Check flux file(s).')
    checker.add_argument('-j', dest='threads', default=1, type=int, required=False,
                         help='Number of threads to use parallel (default is 1).')
    checker.add_argument('--whitelist', '-w', type=argparse.FileType('r'), required=False,
                         help='File containing a list of whitelisted files (one line for each file).')
    checker.add_argument('--flux-model',
                         dest='fluxmodel',
                         help='Flux model file (default: all .flux files in subfolders)')
    checker.set_defaults(func=check)


def check(args):
    if args.fqmexe:
        if lucxutils.is_exe(args.fqmexe):
            fqm_executable = args.fqmexe
        else:
            raise TypeError("'{}' not an executable.".format(args.fqmexe))
    else:
        if args.fqmversion:
            fqm_executable = _find_fqm_executable(_version_path(args.fqmdir, args.fqmversion))
        else:
            raise ValueError("'--fqm-version' required with '--fqm-dir'.")

    LOGGER.info('FQM installed at "%s".', fqm_executable)
    matches = [args.fluxmodel] if args.fluxmodel else finder.get_files_with_ending(endings=[".flux"])

    file_names = remove_whitelisted_files(matches, args.whitelist) if args.whitelist else matches

    LOGGER.debug("Executing fqm check for %s files with %s thread(s).", len(file_names), args.threads)
    cmds = [[fqm_executable, file_name, "--out", file_name + ".json"] for file_name in file_names]
    results = lucxutils.parallel_execute(cmds, args.threads)

    count = 0
    for cmd in results:
        out, err, returncode = results[cmd]
        file_name = cmd
        if returncode != 0:
            LOGGER.error("Error while processing '%s':", file_name)
            LOGGER.error("stdout:\n%s", out)
            LOGGER.error("stderr:\n%s", err)
            count = count + 1
    LOGGER.info("Error in %s files", count)
    return count


def remove_whitelisted_files(matches, whitelist):
    patterns = []
    file_names = []
    for line in whitelist.readlines():
        pattern = line.strip()
        if pattern.startswith('#'):
            LOGGER.debug("Line starts with '#'. Seems to be a comment'%s'", pattern)
        else:
            patterns.append(pattern)
    for match in matches:
        file_names.append(match)
        for pattern in patterns:
            if matches_wildcard_pattern(match, pattern):
                LOGGER.debug("Removing '%s' since it is whitelisted by pattern '%s'.", match, pattern)
                file_names.remove(match)
                break
    return file_names


def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
