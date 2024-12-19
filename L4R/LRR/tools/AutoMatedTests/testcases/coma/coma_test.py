# -*- coding: utf-8 -*-

import sys
import time
import os
import math

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
import coma_constants as constant
from testbase import CTestCaseResult

# constants used in test cases for verification


class CTestSuiteComa(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteComa"), canoe_api, t32_api, relay_api, hw,
                         globalTestcaseFilter)

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
        "swTest_sensorFeedbackPDU_commParams;swTest_locationAttributePDU_commParams;swTest_locationData0PDU_commParams;")
        
        numberFailedTests = self.executeFilteredFunctionUser(t32_api, localFilterList)
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)

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
    #  @swtest_expResult SW variables shall be updated with the valid values received from the communication bus immediately. 
    #  @sw_requirement{SDC-R_SW_COMA_1137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1137-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1140, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1140-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1264, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1264-00159bc3?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_COMA_1138, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1138-00159bc3?doors.view=00000004}
    
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
    #  @swtest_expResult The Communication Parameters of SensorFeedback PDU must be as per LGP Specifications
    #  @sw_requirement{SDC-R_SW_COMA_1174, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/?urn=urn:rational::1-4147106800294823-O-1174-00159bc3}
    #  @sw_requirement{SDC-R_SW_COMA_1175, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/?urn=urn:rational::1-4147106800294823-O-1175-00159bc3}
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
        
        return CTestCaseResult(number_test, number_failed_tests)