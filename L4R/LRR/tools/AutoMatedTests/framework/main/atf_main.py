# -*- coding: utf-8 -*-
"""
Created on Mon May  3 10:25:07 2021

@author: YAH3KOR
"""

import sys
import os
import argparse
import shutil
import subprocess
import time

sys.path.append(os.path.abspath('framework/helper'))
sys.path.append(os.path.abspath('framework/interface'))
sys.path.append(os.path.abspath('framework/scheduling'))

import AD_input_functions
import atf_testexecution
import canoe
import relay
import trace32multiapi
import logger
from pathlib import Path
import atf_globalconstants as globalConstants


uCPath = Path("unarchive/plant/L/")
hexPath=""    
uC1Path = Path("unarchive/plant_uC1/UC1/")
hexPathuC1=""    
uC2Path = Path("unarchive/plant_uC2/UC2/")
hexPathuC2=""    
for p in uC1Path.glob('**/_init/INIT_4_LAB_TEST/*ATR*_Complete.hex'):
    hexPathuC1=p
for p in uC2Path.glob('**/_init/INIT_4_LAB_TEST/*ATR*_Complete.hex'):
    hexPathuC2=p
for p in uCPath.glob('**/_init/INIT_4_LAB_TEST/*ATR*_Complete.hex'):
    hexPath=p

parser = argparse.ArgumentParser(description="Script to run automated Lauterbach scripts")
parser.add_argument("-hw", "--hardware", 
                        help='Hardware to execute tests on. Expected arguments - fr5cu', nargs='?', const='fr5cu')
parser.add_argument("-t32c1", "--trace32-config-uC1",
                        help='Path to uC1 trace32 configuration', nargs='?', const='framework/config/lauterbach_cfg/cfg_z6501/config_uC1.t32')
parser.add_argument("-t32c2", "--trace32-config-uC2",
                        help='Path to uC2 trace32 configuration', nargs='?', const='framework/config/lauterbach_cfg/cfg_z6501/config_uC2.t32')
parser.add_argument("-t32s", "--trace32-startup-script",
                        help='Path to the target startup script', nargs='?', const='C:\TOOLS\T32_Gen5\RadarGen5\StartupIfx.cmm')
parser.add_argument("-r", "--report-dir",
                        help='Directory to store the report in', const='./', nargs='?')
parser.add_argument("-hp1", "--hexfile-pattern-uC1", help='Pattern to find uC1 hex file', nargs='?',
                        const=hexPathuC1)
parser.add_argument("-hp2", "--hexfile-pattern-uC2", help='Pattern to find uC2 hex file', nargs='?',
                        const=hexPathuC2)
parser.add_argument("-ep1", "--elffile-pattern-uC1", help='Pattern to find the elf file', nargs='?',
                    const='unarchive/Radar_FR5CU_DNNN1_NNN_N_XX_2_uC1.elf')
parser.add_argument("-ep2", "--elffile-pattern-uC2", help='Pattern to find the elf file', nargs='?',
                    const='unarchive/Radar_FR5CU_DENN1_CEN_N_XX_2_uC2.elf')
parser.add_argument("-tp", "--toellner-port", help='Toellner Port ', nargs='?', const=5)
parser.add_argument("-filter", "--testcasefilter", help='Filter argument for specific test case execution', nargs='?', const='int')
parser.add_argument("-testmode", "--frameworktestmode", help='Enable/disable internal framework testmode', nargs='?', const=0, type=int)

logger_api = logger.Logger()
logger = logger_api.get_logger('AutomatedTests')    
test_failed = None


def main():
    global test_failed
    ip = AD_input_functions.Input(parser = parser, logger = logger)
    args = ip.get_args()
    t32_api = {}
    canoepath = "../../../athena_mt/pf_rbs/canoe/MAIN.cfg"
    canoe_api = canoe.CANoe(logger_api)
    canoe_api.initAndOpenConfig(os.path.abspath(canoepath))
    # give CANoe some time to settle
    time.sleep(3)
    canoe_api.setupCANoeEnvironment(tollnerPS_port = int(args.toellner_port))
    
    relay_api = relay.Relay(logger_api)
    relay_api.control("reset")
    Cmd = 'C:/TOOLS/T32_Gen5/bin/windows64/t32rem.exe localhost port=20000 QUIT' +  '\n'
    Cmd += 'C:/TOOLS/T32_Gen5/bin/windows64/t32rem.exe localhost port=20001 QUIT' +  '\n'

    try:
        setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    except:
        logger.error("Failed to open a cmd to close unclosed T32 instances")
        sys.exit(10)

    try:
        setOut, setErr = setProcess.communicate(input=Cmd)
        logger.info(setOut)
    except:
        logger.error(setErr)
        logger.info("Failed to close unclosed T32 instances..........")
        sys.exit(20)    

    if args.hardware == globalConstants.k_atf_hardwareLrr:
        t32_api[globalConstants.k_atf_hardwareLrrUc2] = trace32multiapi.Trace32MultiApi(logger_api, args.configFileUC2, 1, args.trace32_startup_script)
        t32_api[globalConstants.k_atf_hardwareLrrUc1] = trace32multiapi.Trace32MultiApi(logger_api, args.configFileUC1, 1, args.trace32_startup_script)
    else : 
        raise Exception ("Hardware not supported. Please pass hw - fr5cu only!")
    
    test_api = atf_testexecution.TestExecution(args, logger_api, canoe_api, t32_api, relay_api)      
    test_failed = test_api.run_tests()


if __name__ == "__main__":
    main()
    path = Path('./')
    os.mkdir(os.path.abspath('../../../generatedFiles/smokeTests'))
    for file in path.glob('**/*.log'):# ** in a path means any number of sub-directories in the path to match regex

        logger.info("Found : " + file.name)
        logger.info("Path  : " + str(file))
        shutil.copy(file, '../../../generatedFiles/smokeTests')

    for file in path.glob('**/*.txt'):# ** in a path means any number of sub-directories in the path to match regex

        logger.info("Found : " + file.name)
        logger.info("Path  : " + str(file))
        shutil.copy(file, '../../../generatedFiles/smokeTests')
    if test_failed :
        sys.exit(30)
    else :
        sys.exit(0)

