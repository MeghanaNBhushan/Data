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
#        Name: YAH3KOR
#  Department: 
#=============================================================================
# @file  testsuite.py
#=============================================================================

import os 
import pandas as pd

from testbase import CTestBase
from testbase import CTestCaseResult
import atf_toolbox as toolbox

k_componentSeparatorSign = ','
k_testFilterSeparatorSign = ';'

class CTestSuite:

    def __init__(self, testsuiteLogger, canoeApi , t32Api, relayApi, hw, globalTestcaseFilter, component):
        self.logger = testsuiteLogger
        self.canoe_api = canoeApi
        self.relay_api = relayApi
        self.t32_api = t32Api
        self.hw = hw
        dir_path = os.path.abspath('testcases')
        self.rqm = pd.read_csv(os.path.join(dir_path, 'RQM.csv'),index_col = 0)
        self.number_of_test = 0
        self.globalTestcaseFilter = globalTestcaseFilter
        self.component = component


    ## @brief Private function for creating a dictionary of all test case functions.
    # 
    def createTestCaseDictionary(self):
        # create dictionary with all callable test cases
        testcaseDict = {}
        # dictionary key: function name, value: callable function
        for functionName in dir(self):
            callFunction = getattr(self, functionName)
                
            if callable(callFunction) and not functionName.startswith("__"):
                if functionName.startswith("swTest_") or functionName.startswith("check_"):
                    testcaseDict[functionName] = callFunction
            elif isinstance(callFunction, CTestBase):
                testcaseDict[functionName] = callFunction
                    
        return testcaseDict 


    ## @brief Private function to retrieve a dictionary based on a input filter.
    #          
    def getFilteredTestCaseDictionary(self, dictFilter, inputDict):        
        filteredTestCaseDict = {}
        
        # iteration over test case dictionary
        for testcaseName, testcaseFunction in inputDict.items():                    
            if k_componentSeparatorSign in dictFilter:
                compList = dictFilter.split(k_componentSeparatorSign)
                for comp in compList:
                    if comp.strip() == self.getComponentName():
                        # own component was found                       
                        filteredTestCaseDict[testcaseName] = testcaseFunction                        
                    else:
                        continue
            elif k_testFilterSeparatorSign in dictFilter:
                testcaseFilterList = dictFilter.split(k_testFilterSeparatorSign)
                for testcaseFiltered in testcaseFilterList:
                    if testcaseFiltered.strip() in testcaseName:
                        # filtered test case was found
                        filteredTestCaseDict[testcaseName] = testcaseFunction
                    else:
                        continue
            else:                                                                
                if dictFilter == '*':
                    # Every function shall be used
                    filteredTestCaseDict[testcaseName] = testcaseFunction
                elif dictFilter in testcaseName:     
                    # simple filter by searching for the substring
                    filteredTestCaseDict[testcaseName] = testcaseFunction
                else:
                    # nothing to do
                    pass
        
        return filteredTestCaseDict
    

    ## @brief Private function to execute all functions of a dictionary. 
    # 
    def executeDictionaryFunction(self, dictionary, t32Api):
        numberFailedTestcases = 0
               
        # iteration over filtered test case dictionary
        for testcaseName, testcaseFunction in dictionary.items():
            toolbox.logInfoTestStart(self.logger, testcaseName, self.component)
            try:             
                if isinstance(testcaseFunction, CTestBase):
                    testcaseResults = testcaseFunction.executeTestCase(t32Api, self.number_of_test)                                        
                    numberFailedTestcases += toolbox.checkFailedTests(testcaseResults.numberFailedTests)                    
                else:                                                
                    testcaseResults = testcaseFunction(t32Api)
                    numberFailedTestcases += toolbox.checkFailedTests(testcaseResults.numberFailedTests)
                
            except Exception as exception:
                # catch exception and mark the test case as failed
                # currently only Trace32 exceptions are caught
                testcaseResults = CTestCaseResult(1, 1) # indicate that something goes wrong with a failed test
                numberFailedTestcases += 1
                # print reason for exception
                self.logger.info(f"{exception}")                
            finally:
                toolbox.logInfoTestEnd(self.logger, testcaseResults.numberTests, testcaseResults.numberPassedTests, 
                                       testcaseResults.numberFailedTests, testcaseName, self.component)
                self.number_of_test += 1
            
        return numberFailedTestcases       
       

    ## @brief Execute function based on global filter
    # 
    def executeFilteredFunction(self, t32Api):
        filteredDict = self.getFilteredTestCaseDictionary(self.globalTestcaseFilter, self.createTestCaseDictionary())
        
        return self.executeDictionaryFunction(filteredDict, t32Api)                                    


    ## @brief Execute function which are preselected by the user, but apply the global filter.
    # 
    def executeFilteredFunctionUser(self, t32Api, userFilter):        
        userDict = self.getFilteredTestCaseDictionary(userFilter, self.createTestCaseDictionary())
        
        # apply global filter on user selected test cases
        userFilteredDict = self.getFilteredTestCaseDictionary(self.globalTestcaseFilter, userDict)
        
        return self.executeDictionaryFunction(userFilteredDict, t32Api)

        
        
class TestSuiteResult:
    def __init__(self, numberTests, numberFailedTests):
        self.numberTests = numberTests
        self.numberFailedTests = numberFailedTests
        
    def __iadd__(self, other):
        return TestSuiteResult(self.numberTests + other.numberTests, self.numberFailedTests + other.numberFailedTests)
        
