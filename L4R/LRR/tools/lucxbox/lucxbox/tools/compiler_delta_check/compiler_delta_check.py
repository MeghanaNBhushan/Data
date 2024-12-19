#!/usr/bin/env python3
""" Script to create and compare compiler warnings
"""
import os
import sys
import re
import json
import argparse
import pprint
import subprocess
import typing
from collections import Counter
import jsonschema
from jinja2 import Environment, FileSystemLoader

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxargs, lucxlog

LOGGER = lucxlog.get_logger()


def positive_int(value: str) -> typing.Optional[int]:
    if int(value) > 0:
        return int(value)
    return None


def nonempty_str(value: str) -> typing.Optional[str]:
    if len(value) > 0:
        return value
    return None


def parse_args() -> argparse.Namespace:
    """Adds and parses command line arguments
    """
    description = "A Compiler warnings delta checker."
    parser = argparse.ArgumentParser(description=description)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    parser.add_argument('-cf', '--changed-files', required=True, type=nonempty_str,
                        help='Name of the file containing list of changed files')
    parser.add_argument('--warnings-baseline-file', required=True, type=nonempty_str,
                        help='Input file containing baseline')
    parser.add_argument('--warnings-file', required=True, type=nonempty_str,
                        help='Input file containing current warnings')
    parser.add_argument('--output-html', required=False, default=None, type=nonempty_str,
                        help='Output HTML report file name')
    parser.add_argument('--output-json', required=False, default=None, type=nonempty_str,
                        help='Output JSON report file name')
    parser.add_argument('--summary-json', required=False, type=nonempty_str,
                        help='JSON file name of summary')
    parser.add_argument('-tf', '--threshold-file', required=False, type=nonempty_str,
                        help='JSON file containing thresholds for tools')
    parser.add_argument('--build-variant', required=True, type=nonempty_str, help='Build variant')
    parser.add_argument('--ignore-type', required=False, type=nonempty_str, default=list(), nargs='+',
                        help='Remove specified warning type from comparison')
    parser.add_argument('--prid', required=False, type=positive_int, default=None, help='Pull request ID')
    parser.add_argument('--build-number', required=False, type=positive_int, default=None, help='Build number')
    parser.add_argument('--target-branch', required=False, type=nonempty_str, default='develop',
                        help='Target branch name or commit id. Default is develop')
    parser.add_argument('--source-branch', required=False, type=nonempty_str, default='@',
                        help='Current branch or commit id. Default is current HEAD')

    return parser.parse_args()


def is_git_repo(path: str = '.') -> bool:
    cmd = 'git rev-parse'
    null_file = open(os.devnull, 'w')
    cmd_result = subprocess.run(cmd.split(), check=False, stderr=null_file, stdout=null_file, cwd=path)
    if cmd_result.returncode != 0:
        return False
    return True


def get_git_renames(dst_branch: str, src_branch: str) -> list:
    """ Get a list of renamed files between two commits from Git summary
    """
    if not is_git_repo():
        LOGGER.warning('Not in git repository, skipping renamed files check')
        return list()

    regex: str = r'rename\s+([^{]+)\s+=>\s+([^}\s]+)|(\S+){(\S+)\s+=>\s+(\S+)}'
    cmd: str = f'git diff --summary {dst_branch} {src_branch}'
    cmd_output = subprocess.run(cmd.split(), check=False, capture_output=True)
    if cmd_output.returncode != 0:
        LOGGER.warning('Git command "%s" returned status %s, message was: %s', cmd, cmd_output.returncode,
                       cmd_output.stderr)
        LOGGER.warning('Skipping search for renamed files. Results may be inaccurate...')
        return list()
    matches = [re.search(regex, line) for line in cmd_output.stdout.decode().split("\n")]
    renames = [tuple(filter(None, match.groups())) for match in matches if match is not None]
    result = list()
    for rename in renames:
        if len(rename) == 2:
            result.append((rename[0], rename[1]))
        elif len(rename) == 3:
            result.append((f'{rename[0]}{rename[1]}', f'{rename[0]}{rename[2]}'))
    return result


def validate_json(schema_file: str, data: dict) -> None:
    """Validate JSON data against provided schema file
    """
    with open(schema_file, 'r') as schf:
        schema = json.load(schf)

    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError:
        LOGGER.error('Failed validation against schema with title "%s"', schema['title'])
        raise


def write_json_file(filename: str, data: typing.Union[dict, list], schema_file: str) -> None:
    validate_json(schema_file, data)
    with open(filename, 'w') as output_file:
        output_file.write(json.dumps(data))


def read_thresholds_file(tool: str, thresholds_file: str) -> typing.Counter:
    """Read content of thresholds file for specified tool

       Thresholds file is a JSON file with following schema:

       { "tool_name": [
         {
          "threshold": -1,
          "component_name": "AUTOSAR"
         }, ...
         ], ...
       }

      Arguments:
        tool: Name of the tool
        thresholds_file: Name of the thresholds file

      Raises:
        IOError
    """
    schema_file = f'{os.path.dirname(__file__)}/schemas/thresholds.json'
    thresholds: typing.Counter = Counter()
    with open(thresholds_file, 'r') as thf:
        data = json.load(thf)
        validate_json(schema_file, data)
        tool_thresholds = data[tool]
        for threshold in tool_thresholds:
            thresholds.update({threshold['component_name']: threshold['threshold']})
    return thresholds


