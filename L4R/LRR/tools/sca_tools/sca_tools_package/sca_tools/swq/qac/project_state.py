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
"""Defines a Project class that extracts project related information from the
HIS report"""

import csv
import json
import re
from xml.etree.ElementTree import parse as etree_parse
from os import path, listdir, walk
from datetime import datetime

from swq.common.component_mapping import ComponentMapper
from swq.common.file.file_utils import calculate_sha256
from swq.common.filesystem.filesystem_utils import open_t, normalize_path
from swq.common.report.constants import LICENSE_WARNING
from swq.common.return_codes import log_and_exit, RC_EXPORT_FAILED
from swq.common.logger import LOGGER
from swq.common.return_codes import RC_INVALID_FILEPATH
from swq.qac.constants import DIAG_FILES_ROOT_DIR
from swq.qac.qac_commands import export_formatted_project_analysis, \
    export_diagnostics

REGEX_FOR_ANALYSIS_LOG_STRING = (
    # Matches OS agnostic filepath
    r'(?P<path>([A-Z]:(\\[^\\:]+)*)|(\/([^:]+))):'
    # Matches the component name
    r'(?P<module>\w+):'
    # Return code (can be non existent, with d+ it
    # runs into catastrophic backtracking)
    r'(?P<return_code>-?\d+):'
    # Files to parse
    r'(?P<files_to_parse>\d+):'
    # Files already parsed
    r'(?P<files_parsed>\d+)\s+?'
    # Timestamp
    r'(?P<timestamp>\([^\)]+\))?')

# Project Metrics
# STCYA: Cyclomatic complexity Across project
# STFEC: File entity change versus parent snapshot
# STNEA: Number of Entry points Across project
# STNFA: Number of Functions Across project
# STNRA: Number of Recursions Across project
# STPPC: Project line percentage change versus parent snapshot
_PROJECT_METRICS = ['STCYA', 'STFEC', 'STNEA', 'STNFA', 'STNRA', 'STPPC']
# File Metrics
# STPLC: Total physical lines of code
# STFNC: Number of functions in file
_FILE_METRICS = ['STVAR', 'STPLC', 'STFNC']
# Class Metrics
# STCBO: Coupling to other classes
# STDIT: Deepest inheritance
# STLCM: Lack of cohesion within class
# STMTH: Number of methods declared in class
# STWMC: Weighted methods in class
_CLASS_METRICS = ['STMTH', 'STWMC', 'STCBO', 'STLCM', 'STDIT']
# Function Metrics
# STAV1: Average size of statement in function
# STAV2: Average size of statement in function
# STAV3: Average size of statement in function
# STST1: Number of statements in function
# STST2: Number of statements in function
# STST3: Number of statements in function
# STCAL: Number of functions called from function.
# STCYC: Cyclomatic complexity
# STM07: Essential Cyclomatic Complexity
# STLCT: Number of local variables declared
# STLIN: Number of code lines
# STLOP: Number of logical operators
# STM29: Number of functions calling this function
# STSUB: Number of function calls
# STUNR: Number of unreachable statements
# STUNV: Unused or non-reused variables
# STXLN: Number of executable lines
# STMIF: Deepest level of nesting
# STPAR: Number of parameters
# STRET: Number of return points in function
# STGTO: Number of GOTO's
# STPTH: Estimated static program paths
_FUNCTION_METRICS = [
    'STAV1', 'STAV2', 'STAV3', 'STCAL', 'STCYC', 'STM07', 'STLCT', 'STLIN',
    'STLOP', 'STM29', 'STSUB', 'STUNR', 'STUNV', 'STXLN', 'STMIF', 'STPAR',
    'STRET', 'STGTO', 'STST1', 'STST2', 'STST3', 'STPTH'
]
_METRICS_OF_INTEREST = {
    *_PROJECT_METRICS, *_FILE_METRICS, *_CLASS_METRICS, *_FUNCTION_METRICS
}


