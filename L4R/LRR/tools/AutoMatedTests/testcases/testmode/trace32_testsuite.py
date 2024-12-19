# -*- coding: utf-8 -*-

import sys
import time
import os

sys.path.append(os.path.abspath('../../framework/helper'))
sys.path.append(os.path.abspath('../../framework/scheduling'))
sys.path.append(os.path.abspath('../../framework/interface'))

import atf_testasserts as testasserts
import AD_lauterbach_test_helper as lauterbachTestHelper
import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants

from testbase import CTestCaseResult
from trace32api import ETrace32State
from canoe import EConnectionStatus

class CTestSuiteTrace32(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteTrace32"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, "trace32")
        

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no trace32 test cases on UC1, but still a TestResult has to be returned
        return testsuite.TestSuiteResult(0, 0)

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllTrace32Tests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "trace32"

    def runAllTrace32Tests(self, t32_api):                                                
        numberFailedTests = self.executeFilteredFunction(t32_api)                      
                            
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests) 
  

    def check_lauterbachReset(self, t32api):       
        numberFailedTests = 0
        numberTest = 1                               
    
        t32Uc1Api = self.t32_api[globalConstants.k_atf_hardwareLrrUc1]            
                
        traceStatusUc2 = t32api.get_state()        
        traceStatusUc1 = t32Uc1Api.get_state()        
        connectionStatus = self.canoe_api.getConnectionStatus()
                       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, traceStatusUc2.value, 
                                                 ETrace32State.TARGET_EXECUTION_RUN.value, "Precondition: Lauterbach uC2 is 'running'")                 
        numberTest += 1
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, traceStatusUc1.value, 
                                                 ETrace32State.TARGET_EXECUTION_RUN.value, "Precondition: Lauterbach uC1 is 'running'")                                                                  
        numberTest += 1
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, connectionStatus.value, 
                                                 EConnectionStatus.LINK_UP.value, "Precondition: Link is up")
        
        # try to reset the sensor 10x times
        for i in range(10):  
            # check if after function call the debugger "comes up" -> Debugger state "running"
            lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
                
            # give the sensor some time to reset and sync
            time.sleep(2)                
        
            traceStatusUc2 = t32api.get_state()
            traceStatusUc1 = t32Uc1Api.get_state()                    
            connectionStatus = self.canoe_api.getConnectionStatus()
            
            numberTest += 1
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, traceStatusUc2.value, 
                                                 ETrace32State.TARGET_EXECUTION_RUN.value, "Check Lauterbach uC2 is 'running'")
            numberTest += 1
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, traceStatusUc1.value, 
                                                 ETrace32State.TARGET_EXECUTION_RUN.value, "Check Lauterbach uC1 is 'running'")                                                 
                                               
            numberTest += 1
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, connectionStatus.value, 
                                                 EConnectionStatus.LINK_UP.value, "Check link is up")                        
                            
        return CTestCaseResult(numberTest, numberFailedTests)  
    
    

