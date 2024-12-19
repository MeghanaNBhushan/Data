"""
QACWrapper

A QAC wrapper script collection
"""
import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog
from lucxbox.tools.qacw import qacw_file_report
from lucxbox.tools.qacw import qacw_project_analysis
from lucxbox.tools.qacw import qacw_project_report
from lucxbox.tools.qacw import qacw_project_setup
from lucxbox.tools.qacw import qacw_project_upload
from lucxbox.tools.qacw import qacw_warnings
from lucxbox.tools.qacw import qacw_xml_to_excel

LOGGER = lucxlog.get_logger()


def parse_args():
    """ Individual ArgumentParser adaptions regarding the script functionality

        Return value:
        ArgumentParser -- parsed arguments object to access given cli arguments
    """
    description = "A QAC+ wrapper script collection"
    parser = argparse.ArgumentParser(description=description)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)

    parser.add_argument('-p', '--qac-path', required=False, dest='path_prqa', help='The path to the PRQA installation.')

    qacw_sub = parser.add_subparsers(title='QAC Sub-Commands')
    parse_args_xml2excel(qacw_sub)
    parse_args_file_report(qacw_sub)

    # Commands for the handling of QAC projects
    parser_project = qacw_sub.add_parser('project', help='Setup QAC Project')
    parser_project_sub = parser_project.add_subparsers(title='QAC Project Sub-Commands')
    parser_project.add_argument('-n', '--name', required=True, dest='project_name', help='Project name')

    # additional parsers
    parse_setup_project(parser_project_sub)
    parse_args_analyze(parser_project_sub)
    parse_args_report(parser_project_sub)
    parse_args_upload(parser_project_sub)
    parse_args_team_mapping(parser_project_sub)
    parse_args_combine_report(parser_project_sub)
    parse_args_check_changed_files(parser_project_sub)
    parse_args_check_warning_week(parser_project_sub)

    return parser.parse_args()


def parse_args_xml2excel(qacw_sub):
    """
    Parse arguments for xml2excel

    :param qacw_sub: The qac sub parser
    """
    parser_xml_to_excel = qacw_sub.add_parser('xml2excel', help='Converts a QAC+ XML Export to an Excel file')
    parser_xml_to_excel.add_argument('-i', '--input', required=True,
                                     help='XML file which contains a QACP analysis output')
    parser_xml_to_excel.add_argument('-o', '--output', required=True, help='Path to the desired XLSX output file')
    parser_xml_to_excel.add_argument('-sl', '--severity-levels', required=False, nargs='+', type=int,
                                     choices=range(1, 10), dest='severity_levels',
                                     help='Specify a subset of interested severity levels as a space separated integer list')
    parser_xml_to_excel.add_argument('-gc', '--guess-component', required=False, dest='guess_component_name',
                                     action='store_true',
                                     help='Whether to guess the component name of extracted files or not. Default is False.')
    parser_xml_to_excel.add_argument('-l', '--layout', required=False, dest='excel_layout', choices=['list', 'matrix'],
                                     help='''Defines which excel sheet layout to use.
                                     Default is a list of files/components where each line equals one finding''')
    parser_xml_to_excel.set_defaults(func=xml_to_excel)


def parse_args_file_report(qacw_sub):
    """
    Parse arguments for file_report

    :param qacw_sub: The qac sub parser
    """
    parser_file_report = qacw_sub.add_parser('filereport', help='Generates report listing files and their analysis status')
    parser_file_report.add_argument('-n', '--name', required=True, dest='project_name', help='Project name')
    parser_file_report.add_argument('-o', '--output', required=True, help='Path where the report shall be stored in CSV format')
    parser_file_report.set_defaults(func=file_report)


