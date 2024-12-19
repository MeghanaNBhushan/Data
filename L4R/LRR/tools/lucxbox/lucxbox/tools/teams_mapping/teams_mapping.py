import argparse
import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import component_mapping, lucxargs, lucxlog

LOGGER = lucxlog.get_logger()


def parse_args():
    desc = "Map input csv warnings report with COMPONENTS file."
    parser = argparse.ArgumentParser(description=desc)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    parser.add_argument('-r', '--report', required=True, type=str,
                        help='''The path to the input report file with warnings
                        in csv format. Any report we want to fit Team and Component
                        information and map it by mapping-column''')
    parser.add_argument('-c', '--components', required=True,
                        type=str, help='The path to the COMPONENTS file')
    parser.add_argument('-t', '--teams-report', required=True, type=str,
                        help='''The output csv report filepath and filename.
                                Output format is based on the input file dialect provided.''')
    parser.add_argument('-m', '--mapping-column', required=False, default='Filename',
                        type=str, help='Column name for mapping. Usually this is "File", "FilePath", etc.')
    parser.add_argument('-l', '--delimiter', required=False, type=str, default=',', choices=[',', ';', ':', '|'],
                        help='A one-character string used to separate fields.')
    parser.add_argument('-g', '--gitignore-mapping', action='store_true',
                        help='''Switch to enable of team mapping that implements gitignore specification -
                                within one level of precedence, the last matching pattern decides the outcome''')
    return parser.parse_args()


def get_csv_dialect(csv_path):
    """ This is the function to obtain dialect from input report file

    :param csv_path: The path to the report file in csv format containing the warnings
    """
    with open(csv_path, mode='r', newline='') as csv_file:
        return csv.Sniffer().sniff(csv_file.read(1024))


def get_rows_before_header(csv_path, csv_delimiter):
    """ This is the function to check and get numbers of rows before header for
        cases if input report file has additional information or declamers before main table.

    :param csv_path: The path to the report file in csv format containing the warnings
    :param csv_delimiter: Delimiter used for report file creation
    """
    with open(csv_path, mode='r', newline='') as csv_file:
        LOGGER.debug(
            "Checking if csv report %s contains rows before header", csv_path)
        reader = csv.reader(csv_file, delimiter=csv_delimiter)
        idx = next(idx for idx, row in enumerate(reader) if len(row) > 1)
    return idx


def add_fieldnames(add_fieldnames, fieldnames):
    """ This is the function is add new fields to the header(fieldnames).

    :param add_fieldnames: The new filednames list
    :param fieldnames: Current fieldnames list, we can get it as 'dict_reader.fieldnames'
    """
    current_fieldnames = fieldnames
    for field in add_fieldnames:
        if field not in current_fieldnames:
            LOGGER.debug("%s fieldname not in the : %s ", field, fieldnames)
            current_fieldnames.append(field)
    return current_fieldnames


def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)
    if not os.path.exists(args.report):
        LOGGER.critical("Report file %s does not exist. Exiting", args.report)
        sys.exit(-1)

    delimiter = args.delimiter

    LOGGER.info("Input csv report file is %s", args.report)
    LOGGER.info("Input COMPONENTS file is %s", args.components)
    LOGGER.info("Result csv report file is %s", args.teams_report)
    LOGGER.debug("Input csv report file delimiter is '%s'", delimiter)

    # Check if Input report file with warnings contains lines before header
    skip_rows = get_rows_before_header(args.report, delimiter)
    LOGGER.debug(
        "Input csv report contains rows before header: %s ", skip_rows)

    # Read COMPONENTS file and put it into array
    LOGGER.debug("Trying to set components from file '%s'", args.components)
    component_mapper = component_mapping.ComponentMapper(args.components)

    with open(args.report, 'r', newline='') as in_csv_file, open(args.teams_report, 'w', newline='') as out_csv_file:

        # If input report contains lines before header(fieldnames) skip this lines
        if skip_rows > 0:
            for _ in range(skip_rows):
                next(in_csv_file)

        dict_reader = csv.DictReader(
            in_csv_file, delimiter=delimiter, quotechar='"')

        LOGGER.debug("Input csv fieldnames: %s ", dict_reader.fieldnames)

        # Add 2 new columns to the current header(fieldnames)
        fieldnames = add_fieldnames(
            ['Team', 'Components'], dict_reader.fieldnames)

        dict_writer = csv.DictWriter(
            out_csv_file, fieldnames=fieldnames, delimiter=delimiter)
        LOGGER.debug("Output csv fieldnames: %s ", fieldnames)
        dict_writer.writeheader()

        for row in dict_reader:
            path = row[args.mapping_column].replace('\\', '/')
            teams = component_mapper.get_teams_for_path(path)
            components = component_mapper.get_component_names_for_path(path)
            if args.gitignore_mapping:
                row['Team'] = teams[-1] if teams else ''
                row['Components'] = components[-1] if components else ''
            else:
                # Since get_teams_for_path and get_component_names_for_path output is list
                # for better view used join with delimiter ';'. Delimiter should be rather than main csv delimiter.
                row['Team'] = ";".join(teams)
                row['Components'] = ";".join(components)
            dict_writer.writerow(row)

if __name__ == "__main__":
    main()