def _get_metrics(entity_name, entity_type, entity_line, json_entity):
    metrics = json_entity.get('metrics')
    if not metrics:
        return None

    entity_metrics = {
        name: value
        for name, value in metrics.items() if name in _METRICS_OF_INTEREST
    }

    return {
        'name': entity_name,
        'type': entity_type,
        'line': entity_line,
        'metrics': entity_metrics
    }


def _create_file_metrics(filepath, json_data):
    file_metrics = {'type': 'file'}
    metrics = _get_metrics(filepath, 'file', '', json_data)
    if metrics:
        file_metrics['metrics'] = metrics
    submetrics = []
    for entity in json_data.get('entities', []):
        submetric = _get_metrics(entity.get('name'), entity.get('type'),
                                 entity.get('line'), entity)
        if submetric:
            submetrics.append(submetric)
    if submetrics:
        file_metrics['submetrics'] = submetrics

    return file_metrics


def _log_error_if_file_not_in_analysis(analysis, normalized_filepath):
    if not analysis.get(normalized_filepath):
        LOGGER.debug(
            'Information missing for file = %s while adding violations',
            normalized_filepath)


def _normalize_diagnostic_path(root_path, diagnostic):
    if diagnostic.get('filepath'):
        diagnostic['filepath'] = normalize_path(root_path,
                                                diagnostic['filepath'])


def _parse_sub_diag(diag_node, finding_id: str, depth: int = 1):
    parsed_results = []
    for subdiag_node in diag_node.findall("./SubDiag"):
        finding = {
            subdiag_child_element.tag.lower():
            subdiag_child_element.text if subdiag_child_element.text else ''
            for subdiag_child_element in subdiag_node
            if subdiag_child_element.tag != 'SubDiag'
        }
        subdiag_id = subdiag_node.attrib['id']
        finding['id'] = f'{finding_id}_{subdiag_id}'
        finding['depth'] = depth
        parsed_results.append(finding)
        for subdiag_child_element in subdiag_node:
            if subdiag_child_element.tag == 'SubDiag':
                parsed_results.extend(
                    _parse_sub_diag(subdiag_node, finding['id'], depth + 1))

    return parsed_results


def _get_baseline_sha(config):
    return '' if not path.exists(
        config.local_baseline_cache_filepath) else calculate_sha256(
            config.local_baseline_cache_filepath)