def strip_drive(line: str) -> str:
    """Remove windows drive letter from path string
    """
    position: int = line.find(':\\')
    if position != -1:
        return line.rstrip()[position + 2:]
    return line


def get_changed_files(file_name: str) -> list:
    """Get files changed in PR from lucx provided CHANGED_FILES_FILE
    """
    with open(file_name, 'r') as changed_files_file:
        files_list = [strip_drive(line.strip()) for line in changed_files_file.readlines() if line.rstrip() != '']
        return files_list


def get_warnings(file_name: str) -> dict:
    """Read compiler warnings from JSON formatted file
    """
    schema_file = os.path.join(os.path.dirname(__file__), 'schemas', 'compiler_warnings.json')
    with open(file_name, 'r') as wfile:
        warnings = json.load(wfile)
    validate_json(schema_file, warnings)
    return warnings


class CLWarning:
    """Compiler/Linker warning object
    """

    def __init__(self, warning_data: dict):
        self.file_path = warning_data['file_path']
        self.row = warning_data['row']
        self.column = warning_data['column']
        self.message = warning_data['message']
        self.components = warning_data['components']
        self.teams = warning_data['teams']
        self.severity = warning_data['severity']
        self.type_name = warning_data['type_name']
        self.quantity = None
        self.domain = warning_data['domain']
        self.pr_related = True

    def __eq__(self, other: 'CLWarning') -> bool:
        select_keys = ['file_path', 'message', 'components', 'severity', 'type_name']
        return self.__class__ == other.__class__ and \
               ({k: v for k, v in self.__dict__.items() if k in select_keys} ==
                {k: v for k, v in other.__dict__.items() if k in select_keys})

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__})'

    def __hash__(self) -> int:
        severity = self.severity or ''
        type_name = self.type_name or ''

        return hash(self.file_path + str(self.message) + repr(self.components) +
                    severity + type_name)


class CLWarnings(Counter):
    """Object containing list of warnings
    """

    def __init__(self, warnings: dict = None):
        super().__init__()
        if warnings:
            for warning in warnings:
                super().update({CLWarning(warning): warning['quantity']})

    def __sub__(self, other):
        result = CLWarnings()
        diff = super().__sub__(other)
        for elem, count in diff.items():
            result.update({elem: count})
        return result

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined. Use Counter(iterable) instead.')

    def filter_by_domain(self, domain: str) -> 'CLWarnings':
        """ Filter warnings that belong to specified domain
        """
        result = CLWarnings()
        for elem, count in self.items():
            if elem.domain == domain:
                result.update({elem: count})
        return result

    def filter_by_types(self, types: list) -> 'CLWarnings':
        """ Filter out specific warning types

        Args:
          types: list of type strings to filter out
        """
        result = CLWarnings()
        types_upper = [t.upper() for t in types]
        for elem, count in self.items():
            if (elem.type_name is None) or (elem.type_name.upper() not in types_upper):
                result.update({elem: count})
        return result

    def filter_by_component(self, component: str) -> 'CLWarnings':
        """Filter out warnings with specified component
        """
        result = CLWarnings()
        for elem, count in self.items():
            if component.upper() not in map(lambda team: team.upper(), elem.teams):
                result.update({elem: count})
        return result

    def get_warnings_per_component(self) -> typing.Counter:
        """ Get warning count per component
            If warning belongs to multiple components, adds warnings quantity to each component
        """
        result: typing.Counter = Counter()
        for elem, count in self.items():
            for team in elem.teams:
                result.update({team: count})
        return result

    def filter_with_changed_files(self, changed_files: list) -> 'CLWarnings':
        """Filter warnings Counter by removing counter items that do not contain paths from changed files list

        Args:
          changed_files: list of changed files in form of 'dir/subdir/subdir2/filename
        """
        result = CLWarnings()
        LOGGER.debug('Changed files are: %s', changed_files)
        LOGGER.info('Checking changed files...')
        for warning, count in self.items():
            file = warning.file_path
            path = strip_drive(os.path.abspath(file))
            if any(map(lambda changed_file, path=path: changed_file.endswith(path), changed_files)):
                LOGGER.debug('Path %s is found in changed files file', path)
                result.update({warning: count})
        return result

    def apply_renames(self, renames: typing.List[typing.Tuple[str, str]]) -> 'CLWarnings':
        if renames:
            for warning in self.keys():
                for source, destination in renames:
                    if warning.file_path.endswith(source):
                        warning.file_path = destination
        return self


