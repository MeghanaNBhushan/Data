# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath('framework/interface'))

import unittest

from testsuite import TestSuiteResult # class under test


class CTestAtfTestSuiteResult(unittest.TestCase):
       
    def test_TestSuiteResult_addResults(self):        
        initialResult = TestSuiteResult(10, 2)
        
        self.assertEqual(initialResult.numberTests, 10)
        self.assertEqual(initialResult.numberFailedTests, 2)
                
        initialResult += TestSuiteResult(50, 1)
        
        self.assertEqual(initialResult.numberTests, 60)
        self.assertEqual(initialResult.numberFailedTests, 3)

        furtherResult = TestSuiteResult(2, 3)
        
        initialResult += furtherResult
        
        self.assertEqual(initialResult.numberTests, 62)
        self.assertEqual(initialResult.numberFailedTests, 6)
        
        furtherResult += TestSuiteResult(30, 10)
        furtherResult += TestSuiteResult(40, 20)
        furtherResult += TestSuiteResult(50, 30)

        self.assertEqual(furtherResult.numberTests, 122)
        self.assertEqual(furtherResult.numberFailedTests, 63)
