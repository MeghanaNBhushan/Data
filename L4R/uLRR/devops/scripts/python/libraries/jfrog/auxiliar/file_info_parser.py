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

class FileInfoParser:
    def __init__(self, response):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", " Object initialization", g_verbose_mode, "debug_mode")
        # Class member initialization
        self.response = response

    def get_response(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_response: " + str(self.response), g_verbose_mode, "debug_mode")
        return self.response
    
    def get_repo_name(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_repo_name: " + str(self.response['repo']), g_verbose_mode, "debug_mode")
        return self.response['repo']

    def get_path(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_repo_name: " + str(self.response['path']), g_verbose_mode, "debug_mode")
        return self.response['path']

    def get_creation_datetime(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_creation_datetime: " + str(self.response['created']), g_verbose_mode, "debug_mode")
        return self.response['created']
    
    def get_creator(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_creator: " + str(self.response['createdBy']), g_verbose_mode, "debug_mode")
        return self.response['createdBy']
    
    def get_lastmodified_datetime(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_lastmodified_datetime: " + str(self.response['lastModified']), g_verbose_mode, "debug_mode")
        return self.response['lastModified']

    def get_lastmodified_author(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_lastmodified_author: " + str(self.response['modifiedBy']), g_verbose_mode, "debug_mode")
        return self.response['modifiedBy']

    def get_lastUpdated_datetime(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_lastUpdated_datetime: " + str(self.response['lastUpdated']), g_verbose_mode, "debug_mode")
        return self.response['lastUpdated']

    def get_mime_type(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_mime_type: " + str(self.response['mimeType']), g_verbose_mode, "debug_mode")
        return self.response['mimeType']

    def get_size(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_mime_type: " + str(self.response['size']), g_verbose_mode, "debug_mode")
        return self.response['size']

    def get_checksums_sha256(self):
        ConsoleOutput(bcolors.OKBLUE, "FileInfoParser", "Retrieving - get_checksums_sha256: " + str(self.response['checksums']['sha256']), g_verbose_mode, "debug_mode")
        return self.response['checksums']['sha256']
  