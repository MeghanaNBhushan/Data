# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:37:25 2021

@author: YAH3KOR
"""
import fnmatch
import os
from pathlib import Path
import sys

class Input:
    def __init__(self, parser, logger):
        self.parser = parser
        self.logger = logger


    def get_filename(self, pattern):
        
        search_path, file_pattern = os.path.split(pattern)
        
        if os.path.exists(search_path):
            for file in os.listdir(search_path):
                if fnmatch.fnmatch (file, file_pattern):
                    found_file = os.path.abspath(os.path.join(search_path, file))
                    self.logger.info(f"Found file with pattern '{pattern}': {found_file}")
                    return found_file
        
        self.logger.error(f"No file matching the pattern '{pattern}' was found.")
        sys.exit(1)
    
    def get_args(self):
    
        args = self.parser.parse_args()
        args.report_dir = os.path.abspath(str(args.report_dir))
    
        # If called from ExecuteAutomatedTestsWithPCSelection.bat file, the value 'LRZxyza' will be passed as an argument based on user selection.
        # In that case, the path to the config to the Lauterbach will be adapted from the default value: ./cfg_z6501/config_uC1.t32 respectively
        # ./cfg_z6501/config_uC2.t32. 
        args.configFileUC1 = args.trace32_config_uC1
        args.configFileUC2 = args.trace32_config_uC2
        
        args.hexfileuC1 = ""
        if args.hexfile_pattern_uC1 :
            args.hexfileuC1 = self.get_filename(args.hexfile_pattern_uC1)
            
        args.hexfileuC2 = ""
        if args.hexfile_pattern_uC2 :
            args.hexfileuC2 = self.get_filename(args.hexfile_pattern_uC2)
     
        args.elffileuC1 = ""
        if args.elffile_pattern_uC1 :
            args.elffileuC1 = self.get_filename(args.elffile_pattern_uC1)
    
        args.elffileuC2 = ""
        if args.elffile_pattern_uC2 :
            args.elffileuC2 = self.get_filename(args.elffile_pattern_uC2)
    
    
        return args
