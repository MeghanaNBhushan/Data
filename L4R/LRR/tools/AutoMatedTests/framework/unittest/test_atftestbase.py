# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath('framework/interface'))
sys.path.append(os.path.abspath('framework/scheduling'))

import unittest
from unittest.mock import Mock

import testbase # class under test
from atf_exception import CNoDerivedClassError


k_derivedTestcaseFailedTests = 10


class CTestAtfTestBase(unittest.TestCase):

    def setUp(self):
        self.loggerApiMock = Mock(name='loggerApi')
        self.canoeApiMock = Mock(name='canoeApi')
        self.t32ApiMock = Mock(name='t32Api')
        self.replayApiMock = Mock(name='relayApi')
        
        # class CTestBase:  def __init__(self, logger_api, canoe_api , t32_api):
        self.testbaseTestInstance = testbase.CTestBase(self.loggerApiMock, self.canoeApiMock, self.t32ApiMock)
        
    
    ## @unittest_description This unit test checks that an exception is raised if the abstract function 'setUp()' is called on the base class.
    #  @unittest_step 
    #    1. Create an instance of CTestBase
    #    2. Call 'setUp()' on the base class
    #  @unittest_expResult The exception 'CNoDerivedClassError' is raised.
    def test_CTestBase_setUp(self):                            
        self.assertRaises(CNoDerivedClassError, self.testbaseTestInstance.setUp)

    ## @unittest_description This unit test checks that an exception is raised if the abstract function 'tearDown()' is called on the base class.
    #  @unittest_step 
    #    1. Create an instance of CTestBase
    #    2. Call 'tearDown()' on the base class
    #  @unittest_expResult The exception 'CNoDerivedClassError' is raised.
    def test_CTestBase_tearDown(self):                            
        self.assertRaises(CNoDerivedClassError, self.testbaseTestInstance.tearDown)

    ## @unittest_description This unit test checks that an exception is raised if the abstract function 'executeTests()' is called on the base class.
    #  @unittest_step 
    #    1. Create an instance of CTestBase
    #    2. Call 'executeTests()' on the base class
    #  @unittest_expResult The exception 'CNoDerivedClassError' is raised.
    def test_CTestBase_executeTests(self):                            
        self.assertRaises(CNoDerivedClassError, self.testbaseTestInstance.executeTests, self.t32ApiMock)

    ## @unittest_description This unit test checks that all abstract function are called and the defined failed tests are returned.
    #  @unittest_step 
    #    1. Create a test class derived of 'CTestBase' and create an instance of it
    #    2. Check that 'setUp()' and 'tearDown()' were not called before
    #    3. Call 'executeTestCase()' on the created class
    #    4. Check that 'setUp()' and 'tearDown()' were now called
    #  @unittest_expResult The returned failed tests number matches the defined value in the test derived class.
    def test_CTestBase_executeTestCase(self):        
        testDerivedTestInstance = CDerivedTest(self.loggerApiMock, self.canoeApiMock, self.t32ApiMock)

        self.assertEqual(False, testDerivedTestInstance.isSetUpCalled)
        self.assertEqual(False, testDerivedTestInstance.isTearDown)

        failedTests = testDerivedTestInstance.executeTestCase(self.t32ApiMock, 0)

        self.assertEqual(True, testDerivedTestInstance.isSetUpCalled)
        self.assertEqual(True, testDerivedTestInstance.isTearDown)
        
        self.assertEqual(failedTests, k_derivedTestcaseFailedTests)    
    

## Derived test class of CTestBase  
#    
class CDerivedTest(testbase.CTestBase):

    def __init__(self, logger_api, canoe_api, t32_api):
        super().__init__(logger_api, canoe_api , t32_api) 
        
        self.isSetUpCalled = False
        self.isTearDown = False
    
    def setUp(self):
        self.isSetUpCalled = True                      
    
    def tearDown(self):
        self.isTearDown = True
   
    def executeTests(self, t32_api, testCaseNumber):
        return k_derivedTestcaseFailedTests 
        