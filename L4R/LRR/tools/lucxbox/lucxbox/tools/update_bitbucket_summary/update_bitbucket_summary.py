#!/usr/bin/env python3
""" Script to update summary table in comment on Bitbucket PR page
"""

import os
import sys
import re
import logging
import argparse
import typing
import stashy
import urllib3

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxargs, lucxlog
from lucxbox.tools.update_bitbucket_summary.util import read_json_file


def positive_int(value: str) -> typing.Optional[int]:
    """Type check for argparse checks if integer larger than zero
    """
    if int(value) > 0:
        return int(value)
    return None


def nonempty_str(value: str) -> typing.Optional[str]:
    """Non-empty string type check for argparse
    """
    if len(value) > 0:
        return value
    return None


def parse_args() -> argparse.Namespace: # pragma: no cover
    """Adds and parses command line arguments

    Returns:
      Command line arguments
    """
    parser = argparse.ArgumentParser()
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    subparsers = parser.add_subparsers(dest='source', title='Source')
    subparsers.required = True
    add_inline_subparser(subparsers)
    add_file_subparser(subparsers)
    add_common_args(subparsers)

    return parser.parse_args()


def add_inline_subparser(subparsers) -> None: # pragma: no cover
    """ Add subparser for specifying parameters on the command-line.
    """
    inline_parser = subparsers.add_parser('inline', help='Update Bitbucket summary report with inline parameters')
    inline_parser.add_argument('--prid', required=True, dest="pr_id", type=positive_int, help='Pull request ID')
    inline_parser.add_argument('--build-number', required=True, type=positive_int, help='Build number')

    inline_parser.add_argument('--build-variant', required=True, type=nonempty_str, help='Build variant')
    inline_parser.add_argument('--tool', required=True, type=nonempty_str, help='Reporting tool name')
    inline_parser.add_argument('--result', required=True, type=nonempty_str, help='Result of tool execution')
    inline_parser.add_argument('--details', required=False, type=nonempty_str,
                               help='Detail field of summary table. '
                                    'Usually link to full report',
                               default=[], nargs='+')
    inline_parser.add_argument('-c', '--components', required=False, type=nonempty_str,
                               help='List of components',
                               default=[], nargs='+')
    inline_parser.add_argument('--comment', required=False, type=nonempty_str,
                               help='Additional comments to display',
                               default=None)


def add_file_subparser(subparsers) -> None: # pragma: no cover
    """ Add subparser to read parameters from the input file.
    """
    file_parser = subparsers.add_parser('file', help='Update Bitbucket summary report using summary JSON file')
    file_parser.add_argument('--summary-json', required=True, type=nonempty_str,
                             help='JSON file name of summary')


def add_common_args(subparsers) -> None: # pragma: no cover
    """ Add common arguments to each sub parser.
    """
    for subparser in subparsers.choices.values():
        subparser.add_argument('-u', '--user', required=True, type=nonempty_str, help='System user username')
        subparser.add_argument('-p', '--password', required=True, type=nonempty_str, help='System user password')
        subparser.add_argument('-bu', '--bitbucket-url', required=False, type=nonempty_str, help='Bitbucket URL',
                               default='https://sourcecode01.de.bosch.com')
        subparser.add_argument('-br', '--bitbucket-repo', required=True, type=nonempty_str,
                               help='Bitbucket repo name')
        subparser.add_argument('-bp', '--bitbucket-project', required=True, type=nonempty_str,
                               help='Bitbucket project name')


def init_args_from_summary_file(file_name: str, args: argparse.Namespace) -> argparse.Namespace:
    """ Read and initialize the arguments from input JSON file
    """
    summary_data: dict = read_json_file(file_name)
    args.__dict__['pr_id'] = summary_data['pr_id']
    args.__dict__['build_number'] = summary_data['build_number']
    args.__dict__['build_variant'] = summary_data['variant']
    args.__dict__['tool'] = summary_data['tool']
    args.__dict__['result'] = summary_data['result']
    args.__dict__['details'] = summary_data['details']
    args.__dict__['components'] = summary_data['components']
    args.__dict__['comment'] = summary_data['comment']
    return args


