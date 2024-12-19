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
import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants
import diag_testsuitebasic as diagbasic
from testbase import CTestCaseResult
import AD_lauterbach_test_helper as lauterbachTestHelper

# DTC values
k_dtcSENSOR_RADAR_MODULATION = "510022"

# positive response: 59020d, DTC: 510022, status: 0d
k_modulationDtcbyStatusResponse = diagbasic.k_diagReadDtcbyStatusMaskPositiveResponse + diagbasic.k_diagReadDtcInformationStatus + k_dtcSENSOR_RADAR_MODULATION +diagbasic.k_diagReadDtcInformationStatus


class CTestSuiteDiagVariantHandling(testsuite.CTestSuite, CTestRunner):
    
    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteDiagVariantHandling"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, self.getComponentName())

         
    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no Diag test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllDiagVarHdlTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])       

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "diag_variant"
                 
    def runAllDiagVarHdlTests(self, t32_api):   
        # jump to Default Session as precondition for diag tests
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
            
        # Caution: Function name in local filter has to be test case name which should be executed     
        localFilterList = (
            "swTest_checkMacIsWrittenToNvm; swTest_checkMacRead; swTest_checkResetMacAddressToBctConfig; swTest_checkDoIpIsWrittenToNvm;"
            "swTest_checkDoIPAddrRead; swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange1; swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange2;"
            "swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange3; swTest_LGPSrcFromNVMandLGPDestandDIAGFromBCTIsWrittenToNvm;"
            "swTest_PreviousUsedLGPSrcandLGPDestFromBCTIsWrittenToNvm; swTest_LGPSrcFromBCTandLGPDestFromNVMIsWrittenToNvm; swTest_LGPSrcFromBCTandPreviousUsedLGPDestIsWrittenToNvm;"
            "swTest_PreviousUsedLGPSrcandLGPDestFromNVMIsWrittenToNvmForGivenRange1; swTest_PreviousUsedLGPSrcandLGPDestFromNVMIsWrittenToNvmForGivenRange2;"
            "swTest_LGPSrcFromNVMandPreviousUsedLGPDestIsWrittenToNvmForGivenRange1; swTest_LGPSrcFromNVMandPreviousUsedLGPDestIsWrittenToNvmForGivenRange2;"
            "swTest_PreviousUsedLGPSrcLGPDestandDiagIsWrittenToNvm; swTest_PreviousUsedLGPSrcandLGPDestIsWrittenToNvm; swTest_InvalidMaxLGPSrcForGivenRange1;"
            "swTest_InvalidMaxLGPSrcForGivenRange2; swTest_InvalidMaxLGPSrcForGivenRange3; swTest_InvalidMinLGPSrcForGivenRange1; swTest_InvalidMinLGPSrcForGivenRange2;"
            "swTest_InvalidMinLGPSrcForGivenRange3; swTest_InvalidMaxLGPDestForGivenRange1; swTest_InvalidMaxLGPDestForGivenRange2; swTest_InvalidMaxLGPDestForGivenRange3;"       
            "swTest_InvalidMinLGPDestForGivenRange1; swTest_InvalidMinLGPDestForGivenRange2; swTest_InvalidMinLGPDestForGivenRange3; swTest_InvalidsecondbyteLGPDestForGivenMaxRange2;"
            "swTest_InvalidsecondbyteLGPDestForGivenMinRange2; swTest_InvalidsecondbyteLGPDestForGivenRange3; swTest_InvalidsecondbyteLGPSrcForGivenMaxRange2;"
            "swTest_InvalidsecondbyteLGPSrcForGivenMinRange2; swTest_InvalidsecondbyteLGPSrcForGivenRange3;"
            "swTest_reportNRC_requestchangeLGPSrcandusepreviuosconfigforLGPDest; swTest_reportNRC_requestchangeLGPSrcandusepredefinedvaluesforLGPDest;"
            "swTest_reportNRC_requestchangeLGPDestandusepreviuosconfigforLGPSrc; swTest_reportNRC_requestchangeLGPDestandusepredefinedvaluesforLGPSrc;"
            "swTest_InvalidLGPSrcandLGPDestisDifferentRange; swTest_InvalidLGPSrcandLGPDestisEqual; swTest_InvalidFirstByteDiag;"
            "swTest_InvalidSecondByteDiag; swTest_InvalidMinDiag; swTest_InvalidMaxDiag; swTest_checkIPAddrRead; swTest_checkDestinationPortIsWrittenToNvm;"
            "swTest_InvalidMinDestinationPort; swTest_InvalidMaxDestinationPort; swTest_ReadDestinationPort; swTest_storeDestIpNvmRange5NoChangeSource;"
            "swTest_reportNrcDestIpRange5SourceIpOther; swTest_checkModulationControlDefaultvalue; swTest_checkModulationControlvalue_startModulation; swTest_checkModulationControlvalue_stopModulation;"
            "swTest_checkModulationControlvalue_requestoutofrange;swTest_checkMACAddress_requestoutofrange") 
          
        # We need the filter function by user, because some test cases are generic and nested into parameterized function.        
        numberFailedTests = self.executeFilteredFunctionUser(t32_api, localFilterList) 

        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)
    
    ## @swtest_description The test case checks if calling the "Change MAC address" diagnostic service with an NVM Flag = 1 writes the MAC Address from the request.
    #   into the NVM packet at the end reset MAC address to BCT config MAC Adress
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03) and send "Change MAC Address" service with an NVM Flag set to 1. Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet rbDia_mac_Address_Data_au8
    #  @swtest_expResult The NVM mirror value is equal to the address which has been sent in the request.
    #  @sw_requirement{SDC-R_SW_DIMA_73,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-73-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_75,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-75-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_77,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-77-00159bc2?doors.view=0000000b}
    def swTest_checkMacIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        #Step 1: send change MAC address service with NVM Flag2 = 1 and different MAC address than the BCT configured one (e.g. 4C:DE:16:01:10:56)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)   
        #2E06014CDE160110560001
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_RES_MAC_NVN_DATA, self.logger)
        writeMacResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Write MAC to NVM: {writeMacResponse}")        
        #lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        #time.sleep(1)    
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeMacResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MAC, "Step :Check WDBI  Mac - response")      
        numberTest += 1
   
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        #Step 3.Read Mac port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_MAC, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        macvaluenvm               = Read_DID[6:18]
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MAC, readResponseStatus,
                                                 "Step 4:Check RBDI MAC - response")
        numberTest += 1 

        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[4]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[5]")['vvalue'].value, '02x')
        nvmMirrorThirdValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[6]")['vvalue'].value, '02x')
        nvmMirrorFourthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[7]")['vvalue'].value, '02x')
        nvmMirrorFifthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[8]")['vvalue'].value, '02x')
        nvmMirrorSixthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[9]")['vvalue'].value, '02x')
               
        nvmMirrorString = str(nvmMirrorFirstValue) + str(nvmMirrorSecondValue) + str(nvmMirrorThirdValue) + str(nvmMirrorFourthValue) + str(nvmMirrorFifthValue) +  str(nvmMirrorSixthValue)
                                                  
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  macvaluenvm, "Check g_NvMRamMirrorMACAddressNVMDataItem")
        numberTest += 1
        
        # Step 6: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change MAC address service with NVM Flag = 0 --> go back to BCT configured IP Address
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E06018834FE0000010000", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_BCT_MAC_NVM_DATA, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)      
        
        return CTestCaseResult(numberTest, numberFailedTests)
    
        
    ## @swtest_description The test case Reads mac address from NVM or BCT through diagnostic read service with DID 
    #  @swtest_step
    #   1. Checks NVM flag if it is zero update expected data with bct mac address else update RAM mirror values to expected
    #   2. Jump to Default Session (0x10 01) and send "Read MAC Address" service . Reads the values.
    #   3. Check the Expected and actual values
    #  @swtest_expResult Expected and actual read value should match.
    #  @sw_requirement{SDC-R_SW_DIMA_73,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-73-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_74,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-74-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_76,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-76-00159bc2?doors.view=0000000b}
    def swTest_checkMacRead(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
            
        # Step 1: Check if values from the request have been taken over
        # Check NVM mirror which is copied at startup from the NVM
        # format: convert values to 2 digit hex values
        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[4]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[5]")['vvalue'].value, '02x')
        nvmMirrorThirdValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[6]")['vvalue'].value, '02x')
        nvmMirrorFourthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[7]")['vvalue'].value, '02x')
        nvmMirrorFifthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[8]")['vvalue'].value, '02x')
        nvmMirrorSixthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[9]")['vvalue'].value, '02x')
    
        # read nvm flag as string
        macNvmFlag = str(format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[11]")['vvalue'].value, '02x'))
    
        # Step2 checks NVM flag is zero or one
        if macNvmFlag == constant.CONST_DIAG_NVM_FLAG_READ_INITIAL_BCT_VALUES:
            ExpectedData = constant.CONST_DIAG_UDS_SERVICE_RDBI_POS_RESP + constant.CONST_DIAG_UDS_SUBSERVICE_MAC_ADDR + \
                            testHelper.removeColons(constant.CONST_DIAG_INITIAL_BCT_MAC_ADDR) + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA + \
                                constant.CONST_DIAG_NVM_FLAG_READ_INITIAL_BCT_VALUES
        else :
            ExpectedData = constant.CONST_DIAG_UDS_SERVICE_RDBI_POS_RESP + constant.CONST_DIAG_UDS_SUBSERVICE_MAC_ADDR + \
                str(nvmMirrorFirstValue)  + str(nvmMirrorSecondValue) +  str(nvmMirrorThirdValue) + str(nvmMirrorFourthValue) +  \
                    str(nvmMirrorFifthValue) + str(nvmMirrorSixthValue) + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA + constant.CONST_DIAG_NVM_FLAG_READ_VALUES_FROM_NVM
        
        # Step 3:send read diagnostic service to read MAC Address
        serviceRequestString = constant.CONST_DIAG_UDS_SERVICE_RDBI + constant.CONST_DIAG_UDS_SUBSERVICE_MAC_ADDR
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug("f step 1: diagnostic service to read MAC :{Read_DID}")
        time.sleep(2)
        
        readResponseStatus        = Read_DID[0:6]
        self.logger.debug(f"Step 1: READ MAC : {readResponseStatus}")
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MAC, readResponseStatus,
                                                 "Step 4:Check RBDI read MAC - response")
        numberTest += 1
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Check Mac data")
    
        return CTestCaseResult(numberTest, numberFailedTests)
        
    ## @swtest_description The test case checks if calling the "Change MAC address" diagnostic service with an NVM Flag = 0 writes the BCT configured MAC Address from the request
    #   into the NVM packet which is used to provide the MAC address to the other component.
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03) and send "Change MAC Address" service with an NVM Flag set to 0. Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet rbDia_mac_Address_Data_au8
    #  @swtest_expResult The NVM mirror value is equal to the address which has been sent in the request.
    #  @sw_requirement{SDC-R_SW_DIMA_73,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-73-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_75,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-75-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_77,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-77-00159bc2?doors.view=0000000b}
    def swTest_checkResetMacAddressToBctConfig(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change MAC address service with NVM Flag =0 and different MAC address than the BCT configured one (e.g. 88:34:FE:00:00:01)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E06018834FE0000010000", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_RESET_WRITE_MAC_TO_BCT , self.logger)
        resetMacResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Write MAC to NVM: {resetMacResponse}")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3)
        
         #Step 2. Validate Reset response -> positive response
        resetResponseStatus = resetMacResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, resetResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MAC, "Step :Check WDBI  Mac - response")      
        numberTest += 1
        
        #Step 3.Read Mac port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_MAC, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 2: READ MAC : {Read_DID}")        
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        self.logger.debug(f"Step 3: READ MAC : {readResponseStatus}")
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MAC, readResponseStatus,
                                                 "Step 4:Check RBDI destination port - response")
        numberTest += 1
    
        # Step 4: Check if values from the request have been taken over
        # Check NVM mirror which is copied at startup from the NVM
        # format: convert values to 2 digit hex values
        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[4]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[5]")['vvalue'].value, '02x')
        nvmMirrorThirdValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[6]")['vvalue'].value, '02x')
        nvmMirrorFourthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[7]")['vvalue'].value, '02x')
        nvmMirrorFifthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[8]")['vvalue'].value, '02x')
        nvmMirrorSixthValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorMACAddressNVMDataItem[9]")['vvalue'].value, '02x')
    
        nvmMirrorString = str(nvmMirrorFirstValue) + ":" + str(nvmMirrorSecondValue) + ":" + str(nvmMirrorThirdValue) + \
            ":" + str(nvmMirrorFourthValue) + ":" + str(nvmMirrorFifthValue) + ":" + str(nvmMirrorSixthValue)
        self.logger.debug(f"Step 4: Check Reset MAC TO BCT: {nvmMirrorString}")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  constant.CONST_DIAG_INITIAL_BCT_MAC_ADDR, "Check g_NvMRamMirrorMACAddressNVMDataItem")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case checks if calling the "Change DoIP address" diagnostic service writes the DoIP Address from the request into the NVM 
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03) and send "Change DoIP Address" service. Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet rbDia_Doip_Address_Data_au8
    #  @swtest_expResult The NVM mirror value is equal to the address which has been sent in the request.
    #  @sw_requirement{SDC-R_SW_DIMA_79,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-79-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_81,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-81-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_83,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-83-00159bc2?doors.view=0000000b}
    def swTest_checkDoIpIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change DoIP address service with a different DoIP address than the BCT configured one 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E06021256000000000000", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DOIP_WRITE_TO_NVM , self.logger)
        writeDOIPResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Write DOIP to NVM: {writeDOIPResponse}")
              
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeDOIPResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_DOIP, "Step :Check WDBI  Doip - response")      
        numberTest += 1
         
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        # change DoIP Settings in CANoe DoIP Diag Tester Tab
        # format: convert values to 4 digit decimal values
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0x1256, '04d'))
        
        #Step 3.Read Doip port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_DOIP, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        self.logger.debug(f"Step 2: READ DIOP : {Read_DID}")        
        time.sleep(0.5)
        
        readResponseStatus        = Read_DID[0:6]
        readnvmdoip               = Read_DID[6:10]
        self.logger.debug(f"Step 3: Read Doip : {readnvmdoip}")
        #Step 4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_DOIP, readResponseStatus,
                                                 "Step 4:Check RBDI Doip - response")
        numberTest += 1 
    
        # Step 5: Check if values from the request have been taken over
        # Check NVM mirror which is copied at startup from the NVM
        # format: convert values to 2 digit hex values
        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorDOIPAddressNVMDataItem[4]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorDOIPAddressNVMDataItem[5]")['vvalue'].value, '02x')
    
        nvmMirrorString = str(nvmMirrorFirstValue) + str(nvmMirrorSecondValue) 
        self.logger.debug(f"Step 4: Check DOIP writen to NVM: {nvmMirrorString}")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  constant.CONST_DIAG_USER_CONFIGURED_DOIP_ADDR1_HEX, "Check g_NvMRamMirrorDOIPAddressNVMDataItem")
        numberTest += 1  
         
        # change DoIP Settings in CANoe DoIP Diag Tester Tab
        # format: convert values to 4 digit decimal values
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0x1256, '04d'))
    
        # Step 6: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change DoIP address service with initially in BCT configured DoIP Address
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E06021295000000000000", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DOIP_BCT_TO_NVM, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(2)
        # change DoIP Settings back in CANoe DoIP Diag Tester Tab
        # format: convert values to 4 digit decimal values
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0x1295, '04d'))
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case Reads Doip address from NVM 
    #   1. Jump to Default Session (0x10 01) and send "Read DOIP Address" service . Reads the values.
    #   2. Check the Expected and actual values
    #  @swtest_expResult Expected and actual read value should match.
    #  @sw_requirement{SDC-R_SW_DIMA_79,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-79-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_80,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-80-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_82,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-82-00159bc2?doors.view=0000000b}
    def swTest_checkDoIPAddrRead(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: Check if values from the request have been taken over
        # Check NVM mirror which is copied at startup from the NVM
        # format: convert values to 2 digit hex values
        nvmMirrorFirstValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorDOIPAddressNVMDataItem[4]")['vvalue'].value, '02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value(
            "g_NvMRamMirrorDOIPAddressNVMDataItem[5]")['vvalue'].value, '02x')
        
        DOIPAddr = nvmMirrorFirstValue + nvmMirrorSecondValue
        
        if DOIPAddr == constant.CONST_DIAG_DOIP_NVM_NOT_CONFIGURED:
            DOIPAddr = constant.CONST_DIAG_INITIAL_BCT_DOIP_ADDR
        else:
            DOIPAddr = DOIPAddr
    
        #Read response        
        ExpectedData = constant.CONST_DIAG_UDS_SERVICE_RDBI_POS_RESP + constant.CONST_DIAG_UDS_SUBSERVICE_DOIP_ADDR + \
            str(DOIPAddr)+ constant.CONST_DIAG_DOIP_DUMMY
    
        # Step 2:send read diagnostic service to read DOIP Address
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220602", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_SERVICE_RDBI+constant.CONST_DIAG_UDS_SUBSERVICE_DOIP_ADDR, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug("f step 1 : Read DOIP DID :{Read_DID}")
        time.sleep(2)
        
        readResponseStatus        = Read_DID[0:6]
        self.logger.debug(f"Step 1: Read Doip : {readResponseStatus}")
        #Step 3. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_DOIP, readResponseStatus,
                                                 "Step 4:Check RBDI Doip - response")
        numberTest += 1 
                      
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Check DOIP address")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    

    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #     This test case writes valid IP Addresses with the passed range for LGP Src and Dest to NVM RAM With NVM flag 1 and Valid IP addess for Diag to NVM RAM with NVM flag 1
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   2. Check if  LGP Src IP Address have been written to the NVM
    #   3. Check if LGP Dest IP Address have been written to the NVM
    #   4.Check if Diag IP Address have been written to the NVM
    #   5.Cleanup
    #  @swtest_expResult The NVM mirror value is equal to the address which has been User Configured.
    #  @sw_requirement{SDC-R_SW_DIMA_607,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-607-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_677, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-677-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_749 ,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-749-00159bc2?doors.view=0000000bNo} 
    #  @sw_requirement{SDC-R_SW_DIMA_764,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-764-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_767, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-767-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_758,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-758-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_673,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-673-00159bc2?doors.view=00000004}
    def swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange(self, t32_api, range, request, lgpSrcAddr, lgpDestAddr, diagAddr):
        numberFailedTests = 0
        numberTest = 1
        
        # Step 1: send change IP address service with NVM Flag = 1 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, request, self.logger)
       
        writeIPResponse=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Write IP to NVM: {writeIPResponse}")		
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeIPResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_IP_RES, "Step :Check WDBI  ip - response")      
        numberTest += 1
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(2)
        
        Read_Doip=self.canoe_api.getEnvVar("Env_Doip_ECU_IP")  
        
        #set canoe variable 
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1","lgpDestAddr")
        self.canoe_api.setSysVarValue("ROS_LGP_Server","ServerIP_1","lgpSrcAddr")
        self.canoe_api.setEnvVar("Env_Doip_ECU_IP",diagAddr)
        self.logger.debug(f"Step 3: diaaddress : {diagAddr}")
                   
        # Step 3: Check if  LGP Src IP Address have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[4]")['vvalue'].value
        nvmMirrorSecondValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[5]")['vvalue'].value
        nvmMirrorThirdValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[6]")['vvalue'].value
        nvmMirrorFourthValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[7]")['vvalue'].value
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  lgpSrcAddr, "Check g_NvMRamMirrorIPAddressNVMDataItem")
        numberTest += 1
    
        # Step 4: Check if LGP Dest IP Address have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[9]")['vvalue'].value
        nvmMirrorSecondValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[10]")['vvalue'].value
        nvmMirrorThirdValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[11]")['vvalue'].value
        nvmMirrorFourthValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[12]")['vvalue'].value
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  lgpDestAddr, "Check g_NvMRamMirrorIPAddressNVMDataItem")
        numberTest += 1
    
        # Step 5: Check if Diag IP Address have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[14]")['vvalue'].value
        nvmMirrorSecondValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[15]")['vvalue'].value
        nvmMirrorThirdValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[16]")['vvalue'].value
        nvmMirrorFourthValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[17]")['vvalue'].value
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
        self.logger.debug(f"Step 2: nvmMirrorString : {nvmMirrorString}")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  diagAddr, "Check g_NvMRamMirrorIPAddressNVMDataItem")
    
        #Step 6: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1",constant.CONST_LGP_DST_DEFAULT)
        self.canoe_api.setSysVarValue("ROS_LGP_Server","ServerIP_1",constant.CONST_LGP_SRC_DEFAULT)
        self.canoe_api.setEnvVar("Env_Doip_ECU_IP",constant.CONST_BCT_DEFAULT_VALUE)
        
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        return CTestCaseResult(numberTest, numberFailedTests)


    def swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange1(self, t32_api):
        return self.swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange(t32_api, "1",constant.CONST_LGPSRC_RANGE,  constant.CONST_LGP_SRC_RANGE1_IP, 
                                                                                    constant.CONST_LGP_DST_RANGE1_IP, constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR3)

    #2E0600AC13708001AC19223801A9FE559B0100
    def swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange2(self, t32_api):
        return self.swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange(t32_api, "2",constant.CONST_LGPDST_RANGE2, constant.CONST_LGP_SRC_RANGE2_IP, 
                                                                                    constant.CONST_LGP_DST_RANGE2_IP, constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR4)

    #"2E0600C0A8038601C0A8675301A9FE74640100"
    def swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange3(self, t32_api):
        return self.swTest_LGPSrcandLGPDestandDiagFromNVMIsWrittenToNvmForGivenRange(t32_api, "3",constant.CONST_LGPSRC_RANGE3, constant.CONST_LGP_SRC_RANGE3_IP, 
                                                                                    constant.CONST_LGP_DST_RANGE3_IP, constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR5)


    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case writes valid range3 IP Address for LGP Src to NVM RAM With NVM flag 1 ,LGP Dest and Diag use BCT configured as NVM flag is 0
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   2. Check if  LGP Src IP Address have been written to the NVM
    #   3. As nvm flag is 0 for LGP Dest so read through read service and check if it is equal to BCT config or not
    #   4. Cleanup
    #  @swtest_expResult The NVM mirror value is equal to the address which has been User Configured for LGP src.
    #  @swtest_expResult The LGP dest should be BCT configured.
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_607,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-607-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_677, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-677-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_764, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-764-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_768, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-768-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_674, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-674-00159bc2?doors.view=00000004}
    def swTest_LGPSrcFromNVMandLGPDestandDIAGFromBCTIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Source service with NVM Flag = 1
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A8068401C0A8675300A9FE74640000
        
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_LGPSRC_BCT_LGPDST , self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_LGPSRC_BCT , self.logger)
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3)
        #canoe update for LGP_SRC
        self.canoe_api.setSysVarValue("ROS_LGP_Server","ServerIP_1",constant.CONST_LGP_SRC_RANGE3_IP1)
        
        # Step 2: Check if  LGP Src IP Address have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[4]")['vvalue'].value
        nvmMirrorSecondValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[5]")['vvalue'].value
        nvmMirrorThirdValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[6]")['vvalue'].value
        nvmMirrorFourthValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[7]")['vvalue'].value
        
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  constant.CONST_LGP_SRC_RANGE3_IP1, "Check g_NvMRamMirrorIPAddressNVMDataItem")
        numberTest += 1
       
        # Step 3:As nvm flag is 0 for LGP Dest so read through read service and check if it is equal to BCT config or not
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_DEST_IP_ADDR = Read_DID[16:24]
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_DEST_INITIAL_BCT_IP_ADDR_HEX,
                                                  LGP_DEST_IP_ADDR, "Check LGP Dest IP Addr")
        numberTest += 1
        
        DIAG = Read_DID[26:34]
        #Check actual and expected are same or not for DIAG
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_DIAG_INITIAL_BCT_IP_ADDR_HEX,
                                                 DIAG, "Check read DIAG")
    

        #Step 4: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        self.canoe_api.setSysVarValue("ROS_LGP_Server","ServerIP_1",constant.CONST_LGP_SRC_DEFAULT)
        #self.canoe_api.setEnvVar("Env_Doip_ECU_IP",constant.CONST_LGP_SRC_DEFAULT)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #     This test case checks previous used LGP Src IP address as NVM flag is 2,LGP Dest and Diag use BCT configured as NVM flag is 0
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   2. As NVM flag is 2 for LGP Src(it will use previous config) and 0 for LGP Dest.Read both IP address Through read service and check if it is with in expected or not
    #   3. Check actual and expected are same or not for LGP Src IP Address
    #   4. Check actual and expected are same or not for LGP Dest IP Address
    #   5. Cleanup
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_607,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-607-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_677, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-677-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_766, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-766-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_768, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-768-00159bc2?doors.view=00000004}
    def swTest_PreviousUsedLGPSrcandLGPDestFromBCTIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Source service with NVM Flag = 1
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A8068402C0A8675300A9FE74640000
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_LGPDST , self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3)
        # Step 2:As NVM flag is 2 for LGP Src(it will use previous config) and 0 for LGP Dest.Read both IP address and check if it is with in expected or not
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)
         
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        #extracting Src and Dest IP Address
        LGP_SRC = Read_DID[6:14]
        LGP_DEST = Read_DID[16:24]
    
        # Step 3:Check actual and expected are same or not for LGP Src IP Address
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_SRC_INITIAL_BCT_IP_ADDR_HEX,
                                                  LGP_SRC, "Check LGP Src IP Address")
        numberTest += 1
       
        # Step 4:Check actual and expected are same or not for LGP Dest IP Address
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_DEST_INITIAL_BCT_IP_ADDR_HEX,
                                                  LGP_DEST, "Check LGP Dest IP Address")
       
        #Step 5: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write range3 IP address for LGP Dest to NVM RAM with NVM Flag is 1,LGP Src and Diag use BCT configured as NVM flag is 0
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   2. Check the NVM Mirror Value of the NVM Packet rbDia_ip_Address_Data_au8 for LGP dest
    #   3. As nvm flag is 0 for LGP Src so read through read service and check if it is equal to BCT config or not
    #   4. Cleanup
    #  @swtest_expResult The NVM mirror value is equal to the address which has been User Configured for LGP dest.
    #  @swtest_expResult The LGP src use BCT configured.
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_765, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-765-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_767, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-767-00159bc2?doors.view=00000004}
    def swTest_LGPSrcFromBCTandLGPDestFromNVMIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Source with NVM flag 0(it will use BCT config),LGP dest with NVM flag 1(it will use user config).
        #         Diag with NVM flag 0(it will use BCT config)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
      
        #2E0600C0A8068400C0A8875701A9FE74640000
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_LGPSRC_BCTDST , self.logger)
        
        #Canoe update  for dest ip address      
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1",constant.CONST_LGP_DST_RANGE3_IP1)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        # Step 2: Check if  LGP Dest IP Address have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[9]")['vvalue'].value
        nvmMirrorSecondValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[10]")['vvalue'].value
        nvmMirrorThirdValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[11]")['vvalue'].value
        nvmMirrorFourthValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[12]")['vvalue'].value
        
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  constant.CONST_LGP_DST_RANGE3_IP1, "Check g_NvMRamMirrorIPAddressNVMDataItem")
        numberTest += 1
        
        
        
        # Step 3:As nvm flag is 0 for LGP Src so read through read service and check if it is equal to BCT config or not
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_SRC_IP_ADDR = Read_DID[6:14]
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_SRC_INITIAL_BCT_IP_ADDR_HEX,
                                                  LGP_SRC_IP_ADDR, "Check LGP Src IP Addr")
    
        #Step 4: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1",constant.CONST_LGP_DST_DEFAULT)
        
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES,self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)       
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case checks previous used IP Address for LGP Dest as NVM Flag is 2,LGP Src and Diag use BCT configured as NVM flag is 0
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   2.  As NVM flag is 0 for LGP Src(it will use BCT config) and 2 for LGP Dest(it will use previous config).Read both IP address and check if it is with in expected or not
    #   3.  Check actual and expected are same or not for LGP Src IP Address
    #   4.  Check actual and expected are same or not for LGP Dest IP Address
    #   5.  Cleanup
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_765,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-765-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_769, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-769-00159bc2?doors.view=00000004}
    def swTest_LGPSrcFromBCTandPreviousUsedLGPDestIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Source with NVM flag 0(it will use BCT config),LGP dest with NVM flag 2(it will use previous config).
        #         Diag with NVM flag 0(it will use BCT config)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A8068400C0A8675302A9FE74640000
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_LGPDEST , self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)   
        # Step 2:As NVM flag is 0 for LGP Src(it will use BCT config) and 2 for LGP Dest(it will use previous config).Read both IP address and check if it is with in expected or not
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        #extracting Src and Dest IP Address
        LGP_SRC = Read_DID[6:14]
        LGP_DEST = Read_DID[16:24]
    
       # Step 3:Check actual and expected are same or not for LGP Src IP Address
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_LGP_SRC_INITIAL_BCT_IP_ADDR_HEX,
                                                 LGP_SRC, "Check LGP Src IP Address")
        numberTest += 1
     
        # Step 4:Check actual and expected are same or not for LGP Dest IP Address
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_DEST_INITIAL_BCT_IP_ADDR_HEX,
                                                  LGP_DEST, "Check LGP Dest IP Address")
    
        #Step 5: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case writes the IP Address with the passed range to NVM RAM for LGP Dest and LGP Src use previous IP Adress as NVM Flag is 2 
    #  @swtest_step
    #   1. As source flag is 2(don't want to change Src IP Address)to test with different range first write both SRC and Dest with the passed Range IP address   
	#   2. Read Src IP Address and store in the  variable
    #   3. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   4. Check if  LGP Dest IP Address have been written to the NVM
    #   5.  As nvm flag is 2 for LGP Src so read through read service and check if it is equal to the passed Range or not
	#   6.  Cleanup
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_766,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-766-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_767, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-767-00159bc2?doors.view=00000004}
    def swTest_PreviousUsedLGPSrcandLGPDestFromNVMIsWrittenToNvmForGivenRange(self, t32_api, range, nvmFlagOneRequest, nvmFlagTwoRequest, lgpDestAddr):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: First write LGP Src and Dest with given range with NVM flag one
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, nvmFlagOneRequest, self.logger)
        
        writeIPResponse=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Write IP to NVM: {writeIPResponse}")		
        #Step 2. Validate write response -> positive response
        writeResponseStatus = writeIPResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_IP_RES, "Step :Check WDBI  ip - response")      
        numberTest += 1
        self.canoe_api.setEnvVar("Env_DoipDirectReceive_AutoIP",lgpDestAddr)
        #canoe update for dest ip address
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1","lgpDestAddr")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
		
        # Step 2:Read Src IP Address and store in the  variable 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_SRC_IP_ADDR = Read_DID[6:14]
        #self.logger.debug(f"Step 4: READ IP : {LGP_SRC_IP_ADDR}")
        
        
        # Step 3: send change IP address for LGP Source with NVM flag 2(it will use previous config),LGP dest with NVM flag 1(it will use user config).
        #         Diag with NVM flag 0(it will use BCT config)
        #self.canoe_api.setEnvVar("Env_Doip_ECU_IP",lgpDestAddr)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, nvmFlagTwoRequest, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        #self.canoe_api.setEnvVar("Env_DoipDirectReceive_AutoIP",lgpDestAddr)
        #self.logger.debug(f"Step 2: lgpDestAddr : {lgpDestAddr}")
		
        # Step 4: Check if  LGP Dest IP Address have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[9]")['vvalue'].value
        nvmMirrorSecondValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[10]")['vvalue'].value
        nvmMirrorThirdValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[11]")['vvalue'].value
        nvmMirrorFourthValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[12]")['vvalue'].value
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
        self.logger.debug(f"Step 3: nvmMirrorString: {nvmMirrorString}")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  lgpDestAddr, "Check g_NvMRamMirrorIPAddressNVMDataItem")
        numberTest += 1
    
       # Step 5:As nvm flag is 2 for LGP Src so read through read service and check if it is equal to given range or not
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)

        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_SRC_IP_ADDR1 = Read_DID[6:14]
        self.logger.debug(f"Step 4: LGP_SRC_IP_ADDR1: {LGP_SRC_IP_ADDR1}")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, LGP_SRC_IP_ADDR,
                                                  LGP_SRC_IP_ADDR1, "Check LGP Src IP Addr")
    
        #Step 6: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1",constant.CONST_LGP_DST_DEFAULT)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
        #2E06000A080684010A55675301A9FE74640000
        
    def swTest_PreviousUsedLGPSrcandLGPDestFromNVMIsWrittenToNvmForGivenRange1(self, t32_api):
        return self.swTest_PreviousUsedLGPSrcandLGPDestFromNVMIsWrittenToNvmForGivenRange(t32_api, "1", constant.CONST_PREV_LGP_SRC_NVM_RANGE1, 
                                                                                        constant.CONST_PREV_LGP_DST_NVM_RANGE1, constant.CONST_LGP_DST_RANGE1_IP1)
        
        #2E0600AC19667402AC1E358401A9FE74640000
    def swTest_PreviousUsedLGPSrcandLGPDestFromNVMIsWrittenToNvmForGivenRange2(self, t32_api):
        return self.swTest_PreviousUsedLGPSrcandLGPDestFromNVMIsWrittenToNvmForGivenRange(t32_api, "2", constant.CONST_PREV_LGP_SRC_NVM_RANGE2, 
                                                                                       constant.CONST_PREV_LGP_DEST_NVM_RANGE2 , constant.CONST_LGP_DST_RANGE2_IP1)    
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case writes IP Addresses with the passed range to NVM RAM for LGP Src and LGP Dest use previous IP Adress as NVM Flag is 2 
    #  @swtest_step
    #   1. As Destn flag is 2(don't want to change Dest IP Address)to test with different range first write both SRC and Dest with the IP address with the passed range   
	#   2. Read dest IP Address and store in the  variable
    #   3. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   4. Check if  LGP Src IP Address have been written to the NVM
    #   5.  As nvm flag is 2 for LGP Dest so read through read service and check if it is equal to the passed range or not
	#   6.  Cleanup
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_764,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-764-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_766,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-766-00159bc2?doors.view=00000004}
    def swTest_LGPSrcFromNVMandPreviousUsedLGPDestIsWrittenToNvmForGivenRange(self, t32_api, range, nvmFlagOneRequest, nvmLgpDestFlagTwoRequest, lgpSrcAddr):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: First write LGP Src and Dest for given range with NVM flag one
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, nvmFlagOneRequest, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        # Step 2:Read Dest IP Address and store in the some variable 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)

        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_DEST_IP_ADDR = Read_DID[16:24]
    
        # Step 3: send change IP address for LGP Source with NVM flag 1(it will use user config),LGP dest with NVM flag 2(it will use previous config).
        # Diag with NVM flag 0(it will use BCT config)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, nvmLgpDestFlagTwoRequest, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1","lgpSrcAddr")
        self.canoe_api.setSysVarValue("ROS_LGP_Server","ServerIP_1","LGP_DEST_IP_ADDR")
        # Step 4: Check if  LGP Src IP Address have been written to the NVM
        # check nvm mirror which is copied at startup from the nvm
        nvmMirrorFirstValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[4]")['vvalue'].value
        nvmMirrorSecondValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[5]")['vvalue'].value
        nvmMirrorThirdValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[6]")['vvalue'].value
        nvmMirrorFourthValue=t32_api.get_variable_value("g_NvMRamMirrorIPAddressNVMDataItem[7]")['vvalue'].value
        
    
        nvmMirrorString = str(nvmMirrorFirstValue) + "." + str(nvmMirrorSecondValue) + "." + str(nvmMirrorThirdValue) + "." + str(nvmMirrorFourthValue)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorString,
                                                  lgpSrcAddr, "Check rbDia_ip_Address_Data_au8")
        numberTest += 1
    
        # Step 5:As nvm flag is 2 for LGP Dest so read through read service and check if it is equal to given range or not
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)

        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_DEST_IP_ADDR1 = Read_DID[16:24]
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, LGP_DEST_IP_ADDR,
                                                  LGP_DEST_IP_ADDR1, "Check LGP Dest IP Address")
        
        #Step 6: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1",constant.CONST_LGP_DST_DEFAULT)
        self.canoe_api.setSysVarValue("ROS_LGP_Server","ServerIP_1",constant.CONST_LGP_SRC_DEFAULT)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    #2E06000A560694010A35175301A9FE74640000
    #2E06000A270724010A45653402A9FE74640000
    def swTest_LGPSrcFromNVMandPreviousUsedLGPDestIsWrittenToNvmForGivenRange1(self, t32_api):
        return self.swTest_LGPSrcFromNVMandPreviousUsedLGPDestIsWrittenToNvmForGivenRange(t32_api, "1", constant.CONST_LGPSRC_FROM_NVM_LGPDST_PREV_RANGE1, 
                                                                                        constant.CONST_LGPSRC_FROM_NVM_LGPDST_PREV_RANGERES1, constant.CONST_LGP_SRC_RANGE1_IP2)
    #2E0600AC14780501AC19455301A9FE74640000
    #2E0600AC12475401AC15653402A9FE74640000
    def swTest_LGPSrcFromNVMandPreviousUsedLGPDestIsWrittenToNvmForGivenRange2(self, t32_api):
        return self.swTest_LGPSrcFromNVMandPreviousUsedLGPDestIsWrittenToNvmForGivenRange(t32_api, "2", constant.CONST_LGPSRC_FROM_NVM_LGPDST_PREV_RANGE2, 
                                                                                        constant.CONST_LGPSRC_FROM_NVM_LGPDST_PREV_RANGERES2, constant.CONST_LGP_SRC_RANGE2_IP2)
    
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case check previous configured IP Address for LGP Src,LGP Dest and Diag
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   2.  Read LGP Src,Dest and Diag IP Address and store in the some variable 
	#   3. Cleanup
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_766,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-766-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_769, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-769-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_676, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-676-00159bc2?doors.view=00000004}
    def swTest_PreviousUsedLGPSrcLGPDestandDiagIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Source with NVM flag 2(it will use previous config),LGP dest with NVM flag 2(it will use previous config).
        #         Diag with NVM flag 2(it will use previous config)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600AC12475402AC15653402A9FE74640200
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_PREVIOUSUSEDLGPSRCLGPDESTANDDIAGISWRITTENTONVM, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        # Step 2:Read LGP Src,Dest and Diag IP Address and store in the some variable 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)

        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_SRC = Read_DID[6:14]
        #Check actual and expected are same or not for LGP Src
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_SRC_INITIAL_BCT_IP_ADDR_HEX,
                                                 LGP_SRC, "Check read LGP_SRC")
        numberTest += 1
    
        LGP_DEST = Read_DID[16:24]
        #Check actual and expected are same or not for LGP Dest
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_DEST_INITIAL_BCT_IP_ADDR_HEX,
                                                 LGP_DEST, "Check read LGP_DEST")
        numberTest += 1
       
        DIAG = Read_DID[26:34]
        #Check actual and expected are same or not for DIAG
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_DIAG_INITIAL_BCT_IP_ADDR_HEX,
                                                 DIAG, "Check read DIAG")
      
        #Step 3: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case check previous configured IP Address for LGP Src and LGP Dest 
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.
    #      Send ECU Hard Reset afterwards.
    #   2.  Read Dest IP Address and store in the some variable
	#   3.Cleanup
    #  @swtest_expResult The LGP src and LGP dest should be in same range.
    #  @sw_requirement{SDC-R_SW_DIMA_766,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-766-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_769, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-769-00159bc2?doors.view=00000004}
    def swTest_PreviousUsedLGPSrcandLGPDestIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        #2E0600AC12475402AC15653402A9FE74640000
        # Step 1: send change IP address for LGP Source with NVM flag 2(it will use previous config),LGP dest with NVM flag 2(it will use previous config).
        #         Diag with NVM flag 2(it will use previous config)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.COSNT_PREVIOUSUSEDLGPSRCANDLGPDESTISWRITTENTONVM, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
       # Step 2:Read Dest IP Address and store in the some variable 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)

        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        LGP_SRC = Read_DID[6:14]
        #Check actual and expected are same or not for LGP Src
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_SRC_INITIAL_BCT_IP_ADDR_HEX,
                                                 LGP_SRC, "Check read LGP_SRC")
        numberTest += 1
    
        LGP_DEST = Read_DID[16:24]
        #Check actual and expected are same or not for LGP Dest
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_LGP_DEST_INITIAL_BCT_IP_ADDR_HEX,
                                                 LGP_DEST, "Check read LGP_DEST")
       
        
        #Step 3: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid Max LGP Src IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidMaxLGPSrcForGivenRange(self, t32_api, range, request):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid max LGP Src 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, request, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                 constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
       
        return CTestCaseResult(numberTest, numberFailedTests)
    #2E0600C0A8786501C0A8000001A9FE22930000
    def swTest_InvalidMaxLGPSrcForGivenRange1(self, t32_api):
        return self.swTest_InvalidMaxLGPSrcForGivenRange(t32_api, "1", constant.CONST_INVALIDMAXLGPSRCFORGIVENRANGE1)
    #2E0600AC14456701AC10000001A9FE22930000
    def swTest_InvalidMaxLGPSrcForGivenRange2(self, t32_api):
        return self.swTest_InvalidMaxLGPSrcForGivenRange(t32_api, "2", constant.CONST_INVALIDMAXLGPSRCFORGIVENRANGE2)
    #2E06000A010389010A00000001A9FE22930000
    def swTest_InvalidMaxLGPSrcForGivenRange3(self, t32_api):
        return self.swTest_InvalidMaxLGPSrcForGivenRange(t32_api, "3", constant.CONST_INVALIDMAXLGPSRCFORGIVENRANGE3)    
            
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid Min LGP Src IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidMinLGPSrcForGivenRange(self, t32_api, range, request):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid min LGP Src 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, request, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
        #2E06000A000000010A09223801A9FE22930100
    def swTest_InvalidMinLGPSrcForGivenRange1(self, t32_api):
        return self.swTest_InvalidMinLGPSrcForGivenRange(t32_api, "1", constant.CONST_INVALIDMINLGPSRCFORGIVENRANGE1)
        #2E0600AC10000001AC19070801A9FE22930000
    def swTest_InvalidMinLGPSrcForGivenRange2(self, t32_api):
        return self.swTest_InvalidMinLGPSrcForGivenRange(t32_api, "2", constant.CONST_INVALIDMINLGPSRCFORGIVENRANGE2)
        #2E0600C0A8000001C0A8070801A9FE22930000
    def swTest_InvalidMinLGPSrcForGivenRange3(self, t32_api):
        return self.swTest_InvalidMinLGPSrcForGivenRange(t32_api, "3", constant.CONST_INVALIDMINLGPSRCFORGIVENRANGE3)
        
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid Max LGP Dest IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidMaxLGPDestForGivenRange(self, t32_api, range, request):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid max LGP Dest 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, request, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    #2E06000A010389010AFFFFFF01A9FE22930000
    def swTest_InvalidMaxLGPDestForGivenRange1(self, t32_api):
        return self.swTest_InvalidMaxLGPDestForGivenRange(t32_api, "1", constant.CONST_INVALIDMAXLGPDESTFORGIVENRANGE1)
    #2E0600AC14456701AC1FFFFF01A9FE22930000
    def swTest_InvalidMaxLGPDestForGivenRange2(self, t32_api):
        return self.swTest_InvalidMaxLGPDestForGivenRange(t32_api, "2", constant.CONST_INVALIDMAXLGPDESTFORGIVENRANGE2)
    #2E0600C0A8786501C0A8FFFF01A9FE22930000
    def swTest_InvalidMaxLGPDestForGivenRange3(self, t32_api):
        return self.swTest_InvalidMaxLGPDestForGivenRange(t32_api, "3", constant.CONST_INVALIDMAXLGPDESTFORGIVENRANGE3)        
        
    
    ##@swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid min LGP Dest IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidMinLGPDestForGivenRange(self, t32_api, range, request):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid min LGP Dest 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, request, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)

    def swTest_InvalidMinLGPDestForGivenRange1(self, t32_api):
        return self.swTest_InvalidMinLGPDestForGivenRange(t32_api, "1", constant.CONST_INVALIDMINLGPDESTFORGIVENRANGE1)
    
    def swTest_InvalidMinLGPDestForGivenRange2(self, t32_api):
        return self.swTest_InvalidMinLGPDestForGivenRange(t32_api, "2", constant.CONST_INVALIDMINLGPDESTFORGIVENRANGE2)
    
    def swTest_InvalidMinLGPDestForGivenRange3(self, t32_api):   
        return self.swTest_InvalidMinLGPDestForGivenRange(t32_api, "3", constant.CONST_INVALIDMINLGPDESTFORGIVENRANGE3)     
    
    
    ##@swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid second byte min LGP Src IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidsecondbyteLGPSrcForGivenRange(self, t32_api, range, request):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid second byte for given range LGP Src address 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, request, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
        #2E0600AC21038901AC14070801A9FE22930000
    def swTest_InvalidsecondbyteLGPSrcForGivenMaxRange2(self, t32_api):
        return self.swTest_InvalidsecondbyteLGPSrcForGivenRange(t32_api, "maxRange2",constant.CONST_INVALIDSEC_LGPSRC_MAXRANGE2 )
        #2E0600AC01038901AC14070801A9FE22930000
    def swTest_InvalidsecondbyteLGPSrcForGivenMinRange2(self, t32_api):
        return self.swTest_InvalidsecondbyteLGPSrcForGivenRange(t32_api, "minRange2",constant.CONST_INVALIDSEC_LGPSRC_MINRANGE2 )
    
    def swTest_InvalidsecondbyteLGPSrcForGivenRange3(self, t32_api):
        #2E0600C0BC038901C0A8070801A9FE22930000
        return self.swTest_InvalidsecondbyteLGPSrcForGivenRange(t32_api, "range3", constant.CONST_INVALIDSEC_LGPSRC_RANGE2)

    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid second byte max LGP Dest IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidsecondbyteLGPDestForGivenRange(self, t32_api, range, request):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid second byte max for given range LGP Dest address 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, request, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC,"Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    def swTest_InvalidsecondbyteLGPDestForGivenMaxRange2(self, t32_api):
        #2E0600AC11038901AC3F070801A9FE22930000
        return self.swTest_InvalidsecondbyteLGPDestForGivenRange(t32_api, "maxRange2",constant.CONST_INVALIDSECBYTE_MAXRANGE2 )
    
    def swTest_InvalidsecondbyteLGPDestForGivenMinRange2(self, t32_api):
        #2E0600AC11038901AC07070801A9FE22930000
        return self.swTest_InvalidsecondbyteLGPDestForGivenRange(t32_api, "minRange2",constant.CONST_INVALIDSECBYTE_MINRANE2 )
    
    def swTest_InvalidsecondbyteLGPDestForGivenRange3(self, t32_api):   
        #2E0600C0A8038901C0F8070801A9FE22930000
        return self.swTest_InvalidsecondbyteLGPDestForGivenRange(t32_api, "range3",constant.CONST_INVALIDSECBYTE_RANGE3)
        
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid LGP Src and Dest IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_762,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-762-00159bc2?doors.view=00000004}
    def swTest_InvalidLGPSrcandLGPDestisDifferentRange(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid LGPSrc and LGPDest 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A87865010A07865401A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_SERVICE_WDBI+constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR+constant.CONST_LGP_SRC_DIAG+constant.CONST_DIAG_NVM_FLAG_READ_VALUES_FROM_NVM+constant.CONST_IP_LGP_DST_INVALID+constant.CONST_DIAG_NVM_FLAG_READ_VALUES_FROM_NVM+constant.CONST_DIAG_USER_CONFIGURED_IP_ADDR3_HEX+constant.CONST_LGP_DEST_NVM_INVALID+constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid LGP Src and Dest IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_761,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-761-00159bc2?doors.view=00000004}
    def swTest_InvalidLGPSrcandLGPDestisEqual(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid LGPSrc and LGPDest 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A8786501C0A8786501A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DESTIS , self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description The test case request to change only LGP Src IP Address  and LGP Dest use previuos config IP Address
    #    This test case writes LGP Src IP Address with different range than LGP Dest
    #    As Destn flag is 2(don't want to change Dest IP Address)to test with different range first write both SRC and Dest with the IP address with the passed range
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service(NVM Mirror will update)
    #   2. Jump to Extended Session (0x10 03). Send "Change IP Address" service(NVM Mirror won't update)
    #   3. Checking software response
    #   4.Cleanup 
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_729,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-729-00159bc2?doors.view=00000004}
    def swTest_reportNRC_requestchangeLGPSrcandusepreviuosconfigforLGPDest(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Src and Dest
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A87865020A12321501A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_REPORT_NRC, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        #time.sleep(0.5)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1","10.18.50.21")
        # Step 2: send change IP address for LGP Src
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A8786501AC13786502A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_REPORT_NRC_RES, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 3: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
        
        #Step 4: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        self.canoe_api.setEnvVar("Env_Doip_ECU_IP",constant.CONST_LGP_DST_DEFAULT)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case request to change only LGP Src IP Address and LGP Dest use predefined IP Address
    #    This test case writes LGP Src IP Address with different range than LGP Dest
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_730,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-730-00159bc2?doors.view=00000004}
    def swTest_reportNRC_requestchangeLGPSrcandusepredefinedvaluesforLGPDest(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address sLGP Src
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E06000A23567801C0A8432100A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_REPORT_NRC_PREDEFINED , self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
     
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case request to change only LGP Dest IP Address and LGP Src use previuos config IP Address
    #    This test case writes LGP Dest IP Address with different range than LGP Src
    #    As Src flag is 2(don't want to change Src IP Address)to test with different range first write both SRC and Dest with the IP address with the passed range
    #  @swtest_step
    #   1. As Src flag is 2(don't want to change Src IP Address)to test with different range first write both SRC and Dest with the IP address with the passed range  
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service(NVM Mirror will update)
    #   2. Jump to Extended Session (0x10 03). Send "Change IP Address" service(NVM Mirror won't update)
    #   3. Checking software response
    #   4. Cleanup
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_662,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-662-00159bc2?doors.view=00000004}
    def swTest_reportNRC_requestchangeLGPDestandusepreviuosconfigforLGPSrc(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Src and Dest
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
		#2E0600AC17864301AC18786501A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_CHANGE_IP_LGP_SRC_DEST, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        #time.sleep(0.5)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1","172.24.120.101")
        self.canoe_api.setSysVarValue("ROS_LGP_Server","ServerIP_1","172.23.134.67")
        # Step 2: send change IP address for LGP Dest 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
		#2E0600C0A87865020A12321501A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_CHANGE_IP_LGP_TO_DEST, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 3: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
        
        #Step 4: Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        self.canoe_api.setEnvVar("Env_Doip_ECU_IP",constant.CONST_LGP_SRC_DEFAULT)
        self.canoe_api.setEnvVar("Env_Doip_ECU_IP",constant.CONST_LGP_DST_DEFAULT)
        # send change Diag IP address service with NVM Flag = 0 --> go back to BCT configured IP Address
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_CLEANUP_NVM_TO_INIT_BCT_IP_ADDR_VALUES, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case request to change only LGP Dest IP Address and LGP Src use predefined IP Address
    #    This test case writes LGP Dest IP Address with different range than LGP Src
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_663,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-663-00159bc2?doors.view=00000004}
    def swTest_reportNRC_requestchangeLGPDestandusepredefinedvaluesforLGPSrc(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address for LGP Dest 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E06000A23567800AC18923401A9FE22930800
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_REPORT_NRC_PREDEFINEDLGP , self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        self.canoe_api.setSysVarValue("ROS_LGP_Client","ClientIP_1","172.24.146.52")
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
     
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid First byte Diag IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidFirstByteDiag(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid max Range3 LGP DestFirst Byte Diag 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A8786501C0A8456301B9FE22930100
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_INVALID_FIRST_DIAG , self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid second byte Diag IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidSecondByteDiag(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid max Range3 LGP Dest Second Byte Diag 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        
        #2E0600C0A8786501C0A8456301A9FF22930100
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_INVALID_SEC_DIAG , self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid min Diag IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidMinDiag(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid Min Diag 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        
        #2E0600C0A8786501C0A8456301A9FE00000100
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_MINDIAG , self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change ip address through diag write services for LGP Src,LGP Dest and diag
    #    This test case write Invalid max Diag IP Address
    #  @swtest_step
    #   1. Jump to Extended Session (0x10 03). Send "Change IP Address" service.   
    #   2.  the NVM Mirror won't be updated because Invalid data
    #  @swtest_expResult it should returns NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-658-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_659,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-659-00159bc2?doors.view=00000004}
    def swTest_InvalidMaxDiag(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1: send change IP address service with Invalid max  Diag 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        #2E0600C0A8786501C0A8456301A9FEFFFF0100
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_MAXDIAG, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: check write service return NRC 31 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check DID_response-request out of range")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case Reads currently used IP address 
    #   1. Jump to Default Session (0x10 01) and send "Read IP Address" service . Reads the values.
    #   2. Check the Expected and actual values
    #  @swtest_expResult Expected and actual read value should match.
    #  @sw_requirement{SDC-R_SW_DIMA_656,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-656-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_693,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-693-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_694,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-694-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_606,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-606-00159bc2?doors.view=00000004}
    def swTest_checkIPAddrRead(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        # Step 1:send read diagnostic service to read IP Address
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        #canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "220600", self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.USE_CURRENT_IP_FLAG_READ_REQUEST, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        Actual_IP_Response = Read_DID[0:6]
        #Check actual and expected are same or not IP Read Response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_READ_DID_RES_IP,
                                                 Actual_IP_Response, "Check read response")
        numberTest += 1
      
        LGP_SRC = Read_DID[6:14]
        #Check actual and expected are same or not for LGP Src
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,  constant.CONST_LGP_SRC_INITIAL_BCT_IP_ADDR_HEX,
                                                 LGP_SRC, "Check read LGP_SRC")
        numberTest += 1
    
        LGP_DEST = Read_DID[16:24]
        #Check actual and expected are same or not for LGP Dest
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,  constant.CONST_LGP_DEST_INITIAL_BCT_IP_ADDR_HEX,
                                                 LGP_DEST, "Check read LGP_DEST")
        numberTest += 1
       
        DIAG = Read_DID[26:34]
        #Check actual and expected are same or not for LGP Diag
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,  constant.CONST_DIAG_INITIAL_BCT_IP_ADDR_HEX,
                                                 DIAG, "Check read DIAG")
       
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description This test case checks that a range 5 destination IP address is stored in NVM if the address itself is valid and  
    #    the source IP address is not requested to be changed.       
    #  @swtest_step
    #    1. Jump into extended session and read the the current IP address
    #    2. Choose a representative of range 5 destination IP address and request it to be written by the WDBI service
    #    3. Validate that the service response was positive
    #    4. Restart the sensor
    #    5. Validate that the destination IP address written in step 2 is active after sensor restart
    #    6. Restore the changed destination IP address and restart the sensor
    #  @swtest_expResult All test steps are executed and validated successfully.
    #  @sw_requirement{SDC-R_SW_DIMA_759, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-759-00159bc2?doors.view=00000004}
    def swTest_storeDestIpNvmRange5NoChangeSource(self, t32_api):
    # The software shall store the diagnostic requested destination ip address into NVM if destination  IP address is in  range 5 and 
    # no change requested for source IP address.
        numberFailedTests = 0
        numberTest = 1                    
        
        # 1. Read current IP address
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_SERVICE_RDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR, self.logger)
        readIpAddrResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        readResponseStatus = readIpAddrResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, readResponseStatus,
                                                constant.CONST_READ_DID_RES_IP, "Check RBDI IP Address - response")
        numberTest += 1
    
        currentSourceAddr = readIpAddrResponse[6:14]
        currentDestIpAddr = readIpAddrResponse[16:24]
        currentDiagAddr = readIpAddrResponse[26:34]
        
        # 2. Write destination IP in range 5
        # Use one representative IP address of range 5 - IP Address Range 5: 224.0. 0.0 to 239.255.255.255 (Net Mask - na)
        # destIpAddreeRepresentative = "e10001ff" #  225.0.1.255         
        destIpAddreeRepresentative = constant.CONST_DEST_IP_ADDRESS_REP_HEX #  225.0.1.255        
        # Byte 1 to Byte 4 (AA):  Source IP address
        # Byte 5 (AA_Flag) :  Source_Flag
        # Byte 6 to Byte 9 (BB):  Destination IP address
        # Byte 10 (BB_Flag) :  Destination_Flag
        # Byte 11 to Byte 14 (CC):  Diagnostic Source IP address
        # Byte 15 (CC_Flag) :  Diag_Flag
        # Byte 16 (XX) :  Dummy set as 0x00                      
        
        # 2E 0600 | keep previous 02 | destIpAddreeRepresentative 01 | keep previous 02 | 00
        writeIpAddrRequest = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR + \
                            currentSourceAddr + constant.USE_CURRENT_IP_FLAG_WRITE_REQUEST + \
                            destIpAddreeRepresentative + constant.USE_REQUEST_IP_FLAG_WRITE_REQUEST + \
                            currentDiagAddr + constant.USE_CURRENT_IP_FLAG_WRITE_REQUEST + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA
        
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, writeIpAddrRequest, self.logger)
        writeIpAddrResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
        
        # 3. Validate response -> positive response
        writeResponseStatus = writeIpAddrResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_IP, "Check WDBI IP Address - response")
        numberTest += 1                                
        
        # 4. restart sensor
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        
        # 5. Check destination IP address to be same as written in step 2.
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_SERVICE_RDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR, self.logger)
        readIpAddrAfterResetResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
       
        destIpAddrAfterReset = readIpAddrAfterResetResponse[16:24]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, destIpAddrAfterReset,
                                                 destIpAddreeRepresentative, "Check WDBI IP Address - Destination IP address after reset")     
        
        # 6. clean up and restore old destination IP address 
        writeIpAddrRequest = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR + \
                            currentSourceAddr + constant.USE_CURRENT_IP_FLAG_WRITE_REQUEST + \
                            currentDiagAddr + constant.USE_REQUEST_IP_FLAG_WRITE_REQUEST + \
                            currentDiagAddr + constant.USE_CURRENT_IP_FLAG_WRITE_REQUEST + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA
        
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, writeIpAddrRequest, self.logger)
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
                        
        return CTestCaseResult(numberTest, numberFailedTests)
        
    ## @swtest_description This test case checks that a negative response code is received if the destination address in range 5 and source IP address
    #    is requested to be changed.
    #  @swtest_step
    #    1. Jump into extended session and read the the current IP address
    #    2. Choose a representative of range 5 destination & range 2 source IP address and request both to be written by the WDBI service
    #    3. Validate that a negative response code with NRC out of range is received
    #    4. Cleanup and jump back into default session
    #  @swtest_expResult All test steps are executed and validated successfully.
    #  @sw_requirement{SDC-R_SW_DIMA_664, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-664-00159bc2?doors.view=00000004}
    def swTest_reportNrcDestIpRange5SourceIpOther(self, t32_api):
    # The software shall report out of range NRC when requestd destination IP address is in range 5 and also  source IP address is requested to change.
    # NRC when { Source IP = range 1 or 2 or 3 } and { Destination IP = Range 5 }
        numberFailedTests = 0
        numberTest = 1
        
        # 1. Read current IP address
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_SERVICE_RDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR, self.logger)
        readIpAddrResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        readResponseStatus = readIpAddrResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, readResponseStatus,
                                                constant.CONST_READ_DID_RES_IP, "Check RBDI IP Address - response")
        numberTest += 1
    
        currentDiagAddr = readIpAddrResponse[26:34]
        
        # 2. Write destination IP in range 5 and source IP in range 2 
        
        # Use one representative IP address 
        # one of range 5 - IP Address Range 5: 224.0. 0.0 to 239.255.255.255 (Net Mask - na)
        destIpAddreeRepresentative = constant.CONST_DEST_IP_ADDRESS_REP_RANGE5_HEX #  230.255.1.255        
        # one of range 2 - IP Address Range 2: 172.16.0.1 to 172.31.255.254 (Net Mask - 12)
        sourceIpAddreeRepresentative = constant.CONST_SRC_IP_ADDRESS_REP_RANGE2_HEX #  172.25.1.255      
      
        # 2E 0600 | destIpAddreeRepresentative 01 | destIpAddreeRepresentative 01 | keep previous 02 | 00
        writeIpAddrRequest = constant.CONST_DIAG_UDS_SERVICE_WDBI + constant.CONST_DIAG_UDS_SUBSERVICE_IP_ADDR + \
                            sourceIpAddreeRepresentative + constant.USE_REQUEST_IP_FLAG_WRITE_REQUEST + \
                            destIpAddreeRepresentative + constant.USE_REQUEST_IP_FLAG_WRITE_REQUEST + \
                            currentDiagAddr + constant.USE_CURRENT_IP_FLAG_WRITE_REQUEST + constant.CONST_DIAG_VAR_HDL_SERVICE_DUMMY_DATA
      
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, writeIpAddrRequest, self.logger)
        writeIpAddrResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
      
        # 3. Check for NRC 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeIpAddrResponse,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check WDBI negative response NRC")
        
        # 4. cleanup and jump into default session
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)    
    
    ## @swtest_description The test case check destination port read and write 
    #  the test case write Valid destination port number with NVM flag one
    #  @swtest_step
    #    1. Write destination port number data to NVM using WDBI service
    #    2. Validate write response -> positive response
    #    3. Read destination port number value using read service 
    #    4. Validate read response -> positive response
    #    5. Read destination port number from NVM
    #    6. Check destination port num
    #    7. Check nvm flag
    #    8. Cleanup   
    #  @swtest_expResult User configured and NVM  ram value should be same.
    #  @sw_requirement{SDC-R_SW_DIMA_79, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-79-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_81, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-81-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_83,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-83-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_686, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-686-00159bc2?doors.view=00000004}
    def swTest_checkDestinationPortIsWrittenToNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        #1.Write destination port number data to NVM using WDBI service
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_DID_REQ_DESTINATION_PORT_NVM, self.logger)
        writeDestnPortResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
                
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeDestnPortResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_DESTINATION_PORT, "Step 2:Check WDBI Destination port - response")
        
        numberTest += 1
        
        #3.Read destination port number value using read service         
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_REQ_DESTINATION_PORT, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(0.5) 
        
       
        readResponseStatus        = Read_DID[0:6] 
        destinationportvalue      = Read_DID[6:10]
        destinationnvmflag        = Read_DID[20:22]
        
        #4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_DESTINATION_PORT, readResponseStatus,
                                                 "Step 4:Check RBDI destination port - response")
        numberTest += 1
    
    
        #5.Read destination port number from NVM
        nvmMirrorFirstValue  = format(t32_api.get_variable_value("g_NvMRamMirrorDestinationPortNVMDataItem[4]")['vvalue'].value,'02x')
        nvmMirrorSecondValue = format(t32_api.get_variable_value("g_NvMRamMirrorDestinationPortNVMDataItem[5]")['vvalue'].value,'02x')
        
        destnportnvmflagnvmmirror = format(t32_api.get_variable_value("g_NvMRamMirrorDestinationPortNVMDataItem[11]")['vvalue'].value,'02x')
    
        destnportnvmmirror = str(nvmMirrorFirstValue) + str(nvmMirrorSecondValue) 
    
        #6.Check destination port num
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, destnportnvmmirror,
                                                  destinationportvalue, "Check destination port num")
        
        numberTest += 1
    
        #7.Check nvm flag
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, destnportnvmflagnvmmirror,
                                                  destinationnvmflag, "Check destination port nvm flag")
    
        numberTest += 1
    
        #8.Cleanup
        self.logger.debug("Cleanup by sending service to use the initially configured BCT address again")
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_DID_REQ_DESTINATION_PORT_BCT, self.logger)
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change Destination port address through diag write services 
    #  the test case write InValid Min destination port number with NVM flag one
    #  @swtest_step
    #   1.Write destination port number data to NVM using WDBI service.  
    #   2.Check write response 
    #  @swtest_expResult write service should return NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_79, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-79-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_81, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-81-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_83,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-83-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_686, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-686-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_688,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-688-00159bc2?doors.view=00000004}
    def swTest_InvalidMinDestinationPort(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        #1.Write destination port number data to NVM using WDBI service 
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_DESTINATION_PORT_NVM1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # 2.Check write response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check InvalidMinDestinationPort")
     
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case change Destination port address through diag write services 
    #  the test case write InValid Max destination port number with NVM flag one
    #  @swtest_step
    #   1.Write destination port number data to NVM using WDBI service.    
    #   2.Check write response 
    #  @swtest_expResult write service should return NRC 31.
    #  @sw_requirement{SDC-R_SW_DIMA_79, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-79-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_81, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-81-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_83,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-83-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_686, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-686-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_688,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-688-00159bc2?doors.view=00000004}
    def swTest_InvalidMaxDestinationPort(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        #1.Write destination port number data to NVM using WDBI service.  
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_DID_REQ_DESTINATION_PORT_NVM2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
    
        # Step 2: Check write response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response,
                                                  constant.CONST_OUT_OF_RANGE_NRC, "Check InvalidMaxDestinationPort")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case reads destination port address  
    #   1.Send  Read service to read currently used destination port addess
    #   2.Check read response
    #   3.Check destination port 
    #  @swtest_expResult Expected and actual read value should match.
    #  @sw_requirement{SDC-R_SW_DIMA_679,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-679-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_691,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-691-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_692,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-692-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_680,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-680-00159bc2?doors.view=00000004}
    def swTest_ReadDestinationPort(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        #1.Send  Read service to read currently used destination port addess
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_DID_REQ_DESTINATION_PORT, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(0.5)
       
        Actual_DESTN_PORT_Response = Read_DID[0:6]
        #2.Check read response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_READ_DID_RES_DESTN_PORT,
                                                 Actual_DESTN_PORT_Response, "Check Read response")
        numberTest += 1
       
    
        DESTN_PORT = Read_DID[6:10]
        #3.Check destination port 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_BCT_CONFIG_DESTN_PORT,
                                                 DESTN_PORT, "Check  Destn port")
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description This test case check Modulation Control  'startModulation' is set as default NVM value. 
    #  @swtest_step
    #    1. Read modulation control value using read service 
    #    2. Validate read response -> positive response
    #    3. Read modulation control from NVM
    #    4. Check modulation control  
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_926, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-926-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_925, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-925-00159bc2?doors.view=0000000b}   
    def swTest_checkModulationControlDefaultvalue(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
         
        #1.Read modulation control value using read service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_UDS_SERVICE_RDBI+constant.CONST_DIAG_UDS_DID_MODULATION_CNTRL, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(0.5) 
            
        readResponseStatus        = Read_DID[0:6] 
        modulationcntrolvalue     = Read_DID[6:8]
        
         #2. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MODULATION_CNTRL, readResponseStatus,
                                                 "Step 2:Check RBDI Modulation - response")
        numberTest += 1
          
        #3.Read modulation control from NVM
        modulationcntrolvaluenvm      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        self.logger.info(f"### Nvm default value   {modulationcntrolvaluenvm}   ###")
        #4. Check modulation control
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest, modulationcntrolvaluenvm, modulationcntrolvalue,
                                                 "Step 4:Check modulation-control value")
          
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description This test case check Modulation Control value 'start modulation' write and read using diag service. 
    #  @swtest_step
    #    1. Write modulation control value using write service 
    #    2. Validate write response -> positive response
    #    3. Read modulation control value using read service 
    #    4. Validate read response -> positive response
    #    5. Read modulation control from NVM
    #    6. Check modulation control  
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_927, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-927-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_924, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-924-00159bc2?doors.view=0000000b}
    def swTest_checkModulationControlvalue_startModulation(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
         
        #1.Write modulation control value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
       # canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)   
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Step 2:Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control value using read service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_UDS_SERVICE_RDBI+constant.CONST_DIAG_UDS_DID_MODULATION_CNTRL, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(0.5) 
        
       
        readResponseStatus        = Read_DID[0:6] 
        modulationcntrolvalue     = Read_DID[6:8]
        
        #4. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MODULATION_CNTRL, readResponseStatus,
                                                 "Step 4:Check RBDI Modulation - response")
        numberTest += 1
          
        #5.Read modulation control from NVM
        modulationcntrolvaluenvm      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        self.logger.debug(f"Step 2: START MODULATION READ NVM: {modulationcntrolvaluenvm}")
        
        
        #6. Check modulation control
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,modulationcntrolvaluenvm, modulationcntrolvalue,
                                                 "Step 6:Check modulation-control value")
        
       
        return CTestCaseResult(numberTest, numberFailedTests)
    
     ## @swtest_description This test case check Modulation Control value 'stop modulation' write and read using diag service. 
    #  @swtest_step
    #    1. Precondition: Jump to default session and clear all stored DTCs
    #    2. Check that no DTCs are stored
    #    3. Write modulation control value using write service 
    #    4. Validate write response -> positive response
    #    5. Read modulation control value using read service 
    #    6. Validate read response -> positive response
    #    7. Read modulation control from NVM
    #    8. Check modulation control  
    #    9. Check that the DTC- DTC_SENSOR_RADAR_MODULATION  are set
    #    10. Cleanup
    #    11. Clear all DTC 
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_927, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-927-00159bc2?doors.view=0000000b}
    def swTest_checkModulationControlvalue_stopModulation(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
         
        # 1. jump to default session and clear DTCs
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        # ClearDiagnosticInformation (0x14) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Clear DTC response: {clearDtcResponse}")
         
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 1: Check Clear DTC Res")
        numberTest += 1
        
        # 2. make sure no other DTCs are present
        # Retrieving the list of DTCs that match a client defined status mask (sub-function = 0x02 reportDTCByStatusMask)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagReadDtcbyStatusMask + diagbasic.k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 2: Read DTC response: {dtcList}")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList,diagbasic.k_diagReadDtcbyStatusMaskPositiveResponse +diagbasic. k_diagReadDtcInformationStatus, "Step 2: Check no DTC stored")
        numberTest += 1
        
        #3.Write modulation control value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_STOP_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        # canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)   
        # time.sleep(0.5) 
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        #4. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Step 4:Check WDBI Modulation - response")
        
        numberTest += 1
        
        #5.Read modulation control value using read service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_UDS_SERVICE_RDBI+constant.CONST_DIAG_UDS_DID_MODULATION_CNTRL, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(0.5) 
        
       
        readResponseStatus        = Read_DID[0:6] 
        modulationcntrolvalue     = Read_DID[6:8]
        
        #6. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MODULATION_CNTRL, readResponseStatus,
                                                 "Step 6:Check RBDI Modulation - response")
        numberTest += 1
          
        #7. Check modulation control
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest, constant.CONST_MODULATION_CNTRL_STOP_MODULATION, modulationcntrolvalue,
                                                 "Step 7:Check modulation-control value")
        
        numberTest += 1
        
        #8. check stored DTC for DTC_SENSOR_RADAR_MODULATION
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagReadDtcbyStatusMask + diagbasic.k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_modulationDtcbyStatusResponse, "Step 8: DTC match for DTC_SENSOR_RADAR_MODULATION")
        numberTest += 1
        
        
        #10.Cleanup         
        self.logger.debug("Cleanup by sending service to use the default configured modulation  control")
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        # canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)   
        # time.sleep(0.5) 
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        #11. jump to default session and clear DTCs
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        # ClearDiagnosticInformation 0x14) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Clear DTC response: {clearDtcResponse}")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 11: Check Clear DTC Res")
        
        return CTestCaseResult(numberTest, numberFailedTests)
     
    ## @swtest_description This test case check out of range of Modulation control value
    #  @swtest_step
    #    1. Write modulation control value using write service
    #    2. Check write response
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_943, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-943-00159bc2?doors.view=0000000b}
    def swTest_checkModulationControlvalue_requestoutofrange(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        #1.Write modulation control value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_WRONG_MODULATION_VALUE, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")       
        time.sleep(0.5)   
      
        #2.Check write response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Check Modulation Control - DID response NRC")
    
        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description This test case check out of range of MAC Address Write Request
    #  @swtest_step
    #    1. Write MAC Address value using write service for NRC31 scenarios
    #    2. Check write response
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_948, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-948-00159bc2?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_DIMA_949, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-949-00159bc2?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_DIMA_950, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-950-00159bc2?doors.view=00000005}
    def swTest_checkMACAddress_requestoutofrange(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        #1.Write MAC Address value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_EXTENDED_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_MAC_WRITE_REQUEST_OUT_OF_RANGE_FF_REQ, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")       
        time.sleep(0.5)   
      
        #2.Check write response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Check MAC Request Out of Range - DID response NRC")
        
        numberTest += 1
        
        #3.Write MAC Address value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_EXTENDED_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_MAC_WRITE_REQUEST_OUT_OF_RANGE_00_REQ, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")       
        time.sleep(0.5)   
      
        #4.Check write response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Check MAC Request Out of Range - DID response NRC")
        
        numberTest += 1
        
        #5.Write MAC Address value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_EXTENDED_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_MAC_WRITE_REQUEST_OUT_OF_RANGE_NVM_INVALID_REQ, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")       
        time.sleep(0.5)   
      
        #6.Check write response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Check MAC Request Out of Range - DID response NRC")
       
        return CTestCaseResult(numberTest, numberFailedTests)
