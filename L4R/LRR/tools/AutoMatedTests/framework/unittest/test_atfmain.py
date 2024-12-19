# -*- coding: utf-8 -*-

import unittest

import test_atftestsuite
import test_atftestsuiteresult
import test_atftestbase


def testSuiteAtfTestSuite():
    suite = unittest.TestSuite()
    
    suite.addTest(test_atftestsuite.CTestAtfTestSuite('test_CTestSuite_createTestCaseDictionary'))
    suite.addTest(test_atftestsuite.CTestAtfTestSuite('test_CTestSuite_executeDictionaryFunction'))
    suite.addTest(test_atftestsuite.CTestAtfTestSuite('test_CTestSuite_executeDictionaryFunctionException'))
    
    return suite


def testSuiteAtfTestSuiteResult():
    suite = unittest.TestSuite()
    
    suite.addTest(test_atftestsuiteresult.CTestAtfTestSuiteResult('test_TestSuiteResult_addResults'))

    return suite
    

def testSuiteAtfTestBase():
    suite = unittest.TestSuite()
    
    suite.addTest(test_atftestbase.CTestAtfTestBase('test_CTestBase_setUp'))
    suite.addTest(test_atftestbase.CTestAtfTestBase('test_CTestBase_tearDown'))
    suite.addTest(test_atftestbase.CTestAtfTestBase('test_CTestBase_executeTests'))
    suite.addTest(test_atftestbase.CTestAtfTestBase('test_CTestBase_executeTestCase'))
    
    return suite


if __name__ == '__main__':
    testRunner = unittest.TextTestRunner()
    testRunner.run(testSuiteAtfTestSuite())
    testRunner.run(testSuiteAtfTestSuiteResult())
    testRunner.run(testSuiteAtfTestBase())
    
