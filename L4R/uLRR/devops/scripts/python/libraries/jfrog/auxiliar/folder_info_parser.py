__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""
import sys

"""Import of Python Utils"""
sys.path.insert(1, '../../scripts/python/')
from python_utilities import *

import json

# Console output switch
global g_verbose_mode
g_verbose_mode = False

class FolderInfoParser:
    def __init__(self, response):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", " Object initialization", g_verbose_mode, "debug_mode")
        # Class member initialization
        self.response = response

    def get_response(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_response: " + str(self.response), g_verbose_mode, "debug_mode")
        return self.response
    
    def get_repo_name(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_repo_name: " + str(self.response['repo']), g_verbose_mode, "debug_mode")
        return self.response['repo']

    def get_path(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_repo_name: " + str(self.response['path']), g_verbose_mode, "debug_mode")
        return self.response['path']

    def get_creation_datetime(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_creation_datetime: " + str(self.response['created']), g_verbose_mode, "debug_mode")
        return self.response['created']
    
    def get_creator(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_creator: " + str(self.response['createdBy']), g_verbose_mode, "debug_mode")
        return self.response['createdBy']
    
    def get_lastmodified_datetime(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_lastmodified_datetime: " + str(self.response['lastModified']), g_verbose_mode, "debug_mode")
        return self.response['lastModified']

    def get_lastmodified_author(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_lastmodified_author: " + str(self.response['modifiedBy']), g_verbose_mode, "debug_mode")
        return self.response['modifiedBy']

    def get_lastUpdated_datetime(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_lastUpdated_datetime: " + str(self.response['lastUpdated']), g_verbose_mode, "debug_mode")
        return self.response['lastUpdated']

    def get_children(self):
        ConsoleOutput(bcolors.OKBLUE, "FolderInfoParser", "Retrieving - get_children: " + str(self.response['children']), g_verbose_mode, "debug_mode")
        return self.response['children']

        