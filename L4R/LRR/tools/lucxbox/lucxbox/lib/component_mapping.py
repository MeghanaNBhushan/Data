""" Map components by COMPONENTS file """
import os
import sys

from lucxbox.lib.finder import get_git_topmost_root
from lucxbox.lib.lucxlog import get_logger
from lucxbox.lib.wildcards import matches_wildcard_pattern

LOGGER = get_logger()

class Component:
    def __init__(self, pattern, team, root):
        self.pattern = pattern
        self.team = team
        self.root = root

class ComponentMapper:
    """
    Component mapper class that generates components out of a provided components file

    :param use_absolute_paths: Use absolute paths when comparing component patterns.
                               Can be used when mapping warnings from different workspace.
    """

    def __init__(self, components_codeowners_file, use_relative_paths=False):
        if components_codeowners_file:
            component_codeowner_files = [components_codeowners_file]
            if isinstance(components_codeowners_file, list):
                component_codeowner_files = components_codeowners_file
        else:
            component_codeowner_files = self.get_codeowner_files()

        self.components = []
        for cc_file in component_codeowner_files:
            LOGGER.debug("Initializing new component mapper from COMPONENTS file '%s'", cc_file)

            if not os.path.exists(cc_file):
                LOGGER.critical("Components file %s does not exist. Exiting", cc_file)
                sys.exit(-1)

            with open(cc_file) as codeowners_file:
                for line in codeowners_file:
                    is_line_empty = line.strip() == ""
                    is_comment_line = line.startswith("#")

                    if not is_line_empty and not is_comment_line:
                        line_split = line.strip().split("@")
                        if use_relative_paths:
                            component_pattern = line_split.pop(0).strip()
                        else:
                            component_pattern = os.path.dirname(os.path.abspath(cc_file)) + os.sep + line_split.pop(0).strip()
                        component_pattern = component_pattern.replace('\\', '/')

                        while line_split:
                            component_team = line_split.pop(0).strip()
                            new_component = Component(component_pattern, component_team, os.path.abspath(os.path.dirname(cc_file)))
                            self.components.append(new_component)

    def get_components_for_path(self, path):
        """
        Checks for matches between the components, read from the components file, and the provided path.

        :param path: The path to check for matches with the components file
        :return: The resulting list of matches of components
        """
        components_for_path = []
        for component in self.components:
            if matches_wildcard_pattern(path, component.pattern):
                LOGGER.debug("Pattern '%s' matches file path '%s'", component.pattern, path)
                components_for_path += [component]
        return components_for_path

    def get_component_names_for_path(self, path):
        """
        Get component names for a provided path. This function searches the component patterns for component names
        and filters out the wildcard information such as *, **, or /

        :param path: The path to find the component name for
        :return: A list of components, that belong to the respective path
        """
        components = self.get_components_for_path(path)
        component_names = []
        for component in components:
            component_name = component.pattern.replace('*', '')
            component_name = os.path.relpath(component_name, component.root)
            component_names.append(component_name.replace('\\', '/'))

        return component_names

    def get_teams_for_path(self, path):
        """
        Determine the associated team to a provided path.

        :param path: The path to the file that shall be linked with a team
        :return: The name of the team associated with the file. if no component matches, the team will be called "undefined".
        """
        teams = []
        for component in self.components:
            if matches_wildcard_pattern(path, component.pattern) and component.team not in teams:
                teams.append(component.team)

        if teams:
            return teams
        else:
            return ["undefined"]


def get_codeowner_files():
    # TBD evaluate all Codeowner files in repo/submodules
    root = get_git_topmost_root()
    codeowners = os.path.join(root, "CODEOWNERS")
    if os.path.isfile(codeowners):
        return[codeowners]
    return []
