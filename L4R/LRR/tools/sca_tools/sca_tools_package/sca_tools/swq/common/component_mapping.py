# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: component_mapping.py
# ----------------------------------------------------------------------------
""" Map components by codeowners file """
import collections
import re

from os import path
from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, RC_INVALID_FILEPATH
from swq.common.filesystem.filesystem_utils import open_t

WILDCARD_CACHE = {}


def _apply_codeowners_globbing_rules(wildcard_expression):
    if not (wildcard_expression.startswith('**') or
            (wildcard_expression.startswith('/'))):

        if wildcard_expression.startswith('*'):
            if '/' not in wildcard_expression:
                wildcard_expression = '**/{}'.format(wildcard_expression)

        if wildcard_expression.count('/') > 1:
            wildcard_expression = '/{}'.format(wildcard_expression)
        else:
            if wildcard_expression.endswith('/') or (
                    '/' not in wildcard_expression):
                wildcard_expression = '**/{}'.format(wildcard_expression)

    if wildcard_expression.endswith('/'):
        wildcard_expression = '{}**'.format(wildcard_expression)

    return wildcard_expression


def matches_wildcard_pattern(string, wildcard_expression):
    """
    Method for checking if string matches a unix-like wildcard
    expression.
    """
    string = string.replace('\\', '/')
    if not string.startswith('/'):
        string = '/{}'.format(string)

    if wildcard_expression not in WILDCARD_CACHE:
        wildcard_expression = _apply_codeowners_globbing_rules(
            wildcard_expression)
        regex_pattern = wildcard_expression.replace('.', '\\.')
        regex_pattern = regex_pattern.replace("/", '\\/')
        regex_pattern = regex_pattern.replace('*', '[^\\/]*')
        regex_pattern = regex_pattern.replace('[^\\/]*[^\\/]*', '.*')
        regex = re.compile(regex_pattern)
        WILDCARD_CACHE[wildcard_expression] = regex
    else:
        regex = WILDCARD_CACHE[wildcard_expression]

    match = re.match(regex, string)

    return match and match.group(0) == string


def no_regex_matches(regex_list, string):
    """Checks if string does not match any of regular expression in list"""
    return not any(re.search(regex, string) for regex in regex_list)


class ComponentMapper:
    """Component mapper class that generates components out of a provided
    codeowners file"""
    def __init__(self, components_codeowners_files: list):
        self.components = []

        for components_codeowners_file in components_codeowners_files:
            LOGGER.debug(
                "Initializing component mapper from codeowners file '%s'",
                components_codeowners_file)

            if not path.exists(components_codeowners_file):
                LOGGER.error("Codeowners file '%s' does not exist. Exiting",
                             components_codeowners_file)
                log_and_exit(RC_INVALID_FILEPATH)

        self.__processing_codeowners_files(components_codeowners_files)

    def __processing_codeowners_files(self, components_codeowners_files: list):
        component = collections.namedtuple("Component", "pattern team")
        for components_codeowners_file in components_codeowners_files:
            with open_t(components_codeowners_file) as codeowners_file:
                for line in codeowners_file:
                    is_line_empty = line.strip() == ""
                    is_comment_line = line.startswith("#")

                    if not (is_line_empty or is_comment_line):
                        line_split = line.strip().split("@")
                        component_pattern = line_split.pop(0).strip()

                        component_teams = [team.strip() for team in line_split]
                        self.components.append(
                            component(pattern=component_pattern,
                                      team=component_teams))

    def get_components_for_path(self, filepath):
        """
        Checks for matches between the components, read from the
        codeowners file, and the provided path.

        :param filepath: The path to check for matches with the
        codeowners file
        :return: The resulting list of matches of components
        """
        components_for_path = []
        for component in self.components:
            if matches_wildcard_pattern(filepath, component.pattern):
                LOGGER.debug("Pattern '%s' matches file path '%s'",
                             component.pattern, filepath)
                components_for_path += [component]
        return components_for_path

    def get_component_names_for_path(self, filepath):
        """
        Get component located in provided path. This function searches
        the component patterns for component names and filters out the
        wildcard information such as *, **, or /

        :param filepath: The path to find the component name for
        :return: A list of components, that belong to the respective path
        """
        components = self.get_components_for_path(filepath)
        component_names = []
        component_pattern = re.compile("\\w")
        for component in components:
            component_names.append("".join(
                re.findall(component_pattern, component.pattern)))

        return list(dict.fromkeys(component_names))

    def get_teams_for_path(self, filepath):
        """
        Get the associated team to a provided path.

        :param filepath: The path to the file that shall be linked with a team
        :return: The name of the team associated with the file.
        If no component matches, the team will be called "undefined".
        """
        teams = []
        for component in self.components:
            if matches_wildcard_pattern(filepath, component.pattern):
                teams.append(component.team)

        return teams if teams else [["undefined"]]
