from warning import *

class File:
    def __init__(self, filename):
        self.filename = filename
        self.warnings = {}
        self.counter = 0

    def add_warning(self, message, position):
        if message not in self.warnings:
            # New warning in the file
            warning = Warning(message, position)
            self.warnings[message] = Warning(message, position)
            self.counter += 1
            # Known warning but on different position, in the file
        if message in self.warnings and position not in self.warnings[message].position:
            self.warnings[message].increase_counter(position)
            self.counter += 1