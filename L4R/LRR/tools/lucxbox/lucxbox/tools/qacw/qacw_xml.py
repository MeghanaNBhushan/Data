"""
QAC XML Output Parser

Provides interfaces to extract severity level findings
from a QAC+ XML file export.

Not intended to be executed directly and therefore does not have a main
"""

import os
import xml.etree.ElementTree as element_tree
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()


class SeverityFile:
    """Abstracting a physical file that has severity findings"""

    def __init__(self, path):
        """ Create a new severity file with empty findings

            Keyword arguments:
            path -- the path to a severity file, the current qac+ xml contains absolute paths
        """
        self.path = path
        self.component = self.guess_component_name(self.path)
        self.__findings = []

    @staticmethod
    def guess_component_name(file_path):
        """ A function to guess the component name of a given file path based on known path containments
            like inc, src, ext etc.
            We might improve this e.g. by extending the CODEOWNERS file with component patterns to repository paths

            Keyword arguments:
            file_path -- the file path string to the file to guess its component name for

            Return value:
            String -- the guessed component name for file_path
        """
        LOGGER.debug("Trying to guess component name for source/header file '%s'", file_path)

        src_inc_path = None
        if '/inc/' in file_path:
            src_inc_path = 'inc'
        if '/src/' in file_path:
            src_inc_path = 'src'
        if '/include/' in file_path:
            src_inc_path = 'include'
        if '/source/' in file_path:
            src_inc_path = 'source'
        if '/ext/' in file_path:
            src_inc_path = 'ext'

        if src_inc_path is None:
            LOGGER.debug("Did not find a suitable source or header file path indicator")
            return None

        file_path_split = file_path.split('/')
        src_inc_index = file_path_split.index(src_inc_path)

        if src_inc_index > 0:
            component_name_guess = file_path_split[src_inc_index - 1]
            LOGGER.debug("Guessed component name of file '%s' to be '%s'", file_path, component_name_guess)
            return component_name_guess

        return None

    def add_finding(self, severity_finding):
        """ Adds a new finding to the private finding list.
            Every entry has the type SeverityFinding which is also defined in this file
        """
        self.__findings.append(severity_finding)

    def get_all_findings(self):
        """Getter which just returns the private all findings list"""
        return self.__findings

    def get_findings_w_severity_levels(self, severity_levels):
        """ Returns findings that do have a severity level
            that is contained in the given severity_levels list

            Keyword arguments:
            severity_levels -- list of severity levels you want to filter findings

            Return value:
            List -- a list of findings with severity levels in the range of the given ones
        """
        found_findings = []
        for finding in self.__findings:
            if finding.severity in severity_levels:
                found_findings.append(finding)
        return found_findings

    def count_severity(self, severity_level):
        """ Function to count a given severity level violation

            Keyword arguments:
            severity_level -- the severity level as an integer to count for the current file

            Return value:
            Integer -- The number of severity violations of the given severity for the current file
        """
        LOGGER.debug("Counting severity level '%s' occurrences for file '%s'", str(severity_level), self.path)
        findings_with_severity_level_x = self.get_findings_w_severity_levels([severity_level])
        active_severity_x = 0
        for finding in findings_with_severity_level_x:
            active_severity_x += finding.active_occurrences
        return active_severity_x

    def has_finding_w_severity_levels(self, severity_levels):
        """ Method to check if the current file object has at least one finding with
            the given range of severity levels

            Keyword arguments:
            severity_levels -- A list of severity levels to check findings for

            Return value:
            Boolean -- Whether the file as a finding in the range of the given list or not
        """
        LOGGER.debug("Checking if file '%s' has finding with severity levels '%s'", self.path, \
             ','.join(str(x) for x in severity_levels))
        for finding in self.__findings:
            if finding.severity in severity_levels:
                return True
        return False

    def __str__(self):
        return str(self.path) + str(self.__findings)

    def filter_findings(self, severity_levels):
        """ Method to filter findings by kicking out findings that do not match
            the given range of severity levels.
            Will rewrite the member findings.

            WARNING: Will remove findings from file that do have severity levels not in severity_levels list!

            Keyword arguments:
            severity_levels -- A list of severity levels to filter against
        """
        LOGGER.debug("Filtering findings to only include severity levels: %s", ','.join(str(x) for x in severity_levels))
        new_findings = []
        for finding in self.__findings:
            if finding.severity in severity_levels:
                new_findings.append(finding)
        self.__findings = new_findings


class SeverityFinding:
    """ Class that abstracts a finding of the type severity.
        Could be reimplemented if we are interested in CERT warnings as well and more
        Could think about a Base "QACFinding" class where others are inheriting from
    """

    def __init__(self, level, total, active, qac_rule, text):
        self.severity = level
        self.occurrences = total
        self.active_occurrences = active
        self.qac_rule_id = qac_rule
        self.message = text


def get_files_with_severity_levels(files_with_severity_findings, severity_levels):
    """ Method for filtering a given list of SeverityFiles for certain severity levels

        Keyword arguments:
        files_with_severity_findings -- A list of SeverityFiles
        severity_levels -- A list of integer severity levels to filter files for

        Return value:
        List -- A subset of the given SeverityFiles list
    """
    files_with_given_severities = []

    for severity_file in files_with_severity_findings:
        if severity_file.has_finding_w_severity_levels(severity_levels):
            files_with_given_severities.append(severity_file)

    return files_with_given_severities


def get_severity_files_from_xml(xml_file_path):
    """ Method to read in a QAC+ XML Export file

        Keyword arguments:
        xml_file_path -- A path to the xml file, can be relative or absolute

        Return value:
        List -- A list of SeverityFiles
    """
    tree = element_tree.parse(os.path.abspath(xml_file_path))
    root = tree.getroot()

    files_with_severity_findings = []

    file_references = root.findall("./dataroot[@type='per-file']/File")

    for ref in file_references:
        severity_rule_groups = ref.findall("./tree[@type='rules']/RuleGroup")
        violation_file_path = ref.get('path')

        file_with_findings = SeverityFile(violation_file_path)
        real_finding_added = False

        for severity_rule in severity_rule_groups:
            contains_severity_level = "Severity Levels" in severity_rule.attrib["name"]
            if contains_severity_level:
                process_severity_rule(file_with_findings, files_with_severity_findings, real_finding_added, severity_rule)

    return files_with_severity_findings


def process_severity_rule(file_with_findings, files_with_severity_findings, real_finding_added, severity_rule):
    """ Helper method for processing Rules with the name 'Severity Levels' """
    outer_rules = severity_rule.findall("Rule")
    for outer_rule in outer_rules:
        inner_rules = outer_rule.findall("Rule")

        for rule in inner_rules:
            violation_severity_level = int(rule.get('text').replace('Severity Level ', ''))
            messages = rule.findall("Message")

            for message in messages:
                violations = {}
                violations["qac_rule"] = message.get('guid')
                violations["total"] = int(message.get('total'))
                violations["active"] = int(message.get('active'))
                violations["text"] = message.get('text')
                new_finding = SeverityFinding(level=violation_severity_level,
                                              total=violations["total"],
                                              active=violations["active"],
                                              qac_rule=violations["qac_rule"],
                                              text=violations["text"])
                file_with_findings.add_finding(new_finding)
                real_finding_added = True
    if real_finding_added:
        LOGGER.debug("[+File] %s", file_with_findings.path)
        files_with_severity_findings.append(file_with_findings)
