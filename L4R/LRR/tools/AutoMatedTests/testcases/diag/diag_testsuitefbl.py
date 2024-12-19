# -*- coding: utf-8 -*-

import time
import xlrd as rd
import sys
import os

sys.path.append(os.path.abspath('../../framework/helper'))
sys.path.append(os.path.abspath('../../framework/scheduling'))
sys.path.append(os.path.abspath('../../framework/interface'))

import atf_toolbox as testHelper
import atf_testasserts as testasserts
import diag_constants as constant
import AD_canoe_diag_functions as canoeDiagPanel
import AD_lauterbach_test_helper as lauterbachTestHelper
import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants
from testbase import CTestCaseResult


class CTestSuiteDiagFbl(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteDiagFbl"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, self.getComponentName())

        
    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no Diag FBL test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllDiagFblTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])         

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "diag_fbl"
                      
    def runAllDiagFblTests(self, t32_api):    
        # jump to Default Session as precondition for diag tests
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
    
        localFilterList = ("swTest_checkFblBctConfiguredIpIsWrittenToNvm; swTest_checkFblDiagRequestedIpIsWrittenToNvm; swTest_checkFblNoNewIpIsWrittenToNvm;"
                           "swTest_checkFblBctConfiguredMacIsWrittenToNvm; swTest_checkFblDiagRequestedMacIsWrittenToNvm; swTest_checkFblDiagRequestedDoIpIsWrittenToNvm;"
                           "swTest_checkJumpToFblResponsePending")

        # We need the filter function by user, because some function are commented.
        # Once no function is commented the 'executeFilteredFunction' function may be used instead.         
        numberFailedTests = self.executeFilteredFunctionUser(t32_api, localFilterList)         

        # Once the function shall be enabled, add it to the filter above or use 'executeFilteredFunction'
        # numberFailedTests += self.swTest_checkJumpFromFblResetReasonPacket(t32_api)
        # self.number_of_test += 1   
  

        # following two test cases are commented for the moment as sporadically the sensor ends up in a safe state
        # after jump to FBL or jump from FBL to Application. This is due to some issue in Boot Manager V6.3.0
        # Current assumption is that these test cases can be re-activated with SW Version 4.0.0 (as this will use BM V7.0.0)
        
        # Once the function shall be enabled, add it to the filter above or use 'executeFilteredFunction'
        # numberFailedTests += self.swTest_checkEcuResetHandlerDenyDcmRequests(t32_api)
        # self.number_of_test += 1   
    
        # Once the function shall be enabled, add it to the filter above or use 'executeFilteredFunction'
        # numberFailedTests += self.swTest_checkCloseConnectionToDiagTester(t32_api)
        # self.number_of_test += 1   


        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)
    
    
    ## @swtest_description The test case checks if calling the "Change IP address" diagnostic service with an NVM Flag = 0 writes the initially configured
    #   BCT address for the diagnostic communication into the NVM packet which is used to provide the IP address to the Flashbootloader.
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service for the IP address used for Diagnosis (for the other IP addresses, NVM Flag
    #      is set to 2 = don't take over these addresses). Use any IP address in the correct range (e.g. 0xA9 FE 22 93) and set NVM Flag for this address to 0.
    #      Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet NvM_diaFbl_DynamicNetworkConfigFblExchange_st
    #  @swtest_expResult The NVM mirror value is equal to the address which has been configured initially in BCT.
    #  @sw_requirement{SDC-R_SW_DIMA_697, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-697-00159bc2?doors.view=0000000b}
    def swTest_checkFblBctConfiguredIpIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

        # Step 1: send change Diag IP address service with NVM Flag = 0 and different IP address than the BCT configured one (e.g. 169.254.19.150)
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR + \
            constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + \
                constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR_HEX + constant.CONST_DIAG_NVM_FLAG_READ_INITIAL_BCT_VALUES + \
                    constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA
    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        writeFDLResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug("f step 1: write FBL IP to NVM : {writeFDLResponse}")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeFDLResponse[0:6]
        self.logger.debug(f"Step 1: READ FBL BCT : {writeResponseStatus}")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_FBL_IP, "Step 2:Check WDBI  IP - response")
        numberTest += 1
        #Step 3.Read FBL port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_FBL_IP, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 1: READ FBL IP: {Read_DID}")        
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        
      
        self.logger.debug(f"Step 1: READ FBL BCT : {readResponseStatus}")
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_FBL_IP, readResponseStatus,
                                                 "Step 4:Check RBDI FBL IP - response")
        numberTest += 1 
        
        # Step 5: Check if IP Address values from BCT have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[0]")['vvalue'].value
        nvmMirrorSecondValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[1]")['vvalue'].value
        nvmMirrorThirdValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[2]")['vvalue'].value
        nvmMirrorFourthValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[3]")['vvalue'].value
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, self.number_of_test, nvmMirrorString,
                                                  constant.CONST_DIAG_INITIAL_BCT_IP_ADDR, "Check g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if calling the "Change IP address" diagnostic service with an NVM Flag = 1 writes the IP Address from the request
    #   into the NVM packet which is used to provide the IP address to the Flashbootloader.
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03) and send "Change IP Address" service for the IP address used for Diagnosis (for the other IP addresses, NVM Flag
    #      is set to 2 = don't take over these addresses). Use any IP address in the correct range (e.g. 0xA9 FE 13 96) and set NVM Flag for this address to 1.
    #      Send ECU Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet NvM_diaFbl_DynamicNetworkConfigFblExchange_st
    #   3. Cleanup to get back original IP address
    #  @swtest_expResult The NVM mirror value is equal to the address which has been sent in the request (e.g. 0xA9 FE 13 96 = 0d 169.254.19.150).
    #  @sw_requirement{SDC-R_SW_DIMA_698, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-698-00159bc2?doors.view=0000000b}
    def swTest_checkFblDiagRequestedIpIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

        # Step 1: send change Diag IP address service with NVM Flag = 1 and different IP address than the BCT configured one (e.g. 169.254.19.150)
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR + \
            constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + \
                constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR_HEX + constant.CONST_DIAG_NVM_FLAG_READ_VALUES_FROM_NVM + \
                    constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA
    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        writeFDLResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug("f step 1: write FBL IP to NVM : {writeFDLResponse}")
        
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeFDLResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_FBL_IP, "Step 2:Check WDBI  IP - response")
        numberTest += 1
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        #Step 3.Read FBL port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_FBL_IP, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 1: READ FBL IP : {Read_DID}")        
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        self.logger.debug(f"Step 1: READ FBL IP: {readResponseStatus}")
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_FBL_IP, readResponseStatus,
                                                 "Step 4:Check RBDI FBL IP- response")
        numberTest += 1
    
        # Step 5: Check if values from the request have been taken over
        # Check NVM mirror which is copied at startup from the NVM
        nvmMirrorFirstValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[0]")['vvalue'].value
        nvmMirrorSecondValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[1]")['vvalue'].value
        nvmMirrorThirdValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[2]")['vvalue'].value
        nvmMirrorFourthValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[3]")['vvalue'].value
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR, "Check g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
    
        # Step 4: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if calling the "Change IP address" diagnostic service with an NVM Flag = 2 does not override the IP Address
    #   which is currently stored in the NVM packet which is used to provide the IP address to the Flashbootloader with the sent IP Address.
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03) and send "Change IP Address" service for the IP address used for Diagnosis (for the other IP addresses, NVM Flag
    #      is set to 2 = don't take over these addresses). Use any IP address in the correct range (e.g. 0xA9 FE 14 97) and set NVM Flag for this address to 1.
    #      To be sure, use an IP address which has not been used in previous test cases. Send ECU Hard Reset afterwards.
    #   2. Jump to Extended Session. Send "Change IP Address" service with all NVM Flags set to 2. For the IP address used for Diagnosis, use a value different
    #      to the address used in step 1. Send ECU Hard Reset afterwards.
    #   3. Check if values of step 1 are still written into the NVM Mirror Value of NvM_diaFbl_DynamicNetworkConfigFblExchange_st after step 2.
    #   4. Cleanup to get back original IP address
    #  @swtest_expResult The values written in Step 1 are equal to the NVM Mirror NvM_diaFbl_DynamicNetworkConfigFblExchange_st after step 2.
    #  @sw_requirement{SDC-R_SW_DIMA_699, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-699-00159bc2?doors.view=0000000b}
    def swTest_checkFblNoNewIpIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1    
    
        # Step 1: send change Diag IP address service with NVM Flag = 1 and different IP address than the BCT configured one (e.g. 169.254.20.151)
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR + \
            constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + \
                constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR2_HEX + constant.CONST_DIAG_NVM_FLAG_READ_VALUES_FROM_NVM + \
                    constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA

        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        writeFDLResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug("f step 1: write FBL to NVM : {writeFDLResponse}")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeFDLResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_FBL_IP, "Step 2:Check WDBI  IP - response")
        numberTest += 1

        #Step 3.Read FBL port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_FBL_IP, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 1: READ FBL : {Read_DID}")        
        time.sleep(0.5)
        
        #Step 4. Validate read response -> positive response
        readResponseStatus        = Read_DID[0:6]
        self.logger.debug(f"Step 1: READ FBL : {readResponseStatus}")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_FBL_IP, readResponseStatus,
                                                 "Step 4:Check RBDI FBL - response")
        numberTest += 1 
    
        # Step 5: send change Diag IP address service with NVM Flag = 2 and different IP address than the BCT configured one and different to the one from Step 1
        # (e.g. 169.254.19.150). Value should not be taken over as NVM Flag = 2
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR + \
            constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_IP_ADDR_REQUEST_ZERO + \
                constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR_HEX + constant.CONST_DIAG_NVM_FLAG_IGNORE_ADDR_FROM_REQUEST + \
                    constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA

        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
    
        # Step 6: Compare values written in step 1 to current NVM Mirror
        # Check NVM mirror which is copied at startup from the NVM
        nvmMirrorFirstValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[0]")['vvalue'].value
        nvmMirrorSecondValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[1]")['vvalue'].value
        nvmMirrorThirdValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[2]")['vvalue'].value
        nvmMirrorFourthValue = t32_api.get_variable_value("g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[3]")['vvalue'].value
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR2, "Check g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
    
        # Step 4: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if calling the "Change MAC address" diagnostic service with an NVM Flag = 0 writes the initially configured
    #   BCT MAC address into the NVM packet which is used to provide the MAC address to the Flashbootloader. 
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change MAC Address" service with an NVM Flag set to 0. Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet NvM_diaFbl_DynamicNetworkConfigFblExchange_st
    #  @swtest_expResult The NVM mirror value is equal to the address which has been configured initially in BCT.
    #  @sw_requirement{SDC-R_SW_DIMA_704, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-704-00159bc2?doors.view=0000000b}
    def swTest_checkFblBctConfiguredMacIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1    
    
        #Step 1: send change MAC address service with NVM Flag = 0 and different MAC address than the BCT configured one (e.g. 4c:de:16:01:10:ff)
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_MAC_ADDR + \
            testHelper.removeColons(constant.CONST_DIAG_USER_CONFIGURED_MAC_ADDR) + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA + \
                constant.CONST_DIAG_NVM_FLAG_READ_INITIAL_BCT_VALUES 
                
        
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        writeFDLResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug("f step 1: write FBL to NVM : {writeFDLResponse}")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3)
        
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeFDLResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_FBL_MAC, "Step 2:Check WDBI  Mac - response")
        numberTest += 1
        #Step 3.Read FBL port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_FBL_MAC, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 1: READ FBL : {Read_DID}")        
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        self.logger.debug(f"Step 1: READ FBL : {readResponseStatus}")
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_FBL_MAC, readResponseStatus,
                                                 "Step 4:Check RBDI FBL - response")
        numberTest += 1 
        # Step 5: Check if MAC Address values from BCT have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        # format: convert values to 2 digit hex values
        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[4]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[5]")['vvalue'].value, '02x')
        nvmMirrorThirdValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[6]")['vvalue'].value, '02x')
        nvmMirrorFourthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[7]")['vvalue'].value, '02x')
        nvmMirrorFifthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[8]")['vvalue'].value, '02x')
        nvmMirrorSixthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[9]")['vvalue'].value, '02x')
    
        nvmMirrorString = str(nvmMirrorFirstValue) + ":" + str(nvmMirrorSecondValue) + ":" + str(nvmMirrorThirdValue) + \
            ":" + str(nvmMirrorFourthValue) + ":" + str(nvmMirrorFifthValue) + ":" + str(nvmMirrorSixthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  constant.CONST_DIAG_INITIAL_BCT_MAC_ADDR, "Check g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if calling the "Change MAC address" diagnostic service with an NVM Flag = 1 writes the IP Address from the request
    #   into the NVM packet which is used to provide the MAC address to the Flashbootloader.
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03) and send "Change MAC Address" service with an NVM Flag set to 1. Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet NvM_diaFbl_DynamicNetworkConfigFblExchange_st
    #   3. Cleanup to get back original IP address
    #  @swtest_expResult The NVM mirror value is equal to the address which has been sent in the request.
    #  @sw_requirement{SDC-R_SW_DIMA_705, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-705-00159bc2?doors.view=0000000b}
    def swTest_checkFblDiagRequestedMacIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change MAC address service with NVM Flag = 1 and different MAC address than the BCT configured one (e.g. 4C:DE:16:01:10:FF)
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_MAC_ADDR + \
            testHelper.removeColons(constant.CONST_DIAG_USER_CONFIGURED_MAC_ADDR) + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA + \
                    constant.CONST_DIAG_NVM_FLAG_READ_VALUES_FROM_NVM 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        writeFDLResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        
        
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeFDLResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_FBL_MAC, "Step 2:Check WDBI  Mac - response")
        numberTest +=1 
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3)
        
        #Step 3.Read FBL port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_FBL_MAC, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 1: READ FBL MAC : {Read_DID}")        
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        macnvmvalue        = Read_DID[6:18]
        self.logger.debug(f"Step 1: READ FBL MAC : {readResponseStatus}")
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_FBL_MAC, readResponseStatus,
                                                 "Step 4:Check RBDI FBL - response")
        numberTest += 1 
        # Step 5: Check if values from the request have been taken over
        # Check NVM mirror which is copied at startup from the NVM
        # format: convert values to 2 digit hex values
        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[4]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[5]")['vvalue'].value, '02x')
        nvmMirrorThirdValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[6]")['vvalue'].value, '02x')
        nvmMirrorFourthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[7]")['vvalue'].value, '02x')
        nvmMirrorFifthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[8]")['vvalue'].value, '02x')
        nvmMirrorSixthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[9]")['vvalue'].value, '02x')
    
        nvmMirrorString = str(nvmMirrorFirstValue) + str(nvmMirrorSecondValue) + str(nvmMirrorThirdValue) + str(nvmMirrorFourthValue)  + str(nvmMirrorFifthValue) + str(nvmMirrorSixthValue)
        self.logger.debug(f"step :FBL MAC :{nvmMirrorString}")
    
        #numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  #constant.CONST_DIAG_USER_CONFIGURED_MAC_ADDR, "Check g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  macnvmvalue, "Check g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
        numberTest +=1
        
        # Step 6: Cleanup
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_MAC_ADDR + \
            testHelper.removeColons(constant.CONST_DIAG_INITIAL_BCT_MAC_ADDR) + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA + \
                    constant.CONST_DIAG_NVM_FLAG_READ_INITIAL_BCT_VALUES

        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change MAC address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if calling the "Change DoIP address" diagnostic service writes the DoIP Address from the request into the NVM 
    #   packet which is used to provide the DoIP address to the Flashbootloader.
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03) and send "Change DoIP Address" service. Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet NvM_diaFbl_DynamicNetworkConfigFblExchange_st
    #   3. Cleanup to get back original DoIP address
    #  @swtest_expResult The NVM mirror value is equal to the address which has been sent in the request.
    #  @sw_requirement{SDC-R_SW_DIMA_706, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-706-00159bc2?doors.view=0000000b}
    def swTest_checkFblDiagRequestedDoIpIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_DOIP_ADDR + \
            constant.CONST_DIAG_USER_CONFIGURED_DOIP_ADDR_HEX + constant.CONST_DIAG_DOIP_DUMMY
    
        # Step 1: send change DoIP address service with a different DoIP address than the BCT configured one 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        writeFDLResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
       
        
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeFDLResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_FBL_DOIP, "Step 2:Check WDBI  DOIP - response")
        numberTest += 1
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", int(constant.CONST_DIAG_USER_CONFIGURED_DOIP_ADDR_HEX, 16))
        
        #Step 3.Read DOIP port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_FBL_DOIP, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 1: READ FBL DOIP : {Read_DID}")        
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        readfbldoip               = Read_DID[6:10]
        self.logger.debug(f"Step 2: READ FBL DOIP : {readResponseStatus}")
        #Step 5. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_FBL_DOIP, readResponseStatus,
                                                 "Step 3:Check RBDI FBL DOIP - response")
        numberTest += 1 
        # Step 6: Check if values from the request have been taken over
        # Check NVM mirror which is copied at startup from the NVM
        # format: convert values to 2 digit hex values
        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[10]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange[11]")['vvalue'].value, '02x')
    
        nvmMirrorString = str(nvmMirrorFirstValue) + str(nvmMirrorSecondValue) 
    
        #numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  #constant.CONST_DIAG_USER_CONFIGURED_DOIP_ADDR_HEX, "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  readfbldoip, "g_NvMRamMirrorFblDynamicNetworkConfigFblExchange")
        # change DoIP Settings in CANoe DoIP Diag Tester Tab
        # int(value in hex, 16) converts that value to 4 digit decimal value (i.e. 1396 is interpreted as hex and thus converted to 5014)
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", int(constant.CONST_DIAG_USER_CONFIGURED_DOIP_ADDR_HEX, 16))
    
        # Step 7: Cleanup
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_DOIP_ADDR + \
            constant.CONST_DIAG_INITIAL_BCT_DOIP_ADDR + constant.CONST_DIAG_DOIP_DUMMY

        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change DoIP address service with initially in BCT configured DoIP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
    
        # change DoIP Settings back in CANoe DoIP Diag Tester Tab
        # format: convert values to 4 digit decimal values
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", int(constant.CONST_DIAG_INITIAL_BCT_DOIP_ADDR, 16))
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if after the jump from Flashbootloader to Application Software the reset reason flag is reset to zero (RB_RESET_REASON_NOTHING).
    #   It also checks if the value is different to the value from the jump to Flashbootloader to make sure that the flag has been reset and has not always been zero.
    #  @swtest_step
    #   1. Send Tester Present and jump to Programming Session. Save the value of the reset reason while jumping to FBL.
    #   2. Jump back to Application Software via Jump to Default Session Service. Save the value of the reset reason after jumping back to Application.
    #   3. Compare the two values from Step 1 and 2 and check if they are not equal. Also check that the value from step 2.
    #   4. Repeat steps 1-3 just with sending ECU Reset in Step 2 instead of Jump to Default Session
    #   5. Cleanup.
    #  @swtest_expResult Value from Step 2 should be equals to zero (RB_RESET_REASON_NOTHING). Values from Step 1 and Step 2 should be different.
    #  @sw_requirement{SDC-R_SW_DIMA_554, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-554-00159bc2?doors.view=0000000b}
    def swTest_checkJumpFromFblResetReasonPacket(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: Jump to Programming Session.
        # Send Tester Present cyclically because otherwise after 5 seconds control will be transfered back to application (S3 Timeout)
        canoeDiagPanel.sendCyclicTesterPresent(self.canoe_api, self.logger)
    
        # Jump to Programming Session. Don't use the function jumpToProgrammingSession as this includes a time.sleep(self) to wait until jump to 
        # Programming Session is done. In this case we want to check the Reset Reason flag without waiting until we are if self.hw == 'nr5cp': in the Flashbootloader.
        lauterbachTestHelper.setSystemModeNoDebug(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        time.sleep(1)
        canoeDiagPanel.reestablishLostDiagTConnection(self.canoe_api, self.logger)
        RestReason=self.canoe_api.EnvVarButton("Env_DoipProgSession_AutoIP") 
        self.logger.debug(f"Step 1: Rest Reason: {RestReason}")
        lauterbachTestHelper.setSystemModeAttach(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        nvmMirrorValueJumpToBoot = t32_api.get_variable_value("g_NvMRamMirrorResetReasonFblDataItem[0]")['vvalue'].value
        self.logger.debug(f"Step 3: Rest Reason: {nvmMirrorValueJumpToBoot}")
		
        # Step 2: Jump back to Application Software (via Diagnostic Session Control: Default Session service)
        canoeDiagPanel.jumpToDefaultSessionFromProgramming(self.canoe_api, self.t32_api, self.logger)
		
        nvmMirrorValueJumpToAppl = t32_api.get_variable_value("g_NvMRamMirrorResetReasonFblDataItem[0]")['vvalue'].value
        self.logger.debug(f"Step 2: Rest Reason: {nvmMirrorValueJumpToAppl}")
		
        # Step 3: Compare the values from step 1 and 2 and check if value from step 2 is equal to 0
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValueJumpToAppl, 
                            constant.CONST_DIAG_RESET_REASON_NOTHING, "Check g_NvMRamMirrorResetReasonFblDataItem")
        numberTest += 1
        self.logger.debug(f"Step 3: Rest Reason: {nvmMirrorValueJumpToBoot}")
        numberFailedTests += testasserts.TEST_NOT_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValueJumpToBoot, 
                            nvmMirrorValueJumpToAppl, "Check if first and second value of NvM_diaFbl_ResetReason are not equal")
        numberTest += 1
        
        # Step 4: Repeat steps 1-3 just with sending ECU Reset in Step 2 instead of Jump to Default Session
    
        # Jump to Programming Session. Don't use the function jumpToProgrammingSession as this includes a time.sleep(self) to wait until jump to 
        # Programming Session is done. In this case we want to check the Reset Reason flag without waiting until we are in the Flashbootloader.
        lauterbachTestHelper.setSystemModeNoDebug(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        time.sleep(1)
        canoeDiagPanel.reestablishLostDiagTConnection(self.canoe_api, self.logger)
        RestReason=self.canoe_api.EnvVarButton("Env_DoipProgSession_AutoIP") 
		
        lauterbachTestHelper.setSystemModeAttach(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        nvmMirrorValueJumpToBoot = t32_api.get_variable_value("g_NvMRamMirrorResetReasonFblDataItem[0]")['vvalue'].value
    
        # Jump back to Application Software (via ECU Hard Reset service
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3)
        nvmMirrorValueJumpToAppl = t32_api.get_variable_value("g_NvMRamMirrorResetReasonFblDataItem[0]")['vvalue'].value
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValueJumpToAppl, 
                            constant.CONST_DIAG_RESET_REASON_NOTHING, "Check g_NvMRamMirrorResetReasonFblDataItem")
        numberTest += 1
        numberFailedTests += testasserts.TEST_NOT_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValueJumpToBoot, 
                            nvmMirrorValueJumpToAppl, "Check if first and second value of g_NvMRamMirrorResetReasonFblDataItem are not equal")
    
        # Step 5: Cleanup. Stop sending tester presents
        canoeDiagPanel.stopCyclicTesterPresent(self.canoe_api, self.logger)
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if the application software is sending a "Request Correctly Received - Response Pending" NRC when calling the jump to
    #    Flashbootloader service (0x10 02).
    #  @swtest_step
    #   1. Send Tester Present and jump to Programming Session. 
    #   2. Check if "ResponsePending" has been sent by Application Software to the Rest Bus Simulation.
    #   3. Cleanup.
    #  @swtest_expResult Value read from Receive Panel in Rest Bus Simulation in Step 2 should be equal to the referenced constant value.
    #  @sw_requirement{SDC-R_SW_DIMA_638, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-638-00159bc2?doors.view=0000000b}
    def swTest_checkJumpToFblResponsePending(self, t32_api):
        numberFailedTests = 0
        numberTest = 1    
    
        # Step 1: Jump to Programming Session.
        # Send Tester Present cyclically because otherwise after 5 seconds control will be transfered back to application (S3 Timeout)
        canoeDiagPanel.sendCyclicTesterPresent(self.canoe_api, self.logger)
    
        # Jump to Programming Session. Don't use the function jumpToProgrammingSession as this includes a time.sleep(self) to wait until jump to 
        # Programming Session is done. In this case we want to check the "ResponsePending" sent by the Application Software without waiting until 
        # we are in the Flashbootloader.
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        lauterbachTestHelper.setSystemModeNoDebug(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        time.sleep(1)
        canoeDiagPanel.reestablishLostDiagTConnection(self.canoe_api, self.logger)
        AutoIP=self.canoe_api.EnvVarButton("Env_DoipProgSession_AutoIP")
		
        
        # Step 2: Check if "ResponsePending" has been sent by Application Software to the RBS. 
        # retrieve diagnostic response value from RBS
        doipDiagResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(2)
        self.logger.debug(f"Step 1: doipDiagResponses : {doipDiagResponse}")
        
        # Compare diagnostic response from RBS with constant.
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, doipDiagResponse, 
                            constant.CONST_DIAG_DSC_RESPONSE_PENDING, "Check Jump to FBL Response Pending")
    
        # Step 3: Cleanup: Attach Debugger and jump back to Default Session. 
        canoeDiagPanel.jumpToDefaultSessionFromProgramming(self.canoe_api, self.t32_api, self.logger)
    
        # Stop Sending Tester Presents and attach debugger.   
        canoeDiagPanel.stopCyclicTesterPresent(self.canoe_api, self.logger)
        lauterbachTestHelper.setSystemModeAttach(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description This test case checks that the ECU does not accept further DCM requests as soon as a jump to FBL or an ECU Reset Service is called 
    #   until the reset is being executed.
    #  @swtest_step
    #   1. Jump to Programming Session and read out value of the global DCM flag which indicates if DCM accepts requests or not.
    #   2. Check if the flag is set to FALSE.
    #   3. Jump back to Default Session. Repeat steps 1 and 2 for the ECU Reset service instead of Jump to Programming Session
    #   4. Cleanup
    #  @swtest_expResult DCM Accept Requests Flag should be FALSE after "Jump to Programming Session" or "ECU Reset" service is called
    #  @sw_requirement{SDC-R_SW_DIMA_701, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-701-00159bc2?doors.view=0000000b}
    def swTest_checkEcuResetHandlerDenyDcmRequests(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        # Step 1: Jump to Programming Session. 
        # Jump to Programming Session. Don't use the function jumpToProgrammingSession as this includes a time.sleep(self) to wait until jump to 
        # Programming Session is done. In this case we want to check that after the request is sent no further DCM Requests are answered
        # Send Tester Present cyclically because otherwise after 5 seconds control will be transfered back to application (S3 Timeout)
        canoeDiagPanel.sendCyclicTesterPresent(self.canoe_api, self.logger)
        lauterbachTestHelper.setSystemModeNoDebug(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        canoeDiagPanel.reestablishLostDiagTConnection(self.canoe_api, self.logger)
        self.canoe_api.EnvVarButton("Env_DoipProgSession_AutoIP") 
        # attach Debugger
        lauterbachTestHelper.setSystemModeAttach(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        # Read global DCM flag
        dcmRequestAcceptanceFlag = t32_api.get_variable_value("Dcm_acceptRequests_b")['vvalue'].value 
    
        # Step 2: Check if flag is FALSE 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dcmRequestAcceptanceFlag, 
                            0, "Check if DCM_acceptRequests_b flag is set to FALSE")
        numberTest += 1
    
        # Step 3: Jump back to Default Session and repeat steps 1 and 2 for ECU Reset service
        canoeDiagPanel.jumpToDefaultSessionFromProgramming(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)
    
        # Stop Sending Tester Presents (only required as long as we have control in FBL).   
        canoeDiagPanel.stopCyclicTesterPresent(self.canoe_api, self.logger)
        lauterbachTestHelper.setSystemModeNoDebug(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        canoeDiagPanel.reestablishLostDiagTConnection(self.canoe_api, self.logger)
        self.canoe_api.EnvVarButton("Env_DoipEcuHardRest_AutoIP") 
    
        # attach debugger and read Dcm_acceptRequests_b value
        lauterbachTestHelper.setSystemModeAttach(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        dcmRequestAcceptanceFlag = t32_api.get_variable_value("Dcm_acceptRequests_b")['vvalue'].value
    
        # Check if flag is FALSE 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dcmRequestAcceptanceFlag, 
                            0, "Check if DCM_acceptRequests_b flag is set to FALSE")
    
        # Step 4: Cleanup
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description This test case checks that the ECU closes the connection to the Diagnostic Tester as soon as a jump to FBL or an  
    #   ECU Reset Service is called.
    #  @swtest_step
    #   1. Jump to Programming Session and read out value of the global DoIP Activation Line flag. 
    #   2. Check if the flag is set to FALSE.
    #   3. Jump back to Default Session. Repeat steps 1 and 2 for the ECU Reset service instead of Jump to Programming Session
    #   4. Cleanup
    #  @swtest_expResult DCM Accept Requests Flag should be FALSE after "Jump to Programming Session" or "ECU Reset" service is called
    #  @sw_requirement{SDC-R_SW_DIMA_702, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-702-00159bc2?doors.view=0000000b}
    def swTest_checkCloseConnectionToDiagTester(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: Jump to Programming Session. 
        # Don't use the function jumpToProgrammingSession as this includes a time.sleep() to wait until jump to 
        # Programming Session is done. In this case we want to check that the connection to the Diagnostic Tester is closed which would not
        # be possible if we wait for the delay implemented in jumpToProgrammingSession function 
        # Send Tester Present cyclically because otherwise after 5 seconds control will be transfered back to application (S3 Timeout)
        canoeDiagPanel.sendCyclicTesterPresent(self.canoe_api, self.logger)
        lauterbachTestHelper.setSystemModeNoDebug(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        canoeDiagPanel.reestablishLostDiagTConnection(self.canoe_api, self.logger)
        self.canoe_api.EnvVarButton("Env_DoipProgSession_AutoIP") 
        # attach Debugger
        lauterbachTestHelper.setSystemModeAttach(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        # read global DoIP activation line status
        doipActivationLineStatus = t32_api.get_variable_value("DoIP_ActivationLineStatus_u8")['vvalue'].value 
        
        # Step 2: Check if status flag is FALSE 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, doipActivationLineStatus, 
                            0, "Check if DoIP_ActivationLineStatus_u8 flag is set to FALSE")
        numberTest += 1
    
        # Step 3: Jump back to Default Session and repeat steps 1 and 2 for ECU Reset service
        canoeDiagPanel.jumpToDefaultSessionFromProgramming(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)
    
        # Stop Sending Tester Presents.   
        canoeDiagPanel.stopCyclicTesterPresent(self.canoe_api, self.logger)
        lauterbachTestHelper.setSystemModeNoDebug(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        canoeDiagPanel.reestablishLostDiagTConnection(self.canoe_api, self.logger)
        self.canoe_api.EnvVarButton("Env_DoipEcuHardRest_AutoIP") 
    
        # attach debugger and read DoIP_ActivationLineStatus_u8 value
        lauterbachTestHelper.setSystemModeAttach(self.t32_api[globalConstants.k_atf_hardwareLrrUc2], self.logger, globalConstants.k_atf_hardwareLrrUc2)
        doipActivationLineStatus = t32_api.get_variable_value("DoIP_ActivationLineStatus_u8")['vvalue'].value
    
        # Check if flag is FALSE 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, doipActivationLineStatus, 
                            0, "Check if DoIP_ActivationLineStatus_u8 flag is set to FALSE")
    
        # Step 4: Cleanup
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
    
        return CTestCaseResult(numberTest, numberFailedTests)
        
     