class CompilerWarningsDeltaCheck: #pylint: disable=R0902
    """ Class to delta check compiler warnings
    """

    def __init__(self, args: argparse.Namespace) -> None:
        LOGGER.debug('Script called with following args:\n%s\n', pprint.pformat(vars(args)))
        LOGGER.debug('Environment variables are: %s', str(os.environ))

        self.tool = 'compiler'

        self.warnings_baseline_file = args.warnings_baseline_file
        self.warnings_file = args.warnings_file
        self.threshold_file = args.threshold_file
        self.changed_files = args.changed_files
        self.ignore_type = args.ignore_type
        self.output_html = args.output_html
        self.output_json = args.output_json
        self.build_variant = args.build_variant
        self.summary_json = args.summary_json
        self.target_branch = args.target_branch
        self.source_branch = args.source_branch
        self.prid = args.prid or int(os.getenv('LUCX_PULL_REQUEST', '0'))
        self.build_number = args.build_number or int(os.getenv('BUILD_NUMBER', '0'))
        if self.prid <= 0:
            raise ValueError(
                'If the script run as part of the PR, but LUCX_PULL_REQUEST environment variable is not set or prid '
                'is not provided in the command-line arguments')
        if self.build_number <= 0:
            raise ValueError(
                'Could not get environment variable BUILD_NUMBER or build number is not provided in the '
                'command-line arguments')

    def __call__(self):
        """Main method
        """

        try:
            baseline = get_warnings(self.warnings_baseline_file)
            warnings = get_warnings(self.warnings_file)

            baseline_warnings = CLWarnings(baseline) \
                .apply_renames(get_git_renames(self.source_branch, self.target_branch))
            current_warnings = CLWarnings(warnings)

            if self.threshold_file:
                current_warnings = self._apply_thresholds(current_warnings)

            current_linker_warnings = current_warnings.filter_by_domain('linker')
            current_compiler_warnings = current_warnings.filter_by_domain('compiler')

            delta = current_compiler_warnings \
                        .filter_with_changed_files(get_changed_files(self.changed_files)) \
                        .filter_by_types(self.ignore_type) - baseline_warnings

            if delta:
                new_warning_count = sum(delta.values())
                new_warning_components = set()
                for warning in delta.keys():
                    new_warning_components.update(warning.teams)
                if 'undefined' in new_warning_components:
                    new_warning_components.remove('undefined')
                if not new_warning_components:
                    new_warning_components = list()

                report_warnings = list()
                for warning, count in delta.items():
                    warning.quantity = count
                    report_warnings.append(warning.__dict__)
                for warning, count in current_linker_warnings.items():
                    warning.quantity = count
                    report_warnings.append(warning.__dict__)

                LOGGER.error('Compiler delta check has %s new findings', new_warning_count)
                self._write_summary({
                    'pr_id': self.prid,
                    'build_number': self.build_number,
                    'variant': self.build_variant,
                    'tool': self.tool,
                    'result': f'{new_warning_count} :no_entry:',
                    'details': '',
                    'components': list(new_warning_components),
                    'comment': '',
                })

                if self.output_html:
                    self._create_html_report(report_warnings)

                if self.output_json:
                    write_json_file(self.output_json, report_warnings,
                                    schema_file=os.path.join(os.path.dirname(__file__),
                                                             'schemas', 'compiler_warnings.json'))
                sys.exit(1)

        except Exception as exc:  # pylint: disable=W0703
            LOGGER.exception(exc)
            self._write_summary({
                'pr_id': self.prid,
                'build_number': self.build_number,
                'variant': self.build_variant,
                'tool': self.tool,
                'result': ':no_entry:',
                'details': '',
                'components': list(),
                'comment': f':boom: Error: {exc}',
            })
            sys.exit(1)

        LOGGER.info('Compiler delta check has no new findings')
        self._write_summary({
            'pr_id': self.prid,
            'build_number': self.build_number,
            'variant': self.build_variant,
            'tool': self.tool,
            'result': '0 :white_check_mark:',
            'details': '',
            'components': list(),
            'comment': '',
        })
        sys.exit(0)

    def _apply_thresholds(self, warnings: CLWarnings) -> CLWarnings:
        LOGGER.info('Checking thresholds...')
        warnings_per_component = warnings.get_warnings_per_component()
        thresholds = read_thresholds_file(self.tool, self.threshold_file)
        LOGGER.debug('Warnings per component: %s', warnings_per_component)
        LOGGER.debug('Configured thresholds: %s', thresholds)
        for component in thresholds:
            # Filter out the warnings with specified threshold if threshold is -1
            if thresholds[component] == -1:
                LOGGER.info('Ignoring all warnings for component %s', component)
                warnings = warnings.filter_by_component(component)
        return warnings

    def _write_summary(self, summary: dict) -> None:
        if self.summary_json:
            write_json_file(self.summary_json, summary, schema_file=os.path.join(os.path.dirname(__file__),
                                                                                 'schemas', 'summary_table.json'))

    def _create_html_report(self, data: list) -> None:
        """Create HTML report with Jinja2
        """
        loader = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        template = loader.get_template('compiler_delta_report.html')
        page_body = template.render(json_data=json.dumps(data), prid=self.prid, variant=self.build_variant,
                                    build_number=self.build_number)
        report_file = open(self.output_html, 'w')
        report_file.write(page_body)


if __name__ == '__main__':
    cmdargs = parse_args()
    LOGGER.setLevel(cmdargs.log_level)
    CompilerWarningsDeltaCheck(cmdargs)()