class ProjectState:
    """Class that is able to export the current project state"""
    def __init__(self, config):
        self._config = config
        if self._config.codeowners_file:
            self._component_mapper = ComponentMapper(
                self._config.codeowners_file)

    def _generate_consolidated_json(self, file_root):
        project_data = {}

        if file_root is None:
            return project_data

        for file_entity in file_root.iter('File'):
            filepath = path.normpath(file_entity.attrib['path'])
            if file_entity.find('Json') is None:
                LOGGER.error("Error parsing file = %s. Ignoring it.", filepath)
                continue

            json_tag_value = file_entity.find('Json').text
            json_file = path.normpath(json_tag_value)
            json_data = None
            with open_t(json_file) as json_metrics_file:
                json_data = json.loads(json_metrics_file.read())

            if not json_data:
                LOGGER.error("Error parsing json_file = %s. Ignoring it.",
                             json_file)
                continue

            normalized_path = normalize_path(self._config.project_root,
                                             filepath)
            if not normalized_path:
                LOGGER.error('Invalid path = %s', filepath)
                continue

            project_data[normalized_path] = _create_file_metrics(
                filepath, json_data)

        return project_data

    def _parse_analyse_logs(self):
        def _get_analyse_information_from_regex(analysis, re_match):
            normalized_filepath = normalize_path(
                self._config.project_root,
                path.normpath(re_match.group('path')))
            if not normalized_filepath:
                return

            analysis.setdefault(normalized_filepath, []).append({
                'analysis_code':
                re_match.group('return_code'),
                'module':
                re_match.group('module'),
                'timestamp':
                re_match.group('timestamp')
            })

        file_list = [
            path.join(self._config.analysis_path, log_file)
            for log_file in listdir(self._config.analysis_path)
            if log_file.endswith('.log')
        ]
        file_list.sort()

        if not file_list:
            return {}

        log_filepath = file_list[-1]
        LOGGER.info('Opening log %s to extract analysis output information',
                    log_filepath)
        with open_t(log_filepath) as analysis_log:
            analysis_outputs = {}
            for match in re.finditer(REGEX_FOR_ANALYSIS_LOG_STRING,
                                     analysis_log.read(), re.MULTILINE):
                _get_analyse_information_from_regex(analysis_outputs, match)

            return analysis_outputs

    def _add_summary_per_file_to_dict(self, analysis):
        def _parse_file_summary(file_entity):
            severities = {
                severity_entity.attrib['id']: severity_entity.text
                for severity_entity in file_entity.findall('Severity')
            }
            severities_total = file_entity.find('SeverityTotal').text
            analysis_error_count = file_entity.find('AnalysisErrorCount').text
            analysis_exit_status = file_entity.find('AnalysisExitStatus').text
            filepath = file_entity.find('Name').text

            return (filepath, {
                'severities': severities,
                'severities_total': severities_total,
                'analysis_error_count': analysis_error_count,
                'analysis_exit_status': analysis_exit_status
            })

        xml_filepath = path.normpath(
            path.join(self._config.project_reports_path,
                      'severity_summary.xml'))
        if not path.exists(xml_filepath):
            LOGGER.info("File %s does not exist", xml_filepath)
            return

        LOGGER.info("Parsing Summary XML file = %s", xml_filepath)
        xml_tree = etree_parse(xml_filepath)
        xml_root = xml_tree.getroot()
        file_summaries = [
            _parse_file_summary(file_entity)
            for file_entity in xml_root.iter('File')
        ]
        for filepath, file_summary in file_summaries:
            # Sets the file name as it might not have been included by
            # the processing of results_data.xml.
            # In real-life situations it is often not reliable
            normalized_filepath = normalize_path(self._config.project_root,
                                                 filepath)
            _log_error_if_file_not_in_analysis(analysis, normalized_filepath)
            analysis.setdefault(normalized_filepath, {})
            analysis[normalized_filepath]['summary'] = file_summary

        # Adds analysis log section if present
        for filepath, analysis_output in self._parse_analyse_logs().items():
            if analysis.get(filepath):
                analysis[filepath]['summary'].setdefault(
                    'analysis_log', analysis_output)

    def _add_violations_per_file_to_dict(self, analysis):
        def _get_formatted_source_root(source_root):
            filepath = source_root['filepath']
            line = source_root['line']
            column = source_root['column']
            producer = source_root['producer']
            msgnum = source_root['padmsgnum']

            return f'{filepath}:{line}:{column}:{producer}:{msgnum}'

        def _get_subdiagnostic_origins_from_sub_finding(sub_findings):
            if not sub_findings:
                return []

            _sub_findings = sub_findings.copy()
            source_roots = []

            source_root = _sub_findings.pop(0)

            while _sub_findings:
                if source_root['id'] not in _sub_findings[0]['id']:
                    source_roots.append(
                        _get_formatted_source_root(source_root))
                source_root = _sub_findings.pop(0)

            source_roots.append(_get_formatted_source_root(source_root))

            return source_roots

        def _get_diag_xml_file_list(diag_files_path):
            xml_file_list = []
            for root_dir, _, files in walk(diag_files_path):
                for file in files:
                    if file.endswith(".xml"):
                        xml_file_list.append(path.join(root_dir, file))

            return xml_file_list

        export_diagnostics(self._config)
        diag_files_path = path.join(self._config.project_diagnostics_path,
                                    DIAG_FILES_ROOT_DIR)
        if not path.exists(diag_files_path):
            LOGGER.error(
                "Diagnostics export directory {} does not exist".format(
                    diag_files_path))
            log_and_exit(RC_INVALID_FILEPATH)

        for (i,
             xml_file) in enumerate(_get_diag_xml_file_list(diag_files_path),
                                    start=1):
            xml_tree = etree_parse(xml_file)
            xml_root = xml_tree.getroot()
            normalized_filepath = normalize_path(
                self._config.project_root,
                xml_root.find("./File/Name").text)
            _log_error_if_file_not_in_analysis(analysis, normalized_filepath)
            analysis.setdefault(normalized_filepath, {})
            diag_elements = {}
            for diag_node in xml_root.iter('Diag'):
                diag_elements = {
                    diag_child_element.tag.lower():
                    diag_child_element.text if diag_child_element.text else ''
                    for diag_child_element in diag_node
                    if diag_child_element.tag != 'SubDiag'
                }
                diag_id = diag_node.attrib['id']
                diag_elements['depth'] = 0
                diag_elements['id'] = f'{i}_{diag_id}'
                _normalize_diagnostic_path(self._config.project_root,
                                           diag_elements)

                diag_elements['sub_findings'] = _parse_sub_diag(
                    diag_node, diag_elements['id'])
                for subdiag_elements in diag_elements['sub_findings']:
                    _normalize_diagnostic_path(self._config.project_root,
                                               subdiag_elements)

                diag_elements['finding_origins'] = \
                    ' '.join(_get_subdiagnostic_origins_from_sub_finding(
                        diag_elements['sub_findings']))

                analysis[normalized_filepath].setdefault(
                    'findings', []).append(diag_elements)

    def _get_csv_analysis(self):
        analysis_output, returncode = export_formatted_project_analysis(
            self._config)
        # code 2 means: command processing failure
        success_codes = [0, 2]
        if returncode in success_codes:
            LOGGER.info("Export returned code %s", returncode)
        else:
            LOGGER.error("View export returned code: %s", str(returncode))
            log_and_exit(RC_EXPORT_FAILED)

        # Reads input from the analysis output
        return csv.reader(analysis_output.split('\n'),
                          delimiter=',',
                          quotechar='"')

    def _parse_file_root(self):
        xml_filepath = path.normpath(
            path.join(self._config.project_reports_path, 'results_data.xml'))

        if not path.exists(xml_filepath):
            LOGGER.warning('File %s not be found. Report HMR failed?',
                           xml_filepath)
            return None

        LOGGER.info("Parsing XML file = %s", xml_filepath)
        xml_tree = etree_parse(xml_filepath)
        xml_root = xml_tree.getroot()

        file_root = [
            dataroot for dataroot in xml_root.findall('dataroot')
            if dataroot.attrib['type'] == 'per-file'
        ][0]

        return file_root

    def create(self):
        """Create project state of QAC project"""
        git_commit = self._config.project_git_commit

        LOGGER.info('git hash = %s', git_commit)
        file_root = self._parse_file_root()
        ncf_file = self._config.ncf_file.get_input_filenames_as_string() \
            if self._config.ncf_file else ''
        vcf_file = path.basename(self._config.vcf_file) \
            if self._config.vcf_file else None
        state = {
            'license': LICENSE_WARNING,
            'git_commit':
            git_commit,
            'project_root':
            self._config.project_root,
            'prqa_project_relative_path':
            normalize_path(self._config.project_root,
                           self._config.qac_project_path),
            'cli_version':
            self._config.cli_version_string,
            'timestamp':
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'acf':
            self._config.acf_file.get_input_filenames_as_string(),
            'cct':
            ','.join(
                [path.basename(cct) for cct in self._config.compiler_list]),
            'ncf':
            ncf_file,
            'rcf':
            self._config.rcf_file.get_input_filenames_as_string(),
            'vcf':
            vcf_file,
            'user_messages':
            self._config.user_messages.get_input_filenames_as_string(),
            'cache_baseline_path':
            self._config.local_baseline_cache_dir_path,
            'local_baseline_path':
            self._config.local_baseline_path,
            'local_baseline_sha':
            _get_baseline_sha(self._config),
            'analysis':
            self._generate_consolidated_json(file_root)
        }
        # Appends additional information from results_data.xml and jsons
        self._add_violations_per_file_to_dict(state['analysis'])
        # Appends additional information from severity_summary.xml
        self._add_summary_per_file_to_dict(state['analysis'])

        return state
