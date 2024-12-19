"""
This class takes care of associating QAC warnings with teams.
A report file (csv or xlsx) will be generated with a list of all warnings and the respective teams.
In order to do so, a "components" file is required, which links wildcards with teams.
The components file has the following layout:

**/*.py @team_a
**/team_folder/** @team_b
"""
import csv
import os
import sys
from csv import reader
import xlsxwriter


sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxutils, wildcards
from lucxbox.lib.component_mapping import ComponentMapper
from lucxbox.tools.qacw.prqa_installation import PrqaInstallation
from lucxbox.tools.qacw.qac_result import QacResult
from lucxbox.tools.compiler_warnings.compiler_warnings import read_changed_files

LOGGER = lucxlog.get_logger()


def map_team_warnings(project_name, components_files, team_warnings_file, exception_wildcards, report_file, min_severity, path_prqa):
    """ This is the main function which is being called from the command line.

    :param project_name: The project name of the QAC analysis
    :param components_files: The path to the COMPONENTS file
    :param team_warnings_file: Path and filename of the xlsx output report file
    :param exception_wildcards: List of wildcard expressions in order to exclude files from the analysis
    :param report_file: The path to the intermediate report file containing the warnings
    :param min_severity: Filter messages whose severity is less than the supplied severity.
    :param path_prqa: The path to the PRQA executable
    """
    generate_analysis_result_file(project_name, report_file, min_severity, path_prqa)
    qac_results = process_results_file(report_file, exception_wildcards, components_files, min_severity)

    if team_warnings_file.lower().endswith(".xlsx"):
        create_xlsx_report(qac_results, team_warnings_file)
    elif team_warnings_file.lower().endswith(".csv"):
        create_csv_report(qac_results, team_warnings_file)
    else:
        LOGGER.warning("No (known) extension found. Defaulting to csv output.")
        team_warnings_file = team_warnings_file + ".csv"
        create_csv_report(qac_results, team_warnings_file)


def generate_analysis_result_file(project_name, result_file, min_severity, path_prqa):
    """ Performs a qacli command in order to generate a file containing the results of the qac analysis

    :param project_name: The name of the prqa project
    :param result_file: The path where the analysis result file shall be generated
    :param min_severity: Filter messages whose severity is less than the supplied severity.
    :param path_prqa: The path to the PRQA executable
    """
    prqa = PrqaInstallation(path_prqa)

    # check if result file path exists
    if not os.path.exists(os.path.dirname(os.path.abspath(result_file))):
        os.makedirs(os.path.dirname(os.path.abspath(result_file)))

    cmd_list = [prqa.cli, "view",
                "--qaf-project {}".format(project_name),
                "--min-severity {}".format(str(min_severity)),
                "--medium STDOUT",
                "--format \"%F; %l; %Y; %t; %n\""]
    cmd = " ".join(cmd_list)

    LOGGER.info("Generating analysis result file with cmd %s", cmd)
    with open(result_file, "wb") as out:
        _, _, code = lucxutils.execute(cmd, stdout=out)
        if code != 0:
            if code == 2:
                LOGGER.error("Command '%s' exited with code 2, 'Command Processing Failure'. Continuing.", cmd)
            elif code == 3:
                LOGGER.info("Command '%s' exited with code 3, 'Command Success, with some warnings'. Continuing.", cmd)
            else:
                LOGGER.critical("Command '%s' exited with code %s", cmd, code)
                sys.exit(-32)


def process_results_file(file_name, exception_wildcards, components_files, min_severity):
    """ Process the results of the qac analysis and generate a Tuple of custom objects.

    :param file_name: The path where the analysis result file shall be generated
    :param exception_wildcards: List of wildcard expressions in order to exclude files from the analysis
    :param components_files: The path to the COMPONENTS file
    :param min_severity: Filter messages whose severity is less than the supplied severity.
    :return: A list containing QacResult objects
    """
    LOGGER.info("Processing results file %s", file_name)

    component_mapper = ComponentMapper(components_files)

    qac_results = []
    with open(file_name) as result_file:
        for line in result_file:
            if check_if_analyze_line(exception_wildcards, line):
                result_split = line.split(";")
                path = result_split[0].strip()
                severity = int(result_split[2].strip())
                try:
                    qac_result = QacResult(
                        path=path,
                        line_number=int(result_split[1].strip()),
                        severity=severity,
                        msg_text=result_split[3].strip(),
                        msg_id=result_split[4].strip()
                    )
                    qac_result.teams = component_mapper.get_teams_for_path(path)
                    qac_result.components = component_mapper.get_component_names_for_path(path)

                    # check if severity is >= min_severity, if so add result to list
                    if severity >= min_severity:
                        qac_results.append(qac_result)
                except IndexError as idx_error:
                    print(line)
                    print(idx_error.message)
                    sys.exit(33)

    return qac_results


