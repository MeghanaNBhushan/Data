# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 00:05:38 2020

@author: YAH3KOR
"""

import argparse
parser = argparse.ArgumentParser(description="Script to run automated cantata tests on host")
parser.add_argument("-c", "--cantataBuildOption",
                        help='Option to be passed to the cantata build', nargs='?', const='FR5CU_DENN1_CEN_N_XX_2_uC2')
parser.add_argument("-v", "--variant",
                        help='Variant built', nargs='?', const='Radar_FR5CU_DENN1_CEN_N_XX_2_uC2')
parser.add_argument("-bt", "--buildType",
                        help='partial change based build or full build', nargs='?', const='full')

args = parser.parse_args()
cantataBuildOption = str(args.cantataBuildOption)
variant = str(args.variant)
buildType = str(args.buildType)

import logging
logger = logging.getLogger("AutomatedCantataTests")
logger.setLevel(logging.DEBUG)
    
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.DEBUG)
    
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_console_handler.setFormatter(log_format)
logger.addHandler(logger_console_handler)  

import os

archive = os.path.abspath('../../../generatedFiles/SWQualityReports/Cantata')

from pathlib import Path
import sys
import re

testScriptPathList = []
componentPathList = []
testScriptList = []

logger.info("Set environment to search ..........")
setCmd = 'set_env.bat ' + cantataBuildOption +  '\n'

import subprocess
try:
    setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
except:
    logger.error("Failed to open a cmd to run commands")
    sys.exit(-1)
    
try:
    setOut, setErr = setProcess.communicate(input=setCmd)
    logger.info(setOut)
except:
    logger.error(setErr)
    logger.info("Failed to set environment to search scripts..........")
    sys.exit(-1)

logger.info("Searching directory for test scripts ............")
path1 = Path("../../component/")

for file in path1.glob('**/comptest_*.c'):# ** in a path means any number of sub-directories in the path to match regex

    if re.search("( |;)"+file.stem+"( |;|\n)", setOut):
        logger.info("Found : " + file.name)
        testScriptPathList.append(file)
        componentPathList.append(file.parent)
        testScriptList.append(file.stem)

for file in path1.glob('**/comptest_*.cpp'): # ** in a path means any number of sub-directories in the path to match regex

    if re.search("( |;)"+file.stem+"( |;|\n)", setOut):
        logger.info("Found : " + file.name)
        testScriptPathList.append(file)
        componentPathList.append(file.parent)
        testScriptList.append(file.stem)

for file in path1.glob('**/test_*.c'): # ** in a path means any number of sub-directories in the path to match regex

    if re.search("( |;)"+file.stem+"( |;|\n)", setOut):

        logger.info("Found : " + file.name)
        testScriptPathList.append(file)
        componentPathList.append(file.parent.parent)
        testScriptList.append(file.stem)

for file in path1.glob('**/test_*.cpp'): # ** in a path means any number of sub-directories in the path to match regex

    if re.search("( |;)"+file.stem+"( |;|\n)", setOut):
        logger.info("Found : " + file.name)
        testScriptPathList.append(file)
        componentPathList.append(file.parent.parent)
        testScriptList.append(file.stem)


if len(testScriptPathList) == 0:
    if not os.path.isdir(os.path.abspath('../../../generatedFiles/SWQualityReports')):
        os.mkdir(os.path.abspath('../../../generatedFiles/SWQualityReports'))
        os.mkdir(archive)
    logger.info("No Cantata test scripts found for variant!")
    sys.exit(1)

if buildType == 'partial' :

    logger.info("Executing Partial build on only changed files !")

    componentNameList = []
    for componentPath in componentPathList:
        componentNameList.append(re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1))
    componentNameList = set(componentNameList)
    changedFiles = open('../../../changed_file_list.txt', 'r')
     
    changedfilePaths = changedFiles.readlines()
    
    componentsToBuild = []
    
    for componentName in componentNameList : 
        for changedfilePath in changedfilePaths :
            if componentName in str(changedfilePath):
                componentsToBuild.append(componentName)
    
    componentsToBuild = set(componentsToBuild)
    logger.info("Component to build : " + str(componentsToBuild))

    newTestScriptList = []
    newComponentPathList = []
    newTestScriptPathList = []
    
    for (component,componentPath, scriptPath) in zip(testScriptList, componentPathList, testScriptPathList):
        for componentToBuild in componentsToBuild:
            if componentToBuild in str(componentPath):
                newTestScriptList.append(component)
                newComponentPathList.append(componentPath)
                newTestScriptPathList.append(scriptPath)
                logger.info("Script to build : " + component)
    
    testScriptList = newTestScriptList
    componentPathList = newComponentPathList
    testScriptPathList = newTestScriptPathList

    if len(testScriptPathList) == 0:
        if not os.path.isdir(os.path.abspath('../../../generatedFiles/SWQualityReports')):
            os.mkdir(os.path.abspath('../../../generatedFiles/SWQualityReports'))
            os.mkdir(archive)
        logger.info("No changes in files related to cantata build. Skipping cantata build !")
        sys.exit(1)
     
try:
    process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
except:
    logger.error("Failed to open a cmd to run commands")
    sys.exit(-1)

logger.debug("---------------------------------------------------------------------------------")
makeLog_logger = logging.FileHandler(variant+"_cantataMakeLog.txt",mode="w")
makeLog_logger.setLevel(logging.INFO)
logger.addHandler(makeLog_logger)

import shutil

makeLog_path = os.path.abspath('./'+variant+"_cantataMakeLog.txt")
cmd = 'set_env.bat ' + cantataBuildOption +  '\n' + 'cd '+ os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant)) + '\n'

for script in testScriptList:
    cmd = cmd + 'mingw32-make ' + script + '\n'
for script in testScriptList:
    cmd = cmd + script + '.exe' + '\n'
try:
    out, err = process.communicate(input=cmd)
    logger.info(out)
except:
    logger.error(err)
    logger.info("Failed to make testscript..........")
    if not os.path.isdir(archive):
        os.mkdir(archive)
    logger.debug("Copying make log to " +  archive)
    shutil.copy(makeLog_path, archive)
    sys.exit(-1)


import pandas as pd
import numpy as np

failRegex1 = r'\s+failed\n'
failRegex2 = r'FAIL\s+'
failRegex3 = r'\s+No rule to make target\s+'
C0 = {}
C1 = {}

threshC0 = {'MntPosMgmt': 0.6,
 'rbSysEvM': 0.6,
 'diag': 0.6,
 'LocDataIF': 0.6,
 'sdm': 0.6,
 'measurement_program': 0.6,
 'EgoVehDataIF': 0.6, 
 'outputhandler':0.6, 
 'inputhandler':0.6,
 'net_x':0.6
 }

threshC1 = {'MntPosMgmt': 0.5,
 'rbSysEvM': 0.5,
 'diag': 0.5,
 'LocDataIF': 0.5,
 'sdm': 0.5,
 'measurement_program': 0.5,
 'EgoVehDataIF': 0.5,
 'outputhandler': 0.5, 
 'inputhandler' : 0.5,
 'net_x':0.5 }

envCmd = 'set LSFORCEHOST=FE0VMC0829.de.bosch.com'+'\n'    
envCmd += 'set TCC_CANTATA_HOME=C:\TCC\Tools\cantata\9.5.0_WIN64' + '\n'
envCmd += 'set TCC_MINGW64_HOME=C:\TCC\Tools\mingw64\5.4.0_WIN64' + '\n'
envCmd += 'set QNX_HOST=' + '\n'
envCmd += 'set QNX_TARGET=' + '\n'
envCmd += 'set PATH=C:/TCC/Tools/mingw64/5.4.0_WIN64/bin;C:/TCC/Tools/cmake/3.17.1_WIN64/bin;c:/TCC/Tools/doxygen/1.8.12_WIN64/bin;c:/TCC/Tools/cantata/9.5.0_WIN64/bin;%path%'+'\n'
envCmd += 'set ARMLMD_LICENSE_FILE=8224@rb-lic-armlmd-ccda-video.de.bosch.com'+'\n'
envCmd += 'set RLM_LICENSE=5062@rb-lic-lauterbach-cc.de.bosch.com'+'\n'
envCmd += 'c:\TCC\Tools\mingw64\5.4.0_WIN64/bin/mingw32-make.exe'+'\n'
cantppc = 'C:\TCC\Tools\cantata\9.5.0_WIN64\cantppc.exe'

ExportColumns = ['ctr_source_file_name','FilePath','C0 Coverage','C1 Coverage','MCDC Coverage','Entry Coverage', \
                 'calculated_file_statement_executed', 'calculated_file_statement_unexecuted',  \
                 'calculated_file_decision_executed', 'calculated_file_decision_unexecuted' , \
                 'calculated_file_boolean_effective', 'calculated_file_boolean_not_effective', \
                 'calculated_file_entrypoint_executed', 'calculated_file_entrypoint_unexecuted', \
                 'Team','Components', 'no_data_confirmed']

ExportIndex = ['ctr_source_file_name']
ExportDF = pd.DataFrame(columns = ExportColumns, index = ExportIndex)
logger.debug("Columns : "+ExportDF.columns)
logger.debug("Index : "+ExportDF.index)
knownSMFComponents = ['sdm', 'rbSysEvM',  'diag', 'outputhandler', 'inputhandler']
knownLGCComponents = ['measurement_program', 'MntPosMgmt', 'LocDataIF', 'EgoVehDataIF', 'net_x']

if re.search(failRegex3, err) != None : 
    logger.error(err)
    logger.info("No rule to make target error . Check naming conventions, folder structure of unit tests, cop file, etc")
    if not os.path.isdir(archive):
        os.mkdir(archive)
    logger.debug("Copying make log to " +  archive)
    shutil.copy(makeLog_path, archive)
    sys.exit(-1)   

elif re.search(failRegex1, out) != None :
    logger.error(err)
    logger.info("Failed to make testscript..........")
    if not os.path.isdir(archive):
        os.mkdir(archive)
    logger.debug("Copying make log to " +  archive)
    shutil.copy(makeLog_path, archive)
    sys.exit(-1)

elif re.search(failRegex2, out) == None :
    logger.info("All testcases passed")
    logger.info("Creating Test Reports.............")
    componentPathList = [re.search('(^.*\\\\test).*$', str(x)).group(1) for x in componentPathList]

    for (component,componentPath, scriptPath) in zip(testScriptList, componentPathList, testScriptPathList):
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        dst = os.path.join(str(componentPath) +'/'+ componentName)
        logger.debug("Creating cantata workspace for script"+component+"........")
        src1 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.cov'))
        src2 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.ctr'))
        src3 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.ctg'))
        src4 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.exe'))
        logger.debug("Creating directory : "+dst)
        if not os.path.isdir(dst):
            os.mkdir(dst)
        logger.debug("Copying cov, ctr, ctg and exe to" + dst)
        try:
            shutil.copy(src1, dst)
            shutil.copy(src2, dst)
            shutil.copy(src3, dst)
            shutil.copy(src4, dst)
        except:
            logger.error("Copying cov, ctr, ctg failed. Check if the name of cov, ctr, ctg is same as test_script")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

    for componentPath in set(componentPathList):
        logger.debug("Setting Cantata environment variables and execute test report generation command: ")
        ws = os.path.join(str(componentPath) +f"/ws")
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        dst = os.path.join(str(componentPath) +'/'+ componentName)
        try:
            reportProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
        except:
            logger.error("Failed to open a cmd to generate reports")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

        reportCmd = envCmd + cantppc +f" -data {ws} -application com.ipl.products.eclipse.cantpp.cdt.TestReportGenerator -noSplash {dst} HTML_DETAILED_REPORT" + '\n'

        try:
            out, err = reportProcess.communicate(input=reportCmd)
            logger.info(out)

            logger.info("Collecting C0 and C1 coverage per component........")
            df = pd.read_html(os.path.join(dst + '/' +'Cantata Output/test_report.html'))
            sumDF = df[1]
            covDF = df[2]
            sumDF.set_index(0, inplace = True)
            sumDF.rename({1:'value'}, axis = 1, inplace = True)
            covDF.set_index('Coverage Type', inplace = True)
            covDF['Coverage Achieved'] = covDF['Coverage Achieved'].str.strip('%').astype(int)
            C0[componentName] = (int(sumDF.loc['Test cases passed','value'])*covDF.loc['Statement','Coverage Achieved'])/(int(sumDF.loc['Total number of test cases','value'])*100)
            C1[componentName] = (int(sumDF.loc['Test cases passed','value'])*covDF.loc['Decision','Coverage Achieved'])/(int(sumDF.loc['Total number of test cases','value'])*100)

            logger.info("Archiving reports.............")
            archivePath = os.path.abspath(os.path.join('../../../generatedFiles', 'SWQualityReports/Cantata'+'/'+'Host_'+ variant+'/'+componentName))
            logger.info(f"Copying {dst} to {archivePath}")
            shutil.copytree(dst, archivePath)

        except:
            logger.error(err)
            logger.info("Cantata test report generator and copying failed ..........")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

    for (script, scriptPath) in zip(testScriptList, testScriptPathList):
        path, file = os.path.split(scriptPath)
        dst = os.path.join(str(path) +'/'+ script)
        logger.debug("Reading ctr metrics for splunk upload for script : "+script+"........")
        src = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.ctr'))
        file_obj = open(src)
        ExportDF.loc[script, :] = 0
        file = list(file_obj)
        coverage_type = None
        for line in file:
            if 'entry point coverage details' in line : 
                coverage_type = 'entry'
            elif 'statement coverage details' in line : 
                coverage_type = 'stmt'
            elif 'decision coverage details' in line : 
                coverage_type = 'decision'
            elif 'boolean operand effectiveness coverage details' in line : 
                coverage_type = 'bool'        
            else :
                if coverage_type == 'entry':
                    if re.search('\s+executed\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_entrypoint_executed'] += int(re.search('(\d+)',re.search('\s+executed\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+un-executed\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_entrypoint_unexecuted'] += int(re.search('(\d+)',re.search('\s+un-executed\s+(\d+)', line).group(0)).group(0))
                elif coverage_type == 'stmt':
                    if re.search('\s+executed\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_statement_executed'] += int(re.search('(\d+)',re.search('\s+executed\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+un-executed\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_statement_unexecuted'] += int(re.search('(\d+)',re.search('\s+un-executed\s+(\d+)', line).group(0)).group(0))
                elif coverage_type == 'decision':
                    if re.search('\s+executed\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_decision_executed'] += int(re.search('(\d+)',re.search('\s+executed\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+un-executed\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_decision_unexecuted'] += int(re.search('(\d+)',re.search('\s+un-executed\s+(\d+)', line).group(0)).group(0))
                elif coverage_type == 'bool':
                    if re.search('\s+not effective\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_boolean_not_effective'] += int(re.search('(\d+)',re.search('\s+not effective\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+effective\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_boolean_effective'] += int(re.search('(\d+)',re.search('\s+effective\s+(\d+)', line).group(0)).group(0))
        logger.debug("Ctr metrics for splunk upload for script : "+script+" read successfully")

    for (script, scriptPath) in zip(testScriptList, testScriptPathList):
        path, file = os.path.split(scriptPath)
        dst = os.path.join(str(path) +'/'+ script)
        logger.debug("Creating cantata workspace for script"+script+"........")
        src1 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.cov'))
        src2 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.ctr'))
        src3 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.ctg'))
        src4 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.exe'))
        logger.debug("Creating directory : "+dst)
        if not os.path.isdir(dst):
            os.mkdir(dst)
        logger.debug("Copying cov, ctr, ctg and exe to" + dst)
        try:
            shutil.copy(src1, dst)
            shutil.copy(src2, dst)
            shutil.copy(src3, dst)
            shutil.copy(src4, dst)
        except:
            logger.error("Copying cov, ctr, ctg failed. Check if the name of cov, ctr, ctg is same as test_script")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)
            
    for (script, scriptPath, componentPath) in zip(testScriptList, testScriptPathList, componentPathList):
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        logger.debug("Setting Cantata environment variables and execute test report generation command: ")
        path, file = os.path.split(scriptPath)
        ws = os.path.join(str(path) +'/' + f'/'+script+'_ws')
        dst = os.path.join(str(path) +'/'+ script)
        try:
            reportProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
        except:
            logger.error("Failed to open a cmd to generate reports")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

        reportCmd = envCmd + cantppc + f" -data {ws} -application com.ipl.products.eclipse.cantpp.cdt.TestReportGenerator -noSplash {dst} HTML_DETAILED_REPORT" + '\n'

        try:
            out, err = reportProcess.communicate(input=reportCmd)
            logger.info(out)

        except:
            logger.error(err)
            logger.info("Cantata test report generator failed ..........")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)
            
        try:
        
            logger.info("Collecting C0 and C1 coverage per component........")
            df = pd.read_html(os.path.join(dst + '/' +'Cantata Output/test_report.html'))
            sumDF = df[1]
            covDF = df[2]
            sumDF.set_index(0, inplace = True)
            sumDF.rename({1:'value'}, axis = 1, inplace = True)
            covDF.set_index('Coverage Type', inplace = True)
            covDF['Coverage Achieved'] = covDF['Coverage Achieved'].str.strip('%').astype(int)

            ExportDF.loc[script, 'ctr_source_file_name'] = script
            ExportDF.loc[script, 'FilePath'] = os.path.abspath(scriptPath)
            ExportDF.loc[script,'C0 Coverage'] = covDF.loc['Statement','Coverage Achieved']
            ExportDF.loc[script,'C1 Coverage'] = covDF.loc['Decision','Coverage Achieved']
            ExportDF.loc[script,'MCDC Coverage'] = covDF.loc['Boolean Operand Effectiveness (Masking)','Coverage Achieved'] 
            ExportDF.loc[script,'Entry Coverage'] = covDF.loc['Entry Point','Coverage Achieved']
            ExportDF.loc[script,'Components'] = componentName
        
        except KeyError : 
            logger.error(f" Testscript {script} is not generating coverage info. Either it is not written or not instrumented correctly. Placing 0 for values")
            ExportDF.loc[script, 'ctr_source_file_name'] = script
            ExportDF.loc[script, 'FilePath'] = os.path.abspath(scriptPath)
            ExportDF.loc[script,'C0 Coverage'] = 0
            ExportDF.loc[script,'C1 Coverage'] = 0
            ExportDF.loc[script,'MCDC Coverage'] = 0 
            ExportDF.loc[script,'Entry Coverage'] = 0
            ExportDF.loc[script,'Components'] = componentName
        except:
            logger.error("Cantata coverage extraction failed")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

        try : 
            if componentName in knownSMFComponents :
                ExportDF.loc[script,'Team'] = 'SMF'
            elif componentName in knownLGCComponents :
                ExportDF.loc[script,'Team'] = 'LGC'
            else : 
                raise ValueError(f'Unknown component : {componentName}. Please Manually add it to known components list')            
        except ValueError as compErr:
            logger.error(compErr)
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)
            
        except:
            logger.error("Team assignment to script failed")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)
    if buildType != 'partial' :

        logger.info("Converting data to a excel sheet.............")
        ExportDF.to_excel(os.path.abspath(os.path.join('../../../generatedFiles', 'SWQualityReports/Cantata'+'/'+'Host_'+ variant+'/'+'Cantata.xlsx')), index = False) 
        logger.info("Excel report generation is successful")
        
    dst = os.path.abspath(os.path.join('../../../generatedFiles', 'SWQualityReports/Cantata'+'/'+'Host_'+ variant))
    shutil.make_archive( dst,'zip', dst)
    logger.info("Archiving reports successful")

    thresholdBroken = False
    for componentPath in set(componentPathList):
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        if C0[componentName] < threshC0[componentName] or C1[componentName] < threshC1[componentName] :
            thresholdBroken = True

    if thresholdBroken == True : 
        if not os.path.isdir(archive):
            os.mkdir(archive)
        logger.debug("Copying make log to " +  archive)
        shutil.copy(makeLog_path, archive)
        sys.exit(-1)
    else : 
        if not os.path.isdir(archive):
            os.mkdir(archive)
        logger.debug("Copying make log to " +  archive)
        shutil.copy(makeLog_path, archive)
        sys.exit(0)

else:

    logger.info("Some or all testcases failed")
    logger.info("Creating Test Reports.............")
    componentPathList = [re.search('(^.*\\\\test).*$', str(x)).group(1) for x in componentPathList]

    for (component,componentPath, scriptPath) in zip(testScriptList, componentPathList, testScriptPathList):
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        dst = os.path.join(str(componentPath) +'/'+ componentName)
        logger.debug("Creating cantata workspace for script"+component+"........")
        src1 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.cov'))
        src2 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.ctr'))
        src3 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.ctg'))
        src4 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+component+'.exe'))
        logger.debug("Creating directory : "+dst)
        if not os.path.isdir(dst):
            os.mkdir(dst)
        logger.debug("Copying cov, ctr, ctg and exe to" + dst)
        try:
            shutil.copy(src1, dst)
            shutil.copy(src2, dst)
            shutil.copy(src3, dst)
            shutil.copy(src4, dst)
        except:
            logger.error("Copying cov, ctr, ctg failed. Check if the name of cov, ctr, ctg is same as test_script")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

    for componentPath in set(componentPathList):
        logger.debug("Setting Cantata environment variables and execute test report generation command: ")
        ws = os.path.join(str(componentPath) +f"/ws")
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        dst = os.path.join(str(componentPath) +'/'+ componentName)
        try:
            reportProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
        except:
            logger.error("Failed to open a cmd to generate reports")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

        reportCmd = envCmd + cantppc + f" -data {ws} -application com.ipl.products.eclipse.cantpp.cdt.TestReportGenerator -noSplash {dst} HTML_DETAILED_REPORT" + '\n'

        try:
            out, err = reportProcess.communicate(input=reportCmd)
            logger.info(out)

            logger.info("Collecting C0 and C1 coverage per component........")
            df = pd.read_html(os.path.join(dst + '/' +'Cantata Output/test_report.html'))
            sumDF = df[1]
            covDF = df[2]
            sumDF.set_index(0, inplace = True)
            sumDF.rename({1:'value'}, axis = 1, inplace = True)
            covDF.set_index('Coverage Type', inplace = True)
            covDF['Coverage Achieved'] = covDF['Coverage Achieved'].str.strip('%').astype(int)
            C0[componentName] = (int(sumDF.loc['Test cases passed','value'])*covDF.loc['Statement','Coverage Achieved'])/(int(sumDF.loc['Total number of test cases','value'])*100)
            C1[componentName] = (int(sumDF.loc['Test cases passed','value'])*covDF.loc['Decision','Coverage Achieved'])/(int(sumDF.loc['Total number of test cases','value'])*100)

            logger.info("Archiving reports.............")
            archivePath = os.path.abspath(os.path.join('../../../generatedFiles', 'SWQualityReports/Cantata'+'/'+'Host_'+ variant+'/'+componentName))
            logger.info(f"Copying {dst} to {archivePath}")
            shutil.copytree(dst, archivePath)

        except:
            logger.error(err)
            logger.info("Cantata test report generator and copying failed ..........")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

    for (script, scriptPath) in zip(testScriptList, testScriptPathList):
        path, file = os.path.split(scriptPath)
        dst = os.path.join(str(path) +'/'+ script)
        logger.debug("Reading ctr metrics for splunk upload for script : "+script+"........")
        src = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.ctr'))
        file_obj = open(src)
        ExportDF.loc[script, :] = 0
        file = list(file_obj)
        coverage_type = None
        for line in file:
            if 'entry point coverage details' in line : 
                coverage_type = 'entry'
            elif 'statement coverage details' in line : 
                coverage_type = 'stmt'
            elif 'decision coverage details' in line : 
                coverage_type = 'decision'
            elif 'boolean operand effectiveness coverage details' in line : 
                coverage_type = 'bool'        
            else :
                if coverage_type == 'entry':
                    if re.search('\s+executed\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_entrypoint_executed'] += int(re.search('(\d+)',re.search('\s+executed\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+un-executed\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_entrypoint_unexecuted'] += int(re.search('(\d+)',re.search('\s+un-executed\s+(\d+)', line).group(0)).group(0))
                elif coverage_type == 'stmt':
                    if re.search('\s+executed\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_statement_executed'] += int(re.search('(\d+)',re.search('\s+executed\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+un-executed\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_statement_unexecuted'] += int(re.search('(\d+)',re.search('\s+un-executed\s+(\d+)', line).group(0)).group(0))
                elif coverage_type == 'decision':
                    if re.search('\s+executed\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_decision_executed'] += int(re.search('(\d+)',re.search('\s+executed\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+un-executed\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_decision_unexecuted'] += int(re.search('(\d+)',re.search('\s+un-executed\s+(\d+)', line).group(0)).group(0))
                elif coverage_type == 'bool':
                    if re.search('\s+not effective\s+(\d+)', line) != None: 
                        ExportDF.loc[script,'calculated_file_boolean_not_effective'] += int(re.search('(\d+)',re.search('\s+not effective\s+(\d+)', line).group(0)).group(0))
                    elif re.search('\s+effective\s+(\d+)', line) != None:
                        ExportDF.loc[script,'calculated_file_boolean_effective'] += int(re.search('(\d+)',re.search('\s+effective\s+(\d+)', line).group(0)).group(0))

        logger.debug("Ctr metrics for splunk upload for script : "+script+" read successfully")

    for (script, scriptPath) in zip(testScriptList, testScriptPathList):
        path, file = os.path.split(scriptPath)
        dst = os.path.join(str(path) +'/'+ script)
        logger.debug("Creating cantata workspace for script"+script+"........")
        src1 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.cov'))
        src2 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.ctr'))
        src3 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.ctg'))
        src4 = os.path.abspath(os.path.join('../../../generatedFiles', 'CANTATA_host_'+ variant+'/'+script+'.exe'))
        logger.debug("Creating directory : "+dst)
        if not os.path.isdir(dst):
            os.mkdir(dst)
        logger.debug("Copying cov, ctr, ctg and exe to" + dst)
        try:
            shutil.copy(src1, dst)
            shutil.copy(src2, dst)
            shutil.copy(src3, dst)
            shutil.copy(src4, dst)
        except:
            logger.error("Copying cov, ctr, ctg failed. Check if the name of cov, ctr, ctg is same as test_script")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

    for (script, scriptPath, componentPath) in zip(testScriptList, testScriptPathList, componentPathList):
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        logger.debug("Setting Cantata environment variables and execute test report generation command: ")
        path, file = os.path.split(scriptPath)
        ws = os.path.join(str(path) +'/' + f'/'+script+'_ws')
        dst = os.path.join(str(path) +'/'+ script)
        try:
            reportProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
        except:
            logger.error("Failed to open a cmd to generate reports")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

        reportCmd = envCmd + cantppc +f" -data {ws} -application com.ipl.products.eclipse.cantpp.cdt.TestReportGenerator -noSplash {dst} HTML_DETAILED_REPORT" + '\n'

        try:
            out, err = reportProcess.communicate(input=reportCmd)
            logger.info(out)

        except:
            logger.error(err)
            logger.info("Cantata test report generator failed ..........")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)
            
        try:
        
            logger.info("Collecting C0 and C1 coverage per component........")
            df = pd.read_html(os.path.join(dst + '/' +'Cantata Output/test_report.html'))
            covDF = df[2]
            covDF.set_index('Coverage Type', inplace = True)
            covDF['Coverage Achieved'] = covDF['Coverage Achieved'].str.strip('%').astype(int)
            ExportDF.loc[script, 'ctr_source_file_name'] = script
            ExportDF.loc[script, 'FilePath'] = os.path.abspath(scriptPath)
            ExportDF.loc[script,'C0 Coverage'] = covDF.loc['Statement','Coverage Achieved']
            ExportDF.loc[script,'C1 Coverage'] = covDF.loc['Decision','Coverage Achieved']
            ExportDF.loc[script,'MCDC Coverage'] = covDF.loc['Boolean Operand Effectiveness (Masking)','Coverage Achieved']
            ExportDF.loc[script,'Entry Coverage'] = covDF.loc['Entry Point','Coverage Achieved']
            ExportDF.loc[script,'Components'] = componentName
        
        except KeyError : 
            logger.error(f" Testscript {script} is not generating coverage info. Either it is not written or not instrumented correctly. Placing 0 for values")
            ExportDF.loc[script, 'ctr_source_file_name'] = script
            ExportDF.loc[script, 'FilePath'] = os.path.abspath(scriptPath)
            ExportDF.loc[script,'C0 Coverage'] = 0
            ExportDF.loc[script,'C1 Coverage'] = 0
            ExportDF.loc[script,'MCDC Coverage'] = 0 
            ExportDF.loc[script,'Entry Coverage'] = 0
            ExportDF.loc[script,'Components'] = componentName
        except:
            logger.error("Cantata coverage extraction failed")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)

        try : 
            if componentName in knownSMFComponents :
                ExportDF.loc[script,'Team'] = 'SMF'
            elif componentName in knownLGCComponents :
                ExportDF.loc[script,'Team'] = 'LGC'
            else : 
                raise ValueError(f'Unknown component : {componentName}. Please Manually add it to known components list ')            
        except ValueError as compErr:
            logger.error(compErr)
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)
            
        except:
            logger.error("Team assignment to script failed")
            if not os.path.isdir(archive):
                os.mkdir(archive)
            logger.debug("Copying make log to " +  archive)
            shutil.copy(makeLog_path, archive)
            sys.exit(-1)
    
    if buildType != 'partial' :

        logger.info("Converting data to a excel sheet.............")
        ExportDF.to_excel(os.path.abspath(os.path.join('../../../generatedFiles', 'SWQualityReports/Cantata'+'/'+'Host_'+ variant+'/'+'Cantata.xlsx')), index = False) 
        logger.info("Excel report generation is successful")

    dst = os.path.abspath(os.path.join('../../../generatedFiles', 'SWQualityReports/Cantata'+'/'+'Host_'+ variant))
    shutil.make_archive( dst,'zip', dst)
    logger.info("Archiving reports successful")

    thresholdBroken = False
    for componentPath in set(componentPathList):
        componentName = re.search('^.*component\\\\(.*)\\\\test.*$', str(componentPath)).group(1)
        if C0[componentName] < threshC0[componentName] or C1[componentName] < threshC1[componentName] :
            thresholdBroken = True
            logger.error('ERROR : One of the more of the components have decreased in one of the coverage metrics')
            logger.error(f'ERROR : For component {componentName} Actual C0 coverage : {C0[componentName]} Expected C0 coverage : {threshC0[componentName]}')
            logger.error(f'ERROR : For component {componentName} Actual C1 coverage : {C1[componentName]} Expected C1 coverage : {threshC1[componentName]}')

    if thresholdBroken == True : 
        if not os.path.isdir(archive):
            os.mkdir(archive)
        logger.debug("Copying make log to " +  archive)
        shutil.copy(makeLog_path, archive)
        sys.exit(-1)
    else : 
        if not os.path.isdir(archive):
            os.mkdir(archive)
        logger.debug("Copying make log to " +  archive)
        shutil.copy(makeLog_path, archive)
    logger.info("Some or all testcases failed")
    sys.exit(-1)