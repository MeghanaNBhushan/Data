"""
PRQA File Report Generator
"""

import csv
import os
import re
import subprocess
import sys
from tempfile import TemporaryFile
from xml.etree import ElementTree

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.qacw.prqa_installation import PrqaInstallation

LOGGER = lucxlog.get_logger()


def main(args):
    project_path = os.path.join(os.getcwd(), args.project_name)
    project_xml_path = os.path.join(project_path, 'prqaproject.xml')

    prqa = PrqaInstallation(args.path_prqa)

    file_filters = _read_file_filters(project_xml_path)
    source_exts = _read_source_exts(project_xml_path)
    output_file = _exec_qacli_view(prqa.cli, project_path)
    analysis_results = _read_analysis_results(output_file)
    _write_csv_output(project_path, file_filters, source_exts, analysis_results, args.output)


def _read_file_filters(project_xml_path):
    """
    Reads the file filters inside the project xml.

    :param project_xml_path: Path to the project xml file.
    """
    tree = ElementTree.parse(project_xml_path)
    root = tree.getroot()

    root_path_elements = root.findall('./configurations/root_paths/root_path')
    root_paths = {element.attrib['name']: element.attrib['path'] for element in root_path_elements}
    option_elements = root.findall('./configurations/processMonitor/fileFilterStrings/option')

    filters = []
    for element in option_elements:
        path = element.attrib['string']

        for root_path_name, root_path in root_paths.items():
            path = path.replace('${' + root_path_name + '}', root_path)

        filters.append(path)

    return filters


def _read_source_exts(project_xml_path):
    """
    Reads the source file extensions inside the project xml.

    :param project_xml_path: Path to the project xml file.
    """
    tree = ElementTree.parse(project_xml_path)
    root = tree.getroot()

    return [element.attrib['ext'] for language_element in root.findall('./file_extensions/language')
            for element in language_element.findall('extension')]


def _exec_qacli_view(cli, project_path):
    """
    Runs qacli view and returns a file with the stdout output.

    :param cli: The PRQA cli.
    :param project_path: Path to the PRQA project.
    """
    # Example match for formatting expression:
    # error;/project/file;39;10; Possible null pointer exception.

    cmd_view = '{0} view --qaf-project "{1}" --medium STDOUT --format "%?g==2%(error%:%?u==0%(warning%: %)%);%F;%l;%c;%t"'.format(
        cli, project_path)
    output_file = TemporaryFile()

    exit_code = subprocess.call(cmd_view, shell=True, stdout=output_file)
    if exit_code != 0:
        output_file.seek(0)
        line = output_file.readline().decode()

        if exit_code != 2 or line.startswith('The specified project directory could not be found'):
            LOGGER.critical("No valid PRQA project found in '%s'", project_path)
            sys.exit(-10)

    output_file.seek(0)
    return output_file


def _read_analysis_results(output_file):
    """
    Reads the analysis files from qacli view output.

    :param output_file: File containing the qacli view output.
    """
    file_results_pattern = re.compile('^// ======= Results for (?P<path>.+)$')
    file_zero_pattern = re.compile('^(?P<path>.+) - zero diagnostics found$')

    error_pattern = re.compile('^error;(?P<path>.+);(?P<line>\\d+);(?P<column>\\d+);\\s*(?P<message>.+)$')
    last_file_path = None
    results = {}

    for line in output_file:
        line = line.decode().strip()

        if line == '':
            last_file_path = None
        elif last_file_path is not None:
            if line.startswith('error;'):
                match = re.match(error_pattern, line)
                error_path = match.group('path')
                error_line = match.group('line')
                error_column = match.group('column')
                error_message = match.group('message')

                results[last_file_path].append('{0}({1},{2}): {3}'.format(error_path, error_line, error_column, error_message))
        else:
            match = re.match(file_results_pattern, line) or re.match(file_zero_pattern, line)

            if match is not None:
                last_file_path = match.group('path')
                results[last_file_path] = []

    return results


def _write_csv_output(project_path, file_filters, source_exts, analysis_results, output_path):
    """
    Writes the CSV output file.

    :param project_path: Path to the QAF project.
    :param file_filters: List with file filter paths.
    :param source_exts: List with source code file extensions.
    :param analysis_results: Dict mapping a file path to its analysis results.
    :param output_path: Path where the CSV file shall be created.
    """
    with open(output_path, 'w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['path', 'analyzed', 'cause', 'details'])

        for root, _, files in os.walk(os.getcwd()):
            # Ignore files in the PRQA project directory
            if root.startswith(project_path):
                continue

            for file_name in files:
                file_path = os.path.join(root, file_name)
                analyzed, cause, details = _get_file_info(file_path, file_filters, source_exts, analysis_results)

                writer.writerow([file_path, int(analyzed), cause, '\\n'.join(details)])


def _get_file_info(file_path, file_filters, source_exts, analysis_results):
    """
    Gets information for a file.

    :param file_path: Path to the file.
    :param file_filters: List with file filter paths.
    :param source_exts: List with source code file extensions.
    :param analysis_results: Dict mapping a file path to its analysis results.
    """
    analyzed = False
    cause = 'unknown'
    details = []

    if file_path in analysis_results:
        details = analysis_results[file_path]

        if details:
            cause = 'parse error'
        else:
            analyzed = True
            cause = ''
    else:
        applicable_filter = None
        for file_filter in file_filters:
            if file_path.startswith(file_filter):
                applicable_filter = file_filter
                break

        if applicable_filter is not None:
            cause = 'ignored'
            details = ['ignored by filter ' + applicable_filter]
        elif not any([file_path.endswith(ext) for ext in source_exts]):
            cause = 'no source'

    return analyzed, cause, details
