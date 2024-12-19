#!/usr/bin/env python3
"""
process jira problem ticket data

# Author: Dirk Bodenschatz (XC-DA/ESS1), Jochen Held (XC-DA/EDB7)
"""
import os
import glob
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class problem_obj(object):
    def __init__(self):
        self.severity = "n.a."
        # [Open,In Progress, Closed]
        self.counts = [0, 0, 0]


adoc_table_cfg = {
    "headerFormat": '[width="100%", cols="1a,1a,1a,1a", options="header"]',
    "tableName": ".Problems Statistics",
    "ColumnTitles": "| Severity | Open| In Progress| Closed",
}


def write_problem_stats(output_file, problem_obj):

    with open(
        Path(output_file),
        "w+",
        newline="",
        # encoding="utf-8-sig",
    ) as adoc_file:
        # adoc_file.write("." + adoc_table_cfg["tableName"] + os.linesep)
        adoc_file.write(adoc_table_cfg["headerFormat"] + os.linesep)
        adoc_file.write("|===" + os.linesep)
        adoc_file.write(adoc_table_cfg["ColumnTitles"] + os.linesep)
        for item in problem_obj:
            # Iteration  class items
            # attr name after (self.) and value is the value of self.xxx = ...
            for attr, value in vars(item).items():
                if attr == "severity":
                    adoc_file.write("|" + str(value))
                    # adoc_file.write(os.linesep)
                elif attr != "severity":
                    for x in value:
                        adoc_file.write("|" + str(x))
                    # adoc_file.write(os.linesep)
            adoc_file.write(os.linesep)
        adoc_file.write("|===" + os.linesep)


def generate_problem_object(f_jira_problem_dict):

    # Define the List to filled based jira tickets
    problems = []

    # Add "Strong" the severity list
    problem_information = problem_obj()
    problem_information.severity = "Strong"
    problems.append(problem_information)

    # Add "Medium" the severity list
    problem_information = problem_obj()
    problem_information.severity = "Medium"
    problems.append(problem_information)

    # Add "Minor" the severity list
    problem_information = problem_obj()
    problem_information.severity = "Minor"
    problems.append(problem_information)

    # Add "Total" to the end of the severity list
    # Important: Expected to be at the End of the list!!!
    problem_information = problem_obj()
    problem_information.severity = "Total"
    problems.append(problem_information)

    for tickets in f_jira_problem_dict:
        for prob in problems:
            if prob.severity == tickets["Severity"]:
                if tickets["IssueStatus"] == "Open":
                    # increment count per severity
                    prob.counts[0] += 1
                    # increment count in total
                    problems[-1].counts[0] += 1
                if tickets["IssueStatus"] == "Closed":
                    # increment count per severity
                    prob.counts[2] += 1
                    # increment count in total
                    problems[-1].counts[2] += 1
                else:
                    # increment count per severity
                    prob.counts[1] += 1
                    # increment count in total
                    problems[-1].counts[1] += 1

    return problems


def generate_problem_stats_adoc(export_dir, adoc_input_dir):

    jira_problem_int_full = []
    jira_problem_ext_full = []

    for counter, file in enumerate(
        glob.glob(
            str(Path(export_dir)) + "/**/*.json",
            recursive=True,
        )
    ):
        try:
            with open(file, "r", newline="", encoding="utf-8-sig") as json_file:
                json_data = json.load(json_file)

                filename = Path(file).stem

                if "_int" in filename:
                    jira_problem_int_full = jira_problem_int_full + json_data

                elif "_ext" in filename:
                    jira_problem_ext_full = jira_problem_ext_full + json_data
        except EnvironmentError:
            logger.error("Importing " + Path(file).name + "failed")

    problem_stats_int = generate_problem_object(jira_problem_int_full)
    problem_stats_ext = generate_problem_object(jira_problem_ext_full)

    write_problem_stats(
        Path(adoc_input_dir).joinpath("Problem_stats_int.txt"), problem_stats_int
    )
    write_problem_stats(
        Path(adoc_input_dir).joinpath("Problem_stats_ext.txt"), problem_stats_ext
    )


def main():

    input_dir = (
        "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/export/jira_export"
    )
    output_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/adoc_input/"

    generate_problem_stats_adoc(input_dir, output_dir)


if __name__ == "__main__":
    main()
