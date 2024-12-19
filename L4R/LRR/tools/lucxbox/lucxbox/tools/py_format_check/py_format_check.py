#!/usr/bin/env python3.7
# pylint: disable=logging-fstring-interpolation
import sys
import argparse
import logging
from pathlib import Path

try:
    import format_tracker
except ImportError:
    from lucxbox.tools.py_format_check import format_tracker


def main():
    # Create top-level parser
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Create another parent parser to share args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="""Select verbosity level. Default is 0.
              Values above -vv are casted to DEBUG""",
    )

    # Add common arguments
    parser.add_argument(
        "-d",
        "--dir_path",
        default=str(Path(__file__).resolve().parent),
        type=str,
        help="""Directory path in a repository. Not necessarily the root.
              A single valid flake8 configuration file
              in the project's root dir is required.
              This defaults to the current script's dir""",
    )
    parent_parser.add_argument(
        "-o",
        "--output",
        default="flake8_run.txt",
        type=str,
        help="File name to be saved in repo root for flake8 output",
    )
    parent_parser.add_argument(
        "-pkl",
        "--pickle",
        type=str,
        help="Name for DataFrame pickle of flake8 run. Saved in repo root",
    )

    # Create subparsers
    subparsers = parser.add_subparsers(help="Command to run")
    subparsers.dest = "command"
    subparsers.required = True

    # Create parser for lint repo
    repo_parser = subparsers.add_parser(
        "lintAll",
        parents=[parent_parser],
        help="""Lint all *.py files from a whole project repository.
              Returns zero exit code iff flake8 ran successfully
              or if the output could be saved.
              See https://flake8.pycqa.org/en/latest/user/configuration.html
              """,
    )
    repo_parser.set_defaults(func=format_tracker.lint_all)

    # Create parser for lint diff
    branch_parser = subparsers.add_parser(
        "lintDiff",
        parents=[parent_parser],
        help="""Lint only the *.py files found in the diff from
              the current checked out branch against some target branch.
              Returns zero exit code iff flake8 ran successfully
              or if the output could be saved""",
    )
    branch_parser.add_argument(
        "-tb",
        "--target_branch",
        default="origin/develop",
        type=str,
        help="Branch to do the diff against. Defaults to 'origin/develop'",
    )
    branch_parser.set_defaults(func=format_tracker.lint_diff)

    # Create parser for lint comparison
    compare_parser = subparsers.add_parser(
        "compareLint",
        help="""Compare two linting results from flake8 runs.
              Requires a valid baseline pickle (see lint_repo)
              and newly added changes (see lint_diff).
              Returns zero exit code iff no new linting errors
              were added w.r.t. the baseline""",
    )
    compare_parser.add_argument(
        "-b",
        "--baseline",
        type=str,
        help="""Pandas DataFrame pickle from a flake8 run
              used as a baseline as a comparison""",
    )
    compare_parser.add_argument(
        "-l",
        "--local_changes",
        type=str,
        help="""Pandas DataFrame pickle from a flake8 run
              to be compared against baseline""",
    )
    compare_parser.set_defaults(func=format_tracker.compare_linting)

    # Parse and keep only the function arguments
    args = parser.parse_args()
    args = vars(args)

    # Define logging level
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, args.pop("verbose"))]
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")

    # Call corresponding function
    func = args.pop("func")
    logging.debug(f"Running command {args.pop('command')} with flags:")
    for key, value in args.items():
        logging.debug(f"     {key}:    {value}")

    err = func(**args)

    return err


if __name__ == "__main__":
    sys.exit(main())
