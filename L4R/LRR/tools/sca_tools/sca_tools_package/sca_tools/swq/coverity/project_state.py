# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: project_state.py
# ----------------------------------------------------------------------------
"""Defines a Project State class that extracts project related information"""
from os import path
from datetime import datetime
from json import loads

from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t, normalize_path, \
    create_dirs_if_necessary
from swq.common.return_codes import \
    check_return_code_for_cmd_and_exit_if_failed
from swq.coverity.coverity_commands import cov_commit_defects, \
    coverity_export_errors_json, coverity_export_errors_html
from swq.coverity.coverity_utils import list_translation_units


def _add_findings_per_issue(issue):
    findings_data = {}
    findings_data['cid'] = ''
    findings_data['merge_key'] = issue['mergeKey']
    findings_data['line'] = issue['mainEventLineNumber']
    findings_data['producer'] = issue['checkerName']
    findings_data['subcategory'] = issue['subcategory']
    findings_data['extra'] = issue['extra']
    findings_data['domain'] = issue['domain']
    findings_data['language'] = issue['language']
    findings_data['category'] = issue['checkerProperties']['category']
    findings_data['cwe_category'] = issue['checkerProperties']['cweCategory']
    findings_data['issue_kinds'] = issue['checkerProperties']['issueKinds']
    findings_data['severity'] = issue['checkerProperties']['impact']
    findings_data['subcategory_local_effect'] = issue['checkerProperties'][
        'subcategoryLocalEffect']
    findings_data['msgtext'] = issue['checkerProperties'][
        'subcategoryLongDescription']

    return findings_data


class ProjectState:
    """Project state class"""
    def __init__(self, config):
        self._config = config

    def _add_cid_value_to_issues(self, analysis_data):
        def _map_merge_keys_with_cid(json_data):
            merge_keys_mapping = {}
            for issue_in_preview_report in json_data['issueInfo']:
                merge_keys_mapping[issue_in_preview_report[
                    'mergeKey']] = issue_in_preview_report['cid']

            return merge_keys_mapping

        with open_t(self.export_preview_report()) as preview_report_json:
            json_data = loads(preview_report_json.read())

        merge_keys_mapping = _map_merge_keys_with_cid(json_data)

        for analyzed_file in analysis_data:
            for finding in analysis_data[analyzed_file]['findings']:
                merge_key = finding['merge_key']
                if merge_key in merge_keys_mapping.keys():
                    finding['cid'] = merge_keys_mapping[merge_key]

    def _generate_consolidated_json(self):
        analysis_data = {}
        with open_t(self.export_errors()) as export_errors_json:
            json_data = loads(export_errors_json.read())

        try:
            for issue in json_data['issues']:
                analyzed_file = issue['strippedMainEventFilePathname']
                if analyzed_file in analysis_data.keys():
                    analysis_data[analyzed_file]['findings'].append(
                        _add_findings_per_issue(issue))
                else:
                    analysis_data[analyzed_file] = {}
                    analysis_data[analyzed_file].setdefault('type', 'file')
                    analysis_data[analyzed_file].setdefault(
                        'findings', []).append(_add_findings_per_issue(issue))

            if self._config.with_cid:
                self._add_cid_value_to_issues(analysis_data)

        except KeyError as exception:
            LOGGER.error(exception)

        return analysis_data

    def export_preview_report(self):
        """Instead of sending files, cross-references, and other assets
        to the Coverity Connect server, this option sends only the defect
        occurrences. The server returns a commit preview report,
        which is written in JSON format"""

        preview_report_json = create_dirs_if_necessary(
            self._config.preview_report_json_filepath)
        [_, return_value] = cov_commit_defects(self._config,
                                               preview_report_json)
        check_return_code_for_cmd_and_exit_if_failed(return_value)

        return preview_report_json

    def export_errors(self):
        """Generates analysis result report in JSON format"""
        coverity_json_filepath = create_dirs_if_necessary(
            self._config.cov_errors_json_filepath)
        LOGGER.info("coverity_json_filepath {}".format(coverity_json_filepath))
        [_, return_value] = \
            coverity_export_errors_json(self._config,
                                        coverity_json_filepath)
        check_return_code_for_cmd_and_exit_if_failed(return_value)

        if self._config.with_native_html_report:
            LOGGER.info('Generating Coverity native html report in %s',
                        self._config.cov_errors_html_dirpath)
            [_, return_value] = \
                coverity_export_errors_html(self._config)
            check_return_code_for_cmd_and_exit_if_failed(return_value)

        return coverity_json_filepath

    def create(self):
        """Creates project state of Coverity project"""
        git_commit = self._config.project_git_commit
        LOGGER.info('git hash = %s', git_commit)
        found_tus = list_translation_units(self._config)
        state = {
            'git_commit': git_commit,
            'project_root':
            self._config.project_root,
            'sca_project_relative_path':
            normalize_path(self._config.project_root,
                           self._config.coverity_project_path),
            'cli_version':
            self._config.cli_version_string,
            'timestamp':
            datetime.now().strftime('%Y_%m_%d_%H_%M_%S'),
            'compilers':
            ','.join(
                [path.basename(cct) for cct in self._config.compiler_list]),
            'number_of_found_tus':
            found_tus['total_numberof_tus'],
            'number_of_failed_tus':
            found_tus['numberof_failed_tus'],
            'percentage_of_successful_tus':
            found_tus['percentage_of_successful_tus'],
            'analysis':
            self._generate_consolidated_json()
        }

        return state
