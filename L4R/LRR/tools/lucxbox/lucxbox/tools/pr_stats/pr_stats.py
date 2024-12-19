""" Pull Request Statistics generation """

import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.tools.pr_stats import pr_statistics
from lucxbox.tools.pr_stats.spacetime import Spacetime
from lucxbox.lib import lucxargs, lucxlog, bitbucket


def parse_args():
    description = "Pull Request Statistics generation"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-m', '--max-prs', required=False, type=int, default=9999,
                        help='Maximum number of pull requests to fetch from bitbucket (default: 9999).')
    parser.add_argument('--project', required=True)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--loc', action='store_true', default=False,
                        help='Calculate the line of code by duration (might take a long time).')
    parser.add_argument('-url', '--bitbucket_url', required=False, type=str, default="https://sourcecode.socialcoding.bosch.com",
                        help='Bitbucket URL root ( default: https://sourcecode.socialcoding.bosch.com ).')
    parser = lucxargs.add_log_level(parser)

    return parser.parse_args()


def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)
    LOGGER.debug("Creating pull requests statistics.")

    spacetime = Spacetime()
    prs = bitbucket.get_prs(args.max_prs, args.project, args.repo, args.username, args.password, args.bitbucket_url, args.loc)
    pr_statistics.get_pr_open(spacetime, prs, "open_prs.png")
    pr_statistics.get_pr_opened(spacetime, prs, "opened_prs.png")
    pr_statistics.get_pr_merged(spacetime, prs, "merged_prs.png")
    pr_statistics.get_pr_diff(spacetime, prs, "diff_prs.png")
    pr_statistics.get_pr_duration(spacetime, prs, "duration_prs.png")
    if args.loc:
        pr_statistics.get_loc_by_duration(spacetime, prs, "loc_by_duration_prs.png")


if __name__ == "__main__":
    LOGGER = lucxlog.get_logger()
    main()
