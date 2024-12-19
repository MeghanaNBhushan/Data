#!/usr/bin/python
""" coverity configuration object """


class CoverityConfiguration:

    def __init__(self):
        self.output_dir = ''
        self.dir = ''
        self.port = 0
        self.host = ''
        self.stream = ''
        self.analyze_options = ''
        self.filter = []
