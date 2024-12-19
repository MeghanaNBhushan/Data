#!/usr/bin/python
""" coverity tcc configuration object """


class TccConfiguration:

    def __init__(self):
        self.use_tcc = False
        self.compiler_tool_name = ''
        self.compiler_relative_path = ''
        self.path = ''
        self.xml = ''
        self.install = False
        self.invoker = ''
