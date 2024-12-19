#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The artifacts_cache downloads artifacts from a given artifactory path and stores them in a local cache.
"""
import argparse
import parser
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog, lucxargs
from lucxbox.tools.artifactory_cache.ArtifactoryCache import ArtifactCache


LOGGER = lucxlog.get_logger(__file__)

ARTIFACTORY_URL = 'https://rb-artifactory.bosch.com/artifactory'
CACHE_DIR = os.path.abspath(os.path.join(os.path.expanduser('~'), 'artifactory_cache'))


def parse_arguments(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser = add_arguments(parser)
    parser = lucxargs.add_log_level(parser)

    args = parser.parse_args(args)
    check_arguments(parser, args)
    return args

def add_arguments(arg_parser):
    arg_parser.add_argument('-u', '--user',
                            help='User name for Artifactory')
    arg_parser.add_argument('-a', '--artifact-path',
                            help='The artifact path and filename to fetch')
    arg_parser.add_argument('-p', '--password',
                            help="User password or API key for Artifactory "
                                 "(API-key can also be provided using an environment variable 'ARTIFACTORY_API_KEY'")
    arg_parser.add_argument('--url',
                            help='Base URL of Artifactory',
                            default=ARTIFACTORY_URL)
    arg_parser.add_argument('-o', '--output-path',
                            help='The output filename and path for the artifact')
    arg_parser.add_argument('--clear', action='store_true',
                            help="Clear artifactory cache before download")
    arg_parser.add_argument('--track-changes', action='store_true',
                            help="Re-download cached files if the local file hash does not match the remote hash."
                                 " Use this for changing artifact like 'latest'")
    return arg_parser


def check_arguments(parser, args):
    if args.artifact_path:
        if not args.user:
            parser.error("You need to provide the user to access artifactory.")
        if not args.password and not os.getenv('ARTIFACTORY_API_KEY'):
            parser.error("You need to provide either a password or the apikey to authenticate.")
    elif not args.clear:
        parser.error("You need to provide either an artifact to fetch or '--clear'")


def main(args):
    try:
        args = parse_arguments(args)
    except parser.ParserError:
        LOGGER.error("Missing Arguments. You need to define either a password or the apikey to authenticate.")
        sys.exit(1)

    LOGGER.setLevel(args.log_level)

    cache = ArtifactCache(args.user, args.password, artifactory_url=args.url,
                          update_tracked_artifacts=args.track_changes)
    if args.clear:
        LOGGER.warning("Removing cache '%s'", CACHE_DIR)
        cache.clear(args.artifact_path)

    if not args.artifact_path:
        # no artifact to fetch was specified (clear only)
        return

    output_path = os.path.join(os.path.abspath('.'), args.artifact_path)
    if args.output_path:
        output_path = os.path.abspath(args.output_path)
    LOGGER.info("Output path will be '%s'", output_path)

    cache.get_artifact(args.artifact_path, output_path)


if __name__ == '__main__':
    main(sys.argv[1:])
