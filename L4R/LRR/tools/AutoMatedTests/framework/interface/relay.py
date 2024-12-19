# Date  : 19.08.2020
# Author: CC-DA/EAS2 Alexander Miller
import os
import time
import argparse
import subprocess

import logger
import time

class Relay:

    logger = None
    
    def __init__(self, logger_api):
        self.logger = logger_api.get_logger("Relay")
        self.relay = None

    def control(self, behaviour):
        if behaviour == "reset":
            self.logger.debug("Resetting using relay.............")
            try:
                setProcess = subprocess.Popen('C:/TOOLS/Relay_control/CVORelayBoxInterface.exe', stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
            except:
                self.logger.error("Failed to find relay exe............")
                sys.exit(10)

            try:
                setOut, setErr = setProcess.communicate(input='0010', timeout = 10)
                self.logger.info(setOut)
            except subprocess.TimeoutExpired : 
                setProcess.kill()
                self.logger.info("No relay found................ Continue executing")
            except:
                setProcess.kill()
                self.logger.info("Failed to reset relay................")
                sys.exit(20)    
                #subprocess.run("start /b C:/TOOLS/Relay_control/CVORelayBoxInterface.exe & timeout /t 10 & taskkill /im C:/TOOLS/Relay_control/CVORelayBoxInterface.exe /f")
            time.sleep(5);

            try:
                setProcess = subprocess.Popen('C:/TOOLS/Relay_control/CVORelayBoxInterface.exe', stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
            except:
                self.logger.error("Failed to find relay exe............")
                sys.exit(10)

            try:
                setOut, setErr = setProcess.communicate(input='0000', timeout = 10)
                self.logger.info(setOut)
            except subprocess.TimeoutExpired : 
                setProcess.kill()
                self.logger.info("No relay found................ Continue executing")
            except:
                setProcess.kill()
                self.logger.info("Failed to reset relay................")
                sys.exit(20)    

            self.logger.info("SUCCESS - Resetting using relay............done")
        else :
            self.logger.error(f"No matching behaviour with relay. Expected : reset. Passed : {behaviour}")

