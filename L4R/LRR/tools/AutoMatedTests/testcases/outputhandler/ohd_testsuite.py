# -*- coding: utf-8 -*-

import sys
import time
import os

import re

sys.path.append(os.path.abspath('../../framework/scheduling'))
sys.path.append(os.path.abspath('../../framework/interface'))

import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants

import ohd_testcasecustomerversion as customerversion 
import ohd_testcaseinternalversion as internalversion


class CTestSuiteOutputhandler(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteOutputhandler"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, self.getComponentName())
                                                                               
        self.testCaseCustomerVersion = customerversion.CTestCaseOutputhandlerCustomerVersion(self.logger, canoe_api, t32_api)
        self.testCaseInternalVersion = internalversion.CTestCaseOutputhandlerInternalVersion(self.logger, canoe_api, t32_api)

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no outputhandler test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllOutputhandlerTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])
               
    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "outputhandler"

    def runAllOutputhandlerTests(self, t32_api):
        numberFailedTests = self.executeFilteredFunction(t32_api)
        
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests) 
    
    

        


