# -*- coding: utf-8 -*-

from atf_exception import CNoDerivedClassError 

class CTestBase(object):
    
    def __init__(self, loggerApi, canoeApi , t32Api):
        self.logger = loggerApi
        self.canoe_api = canoeApi
        self.t32_api = t32Api
               
    def setUp(self):
        raise CNoDerivedClassError("Function: setUp() has to be implemented in derived class")
    
    def tearDown(self):
        raise CNoDerivedClassError("Function: tearDown() has to be implemented in derived class")
    
    def executeTests(self, t32_api):
        raise CNoDerivedClassError("Function: executeTests() has to be implemented in derived class")
    
    def executeTestCase(self, t32_api, testCaseNumber):
        self.setUp()
        failedTests = self.executeTests(t32_api, testCaseNumber)
        self.tearDown()    

        return failedTests
    
    
class CTestCaseResult:
    def __init__(self, numberTests, numberFailedTests):
        self.numberTests = numberTests
        self.numberPassedTests = (numberTests - numberFailedTests)
        self.numberFailedTests = numberFailedTests        