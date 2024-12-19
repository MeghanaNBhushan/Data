# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 08:19:05 2021

@author: cis9lr
"""
from pathlib import Path

testScriptPathList = [Path('../../component/EgoVehDataIF/test/unittest/comptest_EgoVehDataIF_x.cpp'),
 Path('../../component/LocDataIF/test/unittest/comptest_locdataif_x.cpp'),
 Path('../../component/MntPosMgmt/test/unittest/comptest_MntPosMgmt_x.cpp'),
 Path('../../component/net_x/test/unittest/comptest_net_x.cpp'),
 Path('../../component/diag/test/unittest/dsc_appl_x/test_dsc_appl_x.c'),
 Path('../../component/diag/test/unittest/dsc_appl_x/test_dsc_appl_x_callbacks.c'),
 Path('../../component/diag/test/unittest/EcuResetAdapter/test_ecu_reset_adapter.c'),
 Path('../../component/diag/test/unittest/EcuResetAdapter/test_rb_EthRstHdl.c'),
 Path('../../component/diag/test/unittest/rdbi_appl_x/test_rdbi_appl_x_eventmask.c'),
 Path('../../component/diag/test/unittest/rdbi_appl_x/test_rdbi_appl_x_identification.c'),
 Path('../../component/diag/test/unittest/rdbi_appl_x/test_rdbi_appl_x_mcs.c'),
 Path('../../component/diag/test/unittest/rdbi_appl_x/test_rdbi_appl_x_MntPosMgmt.c'),
 Path('../../component/diag/test/unittest/rdbi_appl_x/test_rdbi_appl_x_mp.c'),
 Path('../../component/diag/test/unittest/wdbi_appl_x/test_wdbi_appl_x_eventmask.c'),
 Path('../../component/diag/test/unittest/wdbi_appl_x/test_wdbi_appl_x_mcs.c'),
 Path('../../component/diag/test/unittest/wdbi_appl_x/test_wdbi_appl_x_MntPosMgmt.c'),
 Path('../../component/diag/test/unittest/wdbi_appl_x/test_wdbi_appl_x_mp.c'),
 Path('../../component/EgoVehDataIF/test/unittest/test_EgoVehDataIF_functional.c'),
 Path('../../component/diag/test/unittest/dsc_appl_x/test_dsc_appl_adapter_x.cpp'),
 Path('../../component/inputhandler/test/unittest/runnable/test_ihd_inputhandlerrunnable.cpp')]

componentPathList = ['..\\..\\component\\EgoVehDataIF\\test',
 '..\\..\\component\\LocDataIF\\test',
 '..\\..\\component\\MntPosMgmt\\test',
 '..\\..\\component\\net_x\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\EgoVehDataIF\\test',
 '..\\..\\component\\diag\\test',
 '..\\..\\component\\inputhandler\\test']

testScriptList = ['comptest_EgoVehDataIF_x',
 'comptest_locdataif_x',
 'comptest_MntPosMgmt_x',
 'comptest_net_x',
 'test_dsc_appl_x',
 'test_dsc_appl_x_callbacks',
 'test_ecu_reset_adapter',
 'test_rb_EthRstHdl',
 'test_rdbi_appl_x_eventmask',
 'test_rdbi_appl_x_identification',
 'test_rdbi_appl_x_mcs',
 'test_rdbi_appl_x_MntPosMgmt',
 'test_rdbi_appl_x_mp',
 'test_wdbi_appl_x_eventmask',
 'test_wdbi_appl_x_mcs',
 'test_wdbi_appl_x_MntPosMgmt',
 'test_wdbi_appl_x_mp',
 'test_EgoVehDataIF_functional',
 'test_dsc_appl_adapter_x',
 'test_ihd_inputhandlerrunnable']

cantataBuildOption = '0'
variant = 'Radar_FR5CU_DENN1_CEN_N_XX_2_uC2'
setCmd = 'set_env_target.bat ' + cantataBuildOption +  '\n'

import subprocess
import logging
logger = logging.getLogger("AutomatedCantataTests")
logger.setLevel(logging.DEBUG)
    
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.DEBUG)
    
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_console_handler.setFormatter(log_format)

logger.addHandler(logger_console_handler)  

import sys

#try:
#    setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
#except:
#    logger.error("Failed to open a cmd to run commands")
#    sys.exit(-1)
#    
#try:
#    setOut, setErr = setProcess.communicate(input=setCmd)
#    logger.info(setOut)
#except:
#    logger.error(setErr)
#    logger.info("Failed to set environment to seach scripts..........")
#    sys.exit(-1)
#
#logger.info("Searching directory for test scripts ............")
#path1 = Path("../../component/")
#
try:
    process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
except:
    logger.error("Failed to open a cmd to run commands")
    sys.exit(-1)


import os
cfgFile = os.path.abspath('./cfg/config_uC1.t32')
cmd = 'set_env_target.bat ' + cantataBuildOption +  '\n' + ' cd '+ os.path.abspath(os.path.join('../../../../../generatedFiles', 'CANTATA_target_'+ variant)) + '\n'
targetCmd = f'C:/TCC/Tools/python/2.7.13-2_WIN64/python.exe %TCC_CANTATA_HOME%/ExtraFiles/T_TriCore_greenhills_ifx_comp_201815_5fp_cxtri_c++11/IDEIntegration/Trace32/t32.py --debugger=C:/TOOLS/T32_Gen5/bin/windows64/t32mtc.exe --cmm=C:/temp/t32.cmm --ref=%TCC_CANTATA_HOME%/ExtraFiles/T_TriCore_greenhills_ifx_comp_201815_5fp_cxtri_c++11/Target/t32.ref --cfg={cfgFile} --elf='
ctrGenCmd = '%TCC_CANTATA_HOME%/tools/get_cov_report_ASIL_D.exe'
for script in testScriptList:
    cmd = cmd + '%MAKE_EXE% ' + script + '\n'
for script in testScriptList:
    cmd = cmd + targetCmd + script + '.elf' + '\n'
for script in testScriptList:
    cmd = cmd + ctrGenCmd + ' ' + script + ' ' + script + '.cov' + '\n'

try:
    out, err = process.communicate(input=cmd)
    logger.info(out)
except:
    logger.error(err)
    logger.info("Failed to make testscript..........")
    sys.exit(-1)
