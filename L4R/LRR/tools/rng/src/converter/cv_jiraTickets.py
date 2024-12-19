#!/usr/bin/env python3
"""
jira ticket processing

# Author: Jochen Held (XC-DA/EDB7)
"""
import os
import glob
from pathlib import Path
import json

from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def generate_jira_tickets_adoc(input_dir, output_dir):

    # os.chdir(input_dir)

    for counter, file in enumerate(
        glob.glob(
            str(Path(input_dir)) + "/**/*.json",
            recursive=True,
        )
    ):
        try:
            with open(file, "r", newline="", encoding="utf-8-sig") as json_file:
                json_data = json.load(json_file)

                filename = Path(file).stem

                process_file = True
                if "Features" in filename:
                    adoc_table_header_Format = (
                        '[width="100%", cols="1a,5a,5a,1a", options="header"]'
                    )
                    adoc_table_header = (
                        "| ID | Feature  |  Stakeholder Summary | Status"
                    )
                elif "Problems" in filename:
                    adoc_table_header_Format = (
                        '[width="100%", cols="2a,3a,6a,3a,3a,2a", options="header"]'
                    )
                    adoc_table_header = "| ID | Summary | Description	| Severity (_see note above_)| Safety Relevance (_yes/no_) | Status"
                else:
                    process_file = False
                    logger.warning("File not processed:" + Path(file))

                if process_file == True:
                    with open(
                        Path(output_dir).joinpath(filename + ".txt"),
                        "w+",
                        encoding="utf-8",
                        newline="",
                    ) as adoc_file:
                        adoc_file.write(adoc_table_header_Format + os.linesep)
                        adoc_file.write("|===" + os.linesep)
                        adoc_file.write(adoc_table_header + os.linesep)

                        if "Features" in filename:
                            for element in json_data:
                                adoc_file.write(
                                    "| "
                                    + str(element["IssueURL"])
                                    + "["
                                    + str(element["IssueID"])
                                    + "]"
                                    + "| "
                                    + str(element["Summary"])
                                    + "| "
                                    + str(element["StakeholderSummary"])
                                    + "| "
                                    + str(element["IssueStatus"])
                                )
                                adoc_file.write(os.linesep)
                        elif "Problems" in filename:
                            for element in json_data:
                                adoc_file.write(
                                    "| "
                                    + str(element["IssueURL"])
                                    + "["
                                    + str(element["IssueID"])
                                    + "]"
                                    + "| "
                                    + str(element["Summary"])
                                    + "| "
                                    + str(element["StakeholderSummary"])
                                    + "| "
                                    + str(element["Severity"])
                                    + "| "
                                    + str(element["SafetyRelevance"])
                                    + "| "
                                    + str(element["IssueStatus"])
                                )
                                adoc_file.write(os.linesep)

                        adoc_file.write("|===" + os.linesep)
        except EnvironmentError:
            logger.error("Importing " + Path(file).name + "failed")


def main():

    input_dir = (
        "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/input/jira_export"
    )
    output_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/input/"

    generate_jira_tickets_adoc(input_dir, output_dir)


if __name__ == "__main__":
    main()
