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
import coma_constants as comaConstant
import lodm_constants as constant
from testbase import CTestCaseResult

# constants used in test cases for verification
k_sensorTimeOffsetMin               = 22000000
k_sensorTimeOffsetMid               = 33000000
k_sensorTimeOffsetMax               = 44000000
k_lguLocDataLgpVer                  = 1536
k_lguFeedBackLgpVer                 = 1536
k_lguFeedBackStbmTimeMin            = 0
k_lguFeedbackStbmTimeMax            = 4294967295
k_numOfLocationsMin                 = 0
k_numOfLocationsMax                 = 1024
k_constantOne                       = 1
k_timeslotSyncValue                 = 1
k_constantZero                      = 0
k_blockCounterMin                   = 0
k_blockCounterMax                   = 255
k_maxLocPerPdu                      = 16
k_lgpVersionRegex                   = "LGP_VERSION_INFO\s\{([a-zA-Z0-9\s',]*)"
rbBuildVersionFile = open('./../../../generatedFiles/rbBuild_Version_Cfg.h', 'r') 
k_lgpVersion = rbBuildVersionFile.readlines()[35][27:35]
    
#global variables
mp_number_failed_tests = 0
mp_number_test = 1

class CTestSuiteLodm(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteLodm"), canoe_api, t32_api, relay_api, hw,
                         globalTestcaseFilter, self.getComponentName())

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no lodm test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllLodmTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "lodm"

    def runAllLodmTests(self, t32_api):
        #numberFailedTests = self.executeFilteredFunction(t32_api)   

        # We need the filter function by user, because some function are commented.
        #Once no function is commented the 'executeFilteredFunction' function may be used instead. 
        localFilterList = ("swTest_MeasurementProgramIndex_via_DID;"
            "swTest_MeasurementProgramIndex_via_DIDWrite_Default_Value;"
            "swTest_MeasurementProgramIndex_via_DID_InValidValue;"
            "swTest_MeasurementProgramIndex_via_PDU;"
            "swTest_MeasurementProgramIndex_via_PDU_InvalidValue_afterreset;"
            "swTest_MeasurementProgramIndex_via_PDU_InvalidValue_run;"
            "swTest_MeasurementProgramIndex_via_DID_reset_default_value;"
            "swTest_sensorfeedback_channel_PDU;"
            "swTest_locationDataHeader_signalValidation;"
            "swTest_locationAttribHeader_signalValidation;"
            "swTest_MountingPosition_Data_Default;"
            "swTest_MountingPosition_Range_Check;"
            "swTest_MountingPosition_Data_Min;"
            "swTest_MountingPosition_Data_Max;"
            "swTest_MountingPosition_Data_Mid;"
            "swTest_MountingPosition_reset_default_value")
                      
            
        numberFailedTests = self.executeFilteredFunctionUser(t32_api, localFilterList)
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)

    ## @swtest_description The test case checks if the MCS Data Sync Type and Offset gets updated from Diagnostic manager
    #  @swtest_step
    #    1. Write DID 060B to update the MCS selector type as 0, MCS Sync Type as 0 and MCS Sensor Time Offset as 0.
    #    2. Write DID 060B to update the MCS Sync Type as 1 and MCS Sensor Time Offset as 22 microseconds.
    #    3. Write DID 060B to update the MCS Sync Type as 1 and MCS Sensor Time Offset as 33 microseconds.
    #    4. Write DID 060B to update the MCS Sync Type as 1 and MCS Sensor Time Offset as 44 microseconds.
    #  @swtest_expResult The MCS Data Sync type and offset should get updated in LODM output as per the data written in DID
    #  @sw_requirement{SDC-R_SW_LODM_1721, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1721-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1722, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1722-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1729, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1729-00159bc0?doors.view=00000004}
    def swTest_check_MCSSyncType_and_sensortimeOffset_via_DiagnosticManager(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: Write DID 060B to update the MCS selector type as 0, MCS Sync Type as 0 and MCS Sensor Time Offset as 0.
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeDefaultValue = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeDefaultValue['vvalue'].value, 0,"Check Measurement Program")
        number_test += 1

        MCSOffsetDefaultValue = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetDefaultValue['vvalue'].value, 0, "Check Measurement Program")
        number_test += 1

        # Step 2: Write DID 060B to update the MCS Sync Type as 1 and MCS Sensor Time Offset as 22 microseconds and read it in lauterbach
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_YES + constant.CONST_MCS_SENS_OFFSET_MIN + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue1['vvalue'].value, k_constantOne, "MCS Sync Type value written from DID")
        number_test += 1

        MCSOffsetValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue1['vvalue'].value, k_sensorTimeOffsetMin, "MCS Offset value written from DID")
        number_test += 1

        # Step 3: Write DID 060B to update the MCS Sync Type as 0 and MCS Sensor Time Offset as 33 microseconds and read it in lauterbach
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_MID + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeValue2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue2['vvalue'].value, k_constantZero, "MCS Sync Type value written from DID")
        number_test += 1

        MCSOffsetValue2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue2['vvalue'].value, k_sensorTimeOffsetMid, "MCS Offset value written from DID")
        number_test += 1

        # Step 4: Write DID 060B to update the MCS Sync Type as 1 and MCS Sensor Time Offset as 44 microseconds and read it in lauterbach
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_YES + constant.CONST_MCS_SENS_OFFSET_MAX + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeValue3 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue3['vvalue'].value, k_constantOne, "MCS Sync Type value written from DID")
        number_test += 1

        MCSOffsetValue3 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue3['vvalue'].value, k_sensorTimeOffsetMax, "MCS Offset value written from DID")

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if the MCS Data Sync Type and Offset gets updated from Communication manager
    #  @swtest_step
    #   1. Write DID 060B to make the MCS selector type as 1.
    #   2. Update the MCS Sync Type as 0 and MCS Sensor Time Offset as 0 using PDU.
    #   3. Update the MCS Sync Type as 1 and MCS Sensor Time Offset as 22 microseconds using PDU
    #   4. Update the MCS Sync Type as 1 and MCS Sensor Time Offset as 33 microseconds using PDU
    #   5. Update the MCS Sync Type as 1 and MCS Sensor Time Offset as 44 microseconds using PDU
    #   6. update MCS Sync Type as 0 and MCS Sensor Time Offset as 0 microseconds using PDU
    #  @swtest_expResult The MCS Data Sync type and offset should get updated in LODM output as per the data sent by PDU
    #  @sw_requirement{SDC-R_SW_LODM_1729, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1729-00159bc0?doors.view=00000004}
    def swTest_check_MCSSyncType_and_sensortimeOffset_via_CommunicationManager(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: Write DID 060B to update the MCS Selector type as 1 and read it in lauterbach
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ONE
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        # Step 2: update MCS Sync Type as 0 and MCS Sensor Time Offset as 0 microseconds using PDU and read it in lauterbach
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)

        MCSSyncTypeValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue1['vvalue'].value, k_constantZero, "MCS Sync Type value updated as per PDU")

        MCSOffsetValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test,  MCSOffsetValue1['vvalue'].value, k_constantZero, "MCS Offset value updated as per PDU")
        number_test += 1

        # Step 3: update MCS Sync Type as 1 and MCS Sensor Time Offset as 22 microseconds using PDU and read it in lauterbach
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", k_sensorTimeOffsetMin)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)

        MCSSyncTypeValue2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue2['vvalue'].value, k_constantOne, "MCS Sync Type value updated as per PDU")

        MCSOffsetValue2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue2['vvalue'].value, k_sensorTimeOffsetMin, "MCS Offset value updated as per PDU")
        number_test += 1

        # Step 4: update MCS Sync Type as 1 and MCS Sensor Time Offset as 33 microseconds using PDU and read it in lauterbach
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", k_sensorTimeOffsetMid)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)

        MCSSyncTypeValue3 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue3['vvalue'].value, k_constantOne, "MCS Sync Type value updated as per PDU")

        MCSOffsetValue3 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue3['vvalue'].value, k_sensorTimeOffsetMid, "MCS Offset value updated as per PDU")
        number_test += 1

        # Step 5: update MCS Sync Type as 1 and MCS Sensor Time Offset as 44 microseconds using PDU and read it in lauterbach
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", k_sensorTimeOffsetMax)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)

        MCSSyncTypeValue4 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue4['vvalue'].value, k_constantOne, "MCS Sync Type value updated as per PDU")

        MCSOffsetValue4 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue4['vvalue'].value, k_sensorTimeOffsetMax, "MCS Offset value updated as per PDU")
        number_test += 1

        # Step 6: update MCS Sync Type as 0 and MCS Sensor Time Offset as 0 microseconds using PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(0.5)

        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)


        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case is to validate MCS Sensor Time Offset Data is as per DID and PDU.
    #  @swtest_step
    #   1. Write DID for MCS data with for Min value. Perform ECU reset.
    #   2. Write DID for MCS data with for mid value (0x 01 4F B1 80) . Perform ECU reset.
    #   3. Update MCS Sync Type as 1 and MCS Sensor Time Offset as 33 microseconds using PDU.
    #  @swtest_expResult MCS syncType and sensorTimeOffset shall update as expected.
    #  @sw_requirement{SDC-R_SW_LODM_1710, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1710-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1715, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1715-00159bc0?doors.view=00000004}
    def swTest_MCS_sensortimeOffset_DID_PDU(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: Write DID for MCS data with for Min value. Perform ECU reset.
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_YES + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeDefaultValue = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeDefaultValue['vvalue'].value, k_constantOne, "Check Measurement Program Sync Type")
        number_test += 1
        
        MCSOffsetDefaultValue = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetDefaultValue['vvalue'].value, k_constantZero, "Check Measurement Program sensorTimeOffset")
        number_test += 1
        
        # Step 2: Write DID for MCS data with for mid value (0x 01 4F B1 80) . Perform ECU reset.
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_YES + constant.CONST_MCS_SENS_OFFSET_MIN + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue1['vvalue'].value, k_constantOne, "MCS Sync Type value written from DID")
        number_test += 1
        
        MCSOffsetValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue1['vvalue'].value, k_sensorTimeOffsetMin, "MCS Offset value written from DID")
        number_test += 1

        # Step 3: Update MCS Sync Type as 1 and MCS Sensor Time Offset as 33 microseconds using PDU and read it in lauterbach
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ONE
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", k_sensorTimeOffsetMid)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(5)

        MCSSyncTypeValue3 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue3['vvalue'].value, k_constantOne, "MCS Sync Type value updated as per PDU")
        number_test += 1
        
        MCSOffsetValue3 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue3['vvalue'].value, k_sensorTimeOffsetMid, "MCS Offset value updated as per PDU")

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case is to validate MCS syncType is as per DID and PDU.
    #  @swtest_step
    #   1. From RBS write DID with MCS Selector flag = 0 and MCS Sync type = 0. Perform ECU reset.
    #   2. From RBS write DID with MCS Selector flag = 0 and MCS Sync type = 1. Perform ECU reset.
    #   3. From RBS write DID with MCS Selector flag = 1 and perform SW reset. Send MCS Sync type = 0 through PDU
    #   4. From RBS write DID with MCS Selector flag = 1 and perform SW reset. Send MCS Sync type = 1 through PDU
    #  @swtest_expResult MCS syncType shall update as expected.
    #  @sw_requirement{SDC-R_SW_LODM_1710, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1710-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1712, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1712-00159bc0?doors.view=00000004}
    def swTest_MCS_synctypedata_DID_PDU(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: From RBS write DID with MCS Selector flag = 0 and MCS Sync type = 0. Perform ECU reset.
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeDefaultValue = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeDefaultValue['vvalue'].value, k_constantZero, "Check Measurement Program")
        number_test += 1

        # Step 2: From RBS write DID with MCS Selector flag = 0 and MCS Sync type = 1. Perform ECU reset.
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_YES + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue1['vvalue'].value, k_constantOne, "MCS Sync Type value written from DID")
        number_test += 1

        # Step 3: From RBS write DID with MCS Selector flag = 1 and perform SW reset. Send MCS Sync type = 0 through PDU
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ONE
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        canoeDiagPanel.sendEcuHardReset(self.canoe_api, self.t32_api, self.logger)
        time.sleep(2)

        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", 00000000)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(2)

        MCSSyncTypeValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue1['vvalue'].value, k_constantZero, "MCS Sync Type value as per PDU")
        number_test += 1

        # Step 4: From RBS write DID with MCS Selector flag = 1 and perform SW reset. Send MCS Sync type = 1 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "xRR_LGU_MCS_SenTimeOff", k_sensorTimeOffsetMid)
        time.sleep(0.5)

        MCSSyncTypeValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue1['vvalue'].value, k_constantOne, "MCS Sync Type value written from PDU")

        return CTestCaseResult(number_test, number_failed_tests)



    def Validate_COMBuffer_MountX(self,expected_value):
        number_failed_tests = 0
        global mp_number_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_mountPosX_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[493]")['vvalue'].value,'02x')
        m_mountPosX_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[494]")['vvalue'].value,'02x')
        m_mountPosX_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[495]")['vvalue'].value,'02x')
        m_mountPosX_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[496]")['vvalue'].value,'02x')
        m_mountPosX_ValidValue  = str(m_mountPosX_com_byte0) + str(m_mountPosX_com_byte1) + str(m_mountPosX_com_byte2) + str(m_mountPosX_com_byte3)       
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, m_mountPosX_ValidValue, expected_value , "Mount X  Valid Value as per DID")
        mp_number_test += 1
        return number_failed_tests  

    def Validate_COMBuffer_MountY(self,expected_value):
        number_failed_tests = 0
        global mp_number_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_mountPosY_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[497]")['vvalue'].value,'02x')
        m_mountPosY_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[498]")['vvalue'].value,'02x')
        m_mountPosY_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[499]")['vvalue'].value,'02x')
        m_mountPosY_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[500]")['vvalue'].value,'02x')
        m_mountPosY_ValidValue  = str(m_mountPosY_com_byte0) + str(m_mountPosY_com_byte1) + str(m_mountPosY_com_byte2) + str(m_mountPosY_com_byte3)        
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, m_mountPosY_ValidValue, expected_value,"Mount Y Valid Value as per DID")
        mp_number_test += 1
        return number_failed_tests  
        
    def Validate_COMBuffer_MountZ(self,expected_value):
        number_failed_tests = 0
        global mp_number_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_mountPosZ_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[501]")['vvalue'].value,'02x')
        m_mountPosZ_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[502]")['vvalue'].value,'02x')
        m_mountPosZ_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[503]")['vvalue'].value,'02x')
        m_mountPosZ_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[504]")['vvalue'].value,'02x')
        m_mountPosZ_ValidValue  = str(m_mountPosZ_com_byte0) + str(m_mountPosZ_com_byte1) + str(m_mountPosZ_com_byte2) + str(m_mountPosZ_com_byte3)       
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, m_mountPosZ_ValidValue, expected_value,"Mount Z Valid Value as per DID")
        mp_number_test += 1
        return number_failed_tests 

    def Validate_COMBuffer_Azimuth(self,expected_value):
        number_failed_tests = 0
        global mp_number_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_mountAngleNomAzi_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[505]")['vvalue'].value,'02x')
        m_mountAngleNomAzi_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[506]")['vvalue'].value,'02x')
        m_mountAngleNomAzi_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[507]")['vvalue'].value,'02x')
        m_mountAngleNomAzi_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[508]")['vvalue'].value,'02x')
        m_mountAngleNomAzi_ValidValue  = str(m_mountAngleNomAzi_com_byte0) + str(m_mountAngleNomAzi_com_byte1) + str(m_mountAngleNomAzi_com_byte2) + str(m_mountAngleNomAzi_com_byte3)       
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, m_mountAngleNomAzi_ValidValue, expected_value,"SenPosAzimuth angle Valid Value as per DID")
        mp_number_test += 1
        return number_failed_tests 

    def Validate_COMBuffer_Elevation(self,expected_value):
        number_failed_tests = 0
        global mp_number_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_mountAngleNomEle_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[509]")['vvalue'].value,'02x')
        m_mountAngleNomEle_com_byte1 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[510]")['vvalue'].value,'02x')
        m_mountAngleNomEle_com_byte2 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[511]")['vvalue'].value,'02x')
        m_mountAngleNomEle_com_byte3 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[512]")['vvalue'].value,'02x')
        m_mountAngleNomEle_ValidValue  = str(m_mountAngleNomEle_com_byte0) + str(m_mountAngleNomEle_com_byte1) + str(m_mountAngleNomEle_com_byte2) + str(m_mountAngleNomEle_com_byte3)       
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, m_mountAngleNomEle_ValidValue, expected_value,"SenPosElevation angle Valid Value as per DID")
        mp_number_test += 1
        return number_failed_tests 
        
    def Validate_COMBuffer_Orientation(self,expected_value):
        number_failed_tests = 0
        global mp_number_test
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        m_sensorOrientation_com_byte0 = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_LocAttribByte[513]")['vvalue'].value,'02x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, str(m_sensorOrientation_com_byte0), expected_value,"SenOrientation Valid Value as per DID")
        return number_failed_tests 
                                                                         
    ## @swtest_description The test case validates the default value of 0x500 DID,data sent to the COM buffer 
    #  @swtest_step
    #   1. Validate Read DID response using 0x22 RDBI service.
    #   2. Validate the data sent to the COM buffer.
    #  @swtest_expResult SW variables shall be updated with the valid default values.
    #  @sw_requirement{SDC-R_SW_LODM_1612, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1612-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1617, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1617-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1870, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1870-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1600, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1600-00159bc0?doors.view=00000004}
    def swTest_MountingPosition_Data_Default(self, t32_api):
        # Step 1: Validate Read DID response using 0x22 RDBI service.
        global mp_number_failed_tests 
        global mp_number_test
        mp_number_failed_tests = 0
        mp_number_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)             
        ExpectedData = constant.CONST_READ_RESP_DEFAULT_MOUNTING_POSITION

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read default Mounting position and misalignment data {constant.CONST_READ_RESP_DEFAULT_MOUNTING_POSITION}")
        mp_number_test += 1
        
        # Step 2: Validate the data sent to the COM buffer.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_DEFAULT_PHYSICAL_VALUE_ORIENTATION)
        
        return CTestCaseResult(mp_number_test, mp_number_failed_tests)



    ## @swtest_description The test case is to reset the 0x500 DID to default value.
    #  @swtest_step
    #   1. Write the default Mounting position data to NVM.    
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate the data sent to the COM buffer.
    #  @swtest_expResult SW variables shall be updated with the valid default values.
    #  @sw_requirement{SDC-R_SW_LODM_1612, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1612-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1617, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1617-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1870, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1870-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1600, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1600-00159bc0?doors.view=00000004}
    def swTest_MountingPosition_reset_default_value(self, t32_api):
        # Step 1: Write the default Mounting position data to NVM.
        global mp_number_failed_tests 
        global mp_number_test
        mp_number_failed_tests = 0
        mp_number_test = 1        
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_DEFAULT_MOUNTING_POSITION, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, constant.CONST_WRITE_RESP_MOUNTING_POSITION, 
                                                   f"Write {constant.CONST_WRITE_REQ_DEFAULT_MOUNTING_POSITION} - DID Data written to NVM")    
        mp_number_test += 1
                        
        # Step 2: Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)             
        ExpectedData = constant.CONST_READ_RESP_DEFAULT_MOUNTING_POSITION

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read default Mounting position and misalignment data {constant.CONST_READ_RESP_DEFAULT_MOUNTING_POSITION}")
        mp_number_test += 1
        
        # Step 3: Validate the data sent to the COM buffer.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_DEFAULT_MP_PHYSICAL_VALUE )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_DEFAULT_PHYSICAL_VALUE_ORIENTATION)
        
        return CTestCaseResult(mp_number_test, mp_number_failed_tests)

                                                                         
    ## @swtest_description The test case validates minimum value of Sensor PosX,Sensor PosY, Sensor PosZ, Sensor Azimuth, Sensor Elevation, Sensor Orientation,data sent to the COM buffer  
    #  @swtest_step
    #   1. Set Sensor PosX with 0x0000,Sensor PosY with 0x0000,Sensor PosZ with 0x0000,Sensor Azimuth with 0x0000,Sensor Elevation with 0x0000,Sensor Orientation with 0x00.
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate the data sent to the COM buffer.
    #  @swtest_expResult SW variables shall be updated with the valid min values.
    #  @sw_requirement{SDC-R_SW_LODM_1612, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1612-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1617, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1617-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1870, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1870-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1600, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1600-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1601, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1601-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1602, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1602-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1620, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1620-00159bc0?doors.view=00000004}
    def swTest_MountingPosition_Data_Min(self, t32_api):
        # Step 1: Set Sensor PosX with 0x0000,Sensor PosY with 0x0000,Sensor PosZ with 0x0000,Sensor Azimuth with 0x0000,Sensor Elevation with 0x0000,Sensor Orientation with 0x00.
        global mp_number_failed_tests 
        global mp_number_test 
        mp_number_failed_tests = 0
        mp_number_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_MIN, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, constant.CONST_WRITE_RESP_MOUNTING_POSITION, 
                                                   f"Write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_MIN} - DID Data written to NVM")    
        mp_number_test += 1
        # Step 2: Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)             
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_MIN

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_MIN}")
        mp_number_test += 1
        
        # Step 3: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MIN_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_MIN_SENSOR_POS_Y)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_MIN_SENSOR_POS_Z)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MIN_SENSOR_AZIMUTH )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MIN_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MIN_SENSOR_ORIENTATION)
        
        return CTestCaseResult(mp_number_test, mp_number_failed_tests)
        
    ## @swtest_description The test case validates maximum value of Sensor PosX,Sensor PosY, Sensor PosZ, Sensor Azimuth, Sensor Elevation, Sensor Orientation,data sent to the COM buffer  
    #  @swtest_step
    #   1. Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8cA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate the data sent to the COM buffer.
    #  @swtest_expResult SW variables shall be updated with the valid min values.
    #  @sw_requirement{SDC-R_SW_LODM_1612, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1612-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1617, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1617-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1870, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1870-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1600, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1600-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1601, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1601-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1602, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1602-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1620, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1620-00159bc0?doors.view=00000004}
    def swTest_MountingPosition_Data_Max(self, t32_api):
        # Step 1: Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8cA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
        global mp_number_failed_tests 
        global mp_number_test 
        mp_number_failed_tests = 0
        mp_number_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_MAX, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, constant.CONST_WRITE_RESP_MOUNTING_POSITION, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_MAX} - DID Data written to NVM")    
        mp_number_test += 1
        
        # Step 2: Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)             
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_MAX

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_MAX}")
        mp_number_test += 1
         
        # Step 3: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_MAX_SENSOR_POS_Y)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_MAX_SENSOR_POS_Z)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH)
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION)
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION)
                
        return CTestCaseResult(mp_number_test, mp_number_failed_tests)

    ## @swtest_description The test case verifies a valid value of Sensor PosX,Sensor PosY, Sensor PosZ, Sensor Azimuth, Sensor Elevation, Sensor Orientation,data sent to the COM buffer 
    #  @swtest_step
    #   1. Set Sensor PosX with 0x2000,Sensor PosY with 0x2000,Sensor PosZ with 0x2000,Sensor Azimuth with 0x4650,Sensor Elevation with 0x05DC,Sensor Orientation with 0x00.
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate the data sent to the COM buffer.
    #  @swtest_expResult SW variables shall be updated with the valid min values.
    #  @sw_requirement{SDC-R_SW_LODM_1612, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1612-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1617, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1617-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1870, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1870-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1600, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1600-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1601, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1601-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1602, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1602-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1620, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1620-00159bc0?doors.view=00000004}
    def swTest_MountingPosition_Data_Mid(self, t32_api):
        # Step 1: Set Sensor PosX with 0x2000,Sensor PosY with 0x2000,Sensor PosZ with 0x2000,Sensor Azimuth with 0x4650,Sensor Elevation with 0x05DC,Sensor Orientation with 0x00.
        global mp_number_failed_tests 
        global mp_number_test
        mp_number_failed_tests = 0
        mp_number_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_MID, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, constant.CONST_WRITE_RESP_MOUNTING_POSITION, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_MID} - DID Data written to NVM")    
        mp_number_test += 1
        
        # Step 2: Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)             
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_MID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_MID}")
        mp_number_test += 1
                 
        # Step 3: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MID_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_MID_SENSOR_POS_Y)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_MID_SENSOR_POS_Z)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MID_SENSOR_AZIMUTH )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MID_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MID_SENSOR_ORIENTATION) 
        
        return CTestCaseResult(mp_number_test, mp_number_failed_tests)
                
    ## @swtest_description The test case validates the valid range of data allowed for Sensor PosX,Sensor PosY,Sensor PosZ,Sensor Azimuth,Sensor Elevation,Sensor Orientation,data sent to the COM buffer 
    #  @swtest_step
    #   1. Set Sensor PosX with 0x4000,Sensor PosY with 0x3000,Sensor PosZ with 0x1000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
    #   2. Validate Read DID response using 0x22 RDBI service.
    #   3. Validate the data sent to the COM buffer.
    #   4. Set Sensor PosX with 0x4001,Sensor PosY with 0x3000,Sensor PosZ with 0x1000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
    #   5. Validate Read DID response using 0x22 RDBI service.
    #   6. Validate the data sent to the COM buffer.
    #   7. Set Sensor PosX with 0x4000,Sensor PosY with 0x4001,Sensor PosZ with 0x1000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
    #   8. Validate Read DID response using 0x22 RDBI service.
    #   9. Validate the data sent to the COM buffer.
    #   10. Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4001,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
    #   11. Validate Read DID response using 0x22 RDBI service.
    #   12. Validate the data sent to the COM buffer.
    #   13. Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8CA1,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
    #   14. Validate Read DID response using 0x22 RDBI service.
    #   15. Validate the data sent to the COM buffer.
    #   16. Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB9,Sensor Orientation with 0x02.
    #   17. Validate Read DID response using 0x22 RDBI service.
    #   18. Validate the data sent to the COM buffer.
    #   19. Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x01.
    #   20. Validate Read DID response using 0x22 RDBI service.
    #   21. Validate the data sent to the COM buffer.
    #  @swtest_expResult SW variables shall be updated with the valid default values.
    #  @sw_requirement{SDC-R_SW_LODM_1600, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1600-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1612, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1612-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1661, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1661-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1775, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1775-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1658, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1658-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1870, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1870-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1617, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1617-00159bc0?doors.view=00000004}
    def swTest_MountingPosition_Range_Check(self, t32_api):
        # Step 1: Set Sensor PosX with 0x4000,Sensor PosY with 0x3000,Sensor PosZ with 0x1000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
        global mp_number_failed_tests
        global mp_number_test
        mp_number_failed_tests = 0
        mp_number_test = 1
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_VALID, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, constant.CONST_WRITE_RESP_MOUNTING_POSITION, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_VALID} - DID Data written to NVM")    
        mp_number_test += 1
        
        #Step 2:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_VALID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_VALID}")
        mp_number_test += 1
        
        # Step 3: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_SENSOR_POS_Y_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_SENSOR_POS_Z_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH)
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION )

        #Step 4. Set Sensor PosX with 0x4001,Sensor PosY with 0x3000,Sensor PosZ with 0x1000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET1, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET1} - DID Data written to NVM")    
        mp_number_test += 1
        
        #Step 5:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_VALID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_VALID}")
        mp_number_test += 1
        
        # Step 6: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_SENSOR_POS_Y_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_SENSOR_POS_Z_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION)
        
        # Step 7: Set Sensor PosX with 0x4000,Sensor PosY with 0x4001,Sensor PosZ with 0x1000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET2, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET2} - DID Data written to NVM")    
        mp_number_test += 1
        
        #Step 8:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_VALID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_VALID}")
        mp_number_test += 1
        
        # Step 9: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_SENSOR_POS_Y_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_SENSOR_POS_Z_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION)

        # Step 10: Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4001,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET3, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET3} - DID Data written to NVM")    
        mp_number_test += 1
        
        #Step 11:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_VALID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data{constant.CONST_READ_RESP_MOUNTING_POSITION_VALID}")
        mp_number_test += 1
        
        # Step 12: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_SENSOR_POS_Y_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_SENSOR_POS_Z_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH)
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION)

        # Step 13: Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8CA1,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x02.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET4, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET4} - DID Data written to NVM")    
        mp_number_test += 1
        
        #Step 14:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_VALID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data{constant.CONST_READ_RESP_MOUNTING_POSITION_VALID}")
        mp_number_test += 1
        
 
        # Step 15: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_SENSOR_POS_Y_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_SENSOR_POS_Z_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION)
        
        # Step 16: Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB9,Sensor Orientation with 0x02.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET5, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET5} - DID Data written to NVM")    
        mp_number_test += 1
        
        #Step 17:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_VALID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_VALID}")
        mp_number_test += 1

        # Step 18: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_SENSOR_POS_Y_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_SENSOR_POS_Z_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION)
        
        # Step 19: Set Sensor PosX with 0x4000,Sensor PosY with 0x4000,Sensor PosZ with 0x4000,Sensor Azimuth with 0x8CA0,Sensor Elevation with 0x0BB8,Sensor Orientation with 0x01.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET6, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        time.sleep(1) 
        
        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, DID_response, diagConstant.CONST_OUT_OF_RANGE_NRC, 
                                                   f"write {constant.CONST_WRITE_REQ_MOUNTING_POSITION_INVALID_SET6} - DID Data written to NVM")    
        mp_number_test += 1
        
        #Step 20:Validate Read DID response using 0x22 RDBI service.
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, constant.CONST_READ_REQ_MOUNTING_POSITION, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2) 
              
        ExpectedData = constant.CONST_READ_RESP_MOUNTING_POSITION_VALID

        mp_number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, mp_number_test, Read_DID, ExpectedData, f"Read Mounting position and misalignment data {constant.CONST_READ_RESP_MOUNTING_POSITION_VALID}")
        mp_number_test += 1
     
        # Step 21: Validate the data sent on the communication bus.
        mp_number_failed_tests += self.Validate_COMBuffer_MountX(constant.CONST_PHYS_MAX_SENSOR_POS_X)
        mp_number_failed_tests += self.Validate_COMBuffer_MountY(constant.CONST_PHYS_SENSOR_POS_Y_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_MountZ(constant.CONST_PHYS_SENSOR_POS_Z_VALUE_SET1)
        mp_number_failed_tests += self.Validate_COMBuffer_Azimuth(constant.CONST_PHYS_MAX_SENSOR_AZIMUTH )
        mp_number_failed_tests += self.Validate_COMBuffer_Elevation(constant.CONST_PHYS_MAX_SENSOR_ELEVATION )
        mp_number_failed_tests += self.Validate_COMBuffer_Orientation(constant.CONST_PHYS_MAX_SENSOR_ORIENTATION)

        return CTestCaseResult(mp_number_test, mp_number_failed_tests)

    ## @swtest_description The test case checks if Measurement Program Index updates as per DID 060C for valid values of DMP index , Dmp selector , velocity range 1 and velocity range 2
    #  @swtest_step
    #   1. Set EgoData_VehSpd with value 0m/s.
    #   2. Write DID 060C with a DMP index value 00 and DMP selector value 00.
    #   3. Write DID 060C with a DMP index value 01 and DMP selector value 00.
    #   4. Write DID 060C with a DMP index value 02 and DMP selector value 00.
    #   5. Write DID 060C with a DMP index value 04 and DMP selector value 00.
    #   6. Set EgoData_VehSpd with value 5.55m/s.
    #   7. Write DID 060C with a DMP index value 05 and DMP selector value 00 ,velocity range 1 as 30kph , velocity range 2 as 60kph.
    #   8. Set EgoData_VehSpd with value 11.11m/s.
    #   9. Validate Mode 2 is delivered as per the ego vehicle.
    #   10. Set EgoData_VehSpd with value 19.44m/s. 
    #   11. Validate Mode 4 is delivered as per the ego vehicle velocity.
    #  @swtest_expResult SW variables shall be updated with DID values immediately. 
    #  @sw_requirement{SDC-R_SW_LODM_1849, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1849-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1851, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1851-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1853, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1853-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1875, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1875-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1862, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1862-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1774, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1774-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1852, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1852-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1671, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1671-00159bc0?doors.view=00000004}
    
    def swTest_MeasurementProgramIndex_via_DID(self, t32_api):
        number_failed_tests = 0
        number_test = 1
       
       # Step 1:From RBS LGP on Eth Panel, send Velocity data = 0 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 0.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
       
       # Step 2: Write DID 060C with a DMP index value 00 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP01
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000000FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00
       
         
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP00 , "Measurement Program Index Auto Mode")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue, dmp_index , "dsp DmpID Default value")
        number_test += 1
        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
               

       # Step 3: Write DID 060C with a DMP index value 01 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP01
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000100FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
         
        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_65_115KPH
                 
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue,dmp_index , "Measurement Program Index DMP01")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue, dmp_index , "dsp DmpID Mode 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
   

       # Step 4: Write DID 060C with a DMP index value 02 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP02
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000200FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_65_115KPH
         
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue,dmp_index , "Measurement Program Index DMP02")
        number_test += 1
        
        dsp_DmpID_DefValue = format(format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x'))
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 2")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 
       # Step 5: Write DID 060C with a DMP index value 04 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP04
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000400FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP04
         
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, dmp_index , "Measurement Program Index DMP04")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 4")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 

       # Step 6: From RBS LGP on Eth Panel, send Velocity data = 5.55 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 5.55)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
          
         
       # Step 7: Write DID 060C with a DMP index value 05 and DMP selector value 00 and deliver Mode 1
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP01
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000500001E003C00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger) 

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_30_60KPH

        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, dmp_index , "Measurement Program Index DMP01")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 1")
        number_test += 1
 
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
     
       # Step 8: From RBS LGP on Eth Panel, send Velocity data = 11.11 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 11.11)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
            

       # Step 9: Validate Mode 2 is delivered
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP02

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_30_60KPH

        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, dmp_index , "Measurement Program Index DMP02")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 2")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1

 
      # Step 10: From RBS LGP on Eth Panel, send Velocity data = 19.44 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 19.44)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
            
       # Step 11: Validate Mode 4 is delivered
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP04

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_30_60KPH

        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, dmp_index , "Measurement Program Index DMP04")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 4")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")


        return CTestCaseResult(number_test, number_failed_tests)


    ## @swtest_description The test case checks if Measurement Program Index updates as per DID 060C for valid values of DMP index , Dmp selector , velocity range 1 and velocity range 2
    #  @swtest_step
    #   1. Set EgoData_VehSpd with value 25.0 m/s.
    #   2. Write DID 060C with a DMP index value 05 and DMP selector value 00 ,velocity range 1 as 100kph ,velocity range 2 as 150kph.
    #   3. Write DID 060C with a DMP index value 05 and DMP selector value 00 ,velocity range 1 as 65kph ,velocity range 2 as 115kph.
    #  @swtest_expResult SW variables shall be updated with DID values immediately. 
    #  @sw_requirement{SDC-R_SW_LODM_1849, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1849-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1851, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1851-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1853, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1853-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1875, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1875-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1862, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1862-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1774, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1774-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1852, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1852-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1671, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1671-00159bc0?doors.view=00000004}
    
    def swTest_MeasurementProgramIndex_via_DIDWrite_Default_Value(self, t32_api):
        number_failed_tests = 0
        number_test = 1
       
       # Step 1:From RBS LGP on Eth Panel, send Velocity data = 25.0 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 25.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
       
       # Step 2: Write DID 060C with a DMP index value 05 and DMP selector value 00 ,velocity range 1 as 100kph ,velocity range 2 as 150kph 

        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP01
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C0005000064009600", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger) 

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_100_150KPH

        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, dmp_index , "Measurement Program Index DMP01")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1

       # Step 3: Write DID 060C with default velocity value . 

        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C0005000041007300", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger) 

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP05_65_115KPH

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")

        return CTestCaseResult(number_test, number_failed_tests)

          
    ## @swtest_description The test case checks the Measurement Program Index delivered to DSP as per DID 060C for invalid values of DMP index , Dmp selector , velocity range 1 and velocity range 2
    #  @swtest_step
    #   1. Set EgoData_VehSpd with value 0m/s.
    #   2. Write DID 060C with a DMP index value 00 and DMP selector value 00.
    #   3. Write DID 060C with a DMP index value 01 and DMP selector value 00.
    #   4. Write DID 060C with a DMP index value 03 and DMP selector value 00.
    #   5. Write DID 060C with a DMP index value 04 and DMP selector value 00.
    #  @swtest_expResult SW variables shall be updated with DID values immediately. 
    #  @sw_requirement{SDC-R_SW_LODM_1849, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1849-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1851, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1851-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1853, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1853-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1875, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1875-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1862, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1862-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1774, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1774-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1852, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1852-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1671, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1671-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1861, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1861-00159bc0?doors.view=00000004}
    
    def swTest_MeasurementProgramIndex_via_DID_InValidValue(self, t32_api):
        number_failed_tests = 0
        number_test = 1
       
       # Step 1:From RBS LGP on Eth Panel, send Velocity data = 0 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 0.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
       
       # Step 2: Write DID 060C with a DMP index value 00 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP01
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000000FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
                 
        ExpectedData =  diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00
       
         
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP00 , "Measurement Program Index Auto Mode")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue, dmp_index , "dsp DmpID Default value")
        number_test += 1
        
        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
               

       # Step 3: Write DID 060C with a DMP index value 01 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP01
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000100FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
         
        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_65_115KPH
                 
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue,dmp_index , "Measurement Program Index DMP01")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue, dmp_index , "dsp DmpID Mode 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
   

       # Step 4: Write DID 060C with a DMP index value 03 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP01
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000300FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     


        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_65_115KPH
         
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, dmp_index , "Measurement Program Index DMP01")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 
       # Step 5: Write DID 060C with a DMP index value 04 and DMP selector value 00
        dmp_index = diagConstant.CONST_DIAG_UDS_DID_DMP04
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000400FFFFFFFF00", self.logger)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP04
         
        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, dmp_index , "Measurement Program Index DMP04")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue,dmp_index , "dsp DmpID Mode 4")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
 
        return CTestCaseResult(number_test, number_failed_tests)


    ## @swtest_description The test case checks if Measurement Program Index updates as per PDU data sent through RBS
    #  @swtest_step
    #   1. Set EgoData_VehSpd with value 0m/s.
    #   2. Write DID 060C with a DMP index value 00 and DMP selector value 01.
    #   3. Send DMP index value 00 through Measurement Program PDU.
    #   4. Send DMP index value 01 through Measurement Program PDU.
    #   5. Send DMP index value 02 through Measurement Program PDU.
    #   6. Send DMP index value 04 through Measurement Program PDU.
    #   7. Set EgoData_VehSpd with value 20m/s.
    #   8. Set velocity range 1 as 90kph and velocity range 2 as 150kph via DID.
    #   9. Send DMP index value 05 through Measurement Program PDU.
    #   10. Set EgoData_VehSpd with value 30m/s.
    #   11. Set EgoData_VehSpd with value 50m/s.
    #  @swtest_expResult Measurement Program Index variable shall be updated as per PDU data.
    #  @sw_requirement{SDC-R_SW_LODM_1850, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1850-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1863, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1863-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1860, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1860-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1861, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1861-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1852, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1852-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1851, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1851-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1875, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1875-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1862, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1862-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1774, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1774-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1671, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1671-00159bc0?doors.view=00000004}
    
    def swTest_MeasurementProgramIndex_via_PDU(self, t32_api):
        number_failed_tests = 0
        number_test = 1


       # Step 1: From RBS LGP on Eth Panel, send Velocity data = 0 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 0.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
            
        # Step 2: Write DID 060C with Selector as 1 (PDU data to be considered for updating Measurement Program data)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000001FFFFFFFF00", self.logger)
        time.sleep(1)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00_SELECTOR_1

        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP00, "Measurement Program Index Default value")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID Default value")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1

        # Step 3: Send the Measurement Program Index as 0 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP00, "Measurement Program Index value 0")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID value 0")
        number_test += 1


        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1


        # Step 4: Send the Measurement Program Index as 1 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1,diagConstant.CONST_DIAG_UDS_DID_DMP01, "Measurement Program Index value 1")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID value 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1

        # Step 5: Send the Measurement Program Index as 2 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 2)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP02, "Measurement Program Index value 2")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP02, "dsp DmpID value 2")
        number_test += 1
 

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 
        # Step 6: Send the Measurement Program Index as 4 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 4)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP04_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP04, "Measurement Program Index value 4")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP04, "dsp DmpID value 4")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
         
        # Step 7: From RBS LGP on Eth Panel, send Velocity data = 20 m/s (-100.0 to +100.0 m/s)
        
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 20.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
       
        # Step 8: Set velocity range 1 as 90kph and velocity range 2 as 150kph
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060CFFFF01005A009600", self.logger)
        time.sleep(1)

        
        # Step 9: Send Measurement Program Index as 5 
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 5)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_90_150KPH
 
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP01, "Measurement Program Index value 1")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID value 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 

        # Step 10: From RBS LGP on Eth Panel, send Velocity data = 30 m/s (-100.0 to +100.0 m/s)

        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 30.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_90_150KPH
 
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP02, "Measurement Program Index value 2")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP02, "dsp DmpID value 2")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 

        # Step 11: From RBS LGP on Eth Panel, send Velocity data = 50 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 50.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
 
        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP04_90_150KPH
 
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP04, "Measurement Program Index value 4")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP04, "dsp DmpID value 4")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
        
        # Writing Back the default value velocity value
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060CFFFF000041007300", self.logger)
        time.sleep(1)


        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00
        
        # From RBS LGP on Eth Panel, send Velocity data = 0 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 0.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Send Measurement Program Index as 0 and set the velocity range
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)


        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
          
        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if invalid data sent through RBS for Measurement Program Index is not considered by SW
    #  @swtest_step
    #   1. Write DID 060C with  DMP selector value 01 
    #   2. Send the Measurement Program Index as 1 through PDU.
    #   3. Send the Measurement Program Index as 2 through PDU.
    #   4. Send the Measurement Program Index as 3 through PDU.
    #   5. Send the Measurement Program Index as 4 through PDU.
    #  @swtest_expResult Invalid value send through RBS for Measurement Program Index shall not be updated.
    #  @sw_requirement{SDC-R_SW_LODM_1850, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1850-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1863, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1863-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1860, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1860-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1861, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1861-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1852, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1852-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1851, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1851-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1875, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1875-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1862, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1862-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1774, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1774-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1671, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1671-00159bc0?doors.view=00000004}
    
    def swTest_MeasurementProgramIndex_via_PDU_InvalidValue_run(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: Write DID 060C with Selector as 1 (PDU data to be considered for updating Measurement Program data)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000001FFFFFFFF00", self.logger)
        time.sleep(1)
        
        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00_SELECTOR_1

        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP00, "Measurement Program Index Default value")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID Default value")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
  
        # Step 2: Send the Measurement Program Index as 1 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP01_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1,diagConstant.CONST_DIAG_UDS_DID_DMP01, "Measurement Program Index value 1")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID value 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
  
        # Step 3: Send the Measurement Program Index as 2 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 2)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1,diagConstant.CONST_DIAG_UDS_DID_DMP02, "Measurement Program Index value 2")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP02, "dsp DmpID value 2")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
  
        # Step 4: Send the Measurement Program Index as 3 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 3)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP02_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP02, "Measurement Program Index value 2")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP02, "dsp DmpID value 2")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
  
        # Step 5: Send the Measurement Program Index as 4 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 4)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)
 
        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP04_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1,diagConstant.CONST_DIAG_UDS_DID_DMP04, "Measurement Program Index value 4")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1,diagConstant.CONST_DIAG_UDS_DID_DMP04, "dsp DmpID value 4")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
  
        # Writing Back the default value
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000000FFFFFFFF00", self.logger)
        time.sleep(1)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00
        
        # From RBS LGP on Eth Panel, send Velocity data = 0 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 0.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Send Measurement Program Index as 0 and set the velocity range
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
                  
        return CTestCaseResult(number_test, number_failed_tests)
        
        
    ## @swtest_description The test case checks if invalid data sent through RBS for Measurement Program Index is not considered by SW immediately after reset
    #  @swtest_step
    #   1. Write DID 060C with Selector as 1. 
    #   2. Send the Measurement Program Index as 3 through PDU.
    #   3. Send the Measurement Program Index as 3 through PDU (Invalid value).
    #  @swtest_expResult Invalid value send through RBS for Measurement Program Index shall not be updated and auto mode should be delivered to DSP .
    #  @sw_requirement{SDC-R_SW_LODM_1850, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1850-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1863, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1863-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1860, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1860-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1861, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1861-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1852, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1852-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1851, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1851-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1875, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1875-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1862, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1862-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1774, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1774-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1671, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1671-00159bc0?doors.view=00000004}
    
    def swTest_MeasurementProgramIndex_via_PDU_InvalidValue_afterreset(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: Write DID 060C with Selector as 1 (PDU data to be considered for updating Measurement Program data)
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "2E060C000001FFFFFFFF00", self.logger)
        time.sleep(1)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00_SELECTOR_1

        m_dmpIndex_DefValue = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP00, "Measurement Program Index Default value")
        number_test += 1
        
        dsp_DmpID_DefValue = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_DefValue, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID Default value")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 
        # Step 2: Send the Measurement Program Index as 3 through PDU
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 3)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        ExpectedData = diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00_SELECTOR_1
        
        m_dmpIndex_Value1 = format(t32_api.get_variable_value("scom::g_ad_radar_apl_component_DMP_x_DMP_Runnable_m_dmpIndex_out_local.m_arrayPool[4].elem.m_dmpIndex")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_dmpIndex_Value1,diagConstant.CONST_DIAG_UDS_DID_DMP00, "Measurement Program Index value 1")
        number_test += 1
        
        dsp_DmpID_Value1 = format(t32_api.get_variable_value("rbDsp::DspCopyDataPacket.CopyModDataPacket.DmpID")['vvalue'].value,'04x')
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dsp_DmpID_Value1, diagConstant.CONST_DIAG_UDS_DID_DMP01, "dsp DmpID value 1")
        number_test += 1

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
        number_test += 1
 
        # Writing Back the default value

        # From RBS LGP on Eth Panel, send Velocity data = 0 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 0.0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Send Measurement Program Index as 0 and set the velocity range
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "MeasPgm_ID", 0)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MeasurementProgram_Input", "trigger", 1)
        time.sleep(0.5)

        #Read Measurement Program data            
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, "22060C", self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, Read_DID, ExpectedData, "Read DID Measurement Program data")
         
        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if Vehicle velocity sent through RBS is updated to DSP
    #  @swtest_step
    #   1. From RBS LGP on Eth Panel, send Velocity data = 56.32 m/s () -100.0 to +100.0 m/s)
    #   2. Check if out mempool to DSP is updated with Velocity value (after conversion)
    #   3. From RBS LGP on Eth Panel, send Velocity data = -40.51 m/s () -100.0 to +100.0 m/s)
    #   4. Check if out mempool to DSP is updated with Velocity value (after conversion)
    #  @swtest_expResult Vehicle velocity sent through RBS is updated to DSP
    #  @sw_requirement{SDC-R_SW_LODM_1653, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1653-00159bc0?doors.view=00000004}
    def swTest_VehVelocity_RBS_DSP(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: From RBS LGP on Eth Panel, send Velocity data = 56.32 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", 56.320)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Step 2: Check if out mempool to DSP is updated with Velocity value (after conversion) Conversion factor = RBS_value * 256
        m_VehVelocity_Value1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRef_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehVelocity_Value1['vvalue'].value, 14417, "Vehicle Velocity value 1")
        number_test += 1

        # Step 3: From RBS LGP on Eth Panel, send Velocity data = -40.51 m/s (-100.0 to +100.0 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpd", -40.51)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Step 4: Check if out mempool to DSP is updated with Velocity value (after conversion) Conversion factor = RBS_value * 256
        m_VehVelocity_Value2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRef_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehVelocity_Value2['vvalue'].value, -10370, "Vehicle Velocity value 2")

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if Vehicle Velocity Quality/Standard Deviation sent through RBS is updated to DSP
    #  @swtest_step
    #   1. From RBS LGP on Eth Panel, send Velocity data = 18 m/s (-128.0 to +127.99 m/s)
    #   2. Check if out mempool to DSP is updated with Velocity Quality/Standard Deviation value (after conversion)
    #   3. From RBS LGP on Eth Panel, send Velocity data = -20.51 m/s (-128.0 to +127.99 m/s)
    #   4. Check if out mempool to DSP is updated with Velocity Quality/Standard Deviation value (after conversion)
    #  @swtest_expResult Vehicle velocity Quality/Standard Deviation sent through RBS is updated to DSP
    #  @sw_requirement{SDC-R_SW_LODM_1652, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1652-00159bc0?doors.view=00000004}
    def swTest_VehVelocityErr_RBS_DSP(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: From RBS LGP on Eth Panel, send Velocity data Quality/Standard Deviation = 18.314 m/s (-128.0 to +127.99 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", 18.314)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Step 2: Check if out mempool to DSP is updated with Velocity value (after conversion) Conversion factor = RBS_value * 256
        m_VehSpdStdDev_Value1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRefErr_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehSpdStdDev_Value1['vvalue'].value, 4688, "Vehicle Quality/Standard Deviation value 1")
        number_test += 1

        # Step 3: From RBS LGP on Eth Panel, send Velocity data Quality/Standard Deviation = -4.510 m/s (-128.0 to +127.99 m/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "EgoData_VehSpdStdDev", -4.510)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
       
        # Step 4: Check if out mempool to DSP is updated with Velocity value (after conversion) Conversion factor = RBS_value * 256
        m_VehSpdStdDev_Value2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.vxvRefErr_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehSpdStdDev_Value2['vvalue'].value, -1154, "Vehicle Quality/Standard Deviation value 2")

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if Vehicle Acceleration sent through RBS is updated to DSP
    #  @swtest_step
    #   1. From RBS LGP on Eth Panel, send acceleration data = 0.314 m/s^2 (-16.0 to + 15.99 m/s^2)
    #   2. Check if out mempool to DSP is updated with acceleration value (after conversion)
    #   3. From RBS LGP on Eth Panel, send acceleration data = -4.51 m/s^2 (-16.0 to + 15.99 m/s^2)
    #   4. Check if out mempool to DSP is updated with acceleration value (after conversion)
    #  @swtest_expResult Vehicle Acceleration sent through RBS is updated to DSP
    #  @sw_requirement{SDC-R_SW_LODM_1651, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1651-00159bc0?doors.view=00000004}
    def swTest_VehAcceleration_RBS_DSP(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: From RBS LGP on Eth Panel, send acceleration data = 0.314 m/s^2 (-16.0 to + 15.99 m/s^2)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "xRR_LGU_EgoData_LogAcc", 0.314)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Step 2: Check if out mempool to DSP is updated with acceleration value (after conversion) Conversion factor = RBS_value * 2048
        m_VehAcceleration_Value1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.axvRef_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehAcceleration_Value1['vvalue'].value, 643, "Vehicle acceleration value 1")
        number_test += 1

        # Step 3: From RBS LGP on Eth Panel, send acceleration data = -4.510 m/s^2 (-16.0 to + 15.99 m/s^2)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "xRR_LGU_EgoData_LogAcc", -4.510)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
      
        # Step 4: Check if out mempool to DSP is updated with acceleration value (after conversion) Conversion factor = RBS_value * 2048
        m_VehAcceleration_Value2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.axvRef_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehAcceleration_Value2['vvalue'].value, -9236, "Vehicle acceleration value 2")

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if Vehicle Yaw rate sent through RBS is updated to DSP
    #  @swtest_step
    #   1. From RBS LGP on Eth Panel, send Yaw rate data = 0.274 deg/s(-114.59 to +114.59 deg/s)
    #   2. Check if out mempool to DSP is updated with Yaw rate value (after conversion)
    #   3. From RBS LGP on Eth Panel, send Yaw rate data = -4.51 m/s (-114.59 to +114.59 deg/s)
    #   4. Check if out mempool to DSP is updated with Yaw rate value (after conversion)
    #  @swtest_expResult Vehicle Yaw rate sent through RBS is updated to DSP
    #  @sw_requirement{SDC-R_SW_LODM_1675, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1675-00159bc0?doors.view=00000004}
    def swTest_VehYawRate_RBS_DSP(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # Step 1: From RBS LGP on Eth Panel, send YawRate data = 0.274 m/s^2 (-114.59 to +114.59 deg/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "xRR_LGU_EgoData_RelYawRate", 0.274)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Step 2: Check if out mempool to DSP is updated with YawRate value (after conversion) Conversion factor = RBS_value * 16384 (norm value) * 0.017453292519943 (deg to rad)
        m_VehAcceleration_Value1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.psiDtOpt_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehAcceleration_Value1['vvalue'].value, 78, "Vehicle YawRate value 1")
        number_test += 1

        # Step 3: From RBS LGP on Eth Panel, send YawRate data = -4.51 m/s^2 (-114.59 to +114.59 deg/s)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "xRR_LGU_EgoData_RelYawRate", -4.51)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "Ego_VehicleData", "trigger", 1)
        time.sleep(0.5)
        
        # Step 4: Check if out mempool to DSP is updated with YawRate value (after conversion) Conversion factor = RBS_value * 16384 (norm value) * 0.017453292519943 (deg to rad)
        m_VehAcceleration_Value2 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_EgoVehDataIF_out_local.m_arrayPool[4].elem.psiDtOpt_sw")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, m_VehAcceleration_Value2['vvalue'].value, -1289, "Vehicle YawRate value 2")

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if LGP Version Info  is sent as LGP header
    #  @swtest_step
    #   1. Read the PDU signal LGU_LocData_LgpVer , check if the value is updated as per SW version.
    #   2. Confirm same value is updated in Sensorfeedback PDUs.
    #  @swtest_expResult LGP Version Information shall be sent as LGP header.
    #  @sw_requirement{SDC-R_SW_LODM_1763, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1763-00159bc0?doors.view=00000004}
    def swTest_LgpVersion_LGU_LocData_PDU(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # 1. Read the PDU signal LGU_LocData_LgpVer , check if the value is updated as per SW version
        LGU_LocData_LgpVer = self.canoe_api.getSysVar("ROS_LGP_Client", "Loc_Data", "xRR_LGU_LocData_LgpVer")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_LocData_LgpVer,k_lguLocDataLgpVer,"Canoe getSysVar(\"ROS_LGP_Client\", \"Loc_Data\", \"xRR_LGU_LocData_LgpVer\")")
        number_test += 1
        
        # 2. Read the PDU signal LGU_FeedBack_LgpVer , check if the value is updated as per SW version
        LGU_FeedBack_LgpVer = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "xRR_LGU_FeedBack_LgpVer")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_FeedBack_LgpVer, k_lguLocDataLgpVer, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"xRR_LGU_FeedBack_LgpVer\")")

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if LocDataPDU block counter is updated within range.
    #  @swtest_step
    #   1. Read the PDU signal LGU_LocData_BlockCounter
    #  @swtest_expResult Block counter value is updated with range of 0 to 15.
    #  @sw_requirement{SDC-R_SW_LODM_1789, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1789-00159bc0?doors.view=00000004}
    def swTest_blockcounter_LGU_LocData_PDU(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # 1. Read the PDU signal LGU_LocData_BlockCounter
        for i in range(0,10):
            BlockCounter = self.canoe_api.getSysVar("ROS_LGP_Client","Loc_Data", "xRR_LGU_LocData_BlockCounter")

            number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test,BlockCounter, k_blockCounterMin,"Canoe getSysVar(\"ROS_LGP_Client\", \"Loc_Data\", \"xRR_LGU_LocData_BlockCounter\")")
            number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test,BlockCounter, k_blockCounterMax,"Canoe getSysVar(\"ROS_LGP_Client\", \"Loc_Data\", \"xRR_LGU_LocData_BlockCounter\")")
            number_test += 1
            time.sleep(0.3)

        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case validates the Sensor Feedback Channel signals on bus
    #  @swtest_step
    #   1. Read the PDU signal LGU_FeedBack_LgpVer.
    #   2. Get Sensor Feedback PDU Timestamp seconds signal value from bus
    #       value 0 : Nanoseconds value has not changed, but seconds value has changed
    #       value 1 : Nanoseconds value has changed
    #   3. Wait for seconds signal value to change
    #   4. Get Sensor Feedback PDU Timestamp seconds signal value from bus
    #   5. Verify if seconds information is incremented by 1
    #   6. Wait until nanoseconds signal value has rolled over and is lesser than 0.6 seconds to verify increment behavior
    #   7. Get Sensor Feedback PDU Timestamp nanoseconds signal value from bus
    #   8. Wait until nanoseconds value has changed from current value
    #   9. Get Sensor Feedback PDU Timestamp nanoseconds signal value from bus
    #   10. Verify if nanoseconds signal value is updated
    #   11. Read the PDU signal LGU_FeedBack_TimeS and LGU_FeedBack_TimeNs.
    #   12. Update MCS data from the DID and check the sync type and sensor timeoffset signal on the bus
    #   13. Update MCS data from the PDU and check the sync type and sensor timeoffset signal on the bus
    #   14. switch ON STBM PTP from RBS 
    #   15. Validate StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus is 0x08, com buffer and Sensor Feedback PDU TimeSyncState signal is updated
    #   14. switch OFF STBM PTP from RBS 
    #   15. Validate StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus is 0x09, com buffer and Sensor Feedback PDU TimeSyncState signal is updated
    #   @swtest_expResult Sensor Feedback Channel shall update the signals properly on bus
    #   @sw_requirement{SDC-R_SW_LODM_1715, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1715-00159bc0?doors.view=00000004}
    #   @sw_requirement{SDC-R_SW_COMA_1196, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1196-00159bc3?doors.view=00000005}
    #   @sw_requirement{SDC-R_SW_LODM_1712, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1712-00159bc0?doors.view=00000004}
    #   @sw_requirement{SDC-R_SW_COMA_1282, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1282-00159bc3?doors.view=00000005}
    def swTest_sensorfeedback_channel_PDU(self, t32_api):
        number_failed_tests = 0
        number_test = 1
        
        if(not self.isTxCommunication("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeS")):
            self.logger.debug("Communication Error!! ")
            number_failed_tests = 1
            return CTestCaseResult(number_test, number_failed_tests)        

        time.sleep(2)
        
        # 1. Read the PDU signal LGU_FeedBack_LgpVer.
        LGU_FeedBack_LgpVer = format(self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output","FeedBack_LgpVer"),'08x')

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_FeedBack_LgpVer, k_lgpVersion, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_LgpVer\")")
        number_test += 1
        
        time.sleep(2)
        
        #2. Get Sensor Feedback PDU Timestamp seconds signal value from bus
        timeStSec_current = self.canoe_api.getSysVar("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeS")

        #3. Wait for seconds signal value to change
        while(timeStSec_current == self.canoe_api.getSysVar("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeS")):
            continue

        #4. Get Sensor Feedback PDU Timestamp seconds signal value from bus
        timeStSec_next = self.canoe_api.getSysVar("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeS")

        #5. Verify if seconds information is incremented by 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, timeStSec_next, timeStSec_current+1,"Timestamp seconds is incremented by 1 after each second")
        number_test += 1
        
        time.sleep(2)
        
        #6. Wait until nanoseconds signal value has rolled over and is lesser than 0.6 seconds to verify increment behavior
        while(self.canoe_api.getSysVar("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeNs") > 600000000):
            continue
        
        #7. Get Sensor Feedback PDU Timestamp nanoseconds signal value from bus
        timeStNs_current = self.canoe_api.getSysVar("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeNs")
        
        #8. Wait until nanoseconds value has changed from current value
        while(timeStNs_current == self.canoe_api.getSysVar("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeNs")):
            continue
        
        #9. Get Sensor Feedback PDU Timestamp nanoseconds signal value from bus
        timeStNs_next = self.canoe_api.getSysVar("ROS_LGP_Client","Sensorfeedback_Output", "FeedBack_TimeNs")
        
        #10. Verify if nanoseconds signal value is updated
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, timeStNs_next, timeStNs_current,"Nanoseconds incremented in next cycle")
        number_test += 1

        self.logger.debug(f"time nanoseconds current = {timeStNs_current}, time nanoseconds next = {timeStNs_next} ")
        
        time.sleep(2)        

        #11. Read the PDU signal LGU_FeedBack_TimeS and LGU_FeedBack_TimeNs.
        LGU_FeedBack_TimeS = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output","FeedBack_TimeS")

        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, LGU_FeedBack_TimeS, k_lguFeedBackStbmTimeMin, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_TimeS\")")
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, LGU_FeedBack_TimeS, k_lguFeedbackStbmTimeMax, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_TimeS\")")
        number_test += 1
        
        LGU_FeedBack_TimeNs = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_TimeNs")

        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, LGU_FeedBack_TimeNs, k_lguFeedBackStbmTimeMin, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_TimeNs\")")
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, LGU_FeedBack_TimeNs, k_lguFeedbackStbmTimeMax,
                                                   "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_TimeNs\")")
        number_test += 1
          
        time.sleep(2)

        #12. Update MCS data from the DID and check the sync type and sensor timeoffset signal on the bus
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_YES + constant.CONST_MCS_SENS_OFFSET_MIN + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ZERO
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(2)

        MCSSyncTypeValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue1['vvalue'].value, k_timeslotSyncValue, "MCS Sync Type value written from DID")
        number_test += 1
        
        MCSOffsetValue1 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        # Multiplying the daddy recieved value by factor of 2 as per DSP requirements
        MCSOffsetValue_1 = MCSOffsetValue1['vvalue'].value * 2
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue_1, k_sensorTimeOffsetMin, "MCS Offset value written from DID")
        number_test += 1
        
        LGU_FeedBack_SyncType = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_SyncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_FeedBack_SyncType, k_timeslotSyncValue, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_SyncType\")")
        number_test += 1
        
        LGU_FeedBack_SenTimeOff = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_SenTimeOff")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_FeedBack_SenTimeOff, k_sensorTimeOffsetMin, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_SenTimeOff\")")
        number_test += 1

        time.sleep(2)
        
        #13. Update MCS data from the PDU and check the sync type and sensor timeoffset signal on the bus
        serviceRequestString = diagConstant.CONST_DIAG_UDS_SERVICE_WDBI + diagConstant.CONST_DIAG_UDS_DID_MCS + \
            constant.CONST_MCS_SYNC_TYPE_NO + constant.CONST_MCS_SENS_OFFSET_DEF + constant.CONST_MCS_RESERVED + constant.CONST_MCS_SELECTOR_ONE
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, serviceRequestString, self.logger)
        time.sleep(1)
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(2)

        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SyncType", 1)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "MCS_SenTimeOff", k_sensorTimeOffsetMax)
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "MCS", "trigger", 1)
        time.sleep(2)

        MCSSyncTypeValue4 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_syncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSSyncTypeValue4['vvalue'].value, k_timeslotSyncValue, "MCS Sync Type value updated as per PDU")
        number_test += 1
        
        MCSOffsetValue4 = t32_api.get_variable_value("scom::g_ad_radar_apl_component_EgoVehDataIF_x_EgoVehDataIF_Runnable_m_MCSData_out_local.m_arrayPool[4].elem.m_sensorTimeOffset")
        # Multiplying the daddy recieved value by factor of 2 as per DSP requirements
        MCSOffsetValue_4 = MCSOffsetValue4['vvalue'].value * 2
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, MCSOffsetValue_4, k_sensorTimeOffsetMax, "MCS Offset value updated as per PDU")
        number_test += 1

        LGU_FeedBack_SyncType = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_SyncType")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_FeedBack_SyncType, k_timeslotSyncValue, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_SyncType\")")
        number_test += 1
        
        LGU_FeedBack_SenTimeOff = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_SenTimeOff")
        self.logger.debug(f"LGU_FeedBack_SenTimeOff = {LGU_FeedBack_SenTimeOff}, Factor converted value = {LGU_FeedBack_SenTimeOff}")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, LGU_FeedBack_SenTimeOff, k_sensorTimeOffsetMax, "Canoe getSysVar(\"ROS_LGP_Client\", \"Sensorfeedback_Output\", \"FeedBack_SenTimeOff\")")
        number_test += 1

        #14. switch ON STBM PTP from RBS 
       
        self.canoe_api.setSysVarValue("RBS_Feature", "RBS_Feature_STBM_State", 1)
        time.sleep(1)
        
        #15. Validate StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus is 0x08, com buffer and Sensor Feedback PDU TimeSyncState signal is updated
        StbM_GlobalTime = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
        timebaseStatus_bufVal = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_SensorFeedbackChannelByte[29]")['vvalue'].value,'02x')
        timesyncState_ethVal = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_TimeSynSta")

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTime , comaConstant.CONST_STBM_ON,"Verify if stbm internal variable of stbm is set to 0x08")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, timebaseStatus_bufVal , comaConstant.CONST_STBM_ON,"Verify if Com buffer is set to 0x08")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, timesyncState_ethVal , int(comaConstant.CONST_STBM_ON),"Verify if ethernet PDU Signal value  is set to 0x08")
        number_test += 1
        
        #16. switch OFF STBM PTP from RBS
        
        self.canoe_api.setSysVarValue("RBS_Feature", "RBS_Feature_STBM_State", 0)
        time.sleep(1)
         
        
        #17. Validate StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus is 0x09, com buffer and Sensor Feedback PDU TimeSyncState signal is updated
        StbM_GlobalTime = format(t32_api.get_variable_value("StbM_GlobalTimeTupleArray_ast[0].timeBaseStatus")['vvalue'].value,'02x')
        timebaseStatus_bufVal = format(t32_api.get_variable_value("Com_dComIPdu_UDP_Tx_SensorFeedbackChannelByte[29]")['vvalue'].value,'02x')
        timesyncState_ethVal = self.canoe_api.getSysVar("ROS_LGP_Client", "Sensorfeedback_Output", "FeedBack_TimeSynSta")

        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, StbM_GlobalTime , comaConstant.CONST_STBM_OFF,"Verify if stbm internal variable of stbm is set to 0x08")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, timebaseStatus_bufVal , comaConstant.CONST_STBM_OFF,"Verify if Com buffer is set to 0x08")
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, timesyncState_ethVal , int(comaConstant.CONST_STBM_OFF),"Verify if ethernet PDU Signal value  is set to 0x08")
        
        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case checks if number of locations sensed by DSP is within range or not.
    #  @swtest_step
    #   1. Read the SW variable for Number of locations
    #   2. Read the DSP variable to indicate number of locations
    #  @swtest_expResult Number of locations from DSP and LODM shall be within the defined range.
    #  @sw_requirement{SDC-R_SW_LODM_1677, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1677-00159bc0?doors.view=00000004}
    def swTest_num_of_locations_by_DSP(self, t32_api):
        number_failed_tests = 0
        number_test = 1

        # 1. Read the PDU signal LGU_LocData_LgpVer , check if the value is updated as per SW version
        for i in range(0,10):
            number_of_locations_LODM = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[4].elem.m_LocationList.NumLocs")
            
            number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, number_of_locations_LODM, k_numOfLocationsMin, "Check if Number of Locations from LODM is within range")               
            number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, number_of_locations_LODM, k_numOfLocationsMax, "Check if Number of Locations from LODM is within range") 
            number_test += 1
            time.sleep(0.5)
        
        #   2. Read the DSP variable to indicate number of location
        for i in range(0,10):
            number_of_locations_DSP = t32_api.get_variable_value("rbDsp::g_locationInterface_st.m_LocationList.NumLocs")
            
            number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, number_of_locations_DSP, k_numOfLocationsMin, "Check if Number of Locations from DSP is within range")               
            number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, number_of_locations_DSP, k_numOfLocationsMax, "Check if Number of Locations from DSP is within range")               
            number_test += 1
            time.sleep(0.5)
        
        return CTestCaseResult(number_test, number_failed_tests)

    # Guard checks - to ensure if PDUs are constantly received from radar on bus and decoded by RBS
    # Function description - For a specifc Time Signal in a PDU(Seconds info), Check if the value is unique after every two seconds
    #                        for 5 consecutive cycles
    # Return Value -
    #               True  - if all 5 values of the timeSignal is unique after each second
    #               False - if anyone value of the timeSignal is repeated value of its previous value after one second
    def isTxCommunication(self, namespace, pdu_name,timeSecondsSig):
        time.sleep(5)
        pduAlive = 0
        pduCounter = 0
        while(pduCounter < 5):
            timeStSec_prev = self.canoe_api.getSysVar(namespace,pdu_name, timeSecondsSig)
        
            time.sleep(2)
        
            timeStSec_current = self.canoe_api.getSysVar(namespace,pdu_name, timeSecondsSig)
        
            if(timeStSec_current != timeStSec_prev):
                    pduAlive = pduAlive + 1
            else:
                return False
            pduCounter = pduCounter + 1
        return (pduAlive == 5)
    
    ## @swtest_description The test case validates all the signals in the location header of Location Attribute PDU.
    #  @swtest_step
    #   1. Get Location Attribute PDU LGP Version signal value from bus
    #   2. Verify if value from bus is same as the value defined in the rbBuild_Version_Cfg.h file
    #   3. Get Location Attribute PDU blockcounter signal value from bus
    #   4. Wait until blockcounter has changed value
    #   5. Get Location Attribute PDU blockcounter signal value from bus
    #   6. Check min, max range of blockcounter value read from bus
    #   7. Verify if blockcounter value has incremented by 1
    #   8. Get Location Attribute PDU Timestamp seconds signal value from bus
    #   9. Wait for seconds signal value to change
    #   10. Get Location Attribute PDU Timestamp seconds signal value from bus
    #   11. Verify if seconds information is incremented by 1
    #   12. Wait until nanoseconds signal value has rolled over and is lesser than 0.6 seconds to verify increment behavior
    #   13. Get Location Attribute PDU Timestamp nanoseconds signal value from bus
    #   14. Wait until nanoseconds value has changed from current value
    #   15. Get Location Attribute PDU Timestamp nanoseconds signal value from bus
    #   16. Verify if nanoseconds signal value is updated
    #   17. Get Opmode value from DSP Scom Senderport
    #   18. Get Opmode value from Location Attribute PDU on Bus
    #   19. Verify Opmode dsp value and value on bus are same
    #   20. Get DataMeasured value from DSP Scom Senderport
    #   21. Get DataMeasured value from Location Attribute PDU on Bus
    #   22. Verify DataMeasured dsp value and value on bus are same
    #  @swtest_expResult All Location Header signal in Location Attribute PDU must be as per LGC Specification
    #  @sw_requirement{SDC-R_SW_LODM_1763 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1763-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1789 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1789-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1835 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1835-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1701 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1701-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1836 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1836-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1724 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1724-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1726 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1726-00159bc0?doors.view=00000004}
    def swTest_locationAttribHeader_signalValidation(self, t32_api):
        number_failed_tests = 0
        number_test = 1
        
        if(not self.isTxCommunication("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeSts")):
            self.logger.debug("Communication Error!! ")
            number_failed_tests = 1
            return CTestCaseResult(number_test, number_failed_tests)

        time.sleep(2)
        
        #1. Get Location Attribute PDU LGP Version signal value from bus
        lgpVersion = format(self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_LgpVer"), '08x')
        
        #2. Verify if value from bus is same as the value defined in the rbBuild_Version_Cfg.h file
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, lgpVersion, k_lgpVersion,"Canoe getSysVar(\"ROS_LGP_Client\", \"LocAtr_PDU\", \"LocAtr_LgpVer\")")
        number_test += 1

        time.sleep(2)
               
        #3. Get Location Attribute PDU blockcounter signal value from bus
        blockcounterValue_current = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_BlockCounter")
        self.logger.debug(f"blockcounter current = {blockcounterValue_current} ")

        #4. Wait until blockcounter has changed value 
        while(blockcounterValue_current == self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_BlockCounter")):
            continue
        
        #5. Get Location Attribute PDU blockcounter signal value from bus
        blockcounterValue_next = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_BlockCounter")
        
        #6. Check min, max range of blockcounter value read from bus
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test,blockcounterValue_current, k_blockCounterMin,"Canoe getSysVar(\"ROS_LGP_Client\", \"LocAtr_PDU\", \"LocAtr_BlockCounter\")")
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test,blockcounterValue_current, k_blockCounterMax,"Canoe getSysVar(\"ROS_LGP_Client\", \"LocAtr_PDU\", \"LocAtr_BlockCounter\")")
        number_test += 1
        
        #7. Verify if blockcounter value has incremented by 1 
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test,blockcounterValue_next, blockcounterValue_current+1,"Verify if blockcounter has incremented by 1")
        number_test += 1
        
        self.logger.debug(f"blockcounter next = {blockcounterValue_next} ")

        time.sleep(2)
        
        #8. Get Location Attribute PDU Timestamp seconds signal value from bus
        timeStSec_current = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeSts")

        #9. Wait for seconds signal value to change
        while(timeStSec_current == self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeSts")):
            continue
        
        #10. Get Location Attribute PDU Timestamp seconds signal value from bus
        timeStSec_next = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeSts")

        #11. Verify if seconds information is incremented by 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, timeStSec_next, timeStSec_current+1,"Timestamp seconds is incremented by 1 after each second")
        number_test += 1
        
        time.sleep(2)
        
        #12. Wait until nanoseconds value has changed from current value
        while(self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeStns") > 600000000):
            continue
        
        #13. Get Location Attribute PDU Timestamp nanoseconds signal value from bus
        timeStNs_current = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeStns")
        
        #14. Verify if nanoseconds signal value is updated
        while(timeStNs_current == self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeStns")):
            continue
        
        #Get Location Attribute PDU Timestamp nanoseconds signal value from bus
        timeStNs_next = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_TimeStns")
        
        #16. Verify if nanoseconds signal value is updated
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, timeStNs_next, timeStNs_current,"next Nanoseconds value is greater than current nanoseconds value")
        number_test += 1

        self.logger.debug(f"time nanoseconds current = {timeStNs_current}, time nanoseconds next = {timeStNs_next} ")
        
        time.sleep(2)
            
        #17. Get Opmode value from DSP Scom Senderport 
        dspOpMode = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[4].elem.m_SensState.OpMode")
        
        #18. Get Opmode value from Location Attribute PDU on Bus
        opModeBusValue = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_OpMode")
        
        #19. Verify Opmode dsp value and value on bus are same
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, opModeBusValue, dspOpMode['vvalue'].value,"Opmode from DSP is to be sent on Bus")
        number_test += 1

        time.sleep(2)
        
        #20. Get DataMeasured value from DSP Scom Senderport 
        dspDataMeasured = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[4].elem.m_SensState.DataMeasured")
        
        #21. Get DataMeasured value from Location Attribute PDU on Bus
        dataMeasuredBusValue = self.canoe_api.getSysVar("ROS_LGP_Client","LocAtr_PDU", "LocAtr_DataMeas")
        
        #22. Verify DataMeasured dsp value and value on bus are same
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dataMeasuredBusValue, dspDataMeasured['vvalue'].value,"DataMeasured from DSP is to be sent on Bus")
        
        return CTestCaseResult(number_test, number_failed_tests)

    ## @swtest_description The test case validates all the signals in the location header of Location Data PDU.
    #  @swtest_step
    #   1. Get Location Data PDU LGP Version signal value from bus
    #   2. Verify if value from bus is same as the value defined in the rbBuild_Version_Cfg.h file
    #   3. Get Location Data PDU blockcounter signal value from bus
    #   4. Wait until blockcounter has changed value
    #   5. Get Location Data PDU blockcounter signal value from bus
    #   6. Check min, max range of blockcounter value read from bus
    #   7. Verify if blockcounter value has incremented by 1
    #   8. Get Location Data PDU Timestamp seconds signal value from bus
    #   9. Wait for seconds signal value to change
    #   10. Get Location Data PDU Timestamp seconds signal value from bus
    #   11. Verify if seconds information is incremented by 1
    #   12. Wait until nanoseconds signal value has rolled over and is lesser than 0.6 seconds to verify increment behavior
    #   13. Get Location Data PDU Timestamp nanoseconds signal value from bus
    #   14. Wait until nanoseconds value has changed from current value
    #   15. Get Location Data PDU Timestamp nanoseconds signal value from bus
    #   16. Verify if nanoseconds signal value is updated
    #   17. Get Opmode value from DSP Scom Senderport
    #   18. Get Opmode value from Location Data PDU on Bus
    #   19. Verify Opmode dsp value and value on bus are same
    #   20. Get DataMeasured value from DSP Scom Senderport
    #   21. Get DataMeasured value from Location Data PDU on Bus
    #   22. Verify DataMeasured dsp value and value on bus are same
    #   23. Get NumLoc value from DSP Scom Senderport
    #   24. Get NumLoc value from Location Data PDU on Bus
    #   25. Verify NumLoc dsp value and value on bus are same
    #   26. Verify if NumLoc dsp value is less than 1024
    #   27. Get MaxLocPerPdu value from Location Data PDU on Bus
    #   28. Verify MaxLocPerPdu is equal to 16
    #  @swtest_expResult All Location Header signal in Location Data PDU must be as per LGC Specification
    #  @sw_requirement{SDC-R_SW_LODM_1763 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1763-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1789 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1789-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1835 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1835-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1701 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1701-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1836 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1836-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1724 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1724-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1726 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1726-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1677 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1677-00159bc0?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_LODM_1846 , https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1846-00159bc0?doors.view=00000004}
    def swTest_locationDataHeader_signalValidation(self, t32_api):
        number_failed_tests = 0
        number_test = 1
        
        if(not self.isTxCommunication("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeSts")):
            self.logger.debug("Communication Error!! ")
            number_failed_tests = 1
            return CTestCaseResult(number_test, number_failed_tests)
        
        time.sleep(2)
        #1. Get Location Data PDU LGP Version signal value from bus
        lgpVersion = format(self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_LgpVer"), '08x')
        
        #2. Verify if value from bus is same as the value defined in the rbBuild_Version_Cfg.h file
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, lgpVersion, k_lgpVersion,"Canoe getSysVar(\"ROS_LGP_Client\", \"LocData_PDU_1\", \"LocData_LgpVer\")")
        number_test += 1
       
        time.sleep(2)
        
        #3. Get Location Data PDU blockcounter signal value from bus
        blockcounterValue_current = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_BlockCounter")
        self.logger.debug(f"blockcounter current = {blockcounterValue_current} ")

        #4. Wait until blockcounter has changed value 
        while(blockcounterValue_current == self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_BlockCounter")):
            continue
        
        #5. Get Location Data PDU blockcounter signal value from bus
        blockcounterValue_next = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_BlockCounter")
        
        #6. Check min, max range of blockcounter value read from bus
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test,blockcounterValue_current, k_blockCounterMin,"Canoe getSysVar(\"ROS_LGP_Client\", \"LocData_PDU_1\", \"LocData_BlockCounter\")")
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test,blockcounterValue_current, k_blockCounterMax,"Canoe getSysVar(\"ROS_LGP_Client\", \"LocData_PDU_1\", \"LocData_BlockCounter\")")
        number_test += 1
        
        #7. Verify if blockcounter value has incremented by 1 
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test,blockcounterValue_next, blockcounterValue_current+1,"Verify if blockcounter has incremented by 1")
        number_test += 1
        
        self.logger.debug(f"blockcounter next = {blockcounterValue_next} ")

        time.sleep(2)
        
        #8. Get Location Attribute PDU Timestamp seconds signal value from bus
        timeStSec_current = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeSts")

        #9. Wait for seconds signal value to change
        while(timeStSec_current == self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeSts")):
            continue
        
        #10. Get Location Attribute PDU Timestamp seconds signal value from bus
        timeStSec_next = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeSts")

        #11. Verify if seconds information is incremented by 1
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, timeStSec_next, timeStSec_current+1,"Timestamp seconds is incremented by 1 after each second")
        number_test += 1
        
        time.sleep(2)
        
        #12. Wait until nanoseconds value has changed from current value
        while(self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeStns") > 600000000):
            continue
        
        #13. Get Location Attribute PDU Timestamp nanoseconds signal value from bus
        timeStNs_current = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeStns")
        
        #14. Verify if nanoseconds signal value is updated
        while(timeStNs_current == self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeStns")):
            continue
        
        #Get Location Attribute PDU Timestamp nanoseconds signal value from bus
        timeStNs_next = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_TimeStns")
        
        #16. Verify if nanoseconds signal value is updated
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, timeStNs_next, timeStNs_current,"next Nanoseconds value is greater than current nanoseconds value")
        number_test += 1

        self.logger.debug(f"time nanoseconds current = {timeStNs_current}, time nanoseconds next = {timeStNs_next} ")
        
        time.sleep(2)
        
        #17. Get Opmode value from DSP Scom Senderport 
        dspOpMode = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[4].elem.m_SensState.OpMode")
        
        #18. Get Opmode value from Location Data PDU on Bus
        opModeBusValue = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_OpMode")
        
        #19. Verify Opmode dsp value and value on bus are same
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, opModeBusValue, dspOpMode['vvalue'].value,"Opmode from DSP is to be sent on Bus")
        number_test += 1
        
        time.sleep(2)
        
        #20. Get DataMeasured value from DSP Scom Senderport 
        dspDataMeasured = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[4].elem.m_SensState.DataMeasured")
        
        #21. Get DataMeasured value from Location Data PDU on Bus
        dataMeasuredBusValue = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_DataMeas")
        
        #22. Verify DataMeasured dsp value and value on bus are same
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, dataMeasuredBusValue, dspDataMeasured['vvalue'].value,"DataMeasured from DSP is to be sent on Bus")
        number_test += 1

        time.sleep(2)
        
        # List to append number of locations from  bus
        numLocList = list()
        # Counter to increment when different numLocs values from bus
        diffNumLocCounter = 0 
        
       #23. Get NumLoc value from DSP Scom Senderport 
        dspNumLoc = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[4].elem.m_LocationList.NumLocs")
        
        #24. Get NumLoc value from Location Data PDU on Bus
        numLocList.append(self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_NumLoc"))

        # Get 3 different values of numLocs from bus to compare with DSP value
        while(diffNumLocCounter < 3):
            while(numLocList[diffNumLocCounter] == self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_NumLoc") and numLocList[diffNumLocCounter] > 0):
                continue
            numLocList.append(self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_NumLoc"))
            diffNumLocCounter = diffNumLocCounter + 1
        
        #25. Verify NumLoc dsp value and value on bus are same
        number_failed_tests += testasserts.TEST_GE(self.logger, self.number_of_test, number_test, numLocList.count(dspNumLoc['vvalue'].value), 0,"numLocs from DSP is to be sent on Bus")
        number_test += 1
        
        self.logger.debug(f"number of locations list = {numLocList} dsp numLocs = {dspNumLoc['vvalue'].value}")
        
        #26. Verify if NumLoc bus value is less than 1024
        number_failed_tests += testasserts.TEST_LE(self.logger, self.number_of_test, number_test, numLocList[0], k_numOfLocationsMax,"numLocs on bus must be less than 1024")
        number_test += 1
        
        time.sleep(2)
        
        #27. Get MaxLocPerPdu value from Location Data PDU on Bus
        maxLocPerPdu = self.canoe_api.getSysVar("ROS_LGP_Client","LocData_PDU_1", "LocData_MaxLocPerPdu")
        
        #28. Verify MaxLocPerPdu is equal to 16
        number_failed_tests += testasserts.TEST_EQ(self.logger, self.number_of_test, number_test, maxLocPerPdu, k_maxLocPerPdu,"maxLocPerPdu Value is fixed with value 16")
        
        return CTestCaseResult(number_test, number_failed_tests)
        

    ## @swtest_description The test case is to reset the Measurement Program DID to default data as per the requirement.
    #  @swtest_step
    #   1. Write the default Measurement Program data to NVM.
    #   2. Verify Read DID  060C response.
    #  @swtest_expResult SW variables shall be updated with RAM packet values immediately. 
    #  @sw_requirement{SDC-R_SW_LODM_1849, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1849-00159bc0?doors.view=00000004}
    def swTest_MeasurementProgramIndex_via_DID_reset_default_value(self, t32_api):
        numberFailedTests = 0
        numberTest = 1

        # 1. Write the default Measurement Program data to NVM  
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagConstant.CONST_DIAG_UDS_WRITE_DID_REQ_DMP05_65_115KPH, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP") 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, diagConstant.CONST_DIAG_UDS_WRITE_RESP_DMP, 
                                                   f"DMP response {diagConstant.CONST_DIAG_UDS_WRITE_RESP_DMP}") 
        numberTest += 1

        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)    
        canoeDiagPanel.jumpToExtendedSession(self.canoe_api, self.logger)    
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagConstant.CONST_DIAG_UDS_WRITE_DID_REQ_DMP00, self.logger)
        DID_response=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP") 
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)     
       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, DID_response, diagConstant.CONST_DIAG_UDS_WRITE_RESP_DMP, 
                                                   f"DMP response {diagConstant.CONST_DIAG_UDS_WRITE_RESP_DMP}") 
        numberTest += 1

        # 2. Verify Read DID  060C response.           
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)  
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagConstant.CONST_DIAG_UDS_READ_RESP_DMP, self.logger)                     
        Read_DID=self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")     
        time.sleep(2)     
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Read_DID, diagConstant.CONST_DIAG_UDS_READ_DID_RESP_DMP00, "Read default DID Measurement Program data")

        return CTestCaseResult(numberTest, numberFailedTests)
        
        
        
        