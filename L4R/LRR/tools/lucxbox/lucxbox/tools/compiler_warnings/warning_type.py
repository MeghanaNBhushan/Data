"""Compiler Warning Type class"""

import json


class WarningType:
    def __init__(self, name, severity):
        self.name = name
        self.severity = severity


def load_warnings_db(db_file):
    types_db = {}
    with open(db_file, 'r') as fdb:
        types = json.load(fdb)
        for warning_type in types:
            name = warning_type['name']
            severity_name = warning_type['severity_name']
            types_db[name] = WarningType(name, severity_name)
    return types_db
