# -*- coding: utf-8 -*-


import sys
import time
import os

sys.path.append(os.path.abspath('../../framework/helper'))
sys.path.append(os.path.abspath('../../framework/scheduling'))
sys.path.append(os.path.abspath('../../framework/interface'))

import atf_toolbox as testHelper
import atf_testasserts as testasserts
import AD_lauterbach_test_helper as lauterbachTestHelper
import rbSysEvM_testsuiteconstants as rbSysEvmConstant
import AD_canoe_diag_functions as canoeDiagPanel
import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants
import diag_testsuitebasic as diagbasic
import diag_testsuitevarianthandling as diagvarianthandling
import diag_constants as constant
from testbase import CTestCaseResult

# inputhandler/inc/interface/ihd_sensormoderequest.hpp
# based on enum class "ESensorModeRequest"
g_invalidSensorMode         = 0
g_startModulationSensorMode = 1
g_stopModulationSensorMode  = 2

# Enable trigger to sent SensorMode
g_sensorModeTriggerDisable = 0
g_sensorModeTriggerEnable  = 1

# DTC values
k_dtcUC_OVER_VOLTAGE = "d60e17"
k_dtcUC_TEMP_FAILURE = "d60e64"

# Diag service request/response
k_diagReadDtcInformationStatus = "0d"
k_diagReadDtcInformationRequest = "1902"
k_diagReadDtcInformationPositiveResponse = "5902"
k_diagClearAllDtcRequest = "14FFFFFF"

# positive response: 59020d, DTC: d60e17, status: 0d
k_ucOverVoltageDtcResponse = k_diagReadDtcInformationPositiveResponse + k_diagReadDtcInformationStatus + k_dtcUC_OVER_VOLTAGE + k_diagReadDtcInformationStatus
# positive response: 59020d, DTC#status: d60e17#0d, d60e64#0d
k_ucOverVoltageUcTempFailureDtcResponse = k_diagReadDtcInformationPositiveResponse + k_diagReadDtcInformationStatus + k_dtcUC_OVER_VOLTAGE + k_diagReadDtcInformationStatus + k_dtcUC_TEMP_FAILURE + k_diagReadDtcInformationStatus

# PDM RAM-Mirror for SensorModeRequest Nvm-DataItem
k_nvmMirrorSensorModeStatusName = "g_NvMRamMirrorSensorModeRequestNvmDataItem[4]"


