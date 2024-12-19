""" Clang Compiler Class """
from swq.compiler_warnings import compiler_warning
from swq.compiler_warnings.compilers import base

from swq.common.logger import LOGGER


class Compiler(base.CompilerBase):
    """ Compiler implementation for clang compiler"""
    def __init__(self):
        name = "clang"
        regex = r"(\S*):(\d+):(\d+): warning:(.*)"
        regex_unknown_warnings = r"\S*: warning:(.*)"
        wregex = r"\[-W(.*)\]"
        super().__init__(name, regex, regex_unknown_warnings, False, wregex)

    def get_warnings_from_lines(self, lines):
        """
        Extracts warnings from log lines and returns list of CompilerWarnings
        """
        warnings = []
        for line in lines:
            matches = self.compiled_regex.findall(line)
            for match in matches:
                warning_name_regex = self.warning_id_regex
                warning_name_match = warning_name_regex.search(match[3])
                warning_name = None
                if warning_name_match:
                    warning_name = warning_name_match.group(1)
                    LOGGER.debug(
                        "Extracted warning name '%s' from message '%s'",
                        warning_name, match[3].strip())
                else:
                    LOGGER.warning(
                        "Did not find warning name match for warning '%s'",
                        match[3])
                warnings.append(
                    compiler_warning.CompilerWarning(match[0],
                                                     int(match[1]),
                                                     int(match[2]),
                                                     match[3].strip(),
                                                     warning_name,
                                                     domain='compiler'))
            if not matches:
                matches = self.compiled_regex_unknown_warning.findall(line)
                for match in matches:
                    warning_name_regex = self.warning_id_regex
                    warning_name_match = warning_name_regex.search(match)
                    warning_name = None
                    if warning_name_match:
                        warning_name = warning_name_match.group(1)
                        LOGGER.debug(
                            "Extracted warning name '%s' from message '%s'",
                            warning_name, match.strip())
                    else:
                        LOGGER.warning(
                            "Did not find warning name match for warning '%s'",
                            match)
                    warnings.append(
                        compiler_warning.CompilerWarning("UnKnownWarnings",
                                                         "NA",
                                                         match.strip(),
                                                         warning_name,
                                                         domain='compiler'))
        return warnings
