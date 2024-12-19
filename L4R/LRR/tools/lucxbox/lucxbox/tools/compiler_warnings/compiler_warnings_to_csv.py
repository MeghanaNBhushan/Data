""" Helper component for warnings parser. """

import sys
import os
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()

def write_csv(warnings_file, warnings, gitignore_mapping, add_package_info):
    """Create a csv report containing the compiler warnings.

    :param csv_file: output file
    :param warnings: list containing the compiler warnings
    :param gitignore_mapping: use gitignore specification for teams and components
    :param add_package_info: add package and sw layer info
    """
    LOGGER.debug("Preparing to write new csv file '%s'", warnings_file)

    with open(warnings_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if add_package_info:
            csv_writer.writerow(["File path", "File name", "Row", "Column", "Components", "Team", "Package", "Layer", "Message", "Severity",
                                 "Type", "Number of occurrences"])
        else:
            csv_writer.writerow(["File path", "File name", "Row", "Column", "Components", "Team", "Message", "Severity", "Type",
                                 "Number of occurrences"])
        for warning in warnings:
            name = os.path.basename(warning.file_path)
            if gitignore_mapping:
                teams = warning.teams[-1] if warning.teams else ''
                components = warning.components[-1] if warning.components else ''
            else:
                teams = "/ ".join(warning.teams)
                components = "/ ".join(warning.components)
                # If package info is required (NRCS) in the COMPONENTS file,
                # following syntax is expected #**/component/** @team-package-layer
                if add_package_info:
                    package = ""
                    layer = ""
                    if "-" in teams:
                        line_split = teams.split("-")
                        teams = line_split.pop(0).strip()
                        package = line_split.pop(0).strip()
                        layer = line_split.pop(0).strip()

                    csv_writer.writerow([warning.file_path, name, warning.row, warning.column, components, teams,
                                         package, layer, warning.message, warning.severity, warning.type_name, warning.quantity])
                else:
                    csv_writer.writerow([warning.file_path, name, warning.row, warning.column, components, teams,
                                         warning.message, warning.severity, warning.type_name, warning.quantity])