class CTestSuiteRbSysEvm(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteRbSysEvm"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, self.getComponentName())
                                        
        # DemConf_DemEventParameter_RB_SLV_DSP_CYCLETIME_EXCEEDED                   206u
        self.faultEventIdCycleTimeExceeded = 206
        #define DemConf_DemEventParameter_RB_MST_MMIC_OVERTEMP_STATE                166u
        self.faultEventIdMmicOvertempState = 166
        #define DemConf_DemEventParameter_RB_MST_MMIC1_TXLOWPOW_ERR                 114u
        self.faultEventIdMmicTxLowPowErr   = 114        
        #define DemConf_DemEventParameter_RB_UC_PMSPRI_V3_OV                        381u
        self.faultEventIdRbUcPMSPRIV3Ov    = 381
        #define DemConf_DemEventParameter_RB_UC_PMS_StandbySupply_OV                413u
        self.faultEventIdRbUcPmsStandbySupplyOv  = 413
        #define DemConf_DemEventParameter_RB_UC_PMSSEC_VCore_OV                     401u
        self.faultEventIdRbUcPmssecVCoreOv       = 401
        #define DemConf_DemEventParameter_RB_UC_ADC_TEMPPLAUS_Failure               298u
        self.faultEventIdRbUcAdcTempplausFailure = 298
        #define DemConf_DemEventParameter_RB_UC_TEMP_DEFECT                         448u
        self.faultEventIdRbUcTempDefect          = 448
        #define DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF                204u
        self.faultEventIdRadarModPermanentOFF    = 204            
    
    
    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no rbSysEvM test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllRbSysEvMTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2]) 

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "rbSysEvM"

    def setSensorModeRequestInputCanoeApi(self, sensorMode):         
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "SenModReq_RadMod", sensorMode)
    
    def setSensorModeRequestTriggerCanoeApi(self, trigger):
        self.canoe_api.setSysVarMemberValue("ROS_LGP_Client", "SensorModeRequest_Input", "trigger", trigger)

    def cleanupSensorModeRequest(self, isTriggerEnabled = False):                    
        # Set start modulation as default value in NVM
        self.setSensorModeRequestInputCanoeApi(g_startModulationSensorMode)
        
        if isTriggerEnabled:
            self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)        
        
        # wait that modulation is enabled in sensor
        time.sleep(1) 
        # Stop sending SensorMode
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerDisable)
        # give the sensor some time to store the request in NVM
        time.sleep(1)  

    
    def runAllRbSysEvMTests(self, t32_api):
        numberFailedTests = self.executeFilteredFunction(t32_api)       
       
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests)
    
    
    ## @swtest_description The test case checks if the SensorMode 'startModulation' of communication interface is set as default NVM value.
    #  @swtest_step 
    #   PreconditionS: Plant container is flashed, done by the test environment. 
    #                  The Sensor mode request from diag interface in NVM is "start modulation". 
    #   1. Trigger the 'startModulation' sent from diag interface   
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Check that SensorMode is not sent on the bus     
    #   6. Check nvm mirror of communication interaface which is copied at startup from the nvm
    #  @swtest_expResult The Nvm mirror of communication interface which reflects the Nvm is set to 'startModulation'
    #  @sw_requirement{SDC-R_SW_SESM_125, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-125-00159bc1?doors.view=00000004}       
    def swTest_checkDefaultSensorMode(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)   
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mode request from diag 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest, SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        
        numberTest += 1
                
        sensorModeTrigger = self.canoe_api.getSysVar("ROS_LGP_Client", "SensorModeRequest_Input", "trigger")
    
        #5.Sending for SensorMode is disabled from communication interface       
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorModeTrigger, g_sensorModeTriggerDisable, 
                                                "Canoe getSysVar(\"ROS_LGP_Client\", \"SensorModeRequest_Input\", \"trigger\")")               
        numberTest += 1
    
        time.sleep(1) # make sure nvm data are written into ram mirror
    
        #6.Check nvm mirror of communication interaface which is copied at startup from the nvm 
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
                       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)                       
                    
        return CTestCaseResult(numberTest, numberFailedTests)  
    
    
    ## @swtest_description The test case checks if the received SensorMode request from communication interface is 
    #   reflected in the Nvm mirror to be stored in the Nvm.
    #  @swtest_step 
    #   Preconditions:RBS is running and link is up.
    #                 The Sensor mode request from diag interface in NVM is "start modulation". 
    #   1. Trigger the 'startModulation' sent from diag interface  
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Check nvm mirror of communication interface
    #   6. Trigger the SensorMode 'stopModulation' to be sent on the bus
    #   7. Verify the Nvm mirror  of communication interface reflects the status 'stopModulation'
    #   8. Trigger the SensorMode 'startModulation' to be sent on the bus        
    #   9. Verify the Nvm mirror reflects the status 'startModulation' 
    #   10.Cleanup: Set default that modulation is enabled in NVM and no further requests are sent on the bus
    #   11.  clean up: clear DTCs and reset Sensor
    #  @swtest_expResult The Nvm mirror reflects the received SensorMode requests.
    #  @sw_requirement{SDC-R_SW_SESM_126, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-126-00159bc1?doors.view=00000004}       
    def swTest_checkSensorModeInNvm(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        #Precondition: reset sensor, make sure RBS is running and link is up
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")  
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mode request from diag 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        numberTest += 1
        
        #5.Check nvm mirror of communication interface
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)    
           
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName + " after reset")    
        numberTest += 1
                              
        #6.Trigger the SensorMode 'stopModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_stopModulationSensorMode)        
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)

        time.sleep(1) # propagation into nvm from bus       

        sensorModeBusInput = t32_api.get_variable_value("scom::g_ad_radar_apl_component_inputhandler_x_CInputHandlerRunnable_m_sensorModeRequest_out_local.m_arrayPool[0].elem.m_sensorModeRequest")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorModeBusInput['vvalue'].value, 
                                                 g_stopModulationSensorMode, "Check inputhandler received sensorModeRequest signal")
            
        #7.Verify the Nvm mirror of communication interface reflects the status 'stopModulation'
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)    
           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_stopModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)    
        numberTest += 1
        
        #8.Trigger the SensorMode 'startModulation' to be sent on the bus        
        self.setSensorModeRequestInputCanoeApi(g_startModulationSensorMode)        
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)    
        
        #9. Verify the Nvm mirror of communication interface reflects the status 'startModulation' 
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)    
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)
    
        #10.Cleanup - Stop sending SensorMode                
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerDisable)  
        
        #11.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 11: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)    
    
    
    ## @swtest_description The test case checks if the fault status 'DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF' 
    #   is set correctly if a 'stopModulation' request from communication interface is issued.
    #  @swtest_step 
    #   Preconditions: The Sensor mode request from diag interface in NVM is "start modulation".             
    #   1. Trigger the 'startModulation' sent from diag interface   
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Trigger the SensorMode 'stopModulation' to be sent on the bus
    #   6. Verify the Nvm mirror reflects the status 'stopModulation'
    #   7. Check fault status
    #   8. Cleanup: Set default that modulation is enabled in NVM and no further requests are sent on the bus
    #   9.  clean up: clear DTCs and reset Sensor
    #  @swtest_expResult The reported fault 'DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF' has status failed (bit 0, 1, 5 of the status byte)         
    # @sw_requirement{SDC-R_SW_SESM_127, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-127-00159bc1?doors.view=00000004}
    def swTest_checkStopModulationFault(self, t32_api):
    # [Stop modulation fault]
    #If sensor mode request data stored in NVM from diagnostics is start modulation and sensor mode request  received is to stop the modulation via communication interface, 
    #the software shall report the converted request with error status failed using the internal fault reporting mechanism.    
        numberFailedTests = 0
        numberTest = 1
        
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)  
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mode request from diag 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        numberTest += 1
            
        #5. Trigger the SensorMode 'stopModulation' to be sent on the bus 
        self.setSensorModeRequestInputCanoeApi(g_stopModulationSensorMode)
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)
        
        time.sleep(2) # propagation into nvm from bus
        
        #6. check status in nvm mirror of communication interface
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
        
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                g_stopModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)
        numberTest += 1
    
        #7.   result: check fault status  
        #   rbSysEvM_ReportErrorStatus_v(DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF, DEM_EVENT_STATUS_PASSED);        
        dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRadarModPermanentOFF}]")                                                 
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dem_event_value['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCyclePendingConfirmedLastClear, 
                                                 "Check Dem_AllEventsStatusByte[DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF]")  
        
        numberTest += 1

        #8. Cleanup                        
        self.cleanupSensorModeRequest()            
        
        #9.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 9: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)    
    
    
    ## @swtest_description The test case checks if the fault status 'DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF' 
    #   is set correctly if a 'startModulation' of comunication interface request is issued.
    #  @swtest_step 
    #   Preconditions:RBS is running and link is up. 
    #                 The Sensor mode request from diag interface in NVM is "start modulation".                 
    #   1. Trigger the 'startModulation' sent from diag interface   
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Clear DTC's using ClearDiagnosticInformation (0x14) Service
    #   6. Trigger the SensorMode 'startModulation' to be sent on the bus
    #   7. Verify the Nvm mirror reflects the status 'startModulation'
    #   8. Verify the fault 'DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF' has status passed (no bit is set)         
    #   9. Trigger the SensorMode 'stopModulation' to be sent on the bus, suspend for 2 second and trigger the SensorMode 'startModulation' again to be sent on the bus
    #   10. Verify the Nvm mirror reflects the status 'startModulation'        
    #   11. Check fault status
    #   12. Cleanup: Set default that modulation is enabled in NVM and no further requests are sent on the bus
    #   13.  clean up: clear DTCs and reset Sensor
    #  @swtest_expResult The reported fault 'DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF' has status passed with bits 1 and 5 of the status byte set                           
    # @sw_requirement{SDC-R_SW_SESM_128, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-128-00159bc1?doors.view=00000004}
    def swTest_checkStartModulationFault(self, t32_api):
    # [Start modulation fault]
    #If sensor mode request data stored in NVM from diagnostics is start modulation and the sensor mode request received is to start the modulation via communication interface, the software shall 
    #report the converted request with error status passed using the internal fault reporting mechanism.
        numberFailedTests = 0
        numberTest = 1
    
        #Precondition: reset sensor
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)   
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mode request from diag 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest, SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        numberTest += 1
        
          
        #5. ClearDiagnosticInformation (0x14) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, clearDtcResponse, constant.CONST_CLEAR_DTC_RESP, "Step 5: Check Clear DTC Res")
        
        numberTest += 1
        
        #6.Trigger the SensorMode 'startModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_startModulationSensorMode)
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)
        
        #7.Check status in nvm mirror of communication interface
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)
        numberTest += 1
            
        #8. Check expected result - rbSysEvM_ReportErrorStatus_v(DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF, DEM_EVENT_STATUS_PASSED);        
        dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRadarModPermanentOFF}]")
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dem_event_value['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusPassedAllBits, 
                                                 "Check Dem_AllEventsStatusByte[DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF]")            
    
        #9. Trigger the SensorMode 'stopModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_stopModulationSensorMode)    
        time.sleep(2) # number of seconds execution to be suspended
        #   Trigger the SensorMode 'startModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_startModulationSensorMode)    
        
        numberTest += 1
        
        #10. Check status in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
    
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)
    
        numberTest += 1
        
        #11.  Check expected result - rbSysEvM_ReportErrorStatus_v(DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF, DEM_EVENT_STATUS_PASSED);        
        dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRadarModPermanentOFF}]")
                               
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dem_event_value['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, 
                                                 "Check Dem_AllEventsStatusByte[DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF]") 
        
        numberTest += 1  
            
        #12.Cleanup - Stop sending SensorMode                        
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerDisable)    

        #13.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 13: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
             
        return CTestCaseResult(numberTest, numberFailedTests) 
    
    
    ## @swtest_description The test case checks if the fault status 'DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF' 
    #   is set correctly if a 'stopModulation' request from diag interface is issued.The input from communication interface is ignored 
    #  @swtest_step              
    #   1. Trigger the 'stopModulation' sent from diag interface   
    #   2. Read modulation control from diag NVM
    #   3. Check sensor mode request from diag is 'stopModulation'
    #   4. Check fault status
    #   5. Cleanup: Set default that modulation is enabled from diag interface.
    #   6.  clean up: clear DTCs and reset Sensor
    #  @swtest_expResult The reported fault 'DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF' has status failed (bit 0, 1, 5 of the status byte)         
    # @sw_requirement{SDC-R_SW_SESM_137, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-137-00159bc1?doors.view=0000000b}
    def swTest_checkStopModulationFaultfromDiagInterface(self, t32_api):
    # [Stop modulation fault]
    #If sensor mode request data stored in NVM from diagnostics is stop modulation,the software shall 
    #report the converted request with error status failed using the internal fault reporting mechanism.  
        numberFailedTests = 0
        numberTest = 1
    
        #1.Write modulation control value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_STOP_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)   
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
          
        #3.Read modulation control from diag NVM
        modulationcntrolvaluenvm      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, modulationcntrolvaluenvm, 
                                                constant.CONST_MODULATION_CNTRL_STOP_MODULATION, "Check " + k_nvmMirrorSensorModeStatusName)
        numberTest += 1
    
        #4.   result: check fault status  
        #   rbSysEvM_ReportErrorStatus_v(DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF, DEM_EVENT_STATUS_PASSED);        
        dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRadarModPermanentOFF}]")                                                 
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dem_event_value['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCyclePendingConfirmedLastClear, 
                                                 "Check Dem_AllEventsStatusByte[DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF]")            
            
        
        numberTest += 1
        
        #5.Cleanup         
        self.logger.debug("Cleanup by sending service to use the default configured modulation  control")
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)   
        time.sleep(0.5)           
        
        #6.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 6: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests) 
    
    ## @swtest_description The test case checks that the SensorMode which is stored in NvM of communication interface is used if no SensorMode request is received from communication interface.
    #  @swtest_step 
    #   Preconditions:The Sensor mode request from diag interface in NVM is "start modulation".                            
    #   1. Trigger the 'startModulation' sent from diag interface   
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Trigger the SensorMode 'startModulation' to be sent on the bus         
    #   6. Stop sending the SensorMode on the bus
    #   7. Reset both micro controller
    #   8. Verify that no SensorMode is sent
    #   9. Verify the Nvm mirror reflects the status 'startModulation'
    #   10. Trigger the SensorMode 'stopModulation' to be sent on the bus                 
    #   11. Stop sending the SensorMode on the bus               
    #   12. Reset both micro controller            
    #   13. Verify that no SensorMode is sent         
    #   14. Verify the Nvm mirror reflects the status 'stopModulation'
    #   15. Set default that modulation is enabled in NVM and no further requests are sent on the bus
    #   16.  clean up: clear DTCs and reset Sensor
    #  @swtest_expResult All test steps are executed and passed.
    # @sw_requirement{SDC-R_SW_SESM_129, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-129-00159bc1?doors.view=00000004}
    def swTest_checkNoSensorModeReceived(self, t32_api):
    # [No SensorMode received]
    #If sensor mode request data stored in NVM from diagnostics is start modulation and no sensor mode request is received via communication interface,the software shall 
    #report the converted request with the error status by reading the sensor mode request data of communication interface in NVM.          
        numberFailedTests = 0
        numberTest = 1   
        
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)   
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mode request from diag 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        
        numberTest += 1
        
        #5. Trigger the SensorMode 'startModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_startModulationSensorMode)        
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)    
        # sleep some time to make sure, SensorMode is stored in NvM
        time.sleep(2) # number of seconds execution to be suspended    
        
        #6. stop sending SensorMode            
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerDisable)
        
        #7. reset     
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(1)
        
        #8. get trigger value and verify it is disabled
        sensorModeTrigger = self.canoe_api.getSysVar("ROS_LGP_Client", "SensorModeRequest_Input", "trigger")
                          
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorModeTrigger, 
                                                g_sensorModeTriggerDisable, "Canoe getSysVar(\"ROS_LGP_Client\", \"SensorModeRequest_Input\", \"trigger\")")               
        numberTest += 1
               
        #9. check status in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)
        numberTest += 1
    
        #10. Trigger the SensorMode 'stopModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_stopModulationSensorMode)
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)    
        # sleep some time to make sure, SensorMode is stored in NvM
        time.sleep(2) # number of seconds execution to be suspended    
        
        #11. stop sending SensorMode    
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerDisable)
        
        #12. reset 
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)

        time.sleep(1)
    
        #13. get trigger value and verify it is disabled
        sensorModeTrigger = self.canoe_api.getSysVar("ROS_LGP_Client", "SensorModeRequest_Input", "trigger")
                          
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorModeTrigger, 
                                                 g_sensorModeTriggerDisable, "Canoe getSysVar(\"ROS_LGP\", \"SensorModeRequest_Input\", \"trigger\")")               
        numberTest += 1
               
        #14. check status in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
                       
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_stopModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)    
        
        #15. cleanup
        self.cleanupSensorModeRequest(True)
        
        #16.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 16: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)         
    
    
    ## @swtest_description The test case checks if all possible invalid values do do not change the sensor modulation if the SensorMode 'startModulation' was set previously from communication interface.
    #  @swtest_step 
    #   Precondition: The Sensor mode request from diag interface in NVM is "start modulation". 
    #                 Trigger the SensorMode 'startModulation' to be sent on from communication interface.
    #   1. Trigger the 'startModulation' sent from diag interface
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Trigger the invalid SensorMode with value 0 to be sent on the bus
    #   6. Verify the Nvm mirror reflects the status 'startModulation'
    #   7. Trigger the invalid SensorMode with values greater than 2 (only some representatives are chosen) to be sent on the bus        
    #   8. Cleanup: Set default that modulation is enabled in NVM and no further requests are sent on the bus
    #  @swtest_expResult For all sent invalid signal values, the nvm mirror which reflects the SensorModeRequest is not changed.
    # @sw_requirement{SDC-R_SW_SESM_130, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-130-00159bc1?doors.view=00000004}
    def swTest_checkInvalidSensorModeReceivedStartMod(self, t32_api):
    # [Invalid SensorMode]
    # If sensor mode request data stored in NVM from diagnostics is start modulation and an invalid sensor mode request is received via communication interface,the software shall report the converted 
    #request with the error status by reading the sensor mode request data of communication interface in NVM.           
        numberFailedTests = 0
        numberTest = 1
    
        """ 
        SensorMode values which are defined:
        invalid           = 0, -> invalid per definition
        startModulation   = 1,
        stopModulation    = 2,
        resumeModulation  = 3, -> are currently not used, thus invalid
        suspendModulation = 4  -> are currently not used, thus invalid
        """  
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)   
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mpde request from diag 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest, SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        
        #   Precondition: startModulation is sent on the bus
        #   Trigger SensorMode 'startModulation' to be sent on the bus            
        self.setSensorModeRequestInputCanoeApi(g_startModulationSensorMode)
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)    
    
        # check precondition sensor mode in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
           
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)            
        
        #5. Trigger an invalid SensorMode with value 0 to be sent on the bus            
        self.setSensorModeRequestInputCanoeApi(g_invalidSensorMode)
        
        #6. check status in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)

        numberTest += 1           
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)            
    
        #7. Trigger invalid sensor mode as defined in following array
        invalidSensorModes = [3, 4, 10, 120, 200, 255]
        # signal 'xRR_LGU_SenModReq_RadMod' has length 8 bits -> 255
        for i in invalidSensorModes:
            # Trigger an invalid SensorMode with value i            
            self.logger.debug(f"Sending invalid SensorMode: {i}")
            self.setSensorModeRequestInputCanoeApi(i)
        
            # check sensor mode of communication interface in nvm mirror
            nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
        
            numberTest += 1
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                     g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)                                    
    
    
        #8. Cleanup                        
        self.cleanupSensorModeRequest()            
                               
        return CTestCaseResult(numberTest, numberFailedTests)           
    
    
    ## @swtest_description The test case checks if all possible invalid values do do not change the sensor modulation if the SensorMode 'stopModulation' was set previously from communication interface.
    #  @swtest_step 
    #   Precondition:The Sensor mode request from diag interface in NVM is "start modulation". 
    #                Trigger the SensorMode 'stopModulation' to be sent on the bus.     
    #   1. Trigger the 'startModulation' sent from diag interface 
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Trigger the invalid SensorMode with value 0 to be sent on the bus
    #   6. Verify the Nvm mirror reflects the status 'stopModulation'
    #   7. Trigger the invalid SensorMode with values greater than 2 (only some representatives are chosen) to be sent on the bus
    #   8. Cleanup: Set default that modulation is enabled in NVM and no further requests are sent on the bus             
    #   9.  clean up: clear DTCs and reset Sensor
    #  @swtest_expResult For all sent invalid signal values, the nvm mirror which reflects the SensorModeRequest is not changed.    
    # @sw_requirement{SDC-R_SW_SESM_130, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-130-00159bc1?doors.view=00000004}
    def swTest_checkInvalidSensorModeReceivedStopMod(self, t32_api):
    # [Invalid SensorMode]
    # If sensor mode request data stored in NVM from diagnostics is start modulation and an invalid sensor mode request is received via communication interface,the software shall report the converted 
    #request with the error status by reading the sensor mode request data of communication interface in NVM.           
        numberFailedTests = 0
        numberTest = 1
        
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger) 
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mode request from diag 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        
        numberTest += 1 
    
        #   Precondition: stopModulation is sent on the bus
        #   Trigger SensorMode 'stopModulation' to be sent on the bus        
        self.setSensorModeRequestInputCanoeApi(g_stopModulationSensorMode)
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)        
        
        # wait until request is propagated into NVM
        time.sleep(4)
        
        # check precondition sensor mode in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
           
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                g_stopModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)    
        
        #5. Trigger an invalid SensorMode with value 0 to be sent on the bus            
        self.setSensorModeRequestInputCanoeApi(g_invalidSensorMode)
        
        #6. check status in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
        
        numberTest += 1   
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                 g_stopModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)            

        # 7. Trigger invalid sensor mode as defined in following array
        invalidSensorModes = [3, 4, 8, 91, 189, 255]           
        # signal 'xRR_LGU_SenModReq_RadMod' has length 8 bits -> 255
        for i in invalidSensorModes:
            # Trigger an invalid SensorMode with value i            
            self.logger.debug(f"Sending invalid SensorMode: {i}")
            self.setSensorModeRequestInputCanoeApi(i)
        
            # check sensor mode of communication interface in nvm mirror
            nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
            
            numberTest += 1       
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                     g_stopModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)                            
                
    
        # 8. Cleanup                
        self.cleanupSensorModeRequest()      
        
        #9.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 9: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description The test case checks if the FId-Status towards DSP is set according the SensorMode request from diag interface. 
    #  @swtest_step 
    #   1. Trigger the 'stopModulation' sent from diag interface   
    #   2. Read modulation control from diag NVM
    #   3. Check sensor mode request from diag is 'stopModulation'
    #   4.Check Fid status       
    #   5. Cleanup: Set default that modulation is enabled from diag interface.     
    #   6.  clean up: clear DTCs and reset Sensor
    #  @swtest_expResult The FId-Status which is sent towards DSP, has the FId-Status 0.
    # @sw_requirement{SDC-R_SW_SESM_131, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-131-00159bc1?doors.view=00000004}
    def swTest_checkDisableModulationfromDiagInterface(self, t32_api):
    # [Disable modulation DSP]
    # The software shall use the DSP interface to disable the modulation of the sensor, if the converted request was reported as failed in the current execution cycle.
        numberFailedTests = 0
        numberTest = 1

        #1.Write modulation control value using write service         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_STOP_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
          
        #3.Read modulation control from NVM
        modulationcntrolvaluenvm      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, modulationcntrolvaluenvm, 
                                                constant.CONST_MODULATION_CNTRL_STOP_MODULATION, "Check " + k_nvmMirrorSensorModeStatusName)
        numberTest += 1
    
        #4  result. check rbSysEvM mempool for the Fid to Dsp      
        dspFidStatus = t32_api.get_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable_m_dspFidStates_out_local.m_arrayPool[4].elem.m_radarModulationOff_u8")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFidStatus['vvalue'].value, 
                                                 rbSysEvmConstant.g_fimPermissionDenied, "Check mempool for dspFidStates")
    
        #5.Cleanup         
        self.logger.debug("Cleanup by sending service to use the default configured modulation  control")
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(0.5)            
        
        #6.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 6: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests) 
    
    ## @swtest_description The test case checks if the FId-Status towards DSP is set according the SensorMode request on the bus. 
    #  @swtest_step 
    #   Precondition:The Sensor mode request from diag interface in NVM is "start modulation". 
    #   1. Trigger the 'startModulation' sent from diag interface   
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Trigger the SensorMode 'stopModulation' to be sent on the bus
    #   6. Verify the Nvm mirror reflects the status 'stopModulation'
    #   7.Check Fid status
    #   8. Cleanup: Set default that modulation is enabled in NVM and no further requests are sent on the bus    
    #   9.  clean up: clear DTCs and reset Sensor            
    #  @swtest_expResult The FId-Status which is sent towards DSP, has the FId-Status 0.
    # @sw_requirement{SDC-R_SW_SESM_131, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-131-00159bc1?doors.view=00000004}
    def swTest_checkDisableModulationOnInterface(self, t32_api):
    # [Disable modulation DSP]
    # The software shall use the DSP interface to disable the modulation of the sensor, if the converted request was reported as failed in the current execution cycle.
        numberFailedTests = 0
        numberTest = 1
        
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mpde request from daig 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        
        numberTest += 1
    
        #5. Trigger the SensorMode 'stopModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_stopModulationSensorMode)   
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)     
                          
        #6. check sensor mode in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
        
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                g_stopModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)
        numberTest += 1
    
        #7.result. check rbSysEvM mempool for the Fid to Dsp      
        dspFidStatus = t32_api.get_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable_m_dspFidStates_out_local.m_arrayPool[4].elem.m_radarModulationOff_u8")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFidStatus['vvalue'].value, 
                                                 rbSysEvmConstant.g_fimPermissionDenied, "Check mempool for dspFidStates")
        
        numberTest += 1
    
        #8. Cleanup                
        self.cleanupSensorModeRequest()         
        
        #9.  clean up: clear DTCs and reset Sensor
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, diagbasic.k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 9: Clear DTC response: {clearDtcResponse}")
    
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
                    
        return CTestCaseResult(numberTest, numberFailedTests)     
    
    
    ## @swtest_description The test case checks if the FId-Status towards DSP is set according the SensorMode request on the bus.
    #  @swtest_step 
    #   Precondition:The Sensor mode request from diag interface in NVM is "start modulation".
    #   1. Trigger the 'startModulation' sent from diag interface   
    #   2. Validate write response -> positive response
    #   3. Read modulation control from diag NVM
    #   4. Check sensor mode request from diag is 'startModulation'
    #   5. Trigger the SensorMode 'startModulation' to be sent on the bus
    #   6. Verify the Nvm mirror reflects the status 'startModulation'    
    #   7.Check Fid status     
    #   8. Cleanup: Set default that modulation is enabled in NVM and no further requests are sent on the bus             
    #  @swtest_expResult The FId-Status which is sent towards DSP, has the FId-Status 1.
    # @sw_requirement{SDC-R_SW_SESM_132, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-132-00159bc1?doors.view=00000004}
    def swTest_checkEnableModulationOnInterface(self, t32_api):
    # [Enable modulation DSP]
    # The software shall use the DSP interface to enable the modulation of the sensor, if the converted request was reported as passed in the current execution cycle.
        numberFailedTests = 0
        numberTest = 1
    
        #1.Configure 'startmodulation' for sensor mode request from diag interface         
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_DIAG_SESSION_CNTRL_BOSCH_SESSION_REQ, self.logger)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api,constant.CONST_WRITE_DID_REQ_START_MODULATION, self.logger)
        writeModulationResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger) 
        time.sleep(0.5) 
        
        #2. Validate write response -> positive response
        writeResponseStatus = writeModulationResponse[0:6]
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, writeResponseStatus,
                                                 constant.CONST_WRITE_DID_RES_MODULATION_CNTRL, "Check WDBI Modulation - response")
        
        numberTest += 1
        
        #3.Read modulation control from diag NVM
        SensorModefromdiag      = format(t32_api.get_variable_value("g_NvMRamMirrorModulationControlDiagNVMData[4]")['vvalue'].value,'02x')
        
        #4.Check sensor mode request from daig 
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test,numberTest, SensorModefromdiag, constant.CONST_MODULATION_CNTRL_START_MODULATION,
                                                 "Check Sensor mode request from diag interface")
        
        numberTest += 1
        
        #5. Trigger the SensorMode 'startModulation' to be sent on the bus
        self.setSensorModeRequestInputCanoeApi(g_startModulationSensorMode)
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerEnable)            
                      
        #6. check sensor mode in nvm mirror
        nvmMirrorValue = t32_api.get_variable_value(k_nvmMirrorSensorModeStatusName)
        
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, nvmMirrorValue['vvalue'].value, 
                                                g_startModulationSensorMode, "Check " + k_nvmMirrorSensorModeStatusName)
        numberTest += 1
        
        #7.result. check rbSysEvM mempool for the Fid to Dsp
        dspFidStatus = t32_api.get_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable_m_dspFidStates_out_local.m_arrayPool[4].elem.m_radarModulationOff_u8")
                                
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFidStatus['vvalue'].value, 
                                                 rbSysEvmConstant.g_fimPermissionGranted, "Check mempool for dspFidStates")        
    
        #8.Cleanup - Stop sending SensorMode                
        self.setSensorModeRequestTriggerCanoeApi(g_sensorModeTriggerDisable)            
            
        return CTestCaseResult(numberTest, numberFailedTests)
                       
    
    ## @swtest_description This test case checks if the DSP fault mapping to the DEM fault events is working properly. 
    #  @swtest_step 
    #    1. Activate 'ShadowCopy' in DSP-Interface
    #    1.1 Check first if it is not already enabled
    #    1.2 Enable 'ShadowCopy' and check that it is enabled
    #    2. For every DSP fault:
    #    2.1 Set DSP fault in 'ShadowCopy' as 'prefailed'
    #    2.2 Some time until fault is propagated into DEM
    #    2.3 Check that the corresponding DEM fault event status of the DSP fault reflects the status set in the 'ShadowCopy'
    #    3. Deactivate 'ShadowCopy' and clean up (reset sensor)     
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_SESM_82, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-82-00159bc1?doors.view=00000004}    
    def swTest_checkDspDemFaultMapping(self, t32_api):
        numberFailedTests = 0
    
    #   1. Activate 'ShadowCopy' in DSP-Interface
        dspFaultActivation = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        
        numberTest = 1    
        # 1.1 Check DspFaultActivation is not enabled
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivation['vvalue'].value, 
                                                 0, "Check rbDsp::DspFaultEventsTestActivation not enabled")
            
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", rbSysEvmConstant.g_dspFaultEventsTestActivation, 0)
    
        time.sleep(1) # number of seconds execution to be suspended
    
        # 1.2 Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        numberTest += 1
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivationSet['vvalue'].value, 
                                                 rbSysEvmConstant.g_dspFaultEventsTestActivation, 
                                                 "Check rbDsp::DspFaultEventsTestActivation is enabled")    
                      
    #   2. Test Faults in DSP-ShadowCopy   
        demEventMapInfo = t32_api.get_variable_info("sysEvm::k_dspFaultEventDemIdMap")    
        demEventMapDspFaultSize = int(demEventMapInfo['vsize'].value / 4)
    
        self.logger.debug(f"DemEventMap - DspFaultEventSize: {demEventMapDspFaultSize}")
    
        # skip first two dsp faults as they are InternalAsserts and not reported to DEM
        for i in range(2, demEventMapDspFaultSize):
            dspFaultEventId = t32_api.get_variable_value(f"sysEvm::k_dspFaultEventDemIdMap[{i}].m_dspFaultEventId")
            dspFaultEventIdVValue = dspFaultEventId['vvalue'].value
            demEventId = t32_api.get_variable_value(f"sysEvm::k_dspFaultEventDemIdMap[{i}].m_demEventId")
            demEventIdVValue = demEventId['vvalue'].value
            # Set Fault in DSP-ShadowCopy        
            t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{dspFaultEventIdVValue}]", 
                                       rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
            
            # Wait until fault is propagated into DEM
            # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable
            time.sleep(0.36)
    
            self.logger.debug(f"Comparing status of rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{dspFaultEventIdVValue}] with Dem_AllEventsStatusByte[{demEventIdVValue}]...")
            # Check status in Dem_AllEventsStatusByte
            demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{demEventIdVValue}]")
    
            numberTest += 1
            numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, 
                                                     rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
    
    #   3. Clean up - deactivate 'ShadowCopy'
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", 0, 0)
               
        # reset Sensor that all irreversible faults are cleared
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
            
        return CTestCaseResult(numberTest, numberFailedTests)     


    ## @swtest_description This test case check the reporting mechanism for internal faults and the configuration of different parameter. For that 3 different faults are taken out of different configuration classes.
    #  @swtest_step 
    #    1. Activate DEM Test sequence
    #    2. Inject faultEventIdCycleTimeExceeded as 'prefailed'  
    #    3. Wait 20ms until the fault is propagated into DEM and the fault is debounced
    #    4. Inject faultEventIdMmicOvertempState as 'prefailed'
    #    5. Wait 20ms until the fault is propagated into DEM and the fault is debounced
    #    6. Check status in Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded to be still passed and faultEventIdMmicOvertempState to be already failed
    #    7. Inject faultEventIdCycleTimeExceeded as 'prefailed' for another 300ms    
    #    8. Inject faultEventIdMmicTxLowPowErr as 'prefailed'    
    #    9. Wait 300ms until the faults are propagated into DEM and debounced        
    #    10. Check status in Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded, faultEventIdMmicOvertempState and faultEventIdMmicTxLowPowErr to be failed    
    #    11. Set faultEventIdCycleTimeExceeded to 'prepassed' for 400ms    
    #    12. Set faultEventIdMmicOvertempState to  'prepassed' for 700ms    
    #    13. Set faultEventIdMmicTxLowPowErr to  'prepassed' for 300ms    
    #    14. Check status in Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded, faultEventIdMmicTxLowPowErr to be still failed and faultEventIdMmicOvertempState already passed
    #    15. Set faultEventIdCycleTimeExceeded to 'prepassed' for another 700ms to make sure the fault get healed
    #    16. Check status in Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded and faultEventIdMmicOvertempState are already passed and faultEventIdMmicTxLowPowErr is still failed as the fault is irreversible 
    #    17. Clean up and reset sensor
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_SESM_60, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-60-00159bc1?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_SESM_63, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-63-00159bc1?doors.view=00000005}    
    def swTest_faultReportingConfiguration(self, t32_api):
    # [Fault Reporting] and [Fault configuration]
        numberFailedTests = 0
        numberTest = 1
    
        testPassedComb = (rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleLastClear, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, rbSysEvmConstant.g_demEventStatusPassedFailedThisCyclePendingDTCLastClear, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleConfirmedDTCLastClear)

        # 1. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", 
                                   rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, 
                                                 rbSysEvmConstant.k_demTestActicationSequence, "Step 1: Check DEM Test Sequence activation")
        numberTest += 1                              
        
        # 2. inject self.faultEventIdCycleTimeExceeded mapped to DSP class F:
        # preFail Debounce (number of prefailed for failed) 5
        # prePass Debounce (number of prepassed for passed) 10
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdCycleTimeExceeded, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)

        # 3. Wait until fault is propagated into DEM and debounce
        time.sleep(0.02)

        # 4. inject self.faultEventIdMmicOvertempState mapped to DSP class A:
        # preFail Debounce (number of prefailed for failed) 1
        # prePass Debounce (number of prepassed for passed) 6
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdMmicOvertempState, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
        
        # 5. Wait until fault is propagated into DEM and debounce
        time.sleep(0.1)                 

        # 6. Check current fault event status
        demStatusCycleTimeExceeded = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdCycleTimeExceeded}]")            
        demStatusMmicOvertemp = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdMmicOvertempState}]")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demStatusCycleTimeExceeded['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusPassedAllBits, 
                                                 "Step 6: Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded")
        numberTest += 1        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatusMmicOvertemp['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle, 
                                                 "Step 6: Dem_AllEventsStatusByte for faultEventIdMmicOvertempState")
        numberTest += 1                 

        # 7. inject self.faultEventIdCycleTimeExceeded mapped to DSP class F:
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdCycleTimeExceeded, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)

        # Wait until fault is propagated into DEM and debounce
        time.sleep(0.3)

        # 8. inject self.faultEventIdMmicTxLowPowErr mapped to DSP class D (irreversible):
        # preFail Debounce (number of prefailed for failed) 2
        # prePass Debounce (number of prepassed for passed) 1 (but not relevant)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdMmicTxLowPowErr, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
                 
        # 9. Wait until fault is propagated into DEM and debounce
        time.sleep(0.3)                 

        # 10. Check current fault event status
        demStatusCycleTimeExceeded = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdCycleTimeExceeded}]")    
        demStatusMmicOvertemp = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdMmicOvertempState}]")
        demStatusMmicTxLowPow = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdMmicTxLowPowErr}]")
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatusCycleTimeExceeded['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle, 
                                                 "Step 10: Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded")
        numberTest += 1
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatusMmicOvertemp['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle, 
                                                 "Step 10: Dem_AllEventsStatusByte for faultEventIdMmicOvertempState")
        numberTest += 1
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatusMmicTxLowPow['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle, 
                                                 "Step 10: Dem_AllEventsStatusByte for faultEventIdMmicTxLowPowErr")
        numberTest += 1                 

        # 11. Try to heal fault
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdCycleTimeExceeded, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPrePassed, 0)

        # Wait until fault is propagated into DEM and debounce
        time.sleep(0.4)

        # 12. Try to heal fault
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdMmicOvertempState, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPrePassed, 0)        

        # Wait until fault is propagated into DEM and debounce
        time.sleep(0.7)
        
        # 13. Try to heal fault
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdMmicTxLowPowErr, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPrePassed, 0)

        # Wait until healing is propagated into DEM and debounced
        time.sleep(0.3)
                 
        # 14. Check current fault event status
        demStatusCycleTimeExceeded = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdCycleTimeExceeded}]")    
        demStatusMmicOvertemp = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdMmicOvertempState}]")
        demStatusMmicTxLowPow = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdMmicTxLowPowErr}]")
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatusCycleTimeExceeded['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle, 
                                                 "Step 14: Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded")
        numberTest += 1        
        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, demStatusMmicOvertemp['vvalue'].value, 
                                                       testPassedComb, "Step 14: Dem_AllEventsStatusByte for faultEventIdMmicOvertempState")
        numberTest += 1
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatusMmicTxLowPow['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle, "Step 14: Dem_AllEventsStatusByte for faultEventIdMmicTxLowPowErr")
        numberTest += 1        
        
        # 15. set to prepassed 
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdCycleTimeExceeded, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        
        # Wait until healing is propagated into DEM and debounced
        time.sleep(0.7)

        # 16.  Check current fault event status
        demStatusCycleTimeExceeded = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdCycleTimeExceeded}]")    
        demStatusMmicOvertemp = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdMmicOvertempState}]")
        demStatusMmicTxLowPow = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdMmicTxLowPowErr}]")
        
        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, demStatusCycleTimeExceeded['vvalue'].value, 
                                                       testPassedComb, "Step 16: Dem_AllEventsStatusByte for faultEventIdCycleTimeExceeded")
        numberTest += 1
        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, demStatusMmicOvertemp['vvalue'].value, 
                                                       testPassedComb, "Step 16: Dem_AllEventsStatusByte for faultEventIdMmicOvertempState")
        numberTest += 1
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatusMmicTxLowPow['vvalue'].value, 
                                                 rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle, 
                                                 "Step 16: Dem_AllEventsStatusByte for faultEventIdMmicTxLowPowErr")
               
        # 17. reset Sensor that all irreversible faults are cleared
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
            
        return CTestCaseResult(numberTest, numberFailedTests) 


    ## @swtest_description This test case checks that a mechanism is given to aggregate internal faults (DEM fault events) to customer visible summaries (DTCs). For that,
    #    different fault event Ids are triggered and checked if only the mapped DTCs are stored.
    #  @swtest_step
    #    1. Precondition: Jump to default session and clear all stored DTCs
    #    2. Check that no DTCs are stored
    #    3. Activate DEM Test sequence
    #    4. Trigger faults which are mapped to DTC_UC_OVER_VOLTAGE DTC
    #    5. Check that in the status byte of the triggered faults, the bits for DTC pending or DTC confirmed are set for RB_UC_PMSPRI_V3_OV
    #    and not set for RB_UC_PMS_StandbySupply_OV and RB_UC_PMSSEC_VCore_OV
    #    6. Check that the DTC DTC_UC_OVER_VOLTAGE is set
    #    7. Trigger faults which are mapped to DTC_UC_TEMP_FAILURE DTC    
    #    8. Check that in the status byte of the triggered faults, the bits for DTC pending or DTC confirmed are set for RB_UC_ADC_TEMPPLAUS_Failure
    #    and not set for RB_UC_TEMP_DEFECT
    #    9. Check that the DTCs DTC_UC_OVER_VOLTAGE and DTC_UC_TEMP_FAILURE are set
    #    10. Clear all DTC and reset the sensor 
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_SESM_62, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-62-00159bc1?doors.view=00000005}    
    def swTest_checkFaultAggregation(self, t32_api):
    # [Fault aggregation] The software shall provide a mechanism that allows aggregation of internal faults to customer visible summaries.
        numberFailedTests = 0
        numberTest = 1
    
        dtcTestFailedStatusBit = 0x1
        dtcPendingStatusBit = 0x4
        dtcConfirmedStatusBit = 0x8
        dtcTestFailedPendingConfirmedStatusBit = 0xD
        
        dtcStatusComb = (dtcTestFailedStatusBit, dtcPendingStatusBit, dtcConfirmedStatusBit, dtcTestFailedPendingConfirmedStatusBit)
        
        dtcTestFailedPendingConfirmedStatusMask = 0xD
        testFailedFailedThisCycleMask = 0xF
        
        testFailedStatusBit = 0x1
        testFailedThisCycleStatusBit = 0x2
        testFailedFailedThisCycleBite = 0x3
        testFailedComb = (testFailedStatusBit, testFailedThisCycleStatusBit, testFailedFailedThisCycleBite)

        # Used FaultEventId to DTC mapping in this test
        # DTC_UC_OVER_VOLTAGE - 14028311
        # FR5CU: RB_UC_PMSPRI_V3_OV, RB_UC_PMS_StandbySupply_OV, RB_UC_PMSSEC_VCore_OV
        
        # DTC_UC_TEMP_FAILURE - 14028388
        # FR5CU: RB_UC_ADC_TEMPPLAUS_Failure, RB_UC_TEMP_DEFECT

        # 1. jump to default session and clear DTCs
        canoeDiagPanel.jumpToDefaultSession(self.canoe_api, self.logger)
        # ClearDiagnosticInformation (0x14) Service
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 1: Clear DTC response: {clearDtcResponse}")
        
        # 2. make sure no other DTCs are present
        # Retrieving the list of DTCs that match a client defined status mask (sub-function = 0x02 reportDTCByStatusMask)
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcInformationRequest + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 2: Read DTC response: {dtcList}")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, 
                                                 k_diagReadDtcInformationPositiveResponse + k_diagReadDtcInformationStatus, 
                                                 "Step 2: Check no DTC stored")
        numberTest += 1

        #  3. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", 
                                   rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, 
                                                 rbSysEvmConstant.k_demTestActicationSequence, "Step 3: Check DEM Test Sequence activation")
        numberTest += 1                                    
           
        # 4. trigger faults which are mapped to DTC_UC_OVER_VOLTAGE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdRbUcPMSPRIV3Ov, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)        
        time.sleep(0.5) # propagation and debounce
        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdRbUcPmsStandbySupplyOv, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)                        
        time.sleep(0.5) # propagation and debounce
        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdRbUcPmssecVCoreOv, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
        time.sleep(0.5) # propagation and debounce       
           
        # 5. check status byte: DTC pending or confirmed for first fault 
        demStatusRbUcPMSPRIV3Ov = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRbUcPMSPRIV3Ov}]")    
        demStatusRbUcPmsStandbySupplyOv = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRbUcPmsStandbySupplyOv}]")
        demStatusRbUcPmssecVCoreOv = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRbUcPmssecVCoreOv}]")

        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, 
                                                       demStatusRbUcPMSPRIV3Ov['vvalue'].value & dtcTestFailedPendingConfirmedStatusMask, 
                                                       dtcStatusComb, "Step 5: Dem_AllEventsStatusByte for RbUcPMSPRIV3Ov")
        numberTest += 1
        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, 
                                                       demStatusRbUcPmsStandbySupplyOv['vvalue'].value & testFailedFailedThisCycleMask, 
                                                       testFailedComb, "Step 5: Dem_AllEventsStatusByte for RbUcPmsStandbySupplyOv")
        numberTest += 1
        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, 
                                                       demStatusRbUcPmssecVCoreOv['vvalue'].value & testFailedFailedThisCycleMask, 
                                                       testFailedComb, "Step 5: Dem_AllEventsStatusByte for RbUcPmssecVCoreOv")
        numberTest += 1
           
        # 6. check stored DTC for DTC_UC_OVER_VOLTAGE
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcInformationRequest + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, k_ucOverVoltageDtcResponse, 
                                                 "Step 6: DTC match for DTC_UC_OVER_VOLTAGE")
        numberTest += 1               

        # 7. trigger faults which are mapped to DTC_UC_TEMP_FAILURE
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdRbUcAdcTempplausFailure, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)        
        time.sleep(0.5) # propagation and debounce
        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", 
                                   self.faultEventIdRbUcTempDefect, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", 
                                   rbSysEvmConstant.g_demFaultStatusPreFailed, 0)                        
        time.sleep(0.5) # propagation and debounce

        # 8. check status byte: DTC pending or confirmed
        demStatusRbUcAdcTempplausFailure = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRbUcAdcTempplausFailure}]")    
        demStatusRbUcTempDefect = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.faultEventIdRbUcTempDefect}]")

        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, 
                                                       demStatusRbUcAdcTempplausFailure['vvalue'].value & dtcTestFailedPendingConfirmedStatusMask, 
                                                       dtcStatusComb, "Step 8: Dem_AllEventsStatusByte for RbUcAdcTempplausFailure")
        numberTest += 1
        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, 
                                                       demStatusRbUcTempDefect['vvalue'].value & testFailedFailedThisCycleMask, 
                                                       testFailedComb, "Step 8: Dem_AllEventsStatusByte for RbUcTempDefect")
        numberTest += 1
           
        # 9. check stored DTC for DTC_UC_TEMP_FAILURE
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagReadDtcInformationRequest + k_diagReadDtcInformationStatus, self.logger)
        dtcList = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")        

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dtcList, 
                                                 k_ucOverVoltageUcTempFailureDtcResponse, "Step 9: DTC match for DTC_UC_TEMP_FAILURE")                    
        
        # 10. clean up: clear DTCs and reset Sensor 
        canoeDiagPanel.sendSpecificDiagService(self.canoe_api, k_diagClearAllDtcRequest, self.logger)
        clearDtcResponse = self.canoe_api.getEnvVar("Env_DoipDirectReceive_AutoIP")
        self.logger.debug(f"Step 10: Clear DTC response: {clearDtcResponse}")
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)
    