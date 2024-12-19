# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath('framework/interface'))
sys.path.append(os.path.abspath('framework/scheduling'))

import unittest
from unittest.mock import Mock

import testsuite # class under test
import testbase
import atf_globalconstants as globalConstants


class CTestAtfTestSuite(unittest.TestCase):

    def setUp(self):
        self.loggerApiMock = Mock(name='loggerApi')
        self.canoeApiMock = Mock(name='canoeApi')
        self.t32ApiMock = Mock(name='t32Api')
        self.replayApiMock = Mock(name='relayApi')          
        
        # class CTestSuite:  def __init__(self, logger_api, canoe_api , t32_api, relay_api, hw, globalTestcaseFilter):            
        self.testcaseTestInstance = CCustomTestSuite(self.loggerApiMock, self.canoeApiMock, self.t32ApiMock, self.replayApiMock, 
                                                  globalConstants.k_atf_hardwareLrr, '*')
        

    def test_CTestSuite_createTestCaseDictionary(self):        
        expectedFunctionNames = ('swTest_testcaseIntial', 'swTest_testcaseNew', 'swTest_testcaseOld', 'swTest_testcaseException',
                                 'check_testcaseInitial', 'check_testcaseNew', 'check_testcaseOld',
                                 'exampleTestCaseInitial', 'exampleTestCaseNew', 'failedTestCase', 'failedExceptionTestCase',
                                 'swTest_testcaseFailed')
        
        testDict = self.testcaseTestInstance.createTestCaseDictionary()
        
        # dictionary has: 
        # key: function name, value: callable function        
        for key, value in testDict.items():
            self.assertTrue(self.isValueInList(key, expectedFunctionNames), f"function: {key} not in expected list")                			
                
        
    def isValueInList(self, value, expectedValueList):
        expectedValueFound = False
    
        for valueIter in expectedValueList:
            if valueIter == value:
                expectedValueFound = True
                break 
            
        return expectedValueFound

    def test_CTestSuite_executeDictionaryFunction(self):                
        userFilter = ("swTest_testcaseIntial; swTest_testcaseNew; swTest_testcaseOld;"
                      "check_testcaseInitial; check_testcaseNew; check_testcaseOld;"
                      "exampleTestCaseInitial; exampleTestCaseNew")

        filteredDict = self.testcaseTestInstance.getFilteredTestCaseDictionary(userFilter, self.testcaseTestInstance.createTestCaseDictionary())

        # all passed test cases                
        self.assertEqual(0, self.testcaseTestInstance.executeDictionaryFunction(filteredDict, self.t32ApiMock))
        
        userFilter = ("swTest_testcaseIntial; swTest_testcaseNew; swTest_testcaseOld;"
                      "check_testcaseInitial; check_testcaseNew; check_testcaseOld;"
                      "failedTestCase")
                      
        filteredDict = self.testcaseTestInstance.getFilteredTestCaseDictionary(userFilter, self.testcaseTestInstance.createTestCaseDictionary())
        
        # Tests in CFailedTestCase are failed, but only one Test case is failed: 'failedTestCase'                 
        self.assertEqual(1, self.testcaseTestInstance.executeDictionaryFunction(filteredDict, self.t32ApiMock))
        
        userFilter = ("swTest_testcaseIntial; swTest_testcaseOld;"
                      "check_testcaseInitial; check_testcaseOld;"
                      "failedTestCase; swTest_testcaseFailed")
                      
        filteredDict = self.testcaseTestInstance.getFilteredTestCaseDictionary(userFilter, self.testcaseTestInstance.createTestCaseDictionary())
        
        # Tests in CFailedTestCase and swTest_testcaseFailed are failed                 
        self.assertEqual(2, self.testcaseTestInstance.executeDictionaryFunction(filteredDict, self.t32ApiMock))        
        
    def test_CTestSuite_executeDictionaryFunctionException(self):
        userFilter = ("swTest_testcaseIntial; swTest_testcaseException; failedExceptionTestCase")

        filteredDict = self.testcaseTestInstance.getFilteredTestCaseDictionary(userFilter, self.testcaseTestInstance.createTestCaseDictionary())
                    
        # check if the test cases raise exceptions                    
        self.assertRaises(Exception, self.testcaseTestInstance.executeDictionaryFunction(filteredDict, self.t32ApiMock))
        self.assertEqual(2, self.testcaseTestInstance.executeDictionaryFunction(filteredDict, self.t32ApiMock))        


class CCustomTestSuite(testsuite.CTestSuite):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api, canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, "test_atftestsuite")

        self.exampleTestCaseInitial = CExampleTestCaseInitial(logger_api, canoe_api, t32_api)
        self.exampleTestCaseNew = CExampleTestCaseNew(logger_api, canoe_api, t32_api)
        self.failedTestCase = CFailedTestCase(logger_api, canoe_api, t32_api)
        self.failedExceptionTestCase = CFailedExceptionTestCase(logger_api, canoe_api, t32_api)

    # Define some functions for the dictionary 
    # some which start with 'swTest_', some with 'check_' and some other which do not match the criteria

    def swTest_testcaseIntial(self, t32_api):
        return testbase.CTestCaseResult(3, 0)
    
    def swTest_testcaseNew(self, t32_api):
        return testbase.CTestCaseResult(2, 0)
    
    def swTest_testcaseOld(self, t32_api):
        return testbase.CTestCaseResult(5, 0)
    
    def swTest_testcaseFailed(self, t32_api):
        return testbase.CTestCaseResult(5, 3)    
    
    def swTest_testcaseException(self, t32_api):
        raise Exception("Test case swTest_testcaseException failed with Exception")
        return testbase.CTestCaseResult(8, 8)
    
    def check_testcaseInitial(self, t32_api):
        return testbase.CTestCaseResult(1, 0)
    
    def check_testcaseNew(self, t32_api):
        return testbase.CTestCaseResult(4, 0)
    
    def check_testcaseOld(self, t32_api):
        return testbase.CTestCaseResult(8, 0)

    def sdm_swTest_testcaseInitial(self):
        pass
    
    def diag_check_testcaseNew(self):
        pass

    def simpleFunction(self):
        pass
    
    def TestFunc(self):
        pass
    
    def checkTestFunc(self):
        pass


class CExampleTestCaseInitial(testbase.CTestBase):
    def setUp(self):
        pass                      
    
    def tearDown(self):
        pass
   
    def executeTests(self, t32_api, testCaseNumber):
        return testbase.CTestCaseResult(10, 0)

class CExampleTestCaseNew(testbase.CTestBase):
    def setUp(self):
        pass                      
    
    def tearDown(self):
        pass
   
    def executeTests(self, t32_api, testCaseNumber):
        return testbase.CTestCaseResult(5, 0)
    
class CFailedTestCase(testbase.CTestBase):
    def setUp(self):
        pass                      
    
    def tearDown(self):
        pass
   
    def executeTests(self, t32_api, testCaseNumber):
        return testbase.CTestCaseResult(13, 13)  

class CFailedExceptionTestCase(testbase.CTestBase):
    def setUp(self):
        pass                      
    
    def tearDown(self):
        pass
   
    def executeTests(self, t32_api, testCaseNumber):
        raise Exception("Test case CFailedExceptionTestCase failed with Exception")
        return testbase.CTestCaseResult(20, 20)        

