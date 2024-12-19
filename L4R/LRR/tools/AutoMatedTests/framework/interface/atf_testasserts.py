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
#  Department: CC-DA/EDB7
#=============================================================================
# @file  atf_testasserts.py
#=============================================================================

import atf_toolbox as toolbox

    
def TEST_EQ(logger, testCaseNumber, testNumber, value, expectedValue, testString):
    numberFailedTests = 0

    toolbox.logInfoTestRun(logger, testCaseNumber, testNumber)

    if value == expectedValue:
        toolbox.logInfoTestPassed(logger, testCaseNumber, testNumber)
    else:
        toolbox.logInfoTestFailedEq(logger, testCaseNumber, testNumber, value, expectedValue, testString)
        numberFailedTests += 1                
        
    return numberFailedTests

def TEST_NOT_EQ(logger, testCaseNumber, testNumber, firstValue, secondValue, testString):
    numberFailedTests = 0

    toolbox.logInfoTestRun(logger, testCaseNumber, testNumber)

    if firstValue != secondValue:
        toolbox.logInfoTestPassed(logger, testCaseNumber, testNumber)
    else:
        toolbox.logInfoTestFailedNotEq(logger, testCaseNumber, testNumber, firstValue, secondValue, testString)
        numberFailedTests += 1                
        
    return numberFailedTests

def TEST_GE(logger, testCaseNumber, testNumber, value, expectedValue, testString):
    numberFailedTests = 0

    toolbox.logInfoTestRun(logger, testCaseNumber, testNumber)

    if value >= expectedValue:
        toolbox.logInfoTestPassed(logger, testCaseNumber, testNumber)
    else:
        toolbox.logInfoTestFailedGe(logger, testCaseNumber, testNumber, value, expectedValue, testString)
        numberFailedTests += 1                
        
    return numberFailedTests

def TEST_GT(logger, testCaseNumber, testNumber, value, expectedValue, testString):
    numberFailedTests = 0

    toolbox.logInfoTestRun(logger, testCaseNumber, testNumber)

    if value > expectedValue:
        toolbox.logInfoTestPassed(logger, testCaseNumber, testNumber)
    else:
        toolbox.logInfoTestFailedGt(logger, testCaseNumber, testNumber, value, expectedValue, testString)
        numberFailedTests += 1                
        
    return numberFailedTests    

def TEST_LE(logger, testCaseNumber, testNumber, value, expectedValue, testString):
    numberFailedTests = 0

    toolbox.logInfoTestRun(logger, testCaseNumber, testNumber)

    if value <= expectedValue:
        toolbox.logInfoTestPassed(logger, testCaseNumber, testNumber)
    else:
        toolbox.logInfoTestFailedLe(logger, testCaseNumber, testNumber, value, expectedValue, testString)
        numberFailedTests += 1                
        
    return numberFailedTests

def TEST_CONTAINS(logger, testCaseNumber, testNumber, value, expectedValueList, testString):
    expectedValueFound = False

    toolbox.logInfoTestRun(logger, testCaseNumber, testNumber)
    
    for valueIter in expectedValueList:
        if valueIter == value:
            toolbox.logInfoTestPassed(logger, testCaseNumber, testNumber)
            expectedValueFound = True
            break
        
    if expectedValueFound:
        return 0
    else:
        toolbox.logInfoTestFailedContains(logger, testCaseNumber, testNumber, value, expectedValueList, testString)
        return 1         
  