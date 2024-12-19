""" Microsoft Visual Compiler Class """
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.compiler_warnings import compiler, compiler_warning

LOGGER = lucxlog.get_logger()


class Compiler(compiler.CompilerBase):

    def __init__(self):
        name = "msvc"
        regex = r">(\S*)\((\d+)\):\s+warning\s+(C\d+):(.*)\(compiling"
        wregex = r"warning\s+C\d+"
        super(Compiler, self).__init__(name, regex, None, False, wregex)

    def get_warnings_from_lines(self, lines):
        """ Extracts warnings from log lines and returns list of CompilerWarnings """
        warnings = []
        for line in lines:
            matches = self.compiled_regex.findall(line)
            for match in matches:
                warnings.append(compiler_warning.CompilerWarning(match[0], int(match[1]), None, match[3], match[2], domain='compiler'))
        return warnings
