# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:22:18 2021

@author: YAH3KOR
"""
import sys
import os
import subprocess
import time
from datetime import timedelta

sys.path.append(os.path.abspath('framework/helper'))
sys.path.append(os.path.abspath('framework/interface'))
sys.path.append(os.path.abspath('testcases/diag'))
sys.path.append(os.path.abspath('testcases/int'))
sys.path.append(os.path.abspath('testcases/outputhandler'))
sys.path.append(os.path.abspath('testcases/rbSysEvM'))
sys.path.append(os.path.abspath('testcases/sdm'))
sys.path.append(os.path.abspath('testcases/lodm'))
sys.path.append(os.path.abspath('testcases/coma'))
sys.path.append(os.path.abspath('testcases/vama'))
sys.path.append(os.path.abspath('testcases/testmode'))

import AD_lauterbach_test_helper as lauterbachTestHelper
import rbSysEvM_testsuite as swTestRbSysEvM
import diag_testsuitefbl as swTestDiagFbl
import diag_testsuitevarianthandling as swTestDiagVarHdl
import diag_testsuitebasic as swTestDiag
import int_testsuite as swTestInt
import sdm_testsuite as swTestSdm
import ohd_testsuite as swTestOutputhandler
import lodm_testsuite as swTestLodm
import coma_testsuite as swTestComa
import vama_testsuite as swTestVama
import trace32_testsuite as testmode_lauterbach
import testsuite
import atf_globalconstants as globalConstants

from atf_executiontime import CExecutionTime


class TestExecution:
    def __init__(self, args, logger_api, canoe_api, t32_api, relay_api):
        self.smoketest_failed = False
        self.logger_api = logger_api
        self.logger = logger_api.get_logger("TEST_EXECUTION")
        self.lauterbach_helper_logger = logger_api.get_logger("LAUTERBACH_TEST_HELPER")
        self.canoe_api = canoe_api
        self.relay_api = relay_api
        self.t32_api = t32_api
        self.testmode = int(args.frameworktestmode)
        self.args = args 
        self.logger_api.create_report(args.report_dir, self.logger, args.hardware)
        self.intTests = swTestInt.CTestSuiteInt(logger_api, canoe_api, t32_api, relay_api, self.args.hardware, args.testcasefilter)
        self.diagTests = swTestDiag.CTestSuiteDiagBasic(self.logger_api, self.canoe_api , self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.diagFblTests = swTestDiagFbl.CTestSuiteDiagFbl(self.logger_api, self.canoe_api , self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.diagVarHdlTests = swTestDiagVarHdl.CTestSuiteDiagVariantHandling(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.evmTests = swTestRbSysEvM.CTestSuiteRbSysEvm(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.sdmTests = swTestSdm.CTestSuiteSdm(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.outputhandlerTests = swTestOutputhandler.CTestSuiteOutputhandler(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.lodmTests = swTestLodm.CTestSuiteLodm(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.comaTests = swTestComa.CTestSuiteComa(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.vamaTests = swTestVama.CTestSuiteVama(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)
        self.lauterbachTests =  testmode_lauterbach.CTestSuiteTrace32(self.logger_api, self.canoe_api, self.t32_api, self.relay_api, self.args.hardware, args.testcasefilter)		
        
        self.printTestFrameworkInformation(args.testcasefilter)
        
        time.sleep(1)


    def __del__(self):
        if self.args.hardware == globalConstants.k_atf_hardwareLrr:
            self.t32_api[globalConstants.k_atf_hardwareLrrUc1].synch_off()
            self.t32_api[globalConstants.k_atf_hardwareLrrUc2].synch_off()
            self.t32_api[globalConstants.k_atf_hardwareLrrUc1].close_power_view()
            self.t32_api[globalConstants.k_atf_hardwareLrrUc2].close_power_view()

        output = subprocess.check_output('tasklist', shell=True)
        if "CANoe64.exe" in str(output):
            os.system("taskkill /im CANoe64.exe /f 2>nul >nul") 


    def printTestFrameworkInformation(self, testcaseFilter):
        self.logger.info("------------------------------------------")
        self.logger.info("----Automated------Test------Framework----")
        self.logger.info("------------------------------------------")        
        self.logger.info("      ___                       ___       ")
        self.logger.info("     /  /\          ___        /  /\      ")
        self.logger.info("    /  /::\        /  /\      /  /:/_     ")
        self.logger.info("   /  /:/\:\      /  /:/     /  /:/ /\    ")
        self.logger.info("  /  /:/~/::\    /  /:/     /  /:/ /:/    ")
        self.logger.info(" /__/:/ /:/\:\  /  /::\    /__/:/ /:/     ")
        self.logger.info(" \  \:\/:/__\/ /__/:/\:\   \  \:\/:/      ")
        self.logger.info("  \  \::/      \__\/  \:\   \  \::/       ")
        self.logger.info("   \  \:\           \  \:\   \  \:\       ")
        self.logger.info("    \  \:\           \__\/    \  \:\      ")
        self.logger.info("     \__\/                     \__\/      ")              
        self.logger.info("------------------------------------------")
        self.logger.info(f"Version: {globalConstants.k_atfVersion}")                                                
        self.logger.info(f"Hardware: {globalConstants.k_atf_hardwareLrr}")
        self.logger.info(f"Filter: {testcaseFilter}")        
        self.logger.info("------------------------------------------")                    


    def run_tests(self):          
        if self.args.hardware == globalConstants.k_atf_hardwareLrr:
            try :                
                lauterbachTestHelper.flash_ecu_run_fr5cu(self.t32_api, self.lauterbach_helper_logger, self.args)        
                self.logger.debug("Flashing uC1 and uC2    -> success")
        
                self.logger.info("Starting SW tests on uC1...\n")
                self.run_tests_uC1()
                self.logger.info("Starting SW tests on uC2...\n")
                self.run_tests_uC2()

                self.logger.info("##########################################")
                self.logger.info("###      FR5CU SW TESTS FINISHED      ####")
                self.logger.info("###        ---- SUCCESS ----          ####")
                self.logger.info("##########################################")

            except Exception as exception:
                 self.logger.info(f"    -> FAILED :-( with exception: '{exception}' \n\n")
                 self.smoketest_failed = True
                
                 self.logger.info("##########################################")
                 self.logger.info("###      FR5CU SW TESTS FINISHED      ####")
                 self.logger.info("###        ---- FAILURE ----          ####")
                 self.logger.info("##########################################")
                 raise Exception(f"[E] Smoke test failed with exception : '{exception}'")	

            finally:
                 self.canoe_api.stopMeasurement()
                 return self.smoketest_failed

        else:
            # last supported release for NR5CP was xRR_LGU_PF_V7.0.0
            raise Exception("Different hardware not supported - FR5CU supported only!")


    ## @brief Main routine to run all FR5CU UC1 test cases.
    # 
    # On every test suite the abstract function \e executeFr5CuTestsUC1 is called to execute the corresponding test cases.  
    def run_tests_uC1(self):
        testResults = testsuite.TestSuiteResult(0, 0)
        functionTimer = CExecutionTime()
        totalTestDuration = timedelta(seconds = 0)

        self.logger.debug(f"TestMode on uC1: {self.testmode}")

        if (self.testmode == 1):
            # define 'testMode' components which shall be executed
            allTestComponents = (self.lauterbachTests,)
        else:
            # define execution order in tuple
            allTestComponents = (self.intTests,)                                                            
        
        #execute all tests and measure the execution time
        for component in allTestComponents:
            resultTuple = functionTimer.measureFunctionTime(component.executeFr5CuTestsUC1)
            testResults += resultTuple[1]
            totalTestDuration += resultTuple[0]
            self.logger.info(f"Execution of test cases in component \"{component.getComponentName()}\" took {resultTuple[0]} time")        
                              
        self.printTestResults(globalConstants.k_atf_hardwareLrr, False, testResults, totalTestDuration)

        
    ## @brief Main routine to run all FR5CU UC2 test cases.
    # 
    # On every test suite the abstract function \e executeFr5CuTestsUC2 is called to execute the corresponding test cases.        
    def run_tests_uC2(self):
        testResults = testsuite.TestSuiteResult(0, 0)
        functionTimer = CExecutionTime()
        totalTestDuration = timedelta(seconds = 0)
                      
        self.logger.debug(f"TestMode on uC2: {self.testmode}")                      
                      
        if (self.testmode == 1):
            # define 'testMode' components which shall be executed
            allTestComponents = (self.lauterbachTests,)
        else:
            # define execution order in tuple
            allTestComponents = (self.intTests, self.evmTests, self.sdmTests, self.diagVarHdlTests, self.diagTests, 
                                 self.diagFblTests, self.outputhandlerTests,self.lodmTests,self.comaTests,self.vamaTests)                                                            
        
        #execute all tests and measure the execution time
        for component in allTestComponents:
            if (component.getComponentName() == "diag_variant"):
                # connect Toellner Panel in RBS which is required for Diag tests
                self.canoe_api.connectPowerSupply()
                
            resultTuple = functionTimer.measureFunctionTime(component.executeFr5CuTestsUC2)
            testResults += resultTuple[1]
            totalTestDuration += resultTuple[0]
            self.logger.info(f"Execution of test cases in component \"{component.getComponentName()}\" took {resultTuple[0]} time")
        
        self.printTestResults(globalConstants.k_atf_hardwareLrr, True, testResults, totalTestDuration)


    def printTestResults(self, variant, isFr5CuUc2, testSuiteResult, totalTestDuration):
        variantString = "uC2"
        
        if (globalConstants.k_atf_hardwareLrr == variant and isFr5CuUc2 == False):
            variantString = "uC1"
        else:
            # already set to uC2
            pass

        self.logger.info("#####################################")
        self.logger.info(f"###     {variantString} TEST FINISHED       ###")
                
        if testSuiteResult.numberFailedTests != 0:

            self.logger.info("###      ---- FAILURE ----        ###")
            self.logger.info(f"#### Tests failed {testSuiteResult.numberFailedTests} of {testSuiteResult.numberTests}      ###")
            self.logger.info(f"### Total time   {totalTestDuration}   ###")
            self.logger.info("#####################################")
            raise Exception("Test cases failed")
        else:
            self.logger.info("###      ---- SUCCESS ----        ###")
            self.logger.info(f"### Tests passed {testSuiteResult.numberTests} of {testSuiteResult.numberTests}       ###")
            self.logger.info(f"### Total time   {totalTestDuration}   ###")
            self.logger.info("#####################################")                
        