def parse_setup_project(parser_project_sub):
    """
    Parse arguments for qac project setup.

    :param parser_project_sub: the project sub parser
    """
    parser_project_setup = parser_project_sub.add_parser('setup',
                                                         help="""Setup the QAC project. This command performs the following tasks:
                                                              - check the required licenses
                                                              - create the QAF project and set the source code root
                                                              - set file filters""")
    parser_project_setup.add_argument('--acf', required=True, dest='acf', help='The path to the Analysis Configuration File (ACF).')
    parser_project_setup.add_argument('--cct', required=True, action='append',
                                      help="""The path to the Compiler Compatibility Template (CCT). The '--cct' argument may be specified
                                           more than once in order to add support to a project for more than one compiler.""")
    parser_project_setup.add_argument('--rcf', required=True, dest='rcf', help='The path to the Rule Configuration File (RCF).')
    parser_project_setup.add_argument('--vcf', required=False, dest='vcf',
                                      help='The path to the Version Control Compatibility File (VCF)')
    parser_project_setup.add_argument('--user-messages', required=False, dest='user_messages', help='User messages configuration file')
    parser_project_setup.add_argument('-f', '--file-filters', required=False, dest='file_filters', nargs='*', type=str, default=[],
                                      help='List of file filters to be applied to the analysis.')
    parser_project_setup.add_argument('--no-remap-c', dest='remap', action='store_false',
                                      help='''Remap C files as Cpp files for the analysis. When this argument is not added,
                                      a remap is done (default)''')
    parser_project_setup.set_defaults(func=project_setup)


def parse_args_analyze(parser_project_sub):
    """
    Parse arguments for qac analysis

    :param parser_project_sub: the project sub parser
    """
    parser_project_analyze = parser_project_sub.add_parser('analyze',
                                                           help="""Analyze the QAC project. This command performs the following tasks:
                                                          - check the required licenses
                                                          - build the software with build monitoring activated
                                                          - do the actual analysis""")
    parser_project_analyze.add_argument('-b', '--build-cmd', required=True, dest='build_command', help='Build Command')
    parser_project_analyze.add_argument('-f', '--file-list', required=False, dest='file_list', help='File list to analyze')
    parser_project_analyze.add_argument('-c', '--clean', default=False, dest='clean_build', action='store_true',
                                        help="""Cleans all analysis data from the specified qaf-project before performing analysis.
                                        In the case where the 'cma-project' option is specified, all PRQA Framework projects involved
                                        in the analysis will be cleaned.""")
    parser_project_analyze.add_argument('-m', '--messages-output', required=False, dest='output_path',
                                        help="""Exports messages report in the format suitable for SonarQube QAF plugin into specified
                                        file or folder depending on the format.""")
    parser_project_analyze.add_argument('-M', '--messages-output-format', required=False, dest='output_format',
                                        choices=['txt', 'xml'], default='txt',
                                        help="""Sets the format of `--messages-output`. Possible values are xml and
                                        txt (default).""")
    parser_project_analyze.add_argument('-I', '--inter-tu-dataflow', default=False, dest='inter_tu_dataflow', action='store_true',
                                        help="""Perform Inter TU Dataflow analysis. This option is only valid for QAC/QAC++.
                                        When enabled, the first pass will be run with df::inter=0 and the second pass will be run with the
                                        value of df::inter (previously set by the user).""")
    parser_project_analyze.add_argument('--suppress-h-files', dest='suppress_h', action='store_true',
                                        help='Supress h include headers for the qacpp analysis')
    parser_project_analyze.set_defaults(func=project_analyze)


def parse_args_report(parser_project_sub):
    """
    Parse arguments for qac analysis report

    :param parser_project_sub: the project sub parser
    """
    parser_project_report = parser_project_sub.add_parser('report', help='Generate QAC Report')
    parser_project_report.add_argument('-r', '--report-types', required=False, dest='report_types', nargs='+', type=str,
                                       choices=['CRR', 'HMR', 'MDR', 'RCR', 'SSR', 'SUR'],
                                       help="""A space separated integer list with the report types:
                                               CRR - Code Review Report
                                               HMR - HIS Metrics Report
                                               MDR - Metrics Data Report
                                               RCR - Rule Compliance Report
                                               SSR - Severity Summary Report
                                               SUR - Suppressions Report""")
    parser_project_report.add_argument('-f', '--file-list', required=False, dest='file_list', help='File list to report')
    parser_project_report.add_argument('-a', '--archive-target-dir', required=False, dest='archive_target_dir', default='',
                                       help='The path where the report shall be archived.')
    parser_project_report.set_defaults(func=project_report)


