# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: parameter_properties.py
# ----------------------------------------------------------------------------
"""Defines SCA tools parameters properties class"""


class ParameterProperties:
    """Helper class for Params class, defines params properties"""
    def __init__(self, key, data):
        self.__key = key
        self.__data = data

    @property
    def alias(self):
        """Gets property alias"""
        return self.__data.get('alias', self.__key.lower())

    @property
    def cli(self):
        """Gets property cli"""
        return self.__data.get('cli', True)

    @property
    def env(self):
        """Gets property env"""
        return self.__data.get('env', True)

    @property
    def json(self):
        """Gets property json"""
        return self.__data.get('json', True)

    @property
    def mandatory(self):
        """Gets property mandatory"""
        return self.__data.get('mandatory', False)

    @property
    def cli_option(self):
        """Gets property cli_option"""
        return self.__data.get('cli_option', self.alias)

    @property
    def cli_option_short(self):
        """Gets property cli_option_short"""
        return self.__data['cli_option_short']

    @property
    def flag_long(self):
        """Gets property flag_long"""
        return f'--{self.cli_option}'

    @property
    def flag_short(self):
        """Gets property flag_short"""
        return f'-{self.cli_option_short}'

    @property
    def description(self):
        """Gets property description"""
        return self.__data['description']

    @property
    def deprecated(self):
        """Gets property deprecated"""
        return self.__data.get('deprecated', False)

    @property
    def deprecation_message(self):
        """Gets property deprecation message"""
        return self.__data['deprecation_message']
