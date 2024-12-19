# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:03:51 2021

@author: YAH3KOR
"""
import logging
import os
import time
import re

class Logger : 
    def __init__(self):
        self.logger_file_handler = logging.FileHandler("AD_Radar_SW_Test.log",mode="w")
        self.logger_file_handler.setLevel(logging.DEBUG)
        
        self.logger_console_handler = logging.StreamHandler()
        self.logger_console_handler.setLevel(logging.DEBUG)
        
        log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger_file_handler.setFormatter(log_format)
        self.logger_console_handler.setFormatter(log_format)
        self.report_file_handler = None
    
        
    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.logger_console_handler)
        logger.addHandler(self.logger_file_handler)
        
        if self.report_file_handler != None :
            logger.addHandler(self.report_file_handler)
        
        return logger
    
    
    def create_report(self, report_dir, logger, hw):
        logger.debug("Creating report file...........")
        
        if hw == 'fr5cu':
            report_file_path = os.path.join(report_dir, "ATR_AD_LRR_SWTest_Report.txt")
        else :
            report_file_path = os.path.join(report_dir, "SWTest_Report.txt")            
        
        path, file = os.path.split(report_file_path)
        
        if not os.path.isdir(path):
            os.makedirs(path)
            time.sleep(0.1)
    
        self.report_file_handler = logging.FileHandler(report_file_path, mode="a")
        self.report_file_handler.setLevel(logging.INFO)
    
        report_format = logging.Formatter("%(message)s")
        self.report_file_handler.setFormatter(report_format)    
        
        logger.addHandler(self.report_file_handler)
        logger.debug("Report file created.............")
        

    def create_excel(self, report_dir, logger, hw):
        logger.debug("Creating excel file...........")
        
        if hw == 'fr5cu':
            report_file_path = os.path.join(report_dir, "ATR_AD_LRR_SWTest_Report.txt")
        else :
            report_file_path = os.path.join(report_dir, "SWTest_Report.txt")            
        
        path, file = os.path.split(report_file_path)
        
        with open(report_file_path, 'r') as reader:
            for line in reader:
                print(line, end='')

        logger.debug("Report file created.............")

    
    def del_logger(self, logger):
        handlers = logger.handlers[:]
        logger.info("Reports closed")
        logger.debug(f"{handlers}")
        
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
          