def check_if_analyze_line(exception_wildcards, line):
    """ This method determines whether a line of the analysis file shall be analyzed or not

    :param exception_wildcards: List of wildcard expressions in order to exclude files from the analysis
    :param line: The current line of the analysis file
    :return: True if the line shall be analyzed, False otherwise
    """
    is_line_empty = line.strip() == ""
    is_overview_line = "// =" in line
    is_harderror_line = "- was analyzed resulting" in line
    is_diagnostics_line = " diagnostics found" in line
    has_no_result_in_db = "no results for this file in the database" in line
    is_excepted = False
    is_stdout_line = "STDOUT" in line
    is_last_line = "success" in line
    is_log_line = "See log" in line
    for wildcard in exception_wildcards:
        if wildcards.matches_wildcard_pattern(line.lower().strip(), wildcard.lower()):
            is_excepted = True
            break

    return not [is_line_empty, is_overview_line, is_harderror_line,
                is_diagnostics_line, has_no_result_in_db, is_excepted, is_stdout_line, is_last_line, is_log_line].__contains__(True)


def create_csv_report(qac_results, team_warnings_file):
    """Create a csv report containing the qac results.

    :param qac_results: A list containing QacResult objects
    :param team_warnings_file: Path and filename of the xlsx output report file
    """
    LOGGER.info("Generating csv report to %s", team_warnings_file)

    if not os.path.exists(os.path.dirname(os.path.abspath(team_warnings_file))):
        os.makedirs(os.path.dirname(os.path.abspath(team_warnings_file)))

    with open(team_warnings_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Team", "Components", "Filename", "Line number", "Severity", "Message text",
                             "Producer component:Message number"])
        for result in qac_results:
            teams = ";".join(result.teams)
            components = "; ".join(result.components)
            path = result.path
            line_number = result.line_number
            severity = result.severity
            msg_text = result.msg_text
            msg_id = result.msg_id

            csv_writer.writerow([teams, components, path, line_number, severity, msg_text, msg_id])


def create_xlsx_report(qac_results, team_warnings_file):
    """Create a workbook and add a worksheet containing the qac results.

    :param qac_results: A list containing QacResult objects
    :param team_warnings_file: Path and filename of the xlsx output report file
    """
    LOGGER.info("Generating xlsx report to %s", team_warnings_file)

    excel_max_rows = 1048576
    num_of_excel_rows = len(qac_results) + 1

    if num_of_excel_rows > excel_max_rows:
        warning = "The number of warnings exceeds the maximum number of rows in the excel sheet. {} warning(s) will not be stored! " \
                  "Consider changing to csv file format to avoid that.".format(num_of_excel_rows - excel_max_rows)
        LOGGER.warning(warning)

    if not os.path.exists(os.path.dirname(os.path.abspath(team_warnings_file))):
        os.makedirs(os.path.dirname(os.path.abspath(team_warnings_file)))

    workbook = xlsxwriter.Workbook(team_warnings_file)
    worksheet = workbook.add_worksheet("QAC Results")
    worksheet.write("A1", "Team")
    worksheet.write("B1", "Components")
    worksheet.write("C1", "Filename")
    worksheet.write("D1", "Line number")
    worksheet.write("E1", "Severity")
    worksheet.write("F1", "Message text")
    worksheet.write("G1", "Producer component:Message number")

    for idx, result in enumerate(qac_results):
        worksheet.write(idx + 1, 0, ", ".join(result.teams))
        worksheet.write(idx + 1, 1, ", ".join(result.components))
        worksheet.write(idx + 1, 2, result.path)
        worksheet.write(idx + 1, 3, result.line_number)
        worksheet.write(idx + 1, 4, result.severity)
        worksheet.write(idx + 1, 5, result.msg_text)
        worksheet.write(idx + 1, 6, result.msg_id)
    workbook.close()


def combine_csv_reports(team_warnings_file1, team_warnings_file2):
    """Combine two csv reports into one (for qac and qacpp analysis)

    :param team_warnings_file1: Path and filename of the first csv output report file
    :param team_warnings_file2: Path and filename of the second csv output report file
    """
    LOGGER.info("Combining  %s and %s", team_warnings_file1, team_warnings_file2)

    #output csv
    fout = open("team_mapping_qac.csv", "a")

    # first file:
    for line in open(team_warnings_file1):
        fout.write(line)

    # second file:
    file2 = open(team_warnings_file2)

    # skip the header as it is the same one
    next(file2)
    for line in file2:
        fout.write(line)
    file2.close()
    fout.close()

def check_changed_lines_file(changed_files, warnings_report):
    changed_files_pr = read_changed_files(changed_files)
    relevant_warnings = []

    with open(warnings_report, 'r') as warnings:
        csv_reader = reader(warnings)
        for row in csv_reader:
            if (row[2]) in changed_files_pr:
                if int(row[3]) in changed_files_pr[os.path.abspath(row[2])]:
                    relevant_warnings.append(row)

    report = ('\n' + 20 * '-' + '\n').join(map(str, relevant_warnings))
    print(report)

    if relevant_warnings:
        LOGGER.error("The changed files introduced new warnings!")
        sys.exit(-1)

def check_warning_week(changed_files, warnings_report, warnings_week):
    changed_files_pr = read_changed_files(changed_files)
    relevant_warnings = []

    with open(warnings_report, 'r') as warnings:
        csv_reader = reader(warnings)
        for row in csv_reader:
            if (row[2]) in changed_files_pr:
                if (row[6]) in warnings_week:
                    relevant_warnings.append(row)

    report = ('\n' + 20 * '-' + '\n').join(map(str, relevant_warnings))
    print(report)

    if relevant_warnings:
        LOGGER.error("The changed files has warnings of the week, please fix them before merging the PR!")
        sys.exit(-1)
