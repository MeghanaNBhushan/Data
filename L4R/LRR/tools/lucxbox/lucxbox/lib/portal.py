""" Portal is a library for helping you jump around in directories. """
import os
from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()


class In:
    """ Class for changing the current working directory """

    def __init__(self, new_path):
        self.saved_path = None
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        if not os.path.exists(self.new_path):
            os.mkdir(self.new_path)
        os.chdir(self.new_path)
        LOGGER.debug("Entering '%s'", self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)
        LOGGER.debug("Changing back to '%s'", self.saved_path)


def do_for_subfolders(func, exclude=None):
    """ Function to execute a passed function in subfolders """
    folders = next(os.walk('.'))[1]
    for folder in folders:
        if exclude is not None and folder in exclude:
            continue
        func(folder)
