""" Clang Compiler Class """
import re

from lucxbox.lib import lucxlog
from lucxbox.tools.compiler_warnings import compiler, compiler_warning

LOGGER = lucxlog.get_logger()


class Compiler(compiler.CompilerBase):

    def __init__(self):
        name = "clang"
        regex = r"(\S*):(\d+):.*?PRQA\sS\s(?:QACPP\()?(\d+(?:,\s?\d+)*)(?:\))?(.*)"
        regex_unknown_warnings = r"(\S*):(\d+):.*?PRQA\sS\s(?:QACPP\()?(\d+(?:,\s?\d+)*)(?:\))?"
        super(Compiler, self).__init__(name, regex, regex_unknown_warnings)

    def get_warnings_from_lines(self, lines):
        """ Extracts warnings from log lines and returns list of CompilerWarnings """
        regex_multiple_warnigns = re.compile(r"// PRQA .* //")

        warnings = []
        for line in lines:
            while True:
                matches = self.compiled_regex.findall(line)
                for match in matches:
                    warnings.append(compiler_warning.CompilerWarning(match[0], int(match[1]), None, match[3].strip(), match[2].strip()))
                if not matches:
                    matches = self.compiled_regex_unknown_warning.findall(line)
                    for match in matches:
                        warnings.append(compiler_warning.CompilerWarning(match[0], int(match[1]), None, "", match[2].strip()))
                # VIDEOGENTHREE-45605 Support multiple exceptions per line
                if re.search(regex_multiple_warnigns, line):
                    line = re.sub(regex_multiple_warnigns, "//", line)
                    continue
                break
        return warnings