def parse_args_upload(parser_project_sub):
    """
    Parse arguments for qac analysis upload

    :param parser_project_sub: the project sub parser
    """
    parser_project_upload_qav = parser_project_sub.add_parser('upload-qav', help='Upload QAC Analysis to QAVerify')
    parser_project_upload_qav.add_argument('--stream', dest='stream', required=True, help='The name of the QAVerify project')
    parser_project_upload_qav.add_argument('--snapshot', dest='snapshot', required=True,
                                           help='The name of the snapshot (e.g. the git commit hash)')
    parser_project_upload_qav.add_argument('--upload-source', dest='upload_source', default='ALL', required=False,
                                           choices=['ALL', 'NOT_IN_VCS', 'NONE'], help="""Whether to upload the source code to QAVerify.
                                              Options are 'ALL', 'NOT_IN_VCS', and 'NONE'. The default value is 'ALL'""")
    parser_project_upload_qav.add_argument('--url', dest='url', required=True, help='The url of the QAVerify server.')
    parser_project_upload_qav.add_argument('-u', '--username', dest='username', required=True, help='The user to perform the upload.')
    parser_project_upload_qav.add_argument('-p', '--password', dest='password', required=True, help='The password to perform the upload')
    parser_project_upload_qav.set_defaults(func=project_upload_qav)

    parser_project_upload_s101 = parser_project_sub.add_parser('upload-s101', help='Upload QAC Analysis to S101')
    parser_project_upload_s101.set_defaults(func=project_upload_s101)


def parse_args_team_mapping(parser_project_sub):
    """
    Parse arguments for qac analysis team mapping

    :param parser_project_sub: the project sub parser
    """
    parser_project_warnings_mapping = parser_project_sub.add_parser('map-team-warnings', help='Map QAC analysis warnings to teams.')
    parser_project_warnings_mapping.add_argument('-c', '--components-file', dest='components_files', nargs='+', required=True,
                                                 help='The path to the components files containing the mapping components <-> team')
    parser_project_warnings_mapping.add_argument('-t', '--team-warnings-file', dest='team_warnings_file', required=True,
                                                 help="""Path and filename of the output report file. Output format is based on the file
                                                 extension provided in this argument. For very large reports use csv as output format
                                                 as Excel has a maximum of 1.048.576 lines. Possible file formats are 'xlsx' and 'csv'.""")
    parser_project_warnings_mapping.add_argument('-s', '--min-severity', dest='min_severity', type=int, required=False, default=2,
                                                 help="""Filter messages whose severity is less than the supplied severity.
                                                 Valid values are in the range 1-9. 0 and 1 are acceptable, but will display everything.
                                                 Values greater than 9 will filter everything.""")
    parser_project_warnings_mapping.add_argument('-e', '--exception-wildcards', dest='exception_wildcards', required=False,
                                                 nargs='+', type=str, default=[],
                                                 help='List of wildcard expressions in order to exclude files from the analysis')
    parser_project_warnings_mapping.add_argument('-r', '--report-file', dest='report_file', required=False,
                                                 default="report.log",
                                                 help='The path to the intermediate report file containing the warnings')
    parser_project_warnings_mapping.set_defaults(func=map_team_warnings)


def parse_args_combine_report(parser_project_sub):
    """
    Parse arguments for combination of reports

    :param parser_project_sub: the project sub parser
    """
    parser_project_combine_report = parser_project_sub.add_parser('combine-reports', help='Combine two reports into one.')

    parser_project_combine_report.add_argument('-f', '--first-report', dest='first_report', required=True, help='First csv report')
    parser_project_combine_report.add_argument('-s', '--second-report', dest='second_report', required=True, help='Second csv report')
    parser_project_combine_report.set_defaults(func=combine_csv_reports)


