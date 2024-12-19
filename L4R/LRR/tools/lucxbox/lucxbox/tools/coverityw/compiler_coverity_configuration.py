#!/usr/bin/python
""" coverity compiler configuration object """


class CompilerCoverityConfiguration:

    def __init__(self):
        self.build_command = ''
        self.path = ''
        self.configs = []
        self.build_args = ''
