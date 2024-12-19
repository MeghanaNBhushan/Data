import getpass
import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxargs
from lucxbox.tools.artifactoryw import artifactoryw_clean

LOGGER = lucxlog.get_logger()


def parse_args():
    """ Individual ArgumentParser adaptions regarding the script functionality

        Return value:
        ArgumentParser -- parsed arguments object to access given cli arguments
    """
    parser = argparse.ArgumentParser(description='The Artifactory script collection')
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    rt_sub = parser.add_subparsers(title='The Artifactory sub-commands')
    parse_args_clean(rt_sub)
    return parser.parse_args()


def parse_args_clean(rt_sub):
    """ Parse arguments for Artifactory cleanup

        :param rt_sub: The Artifactory sub parser
    """
    clean_args = rt_sub.add_parser('clean', help='Cleaning in Artifactory.')
    clean_args.add_argument('--url',
                            dest='artifactory_url',
                            required=True,
                            help='The Artifactory URL.')
    clean_args.add_argument('-r', '--repository',
                            dest='artifactory_repository',
                            required=True,
                            help='The Artifactory repository.')
    clean_args.add_argument('--include-path-pattern',
                            dest='include_path_pattern',
                            help='''Search only files whose path (excluding file name) matches pattern,
                                 using wildcard matching.
                                 A pattern can use '*' and '?' as wildcards.
                                 Example: '/path/to/dir*/where/file/is/?tored'.''')
    clean_args.add_argument('--exclude-list',
                            help='''Comma-separated list of files to skip.
                                 Pattern is {repo}/{path}/{name}. 
                                 Example: 'project-repository/path/to/item.zip,project-repository/path/to/item.jar'.''')
    clean_args.add_argument('-t', '--retention-period',
                            dest='retention_period',
                            required=True,
                            help='''Time periods are specified with a number and one of the following suffixes:
                                 - milliseconds "ms"
                                 - seconds "s"
                                 - minutes "minutes"
                                 - days "d"
                                 - weeks "w"
                                 - months "mo"
                                 - years "y"
                                 For example: -t=5d''')
    clean_args.add_argument('-df', '--domain-field',
                            dest='domain_field',
                            choices=['c', 'dl'],
                            required=True,
                            help='''The Artifactory AQL domain field.
                                    - c , `created`    When the item was created.
                                    - dl, `downloaded` The last time an item was downloaded.''')
    clean_args.add_argument('-u', '--username',
                            default=getpass.getuser(),
                            help='User for accessing Artifactory (default: current user).')
    clean_args.add_argument('-p', '--password',
                            help='Password for accessing Artifactory (prompt if not provided).')
    clean_args.add_argument('--dry-run',
                            default=False,
                            action='store_true',
                            help='Set to True to disable communication with the Artifactory.')
    clean_args.set_defaults(func=clean)


def clean(args):
    """Calls the subparser implementation for Artifactory cleanup

    Arguments:
        args Object -- Object containing all passed arguments
    """
    args.password = args.password or prompt_password(args.username)

    LOGGER.info('Execution parameters:')
    LOGGER.info('Artifactory URL: `%s`.', args.artifactory_url)
    LOGGER.info('Artifactory repository: `%s`.', args.artifactory_repository)

    if args.include_path_pattern:
        LOGGER.info('Include path pattern: `%s`.', args.include_path_pattern)
    if args.exclude_list:
        args.exclude_list = [item.strip() for item in args.exclude_list.split(',')]
        LOGGER.info('Exclude list:')
        for item in args.exclude_list:
            LOGGER.info('\t`%s`', item)

    LOGGER.info('Retention period: `%s`.', args.retention_period)
    LOGGER.info('Domain field: `%s`.', args.domain_field)
    LOGGER.info('Dry-Run: `%s`.', args.dry_run)

    artifactoryw_clean.clean(args)


def prompt_password(username):
    return getpass.getpass(prompt='Enter the Artifactory password for user "{}": '.format(username))


def main():
    """Main function to call when this script is called directly and not imported"""
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
