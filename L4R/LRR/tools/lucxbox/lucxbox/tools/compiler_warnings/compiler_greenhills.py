""" Greenhills Compiler Class """
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.compiler_warnings import compiler, compiler_warning

LOGGER = lucxlog.get_logger()


class Compiler(compiler.CompilerBase):

    def __init__(self):
        name = "greenhills"
        regex = r'"(\S*)", line (\d+): warning #(.*?):\s[\r\n]*([^^]*?)(?:\^|\n{4})'
        regex_unknown_warnings = r'"(\S*)", At (end) of source: warning #(.*?):([^\n]*)'
        linker_warning_regex = r'\[(elxr)\] \(warning #([^\)]*)\)(.*)\(([^)]*)\.o\)([^\n]*)'
        super(Compiler, self).__init__(name, regex, regex_unknown_warnings, True, None, linker_warning_regex)

    def get_warnings_from_lines(self, lines, filemapping):
        """ Extracts warnings from log lines and returns list of CompilerWarnings and linkerWarnings"""
        warnings = []
        for line in lines:
            matches = self.compiled_regex.findall(line)
            for match in matches:
                warnings.append(compiler_warning.CompilerWarning
                                (match[0],
                                 int(match[1]),
                                 None,
                                 match[3].strip().replace(';', '').replace('\r', '').replace('\n', ''),
                                 match[2],
                                 'compiler'
                                )
                               )
            matches = self.compiled_regex_unknown_warning.findall(line)
            for match in matches:
                warnings.append(compiler_warning.CompilerWarning
                                (match[0],
                                 match[1],
                                 None,
                                 match[3].strip().replace(';', '').replace('\r', '').replace('\n', ''),
                                 match[2],
                                 'compiler'
                                )
                               )
            matches = self.compiled_regex_linker_warning.findall(line)
            for match in matches:
                filename = match[3].strip(".o")
                filepath = filemapping.get(filename) or filename
                warnings.append(compiler_warning.CompilerWarning
                                (filepath,
                                 match[0],
                                 None,
                                 (match[2]+match[4]).strip().replace(';', '').replace('\r', '').replace('\n', ''),
                                 match[1],
                                 'linker'
                                )
                               )
        return warnings
