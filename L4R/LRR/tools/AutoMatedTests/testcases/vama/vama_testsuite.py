# -*- coding: utf-8 -*-

import sys
import time
import os

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
import lodm_constants as lodmConstant
import coma_constants as comaConstant
import vama_constants as constant
from testbase import CTestCaseResult


number_vama_failed_tests = 0
number_vama_test = 1

# constants used in test cases for verification


class CTestSuiteVama(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteVama"), canoe_api, t32_api, relay_api, hw,
                         globalTestcaseFilter, self.getComponentName())

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no vama test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllVamaTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "vama"

    def runAllVamaTests(self, t32_api):
        #numberFailedTests = self.executeFilteredFunction(t32_api)   

        # We need the filter function by user, because some function are commented.
        #Once no function is commented the 'executeFilteredFunction' function may be used instead. 
        localFilterList = ("swTest_LGP_Local_IP_Variant_Handling;swTest_LGP_Remote_IP_Variant_Handling;swTest_LGP_Remote_Port_Variant_Handling;swTest_LGP_Variant_Handling_MulticastTX;swTest_LGP_MAC_Variant_Handling;swTest_LGP_Variant_Handling_SourceDiagIP;swTest_LGP_Variant_Handling_DOIP;swTest_Variant_handling_IP_range_1;swTest_Variant_handling_IP_range_2;swTest_Variant_handling_IP_range_3;swTest_LGP_Variant_handling_MulticastRX")
        
        numberFailedTests = self.executeFilteredFunctionUser(t32_api, localFilterList)
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)

    def ValidateTXEthFrame(self,pdu_name,class_IPaddress,modified_value):  
        number_TX_failed_tests = 0
        global number_vama_test
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  comaConstant.CONST_CLEAR_ENUM)
        time.sleep(0.05)
        self.canoe_api.setSysVarValue("swTesting", "PDU_NAME",  pdu_name)
        if modified_value == constant.CONST_LOCAL_IP:
            destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
            number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destPort), constant.CONST_DEFAULT_REMOTE_PORT_NUMBER_HEX, "Verify Destination Port Number")
            number_vama_test += 1
            sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
            destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
            if pdu_name == constant.CONST_SENSOR_BROADCAST_TX:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER_BROADCAST, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_BROADCAST_HEX, "Verify Destination IP Address")
                number_vama_test += 1
            else:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_HEX, "Verify Destination IP Address")
                number_vama_test += 1
            if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:       
                sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_RADAR_IP_ADDRESS_HEX, "Verify Source IP Address")
                number_vama_test += 1
            elif class_IPaddress == constant.CONST_USERDEFINED_SET1:    
                sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_USERDEFINED_RADAR_IP_CLASS_C_SET1_HEX, "Verify Source IP Address")
                number_vama_test += 1
            elif class_IPaddress == constant.CONST_USERDEFINED_SET2:        
                sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_USERDEFINED_RADAR_IP_CLASS_C_SET2_HEX, "Verify Source IP Address")
                number_vama_test += 1
        if modified_value == constant.CONST_REMOTE_IP:
       	    destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
            number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destPort), constant.CONST_DEFAULT_REMOTE_PORT_NUMBER_HEX, "Verify Destination Port Number")
            number_vama_test += 1
            sourceIPAdrress  = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
            number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_RADAR_IP_ADDRESS_HEX, "Verify Source IP Address")
            number_vama_test += 1
       	    sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
            destIPAdrress  = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
            if pdu_name == constant.CONST_SENSOR_BROADCAST_TX:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER_BROADCAST, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_BROADCAST_HEX, "Verify Destination IP Address")
                number_vama_test += 1
            else:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")                    
                number_vama_test += 1
                if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:      
                    destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
                    number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_HEX, "Verify Destination IP Address")
                    number_vama_test += 1
                elif class_IPaddress == constant.CONST_USERDEFINED_SET1:    
                    destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
                    number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_USERDEFINED_REMOTE_IP_CLASS_C_SET1_HEX, "Verify Destination IP Address")
                    number_vama_test += 1
                elif class_IPaddress == constant.CONST_USERDEFINED_SET2:        
                    destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
                    number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_USERDEFINED_REMOTE_IP_CLASS_C_SET2_HEX, "Verify Destination IP Address")
                    number_vama_test += 1
        if modified_value == constant.CONST_REMOTE_PORT:
            sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
            number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_RADAR_IP_ADDRESS_HEX, "Verify Source IP Address")
            number_vama_test += 1
       	    sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
            destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
            if pdu_name == constant.CONST_SENSOR_BROADCAST_TX:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER_BROADCAST, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_BROADCAST_HEX, "Verify Destination IP Address")
                number_vama_test += 1
       	    else:	
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_HEX, "Verify Destination IP Address")
                number_vama_test += 1
            if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:       
                destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destPort), constant.CONST_DEFAULT_REMOTE_PORT_NUMBER_HEX, "Verify Destination Port Number")
                number_vama_test += 1
            elif class_IPaddress == constant.CONST_USERDEFINED_SET1:    
                destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destPort), constant.CONST_USER_DEFINED_REMOTE_PORT_SET1_HEX, "Verify Destination Port Number")
                number_vama_test += 1
            elif class_IPaddress == constant.CONST_USERDEFINED_SET2:        
                destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destPort), constant.CONST_USER_DEFINED_REMOTE_PORT_SET2_HEX, "Verify Destination Port Number")
                number_vama_test += 1
        if modified_value == constant.CONST_REMOTE_IP_MULTICAST:
       	    destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
            number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destPort), constant.CONST_DEFAULT_REMOTE_PORT_NUMBER_HEX, "Verify Destination Port Number")
            number_vama_test += 1
            sourceIPAdrress  = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
            number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_RADAR_IP_ADDRESS_HEX, "Verify Source IP Address")
            number_vama_test += 1
       	    sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
            destIPAdrress  = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
            if pdu_name == constant.CONST_SENSOR_BROADCAST_TX:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER_BROADCAST, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_BROADCAST_HEX, "Verify Destination IP Address")
                number_vama_test += 1
            else:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_USERDEFINED_REMOTE_MULTICAST_IP_HEX, "Verify Destination IP Address")
                number_vama_test += 1
        if modified_value == constant.CONST_RADAR_MAC:
            destMACAddress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestMac")
            if pdu_name == constant.CONST_SENSOR_BROADCAST_TX:
                number_TX_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destMACAddress), constant.CONST_DEFAULT_DEST_MAC_BROADCAST_ADDRESS, "Verify Destination MAC Address"))
            else:    
                number_TX_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destMACAddress), comaConstant.CONST_DEFAULT_DEST_MAC_ADDRESS, "Verify Destination MAC Address"))
            number_vama_test += 1
            sourceMAC = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourceMac")
            if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:
                number_TX_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceMAC), comaConstant.CONST_DEFAULT_SOURCE_MAC_ADDRESS, "Verify Source MAC Address"))
            elif class_IPaddress == constant.CONST_USERDEFINED_SET1:
                number_TX_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceMAC), constant.CONST_USERDEFINED_MAC_SET1_HEX, "Verify Source MAC Address"))
            elif class_IPaddress == constant.CONST_USERDEFINED_SET2:
                number_TX_failed_tests += (testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceMAC), constant.CONST_USERDEFINED_MAC_SET2_HEX, "Verify Source MAC Address"))            
            number_vama_test += 1
        if modified_value == constant.CONST_USER_IP:
            destPort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "DestPort")
            number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destPort), constant.CONST_DEFAULT_REMOTE_PORT_NUMBER_HEX, "Verify Destination Port Number")
            number_vama_test += 1
            sourcePort = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "SourcePort")
            destIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Dest_IP_Address")
            sourceIPAdrress = self.canoe_api.getSysVar("swTesting", "TransmitPDU", "Source_IP_Address")
            if pdu_name == constant.CONST_SENSOR_BROADCAST_TX:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER_BROADCAST, "Verify Source Port Number")
                number_vama_test += 1
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_BROADCAST_HEX, "Verify Destination IP Address")
                number_vama_test += 1
            else:
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourcePort), constant.CONST_DEFAULT_SOURCE_PORT_NUMBER, "Verify Source Port Number")
                number_vama_test += 1
            if class_IPaddress == constant.CONST_USERDEFINED_SET1:       
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_RADAR_IP_ADDRESS_SET1_HEX, "Verify Source IP Address")
                number_vama_test += 1
                if pdu_name != constant.CONST_SENSOR_BROADCAST_TX:
                    number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_REMOTE_IP_ADDRESS_SET1_HEX, "Verify Destination IP Address")
                    number_vama_test += 1                
            elif class_IPaddress == constant.CONST_USERDEFINED_SET2:    
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_RADAR_IP_ADDRESS_SET2_HEX, "Verify Source IP Address")
                number_vama_test += 1
                if pdu_name != constant.CONST_SENSOR_BROADCAST_TX:                
                    number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_REMOTE_IP_ADDRESS_SET2_HEX, "Verify Destination IP Address")
                    number_vama_test += 1  
            elif class_IPaddress == constant.CONST_USERDEFINED_SET3:        
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_RADAR_IP_ADDRESS_SET3_HEX, "Verify Source IP Address")
                number_vama_test += 1
                if pdu_name != constant.CONST_SENSOR_BROADCAST_TX:                               
                    number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_REMOTE_IP_ADDRESS_SET3_HEX, "Verify Destination IP Address")
                    number_vama_test += 1  
            elif class_IPaddress == constant.CONST_USERDEFINED_SET4:        
                number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(sourceIPAdrress), constant.CONST_DEFAULT_RADAR_IP_ADDRESS_HEX, "Verify Source IP Address")
                number_vama_test += 1
                if pdu_name != constant.CONST_SENSOR_BROADCAST_TX:                
                    number_TX_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, hex(destIPAdrress), constant.CONST_DEFAULT_REMOTE_IP_ADDRESS_HEX, "Verify Destination IP Address")
                    number_vama_test += 1  
        return number_TX_failed_tests
    
    
         
                    
    def setMPMessageCanoeApi(self,class_IPaddress):  
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", constant.CONST_MEAS_PGM_DMP01)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", constant.CONST_MEAS_PGM_DMP02)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", constant.CONST_MEAS_PGM_DMP04)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
            time.sleep(0.5)
                     
    def setSensorModeRequestMessageCanoeApi(self,class_IPaddress):         
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", constant.CONST_SENSOR_MODE_START_MODULTATION)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", constant.CONST_SENSOR_MODE_STOP_MODULTATION)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", constant.CONST_SENSOR_MODE_SUSPEND_MODULTATION)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", 1)
            time.sleep(0.5)
        
    def setMCSMessageCanoeApi(self,class_IPaddress):
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", constant.CONST_SENSORTIME_SLOT_SYNCHTYPE)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff", constant.CONST_SENSORTIME_22_MILLI_SECONDS_PDU)    
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", constant.CONST_SENSORTIME_SLOT_SYNCHTYPE)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff",constant.CONST_SENSORTIME_33_MILLI_SECONDS_PDU)    
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", constant.CONST_SENSORTIME_SLOT_SYNCHTYPE)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff",constant.CONST_SENSORTIME_44_MILLI_SECONDS_PDU)    
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)

    def setEgoVehicleDataMessageCanoeApi(self,class_IPaddress):
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", constant.CONST_EGO_VEHICLE_SPEED_MIN)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", constant.CONST_EGO_VEHICLE_YAWRATE_MIN)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", constant.CONST_EGO_VEHICLE_SPEED_STDDEV_MIN)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", constant.CONST_EGO_VEHICLE_ACCEL_MIN)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)  
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", constant.CONST_EGO_VEHICLE_SPEED_MAX)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", constant.CONST_EGO_VEHICLE_YAWRATE_MAX)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", constant.CONST_EGO_VEHICLE_SPEED_STDDEV_MAX)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", constant.CONST_EGO_VEHICLE_ACCEL_MAX)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)               
            time.sleep(0.5)
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:       
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd",constant.CONST_EGO_VEHICLE_SPEED_MID)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_RelYawRate", constant.CONST_EGO_VEHICLE_YAWRATE_MID)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev",constant.CONST_EGO_VEHICLE_SPEED_STDDEV_MID)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_LogAcc", constant.CONST_EGO_VEHICLE_ACCEL_MID)
            self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)       
            time.sleep(0.5)
                    
        
    def ValidateSensorModeRequestMessageCOMbuffer(self,class_IPaddress):
        number_sensormode_failed_tests = 0
        global number_vama_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_sensorMode_request = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_SensorModeRequest_InputByte[0]")['vvalue'].value,'02x')
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:
            number_sensormode_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_sensorMode_request, constant.CONST_COM_SENSOR_MODE_REQUEST_START_MODULATION , "start modulation")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:
            number_sensormode_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_sensorMode_request, constant.CONST_COM_SENSOR_MODE_REQUEST_STOP_MODULATION , "stop modulation")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:
            number_sensormode_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_sensorMode_request, constant.CONST_COM_SENSOR_MODE_REQUEST_SUSPEND_MODULATION , "suspend modulation")
        number_vama_test +=1 
        return number_sensormode_failed_tests
         
    def ValidateMPMessageCOMbuffer(self,class_IPaddress):
        number_dmp_failed_tests = 0
        global number_vama_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_measPgm_LSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[1]")['vvalue'].value,'02x')
        m_measPgm_MSB = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_MeasurementProgramByte[0]")['vvalue'].value,'02x')
        m_measPgm_byte = str(m_measPgm_MSB) + str(m_measPgm_LSB)
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:
            number_dmp_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_measPgm_byte, lodmConstant.CONST_MEAS_PGM_ID1 , "DMP01")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:
            number_dmp_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_measPgm_byte, lodmConstant.CONST_MEAS_PGM_ID2 , "DMP02")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:
            number_dmp_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_measPgm_byte, lodmConstant.CONST_MEAS_PGM_ID4 , "DMP04")
        number_vama_test +=1 
        return number_dmp_failed_tests


    def ValidateMCSMessageCOMbuffer(self,class_IPaddress):
        number_mcs_failed_tests = 0
        global number_vama_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_sensorTimeOffset_first_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[1]")['vvalue'].value,'02x')
        m_sensorTimeOffset_second_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[2]")['vvalue'].value,'02x')
        m_sensorTimeOffset_third_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[3]")['vvalue'].value,'02x')
        m_sensorTimeOffset_fourth_byte = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[4]")['vvalue'].value,'02x')
        m_synctype_received  =  format(t32_api.get_variable_value("Com_dComIPdu_UDP_Rx_LGP_MCS_InputByte[0]")['vvalue'].value,'02x')  
        m_sensorTimeOffset_received = str(m_sensorTimeOffset_first_byte) + str(m_sensorTimeOffset_second_byte)+ str(m_sensorTimeOffset_third_byte)+ str(m_sensorTimeOffset_fourth_byte)
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:
            number_mcs_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_sensorTimeOffset_received ,comaConstant.CONST_SENSORTIME_22_MILLI_SECONDS_PDU,  "Sensor Time Offset 22ms")
            number_mcs_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_synctype_received ,comaConstant.CONST_TIME_SLOT_SYNCHTYPE,  "Time slot Synchronization")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:
            number_mcs_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_sensorTimeOffset_received ,comaConstant.CONST_SENSORTIME_33_MILLI_SECONDS_PDU, "Sensor Time Offset 33ms")
            number_mcs_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_synctype_received ,comaConstant.CONST_TIME_SLOT_SYNCHTYPE,  "Time slot Synchronization")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:
            number_mcs_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_sensorTimeOffset_received ,comaConstant.CONST_SENSORTIME_44_MILLI_SECONDS_PDU,  "Sensor Time Offset 44ms")
            number_mcs_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_synctype_received ,comaConstant.CONST_TIME_SLOT_SYNCHTYPE,  "Time slot Synchronization")
        number_vama_test += 2
        return number_mcs_failed_tests


    def ValidateEgoVehicleDataMessageCOMbuffer(self,class_IPaddress):
        number_ego_veh_failed_tests = 0;
        global number_vama_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
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
        if class_IPaddress == constant.CONST_DEFAULT_ADDRESS:
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_VehSpd_com, comaConstant.CONST_EGO_VEHICLE_SPEED_MINVALUE , "EgoData_VehSpd")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_RelYawRate_com, comaConstant.CONST_EGO_VEHICLE_YAW_RATE_MINVALUE, "EgoData_RelYawRate")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_VehSpdStdDev_com, comaConstant.CONST_EGO_VEHICLE_SPEED_DEV_MINVALUE , "EgoData_VehSpdStdDev")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_LogAcc_com, comaConstant.CONST_EGO_VEHICLE_ACCEL_MINVALUE , "EgoData_LogAcc")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET1:
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_VehSpd_com, comaConstant.CONST_EGO_VEHICLE_SPEED_MAXVALUE , "EgoData_VehSpd")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_RelYawRate_com, comaConstant.CONST_EGO_VEHICLE_YAW_RATE_MAXVALUE , "EgoData_RelYawRate")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_VehSpdStdDev_com, comaConstant.CONST_EGO_VEHICLE_SPEED_DEV_MAXVALUE , "EgoData_VehSpdStdDev")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_LogAcc_com, comaConstant.CONST_EGO_VEHICLE_ACCEL_MAXVALUE , "EgoData_LogAcc")
        elif class_IPaddress == constant.CONST_USERDEFINED_SET2:
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_VehSpd_com, comaConstant.CONST_EGO_VEHICLE_SPEED_MIDVALUE , "EgoData_VehSpd")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_RelYawRate_com, comaConstant.CONST_EGO_VEHICLE_YAW_RATE_MIDVALUE , "EgoData_RelYawRate")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_VehSpdStdDev_com, comaConstant.CONST_EGO_VEHICLE_SPEED_DEV_MIDVALUE , "EgoData_VehSpdStdDev")
            number_ego_veh_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, m_EgoData_LogAcc_com, comaConstant.CONST_EGO_VEHICLE_ACCEL_MIDVALUE , "EgoData_LogAcc")
        number_vama_test += 4
        return number_ego_veh_failed_tests

        
    ## @swtest_description The test case checks if RADAR MAC address can be changed based on the valid user configured DID data,normal communication can be established based on the changed MAC address.
    #  @swtest_step
    #   1. Validate the RADAR default MAC address using 0x22 RDBI service.
    #   2. Validate RX communication with default MAC address.
    #   3. Validate TX communication with default MAC address.
    #   4. Set Radar MAC address to 0x8834fe851125 and verify the response
    #   5. Validate Read DID response using 0x22 RDBI service.
    #   6. Validate RX communication with new MAC address.
    #   7. Validate TX communication with new MAC address.
    #   8. Set Radar MAC address to 0x8834fe456398 and verify the response
    #   9. Validate Read DID response using 0x22 RDBI service.
    #   10. Validate RX communication with new MAC address.
    #   11. Validate TX communication with new MAC address.
    #   12. Set Radar MAC address to 0x8834fe000001 and verify the response
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_117, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-117-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_118, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-118-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_119, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-119-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_120, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-120-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_121, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-121-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_125, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-125-00159bc9?doors.view=00000004}

    def swTest_LGP_MAC_Variant_Handling(self, t32_api):
               
       # Step 1:Validate the RADAR default MAC address using 0x22 RDBI service
        global number_vama_failed_tests       
        global number_vama_test  
        number_vama_failed_tests = 0
        number_vama_test = 1 
        
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_MAC_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)             
        ExpectedData = constant.CONST_READ_RESP_DEFAULT_MAC_ADDRESS

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR Default MAC address {constant.CONST_DEFAULT_RADAR_MAC_ADDRESS}")
        number_vama_test += 1

       # Step 2:Validate RX communication with default MAC address
        self.setMPMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setMCSMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        time.sleep(2)             
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)

       # Step 3:Validate TX communication with default MAC address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_RADAR_MAC)

       # Step 4:Set Radar MAC address to 0x8834fe851125 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_MAC_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_MAC_ADDRESS, 
                                                   f"RADAR MAC {constant.CONST_USERDEFINED_MAC_SET1} - DID Data written to NVM")    
        number_vama_test += 1
                                                       
       # Step 5:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_MAC_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_MAC_SET1

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR MAC address {constant.CONST_USERDEFINED_MAC_SET1}")
        number_vama_test += 1

       # Step 6:Validate RX communication with new MAC address
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        
       # Step 7:Validate TX communication with new MAC address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_RADAR_MAC)

        
       # Step 8:Set Radar MAC address to 0x8834fe456398  and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_MAC_SET2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_MAC_ADDRESS, 
                                                   f"RADAR MAC {constant.CONST_USERDEFINED_MAC_SET2} - DID Data written to NVM")    
        number_vama_test += 1
         
       # Step 9:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_MAC_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_MAC_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR IP address {constant.CONST_USERDEFINED_MAC_SET2}")
        number_vama_test += 1

       # Step 10:Validate RX communication with new MAC address
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
                       
       # Step 11:Validate TX communication with new MAC address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_RADAR_MAC)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_RADAR_MAC)

       # Step 12:Set Radar MAC address to 0x8834fe000001 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_MAC_ADDRESS, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_MAC_ADDRESS, 
                                                   f"RADAR MAC {constant.CONST_DEFAULT_RADAR_MAC_ADDRESS} - DID Data written to NVM")    
                       
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)


        
    ## @swtest_description The test case checks if RADAR Diagnostic SourceIP address can be changed based on the valid user configured DID data,diagnostic communication can be established based on the changed diag IP address.
    #  @swtest_step
    #   1. Validate the RADAR default Diag source IP address using 0x22 RDBI service
    #   2. Set Radar Diag source IP address to 169.254.0.1 and verify the response
    #   3. Validate the RADAR Diag source IP address using 0x22 RDBI service
    #   4. Set Radar Diag source IP address to 169.254.255.254 and verify the response
    #   5. Validate the RADAR Diag source IP address using 0x22 RDBI service
    #   6. Set Radar Diag source IP address to 169.254.255.255 and verify the response
    #   7. Validate the RADAR Diag source IP address using 0x22 RDBI service
    #   8. Set default Radar Diag source IP address to 169.254.18.149 and verify the response
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_153, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-153-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_154, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-154-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_155, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-155-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_151, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-151-00159bc9?doors.view=00000004}

    def swTest_LGP_Variant_Handling_SourceDiagIP(self, t32_api):
               
       # Step 1:Validate the RADAR default Diag source IP address using 0x22 RDBI service
        global number_vama_failed_tests       
        global number_vama_test    
        number_vama_failed_tests = 0
        number_vama_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
         
        ExpectedData = constant.CONST_READ_RESP_DEFAULT_DIAG_SOURCE_IP_ADDRESS

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR Diag source IP address {constant.CONST_DEFAULT_DIAG_SOURCE_IP_ADDRESS}")
        number_vama_test += 1
 
       # Step 2:Set Radar Diag source IP address to 169.254.0.1 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_DIAG_SOURCE_IP_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Diag Source IP {constant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET1} - DID Data written to NVM")    
        number_vama_test += 1

       # Step 3:Validate the RADAR Diag source IP address using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_DIAG_SOURCE_IP_SET1

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR Diag source IP address {constant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET1}")
        number_vama_test += 1
        
       # Step 4:Set Radar Diag source IP address to 169.254.255.254 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_DIAG_SOURCE_IP_SET2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Diag Source IP {constant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET2} - DID Data written to NVM")    
        number_vama_test += 1

       # Step 5:Validate the RADAR Diag source IP address using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_DIAG_SOURCE_IP_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR Diag source IP address {constant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET2}")
        number_vama_test += 1

       # Step 6:Set Radar Diag source IP address to 169.254.255.255 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_DIAG_SOURCE_IP_SET3, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   f"RADAR Diag Source IP {constant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET3} - DID Data is not written to NVM")    
        number_vama_test += 1

       # Step 7:Validate the RADAR Diag source IP address using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_DIAG_SOURCE_IP_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR Diag source IP address {constant.CONST_USER_DEFINED_DIAG_SOURCE_IP_ADDRESS_SET3}")
        number_vama_test += 1
       
       # Step 8:Set default Radar Diag source IP address to 169.254.18.149 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_RADAR_DIAG_SOURCE_IP, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Diag Source IP {constant.CONST_DEFAULT_DIAG_SOURCE_IP_ADDRESS} - DID Data written to NVM")    
        
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)
                
    ## @swtest_description The test case checks if RADAR IP address can be changed based on the valid user configured DID data,normal communication can be established based on the changed local IP address.
    #  @swtest_step
    #   1. Validate the RADAR default IP address using 0x22 RDBI service.
    #   2. Validate RX communication with default IP address.    
    #   3. Validate TX communication with default IP address.
    #   4. Set Radar IP address to 192.168.0.1 and verify the response
    #   5. Validate Read DID response using 0x22 RDBI service.
    #   6. Validate RX communication with new IP address.    
    #   7. Validate TX communication with new IP address.
    #   8. Set Radar IP address to 192.168.255.254  and verify the response
    #   9. Validate Read DID response using 0x22 RDBI service.
    #   10. Validate RX communication with new IP address.    
    #   11. Validate TX communication with new IP address.
    #   12. Set Radar IP address to an invalid value from class C 192.168.255.255 and verify the response
    #   13. Validate Read DID response using 0x22 RDBI service.
    #   14. Validate RX communication with previous valid IP address.    
    #   15. Validate TX communication with previous valid IP address.
    #   16. Write RADAR default IP address 192.168.40.51.
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_129, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-129-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_185, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-185-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_94, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-94-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_182, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-182-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_98, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-98-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_96, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-96-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-137-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_168, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-168-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_124, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-124-00159bc9?doors.view=00000004}

    def swTest_LGP_Local_IP_Variant_Handling(self, t32_api):
               
       # Step 1:Validate the RADAR default IP address using 0x22 RDBI service
        global number_vama_failed_tests       
        global number_vama_test    
        number_vama_failed_tests = 0
        number_vama_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_DEFAULT_IP_ADDRESS

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR Default IP address {constant.CONST_DEFAULT_RADAR_IP_ADDRESS}")
        number_vama_test += 1

       # Step 2:Validate RX communication with default IP address
        self.setMPMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setMCSMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        
       # Step 3:Validate TX communication with default IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_LOCAL_IP)

       # Step 4:Set Radar IP address to 192.168.0.1 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_IP_CLASS_C_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Local IP {constant.CONST_USERDEFINED_RADAR_IP_CLASS_C_SET1} - DID Data written to NVM")    
        number_vama_test += 1
                                                       
       # Step 5:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_IP_CLASS_C_SET1

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR IP address {constant.CONST_USERDEFINED_RADAR_IP_CLASS_C_SET1}")
        number_vama_test += 1

       # Step 6:Validate RX communication with new IP address
        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "192.168.0.1")                
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)
        time.sleep(0.5)        
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        
       # Step 7:Validate TX communication with new IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_LOCAL_IP)

        
       # Step 8:Set Radar IP address to 192.168.255.254  and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_IP_CLASS_C_SET2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Local IP {constant.CONST_USERDEFINED_RADAR_IP_CLASS_C_SET2} - DID Data written to NVM")    
        number_vama_test += 1.
         
       # Step 9:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_IP_CLASS_C_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR IP address {constant.CONST_USERDEFINED_RADAR_IP_CLASS_C_SET2}")
        number_vama_test += 1 

       # Step 10:Validate RX communication with new IP address
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 0)       
        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "192.168.255.254")                
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)
        time.sleep(0.5)           
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
                       
       # Step 11:Validate TX communication with new IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)

        
       # Step 12:Set Radar IP address to an invalid value from class C 192.168.255.255 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_INVALID_RADAR_IP_CLASS_C, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Invalid RADAR IP - DID response NRC")    
        number_vama_test += 1
           
       # Step 13:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_IP_CLASS_C_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR IP address {constant.CONST_USERDEFINED_RADAR_IP_CLASS_C_SET2}")
        number_vama_test += 1 

       # Step 14:Validate RX communication with previous valid IP address
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
     
       # Step 15:Validate TX communication with previous valid IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_LOCAL_IP)
        
       # Step 16:Write RADAR default IP address 192.168.40.51
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_RADAR_IP_ADDRESS, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 0)        
        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "192.168.40.51")                
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)
        time.sleep(0.5)   
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response,constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR IP {constant.CONST_DEFAULT_RADAR_IP_ADDRESS} - DID Data written to NVM")    
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)
 
    ## @swtest_description The test case checks if remote IP address can be changed based on the valid user configured DID data,normal communication can be established based on the changed remote IP address.
    #  @swtest_step
    #   1. Validate the default remote IP address using 0x22 RDBI service.
    #   2. Validate RX communication with default remote IP address.    
    #   3. Validate TX communication with default remote IP address.
    #   4. Set remote IP address to 192.168.0.5 and verify the response
    #   5. Validate Read DID response using 0x22 RDBI service.
    #   6. Validate RX communication with new remote IP address.    
    #   7. Validate TX communication with new remote IP address.    
    #   8. Set remote IP address to 192.168.255.252  and verify the response
    #   9. Validate Read DID response using 0x22 RDBI service.
    #   10. Validate RX communication with new remote IP address.    
    #   11. Validate TX communication with new remote IP address.    
    #   12. Set remote IP address to an invalid value from class C 192.168.255.255 and verify the response
    #   13. Validate Read DID response using 0x22 RDBI service.
    #   14. Validate RX communication with previous valid remote IP address.    
    #   15. Validate TX communication with previous valid remote IP address.    
    #   16. Write RADAR default remote IP address 192.168.40.2
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_129, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-129-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_94, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-94-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_182, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-182-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_98, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-98-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_96, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-96-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-137-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_168, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-168-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_124, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-124-00159bc9?doors.view=00000004}
    def swTest_LGP_Remote_IP_Variant_Handling(self, t32_api):
               
       # Step 1:Validate the default remote IP address using 0x22 RDBI service
        global number_vama_failed_tests       
        global number_vama_test    
        number_vama_failed_tests = 0
        number_vama_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_DEFAULT_REMOTE_IP_ADDRESS

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read remote Default IP address {constant.CONST_DEFAULT_REMOTE_IP_ADDRESS}")
        number_vama_test += 1

       # Step 2:Validate RX communication with default remote IP address
        self.setMPMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setMCSMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)


       # Step 3:Validate TX communication with default remote IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_IP)
        
       # Step 4:Set remote IP address to 192.168.0.5 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_REMOTE_IP_CLASS_C_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"Remote Local IP {constant.CONST_USERDEFINED_REMOTE_IP_CLASS_C_SET1} - DID Data written to NVM")    
        number_vama_test += 1  
        
       # Step 5:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_REMOTE_IP_CLASS_C_SET1

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR IP address {constant.CONST_USERDEFINED_REMOTE_IP_CLASS_C_SET1}")
        number_vama_test += 1

       # Step 6:Validate RX communication with new remote IP address
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "192.168.0.5")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5)    
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)

       # Step 7:Validate TX communication with new remote IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP)
                                     
       # Step 8:Set remote IP address to 192.168.255.252 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_REMOTE_IP_CLASS_C_SET2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"Remote Local IP {constant.CONST_USERDEFINED_REMOTE_IP_CLASS_C_SET2} - DID Data written to NVM")    
        number_vama_test += 1 
              
       # Step 9:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_REMOTE_IP_CLASS_C_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR remote IP address {constant.CONST_USERDEFINED_REMOTE_IP_CLASS_C_SET2}")
        number_vama_test += 1 

       # Step 10:Validate RX communication with new remote IP address
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)        
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "192.168.255.252")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5) 
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)


       # Step 11:Validate TX communication with new remote IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
                             
       # Step 12:Set remote IP address to an invalid value from class C 192.168.255.255 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_INVALID_REMOTE_IP_CLASS_C, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response,diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   "Invalid Remote IP - DID response NRC")    
        number_vama_test += 1 
              
       # Step 13:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_REMOTE_IP_CLASS_C_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR remote IP address {constant.CONST_USERDEFINED_REMOTE_IP_CLASS_C_SET2}")
        number_vama_test += 1 

       # Step 14:Validate RX communication with previous remote IP address
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)

       # Step 15:Validate TX communication with previous remote IP address
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_IP)
                               
       # Step 16:Write back RADAR default remote IP address 192.168.40.2
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_REMOTE_IP_ADDRESS, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)        
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "192.168.40.2")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5) 
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response,constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Remote IP {constant.CONST_DEFAULT_REMOTE_IP_ADDRESS} - DID Data written to NVM")    
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)

    ## @swtest_description The test case checks if remote port can be changed based on the valid user configured DID data,normal communication can be established based on the changed remote port.
    #  @swtest_step
    #   1. Validate the default remote port using 0x22 RDBI service.
    #   2. Validate RX communication with default remote port.        
    #   3. Validate TX communication with default remote port.
    #   4. Set remote port to 0x8756 and verify the response
    #   5. Validate Read DID response using 0x22 RDBI service.
    #   6. Validate RX communication with new remote port.    
    #   7. Validate TX communication with new remote port.
    #   8. Set remote port to 0x9645 and verify the response
    #   9. Validate Read DID response using 0x22 RDBI service.
    #   10. Validate RX communication with new remote port.    
    #   11. Validate TX communication with new remote port.
    #   12. Set remote port to an invalid value 0xDFFF and verify the response
    #   13. Validate Read DID response using 0x22 RDBI service.
    #   14. Validate RX communication with previous valid remote port.        
    #   15. Validate TX communication with previous valid remote port.
    #   16. Write default remote port address 0x76C0
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_161, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-161-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_162, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-162-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_163, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-163-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_164, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-164-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_167, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-167-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_165, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-165-00159bc9?doors.view=00000005}
    
    def swTest_LGP_Remote_Port_Variant_Handling(self, t32_api):
               
       # Step 1:Validate the default remote port using 0x22 RDBI service
        global number_vama_failed_tests       
        global number_vama_test    
        number_vama_failed_tests = 0
        number_vama_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_REMOTE_PORT, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_DID_READ_RESP_DEFAULT_REMOTE_PORT

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read remote port {constant.CONST_DEFAULT_REMOTE_PORT_NUMBER_HEX}")
        number_vama_test += 1

       # Step 2:Validate RX communication with default remote port
        self.setMPMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setMCSMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_DEFAULT_ADDRESS)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_DEFAULT_ADDRESS)
 
       # Step 3:Validate TX communication with default remote port
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_DEFAULT_ADDRESS,constant.CONST_REMOTE_PORT)
        
       # Step 4:Set remote port to 0x8756 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_REMOTE_PORT_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_REMOTE_PORT, 
                                                   f"RADAR Remote Port {constant.CONST_USER_DEFINED_REMOTE_PORT_SET1} - DID Data written to NVM")    
        number_vama_test += 1 
                   
       # Step 5:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_REMOTE_PORT, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_REMOTE_PORT_SET1

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR remote port {constant.CONST_USER_DEFINED_REMOTE_PORT_SET1}")
        number_vama_test += 1

       # Step 6:Validate RX communication with new remote port
        self.canoe_api.setSysVarValue("swTesting", "Remote_Port",  0x8756)                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5)        
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
         
       # Step 7:Validate TX communication with new remote port
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_PORT)
        
       # Step 8:Set remote port to 0x9645 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_REMOTE_PORT_SET2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_REMOTE_PORT, 
                                                   f"RADAR Remote Port {constant.CONST_USER_DEFINED_REMOTE_PORT_SET2} - DID Data written to NVM")    
        number_vama_test += 1 
        
       # Step 9:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_REMOTE_PORT, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_REMOTE_PORT_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR remote port {constant.CONST_USER_DEFINED_REMOTE_PORT_SET2}")
        number_vama_test += 1 
 
       # Step 10:Validate RX communication with new remote port
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)       
        self.canoe_api.setSysVarValue("swTesting", "Remote_Port",  0x9645)                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5) 
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
               
       # Step 11:Validate TX communication with new remote port
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        
       # Step 12:Set remote port to an invalid value 0xDFFF and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_INVALID_REMOTE_PORT, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   "RADAR Remote Port - Invalid")    
        number_vama_test += 1     
        
       # Step 13:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_REMOTE_PORT, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_REMOTE_PORT_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read user defined RADAR remote port {constant.CONST_USER_DEFINED_REMOTE_PORT_SET2}")
        number_vama_test += 1 

       # Step 14:Validate RX communication with new remote port
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
 
       # Step 15:Validate TX communication with previous valid remote port
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_REMOTE_PORT)
        
       # Step 16:Write  default remote port 0x76C0
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_REMOTE_PORT_NUMBER, self.logger)

        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)        
        self.canoe_api.setSysVarValue("swTesting", "Remote_Port",  0x76c0)                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5) 
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_REMOTE_PORT, 
                                                   f"Remote Port {constant.CONST_DEFAULT_REMOTE_PORT_NUMBER_HEX} - DID Data written to NVM")    
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)


 

    ## @swtest_description The test case checks if remote IP can be changed to multicast IP range,normal communication can be established based on the changed IP.
    #  @swtest_step
    #   1. Set remote IP to 224.0.0.1 and verify the response
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate TX communication with multicast remote IP. 
    #   4. Validate RX communication with multicast remote IP.    
    #   5. Write default remote IP. 
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_188, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-188-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_168, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-168-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_124, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-124-00159bc9?doors.view=00000005}
    def swTest_LGP_Variant_Handling_MulticastTX(self, t32_api):
               
       # Step 1:Set remote IP to 224.0.0.1 and verify the response
        global number_vama_failed_tests       
        global number_vama_test    
        number_vama_failed_tests = 0
        number_vama_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MULTICAST_REMOTE_IP, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Remote IP {constant.CONST_MULTICAST_REMOTE_IP} - DID Data written to NVM")    
        number_vama_test += 1
 
       # Step 2:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MULTICAST_REMOTE_IP

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read remote IP {constant.CONST_MULTICAST_REMOTE_IP}")
        number_vama_test += 1

       # Step 3:Validate TX communication with multicast remote IP
        self.canoe_api.setSysVarNested("ROS_LGP_Client", "Multicast",  "IpGroup_R" ,"224.0.0.1")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5) 
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP_MULTICAST)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP_MULTICAST)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP_MULTICAST)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP_MULTICAST)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_REMOTE_IP_MULTICAST)

       # Step 4:Validate RX communication with multicast remote IP
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        
       # Step 5:Write back RADAR default remote IP address 192.168.40.2
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_REMOTE_IP_ADDRESS, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)        
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "192.168.40.2")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(0.5)                
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response,constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Remote IP {constant.CONST_DEFAULT_REMOTE_IP_ADDRESS} - DID Data written to NVM")    
                               
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)      
        
 
    ## @swtest_description The test case checks if RADAR DOIP address can be changed based on the valid user configured DID data,diagnostic communication can be established based on the changed DOIP address.
    #  @swtest_step
    #   1. Validate the RADAR default DOIP address using 0x22 RDBI service
    #   2. Set Radar DOIP address to 0x0001 and verify the response
    #   3. Validate the RADAR Diag source IP address using 0x22 RDBI service
    #   4. Set Radar DOIP address to 0xFFFF and verify the response
    #   5. Validate the RADAR Diag source IP address using 0x22 RDBI service
    #   6. Set Radar DOIP address to 0x1345 and verify the response
    #   7. Validate the RADAR Diag source IP address using 0x22 RDBI service
    #   8. Set default Radar DOIP address to 0x1295 and verify the response
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_190, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-190-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_191, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-191-00159bc9?doors.view=00000004}

    def swTest_LGP_Variant_Handling_DOIP(self, t32_api):
               
       # Step 1:Validate the RADAR default Diag source IP address using 0x22 RDBI service
        global number_vama_failed_tests       
        global number_vama_test    
        number_vama_failed_tests = 0
        number_vama_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_DOIP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
         
        ExpectedData = constant.CONST_READ_RESP_DEFAULT_DOIP_ADDRESS

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR DOIP address {constant.CONST_DEFAULT_RADAR_DOIP_ADDRESS}")
        number_vama_test += 1
 
       # Step 2:Set Radar DOIP address to 0x0001 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_DOIP_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_DOIP_ADDRESS, 
                                                   f"RADAR DOIP {constant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET1} - DID Data written to NVM")    
        number_vama_test += 1

        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0x0001, '04d'))


       # Step 3:Validate the RADAR Diag source IP address using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_DOIP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_DOIP_SET1

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR DOIP address {constant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET1}")
        number_vama_test += 1
        
       # Step 4:Set Radar DOIP address to 0xFFFF and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_DOIP_SET2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_DOIP_ADDRESS, 
                                                   f"RADAR DOIP {constant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET2} - DID Data written to NVM")    
        number_vama_test += 1
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0xffff, '04d'))

       # Step 5:Validate the RADAR Diag source IP address using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_DOIP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_DOIP_SET2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read RADAR DOIP address {constant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET2}")
        number_vama_test += 1

       # Step 6:Set Radar DOIP address to 0x1345 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_RADAR_DOIP_SET3, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_DOIP_ADDRESS, 
                                                   f"Radar DOIP address to {constant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET3} - DID Data is not written to NVM")    
        number_vama_test += 1

        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0x1345, '04d'))

       # Step 7:Validate the RADAR Diag source IP address using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_DOIP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_RADAR_DOIP_SET3

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"Read Radar DOIP address to {constant.CONST_USER_DEFINED_RADAR_DOIP_ADDRESS_SET3}")
        number_vama_test += 1
       
       # Step 8:Set default Radar DOIP address to 0x1295 and verify the response
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_RADAR_DOIP_ADDRESS, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_DOIP_ADDRESS, 
                                                   f"RADAR DOIP {constant.CONST_DEFAULT_RADAR_DOIP_ADDRESS} - DID Data written to NVM")    
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        self.canoe_api.setEnvVar("Env_DoipECUlogaddress_AutoIP", format(0x1295, '04d'))
        
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)
 
 
    ## @swtest_description The test case checks if RADAR IP address,Remote address can be changed with the values from IP range 1,normal communication can be established based on the changed address.
    #  @swtest_step
    #   1. Set Radar IP address to 10.0.0.1,remote IP to 10.255.255.254 and verify the response
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate RX communication with new IP. 
    #   4. Validate TX communication with new IP.         
    #  @sw_requirement{SDC-R_SW_VAMA_186, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-186-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_178, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-178-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_187, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-187-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_184, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-184-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_180, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-180-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_133, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-133-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_134, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-134-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-137-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_168, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-168-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_124, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-124-00159bc9?doors.view=00000004}
    def swTest_Variant_handling_IP_range_1(self, t32_api):
       # Step 1:Set Radar IP address to 10.0.0.1,remote IP to 10.255.255.254 and verify the response
        global number_vama_failed_tests
        global number_vama_test
        number_vama_failed_tests = 0
        number_vama_test = 1        
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Local IP and Remote IP {constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_1} - DID Data written to NVM")    
        number_vama_test += 1
                                                       
       # Step 2:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_1

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"RADAR Local IP and Remote IP {constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_1}")
        number_vama_test += 1

       # Step 3:Validate RX communication with new IP 
        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "10.0.0.1")                       
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "10.255.255.254")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)        
        time.sleep(0.5)
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
 
       # Step 4:Validate TX communication with new IP
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET1,constant.CONST_USER_IP)
                
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)
 
   
                             
    ## @swtest_description The test case checks if RADAR IP address,Remote address can be changed with the values from IP range 2,normal communication can be established based on the changed address.
    #  @swtest_step
    #   1. Set Radar IP address to 172.16.0.1,remote IP to 172.31.255.254 and verify the response
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate RX communication with new IP. 
    #   4. Validate TX communication with new IP.      
    #  @sw_requirement{SDC-R_SW_VAMA_186, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-186-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_178, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-178-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_187, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-187-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_184, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-184-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_180, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-180-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_133, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-133-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_134, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-134-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-137-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_168, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-168-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_124, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-124-00159bc9?doors.view=00000004}
    def swTest_Variant_handling_IP_range_2(self, t32_api):
       # Step 1:Set Radar IP address to 172.16.0.1,remote IP to 172.31.255.254 and verify the response
        global number_vama_failed_tests
        global number_vama_test
        number_vama_failed_tests = 0
        number_vama_test = 1        
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Local IP and Remote IP {constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_2} - DID Data written to NVM")    
        number_vama_test += 1
                                                       
       # Step 2:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_2

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"RADAR Local IP and Remote IP { constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_2}")
        number_vama_test += 1

       # Step 3:Validate RX communication with new IP 
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 0)           
        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "172.16.0.1")                       
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "172.31.255.254")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)        
        time.sleep(0.5)
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
 
       # Step 4:Validate TX communication with new IP
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET2,constant.CONST_USER_IP)

        return CTestCaseResult(number_vama_test, number_vama_failed_tests)
 

    ## @swtest_description The test case checks if RADAR IP address,Remote address can be changed with the values from IP range 3,normal communication can be established based on the changed address.
    #  @swtest_step
    #   1. Set Radar IP address to 192.168.0.1,remote IP to 192.168.255.254 and verify the response
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate RX communication with new IP    
    #   4. Validate TX communication with new IP    
    #   5. Set Radar IP address to 192.168.0.2,remote IP to 192.168.255.0 and verify the response with NVM flag value 2
    #   6. Validate Read DID response using 0x22 RDBI service
    #   7. Validate RX communication with new IP    
    #   8. Validate TX communication with new IP        
    #   9. Set Radar IP address to 192.168.0.2,remote IP to 192.168.255.0 and verify the response with NVM flag value 0
    #   10. Validate Read DID response using 0x22 RDBI service.
    #   11. Validate RX communication with new IP    
    #   12. Validate TX communication with new IP 
    #  @sw_requirement{SDC-R_SW_VAMA_186, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-186-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_178, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-178-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_187, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-187-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_184, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-184-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_180, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-180-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_133, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-133-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_134, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-134-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-137-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_168, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-168-00159bc9?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_VAMA_124, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-124-00159bc9?doors.view=00000004}
    def swTest_Variant_handling_IP_range_3(self, t32_api):
       # Step 1:Set Radar IP address to 192.168.0.1,remote IP to 192.168.255.254 and verify the response
        global number_vama_failed_tests
        global number_vama_test
        number_vama_failed_tests = 0
        number_vama_test = 1        
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_3, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Local IP and Remote IP {constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_3} - DID Data written to NVM")    
        number_vama_test += 1
                                                       
       # Step 2:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_3

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"RADAR Local IP and Remote IP {constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_3}")
        number_vama_test += 1

       # Step 3:Validate RX communication with new IP
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 0)            
        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "192.168.0.1")                       
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "192.168.255.254")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)        
        time.sleep(0.5)
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
 
       # Step 4:Validate TX communication with new IP
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        
       # Step 5:Set Radar IP address to 192.168.0.2,remote IP to 192.168.255.0 and verify the response with NVM flag value 2
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_4, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   f"RADAR Local IP and Remote IP {constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_4} - DID Data written to NVM")    
        number_vama_test += 1
                                                       
       # Step 6:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_3

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"RADAR Local IP and Remote IP {constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_3}")
        number_vama_test += 1

       # Step 7:Validate RX communication with new configuration   
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET2)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET2)
 
       # Step 8:Validate TX communication with new configuration
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET3,constant.CONST_USER_IP)
        
       # Step 9:Set Radar IP address to 192.168.0.2,remote IP to 192.168.255.0 and verify the response with NVM flag value 0
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_5, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, DID_response, constant.CONST_DID_WRITE_RESP_IP_ADDRESS, 
                                                   "RADAR Local IP and Remote IP {constant.CONST_WRITE_REQ_USERDEFINED_IP_RANGE_5}  - DID Data written to NVM")    
        number_vama_test += 1
                                                       
       # Step 10:Validate Read DID response using 0x22 RDBI service
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_DID_READ_REQ_IP_ADDRESS, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_5

        number_vama_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_vama_test, Read_DID, ExpectedData, f"RADAR Local IP and Remote IP {constant.CONST_READ_RESP_USERDEFINED_IP_RANGE_3}")
        number_vama_test += 1


       # Step 11:Validate RX communication with new configuration 
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 0)           
        self.canoe_api.setSysVarValue("ROS_LGP_Server", "ServerIP_1",  "192.168.40.51")                       
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "192.168.40.2")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        self.canoe_api.setSysVarValue("swTesting", "ServerIP_Btn", 1)        
        time.sleep(0.5)
        self.setMPMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setSensorModeRequestMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setMCSMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        
        number_vama_failed_tests += self.ValidateMPMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateSensorModeRequestMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateMCSMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)
 
       # Step 12:Validate TX communication with new configuration
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_ATTRIBUTE_TX,constant.CONST_USERDEFINED_SET4,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_LOCATION_DATA0_TX,constant.CONST_USERDEFINED_SET4,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_STATE_TX,constant.CONST_USERDEFINED_SET4,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_FEEDBACK_TX,constant.CONST_USERDEFINED_SET4,constant.CONST_USER_IP)
        number_vama_failed_tests += self.ValidateTXEthFrame(constant.CONST_SENSOR_BROADCAST_TX,constant.CONST_USERDEFINED_SET4,constant.CONST_USER_IP)

        return CTestCaseResult(number_vama_test, number_vama_failed_tests)
 
 
    ## @swtest_description The test case checks if ego vehicle PDU can be received in multicast mode of addressing.
    #  @swtest_step
    #   1. Send ego vehicle PDU in multicast mode from canoe.
    #   2. Validate the data received in COM buffer
    #   3. Send ego vehicle PDU in unicast mode from canoe
    #  @swtest_expResult SW variables shall be updated with the valid values received from the diagnostic data. 
    #  @sw_requirement{SDC-R_SW_VAMA_181, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-181-00159bc9?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_VAMA_168, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-168-00159bc9?doors.view=00000005}
    def swTest_LGP_Variant_handling_MulticastRX(self, t32_api):
               
       # Step 1:Send ego vehicle PDU in multicast mode from canoe
        global number_vama_failed_tests       
        global number_vama_test 
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "Tx_Type",  1)                
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "ClientIP_1",  "192.168.40.2")                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 1)
        time.sleep(2)       
            
       # Step 2: Validate the data received in COM buffer
        self.setEgoVehicleDataMessageCanoeApi(constant.CONST_USERDEFINED_SET1)
        number_vama_failed_tests += self.ValidateEgoVehicleDataMessageCOMbuffer(constant.CONST_USERDEFINED_SET1)

       # Step 3:Write back unicast mode for Ego vehicle PDU from canoe
        self.canoe_api.setSysVarValue("ROS_LGP_Client", "Tx_Type",  0)                
        self.canoe_api.setSysVarValue("swTesting", "RemoteIP_Btn", 0)        
        time.sleep(1)  
                            
        return CTestCaseResult(number_vama_test, number_vama_failed_tests)      
     