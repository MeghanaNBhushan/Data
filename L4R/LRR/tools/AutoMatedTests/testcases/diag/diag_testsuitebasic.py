# -*- coding: utf-8 -*-

import time
import xlrd as rd
import sys
import os
import re

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

import rbSysEvM_testsuiteconstants as rbSysEvmConstant

k_commitIDRegex    = "RBBUILD_VERSION_COMMITID\s\{([a-fA-F0-9\s',]*)"
k_userIDRegex      = "RBBUILD_VERSION_USERID\s\{([a-zA-Z0-9\s',]*)"
k_buildDateRegex   = "RBBUILD_VERSION_BUILD_DATE\s\s\s\{([a-zA-Z0-9\s',]*)"
k_buildTimeRegex   = "RBBUILD_VERSION_BUILD_TIME\s\s\s\{([0-9\s\:',]*)"
k_buildVersionRegex= "RBBUILD_VERSION_CUSTOMER_SWID\s\"([a-zA-Z0-9\_\.]*)"
k_replaceCharacters = ["'",","," "]
k_replaceCharactersStr = ["0x"]

# DTC values
k_dtcUC_UNDER_VOLTAGE = "f00316"


k_diagReadDtcInformationStatus = "0d"

k_diagReadDtcCount ="0001"

k_DTCFormatIdentifier ="01"

# Diag service request/response
k_diagReadDtcbyStatusMask = "1902"
k_diagReadDtcbyStatusMaskPositiveResponse = "5902"

# Diag service request/response
k_diagReadNumberofDtcbyStatusMask = "1901"
k_diagReadNumberofDtcbyStatusMaskPositiveResponse = "5901"

k_diagClearAllDtcRequest = "14FFFFFF"

k_diagreportSupportedDTC = "190A"

k_diagReadSupportedDTCsPositiveResponse="590a"

k_testerPresentRequest ="3E00"

k_controlDTCSettingOn ="8501"
k_controlDTCSettingOff ='8502'

k_ecuHardReset ="1101"
k_ecuSoftReset ='1103'

# positive response: 59020d, DTC: d60e17, status: 0d
k_ucUnderVoltageNumberofDtcbyStatusResponse = k_diagReadNumberofDtcbyStatusMaskPositiveResponse + k_diagReadDtcInformationStatus + k_DTCFormatIdentifier+ k_diagReadDtcCount

# positive response: 59020d, DTC: d60e17, status: 0d
k_ucUnderVoltageDtcbyStatusResponse = k_diagReadDtcbyStatusMaskPositiveResponse + k_diagReadDtcInformationStatus + k_dtcUC_UNDER_VOLTAGE + k_diagReadDtcInformationStatus


def getValuesfromrbBuildVersionCfg():
    #self.logger.info("Extracting information from rbBuild_Version_Cfg.h")
    ASCII_values =[0x62,0xfd,0x0,0x8]
    with open('./../../../generatedFiles/rbBuild_Version_Cfg.h', 'r') as reader:

        # Extracting Build Version
        for line in reader:
            if re.search(k_buildVersionRegex, line):
                buildVer = re.search(k_buildVersionRegex, line).group(1)   
                #converting char into ASCII
                for character in buildVer:
                    ASCII_values.append(ord(character))
                ASCII_values.append(constant.CONST_SEPARATOR_CHARACTER) # Seprator character ';'
    
    # provided by the Unstash.py script     
    with open('./../../../generatedFiles/rbBuild_Version.h', 'r') as reader:
        # Read and print the entire file line by line
        for line in reader:

            #Extracting user Information
            if re.search(k_userIDRegex, line):
                userID = re.search(k_userIDRegex, line).group(1)
                # Replacing space, comma, quotes form the User ID
                for character in k_replaceCharacters:
                   userID = userID.replace(character, "")
                # Converting char into ASCII
                for character in userID:
                    ASCII_values.append(ord(character))
                #assigning 0x00 when the user length is less than 7 in cases of jenkins PC
                if(len(userID)< constant.CONST_USER_LENGTH_LESS_THAN_SEVEN):
                    ASCII_values.append(constant.CONST_APPEND_ZERO)
                    ASCII_values.append(constant.CONST_APPEND_ZERO)
                ASCII_values.append(constant.CONST_SEPARATOR_CHARACTER) # Appending Seprator character ';'
    
    # provided by the Unstash.py script     
    with open('./../../../generatedFiles/rbBuild_Version.h', 'r') as reader:
        # Read and print the entire file line by line
        for line in reader:
            #Extracting Commit ID
            if re.search(k_commitIDRegex, line):
                commitID = re.search(k_commitIDRegex, line).group(1) 
                # Replacing space, comma, quotes form the commit ID
                for character in k_replaceCharacters:
                   commitID = commitID.replace(character,"")
                # Converting char into ASCII
                for character in commitID:
                    ASCII_values.append(ord(character))
                ASCII_values.append(constant.CONST_SEPARATOR_CHARACTER) # Seprator character ';'
            
            #Extracting Build Date
            if re.search(k_buildDateRegex, line):
                buildDate = re.search(k_buildDateRegex, line).group(1)
                # Replacing space, comma, quotes form the Build Date
                for character in k_replaceCharacters:
                   buildDate = buildDate.replace(character, "")

                # To convert date into "Sep 01 2021" format spliting and adding build date with space.
                date = []
                date.append(buildDate[:3])   #Month
                date.append(buildDate[3:5])  #Day
                date.append(buildDate[5:])   #Year
                buildDate = ' '.join(date)

                # Converting char into ASCII
                for character in buildDate:
                    ASCII_values.append(ord(character))   
                ASCII_values.append(constant.CONST_SEPARATOR_CHARACTER)   # Seprator character ';'          
            
            #Extracting Build Time
            if re.search(k_buildTimeRegex, line):
                buildTime = re.search(k_buildTimeRegex, line).group(1)
                # Replacing space, comma, quotes form the Build Time
                for character in k_replaceCharacters:
                   buildTime = buildTime.replace(character, "")
                # Converting char into ASCII
                for character in buildTime:
                    ASCII_values.append(ord(character)) 
        
        #Appending Zeros for the remianing response byte
        for i in range(132-(len(ASCII_values))):
            ASCII_values.append(constant.CONST_APPEND_ZERO) #Appending '0' two times to make it equivalent to '0x00' because single '0' is considered as '0x0'
            ASCII_values.append(constant.CONST_APPEND_ZERO)

        #converting the ASCII values into hex
        for i in range(len(ASCII_values)):
            ASCII_values[i]=hex(ASCII_values[i])    
        
        #Converting the ASCII hex list into String
        hexStr = ""
        # traverse in the string  
        for ele in ASCII_values: 
           hexStr += ele  
        
        #character replacement in Hex String
        for character in k_replaceCharactersStr:
            hexStr = hexStr.replace(character, "") 
    return(hexStr)   
    
