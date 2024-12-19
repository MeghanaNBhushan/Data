""" Greenhills Compiler Class """
from swq.compiler_warnings.compilers import base
from swq.compiler_warnings import compiler_warning


class Compiler(base.CompilerBase):
    """ Compiler implementation for greenhills compiler"""
    def __init__(self):
        name = "greenhills"
        line_regex = r'"(\S*)", line (\d+):'
        warning_regex = r'warning (.*?):\s[\r\n]*([^^]*?)(?:\^|\n{4})'
        regex = line_regex + ' ' + warning_regex
        regex_unknown_warnings = \
            r'"(\S*)", At (end) of source: warning #(.*?):([^\n]*)'
        linker_warning_regex = \
            r'\[(elxr)\] \(warning #([^\)]*)\)(.*)\(([^)]*)\.o\)([^\n]*)'
        super().__init__(name, regex, regex_unknown_warnings, True, None,
                         linker_warning_regex)

    def get_warnings_from_lines(self, lines, filemapping):
        """
        Extracts warnings from log lines and returns list of CompilerWarnings
        and linkerWarnings
        """
        warnings = []
        for line in lines:
            matches = self.compiled_regex.findall(line)
            for match in matches:
                warnings.append(
                    compiler_warning.CompilerWarning(
                        match[0], int(match[1]),
                        None, match[3].strip().replace(';', '').replace(
                            '\r', '').replace('\n', ''), match[2], 'compiler'))
            matches = self.compiled_regex_unknown_warning.findall(line)
            for match in matches:
                warnings.append(
                    compiler_warning.CompilerWarning(
                        match[0], match[1], None, match[3].strip().replace(
                            ';', '').replace('\r', '').replace('\n', ''),
                        match[2], 'compiler'))
            matches = self.compiled_regex_linker_warning.findall(line)
            for match in matches:
                filename = match[3].strip(".o")
                filepath = filemapping.get(filename) or filename
                warnings.append(
                    compiler_warning.CompilerWarning(
                        filepath, match[0], None,
                        (match[2] + match[4]).strip().replace(';', '').replace(
                            '\r', '').replace('\n', ''), match[1], 'linker'))
        return warnings
