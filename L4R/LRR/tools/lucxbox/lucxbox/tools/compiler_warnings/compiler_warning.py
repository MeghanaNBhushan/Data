"""Compiler Warning class"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()


class CompilerWarning:
    """Compiler Warning class"""

    def __init__(self, file_path, row, column, message, type_name=None, domain='unknown'):
        if os.path.isfile(os.path.abspath(file_path)):
            self.file_path = os.path.normpath(os.path.abspath(file_path))
        else:
            self.file_path = os.path.normpath(file_path)
        self.row = row
        self.column = column
        self.message = message
        self.components = []
        self.teams = []
        self.severity = None
        self.type_name = type_name
        self.quantity = 0
        self.domain = domain

    def set_quantity(self, count):
        self.quantity = count

    def has_components(self):
        return len(self.components) > 0

    def has_severity(self):
        return self.severity is not None

    def has_type_name(self):
        return self.type_name is not None

    def has_quantity(self):
        return int(self.quantity) > 0

    def contains_component(self, component):
        for entry in self.components:
            if entry == component:
                return True
        return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        lines = [self.file_path + ':' + str(self.row)]
        lines.append('\t' + self.message)
        return '\n'.join(lines)

    def __hash__(self):

        if self.severity is None:
            severity = ""
        else:
            severity = self.severity

        if self.type_name is None:
            type_name = ""
        else:
            type_name = self.type_name

        return hash(self.file_path + str(self.row) + str(self.column) +
                    str(self.message) + repr(self.components) +
                    severity + type_name)
