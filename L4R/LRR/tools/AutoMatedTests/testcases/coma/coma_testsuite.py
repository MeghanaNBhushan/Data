# -*- coding: utf-8 -*-

import sys
import time
import os
import math
import datetime
import ctypes
import re

sys.path.append(os.path.abspath('../../framework/helper'))
sys.path.append(os.path.abspath('../../framework/scheduling'))
sys.path.append(os.path.abspath('../../framework/interface'))
sys.path.append(os.path.abspath('../diag'))
 

import atf_toolbox as testHelper
import atf_testasserts as testasserts
import AD_lauterbach_test_helper as lauterbachTestHelper
import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants
import AD_canoe_diag_functions as canoeDiagPanel
import diag_constants as diagConstant
import vama_constants as vamaConstant

import coma_constants as constant
from testbase import CTestCaseResult

# constants used in test cases for verification
k_customerVersionMajorNumberRegex = 'SW_VERSION_MAJOR_NUMBER ([0-9]*)U'
k_customerVersionMinorNumberRegex = 'SW_VERSION_MINOR_NUMBER ([0-9]*)U'
k_customerVersionPatchNumberRegex = 'SW_VERSION_PATCH_NUMBER ([0-9]*)U'
k_firstByteMask = ctypes.c_uint32(0x000000ff)
k_secondByteMask = ctypes.c_uint32(0x0000ff00)
k_thirdByteMask = ctypes.c_uint32(0x00ff0000)
k_fourthByteMask = ctypes.c_uint32(0xff000000)
k_maxOneByte = 0xff
k_maxThreeByte = 0xffffff
k_SwCustVersion  = 1536

rbBuildVersionFile = open('./../../../generatedFiles/rbBuild_Version_Cfg.h', 'r') 
k_lgpVersion = rbBuildVersionFile.readlines()[35][27:35]
k_lguSensorstateStbmTimeMin = 0
k_lguSensorstateStbmTimeMax = 4294967295