def parse_args_check_changed_files(parser_project_sub):
    """
    Parse arguments for combination of reports

    :param parser_project_sub: the project sub parser
    """
    parser_project_combine_report = parser_project_sub.add_parser('check-changed-files', help='Combine two reports into one.')

    parser_project_combine_report.add_argument('-c', '--changed-files', dest='changed_files', required=False, nargs='+',
                                               help='Files containing a list of changed files')
    parser_project_combine_report.add_argument('-w', '--warning-reports', dest='warnings_report', required=True,
                                               help='Report with warnings')
    parser_project_combine_report.set_defaults(func=check_changed_lines_file)

def parse_args_check_warning_week(parser_project_sub):
    """
    Parse arguments for combination of reports

    :param parser_project_sub: the project sub parser
    """
    parser_project_combine_report = parser_project_sub.add_parser('check_warning_week', help='Check if warning of the week are present')

    parser_project_combine_report.add_argument('-c', '--changed-files', dest='changed_files', required=False, nargs='+',
                                               help='Files containing a list of changed files')
    parser_project_combine_report.add_argument('-w', '--warning-reports', dest='warnings_report', required=True,
                                               help='Report with warnings')
    parser_project_combine_report.add_argument('-ww', '--warnings-of-week', dest='warnings_week', required=True, nargs='+',
                                               help='List of warnings of the week')
    parser_project_combine_report.set_defaults(func=check_warning_week)

def xml_to_excel(args):
    """Calls the subparser implementation for xml to excel transformation

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_xml_to_excel.main(args)


def file_report(args):
    """Calls the subparser implementation for file report generation

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_file_report.main(args)


def project_setup(args):
    """Calls the subparser implementation for project creation

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_project_setup.setup_project(args.project_name, args.acf, args.cct, args.rcf, args.vcf,
                                     args.user_messages, args.file_filters, args.path_prqa, args.remap)


def project_analyze(args):
    """Calls the subparser implementation for project creation

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_project_analysis.sync_and_analyze(args.project_name, args.build_command, args.file_list,
                                           args.path_prqa, args.clean_build, args.output_path,
                                           args.output_format, args.inter_tu_dataflow, args.suppress_h)


def project_report(args):
    """Calls the subparser implementation for project report

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_project_report.report(args.project_name, args.report_types, args.file_list,
                               args.archive_target_dir, args.path_prqa)


def project_upload_qav(args):
    """Calls the subparser implementation for project upload to qav
    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_project_upload.upload_qav(args.project_name, args.stream, args.snapshot, args.upload_source,
                                   args.url, args.username, args.password, args.path_prqa)


def project_upload_s101(args):
    """Calls the subparser implementation for project upload to s101

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_project_upload.upload_s101(args.project_name, args.path_prqa)


def map_team_warnings(args):
    """Calls the subparser implementation for mapping the qac analysis warnings to the respective teams

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_warnings.map_team_warnings(args.project_name, args.components_files, args.team_warnings_file,
                                    args.exception_wildcards, args.report_file, args.min_severity, args.path_prqa)


def combine_csv_reports(args):
    """Calls the subparser implementation for combining two csv reports

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_warnings.combine_csv_reports(args.first_report, args.second_report)


def check_changed_lines_file(args):
    """Calls the subparser implementation for combining two csv reports

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_warnings.check_changed_lines_file(args.changed_files, args.warnings_report)

def check_warning_week(args):
    """Calls the subparser implementation for combining two csv reports

    Arguments:
        args Object -- Object containing all passed arguments
    """
    qacw_warnings.check_warning_week(args.changed_files, args.warnings_report, args.warnings_week)

def main():
    """Main function to call when this script is called directly and not imported"""
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
