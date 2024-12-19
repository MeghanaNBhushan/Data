#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
# @copyright (c) 2021 - 2022 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
#=============================================================================
#  P R O J E C T   I N F O R M A T I O N
#-----------------------------------------------------------------------------
#     Projectname: L4 Radar
#=============================================================================
#  I N I T I A L   A U T H O R   I D E N T I T Y
#-----------------------------------------------------------------------------
#        Name: BAD2LR
#  Department: XC-AD/PJ-AS12
#=============================================================================
# @file  atf_toolbox.py
#=============================================================================



def checkFailedTests(numberFailedTests):
    if numberFailedTests == 0:
        return 0
    else:
        return 1     

def removeColons(a):
    return a.replace(':','')


def logInfoTestStart(logger, testcaseName, component):
    logger.info(f"[==========] Running tests of {testcaseName} in component {component}")
    
def logInfoTestEnd(logger, testNumber, passedTests, failedTests, testcaseName, component):
    logger.info(f"[==========] Run {testNumber} tests of {testcaseName} in component {component}")
    logger.info(f"[  PASSED  ] {passedTests} tests")    
    if failedTests > 0:
        logger.info(f"[  FAILED  ] {failedTests} tests")
    logger.info("") # newline 

def logInfoTestRun(logger, testcaseNumber, testNumber):
    logger.info(f"[ RUN      ] Test {testcaseNumber}-{testNumber}")

def logInfoTestPassed(logger, testcaseNumber, testNumber):
    logger.info(f"[       OK ] Test {testcaseNumber}-{testNumber}")

def logInfoTestFailedEq(logger, testcaseNumber, testNumber, value, expectedValue, testString):
    logger.info(f"{testString}, actual: {value} != expected value: {expectedValue}")
    logger.info(f"[   FAILED ] Test {testcaseNumber}-{testNumber}")

def logInfoTestFailedNotEq(logger, testcaseNumber, testNumber, firstValue, secondValue, testString):
    logger.info(f"{testString}, first value: {firstValue} == second value: {secondValue}")
    logger.info(f"[   FAILED ] Test {testcaseNumber}-{testNumber}")

def logInfoTestFailedGe(logger, testcaseNumber, testNumber, value, expectedValue, testString):
    logger.info(f"{testString}, actual value: {value} NOT >= expected value: {expectedValue}")
    logger.info(f"[   FAILED ] Test {testcaseNumber}-{testNumber}")
    
def logInfoTestFailedGt(logger, testcaseNumber, testNumber, value, expectedValue, testString):
    logger.info(f"{testString}, actual value: {value} NOT > expected value: {expectedValue}")
    logger.info(f"[   FAILED ] Test {testcaseNumber}-{testNumber}")    

def logInfoTestFailedLe(logger, testcaseNumber, testNumber, value, expectedValue, testString):
    logger.info(f"{testString}, actual value: {value} NOT <= expected value: {expectedValue}")
    logger.info(f"[   FAILED ] Test {testcaseNumber}-{testNumber}")

def logInfoTestFailedContains(logger, testcaseNumber, testNumber, value, expectedValueList, testString):
    logger.info(f"{testString}, actual value: {value} is NOT contained in list")
    logger.info(f"[   FAILED ] Test {testcaseNumber}-{testNumber}")