class CTestSuiteComa(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteComa"), canoe_api, t32_api, relay_api, hw,
                         globalTestcaseFilter, self.getComponentName())

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no coma test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllComaTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "coma"

    def runAllComaTests(self, t32_api):
        #numberFailedTests = self.executeFilteredFunction(t32_api)   

        # We need the filter function by user, because some function are commented.
        #Once no function is commented the 'executeFilteredFunction' function may be used instead. 
        localFilterList = ("swTest_LGP_RX_Message_Sensor_Mode_Request;swTest_LGP_RX_Message_Measurement_Program;swTest_LGP_RX_Message_Measurement_Cycle_Synchronization;swTest_LGP_RX_Message_EgoData;"
        "swTest_SensorFeedbackPDU_commParams;swTest_locationAttributePDU_commParams;swTest_locationData0PDU_commParams;swTest_Time_Syn;swTest_Sensorstinfo_commParams;swTest_SensorBroadcastPDU_commParams_sigValidation")
        
        numberFailedTests = self.executeFilteredFunctionUser(t32_api, localFilterList)
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)

    ## Function to convert a decimal value into hex using the 2's compliment menthod
    def tohex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))
      
    ## @swtest_description The test case checks if Sensor Mode Request PDU data is received and updated in COM buffer , DADDY port as per the data on the communication bus
    #  @swtest_step
    #   1. Set SenModReq_RadMod with value "Start Modulation".
    #   2. Validate the data received in COM local buffer.
    #   3. Validate the data delivered in DADDY port.
    #   4. Set SenModReq_RadMod with value "Stop Modulation".
    #   5. Validate the data received in COM local buffer.
    #   6. Validate the data delivered in DADDY port.
    #   7. Set SenModReq_RadMod with value "Resume Modulation".
    #   8. Validate the data received in COM local buffer.
    #   9. Validate the data delivered in DADDY port.
    #   10. Set SenModReq_RadMod with value "Suspend Modulation".
    #   11. Validate the data received in COM local buffer.
    #   12. Validate the data delivered in DADDY port.
    #   13. Set SenModReq_RadMod with 7 "Invalid Value".
    #   14. Validate the data received in COM local buffer.
    #   15. Validate the data delivered in DADDY port.
    #  @swtest_expResult SW variables shall be updated with the valid values received from the communication bus immediately. 
    #  @sw_requirement{SDC-R_SW_COMA_1184, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1184-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1185, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1185-00159bc3?doors.view=00000004}
    
    def swTest_LGP_RX_Message_Sensor_Mode_Request(self, t32_api):
        number_failed_tests = 0
        number_test = 1
       
       # Step 1:From RBS LGP on Eth Panel, send sensor mode request data = 1(start modultation)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 2: Validate the data received in COM local buffer
        sensorMode_Request = 1

        m_sensorMode_request = t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_SensorModeRequest_InputByte[0]");
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "start modultation")
        number_test += 1
       
       # Step 3: Validate the data delivered in DADDY port

        m_sensorMode_request = t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_sensorModeRequest_out_local.m_arrayPool[0].elem.m_sensorModeRequest")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "start modultation")
        number_test += 1

       # Step 4:From RBS LGP on Eth Panel, send sensor mode request data = 2(stop modultation)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", 2)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
        time.sleep(0.5)

       # Step 5: Validate the data received in COM local buffer
        sensorMode_Request = 2
        
        m_sensorMode_request = t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_SensorModeRequest_InputByte[0]")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "stop modultation")
        number_test += 1
       
       # Step 6: Validate the data delivered in DADDY port

        m_sensorMode_request = t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_sensorModeRequest_out_local.m_arrayPool[0].elem.m_sensorModeRequest")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "stop modultation")
        number_test += 1
          
       # Step 7:From RBS LGP on Eth Panel, send sensor mode request data = 3(Resume modultation)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", 3)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
        time.sleep(0.5)

       # Step 8: Validate the data received in COM local buffer
        sensorMode_Request = 3

        m_sensorMode_request = t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_SensorModeRequest_InputByte[0]")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "Resume modultation")
        number_test += 1
       
       # Step 9: Validate the data delivered in DADDY port
        
        m_sensorMode_request = t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_sensorModeRequest_out_local.m_arrayPool[0].elem.m_sensorModeRequest")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "Resume modultation")
        number_test += 1

       # Step 10:From RBS LGP on Eth Panel, send sensor mode request data = 4(Suspend modultation)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", 4)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
        time.sleep(0.5)

       # Step 11: Validate the data received in COM local buffer
        sensorMode_Request = 4

        m_sensorMode_request = t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_SensorModeRequest_InputByte[0]")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "Suspend modultation")
        number_test += 1
       
       # Step 12: Validate the data delivered in DADDY port
        m_sensorMode_request = t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_sensorModeRequest_out_local.m_arrayPool[0].elem.m_sensorModeRequest")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "Suspend modultation")
        number_test += 1          

       # Step 13:From RBS LGP on Eth Panel, send sensor mode request data = 7(Invalid Value)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", 7)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
        time.sleep(0.5)

       # Step 14: Validate the data received in COM local buffer
        sensorMode_Request_com_buffer = 7
        sensorMode_Request = 0

        m_sensorMode_request = t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_SensorModeRequest_InputByte[0]")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request_com_buffer , "Com buffer Value 7")
        number_test += 1
       
       # Step 15: Validate the data delivered in DADDY port
        m_sensorMode_request = t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_sensorModeRequest_out_local.m_arrayPool[0].elem.m_sensorModeRequest")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorMode_request['vvalue'].value, sensorMode_Request , "Invalid Value")

        return CTestCaseResult(number_test, number_failed_tests)

        
    ## @swtest_description The test case checks if Measurement Program PDU data is received and updated in COM buffer , DADDY port as per the data on the communication bus
    #  @swtest_step
    #   1. Set MeasurementProgram_Input with value "DMP00".
    #   2. Validate the data received in COM local buffer.
    #   3. Validate the data delivered in DADDY port.
    #   4. Set MeasurementProgram_Input with value "DMP01".
    #   5. Validate the data received in COM local buffer.
    #   6. Validate the data delivered in DADDY port.
    #   7. Set MeasurementProgram_Input with value "DMP02".
    #   8. Validate the data received in COM local buffer.
    #   9. Validate the data delivered in DADDY port.
    #   10. Set MeasurementProgram_Input with value "DMP04".
    #   11. Validate the data received in COM local buffer.
    #   12. Validate the data delivered in DADDY port.
    #   13. Set MeasurementProgram_Input with value "DMP05".
    #   14. Validate the data received in COM local buffer.
    #   15. Validate the data delivered in DADDY port.
    #   16. Set MeasurementProgram_Input with value "DMPFF".
    #   17. Validate the data received in COM local buffer.
    #   18. Validate the data delivered in DADDY port.
    #   19. Set MeasurementProgram_Input with value 7.
    #   20. Validate the data received in COM local buffer.
    #   21. Validate the data delivered in DADDY port.    
    #  @swtest_expResult SW variables shall be updated with the valid values received from the communication bus immediately. 
    #  @sw_requirement{SDC-R_SW_COMA_1207, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1207-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1217, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1217-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1237, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1237-00159bc3?doors.view=00000004}
    
    def swTest_LGP_RX_Message_Measurement_Program(self, t32_api):
        number_failed_tests = 0
        number_test = 1
       
       # Step 1:From RBS LGP on Eth Panel, send Measurement Program Index as 0 through PDU(DMP00)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 2: Validate the data received in COM local buffer
        m_measurement_pgm = diagConstant.CONST_DIAG_UDS_DID_DMP00

        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP00")
        number_test += 1
       
       # Step 3: Validate the data delivered in DADDY port

        m_measPgm_byte = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_measurementProgramPDUdata_out_local.m_arrayPool[0].elem.m_measurementProgramIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP00")
        number_test += 1

       # Step 4:From RBS LGP on Eth Panel, send Measurement Program Index as 1 through PDU(DMP01)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 5: Validate the data received in COM local buffer
        m_measurement_pgm = diagConstant.CONST_DIAG_UDS_DID_DMP01

        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP01")
        number_test += 1
       
       # Step 6: Validate the data delivered in DADDY port

        m_measPgm_byte = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_measurementProgramPDUdata_out_local.m_arrayPool[0].elem.m_measurementProgramIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP01")
        number_test += 1

       # Step 7:From RBS LGP on Eth Panel, send Measurement Program Index as 2 through PDU(DMP02)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 2)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 8: Validate the data received in COM local buffer
        m_measurement_pgm = diagConstant.CONST_DIAG_UDS_DID_DMP02

        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP02")
        number_test += 1
       
       # Step 9: Validate the data delivered in DADDY port

        m_measPgm_byte = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_measurementProgramPDUdata_out_local.m_arrayPool[0].elem.m_measurementProgramIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP02")
        number_test += 1

       # Step 10:From RBS LGP on Eth Panel, send Measurement Program Index as 4 through PDU(DMP04)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 4)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 11: Validate the data received in COM local buffer
        m_measurement_pgm = diagConstant.CONST_DIAG_UDS_DID_DMP04

        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP04")
        number_test += 1
       
       # Step 12: Validate the data delivered in DADDY port

        m_measPgm_byte = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_measurementProgramPDUdata_out_local.m_arrayPool[0].elem.m_measurementProgramIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP04")
        number_test += 1
        
       # Step 13:From RBS LGP on Eth Panel, send Measurement Program Index as 5 through PDU(DMP05)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 5)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 14: Validate the data received in COM local buffer
        m_measurement_pgm = diagConstant.CONST_DIAG_UDS_DID_DMP05

        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP05")
        number_test += 1
       
       # Step 15: Validate the data delivered in DADDY port

        m_measPgm_byte = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_measurementProgramPDUdata_out_local.m_arrayPool[0].elem.m_measurementProgramIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMP05")
        number_test += 1

       # Step 16:From RBS LGP on Eth Panel, send Measurement Program Index as 65535 through PDU(DMPFF)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 65535)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 17: Validate the data received in COM local buffer
        m_measurement_pgm = constant.CONST_MEAS_PGM_MAX_VALUE_PDU

        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMPFF")
        number_test += 1
       
       # Step 18: Validate the data delivered in DADDY port

        m_measPgm_byte = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_measurementProgramPDUdata_out_local.m_arrayPool[0].elem.m_measurementProgramIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "DMPFF")
        number_test += 1

       # Step 19:From RBS LGP on Eth Panel, send Measurement Program Index as 7 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 7)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
          
       # Step 20: Validate the data received in COM local buffer
        m_measurement_pgm = "0007"

        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "Invalid value 7")
        number_test += 1
       
       # Step 21: Validate the data delivered in DADDY port

        m_measPgm_byte = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_measurementProgramPDUdata_out_local.m_arrayPool[0].elem.m_measurementProgramIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_measPgm_byte, m_measurement_pgm , "Invalid value 7")

        return CTestCaseResult(number_test, number_failed_tests)




    ## @swtest_description The test case checks if MCS PDU data is received and updated in COM buffer,DADDY port as per the data on the communication bus
    #  @swtest_step
    #   1. Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector to read MCS data from PDU.
    #   2. Set MCS_SyncType with value 0 and MCS_SenTimeOff with value "0 ms".
    #   3. Validate the data received in COM local buffer.
    #   4. Validate the data delivered in DADDY port.
    #   5. Set MCS_SyncType with value 1 "Time Slot Synchronization" and MCS_SenTimeOff with value 22ms.
    #   6. Validate the data received in COM local buffer.
    #   7. Validate the data delivered in DADDY port.
    #   8. Set MCS_SyncType with value 1 "Time Slot Synchronization" and MCS_SenTimeOff with value 44ms.
    #   9. Validate the data received in COM local buffer.
    #   10. Validate the data delivered in DADDY port.
    #   11. Set MCS_SyncType with value 0 "Time Slot Synchronization" and MCS_SenTimeOff with value 44ms.
    #   12. Validate the data received in COM local buffer.
    #   13. Validate the data delivered in DADDY port sync type and sensor time offset members should be 0
    #   14. Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector to read MCS data from DID.
    #   15. Set MCS_SyncType with value 0 "Time Slot Synchronization" and MCS_SenTimeOff with non-zero value.
    #   16. Validate the data delivered in DADDY port sync type and sensor time offset members should be 0
    #  @swtest_expResult SW variables shall be updated with the valid values received from the communication bus immediately. 
    #  @sw_requirement{SDC-R_SW_COMA_1137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1137-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1140, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1140-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1264, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1264-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1138, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1138-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1280, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1280-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1281, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1281-00159bc3?doors.view=00000004}
    
    def swTest_LGP_RX_Message_Measurement_Cycle_Synchronization(self, t32_api):
        number_failed_tests = 0
        number_test = 1
       
       # Step 1:Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)   
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,diagConstant.CONST_DIAG_UDS_WDBI_MCS_REQUEST_MCS_SELECTOR_PDU , self.logger)
        writeMCSResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
       
       # Step 2:From RBS LGP on Eth Panel, set MCS_SyncType with value 0 and MCS_SenTimeOff with value 0.
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)
          
       # Step 3: Validate the data received in COM local buffer
        m_synctype_expected = constant.CONST_NO_SYNCHTYPE
        m_sensortimeoffset_expected = constant.CONST_SENSORTIME_0_MILLI_SECONDS_PDU
        
        m_sensorTimeOffset_first_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[1]")['vvalue'].value,'02x')
        m_sensorTimeOffset_second_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[2]")['vvalue'].value,'02x')
        m_sensorTimeOffset_third_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[3]")['vvalue'].value,'02x')
        m_sensorTimeOffset_fourth_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[4]")['vvalue'].value,'02x')
        
        m_synctype_received  =  format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[0]")['vvalue'].value,'02x')      
        m_sensorTimeOffset_received = str(m_sensorTimeOffset_first_byte) + str(m_sensorTimeOffset_second_byte)+ str(m_sensorTimeOffset_third_byte)+ str(m_sensorTimeOffset_fourth_byte)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensortimeoffset_expected, m_sensorTimeOffset_received , "Sensor Time Offset 0ms")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_expected, m_synctype_received , "Synchronization Type 0")
        number_test += 1  

       # Step 4: Validate the data delivered in DADDY port

        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected , "Sensor Time Offset 0ms")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorSyncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 0")
        number_test += 1

        m_sensortimeoffset_expected_dsp = constant.CONST_DSP_SENSORTIME_0_MILLI_SECONDS_PDU
        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected_dsp , "Sensor Time Offset 0ms")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 0")
        number_test += 1
             
       # Step 5:From RBS LGP on Eth Panel, set MCS_SyncType with value 1 and MCS_SenTimeOff with value 22 milliseconds.
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff", 22000000)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)
          
       # Step 6: Validate the data received in COM local buffer
        m_synctype_expected = constant.CONST_TIME_SLOT_SYNCHTYPE
        m_sensortimeoffset_expected = constant.CONST_SENSORTIME_22_MILLI_SECONDS_PDU
        
        m_sensorTimeOffset_first_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[1]")['vvalue'].value,'02x')
        m_sensorTimeOffset_second_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[2]")['vvalue'].value,'02x')
        m_sensorTimeOffset_third_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[3]")['vvalue'].value,'02x')
        m_sensorTimeOffset_fourth_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[4]")['vvalue'].value,'02x')
        
        m_synctype_received  =  format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[0]")['vvalue'].value,'02x')      
        m_sensorTimeOffset_received = str(m_sensorTimeOffset_first_byte) + str(m_sensorTimeOffset_second_byte)+ str(m_sensorTimeOffset_third_byte)+ str(m_sensorTimeOffset_fourth_byte)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensortimeoffset_expected, m_sensorTimeOffset_received , "Sensor Time Offset 22ms")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_expected, m_synctype_received , "Synchronization Type 1")
        number_test += 1  

       # Step 7: Validate the data delivered in DADDY port

        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected , "Sensor Time Offset 22ms")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorSyncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 1")
        number_test += 1
        
        m_sensortimeoffset_expected_dsp = constant.CONST_DSP_SENSORTIME_11_MILLI_SECONDS_PDU
        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected_dsp , "Sensor Time Offset 11ms")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 1")
        number_test += 1
             

       # Step 8:From RBS LGP on Eth Panel, set MCS_SyncType with value 1 and MCS_SenTimeOff with value 44milliseconds.
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff", 44000000)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)
          
       # Step 9: Validate the data received in COM local buffer
        m_synctype_expected = constant.CONST_TIME_SLOT_SYNCHTYPE
        m_sensortimeoffset_expected = constant.CONST_SENSORTIME_44_MILLI_SECONDS_PDU
        
        m_sensorTimeOffset_first_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[1]")['vvalue'].value,'02x')
        m_sensorTimeOffset_second_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[2]")['vvalue'].value,'02x')
        m_sensorTimeOffset_third_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[3]")['vvalue'].value,'02x')
        m_sensorTimeOffset_fourth_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[4]")['vvalue'].value,'02x')
        
        m_synctype_received  =  format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[0]")['vvalue'].value,'02x')      
        m_sensorTimeOffset_received = str(m_sensorTimeOffset_first_byte) + str(m_sensorTimeOffset_second_byte)+ str(m_sensorTimeOffset_third_byte)+ str(m_sensorTimeOffset_fourth_byte)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensortimeoffset_expected, m_sensorTimeOffset_received , "Sensor Time Offset 44ms")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_expected, m_synctype_received , "Synchronization Type 1")
        number_test += 1  

       # Step 10: Validate the data delivered in DADDY port

        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected , "Sensor Time Offset 44ms")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorSyncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 0")
        number_test += 1


        m_sensortimeoffset_expected_dsp = constant.CONST_DSP_SENSORTIME_22_MILLI_SECONDS_PDU
        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected_dsp , "Sensor Time Offset 22ms.")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 1")
        number_test += 1

        # Step 11:From RBS LGP on Eth Panel, set MCS_SyncType with value 0 and MCS_SenTimeOff with value 44milliseconds.
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff", 44000000)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)
          
       # Step 12: Validate the data received in COM local buffer
        m_synctype_expected = constant.CONST_NO_SYNCHTYPE
        m_sensortimeoffset_comBuff_expected = constant.CONST_SENSORTIME_44_MILLI_SECONDS_PDU
        m_sensortimeoffset_expected = constant.CONST_SENSORTIME_0_MILLI_SECONDS_PDU
        
        m_sensorTimeOffset_first_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[1]")['vvalue'].value,'02x')
        m_sensorTimeOffset_second_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[2]")['vvalue'].value,'02x')
        m_sensorTimeOffset_third_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[3]")['vvalue'].value,'02x')
        m_sensorTimeOffset_fourth_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[4]")['vvalue'].value,'02x')
        
        m_synctype_received  =  format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[0]")['vvalue'].value,'02x')      
        m_sensorTimeOffset_received = str(m_sensorTimeOffset_first_byte) + str(m_sensorTimeOffset_second_byte)+ str(m_sensorTimeOffset_third_byte)+ str(m_sensorTimeOffset_fourth_byte)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensortimeoffset_comBuff_expected, m_sensorTimeOffset_received , "Sensor Time Offset 44ms")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_expected, m_synctype_received , "Synchronization Type 0")
        number_test += 1  

       # Step 13: Validate the data delivered in DADDY port sync type and sensor time offset members should be 0

        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected , "Sensor Time Offset 0ms")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorSyncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 0")
        number_test += 1


        m_sensortimeoffset_expected_dsp = constant.CONST_DSP_SENSORTIME_0_MILLI_SECONDS_PDU
        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected_dsp , "Sensor Time Offset 0ms.")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 0")
        number_test += 1

       # Step 14:Write MCS data to NVM using WDBI service with synchtype,sensortimeoffset and selector
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)   
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,diagConstant.CONST_DIAG_UDS_WDBI_MCS_REQUEST_MCS_SELECTOR_PDU , self.logger)
        writeMCSResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        time.sleep(2)
          
       # Step 15: Set MCS_SyncType with value 0 "Time Slot Synchronization" and MCS_SenTimeOff with non-zero value.
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            diagConstant.CONST_SYNCHTYPE_NO_SYNCHTYPE_FROM_PDU + diagConstant.CONST_SENSORTIME_OFFSET + diagConstant.CONST_MCS_DUMMY \
                + diagConstant.CONST_MCS_SELECTOR_DIAG
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)

        m_synctype_expected = constant.CONST_NO_SYNCHTYPE
        m_sensortimeoffset_expected = constant.CONST_SENSORTIME_0_MILLI_SECONDS_PDU 

       # Step 16: Validate the data delivered in DADDY port sync type and sensor time offset members should be 0

        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected , "Sensor Time Offset 0ms")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_inputHandlerSensorSyncData_out_local.m_arrayPool[0].elem.m_sensorSyncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 0")
        number_test += 1


        m_sensortimeoffset_expected_dsp = constant.CONST_DSP_SENSORTIME_0_MILLI_SECONDS_PDU
        m_sensorTimeOffset_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")['vvalue'].value,'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_sensorTimeOffset_received, m_sensortimeoffset_expected_dsp , "Sensor Time Offset 0ms.")
        number_test += 1
        m_synctype_received = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_synctype_received, m_synctype_expected , "Sensor Synchronization Type 0")
        
        return CTestCaseResult(number_test, number_failed_tests)
        



        
    ## @swtest_description The test case checks if Ego Vehicle Data PDU  is received and updated in COM buffer,DADDY port as per the data on the communication bus
    #  @swtest_step
    #   1. Set minimum value for all signals,EgoData_VehSpd with -100m/s,EgoData_RelYawRate with -114.59deg/s,EgoData_VehSpdStdDev with -128m/s,EgoData_LogAcc with -16m/s2 .
    #   2. Validate the data received in COM local buffer.
    #   3. Validate the data delivered in DADDY port.
    #   4. Set maximum value for all signals,EgoData_VehSpd with 100m/s,EgoData_RelYawRate with 114.59deg/s,EgoData_VehSpdStdDev with 127.99m/s,EgoData_LogAcc with 15.99m/s2 .
    #   5. Validate the data received in COM local buffer.
    #   6. Validate the data delivered in DADDY port.
    #   7. Set a valid value for all signals,EgoData_VehSpd with 50m/s,EgoData_RelYawRate with 100deg/s,EgoData_VehSpdStdDev with 70m/s,EgoData_LogAcc with 10m/s2 .
    #   8. Validate the data received in COM local buffer.
    #   9. Validate the data delivered in DADDY port.
    #   10. Set an out of range value which exceeds minimum value for all signals,EgoData_VehSpd with -130m/s,EgoData_RelYawRate with -120deg/s,EgoData_VehSpdStdDev with -130m/s,EgoData_LogAcc with -20m/s2 .
    #   11. Validate the data received in COM local buffer.
    #   12. Validate the data delivered in DADDY port.
    #   13. Set an out of range value which exceeds maximum value for all signals,EgoData_VehSpd with 130m/s,EgoData_RelYawRate with 120deg/s,EgoData_VehSpdStdDev with 130m/s,EgoData_LogAcc with 20m/s2 .
    #   14. Validate the data received in COM local buffer.
    #   15. Validate the data delivered in DADDY port.
    #  @swtest_expResult SW variables shall be updated with the valid values received from the communication bus immediately. 
    #  @sw_requirement{SDC-R_SW_COMA_1103, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1103-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1102, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1102-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1132, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1132-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1885, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1885-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1892, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1892-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1888, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1888-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1890, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1890-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1886, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1886-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1893, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1893-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1887, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1887-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1894, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1894-00159bc0?doors.view=00000004}   
    def swTest_LGP_RX_Message_EgoData(self, t32_api):
        number_failed_tests = 0
        number_test = 1
       
       # Step 1:From RBS LGP on Eth Panel, send EgoData_VehSpd with -100m/s,EgoData_RelYawRate with -114.59deg/s,EgoData_VehSpdStdDev with -128m/s,EgoData_LogAcc with -16m/s2.
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", -100.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", -114.59)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", -128.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", -16.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
          
       # Step 2: Validate the data received in COM local buffer
        m_EgoData_VehSpd = constant.CONST_EGO_VEHICLE_SPEED_MINVALUE
        m_EgoData_RelYawRate = constant.CONST_EGO_VEHICLE_YAW_RATE_MINVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_EGO_VEHICLE_SPEED_DEV_MINVALUE
        m_EgoData_LogAcc = constant.CONST_EGO_VEHICLE_ACCEL_MINVALUE
        
        m_EgoData_RelYawRate_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[0]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[1]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[2]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[3]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com = str(m_EgoData_RelYawRate_com_byte0) + str(m_EgoData_RelYawRate_com_byte1) + str(m_EgoData_RelYawRate_com_byte2) + str(m_EgoData_RelYawRate_com_byte3)

        m_EgoData_VehSpd_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[4]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[5]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[6]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[7]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com = str(m_EgoData_VehSpd_com_byte0) + str(m_EgoData_VehSpd_com_byte1) + str(m_EgoData_VehSpd_com_byte2) + str(m_EgoData_VehSpd_com_byte3)
        
        m_EgoData_VehSpdStdDev_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[8]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[9]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[10]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[11]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com = str(m_EgoData_VehSpdStdDev_com_byte0) + str(m_EgoData_VehSpdStdDev_com_byte1) + str(m_EgoData_VehSpdStdDev_com_byte2) + str(m_EgoData_VehSpdStdDev_com_byte3)

        m_EgoData_LogAcc_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[12]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[13]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[14]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[15]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com = str(m_EgoData_LogAcc_com_byte0) + str(m_EgoData_LogAcc_com_byte1) + str(m_EgoData_LogAcc_com_byte2) + str(m_EgoData_LogAcc_com_byte3)

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_com, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_com, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_com, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1      
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_com, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1 
        
                
       # Step 3: Validate the data delivered in DADDY port

        m_EgoData_VehSpd = constant.CONST_DSP_EGO_VEHICLE_SPEED_MINVALUE
        m_EgoData_RelYawRate = constant.CONST_DSP_EGO_VEHICLE_YAW_RATE_MINVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_DSP_EGO_VEHICLE_SPEED_DEV_MINVALUE
        m_EgoData_LogAcc = constant.CONST_DSP_EGO_VEHICLE_ACCEL_MINVALUE
        
        m_EgoData_VehSpd_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_daddy, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1

        m_EgoData_RelYawRate_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.psiDtOpt_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_daddy, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1

        m_EgoData_VehSpdStdDev_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRefErr_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_daddy, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1

        m_EgoData_LogAcc_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.axvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_daddy, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1
       
       # Step 4:From RBS LGP on Eth Panel, send EgoData_VehSpd with 100m/s,EgoData_RelYawRate with 114.59deg/s,EgoData_VehSpdStdDev with 127.99m/s,EgoData_LogAcc with 15.99m/s2
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 100.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", 114.59)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", 127.99)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", 15.99)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)

       # Step 5: Validate the data received in COM local buffer
        m_EgoData_VehSpd = constant.CONST_EGO_VEHICLE_SPEED_MAXVALUE
        m_EgoData_RelYawRate = constant.CONST_EGO_VEHICLE_YAW_RATE_MAXVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_EGO_VEHICLE_SPEED_DEV_MAXVALUE
        m_EgoData_LogAcc = constant.CONST_EGO_VEHICLE_ACCEL_MAXVALUE
        
        m_EgoData_RelYawRate_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[0]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[1]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[2]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[3]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com = str(m_EgoData_RelYawRate_com_byte0) + str(m_EgoData_RelYawRate_com_byte1) + str(m_EgoData_RelYawRate_com_byte2) + str(m_EgoData_RelYawRate_com_byte3)

        m_EgoData_VehSpd_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[4]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[5]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[6]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[7]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com = str(m_EgoData_VehSpd_com_byte0) + str(m_EgoData_VehSpd_com_byte1) + str(m_EgoData_VehSpd_com_byte2) + str(m_EgoData_VehSpd_com_byte3)
        
        m_EgoData_VehSpdStdDev_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[8]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[9]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[10]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[11]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com = str(m_EgoData_VehSpdStdDev_com_byte0) + str(m_EgoData_VehSpdStdDev_com_byte1) + str(m_EgoData_VehSpdStdDev_com_byte2) + str(m_EgoData_VehSpdStdDev_com_byte3)

        m_EgoData_LogAcc_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[12]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[13]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[14]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[15]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com = str(m_EgoData_LogAcc_com_byte0) + str(m_EgoData_LogAcc_com_byte1) + str(m_EgoData_LogAcc_com_byte2) + str(m_EgoData_LogAcc_com_byte3)

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_com, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_com, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_com, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1      
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_com, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1 
        
       
       # Step 6: Validate the data delivered in DADDY port

        m_EgoData_VehSpd = constant.CONST_DSP_EGO_VEHICLE_SPEED_MAXVALUE
        m_EgoData_RelYawRate = constant.CONST_DSP_EGO_VEHICLE_YAW_RATE_MAXVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_DSP_EGO_VEHICLE_SPEED_DEV_MAXVALUE
        m_EgoData_LogAcc = constant.CONST_DSP_EGO_VEHICLE_ACCEL_MAXVALUE
        
        m_EgoData_VehSpd_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_daddy, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1

        m_EgoData_RelYawRate_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.psiDtOpt_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_daddy, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1

        m_EgoData_VehSpdStdDev_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRefErr_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_daddy, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1

        m_EgoData_LogAcc_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.axvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_daddy, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1
         
              
       # Step 7:From RBS LGP on Eth Panel, send EgoData_VehSpd with 50m/s,EgoData_RelYawRate with 100deg/s,EgoData_VehSpdStdDev with 70m/s,EgoData_LogAcc with 10m/s2
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 50.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", 100.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", 70.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", 10.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)

       # Step 8: Validate the data received in COM local buffer
        m_EgoData_VehSpd = constant.CONST_EGO_VEHICLE_SPEED_MIDVALUE
        m_EgoData_RelYawRate = constant.CONST_EGO_VEHICLE_YAW_RATE_MIDVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_EGO_VEHICLE_SPEED_DEV_MIDVALUE
        m_EgoData_LogAcc = constant.CONST_EGO_VEHICLE_ACCEL_MIDVALUE
        
        m_EgoData_RelYawRate_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[0]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[1]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[2]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[3]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com = str(m_EgoData_RelYawRate_com_byte0) + str(m_EgoData_RelYawRate_com_byte1) + str(m_EgoData_RelYawRate_com_byte2) + str(m_EgoData_RelYawRate_com_byte3)

        m_EgoData_VehSpd_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[4]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[5]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[6]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[7]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com = str(m_EgoData_VehSpd_com_byte0) + str(m_EgoData_VehSpd_com_byte1) + str(m_EgoData_VehSpd_com_byte2) + str(m_EgoData_VehSpd_com_byte3)
        
        m_EgoData_VehSpdStdDev_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[8]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[9]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[10]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[11]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com = str(m_EgoData_VehSpdStdDev_com_byte0) + str(m_EgoData_VehSpdStdDev_com_byte1) + str(m_EgoData_VehSpdStdDev_com_byte2) + str(m_EgoData_VehSpdStdDev_com_byte3)

        m_EgoData_LogAcc_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[12]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[13]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[14]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[15]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com = str(m_EgoData_LogAcc_com_byte0) + str(m_EgoData_LogAcc_com_byte1) + str(m_EgoData_LogAcc_com_byte2) + str(m_EgoData_LogAcc_com_byte3)

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_com, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_com, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_com, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1      
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_com, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1 
        
       # Step 9: Validate the data delivered in DADDY port
        
        m_EgoData_VehSpd = constant.CONST_DSP_EGO_VEHICLE_SPEED_MIDVALUE
        m_EgoData_RelYawRate = constant.CONST_DSP_EGO_VEHICLE_YAW_RATE_MIDVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_DSP_EGO_VEHICLE_SPEED_DEV_MIDVALUE
        m_EgoData_LogAcc = constant.CONST_DSP_EGO_VEHICLE_ACCEL_MIDVALUE
        
        m_EgoData_VehSpd_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_daddy, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1

        m_EgoData_RelYawRate_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.psiDtOpt_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_daddy, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1

        m_EgoData_VehSpdStdDev_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRefErr_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_daddy, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1

        m_EgoData_LogAcc_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.axvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_daddy, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1
       
               
       # Step 10:From RBS LGP on Eth Panel, send EgoData_VehSpd with -130m/s,EgoData_RelYawRate with -120deg/s,EgoData_VehSpdStdDev with -130m/s,EgoData_LogAcc with -20m/s2 
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", -130.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", -120.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", -130.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", -20.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)

       # Step 11: Validate the data received in COM local buffer
        m_EgoData_VehSpd = constant.CONST_EGO_VEHICLE_SPEED_BEYONDMINVALUE
        m_EgoData_RelYawRate = constant.CONST_EGO_VEHICLE_YAW_RATE_BEYONDMINVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_EGO_VEHICLE_SPEED_DEV_BEYONDMINVALUE
        m_EgoData_LogAcc = constant.CONST_EGO_VEHICLE_ACCEL_BEYONDMINVALUE
        
        m_EgoData_RelYawRate_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[0]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[1]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[2]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[3]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com = str(m_EgoData_RelYawRate_com_byte0) + str(m_EgoData_RelYawRate_com_byte1) + str(m_EgoData_RelYawRate_com_byte2) + str(m_EgoData_RelYawRate_com_byte3)

        m_EgoData_VehSpd_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[4]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[5]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[6]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[7]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com = str(m_EgoData_VehSpd_com_byte0) + str(m_EgoData_VehSpd_com_byte1) + str(m_EgoData_VehSpd_com_byte2) + str(m_EgoData_VehSpd_com_byte3)
        
        m_EgoData_VehSpdStdDev_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[8]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[9]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[10]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[11]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com = str(m_EgoData_VehSpdStdDev_com_byte0) + str(m_EgoData_VehSpdStdDev_com_byte1) + str(m_EgoData_VehSpdStdDev_com_byte2) + str(m_EgoData_VehSpdStdDev_com_byte3)

        m_EgoData_LogAcc_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[12]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[13]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[14]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[15]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com = str(m_EgoData_LogAcc_com_byte0) + str(m_EgoData_LogAcc_com_byte1) + str(m_EgoData_LogAcc_com_byte2) + str(m_EgoData_LogAcc_com_byte3)

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_com, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_com, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_com, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1      
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_com, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1 
        
       
       # Step 12: Validate the data delivered in DADDY port

        m_EgoData_VehSpd = constant.CONST_DSP_EGO_VEHICLE_SPEED_BEYONDMIN
        m_EgoData_RelYawRate = constant.CONST_DSP_EGO_VEHICLE_YAW_RATE_BEYONDMIN
        m_EgoData_VehSpdStdDev = constant.CONST_DSP_EGO_VEHICLE_SPEED_DEV_BEYONDMIN
        m_EgoData_LogAcc = constant.CONST_DSP_EGO_VEHICLE_ACCEL_BEYONDMIN
        
        m_EgoData_VehSpd_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_daddy, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1

        m_EgoData_RelYawRate_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.psiDtOpt_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_daddy, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1

        m_EgoData_VehSpdStdDev_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRefErr_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_daddy, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1

        m_EgoData_LogAcc_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.axvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_daddy, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1
       
        
       # Step 13:From RBS LGP on Eth Panel, send EgoData_VehSpd with 130m/s,EgoData_RelYawRate with 120deg/s,EgoData_VehSpdStdDev with 130m/s,EgoData_LogAcc with 20m/s2 
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 130.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", 120.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", 130.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", 20.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        
        
       # Step 14: Validate the data received in COM local buffer
        m_EgoData_VehSpd = constant.CONST_EGO_VEHICLE_SPEED_BEYONDMAXVALUE
        m_EgoData_RelYawRate = constant.CONST_EGO_VEHICLE_YAW_RATE_BEYONDMAXVALUE
        m_EgoData_VehSpdStdDev = constant.CONST_EGO_VEHICLE_SPEED_DEV_BEYONDMAXVALUE
        m_EgoData_LogAcc = constant.CONST_EGO_VEHICLE_ACCEL_BEYONDMAXVALUE
        
        m_EgoData_RelYawRate_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[0]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[1]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[2]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[3]")['vvalue'].value,'02x')
        m_EgoData_RelYawRate_com = str(m_EgoData_RelYawRate_com_byte0) + str(m_EgoData_RelYawRate_com_byte1) + str(m_EgoData_RelYawRate_com_byte2) + str(m_EgoData_RelYawRate_com_byte3)

        m_EgoData_VehSpd_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[4]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[5]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[6]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[7]")['vvalue'].value,'02x')
        m_EgoData_VehSpd_com = str(m_EgoData_VehSpd_com_byte0) + str(m_EgoData_VehSpd_com_byte1) + str(m_EgoData_VehSpd_com_byte2) + str(m_EgoData_VehSpd_com_byte3)
        
        m_EgoData_VehSpdStdDev_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[8]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[9]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[10]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[11]")['vvalue'].value,'02x')
        m_EgoData_VehSpdStdDev_com = str(m_EgoData_VehSpdStdDev_com_byte0) + str(m_EgoData_VehSpdStdDev_com_byte1) + str(m_EgoData_VehSpdStdDev_com_byte2) + str(m_EgoData_VehSpdStdDev_com_byte3)

        m_EgoData_LogAcc_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[12]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[13]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[14]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_EgoVehData_InputByte[15]")['vvalue'].value,'02x')
        m_EgoData_LogAcc_com = str(m_EgoData_LogAcc_com_byte0) + str(m_EgoData_LogAcc_com_byte1) + str(m_EgoData_LogAcc_com_byte2) + str(m_EgoData_LogAcc_com_byte3)

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_com, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_com, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_com, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1      
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_com, m_EgoData_LogAcc , "EgoData_LogAcc")
        number_test += 1 
        
       # Step 15: Validate the data delivered in DADDY port

        m_EgoData_VehSpd = constant.CONST_DSP_EGO_VEHICLE_SPEED_BEYONDMAX
        m_EgoData_RelYawRate = constant.CONST_DSP_EGO_VEHICLE_YAW_RATE_BEYONDMAX
        m_EgoData_VehSpdStdDev = constant.CONST_DSP_EGO_VEHICLE_SPEED_DEV_BEYONDMAX
        m_EgoData_LogAcc = constant.CONST_DSP_EGO_VEHICLE_ACCEL_BEYONDMAX
        
        m_EgoData_VehSpd_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpd_daddy, m_EgoData_VehSpd , "EgoData_VehSpd")
        number_test += 1

        m_EgoData_RelYawRate_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.psiDtOpt_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_RelYawRate_daddy, m_EgoData_RelYawRate , "EgoData_RelYawRate")
        number_test += 1

        m_EgoData_VehSpdStdDev_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRefErr_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_VehSpdStdDev_daddy, m_EgoData_VehSpdStdDev , "EgoData_VehSpdStdDev")
        number_test += 1

        m_EgoData_LogAcc_daddy = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.axvRef_sw")['vvalue'].value
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_EgoData_LogAcc_daddy, m_EgoData_LogAcc , "EgoData_LogAcc")
       
        
        return CTestCaseResult(number_test, number_failed_tests)

    # Guard checks - to ensure if Location PDUs are constantly received from radar on bus 
    # Function description - Reset the PDU_NAME sys var value to clear. Set the PDU_CycleCount to 5 cycles.Set the correspondong PDU
    #                        to check if the PDU is being transmitted or not. Wait for 5 cycles of the PDU transmission and read the PDU_NAME
    # Return Value -
    #               True  - if isReadData value is ReadyToReadData, implying, the PDU has been sent for 5 consecutive cycles
    #               False - if isReadData value not ReadyToReadData, implying, the PDU is not transmitted by Radar periodically
    def isTxPduSentFromRadar(self, pduName, maxCycleTime):
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  constant.CONST_CLEAR_ENUM)
        
        self.canoe_api.setSysVarValue("swTesting", "PDU_CycleCount",  5)
        
        self.canoe_api.setSysVarValue_withoutDelay("swTesting", "PDU_NAME",  pduName)
        
        time.sleep(math.ceil((maxCycleTime*0.0001)*5))
        
        isReadData = self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")
        
        return (isReadData == constant.CONST_READY_TO_READDATA_ENUM)
        
    ## @swtest_description The test case checks if communication parameters of Location attributes is as per specification
    #  @swtest_step
    #   1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
    #   2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::locationAttributes(0)
    #   3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
    #   4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
    #   5. Read the below parameters from the system variable swTesting::PDU_NAME and verify the same as per LGP Spec
    #       a. Source and Destination MAC Address
    #       b. Source and Destination Port Number
    #       c. Source and Destination IP Address
    #       d. PDU ID
    #       e. PDU Length
    #       f. PDU Average cycle time(20 cycle taken for averaging)
    #  @swtest_expResult The Communication Parameters of Location attribute PDU must be as per LGP Specifications
    #  @sw_requirement{SDC-R_SW_COMA_1242, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1242-00159bc3}
    def swTest_locationAttributePDU_commParams(self, t32_api):
        number_failed_tests = 0
        number_test = 1
        
        if( not self.isTxPduSentFromRadar(constant.CONST_LOCATION_ATTRIBUTE_ENUM,constant.CONST_LOCATION_ATTRIBUTE_CYCLETIME_MAX)):
            self.logger.debug("Location Attribute PDU not recieved at RBS!! Check Communication manually ")
            number_failed_tests = 1
            return CTestCaseResult(number_test, number_failed_tests)

        # 1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  constant.CONST_CLEAR_ENUM)
        time.sleep(1)
        
        # 2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::locationAttributes(0)
        self.canoe_api.setSysVarValue_withoutDelay("swTesting", "PDU_NAME",  constant.CONST_LOCATION_ATTRIBUTE_ENUM)
        time.sleep(0.5)
        
        # 3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
        while(self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")== constant.CONST_LOCATION_ATTRIBUTE_ENUM):
            continue
            
        isReadData = self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")
        
        # 4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, isReadData, constant.CONST_READY_TO_READDATA_ENUM, "Verify if PDU_NAME is ReadyToReadData(-1)")
        number_test += 1
        
        # 5. Read the below parameters from the system variable swTesting::PDU_NAME
        
        # verify Source MAC Address from Bus
        sourceMAC = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourceMac")
        number_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceMAC), constant.CONST_DEFAULT_SOURCE_MAC_ADDRESS, "Verify Source MAC Address"))
        number_test += 1
        
        # verify Source Port Number from Bus
        sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
        number_test += 1
        
        # verify Source IP Address from Bus 
        sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_SOURCE_IP_ADDRESS, "Verify Source IP Address")
        number_test += 1
        
        # verify Destination MAC Address from Bus
        destMACAddress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestMac")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destMACAddress), constant.CONST_DEFAULT_DEST_MAC_ADDRESS, "Verify Destination MAC Address")
        number_test += 1
        
        # verify Destination Port Number from Bus
        destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destPort), constant.CONST_DEFAULT_DEST_PORT_NUMBER, "Verify Destination Port Number")
        number_test += 1
        
        # verify Destination IP Address from Bus 
        destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destIPAdrress), constant.CONST_DEFAULT_DEST_IP_ADDRESS, "Verify Destination IP Address")
        number_test += 1
                
        # verify PDU ID from Bus 
        pduID = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_ID")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(pduID), constant.CONST_LOCATION_ATTRIBUTE_PDU_ID, "Verify PDU ID")
        number_test += 1

        # verify PDU Length from Bus 
        pduLen = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_Length")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, pduLen, constant.CONST_LOCATION_ATTRIBUTE_PDU_LEN, "Verify PDU length")
        number_test += 1
        
        # verify PDU Cycle time on Bus 
        pduCycleTime = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "AvgCycleTime")
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_LOCATION_ATTRIBUTE_CYCLETIME_MIN, "Verify if cycle time is greater than min cycle time")
        number_test += 1
        
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_LOCATION_ATTRIBUTE_CYCLETIME_MAX, "Verify if cycle time is lesser than max cycle time")
        
        return CTestCaseResult(number_test, number_failed_tests)
        
    ## @swtest_description The test case checks if communication parameters of Location Data_0 PDU is as per specification
    #  @swtest_step
    #   1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
    #   2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::locationData0(1)
    #   3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
    #   4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
    #   5. Read the below parameters from the system variable swTesting::PDU_NAME and verify the same as per LGP Spec
    #       a. Source and Destination MAC Address
    #       b. Source and Destination Port Number
    #       c. Source and Destination IP Address
    #       d. PDU ID
    #       e. PDU Length
    #       f. PDU Average cycle time(20 cycle taken for averaging)
    #  @swtest_expResult The Communication Parameters of Location Data_0 PDU must be as per LGP Specifications
    #  @sw_requirement{SDC-R_SW_COMA_1241, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/?urn=urn:rational::1-4147106800294823-O-1241-00159bc3}
    #  @sw_requirement{SDC-R_SW_COMA_1107, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/?urn=urn:rational::1-4147106800294823-O-1107-00159bc3}
    def swTest_locationData0PDU_commParams(self, t32_api):
        number_failed_tests = 0
        number_test = 1
        
        if( not self.isTxPduSentFromRadar(constant.CONST_LOCATION_DATA0_ENUM,constant.CONST_LOCATION_DATA0_CYCLETIME_MAX)):
            self.logger.debug("Location Data PDU not recieved at RBS!! Check Communication manually ")
            number_failed_tests = 1
            return CTestCaseResult(number_test, number_failed_tests)

        # 1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  constant.CONST_CLEAR_ENUM)
        time.sleep(1)
        
        # 2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::locationData0(1)
        self.canoe_api.setSysVarValue_withoutDelay("swTesting", "PDU_NAME",  constant.CONST_LOCATION_DATA0_ENUM)
        time.sleep(0.5)
        
        # 3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
        while(self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")== constant.CONST_LOCATION_DATA0_ENUM):
            continue
            
        isReadData = self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")
        
        # 4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, isReadData, constant.CONST_READY_TO_READDATA_ENUM, "Verify if PDU_NAME is ReadyToReadData(-1)")
        number_test += 1
        
        # 5. Read the below parameters from the system variable swTesting::PDU_NAME
        
        # verify Source MAC Address from Bus
        sourceMAC = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourceMac")
        number_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceMAC), constant.CONST_DEFAULT_SOURCE_MAC_ADDRESS, "Verify Source MAC Address"))
        number_test += 1
        
        # verify Source Port Number from Bus
        sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
        number_test += 1
        
        # verify Source IP Address from Bus 
        sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_SOURCE_IP_ADDRESS, "Verify Source IP Address")
        number_test += 1
        
        # verify Destination MAC Address from Bus
        destMACAddress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestMac")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destMACAddress), constant.CONST_DEFAULT_DEST_MAC_ADDRESS, "Verify Destination MAC Address")
        number_test += 1
        
        # verify Destination Port Number from Bus
        destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destPort), constant.CONST_DEFAULT_DEST_PORT_NUMBER, "Verify Destination Port Number")
        number_test += 1
        
        # verify Destination IP Address from Bus 
        destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destIPAdrress), constant.CONST_DEFAULT_DEST_IP_ADDRESS, "Verify Destination IP Address")
        number_test += 1
                
        # verify PDU ID from Bus 
        pduID = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_ID")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(pduID), constant.CONST_LOCATION_DATA0_PDU_ID, "Verify PDU ID")
        number_test += 1

        # verify PDU Length from Bus 
        pduLen = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_Length")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, pduLen, constant.CONST_LOCATION_DATA0_PDU_LEN, "Verify PDU length")
        number_test += 1
        
        # verify PDU Cycle time on Bus 
        pduCycleTime = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "AvgCycleTime")
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_LOCATION_DATA0_CYCLETIME_MIN, "Verify if cycle time is greater than min cycle time")
        number_test += 1
        
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_LOCATION_DATA0_CYCLETIME_MAX, "Verify if cycle time is lesser than max cycle time")
        
        return CTestCaseResult(number_test, number_failed_tests)
    
    ## @swtest_description The test case checks if communication parameters of SensorFeedback PDU is as per specification
    #  @swtest_step
    #   1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
    #   2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::SensorFeedback(1)
    #   3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
    #   4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
    #   5. Read the below parameters from the system variable swTesting::PDU_NAME and verify the same as per LGP Spec
    #       a. Source and Destination MAC Address
    #       b. Source and Destination Port Number
    #       c. Source and Destination IP Address
    #       d. PDU ID
    #       e. PDU Length
    #       f. PDU Average cycle time(20 cycle taken for averaging)
    #   6. Set value for all signals,EgoData_RelYawRate with 100deg/s,EgoData_VehSpd with 50m/s,EgoData_VehSpdStdDev with 50m/s,EgoData_LogAcc with 10m/s2 .
    #   7. Validate the EgoVehicle Data updated in sensorfeedback PDU.
    #   8. Set another value for all signals,EgoData_RelYawRate with 114deg/s,EgoData_VehSpd with 20m/s,EgoData_VehSpdStdDev with 20m/s,EgoData_LogAcc with 5m/s2 .
    #   9. Validate the EgoVehicle Data updated in sensorfeedback PDU.
    #  @swtest_expResult The Communication Parameters of SensorFeedback PDU must be as per LGP Specifications
    #  @sw_requirement{SDC-R_SW_COMA_1174, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/?urn=urn:rational::1-4147106800294823-O-1174-00159bc3}
    #  @sw_requirement{SDC-R_SW_COMA_1175, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/?urn=urn:rational::1-4147106800294823-O-1175-00159bc3}
    #  @sw_requirement{SDC-R_SW_COMA_1274,https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1274-00159bc3?doors.view=00000004
    def swTest_SensorFeedbackPDU_commParams(self, t32_api):
        number_failed_tests = 0
        number_test = 1
        
        if( not self.isTxPduSentFromRadar(constant.CONST_SENSORFEEDBACK_ENUM,constant.CONST_SENSORFEEDBACK_CYCLETIME_MAX)):
            self.logger.debug("Sensor Feedback PDU not recieved at RBS!! Check Communication manually ")
            number_failed_tests = 1
            return CTestCaseResult(number_test, number_failed_tests)

        # 1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  constant.CONST_CLEAR_ENUM)
        time.sleep(1)
        
        # 2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::SensorFeedback(1)
        self.canoe_api.setSysVarValue_withoutDelay("swTesting", "PDU_NAME",  constant.CONST_SENSORFEEDBACK_ENUM)
        time.sleep(0.5)
        
        # 3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
        while(self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")== constant.CONST_SENSORFEEDBACK_ENUM):
            continue
            
        isReadData = self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")
        
        # 4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, isReadData, constant.CONST_READY_TO_READDATA_ENUM, "Verify if PDU_NAME is ReadyToReadData(-1)")
        number_test += 1
        
        # 5. Read the below parameters from the system variable swTesting::PDU_NAME
        
        # verify Source MAC Address from Bus
        sourceMAC = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourceMac")
        number_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceMAC), constant.CONST_DEFAULT_SOURCE_MAC_ADDRESS, "Verify Source MAC Address"))
        number_test += 1
        
        # verify Source Port Number from Bus
        sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
        number_test += 1
        
        # verify Source IP Address from Bus 
        sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_SOURCE_IP_ADDRESS, "Verify Source IP Address")
        number_test += 1
        
        # verify Destination MAC Address from Bus
        destMACAddress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestMac")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destMACAddress), constant.CONST_DEFAULT_DEST_MAC_ADDRESS, "Verify Destination MAC Address")
        number_test += 1
        
        # verify Destination Port Number from Bus
        destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destPort), constant.CONST_DEFAULT_DEST_PORT_NUMBER, "Verify Destination Port Number")
        number_test += 1
        
        # verify Destination IP Address from Bus 
        destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destIPAdrress), constant.CONST_DEFAULT_DEST_IP_ADDRESS, "Verify Destination IP Address")
        number_test += 1
                
        # verify PDU ID from Bus 
        pduID = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_ID")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(pduID), constant.CONST_SENSORFEEDBACK_PDU_ID, "Verify PDU ID")
        number_test += 1

        # verify PDU Length from Bus 
        pduLen = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_Length")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, pduLen, constant.CONST_SENSORFEEDBACK_PDU_LEN, "Verify PDU length")
        number_test += 1
        
        # verify PDU Cycle time on Bus 
        pduCycleTime = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "AvgCycleTime")
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_SENSORFEEDBACK_CYCLETIME_MIN, "Verify if cycle time is greater than min cycle time")
        number_test += 1
        
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_SENSORFEEDBACK_CYCLETIME_MAX, "Verify if cycle time is lesser than max cycle time")
        
        # 6. Set value for all signals,EgoData_RelYawRate with 100deg/s,EgoData_VehSpd with 50m/s,EgoData_VehSpdStdDev with 50m/s,EgoData_LogAcc with 10m/s2 .

        #send EgoData_RelYawRate with 100deg/s
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", 100.0)
        
        #send EgoData_VehSpd with 50m/s, 
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 50.0)    

        #send EgoData_VehSpdStdDev with 50m/s  
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", 50.0)  

        #EgoData_LogAcc with 10m/s2
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", 10.0)  

        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)

        # 7. Validate the EgoVehicle Data updated in sensorfeedback PDU.

        m_FeedBack_RelYawRate = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_RelYawRate")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_YAW_RATE1,m_FeedBack_RelYawRate,rel_tol=0.005), constant.CONST_FLOATING_POINT_ABS_COMPARE, "FeedBack_RelYawRate value updated in sensorfeedback PDU")
        number_test += 1

        m_FeedBack_VehSpd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_VehSpd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_SPEED1,m_FeedBack_VehSpd), constant.CONST_FLOATING_POINT_ABS_COMPARE, "FeedBack_VehSpd value updated in sensorfeedback PDU")
        number_test += 1

        m_FeedBack_VehSpdStdDev = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_VehSpdStdDev")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_SPEED_DEV1,m_FeedBack_VehSpdStdDev), constant.CONST_FLOATING_POINT_ABS_COMPARE, "FeedBack_VehSpdStdDev value updated in sensorfeedback PDU")
        number_test += 1

        m_FeedBack_LogAcc = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_LogAcc")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_ACCEL1,m_FeedBack_LogAcc), constant.CONST_FLOATING_POINT_ABS_COMPARE, "FeedBack_LogAcc value updated in sensorfeedback PDU")

        # 8  Set another value for all signals,EgoData_RelYawRate with 114deg/s,EgoData_VehSpd with 20m/s,EgoData_VehSpdStdDev with 20m/s,EgoData_LogAcc with 5m/s2 .

        #send EgoData_RelYawRate with 114deg/s
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", 114.0)

        #send EgoData_VehSpd with 20m/s, 
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 20.0)    

        #send EgoData_VehSpdStdDev with 20m/s  
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", 20.0)  

        #EgoData_LogAcc with 5m/s2
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", 5.0)  
        
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)

        # 9. Validate the EgoVehicle Data updated in sensorfeedback PDU.
        m_FeedBack_RelYawRate = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_RelYawRate")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_YAW_RATE2,m_FeedBack_RelYawRate,rel_tol=0.005), constant.CONST_FLOATING_POINT_ABS_COMPARE, "FeedBack_RelYawRate value updated in sensorfeedback PDU")
        number_test += 1

        m_FeedBack_VehSpd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_VehSpd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_SPEED2,m_FeedBack_VehSpd), constant.CONST_FLOATING_POINT_ABS_COMPARE, "FeedBack_VehSpd value updated in sensorfeedback PDU")
        number_test += 1

        m_FeedBack_VehSpdStdDev = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_VehSpdStdDev")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_SPEED_DEV2,m_FeedBack_VehSpdStdDev), constant.CONST_FLOATING_POINT_ABS_COMPARE, "FeedBack_VehSpdStdDev value updated in sensorfeedback PDU")
        number_test += 1

        m_FeedBack_LogAcc = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_LogAcc")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test,math.isclose(constant.CONST_SENSORFEEDBACK_EGOVEH_ACCEL2,m_FeedBack_LogAcc),constant.CONST_FLOATING_POINT_ABS_COMPARE , "FeedBack_LogAcc value updated in sensorfeedback PDU")

        return CTestCaseResult(number_test, number_failed_tests)
    
    ## @swtest_description Test case should check RADAR local time stamp is in sync with global time stamp
    #  @swtest_step
    #   1. Switch ON STBM and check timeBaseStatus = 0x08
    #   2. Switch OFF STBM and check timeBaseStatus = 0x09
    #   3. Switch ON STBM and check for LeaPPast = 0x24
    #   4. Switch ON STBM and check For LeapFuture = 0x18
    #   5. Switch OFF the STBM and check for Reset condition
    #  @swtest_expResult SW variables shall be updated with the valid values received from the communication bus immediately. 
    #  @sw_requirement{SDC-R_SW_SESM_104, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-104-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_108, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-108-00159bc1?doors.view=00000004}
   
    
    def swTest_Time_Syn(self, t32_api):
        number_failed_tests = 0
        number_test = 1
    
        #Step 1:Check STBM switch is ON and check StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus is 0x08
       
        self.canoe_api.setSysVarValue("RBS_Feature", "RBS_Feature_STBM_State", 1)
        time.sleep(1)
        
        #Validate
        StbM_GlobalTime_ON = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
       
     
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTime_ON , constant.CONST_STBM_ON,"SYN with Global Time")
        number_test += 1
        
        #Step 2:Check STBM switch is OFF and check StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus is 0x09
        
        self.canoe_api.setSysVarValue("RBS_Feature", "RBS_Feature_STBM_State", 0)
        time.sleep(1)
         
        
        #validate
        StbM_GlobalTime_OFF = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
        
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTime_OFF , constant.CONST_STBM_OFF,"STBM is OFF")
        number_test += 1
                
        #Step 3 :Leap Future , UNIX time should be more then ECU time
        
        self.canoe_api.setSysVarValue("RBS_Feature","RBS_Feature_STBM_State", 1)
        time.sleep(1)
        
        windowstime = time.time()
        
        self.canoe_api.setSysVarValue("RBS_Feature", "RBS_Feature_STBM_UNIX_time", windowstime*5)
        StbM_GlobalTimebasestatus = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
            
        #Validate
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTimebasestatus, constant.CONST_STBM_LEAPFUTURE, "Verify leap feature bit is set")
        number_test += 1
            
        
        #Step 4 :Leap Past , UNIX time should be less than ECU time
        
        self.canoe_api.setSysVarValue("RBS_Feature","RBS_Feature_STBM_State", 1)
        time.sleep(1)
             
        windowstime = time.time()
        
        self.canoe_api.setSysVarValue("RBS_Feature", "RBS_Feature_STBM_UNIX_time", windowstime-5)
        StbM_GlobalTimebasestatus = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
                      
        #Validate
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTimebasestatus, constant.CONST_STBM_LEAPPAST, "Verify Leap Passed bit is set")
        number_test += 1 
        
        
        #Step 5 :Check Reset when RBS is syn with Global Time
        
        self.canoe_api.setSysVarValue("RBS_Feature","RBS_Feature_STBM_State", 1)
        time.sleep(1)
        
        #Reset
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
       
        #Validate
        
        StbM_GlobalTimebasestatus = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
                
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTimebasestatus, constant.CONST_STBM_ON, "Verify RBS is in SYN with Global Time")
        number_test += 1 
        
        #Step 6 :Check Reset when RBS is not in Syn with Global 
         
        self.canoe_api.setSysVarValue("RBS_Feature","RBS_Feature_STBM_State", 0)
        time.sleep(1)
        
        #Reset
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
                    
        #Validate
        
        StbM_GlobalTimebasestatus = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTimebasestatus, constant.CONST_STBM_GLOBAL_TIME_ZERO, "Verify timebasestatus is zero")
         
        
        return CTestCaseResult(number_test, number_failed_tests)
    
    
    
    ## @swtest_description The test case verifies the static data in E2E header transmitted on the bus for each TX message. 
    #  @swtest_step
    #   1. Validate E2E length and E2E data ID for location attribute.
    #   2. Validate E2E length and E2E data ID for location data.
    #   3. Validate E2E length and E2E data ID for sensor state.
    #   4. Validate E2E length and E2E data ID for sensor feedback.
    #  @swtest_expResult static data in E2E header is updated and transmitted on the bus as per the Specification. 
    #  @sw_requirement{SDC-R_SW_COMA_1259, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1259-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1260, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1260-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1262, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1262-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1263, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1263-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1261, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1261-00159bc3?doors.view=00000004}
    
    def swTest_LGP_TX_Message_E2E(self, t32_api):
        
        number_failed_tests = 0
        number_test = 1
       
       # Step 1. Validate E2E length and E2E data ID for location attribute PDU.
        e2e_length = self.canoe_api.getSysVar("ROS_LGP_Client", "LocAtr_PDU", "LocAtr_E2E_length")
        e2e_dataID = self.canoe_api.getSysVar("ROS_LGP_Client", "LocAtr_PDU", "LocAtr_E2E_DataId")
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_length, constant.CONST_LOC_ATTR_E2E_LENGTH, "Verify E2E length")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_dataID, constant.CONST_LOC_ATTR_E2E_DATAID, "Verify E2E data ID")
        number_test += 1        
               
       # Step 2: Validate E2E length and E2E data ID for location data PDU.
        e2e_length = self.canoe_api.getSysVar("ROS_LGP_Client", "LocData_PDU_1", "LocData_E2E_length")
        e2e_dataID = self.canoe_api.getSysVar("ROS_LGP_Client", "LocData_PDU_1", "LocData_E2E_DataId")

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_length, constant.CONST_LOC_DATA_E2E_LENGTH, "Verify E2E length")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_dataID, constant.CONST_LOC_DATA_E2E_DATAID, "Verify E2E data ID")
        number_test += 1
        
       # Step 3: Validate E2E length and E2E data ID for sensor state PDU.
        e2e_length = self.canoe_api.getSysVar("ROS_LGP_Client", "SensorStateInfo_Output", "SenStInfo_E2E_length")
        e2e_dataID = self.canoe_api.getSysVar("ROS_LGP_Client", "SensorStateInfo_Output", "SenStInfo_E2E_DataId")

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_length, constant.CONST_SENSOR_STATE_E2E_LENGTH, "Verify E2E length")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_dataID, constant.CONST_SENSOR_STATE_E2E_DATAID, "Verify E2E data ID")
        number_test += 1

       # Step 4: Validate E2E length and E2E data ID for sensor feedback PDU.
        e2e_length = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "E2E_length")
        e2e_dataID = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "E2E_DataId")

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_length, constant.CONST_SENSOR_FEEDBACK_E2E_LENGTH, "Verify E2E length")
        number_test += 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, e2e_dataID, constant.CONST_SENSOR_FEEDBACK_E2E_DATAID, "Verify E2E data ID")
        
        return CTestCaseResult(number_test, number_failed_tests)
        

    ## @swtest_description The test case checks if communication parameters of Sensorstinfo PDU is as per specification
    #  @swtest_step
    #   1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
    #   2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Sensorstinfo(1)
    #   3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
    #   4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
    #   5. Read the below parameters from the system variable swTesting::PDU_NAME and verify the same as per LGP Spec
    #       <br>a. Source and Destination MAC Address
    #       <br>b. Source and Destination Port Number
    #       <br>c. Source and Destination IP Address
    #       <br>d. PDU ID
    #       <br>e. PDU Length
    #       <br>f. PDU Average cycle time(10 cycle taken for averaging)
    #   6. Verify LGP version
    #   7. Verify the sensorstate signal in PDU
    #   8. Verify the Unassigned bytes(all zero) and unassigned1 bytes(all 0xff)
    #  @swtest_expResult The Communication Parameters of SensorState PDU must be as per LGP Specifications
    #  @sw_requirement{SDC-R_SW_COMA_1156, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1156-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1151, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1151-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1221, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1221-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1154, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1154-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1182, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1182-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1179, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1179-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1269, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1269-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1276, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1276-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_12, 93https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1293-00159bc3?doors.view=00000004}
    def swTest_Sensorstinfo_commParams(self, t32_api):
        number_failed_tests = 0
        number_test = 1
        
        if( not self.isTxPduSentFromRadar(constant.CONST_SENSORSTATE_ENUM,constant.CONST_SENSORSTATE_CYCLETIME_MAX )):
            self.logger.debug("Sensor state information PDU not recieved at RBS!! Check Communication manually ")
            number_failed_tests = 1
            return CTestCaseResult(number_test, number_failed_tests)

        # 1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  constant.CONST_CLEAR_ENUM)
        time.sleep(1)
        
        # 2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::SensorFeedback(1)
        self.canoe_api.setSysVarValue_withoutDelay("swTesting", "PDU_NAME",  constant.CONST_SENSORSTATE_ENUM)
        time.sleep(0.5)
        
        # 3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
        while(self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")== constant.CONST_SENSORSTATE_ENUM):
            continue
            
        isReadData = self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")
        
        # 4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, isReadData, constant.CONST_READY_TO_READDATA_ENUM, "Verify if PDU_NAME is ReadyToReadData(-1)")
        number_test += 1
        
        # 5. Read the below parameters from the system variable swTesting::PDU_NAME
        
        # verify Source MAC Address from Bus
        sourceMAC = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourceMac")
        number_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceMAC), constant.CONST_DEFAULT_SOURCE_MAC_ADDRESS, "Verify Source MAC Address"))
        number_test += 1
        
        # verify Source Port Number from Bus
        sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
        number_test += 1
        
        # verify Source IP Address from Bus 
        sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_SOURCE_IP_ADDRESS, "Verify Source IP Address")
        number_test += 1
        
        # verify Destination MAC Address from Bus
        destMACAddress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestMac")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destMACAddress), constant.CONST_DEFAULT_DEST_MAC_ADDRESS, "Verify Destination MAC Address")
        number_test += 1
        
        # verify Destination Port Number from Bus
        destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destPort), constant.CONST_DEFAULT_DEST_PORT_NUMBER, "Verify Destination Port Number")
        number_test += 1
        
        # verify Destination IP Address from Bus 
        destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destIPAdrress), constant.CONST_DEFAULT_DEST_IP_ADDRESS, "Verify Destination IP Address")
        number_test += 1
                
        # verify PDU ID from Bus 
        pduID = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_ID")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(pduID), constant.CONST_SENSORSTATE_PDU_ID, "Verify PDU ID")
        number_test += 1

        # verify PDU Length from Bus 
        pduLen = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_Length")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, pduLen, constant.CONST_SENSORSTATE_PDU_LEN, "Verify PDU length")
        number_test += 1
        
        # verify PDU Cycle time on Bus 
        pduCycleTime = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "AvgCycleTime")
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_SENSORSTATE_CYCLETIME_MIN, "Verify if cycle time is greater than min cycle time")
        number_test += 1

        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_SENSORSTATE_CYCLETIME_MAX , "Verify if cycle time is lesser than max cycle time")

        # 6. Verify LGP version  
        lgpver = format(self.canoe_api.getSysVar("ROS_LGP_Client", "SensorStateInfo_Output", "SenStInfo_LgpVer"),'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, lgpver, k_lgpVersion, "Verify LGP version")
        number_test += 1

        # 7. Verify the sensorstate signal in PDU

        SenState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")

        m_sensorState = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable_m_sensorState_out_local.m_arrayPool[0].elem.m_sensorState")

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, SenState,m_sensorState['vvalue'].value, "Verify PDU Signal SenStInfo_SenSt")
        number_test += 1

        # 8. Verify the Unassigned bits
        
        Unassigned = self.canoe_api.getSysVar("ROS_LGP_Client", "SensorStateInfo_Output","SenStInfo_Unassigned")
        Unassigned1 = self.canoe_api.getSysVar("ROS_LGP_Client", "SensorStateInfo_Output","SenStInfo_Unassigned1")
        
        #convert the negative numbers read from canoe to hex values
        Unassigned1_converted = tuple([self.tohex(v,8) for v in Unassigned1])

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Unassigned, constant.CONST_SENSORSTATE_UNASSIGNED, "verify PDU signal SenStInfo_Unassigned")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Unassigned1_converted, constant.CONST_SENSORSTATE_UNASSIGNED1, "verify PDU signal SenStInfo_Unassigned1")  
        
        
        return CTestCaseResult(number_test, number_failed_tests)
       
    ## @swtest_description The test case checks if communication parameters of SensorBroadcast PDU is as per specification
    #  @swtest_step
    #   1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
    #   2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::SensorBroadcast(1)
    #   3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
    #   4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
    #   5. Read the below parameters from the system variable swTesting::PDU_NAME and verify the same as per LGP Spec
    #       <br>a. Source MAC Address  
    #       <br>b. Destination MAC Address 
    #       <br>c. Source Port Number  
    #       <br>d. Destination Port Number
    #       <br>e. Source IP Address
    #       <br>f. Destination IP Address
    #       <br>g. PDU ID from Bus
    #       <br>h. PDU Length from Bus
    #       <br>i. PDU Cycle time on Bus  
    #   6. Verify the signal data transmitted over sensor broadcast PDU.
    #       <br>a. Software & LGP Version Information 
    #       <br>b. Sensor IP address
    #       <br>c. Destination IP
    #       <br>d. VLAN
    #       <br>e. Netmask
    #       <br>f. Source Port
    #       <br>g. Destination Port 
    #       <br>h. Diagnostic Source IP
    #       <br>i. Diagnostic Netmask
    #       <br>j. Diagnostic VLAN
    #       <br>k. Diagnostic Port
    #       <br>l. Sensor MAC address
    #       <br>m. Doip Physical address
    #       <br>n. Doip Functional address
    #       <br>o. Doip Target address
    #       <br>p. Unused bytes
    #    7. Set Radar MAC address to 0x8834fe851125 and verify the response
    #    8. Set Radar IP address to 10.0.0.1,remote IP to 10.255.255.254 and verify the response
    #    9. Set remote port to 0x8756 and verify the response
    #    10. Set Radar Diag source IP address to 169.254.0.1 and verify the response
    #    11. Set Radar DOIP address to 0x0001 and verify the response
    #    12. Set Radar MAC address to 0x8834fe456398  and verify the response
    #    13. Set Radar IP address to 172.16.0.1,remote IP to 172.31.255.254 and verify the response 
    #    14. Set remote port to 0x9645 and verify the response
    #    15. Set Radar Diag source IP address to 169.254.255.254 and verify the response
    #    16. Set Radar DOIP address to 0xFFFF and verify the response
    #  @swtest_expResult The Communication Parameters of SensorBroadcast PDU must be as per LGP Specifications
    #  @sw_requirement{SDC-R_SW_COMA_1223, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1223-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1224, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1224-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1225, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1225-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1226, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1226-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1272, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1272-00159bc3?doors.view=00000004}

    def swTest_SensorBroadcastPDU_commParams_sigValidation(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # 1. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::Clear(-2) to clear any previous data
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  constant.CONST_CLEAR_ENUM)
        time.sleep(1)
        
        # 2. Set the system variable-> swTesting::PDU_NAME to sysvar::swTesting::PDU_NAME::SensorBroadcast(1)
        self.canoe_api.setSysVarValue_withoutDelay("swTesting", "PDU_NAME",  constant.CONST_SENSORBROADCAST_ENUM)
        time.sleep(0.5)
        
        # 3. Wait till PDU_NAME changes from 0 to any other value (Invalid or ReadyToReadData)
        while(self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")== constant.CONST_SENSORBROADCAST_ENUM):
            continue
            
        isReadData = self.canoe_api.getSysVarValue("swTesting", "PDU_NAME")
        
        # 4. Verify if swTesting::PDU_NAME is sysvar::swTesting::PDU_NAME::ReadyToReadData (-1)
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, isReadData, constant.CONST_READY_TO_READDATA_ENUM, "Verify if PDU_NAME is ReadyToReadData(-1)")
        number_test += 1
        
        
        # 5. Read the below parameters from the system variable swTesting::PDU_NAME
        
        # a. verify Source MAC Address from Bus
        sourceMAC = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourceMac")
        number_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceMAC), constant.CONST_DEFAULT_SOURCE_MAC_ADDRESS, "Verify Source MAC Address"))
        number_test += 1
        
        # b. verify Source Port Number from Bus
        sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourcePort), constant.CONST_BROADCAST_SOURCE_PORT_NUMBER, "Verify Source Port Number")
        number_test += 1
        
        # c. verify Source IP Address from Bus 
        sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_SOURCE_IP_ADDRESS, "Verify Source IP Address")
        number_test += 1
        
        # d. verify Destination MAC Address from Bus
        destMACAddress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestMac")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destMACAddress), constant.CONST_BROADCAST_DEST_MAC_ADDRESS, "Verify Destination MAC Address")
        number_test += 1
        
        # e. verify Destination Port Number from Bus
        destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destPort), constant.CONST_DEFAULT_DEST_PORT_NUMBER, "Verify Destination Port Number")
        number_test += 1
        
        # f. verify Destination IP Address from Bus

        destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destIPAdrress), constant.CONST_BROADCAST_DEST_IP_ADDRESS, "Verify Destination IP Address")
        number_test += 1
                
        # g. verify PDU ID from Bus 
        pduID = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_ID")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(pduID), constant.CONST_SENSORBORADCAST_PDU_ID, "Verify PDU ID")
        number_test += 1

        # h. verify PDU Length from Bus 
        pduLen = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "PDU_Length")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, pduLen, constant.CONST_SENSORBORADCAST_PDU_LEN, "Verify PDU length")
        number_test += 1
        
        # i. verify PDU Cycle time on Bus 
        pduCycleTime = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "AvgCycleTime")
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_SENSORBORADCAST_CYCLETIME_MIN, "Verify if cycle time is greater than min cycle time")
        number_test += 1
        
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, pduCycleTime, constant.CONST_SENSORBORADCAST_CYCLETIME_MAX, "Verify if cycle time is lesser than max cycle time")

    
        # 6. Verify the signal data transmitted over sensor broadcast PDU.

        # a. Software & LGP Version Information.
        
        LGU_BroadCast_LgpVer = format(self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_LgpVer"),'08x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_BroadCast_LgpVer, k_lgpVersion, "verify lgp version")
        number_test += 1
        
      
        self.m_parsedCustomerVersionMajorNumber = None
        self.m_parsedCustomerVersionMinorNumber = None
        self.m_parsedCustomerVersionPatchNumber = None
        self.logger.debug("SetUp test case: Extracting information from rbBuild_Version_Cfg.h")
        
        with open('./../../../generatedFiles/rbBuild_Version_Cfg.h', 'r') as reader:
            # Read and print the entire file line by line
            for line in reader:
                if re.search(k_customerVersionMajorNumberRegex, line):
                    customerVersionMajorNumber = re.search(k_customerVersionMajorNumberRegex, line).group(1)                    
                    # convert the string to an integer. 
                    self.m_parsedCustomerVersionMajorNumber = ctypes.c_uint8(int(customerVersionMajorNumber))
                    self.logger.debug(f"customerVersion - MajorNumber of rbBuild_Version_Cfg.h: {self.m_parsedCustomerVersionMajorNumber.value}")
                if re.search(k_customerVersionMinorNumberRegex, line):
                    customerVersionMinorNumber = re.search(k_customerVersionMinorNumberRegex, line).group(1)
                    # convert the string to an integer. 
                    self.m_parsedCustomerVersionMinorNumber = ctypes.c_uint8(int(customerVersionMinorNumber))
                    self.logger.debug(f"customerVersion - MinorNumber of rbBuild_Version_Cfg.h: {self.m_parsedCustomerVersionMinorNumber.value}")
                if re.search(k_customerVersionPatchNumberRegex, line):
                    customerVersionPatchNumber = re.search(k_customerVersionPatchNumberRegex, line).group(1)                    
                    # convert the string to an integer. 
                    self.m_parsedCustomerVersionPatchNumber = ctypes.c_uint8(int(customerVersionPatchNumber))
                    self.logger.debug(f"customerVersion - PatchNumber of rbBuild_Version_Cfg.h: {self.m_parsedCustomerVersionPatchNumber.value}")
        
        # (i). retrieve customer version from the bus
        customerVersionBus = self.canoe_api.getSysVar("ROS_LGP_Client","Sensorbroadcast_Output", "BroadCast_SwCust")        
        self.logger.debug(f"Customer version on bus: {hex(customerVersionBus)}")

        # (ii). check bus value boundaries -> min and max
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, customerVersionBus, 0, "Check customer version boundary")
        number_test += 1        
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, customerVersionBus, k_maxThreeByte, "Check customer version boundary")
        number_test += 1
        
        # (iii). check 4 byte for major version, minor version and patch level 
        customerVersionBusCType = ctypes.c_uint32(customerVersionBus)                                        
        
        unusedByteBus = self.getUnusedByteCustVersion(customerVersionBusCType)
        majorByteBus = self.getMajorByteCustVersion(customerVersionBusCType)
        minorByteBus = self.getMinorByteCustVersion(customerVersionBusCType)
        patchByteBus = self.getPatchLevelByteCustVersion(customerVersionBusCType)
        majorByteParsed = ctypes.c_uint8(k_maxOneByte)
        minorByteParsed = ctypes.c_uint8(k_maxOneByte)
        patchByteParsed = ctypes.c_uint8(k_maxOneByte)

        
      
        if ((self.m_parsedCustomerVersionMajorNumber) and (self.m_parsedCustomerVersionMinorNumber) and(self.m_parsedCustomerVersionPatchNumber)) != None:
            majorByteParsed = self.m_parsedCustomerVersionMajorNumber
            minorByteParsed = self.m_parsedCustomerVersionMinorNumber
            patchByteParsed = self.m_parsedCustomerVersionPatchNumber
                      
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, unusedByteBus.value, 0, "Check unused byte")
        number_test += 1
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, majorByteBus.value, majorByteParsed.value, "Check major version")
        number_test += 1
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, minorByteBus.value, minorByteParsed.value, "Check minor version")
        number_test += 1

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, patchByteBus.value, patchByteParsed.value, "Check patch level")
        number_test += 1
        
        # b. verify Sensor IP Address of signal 
        sensorIPAdrress = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_SenIpAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, sensorIPAdrress, constant.CONST_BROADCAST_SenIpAdd, "verify PDU signal BroadCast_SenIpAdd")
        number_test += 1

        # c. verify Destination IP Address of signal  
        destIPAdrress = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DestIpAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, destIPAdrress, constant.CONST_BROADCAST_DestIpAdd,  "verify PDU signal BroadCast_DestIpAdd")
        number_test += 1

        # d. verify Sensor VLAN of signal  
        senVlan = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_SenVlan")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, senVlan, constant.CONST_BROADCAST_SenVlan, "verify PDU signal BroadCast_SenVlan")
        number_test += 1

        # e. verify Sensor Netmask of signal  
        SenNetmask = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_SenNetmask")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, SenNetmask, constant.CONST_BROADCAST_SenNetmask, "verify PDU signal BroadCast_SenVlan")
        number_test += 1

        # f. verify Source Port Number of signal
        sourcePort = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_SouPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(sourcePort), constant.CONST_BROADCAST_SouPort, "verify PDU signal BroadCast_SouPort")
        number_test += 1

        # g. verify Destination Port Number of signal
        destPort = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DestPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destPort), constant.CONST_BROADCAST_DestPort, "verify PDU signal BroadCast_DestPort")
        number_test += 1
    
        # h. verify Diagnostic Source IP Address of signal  
        diagSouIpAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DiagSouIpAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, diagSouIpAdd, constant.CONST_BROADCAST_DiagSouIpAdd, "verify PDU signal BroadCast_DiagSouIpAdd")
        number_test += 1

        # i. verify Diagnostic Netmask of signal 
        diagNetmask = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DiagNetmask")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, diagNetmask, constant.CONST_BROADCAST_DiagNetmask, "verify PDU signal BroadCast_DiagNetmask")
        number_test += 1

        # j. verify Diagnostic VLAN of signal  
        diagVlan = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_DiagVlan")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, diagVlan, constant.CONST_BROADCAST_DiagVlan, "verify PDU signal BroadCast_DiagVlan")
        number_test += 1

        # k.  verify Diagnostic Port of signal  
        diagPort = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_DiagPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, diagPort, constant.CONST_BROADCAST_DiagPort, "verify PDU signal BroadCast_DiagPort")
        number_test += 1
    
        # l. verify Sensor Mac address of signal  
        senMacAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_SenMacAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, senMacAdd, constant.CONST_BROADCAST_SenMacAdd, "verify PDU signal BroadCast_SenMacAdd")
        number_test += 1

        # m.  verify DOIP Physical address of signal  
        senDoIPPhyAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_SenDoIPPhyAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, senDoIPPhyAdd,constant.CONST_BROADCAST_SenDoIPPhyAdd, "verify PDU signal BroadCast_SenDoIPPhyAdd")
        number_test += 1
        
        # n.  verify DOIP Functional address of signal  
        senDoIPFuncAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_SenDoIPFuncAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, senDoIPFuncAdd,constant.CONST_BROADCAST_SenDoIPFuncAdd, "verify PDU signal BroadCast_SenDoIPFuncAdd")
        number_test += 1

        # o.  verify DOIP Target address of signal  
        senDoIPTarAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_DoIPTarAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(senDoIPTarAdd), constant.CONST_BROADCAST_DoIPTarAdd, "verify PDU signal BroadCast_DoIPTarAdd")
        number_test += 1
        
        # p.  verify DestPortUnassigned of signal  
        DestPortUnassigned = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_DestPortUnassigned")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, DestPortUnassigned, constant.CONST_BROADCAST_DestPortUnassigned, "verify PDU signal BroadCast_DestPortUnassigned")
        number_test += 1
          
        Unassigned = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_Unassigned")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Unassigned, constant.CONST_BROADCAST_Unassigned, "verify PDU signal BroadCast_Unassigned")  
        number_test += 1
        
        SouPortUnassigned = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_SouPortUnassigned")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, SouPortUnassigned, constant.CONST_BROADCAST_SouPortUnassigned, "verify PDU signal BroadCast_SouPortUnassigned")


        # Step 7:Set Radar MAC address to 0x8834fe851125 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, vamaConstant.CONST_WRITE_REQ_USERDEFINED_RADAR_MAC_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, DID_response, vamaConstant.CONST_DID_WRITE_RESP_MAC_ADDRESS, 
                                                   f"RADAR MAC {vamaConstant.CONST_USERDEFINED_MAC_SET1} - DID Data written to NVM")    
        number_test += 1

   
        # i. verify Sensor Mac address of signal  
        senMacAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_SenMacAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, senMacAdd, constant.CONST_USERDEFINED_MAC_SET1, "verify PDU signal BroadCast_SenMacAdd")
        number_test += 1
        

        # Step 8:Set Radar IP address to 10.0.0.1,remote IP to 10.255.255.254 and verify the response
       
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, vamaConstant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, DID_response, vamaConstant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Local IP and Remote IP {vamaConstant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_1} - DID Data written to NVM")    
        number_test += 1

        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "10.0.0.1")                       
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "10.255.255.254")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)        
        time.sleep(0.5)
        
       # i. verify Sensor IP Address 
        sensorIPAdrress = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_SenIpAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, sensorIPAdrress, constant.CONST_USERDEFINED_RADAR_IP_RANGE_1, "verify PDU signal BroadCast_SenIpAdd")
        number_test += 1

        # ii. verify Destination IP Address 
        destIPAdrress = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DestIpAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, destIPAdrress, constant.CONST_USERDEFINED_REMOTE_IP_RANGE_1,  "verify PDU signal BroadCast_DestIpAdd")
        number_test += 1

        # iii. verify Sensor Netmask 
        SenNetmask = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_SenNetmask")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, SenNetmask, constant.CONST_BROADCAST_SENSOR_NETMASK_SET1, "verify PDU signal BroadCast_SenVlan")
        number_test += 1
                
        # Step9:Set remote port to 0x8756 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, vamaConstant.CONST_WRITE_REQ_USERDEFINED_REMOTE_PORT_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, DID_response, vamaConstant.CONST_DID_WRITE_RESP_REMOTE_PORT, 
                                                   f"RADAR Remote Port {vamaConstant.CONST_USER_DEFINED_REMOTE_PORT_SET1} - DID Data written to NVM")    
        number_test += 1 

        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)
        self.canoe_api.setSysVarValue("swTesting", "Remote_Port",  0x8756)                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5)
        
        # i. verify Destination Port Number 
        destPort = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DestPort")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, hex(destPort), constant.CONST_USER_DEFINED_REMOTE_PORT_SET1, "verify PDU signal BroadCast_DestPort")
        number_test += 1
                       

       # Step 10:Set Radar Diag source IP address to 169.254.0.1 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, vamaConstant.CONST_WRITE_REQ_USERDEFINED_RADAR_DIAG_SOURCE_IP_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3) 
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, DID_response, vamaConstant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Diag Source IP {vamaConstant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET1} - DID Data written to NVM")    
        number_test += 1

        # i. verify Diagnostic Source IP Address   
        diagSouIpAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DiagSouIpAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, diagSouIpAdd, constant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET1, "verify PDU signal BroadCast_DiagSouIpAdd")
        number_test += 1

        # ii. verify Diagnostic Netmask of signal 
        diagNetmask = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output", "BroadCast_DiagNetmask")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, diagNetmask, constant.CONST_BROADCAST_DiagNetmask, "verify PDU signal BroadCast_DiagNetmask")
        number_test += 1


       # Step 11:Set Radar DOIP address to 0x0001 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, vamaConstant.CONST_WRITE_REQ_USERDEFINED_RADAR_DOIP_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, DID_response, vamaConstant.CONST_DID_WRITE_RESP_DOIP_ADDRESS, 
                                                   f"RADAR DOIP {vamaConstant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET1} - DID Data written to NVM")    
        number_test += 1

        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(3) 
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0x0001, '04d'))


        # i.  verify DOIP Physical address of signal  
        senDoIPPhyAdd = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorbroadcast_Output","BroadCast_SenDoIPPhyAdd")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, senDoIPPhyAdd,constant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET1, "verify PDU signal BroadCast_SenDoIPPhyAdd")
  
        return CTestCaseResult(number_test, number_failed_tests)
      
    def getUnusedByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_fourthByteMask.value) >> 24)

    def getMajorByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_thirdByteMask.value) >> 16)
        
    def getMinorByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_secondByteMask.value) >> 8)
        
    def getPatchLevelByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_firstByteMask.value))    
        
         
        