class CTestSuiteDiagBasic(testsuite.CTestSuite, CTestRunner):
    
    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteDiagBasic"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, self.getComponentName())
        
        # DemConf_DemEventParameter_RB_ECU_VBAT_UV                   85u
        self.faultEventIdRbECUVbatUV = 85

        
    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no Diag test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllDiagBasicTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])        

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "diag_basic"
             
    def runAllDiagBasicTests(self, t32_api):   
        # jump to Default Session as precondition for diag tests
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
                    
        localFilterList = ("swTest_measurement_cycle_sync_DIDWriteRead_MCSselector_from_diag;swTest_measurement_cycle_sync_DIDWriteRead_MCSselector_pdu;"
                           "swTest_measurement_cycle_sync_DIDWrite_requestoutofrange; swTest_mounting_position_DIDWriteRead;"
                           "swTest_mounting_position_DIDWrite_requestoutofrange;swTest_check_identification_DIDs; swTest_check_BoschFailureMemory_DID;"
                           "swTest_DiagSessionCntrl;swTest_checkClearDTC;swTest_checkReadDTC;swTest_TesterPresent;"
                           "swTest_check_BoschSwVersion_DIDs;"
                           "check_measurement_program_data_DIDRead_DefaultValue;"
                           "check_measurement_program_data_DIDUpdate_DefaultValue_afterReset;"
                           "check_measurement_program_data_DIDWriteRead_DMP00;"
                           "check_measurement_program_data_DIDWriteRead_DMP01;"
                           "check_measurement_program_data_DIDWriteRead_DMP03Invalid;"
                           "check_measurement_program_data_DIDWriteRead_inDMP02;"
                           "check_measurement_program_data_DIDWriteRead_invalid_DMPindex;"
                           "check_measurement_program_data_DIDWriteRead_invalid_DMPselector;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange1_DMP00;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange2_DMP00;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange_DMP00;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange1_DMP05;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange2_DMP05;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange_DMP05;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange1_DMPFFFF;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange2_DMPFFFF;"
                           "check_measurement_program_data_DIDWriteRead_invalid_velocityrange_DMPFFFF;"
                           "check_measurement_program_data_DIDWriteRead_DMP04;"
                           "check_measurement_program_data_DIDWriteRead_DMP05;"
                           "check_measurement_program_data_DIDWriteRead_DMP06Invalid;"
                           "check_measurement_program_data_DIDWriteRead_DMPFFFF_selector0;"
                           "check_measurement_program_data_DIDWriteRead_DMPFFFF_selector1;"
                           "check_measurement_program_data_write_defaultValue;"
                           "swTest_ControlDTCSetting;")
                           
        # We need the filter function by user, because some function are commented.
        # Once no function is commented the 'executeFilteredFunction' function may be used instead.         
        numberFailedTests = self.executeFilteredFunctionUser(t32_api, localFilterList)
                
        # Once the function shall be enabled, add it to the filter above or use 'executeFilteredFunction'
        #numberFailedTests += self.check_measurement_program(t32_api)
        #self.number_of_test += 1     

        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)
    
    ## @swtest_description The test case checks DiagnosticSessionControl service with subfunctions
    #  @swtest_step 
    #   1. Trigger default session request
    #   2. Check default session response
    #   3. Trigger Extended session request
    #   4. Check Extended session response
    #   5. Trigger Bosch session request
    #   6. Check Bosch session response
    # @swtest_expResult The positive response should be received for default,Extended and Bosch session        
    # @sw_requirement{SDC-R_SW_DIMA_90, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-90-00159bc2?doors.view=0000000b}
    # @sw_requirement{SDC-R_SW_DIMA_91, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-91-00159bc2?doors.view=0000000b}
    # @sw_requirement{SDC-R_SW_DIMA_92, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-92-00159bc2?doors.view=0000000b}
    def swTest_DiagSessionCntrl(self, t32_api):    
        numberFailedTests = 0
        numberTest = 1
		
        #1 Trigger default session request
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        Response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        
        #2 Check default session response
        default_session_response = Response[0:4]
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,default_session_response,  constant.CONST_DIAG_SESSION_CNTRL_DEFAULT_SESSION_RESP,
                                                 "Check default session response")
        
        numberTest += 1
         
        #3 Trigger Extended session request
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        Response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        
        #4 Check Extended session response
        Extended_session_response = Response[0:4]
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Extended_session_response, constant.CONST_DIAG_SESSION_CNTRL_EXTENDED_SESSION_RESP,
                                                 "Check Extended session response")
        
        numberTest += 1
        
        #5 Trigger Bosch session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        Response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        
        #6 Check Bosch session response
        Bosch_session_response = Response[0:4]
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,  Bosch_session_response, constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_RESP,
                                                "Check Bosch session response")
        
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description This test case check ClearDiagnosticInformation service 
    #  @swtest_step
    #    1. Precondition: Jump to default session and clear all stored DTCs
    #    2. Check that no DTCs are stored
    #    3. Activate DEM Test sequence
    #    4. Trigger faults which are mapped to DTC_UC_UNDER_VOLTAGE DTC
    #    5. Check that in the status byte of the triggered faults, the bits for DTC Test Failed , Pending or Confirmed are set for RB_ECU_VBAT_UV
    #    6. Check that the DTC- DTC_UC_UNDER_VOLTAGE  are set
    #    7. Making the fault to passive  which are mapped to DTC_UC_UNDER_VOLTAGE DTC
    #    8. Clear all DTC 
    #  @swtest_expResult All test steps are executed and passed..
    #  @sw_requirement{SDC-R_SW_DIMA_109,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-109-00159bc2?doors.view=0000000b}    
    def swTest_checkClearDTC(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        dtcTestFailedStatusBit = 0x1
        dtcPendingStatusBit = 0x4
        dtcConfirmedStatusBit = 0x8
        dtcTestFailedPendingConfirmedStatusBit = 0xD
        
        dtcStatusComb = (dtcTestFailedStatusBit, dtcPendingStatusBit, dtcConfirmedStatusBit, dtcTestFailedPendingConfirmedStatusBit)
        
        dtcTestFailedPendingConfirmedStatusMask = 0xD

        # Used FaultEventId to DTC mapping in this test
        # DTC_UC_UNDER_VOLTAGE - 15729430‬
        # RB_ECU_VBAT_UV
        
        # 1. jump to default session and clear DTCs
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        # ClearDiagnosticInformation (0x14) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Clear DTC response: {clearDtcResponse}")
         
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 1: Check Clear DTC Res")
        numberTest += 1
        
        # 2. make sure no other DTCs are present
        # Retrieving the list of DTCs that match a client defined status mask (sub-function = 0x02 reportDTCByStatusMask)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcbyStatusMask + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 2: Read DTC response: {dtcList}")
        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_diagReadDtcbyStatusMaskPositiveResponse + k_diagReadDtcInformationStatus, "Step 2: Check no DTC stored")
        numberTest += 1
        
        self.logger.debug(f"Step 2: Constant: {rbSysEvmConstant.k_demTestActicationSequence}")
        
        # 3. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Step 3: Check DEM Test Sequence activation")
        numberTest += 1  
        
        # 4. trigger faults which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)        
        time.sleep(0.5) # propagation and debounce
        
        # 5. check status byte: Test Failed or Pending or Confirmed for under voltage fault
        demStatusRbECUVbatUV = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRbECUVbatUV}]")    

        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, demStatusRbECUVbatUV['vvalue'].value & dtcTestFailedPendingConfirmedStatusMask, dtcStatusComb, "Step 5: Dem_AllEventsStatusByte for RbECUVbatUV")
        numberTest += 1
        
        
        # 6. check stored DTC for DTC_UC_UNDER_VOLTAGE
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcbyStatusMask + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_ucUnderVoltageDtcbyStatusResponse, "Step 6: DTC match for DTC_UC_UNDER_VOLTAGE")
        numberTest += 1
        
        # 7.making fault to passive which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)        
        time.sleep(0.5) # propagation and debounce
        
        # 8. clean up: clear DTCs  
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 8: Clear DTC response: {clearDtcResponse}")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 8: Check Clear DTC Res")
        
        return CTestCaseResult(numberTest, numberFailedTests)
        
    ## @swtest_description This test case check ReadDTCInformation service with subfunctions i.e reportNumberOfDTCByStatusMask,reportDTCByStatusMask and reportSupportedDTC
    #  @swtest_step
    #    1. Precondition: Jump to default session and clear all stored DTCs
    #    2. Check that no DTCs are stored
    #    3. Activate DEM Test sequence
    #    4. Trigger faults which are mapped to DTC_UC_UNDER_VOLTAGE DTC
    #    5. Check that in the status byte of the triggered faults, the bits for DTC Test Failed, Pending or Confirmed are set for RB_ECU_VBAT_UV
    #    6. Check DTC DTC_UC_UNDER_VOLTAGE is set using reportNumberofDTCbystatusmask  
    #    7. Check DTC DTC_UC_UNDER_VOLTAGE is set using reportDTCbystatusmask
    #    8. Making the fault to passive  which are mapped to DTC_UC_UNDER_VOLTAGE DTC
    #    9. Clear all DTC 
    #    10. Check list of All DTC's in the software using reportSupportedDTC  
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_111, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-111-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_126, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-126-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_127, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-127-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_196, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-196-00159bc2?doors.view=0000000b}    
    def swTest_checkReadDTC(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        dtcTestFailedStatusBit = 0x1
        dtcPendingStatusBit = 0x4
        dtcConfirmedStatusBit = 0x8
        dtcTestFailedPendingConfirmedStatusBit = 0xD
        
        dtcStatusComb = (dtcTestFailedStatusBit, dtcPendingStatusBit, dtcConfirmedStatusBit, dtcTestFailedPendingConfirmedStatusBit)
        
        dtcTestFailedPendingConfirmedStatusMask = 0xD

        # Used FaultEventId to DTC mapping in this test
        # DTC_UC_UNDER_VOLTAGE - 15729430‬
        # RB_ECU_VBAT_UV
        
        # 1. jump to default session and clear DTCs
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        # ClearDiagnosticInformation (0x14) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Clear DTC response: {clearDtcResponse}")
         
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 1: Check Clear DTC Res")
        numberTest += 1
        
        # 2. make sure no other DTCs are present
        # Retrieving the list of DTCs that match a client defined status mask (sub-function = 0x02 reportDTCByStatusMask)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcbyStatusMask + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 2: Read DTC response: {dtcList}")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_diagReadDtcbyStatusMaskPositiveResponse + k_diagReadDtcInformationStatus, "Step 2: Check no DTC stored")
        numberTest += 1
        
        # 3. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Step 3: Check DEM Test Sequence activation")
        numberTest += 1  
        
        # 4. trigger faults which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)        
        time.sleep(0.5) # propagation and debounce
        
        # 5. check status byte: DTC Test Failed or Pending or Confirmed for under voltage fault
        demStatusRbECUVbatUV = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRbECUVbatUV}]")    

        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, demStatusRbECUVbatUV['vvalue'].value & dtcTestFailedPendingConfirmedStatusMask, dtcStatusComb, "Step 5: Dem_AllEventsStatusByte for RbECUVbatUV")
        numberTest += 1
        
        # 6. check stored DTC for DTC_UC_UNDER_VOLTAGE using ReadNumberofDTCbyStatusMask sub function
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadNumberofDtcbyStatusMask + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_ucUnderVoltageNumberofDtcbyStatusResponse, "Step 6: DTC match for DTC_UC_UNDER_VOLTAGE using ReadNumberofDTCbyStatusMask")
        numberTest += 1
        
        # 7. check stored DTC for DTC_UC_UNDER_VOLTAGE using ReadDTCbyStatusMask sub function
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcbyStatusMask + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_ucUnderVoltageDtcbyStatusResponse, "Step 7: DTC match for DTC_UC_UNDER_VOLTAGE using ReadDTCbyStatusMask")
        numberTest += 1
        
        # 8.making fault to passive which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)        
        time.sleep(0.5) # propagation and debounce
        
        # 9. clean up: clear DTCs  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 9: Clear DTC response: {clearDtcResponse}")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 9: Check Clear DTC Res")
        numberTest += 1
        # 10. check all supported DTC's in the software
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagreportSupportedDTC, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_diagReadSupportedDTCsPositiveResponse+k_diagReadDtcInformationStatus+constant.CONST_SUPPORTED_DTC, "Step 10: All suported DTC's List")
      
            
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description This test case check TesterPresent service 
    #  @swtest_step
    #   1. Jump to default session and request Tester Present
    #  @swtest_expResult TesterPresent should send positive response.
    #  @sw_requirement{SDC-R_SW_DIMA_101,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-101-00159bc2?doors.view=0000000b}         
    def swTest_TesterPresent(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        # 1. jump to default session and request TesterPresent service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        # TesterPresent (0x3E) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_testerPresentRequest, self.logger)
        testerPresentRes = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, testerPresentRes,constant.CONST_TESTER_PRESENT_RES 
                                , "Check TesterPresent")
        
        return CTestCaseResult(numberTest, numberFailedTests)
                 
    def check_measurement_program(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        self.logger.info(f"RQM ID : {self.rqm.loc['Measurement Program','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['Measurement Program','LINK']}")        
        
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2EFD000001", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(5)
    
        measurementProgramIndex = t32_api.get_variable_value("rbDia_Measurement_program_Data_au8.m_dmpIndex")
    
        measurementProgramIndex_memPool = t32_api.get_variable_value(
            "scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_pool.m_values[2].elem.m_dmpIndex")
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, measurementProgramIndex_memPool['vvalue'].value, 
                                measurementProgramIndex['vvalue'].value, "Check Measurement Program")
        
        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description This test case check Measurement cycle synchronization write and read with MCS selector from diag 
    #  @swtest_step
    #    1. Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector
    #    2. Validate Write service response
    #    3. Read synchtype,sensortimeoffset and selector from NVM
    #    4. Read synchtype,sensortimeoffset and selector using diag read service
    #    5. Validate Read service response
    #    6. Check synchtype
    #    7. Check sensorTimeOffset
    #    8. Check MCSSelector   
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_649, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-649-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_650, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-650-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_645, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-645-00159bc2?doors.view=0000000b}    
    def swTest_measurement_cycle_sync_DIDWriteRead_MCSselector_from_diag(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
         
        #1.Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_UDS_WDBI_MCS_REQUEST_MCS_SELECTOR_DIAG, self.logger)
        writeMCSResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(5)
        
        #2. Validate response -> positive response
        writeResponseStatus = writeMCSResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MCS, "Check WDBI MCS - response")
        
        numberTest += 1
          
        #3.Read synchtype,sensortimeoffset and selector from NVM
        sensorTimeOffsetFourthbyte = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementCycleSynchronizationNVMDataItem[4]")['vvalue'].value,'02x')
        sensorTimeOffsetThirdbyte  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementCycleSynchronizationNVMDataItem[5]")['vvalue'].value,'02x')
        sensorTimeOffsetSecondbyte = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementCycleSynchronizationNVMDataItem[6]")['vvalue'].value,'02x')
        sensorTimeOffsetFirtsbyte  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementCycleSynchronizationNVMDataItem[7]")['vvalue'].value,'02x')
        
        synchtypenvmMirror         = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementCycleSynchronizationNVMDataItem[8]")['vvalue'].value,'02x')
        selectornvmMirror          = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementCycleSynchronizationNVMDataItem[9]")['vvalue'].value,'02x')
        
        sensorTimeoffsetnvmMirror = str(sensorTimeOffsetFirtsbyte) + str(sensorTimeOffsetSecondbyte) + str(sensorTimeOffsetThirdbyte) + str(sensorTimeOffsetFourthbyte)
        
        #4.Read synchtype,sensortimeoffset and selector using diag read service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_RDBI_MCS_REQUEST, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(0.5)  
        
        readResponseStatus = Read_DID[0:6]
        syncType           = Read_DID[6:8]
        sensorTimeOffset   = Read_DID[8:16]
        MCSSelector        = Read_DID[20:22]
        
        #5. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MCS, readResponseStatus,
                                                 "Check RBDI MCS - response")
        
        numberTest += 1 
        
        #6.Check synchtype
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, synchtypenvmMirror, syncType, 
                                                   "Check Measurement Cycle Sync - mcs sync type")            
        numberTest += 1            
       
        #7.Check sensorTimeOffset
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest,sensorTimeoffsetnvmMirror, sensorTimeOffset, 
                                                   "Check Measurement Cycle Sync - sensor time offset ")
        numberTest += 1    
       
        #8.Check MCSSelector
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, selectornvmMirror, MCSSelector, 
                                                   "Check Measurement Cycle Sync - MCSSelector")
        numberTest += 1     
          
        return CTestCaseResult(numberTest, numberFailedTests)
        
    ## @swtest_description This test case check Measurement cycle synchronization write and read with MCS selector from pdu
    #  @swtest_step
    #    1. Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector
    #    2. Validate Write service response 
    #    3. Read selector from NVM
    #    4. Read synchtype,sensortimeoffset and selector using diag read service
    #    5. Validate Read service response
    #    6. Check synchtype
    #    7. Check sensorTimeOffset
    #    8. Check MCSSelector   
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_648, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-648-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_647, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-647-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_646, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-646-00159bc2?doors.view=0000000b}
    def swTest_measurement_cycle_sync_DIDWriteRead_MCSselector_pdu(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
               
        #1.Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)   
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_UDS_WDBI_MCS_REQUEST_MCS_SELECTOR_PDU , self.logger)
        writeMCSResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        #canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(5)
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeMCSResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MCS, "Check WDBI MCS - response")
        
        numberTest += 1
            
        #3.Read selector from NVM
        selectornvmMirror           = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementCycleSynchronizationNVMDataItem[9]")['vvalue'].value,'02x')
        
        #4.Read synchtype,sensortimeoffset and selector using diag read service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_RDBI_MCS_REQUEST, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(0.5)  
        
        readResponseStatus = Read_DID[0:6]
        syncType           = Read_DID[6:8]
        sensorTimeOffset   = Read_DID[8:16]
        MCSSelector        = Read_DID[20:22]
        
        #5. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MCS, readResponseStatus,
                                                 "Check RBDI MCS - response")
        
        numberTest += 1  
         
        #6.Check synchtype
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, constant.CONST_SYNCHTYPE_NO_SYNCHTYPE_FROM_PDU, syncType, 
                                                   "Check Measurement Cycle Sync - mcs sync type")            
        numberTest += 1            
       
        #7.Check sensorTimeOffset
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest,constant.CONST_SENSORTIME_OFFSET_FROM_PDU, sensorTimeOffset, 
                                                   "Check Measurement Cycle Sync - sensor time offset ")
        numberTest += 1    
       
        #8.Check MCSSelector
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, selectornvmMirror, MCSSelector, 
                                                   "Check Measurement Cycle Sync - MCSSelector")
        numberTest += 1     
          
        return CTestCaseResult(numberTest, numberFailedTests)
      
    ## @swtest_description This test case check Measurement cycle synchronization write with invalid synchtype,sensortimeoffset and selector
    #  @swtest_step
    #    1. Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector
    #    2. check write response
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_651, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-651-00159bc2?doors.view=0000000b}
    def swTest_measurement_cycle_sync_DIDWrite_requestoutofrange(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
          
        #1.Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector         
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_UDS_WDBI_MCS_REQUEST_MCS_SELECTOR_WRONG, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")       
        time.sleep(0.5)   
      
        #2.check write response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Check Measurement Cycle Sync - DID response NRC")
    
        return CTestCaseResult(numberTest, numberFailedTests)

    
    ## @swtest_description This test case check read and write mounting positions parameters using diag service 
    #  @swtest_step
    #    1. Write Mounting postions data to NVM using WDBI service
    #    2. Validate write response -> positive response
    #    3. Read Mounting positions parameters from NVM
    #    4. Read mounting positions parameters using diag read service
    #    5. Validate read response -> positive response
    #    6. Check posX
    #    7. Check posY
    #    8. Check posZ   
    #    9. Check azimuth 
    #    10.Check elevation
    #    11.Check orientation
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_189, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-189-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_190, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-190-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_645, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-614-00159bc2?doors.view=0000000b} 
    #  @sw_requirement{SDC-R_SW_DIMA_191, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-191-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_192, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-192-00159bc2?doors.view=0000000b}
    def swTest_mounting_position_DIDWriteRead(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        #1.Write Mounting postions data to NVM using WDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_DID_REQ_MOUNTING_POSITION, self.logger) 
        writeMountingPosResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(5)
        
        
        #2. Validate response -> positive response
        writeResponseStatus = writeMountingPosResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MOUNTING_POSITION, "Check MOUNTING POS - response")
        
        numberTest += 1
    
        #3.Read Mounting positions parameters from NVM
        posXSecondbyte       = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[4]")['vvalue'].value,'02x')
        posXFirstbyte        = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[5]")['vvalue'].value,'02x')
        
        posYSecondbyte       = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[6]")['vvalue'].value,'02x')
        posYFirstbyte        = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[7]")['vvalue'].value,'02x')
        
        posZSecondbyte       = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[8]")['vvalue'].value,'02x')
        posZFirstbyte        = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[9]")['vvalue'].value,'02x')
        
        azimuthSecondbyte    = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[10]")['vvalue'].value,'02x')
        azimuthFirstbyte     = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[11]")['vvalue'].value,'02x')
        
        elevationSecondbyte  = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[12]")['vvalue'].value,'02x')
        elevationFirstbyte   = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[13]")['vvalue'].value,'02x')
        
        orientationnvmMirror          = format(t32_api.get_variable_value("g_NvMRamMirrorMountingPositionNVMDataItem[14]")['vvalue'].value,'02x')
        
        posXnvmMirror                 = str(posXFirstbyte) + str(posXSecondbyte)
        
        posYnvmMirror                 = str(posYFirstbyte) + str(posYSecondbyte)
        
        posZnvmMirror                 = str(posZFirstbyte) + str(posZSecondbyte)
        
        azimuthnvmMirror              = str(azimuthFirstbyte) + str(azimuthSecondbyte)
        
        elevationnvmMirror            = str(elevationFirstbyte) + str(elevationSecondbyte)
        
        #4.Read mounting positions parameters using diag read service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_DID_REQ_MOUNTING_POSITION, self.logger)
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(0.5)  
        
        readResponseStatus = Read_DID[0:6]
        posX               = Read_DID[6:10]
        posY               = Read_DID[10:14]
        posZ               = Read_DID[14:18]
        azimuth            = Read_DID[18:22]
        elevation          = Read_DID[22:26]
        orientation        = Read_DID[26:28]
        
        #5. Validate read response -> positive response
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,constant.CONST_READ_DID_RES_MOUNTING_POSITION, readResponseStatus,
                                                 "Check RBDI Mounting Position - response")
        
        numberTest += 1 
        
        #6.Check posX
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, posXnvmMirror, posX, 
                                                   "Mounting Position - Position X")            
        numberTest += 1                
   
        #7.Check posY
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, posYnvmMirror, posY, 
                                                   "Mounting Position - Position Y")
        numberTest += 1
    
        #8.Check posZ
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, posZnvmMirror, posZ, 
                                                   "Mounting Position - Position Z")            
        numberTest += 1   
            
        #9.Check azimuth
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, azimuthnvmMirror, azimuth, 
                                                   "Mounting Position - Azimuth")           
        numberTest += 1   
           
        #10.Check elevation
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,elevationnvmMirror, elevation, 
                                                   "Mounting Position - Elevation")
        numberTest += 1

        #11.Check orientation
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, orientationnvmMirror, 
                                                   orientation, "Mounting Position - Orientation")
        numberTest += 1
            
        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description This test case check invalid mounting position parameters 
    #  @swtest_step
    #    1. Write mounting position parameters
    #    2. check write response
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_DIMA_192, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-192-00159bc2?doors.view=0000000b}  
    def swTest_mounting_position_DIDWrite_requestoutofrange(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_DID_REQ_MOUNTING_POSITION1, self.logger) 
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(2)    
                
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Check Mounting Position - DID response NRC")            
        
        return CTestCaseResult(numberTest, numberFailedTests)


            
    ## @swtest_description The test case verifies the ECU identification data by executing the diagnostic read service for identification DIDs. 
    #  @swtest_step
    #   1. Jump to appropriate Session.
    #   2. Send the appropriate DID request.
    #  @swtest_expResult The read DID response must be equal to the expected value which is defined in the constants.
    #  @sw_requirement{SDC-R_SW_DIMA_593, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-593-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_592, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-592-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_623, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-623-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_627, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-627-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_779, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-779-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_770, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-770-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_775, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-775-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_783, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-783-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_932, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-932-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_936, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-936-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_941, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-941-00159bc2?doors.view=0000000b}
    def swTest_check_identification_DIDs(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        # Software Version is 24 bytes of Data
        # SW Version encoded in ASCII "xRR_LGU_PF_V11.0.0      "
        # Reading 18 bytes of software version form rbbuildversioncfg file
        ExpectedSoftwareVersion = getValuesfromrbBuildVersionCfg()
        ExpectedSoftwareVersion = ExpectedSoftwareVersion[6:40]
        ExpectedDID_F189_Val = constant.CONST_CUSTOMER_SOFTWARE_VERSION_DID_RESP + ExpectedSoftwareVersion +constant. CONST_SPACE_SW_VERSION_ENCODED_DATA
                                  
        
        ExpectedDID_EF13_Val = constant.CONST_ECU_HARDWARE_VERSION_DID_RESP
        ExpectedDID_F195_Val = constant.CONST_ECU_APPLICATION_SW_VERSION_DID_RESP
        ExpectedDID_F197_Val = constant.CONST_ECU_BOOT_SOFTWARE_VERSION_DID_RESP
        ExpectedDID_F18C_Val = constant.CONST_ECU_SERIAL_NUMBER_DID_RESP
        ExpectedDID_F18B_Val = constant.CONST_ECU_MANUFACTURING_DATE_DID_RESP
        ExpectedDID_F187_Val = constant.CONST_SUPPLIER_IDENTIFICATION_DID_RESP
        ExpectedDID_EF16_Val = constant.CONST_ECU_PLANT_CONTAINER_NUMBER_DID_RESP
        ExpectedDID_FDFF_Val = constant.CONST_SOFTWARE_TRAP_INFORMATION_DID_RESPONSE
        ExpectedDID_FDFA_Val = constant.CONST_OS_EXCEPTION_INFORMATION_DID_RESPONSE
        ExpectedDID_FDFB_Val = constant.CONST_SMU_ALARM_INFORMATION_DID_RESPONSE
        
        #DID F189 - Customer Software Version
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_CUSTOMER_SW_VERSION_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                 ExpectedDID_F189_Val, "Check DID F189 - Customer Software Version")
        numberTest += 1
        
        #DID EF13 - Hardware Sample Version
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_HW_VERSION_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_EF13_Val, "Check DID EF13 - Hardware Sample Version")
        numberTest += 1
        
        #DID F195 - Application Software Version
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_APP_SW_VERSION_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_F195_Val, "Check DID F195 - Application Software Version")
        numberTest += 1
    
        #DID F197 - Boot Software Number
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_BOOT_SW_VERSION_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_F197_Val, "Check DID F197 - Boot Software Number")
        
        numberTest += 1
        
        #DID F18B - ECU Manufacturing Date
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_ECU_MANUFACTURING_DATA_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_F18B_Val, "Check DID F18B - ECU Manufacturing Date")
        
        numberTest += 1

        #DID F18C - ECU Serial Number
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_ECU_SERIAL_NUMBER_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_F18C_Val, "Check DID F18C- ECU Serial Number")
        
        numberTest += 1
        
        #DID F187 - System Supplier Identifier
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_SUPPLIER_IDENTIFICATION_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_F187_Val, "Check DID F187- System Supplier Identifier")
        
        numberTest += 1


        #DID EF16 - ECU Plant Container Number
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)                  # Default Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_PLANT_CONTAINER_NUMBER_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_EF16_Val, "Check DID EF16- ECU Plant Container Number")
        
        numberTest += 1
        
        #DID FDFF - Software Trap Information 
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)        # Bosch Diag Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_SOFTWARE_TRAP_INFORMATION_REQUEST, self.logger)   # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_FDFF_Val, "Check DID FDFF- Software Trap Information")

        numberTest += 1
        
        #DID FDFA - OS Exception Log Information
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)        # Bosch Diag Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_OS_EXCEPTION_INFORMATION_REQUEST, self.logger)   # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_FDFA_Val, "Check DID FDFA- OS Exception Log Information")

        numberTest += 1
        
        #DID FDFB - SMU Alarm Information 
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)        # Bosch Diag Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_READ_DID_SMU_ALARM_INFORMATION_REQUEST, self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_FDFB_Val, "Check DID FDFB- SMU Alarm Information")

                                                        
        return CTestCaseResult(numberTest, numberFailedTests)

    
    ## @swtest_description The test case checks BoschSwVersion_DID 0xFD08. 
    #  @swtest_step
    #   1. Fetch the Bosch software build version information from getValuesfromrbBuildVersionCfg()
    #   2. Jump to appropriate Session.
    #   3. Send the appropriate DID request.
    #  @swtest_expResult The read DID response must be equal to the hex string data of Bosch software build version returned by the getValuesfromrbBuildVersionCfg().
    #  @sw_requirement{SDC-R_SW_DIMA_301, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-301-00159bc2?doors.view=0000000b}
    #  @sw_requirement{SDC-R_SW_DIMA_303, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-303-00159bc2?doors.view=0000000b}    
    def swTest_check_BoschSwVersion_DIDs(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        self.logger.info(f"FD08 RQM ID : {self.rqm.loc['FD08','ID']}")
        self.logger.debug(f"FD08 RQM LINK : {self.rqm.loc['FD08','LINK']}")
        
        ExpectedDID_FD08_Val = getValuesfromrbBuildVersionCfg()
        ExpectedDID_FD08_Val = ExpectedDID_FD08_Val[:165] # truncating time stamp as it it will always differ
    
        #DID FD08 - BOSCH Software Version
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,"1060", self.logger)       # Bosch Diag Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,"22FD08", self.logger)     # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        RxData = RxData[:165] # truncating time stamp as it it will always differ
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_FD08_Val, "Check DID FD08 - BOSCH Software Version")

        return CTestCaseResult(numberTest, numberFailedTests)
    
        
    ## @swtest_description The test case checks the read Bosch Failure Memory (0xFD19)DID. 
    #  @swtest_step
    #   1. Jump to appropriate Session.
    #   2. Send the appropriate DID request.
    #  @swtest_expResult The read DID response must give positive response
    #  @sw_requirement{SDC-R_SW_DIMA_712, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-712-00159bc2?doors.view=0000000b}
    def swTest_check_BoschFailureMemory_DID(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        ExpectedDID_FD19_Val = "62fd19"
        
        #DID FD19 - Read Bosch Failure Memory        
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,"1060", self.logger)        # Bosch Diag Session request
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,"22FD19", self.logger)      # Read DID request
        RxData = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        RxData = RxData[0:6]  #only checking the positive response 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, RxData,
                                                  ExpectedDID_FD19_Val, "Check DID FD19 - Read Bosch Failure Memory")
        
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case checks if Measurement Program default data is read as per the requirement.
    #  @swtest_step
    #   1. Read the default Measurement Program data from RAM packet.
    #   2. Validate the mempool data delivered.
    #   3. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_735, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-735-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_723, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-723-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_878, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-878-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_879, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-879-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_922, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-922-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_921, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-921-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_920, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-920-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_736, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-736-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_732, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-732-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_903, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-903-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDRead_DefaultValue(self, t32_api):

        numberFailedTests = 0
        numberTest = 1
        
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP00
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_2 
        
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP00

        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
                
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1
        
        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Default Measurement Program Index DMP00")
        numberTest += 1
      

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data for default value")

        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if Measurement Program default data is delivered to mempool after the reception of an invalid DMP index.
    #  @swtest_step
    #   1. Read the default Measurement Program data from RAM packet.
    #   2. Write DID 060C with a DMP index value 08 and DMP selector value 00.  
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_735, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-735-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_723, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-723-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_878, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-878-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_879, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-879-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_922, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-922-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_921, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-921-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_920, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-920-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_736, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-736-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_732, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-732-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_903, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-903-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_912, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-912-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_910, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-910-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDUpdate_DefaultValue_afterReset(self, t32_api):

        numberFailedTests = 0
        numberTest = 1
        
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP00
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_2 

        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000800FFFFFFFF00", self.logger) 
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(2)    
        
        
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP00

        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
    
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            

        numberTest += 1
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1
        
        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Default Measurement Program Index DMP00")
        numberTest += 1
      

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data for default value")

        return CTestCaseResult(numberTest, numberFailedTests)
                

    ## @swtest_description The test case checks if Measurement Program data is written and read for DMP00 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 00 and DMP selector value 00 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_885, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-885-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_886, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-886-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_887, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-887-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_888, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-888-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_DMP00(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
 
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP00
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_2   
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000000FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP00
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
    
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1

        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Measurement Program Index DMP00")
        numberTest += 1
        
        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data for DMP00")

        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if Measurement Program data is writte and read for DMP01 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 01 and DMP selector value 00 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_885, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-885-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_886, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-886-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_887, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-887-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_888, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-888-00159bc2?doors.view=00000004}
              
    def check_measurement_program_data_DIDWriteRead_DMP01(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
 
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP01
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_2 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000100FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_65_115KPH
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1

        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Measurement Program Index DMP00")
        numberTest += 1
 
        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data for DMP01")

        return CTestCaseResult(numberTest, numberFailedTests)


    ## @swtest_description The test case checks if Measurement Program data is written and read for DMP02 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 02 and DMP selector value 00 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_885, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-885-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_886, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-886-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_887, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-887-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_888, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-888-00159bc2?doors.view=00000004}
  
    def check_measurement_program_data_DIDWriteRead_inDMP02(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
 
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2     
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000200FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH

        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
      
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Measurement Program Index DMP02")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data DMP02")

        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid DMP index as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 07 and DMP selector value 00 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_721, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-721-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_DMPindex(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
  
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2            

        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000700FFFFFFFF00", self.logger) 
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(2)    
        

        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
        
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
      
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
        numberTest += 1
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index,dmp_index ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
        
        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid DMP selector as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 00 and DMP selector value 02 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_734, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-734-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_DMPselector(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

  
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
                
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000002FFFFFFFF00", self.logger) 
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(2)    
        

        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
        
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
    
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
        numberTest += 1
        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
        
        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range 1 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 00 and DMP selector value 00 with velocity range 1 as 30kph and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_904, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-904-00159bc2?doors.view=00000004}
    
    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange1_DMP00(self, t32_api):


  
       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2        
       numberFailedTests = 0
       numberTest = 1
        
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000000001EFFFF00", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
        
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
    
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
       numberTest += 1
        
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range 2 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 00 and DMP selector value 00 with velocity range 1 as 0xFFFF and velocity range 2 as 60kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_904, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-904-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange2_DMP00(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1
       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
        
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000000FFFF003C00", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
    
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
       numberTest += 1
        
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range  as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 00 and DMP selector value 00 with velocity range 1 as 30kph and velocity range 2 as 60kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_904, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-904-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange_DMP00(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1

       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2     
               
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000000001E003C00", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
       
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
        
       numberTest += 1
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)


    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range 1 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 05 and DMP selector value 00 with velocity range 1 as 60kph and velocity range 2 as 30kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_905, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-905-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_906, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-906-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange1_DMP05(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1

       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2      
               
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000500003C001E00", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
        
       numberTest += 1
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range 2 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 00 and DMP selector value 00 with velocity range 1 as 30kph and velocity range 2 as 400kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_905, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-905-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_906, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-906-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange2_DMP05(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1

       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
               
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000500001E019000", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
       
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
       numberTest += 1
        
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range 1 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 0xFFFF and DMP selector value 00 with velocity range 1 as 60kph and velocity range 2 as 30kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_908, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-908-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_909, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-909-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange1_DMPFFFF(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1

       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
                 
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060CFFFF00003C001E00", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
       numberTest += 1
        
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range 2 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 0xffff and DMP selector value 00 with velocity range 1 as 30kph and velocity range 2 as 400kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_908, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-908-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_909, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-909-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange2_DMPFFFF(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1
 
       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
               
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060CFFFF00001E019000", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
       numberTest += 1
        
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range  as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 0xFFFF and DMP selector value 00 with velocity range 1 as 0xFFFF and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_908, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-908-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_909, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-909-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange_DMPFFFF(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1

       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
               
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060CFFFF00FFFFFFFF00", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
       numberTest += 1
        
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid velocity range  as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 05 and DMP selector value 00 with velocity range 1 as 30kph and velocity range 2 as 30kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_905, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-905-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_906, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-906-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_invalid_velocityrange_DMP05(self, t32_api):
    
       numberFailedTests = 0
       numberTest = 1

       dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
       dmp_index = constant.CONST_DIAG_UDS_DID_DMP02
       dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
       dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
               
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
       canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000500001e001e00", self.logger) 
       DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
       time.sleep(2)    
        

       ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_30_60KPH
       
       mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
       mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
       mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
       mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
       mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
       mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
       mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
       mp_index = str(mp_index_msb) + str(mp_index_lsb)
       mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
       mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
        
       numberTest += 1
        
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                  "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
       numberTest += 1
           
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
       numberTest += 1
            
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                 "Check Measurement Program Data - Previous valid Velocity Range 1")
       numberTest += 1

       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
       numberTest += 1


       #Deliver Measurement Program DID data
       m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP02")
       numberTest += 1

       m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
       numberTest += 1


       m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
       numberTest += 1


       m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
       numberTest += 1

        
       #Read Measurement Program data            
       canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
       canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
       Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
       time.sleep(2)     
    
       numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
       
       return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if Measurement Program data is written and read for DMP04 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 04 and DMP selector value 00 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_885, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-885-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_886, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-886-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_887, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-887-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_888, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-888-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_DMP04(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
 
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP04
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_2   
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000400FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP04
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Measurement Program Index DMP04")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data for DMP04")

        return CTestCaseResult(numberTest, numberFailedTests)


     
    ## @swtest_description The test case checks if Measurement Program data is writte and read for DMP05 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 05 and DMP selector value 00 with velocity range 1 as 100kph and velocity range 2 as 150kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_732, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-732-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_903, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-903-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_567, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-567-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_727, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-727-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_733, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-733-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_717, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-717-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_882, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-882-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_880, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-880-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_883, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-883-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_881, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-881-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_907, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-907-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_DMP05(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
 
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP05
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP05_100KPH_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP05_150KPH_VELOCITY_RANGE_2  
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C0005000064009600", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_100_150KPH
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Measurement Program Index DMP02")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data DMP05")

        return CTestCaseResult(numberTest, numberFailedTests)
 

    ## @swtest_description The test case checks if Measurement Program data is written and read for DMPFF as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value FFFF and DMP selector value 00 with velocity range 1 as 30kph and velocity range 2 as 60kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_723, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-723-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_922, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-922-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_902, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-902-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_889, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-889-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_DMPFFFF_selector0(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
 
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP05
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2   
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060CFFFF00001E003C00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_30_60KPH
    
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Measurement Program Index DMP02")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")

        return CTestCaseResult(numberTest, numberFailedTests)

    
    ## @swtest_description The test case checks if Measurement Program data is writte and read for DMPFF as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value FFFF and DMP selector value 01 with velocity range 1 as 30kph and velocity range 2 as 60kph.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_716, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-716-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_726, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-726-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_902, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-902-00159bc2?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_DIMA_889, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-889-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_DMPFFFF_selector1(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
 
        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_1
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP05
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_30KPH_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_60KPH_VELOCITY_RANGE_2  
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060CFFFF01001E003C00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP00_30_60KPH
    
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
      
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index, "Measurement Program Index DMP02")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector, "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")

        return CTestCaseResult(numberTest, numberFailedTests)

 
    ## @swtest_description The test case checks if negative response code is obtained for an invalid DMP index 3 as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 03 and DMP selector value 00 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response. 
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_721, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-721-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_DMP03Invalid(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP01
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP_DEFAULT_VELOCITY_RANGE_2   
                
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000300FFFFFFFF00", self.logger) 
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(2)    
        

        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_65_115KPH
        
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
        numberTest += 1
        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector , 
                                                   "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index  ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1  , 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2 , 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value, dmp_index , "Previous Measurement Program Index DMP01")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1 , "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value, dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
        
        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description The test case checks if negative response code is obtained for an invalid DMP index as per the requirement.
    #  @swtest_step
    #   1. Write DID 060C with a DMP index value 06 and DMP selector value 00 with velocity range 1 and velocity range 2 as 0xFFFF.
    #   2. Read the Measurement Program data from RAM packet.
    #   3. Validate the mempool data delivered.
    #   4. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_721, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-721-00159bc2?doors.view=00000004}

    def check_measurement_program_data_DIDWriteRead_DMP06Invalid(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

        dmp_selector = constant.CONST_DIAG_UDS_DID_DMP_SELECTOR_0
        dmp_index = constant.CONST_DIAG_UDS_DID_DMP05
        dmp_velocity_range1 = constant.CONST_DIAG_UDS_DID_DMP05_100KPH_VELOCITY_RANGE_1
        dmp_velocity_range2 = constant.CONST_DIAG_UDS_DID_DMP05_150KPH_VELOCITY_RANGE_2 
                
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000600FFFFFFFF00", self.logger) 
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")   
        time.sleep(2)    
        

        ExpectedData = constant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_100_150KPH
        
    
        mp_selector  = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[10]")['vvalue'].value,'02x')
        mp_index_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[5]")['vvalue'].value,'02x')
        mp_index_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[4]")['vvalue'].value,'02x')
        mp_velocity_range1_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[7]")['vvalue'].value,'02x')
        mp_velocity_range1_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[6]")['vvalue'].value,'02x')
        mp_velocity_range2_msb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[9]")['vvalue'].value,'02x')
        mp_velocity_range2_lsb = format(t32_api.get_variable_value("g_NvMRamMirrorMeasurementProgramNVMDataItem[8]")['vvalue'].value,'02x')
     
        mp_index = str(mp_index_msb) + str(mp_index_lsb)
        mp_velocity_range1 = str(mp_velocity_range1_msb) + str(mp_velocity_range1_lsb)
        mp_velocity_range2 = str(mp_velocity_range2_msb) + str(mp_velocity_range2_lsb)
                
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Measurement Program Data -Invalid DMP Index - DID response NRC")            
        numberTest += 1
        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_selector, dmp_selector, 
                                                   "Check Measurement Program Data - Previous valid Measurement Program Selector ")             
        numberTest += 1
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_index, dmp_index ,
                                                   "Check Measurement Program Data - Previous valid Measurement Program Index")
        numberTest += 1
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range1,dmp_velocity_range1 , 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 1")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, mp_velocity_range2, dmp_velocity_range2, 
                                                   "Check Measurement Program Data - Previous valid Velocity Range 2")
        numberTest += 1


        #Deliver Measurement Program DID data
        m_dmpIndex_Value =format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramDIDdata")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpIndex_Value,dmp_index , "Previous Measurement Program Index DMP05")
        numberTest += 1

        m_dmpSelector_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_measurementProgramSelector")['vvalue'].value,'02x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_dmpSelector_Value,dmp_selector , "Measurement Program Selector")
        numberTest += 1


        m_velocityrange1_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange1_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange1_Value, dmp_velocity_range1, "Velocity Range 1")
        numberTest += 1


        m_velocityrange2_Value = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_diag_x_diaRunnable_m_measurementProgramDIDdata_out_local.m_arrayPool[0].elem.m_velocityRange2_kph")['vvalue'].value,'04x')
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, m_velocityrange2_Value , dmp_velocity_range2, "Velocity Range 2")
        numberTest += 1

        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, ExpectedData, "Read DID Measurement Program data")
        
        return CTestCaseResult(numberTest, numberFailedTests)
     
    ## @swtest_description This test case check Control DTC Setting service 
    #  @swtest_step
    #   1. Jump to extended session and request Control DTC Setting ON service
    #   2. Trigger a DEM Failure and check the Read DTC by Status Mask information
    #   3. Make the failure passive
    #   4. Jump to extended session and request Control DTC Setting OFF service
    #   5. Trigger a DEM failure and check the Read DTC by Status Mask information
    #   6. Make the failure passive and clear DTCs
    #  @swtest_expResult Control DTC Setting ON should send positive response and no DTC shall log.Similarly, Control DTC Off request shall allow logging of DTC.
    #  @sw_requirement{SDC-R_SW_DIMA_103,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-103-00159bc2?doors.view=0000000b}         
    def swTest_ControlDTCSetting(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        # 1. jump to extended session and request control DTC setting OFF service
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # Control DTC Setting (0x85) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_controlDTCSettingOff, self.logger)
        controlDTCSettingRes = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, controlDTCSettingRes,constant.CONST_CONTROL_DTC_SETTING_OFF_RES 
                                , "Check Control DTC Setting Off")
        
        numberTest += 1

        self.logger.debug(f"Step 2: Constant: {rbSysEvmConstant.k_demTestActicationSequence}")
        
        # 2. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Step 2: Check DEM Test Sequence activation")
        numberTest += 1  
        
               
        # 3. trigger faults which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)        
        time.sleep(0.5) # propagation and debounce

        # 4. Check there is no DTC is triggered
        # Retrieving the list of DTCs that match a client defined status mask (sub-function = 0x02 reportDTCByStatusMask)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcbyStatusMask + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 4: Read DTC response: {dtcList}")
               
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_diagReadDtcbyStatusMaskPositiveResponse + k_diagReadDtcInformationStatus, "Step 4: Check no DTC stored")
        numberTest += 1
 
        # 5.making fault to passive which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)        
        time.sleep(0.5) # propagation and debounce
           
        # 6. jump to extended session and request control DTC setting On service
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        # Control DTC Setting (0x85) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_controlDTCSettingOn, self.logger)
        controlDTCSettingRes = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")

               
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, controlDTCSettingRes,constant.CONST_CONTROL_DTC_SETTING_ON_RES 
                                , "Check Control DTC Setting On")
 
        numberTest += 1
        
        self.logger.debug(f"Step 7: Constant: {rbSysEvmConstant.k_demTestActicationSequence}")
        
        # 7. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Step 7: Check DEM Test Sequence activation")
        numberTest += 1  
        
        # 8. trigger faults which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)        
        time.sleep(0.5) # propagation and debounce

        # 9. check stored DTC for DTC_UC_UNDER_VOLTAGE
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcbyStatusMask + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_ucUnderVoltageDtcbyStatusResponse, "Step 9: DTC match for DTC_UC_UNDER_VOLTAGE")
        numberTest += 1
        
        # 10.making fault to passive which are mapped to DTC_UC_UNDER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.faultEventIdRbECUVbatUV, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)        
        time.sleep(0.5) # propagation and debounce
        
        # 11. clean up: clear DTCs  
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 11: Clear DTC response: {clearDtcResponse}")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 11: Check Clear DTC Res")
               
        return CTestCaseResult(numberTest, numberFailedTests)
        
        
        
    ## @swtest_description The test case is to reset the Measurement Program DID to default data as per the requirement.
    #  @swtest_step
    #   1. Write the default Measurement Program data to NVM.
    #   2. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_DIMA_735, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-735-00159bc2?doors.view=00000004}
    def check_measurement_program_data_write_defaultValue(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

        # 1. Write the default Measurement Program data to NVM  
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_WRITE_DID_REQ_DMP05_65_115KPH, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP") 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_DIAG_UDS_WRITE_RESP_DMP, 
                                                   f"DMP response {constant.CONST_DIAG_UDS_WRITE_RESP_DMP}")
        numberTest += 1

        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_WRITE_DID_REQ_DMP00, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP") 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, constant.CONST_DIAG_UDS_WRITE_RESP_DMP, 
                                                   f"DMP response {constant.CONST_DIAG_UDS_WRITE_RESP_DMP}") 
        numberTest += 1

        # 2. Verify Read DID  060C response.           
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DIAG_UDS_READ_RESP_DMP, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, constant.CONST_DIAG_UDS_READ_DID_RESP_DMP00, "Read default DID Measurement Program data")

        return CTestCaseResult(numberTest, numberFailedTests)
       
               