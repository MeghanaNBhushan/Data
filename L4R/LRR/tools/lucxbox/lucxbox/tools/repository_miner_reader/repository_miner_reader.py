#!/bin/env python3
""" Check for files that might need to be co-modified based on previous merge commit history """

import argparse
import os
import subprocess
import sys
import json
import calendar
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog

LOGGER = lucxlog.get_logger()

def parse_args(arguments):
    desc = "Writes out a txt file that contains suggestions about files that can be co-modified based on " + \
           "association analysis of the previous merge commit history association rules derived by Repository Miner."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--branch", "-b", required=True, help="association rules derived for the given branch " + \
                                                              "will be compared with modifications in the branch " + \
                                                              "you are currently on")
    parser.add_argument("--association-rules-file", "-f", required=True, help="path of the txt file containing " + \
                                                                              "association rules")
    parser.add_argument("--output-path", "-o", required=True, help="path where the comment file shall be stored")
    parser.add_argument("--stats-path", "-s", required=False, help="statistics will be written out here")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args(arguments)


def get_modifications_in_branch(branch):
    LOGGER.debug('Getting modifications in branch %s', branch)
    modifications = []
    subprocess.check_call(["git", "fetch", "origin", "{branch_name}:{branch_name}".format(branch_name=branch)],
                          stderr=subprocess.STDOUT)
    for line in subprocess.check_output(["git", "diff", branch, "--name-only"]).splitlines():
        line = line.decode("utf-8").strip()
        modifications.append(line)
    return modifications


def get_association_rules(association_rules_file):
    LOGGER.debug('Reading association rules')
    return json.load(open(association_rules_file))


def get_comment(rules, modifications, stats_path, branch):
    LOGGER.debug('Building comment')
    comment = ''

    if len(rules) == 0 or len(modifications) == 0:
        return comment

    suggested_files = {}

    for rule in rules:
        not_found = False
        antecedent = rules[rule]['antecedent']
        for antecedent_file in antecedent:
            if antecedent_file not in modifications:
                not_found = True

        if not not_found:
            consequent = rules[rule]['consequent']
            for consequent_file in consequent:
                if consequent_file not in modifications:
                    confidence = rules[rule]['confidence']
                    if consequent_file not in suggested_files:
                        suggested_files[consequent_file] = confidence
                    elif suggested_files[consequent_file] < confidence:
                        suggested_files[consequent_file] = confidence

    if len(suggested_files) != 0:
        comment += 'Based on association analysis of the previous commit history you should also check if ' \
                   'modifications in following files are needed:'
        for suggestion in suggested_files:
            comment += '\\n - {}, Probability for required changes: {}'.format(suggestion, suggested_files[suggestion])

        if stats_path:
            write_out_stats(stats_path, branch, suggested_files)

    return comment


def write_out_comment(comment, output_path):
    LOGGER.debug('Writing out comment to txt file')
    with open(output_path, 'w') as file:
        file.write(comment)
        file.close()


def write_out_stats(stats_path, branch, suggested_files):
    LOGGER.debug("Writing out stats to '%s'", stats_path)
    timestamp = calendar.timegm(time.gmtime())
    stats_file = os.path.join(stats_path, 'stats_{branch_name}.json'.format(branch_name=branch))
    stats_dict = {}
    if os.path.exists(stats_file):
        stats_dict = json.load(open(stats_file, 'r'))
        os.remove(stats_file)
    stats_dict[timestamp] = suggested_files
    with open(stats_file, 'w') as file:
        file.write(json.dumps(stats_dict, indent=4))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv[1:])
    LOGGER.setLevel(args.log_level)

    modifications = get_modifications_in_branch(args.branch)
    rules = get_association_rules(args.association_rules_file)
    comment = get_comment(rules, modifications, args.stats_path, args.branch)
    write_out_comment(comment, args.output_path)


if __name__ == "__main__":
    main()