class UpdateBitbucketSummary:
    comment_start_token = '### Build №'

    def __init__(self,
                 bitbucket: stashy.client.Stash,
                 bitbucket_project: str,
                 bitbucket_repo: str,
                 pr_id: int,
                 build_variant: str,
                 result: str,
                 tool: str,
                 details: str,
                 components: list,
                 comment: str,
                 build_number: int,
                 logger: typing.Optional[logging.RootLogger] = None,
                 ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.bitbucket: stashy.client.Stash = bitbucket
        self.pr: stashy.pullrequests.PullRequest = \
            bitbucket.projects[bitbucket_project].repos[bitbucket_repo].pull_requests[pr_id]  # pylint: disable=C0103
        self.build_variant = build_variant
        self.result = result
        self.tool = tool
        self.details = details or '-'
        self.components = ' '.join(map(lambda component: f'`{component}`', components)) or '-'
        self.comment = comment or '-'
        self.build_number = build_number

    def update(self) -> None:
        comment = self._get_latest_summary_comment()
        if comment is None:
            self.logger.debug('No comment with report table found. Creating new one.')
            self.pr.comment(commentText=self._get_new_comment_text())
            return None

        if comment['text'].startswith(f'{self.comment_start_token}{self.build_number}'):
            self.logger.debug('Build number on comment is matching, updating old comment.')
            try:
                # pylint: disable=fixme
                # TODO: rewrite to use update comment when it will be supported in stashy
                self.pr.delete_comment(comment['id'], comment['version'])
            except stashy.errors.GenericException as exc:
                self.logger.error('Could not delete old comment: %s', exc)
                raise
            self.pr.comment(commentText=self._get_updated_comment_text(comment['text']))
        else:
            self.logger.debug('Build number on comment is older than current build number. Deleting old comment.')
            try:
                self.pr.delete_comment(comment['id'], comment['version'])
            except stashy.errors.GenericException as exc:
                self.logger.warning('Could not delete old comment: %s', exc)
                # If we cannot delete a comment then it is most probably because
                # the comment has replies. Try to create a new comment anyway
            self.logger.debug('Creating comment with new build number')
            self.pr.comment(commentText=self._get_new_comment_text())
        return None

    def _get_latest_summary_comment(self) -> typing.Optional[dict]:
        """ Get and return the comment dictionary object which contain start
            token in the text field. If there is no comment containing start
            token, return None
        """
        for activity in self.pr.activities(fromType='COMMENT'):
            if activity['action'] == 'COMMENTED' and self.comment_start_token in activity['comment']['text']:
                return activity['comment']
        return None

    def _get_new_comment_text(self) -> str:
        """ Returns the text of the new summary comment
        """
        return f'{self.comment_start_token}{self.build_number} Report\n\n' \
               '|**Variant**|**Tool**|**Result**|**Details**|**Components**|**Comment**|\n' \
               '|-|-|-|-|-|-|\n' \
               f'{self._get_table_rows(self.build_variant)}\n\n' \
               f'###### Reply to this comment to make it permanent.'

    def _get_table_rows(self, build_variant: str = '') -> str:
        """ Create table rows. Bitbucket uses Markdown for tables and cannot
            create tables with multi-line cells. This function will simulate
            multi-line cells with multiple table rows.

            Example:
                Result of the function run with the single-line data:
                ||tool-x|OK|-|-|-|

                Result of the function run with the comment section containing
                data "str1\nstr2"
                ||tool-x|OK|-|-|str1|
                ||||||str2|
        """
        table_rows: str = ''
        lists = [[build_variant],
                 [self.tool],
                 self.result.split('\n'),
                 self.details.split('\n'),
                 [self.components],
                 self.comment.split('\n')]
        max_elements: int = max(len(lst) for lst in lists)
        for lst in lists:
            lst.extend([''] * (max_elements - len(lst)))

        for row in zip(*lists):
            table_rows += '|' + '|'.join([str(item) for item in row]) + '|\n'
        return table_rows

    def _get_updated_comment_text(self, text: str) -> str:
        """ Insert newly created rows into the table under the variant name
            that they belong. If there is no such variant in the table, put
            the rows for this variant at the end of the table.

            Example:
                The following examples are for single-row inserts, but multi-row
                inserts work in the same way.

                We have following table in the input text:
                    (truncated input)
                    |-|-|-|-|-|-|\n
                    |V1|tool-x|OK|-|-|-|\n
                    ||tool-z|OK|-|-|-|\n
                    |V2|tool-x|OK|-|-|-|\n
                    \n
                    (truncated input)

                If we are trying to insert the rows for the variant V1 and
                NEW_TOOL, then regex in the re.subn will match rows 2 and 3
                of the input text. Rows 2 and 3 will be replaced with the
                concatenated version of the 2,3, and the new row without
                the variant name.
                Expected result:
                    (truncated input)
                    |-|-|-|-|-|-|\n
                    |V1|tool-x|OK|-|-|-|\n
                    ||tool-z|OK|-|-|-|\n
                    ||NEW_TOOL|OK|-|-|-|\n
                    |V2|tool-x|OK|-|-|-|\n
                    \n
                    (truncated input)

                If we are trying to insert rows for the variant that is not in the
                table (variant V3 and tool NEW_TOOL), then first replace will not
                return a value, and rows will be inserted at the end of the table
                (regex in re.sub matches the whole table).
                Expected result:
                    (truncated input)
                    |-|-|-|-|-|-|\n
                    |V1|tool-x|OK|-|-|-|\n
                    ||tool-z|OK|-|-|-|\n
                    |V2|tool-x|OK|-|-|-|\n
                    |V3|NEW_TOOL|OK|-|-|-|\n
                    \n
                    (truncated input)
        """
        new_rows = self._get_table_rows()
        new_text, replaced = re.subn(r'^(\|' + self.build_variant + r'\|.*?\n(?:^\|\|.*\n)*)',
                                     fr'\g<1>{new_rows}', text, flags=re.MULTILINE)
        if not replaced:
            new_rows = self._get_table_rows(self.build_variant)
            new_text = re.sub(r'^((?:\|.*?\n)+)', fr'\g<1>{new_rows}', text,
                              flags=re.MULTILINE)
        return new_text


def main():
    logger = lucxlog.get_logger()
    args = parse_args()

    verify_ssl = True
    if args.log_level == 'DEBUG':
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        verify_ssl = False

    logger.setLevel(args.log_level)

    if args.source == 'file':
        args = init_args_from_summary_file(args.summary_json, args)

    bitbucket = stashy.connect(args.bitbucket_url,
                               args.user,
                               args.password,
                               verify=verify_ssl,
                               )
    report_updater = UpdateBitbucketSummary(bitbucket,
                                            args.bitbucket_project,
                                            args.bitbucket_repo,
                                            args.pr_id,
                                            args.build_variant,
                                            args.result,
                                            args.tool,
                                            args.details,
                                            args.components,
                                            args.comment,
                                            args.build_number,
                                            logger,
                                            )
    report_updater.update()


if __name__ == '__main__':  # pragma: no cover
    main()
