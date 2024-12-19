# -*- coding: utf-8 -*-

import sys
import time
import os

sys.path.append(os.path.abspath('../../framework/helper'))
sys.path.append(os.path.abspath('../../framework/scheduling'))
sys.path.append(os.path.abspath('../../framework/interface'))
sys.path.append(os.path.abspath('../rbSysEvM'))

import atf_toolbox as testHelper
import atf_testasserts as testasserts
import AD_lauterbach_test_helper as lauterbachTestHelper
import rbSysEvM_testsuiteconstants as rbSysEvmConstant
import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants
from testbase import CTestCaseResult

# SensorStates
g_oosTemporaryL4pfswFailure = 51  # This sensor state indicates temporary failure reported for L4 software resulting in disabling of Radar modulation
g_oosPersistentRadarMmicFailure = 101 #This sensor state indicates persistent failure reported for Radar Mmic resulting in disabling of Radar modulation
g_inSpecificationSensorState = 1 # This sensor state indicates that there are no active failures in the system
g_TemporaryRadarMmicMismatch  =  54 #This sensor state indicates temporary failure reported for Radar Mmic resulting in disabling of Radar function
g_TemporaryRadarMismatch = 63 # This sensor state indicates temporary failure reported from multiple Radar failure categories resulting in disabling of Radar function
g_TemporaryFailure = 68 # This sensor state indicates temporary failure reported from multiple failure components resulting in disabling of Radar modulation
g_PersistentRadarFailure =108 #This sensor state indicates persistent failure reported from multiple Radar failure categories resulting in disabling of Radar modulation


class CTestSuiteSdm(testsuite.CTestSuite, CTestRunner):

    def __init__(self, logger_api, canoe_api, t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteSdm"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, self.getComponentName())
        
        # FR5CU fault values, have to be adapted on DEM configuration changes 
        #DemConf_DemEventParameter_RB_Radar_Mod_Permanent_OFF = 204
        self.demRbRadarModPermanentOff = 204  
        #  enErmMstMmic2MissingFactorydata = 114   
        self.dspFaultIdRbMstMmic5MissingFactoryData = 114
        # DemConf_DemEventParameter_RB_MST_MMIC5_MISSING_FACTORYDATA            148u  
        self.demFaultIdRbMstMmic5MissingFactoryData = 148
        #DemConf_DemEventParameter_RB_UC_MCU_CONFIG                    371u
        self.demFaultId_RB_UC_MCU_CONFIG = 371             
        #DemConf_DemEventParameter_RB_UC_SAFE_STATE_Failure           433u
        self.demFaultId_RB_UC_SAFE_STATE_Failure = 433
        #enErmMstMmic0SnrErr 97u
        self.dspFaultId_RB_MST_MMIC1_SNR_ER = 97
        #define DemConf_DemEventParameter_RB_MST_MMIC1_SNR_ERR               111u
        self.demFaultId_RB_MST_MMIC1_SNR_ER = 111
        #enErmSlvDspInputRangeErr = 202
        self.dspFaultId_RB_SLV_DSP_INPUT_RANGE_ERR = 202
        #DemConf_DemEventParameter_RB_SLV_DSP_INPUT_RANGE_ERR         207u  
        self.demFaultId_RB_SLV_DSP_INPUT_RANGE_ERR = 207
        #enErmSlvMmic1RxcorfrqErr 51u
        self.dspFaultId_RB_SLV_MMIC4_RXCORFRQ_ERR = 51
        #DemConf_DemEventParameter_RB_SLV_MMIC4_RXCORFRQ_ERR          251u
        self.demFaultId_RB_SLV_MMIC4_RXCORFRQ_ERR = 251
        #enErmSlvRif0HwRegister 166u
        self.dspFaultId_RB_SLV_RIF0_HW_REGISTER = 166
        #DemConf_DemEventParameter_RB_SLV_RIF0_HW_REGISTER            270u
        self.demFaultId_RB_SLV_RIF0_HW_REGISTER = 270 
        #enErmSlvSpuExecTime 183u
        self.dspFaultId_RB_SLV_SPU_EXEC_TIME = 183
        #DemConf_DemEventParameter_RB_SLV_SPU_EXEC_TIME               289u
        self.demFaultId_RB_SLV_SPU_EXEC_TIME = 289

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # There are no sdm test cases on UC1
        pass

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        return self.runAllSdmTests(self.t32_api[globalConstants.k_atf_hardwareLrrUc2])

    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "sdm"


    def runAllSdmTests(self, t32_api):                                                
        numberFailedTests = self.executeFilteredFunction(t32_api)                      
                            
        return testsuite.TestSuiteResult(self.number_of_test, numberFailedTests) 
   
    
    def printAllFailedFaultEvents(self, t32_api):
        self.logger.debug("DEBUG - Printing all DEM FaultEvents")
        
        demInfo = t32_api.get_variable_info("Dem_AllEventsStatusByte")    
        self.logger.debug(f"Dem_AllEventsStatusByte array size: {demInfo['vsize'].value}")
       
        for i in range(demInfo['vsize'].value):                                   
            dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{i}]")            
            compare = dem_event_value['vvalue'].value & rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle

            if compare > 0:                        
                self.logger.debug(f"\tFAILED Dem_AllEventsStatusByte[{i}] with status: {dem_event_value['vvalue'].value}")                    
    
    
    
    ## @swtest_description This test case checks that the implemented state machine state "in specification" is executed if no fault is active.  
    #  @swtest_step
    #    1. Check that no FaultEventId is set in DEM (TestFailed and TestFailedThisOperationCycle bits are checked).
    #    2. Check that the current state of the state machine is the state "in specification". 
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_SESM_142, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-142-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_144, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-144-00159bc1?doors.view=00000004}       
    def swTest_checkInSpecState(self, t32_api):
    # [InSpec state] 
    # The software shall implement a "in specification" state which is managed by the state machine to indicate the sensor is 
    # executed in its specification and no fault is active.        
        numberFailedTests = 0
        numberTest = 1                               
        
        # 1. check that there is no fault set in Dem_AllEventsStatusByte                                
        demInfo = t32_api.get_variable_info("Dem_AllEventsStatusByte")    
        self.logger.debug(f"Dem_AllEventsStatusByte array size: {demInfo['vsize'].value}")

        demFaultFound = False
       
        for i in range(demInfo['vsize'].value):                                   
            dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{i}]")
            compare = dem_event_value['vvalue'].value & rbSysEvmConstant.g_demEventStatusFailedFailedTest

            if compare > 0:
                # at least there is one DEM fault
                demFaultFound = True
                self.logger.debug(f"Dem_AllEventsStatusByte[{i}] failed with status: {dem_event_value['vvalue'].value}")
                break

                
        numberFailedTests = testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demFaultFound, False, "FaultId stored in Dem_AllEventsStatusByte")               
        numberTest += 1            
                        
        # 2. check state machine state															
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")                                 
                    
        return CTestCaseResult(numberTest, numberFailedTests)  
    
    
    ## @swtest_description This test case checks if the sensor state "inSpecification" is sent out on the bus, if the state machine state is "in specification". 
    #  @swtest_step
    #    1. Check that the current state of the state machine is the state "in specification".
    #    2. Check that the sensor state "inSpecification" is sent out on the bus
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_SESM_144,  https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-144-00159bc1?doors.view=00000004}      
    def swTest_checkSendInSpec(self, t32_api):
    # The software shall send out the sensor state "in specification" as a sensor reaction only in the "in specification“ 
    # state managed by the state machine.
    
        numberFailedTests = 0
        numberTest = 1
                                                   
        # 1.check state machine state 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1
    
        # 2. check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_inSpecificationSensorState, "Check sensor state on bus")
                    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    ## @swtest_description This test case checks if the sensor state "Temporary Software Application Failure" is sent out on the bus, if the state machine state is in "state temporary". 
    #  @swtest_step
    #    1. Activate DEM test sequence 
    #    2. Inject fault which failure type is temporary,category and component is from software application 
    #    3. Check status in Dem_AllEventsStatusByte
    #    4. Check that the current state of the state machine is the state "state Temporary".
    #    5. Check that the sensor state "Temporary Software Application Failure" is sent out on the bus
    #    6. Heal the fault triggered in step 2. and check if the fault is "passed" in DEM
    #    7. Check that the current state of the state machine is the state "in specification".
    #    8. Check that the sensor state "inSpecification" is sent out on the bus
    #  @swtest_expResult All test steps are executed and passed. 
    #  @sw_requirement{SDC-R_SW_SESM_142, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-142-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_147, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-147-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_154, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-154-00159bc1?doors.view=00000004}
    def swTest_checkSendTemporaryState(self, t32_api):
    # The software shall send out the sensor state "Temporary Software Application Failure" as a sensor reaction only in the "TemporaryState“ managed by the state machine.
    
        numberFailedTests = 0
        numberTest = 1
                                           
        # 1. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Check DEM Test Sequence activation")
        numberTest += 1

        # 2. Inject fault which leads to temporary state                                      
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)
        
        # 3. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
                                  
        # 4. Check state machine state 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        temporaryStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStateTemporary")     
        temporarystateAddress = temporaryStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, temporarystateAddress, "Check state machine state: current - temporarystate")
        numberTest += 1       
        
        # 5. Check SensorState 'Temporary Software Application Failure' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_oosTemporaryL4pfswFailure, "Check sensor state on bus - temporarystate")
        numberTest += 1
        
        # 6. Heal the fault triggered in step 2
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)        
        
        # Wait until fault is propagated into DEM
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 7. Check state machine state 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1
    
        # 8. Check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_inSpecificationSensorState, "Check sensor state on bus")

        return CTestCaseResult(numberTest, numberFailedTests)
    
    ## @swtest_description This test case checks if the sensor states "Temporary Radar Mismatch" and "Temporary Failure" is sent out on the bus, if the state machine state is in "temporary state". 
      #  @swtest_step
      #    1.  Activate 'ShadowCopy' in DSP-Interface
      #    1.1 Check first if it is not already enabled
      #    1.2 Enable 'ShadowCopy' and check that it is enabled
      #    2.  Inject a  DSP-Fault which failure type is temporary,category is RadarExec and component from radar
      #    2.1 Inject a  DSP-Fault which failure type is temporary,category is RadarMmic and component from radar
      #    3   Check status of 2  in Dem_AllEventsStatusByte
      #   3.1 Check status of 2.1  in Dem_AllEventsStatusByte
      #    4.  Check that the current state of the state machine is the state "temporary".
      #    5.  Check SensorState 'Temporary Radar Mismatch' is sent on bus
      #    6. Activate DEM test sequence 
      #    7. Inject fault which failure type is temporary,category and component is from software application 
      #    8. Check status of 7 in Dem_AllEventsStatusByte
      #    9. Check that the current state of the state machine is the state "state Temporary".
      #    10. Check that the sensor state "Temporary Software Application Failure" is sent out on the bus
      #    11. Heal the fault triggered in step 2. and check if the fault is "passed" in DEM
      #    12. Heal the fault triggered in step 2.1 and check if the fault is "passed" in DEM
      #    13. Heal the fault triggered in step 7. and check if the fault is "passed" in DEM
      #    14. Check that the current state of the state machine is the state "in specification".
      #    15. Check that the sensor state "inSpecification" is sent out on the bus
      #    16. Clean up and deactivate 'ShadowCopy'
      #  @swtest_expResult All test steps are executed and passed. 
      #  @sw_requirement{SDC-R_SW_SESM_142, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-142-00159bc1?doors.view=00000004}
      #  @sw_requirement{SDC-R_SW_SESM_147, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-147-00159bc1?doors.view=00000004}
      #  @sw_requirement{SDC-R_SW_SESM_154, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-154-00159bc1?doors.view=00000004}
    def swTest_sendTemporaryStateTriggerfaultfromDifferentCategoryandcomponent(self, t32_api):
    # The software shall send out the sensor states "Temporary Radar Mismatch" and "Temporary Failure" as a sensor reaction only in the "TemporaryState“ managed by the state machine.
    
        numberFailedTests = 0
        numberTest = 1

        #   1. Activate 'ShadowCopy' in DSP-Interface
        dspFaultActivation = t32_api.get_variable_value(
            "rbDsp::DspFaultEventsTestActivation")

        # 1.1 Check DspFaultActivation is not enabled
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 dspFaultActivation['vvalue'].value, 0, "Check rbDsp::DspFaultEventsTestActivation not enabled")
        numberTest += 1

        t32_api.set_variable_value(
            "rbDsp::DspFaultEventsTestActivation", rbSysEvmConstant.g_dspFaultEventsTestActivation, 0)

        time.sleep(1)  # number of seconds execution to be suspended

        # 1.2 Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value(
            "rbDsp::DspFaultEventsTestActivation")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 dspFaultActivationSet['vvalue'].value, rbSysEvmConstant.g_dspFaultEventsTestActivation, "Check rbDsp::DspFaultEventsTestActivation is enabled")
        numberTest += 1

        # 2. Inject a  DSP-Fault which failure type is temporary,category is RadarExec and component from radar
        t32_api.set_variable_value(
            f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_DSP_INPUT_RANGE_ERR}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
        
        # 2.1 Inject a  DSP-Fault which failure type is temporary,category is RadarMmic and component from radar
        t32_api.set_variable_value(
            f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_MMIC4_RXCORFRQ_ERR}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)

        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.72)
        
        # 3. Check status of 2  in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_DSP_INPUT_RANGE_ERR}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte RB_SLV_DSP_INPUT_RANGE_ERR")
        numberTest += 1 
        
        # 3.1 Check status of 2.1 in Dem_AllEventsStatusByte
        demStatus1 = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_MMIC4_RXCORFRQ_ERR}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus1['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte RB_SLV_MMIC4_RXCORFRQ_ERR")
        numberTest += 1 

        # 4. check state machine state
        currentStateAddress = t32_api.get_variable_value(
            "scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")
        temporaryStateInfo = t32_api.get_variable_info(
            "scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStateTemporary")
        temporarystateAddress = temporaryStateInfo['vaddr'].value

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 currentStateAddress['vvalue'].value, temporarystateAddress, "Check state machine state: current - temporarystate")
        numberTest += 1

        # 5. check SensorState 'Temporary Radar Mismatch' is sent on bus
        sensorState = self.canoe_api.getSysVar(
            "ROS_LGP_Client", "SensorStateInfo_Output", "SenStInfo_SenSt")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 sensorState, g_TemporaryRadarMismatch, "Check sensor state on bus - temporarystate")
        numberTest += 1

        # 6. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Check DEM Test Sequence activation")
        numberTest += 1

        # 7. Inject fault which failure type is temporary,category and component is from software application                             
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)
        
        # 8. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 9. check state machine state
        currentStateAddress = t32_api.get_variable_value(
            "scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")
        temporaryStateInfo = t32_api.get_variable_info(
            "scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStateTemporary")
        temporarystateAddress = temporaryStateInfo['vaddr'].value

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 currentStateAddress['vvalue'].value, temporarystateAddress, "Check state machine state: current - temporarystate")
        numberTest += 1

        # 10. check SensorState 'Temporary Failure' is sent on bus
        sensorState = self.canoe_api.getSysVar(
            "ROS_LGP_Client", "SensorStateInfo_Output", "SenStInfo_SenSt")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 sensorState, g_TemporaryFailure, "Check sensor state on bus - temporarystate")
        numberTest += 1

        # 11. Heal the fault triggered in step 2
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_DSP_INPUT_RANGE_ERR}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        
        # Wait until fault is propagated into DEM
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_DSP_INPUT_RANGE_ERR}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1 

        # 12. Heal the fault triggered in step 2.1
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_MMIC4_RXCORFRQ_ERR}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        
        # Wait until fault is propagated into DEM
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus1 = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_MMIC4_RXCORFRQ_ERR}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus1['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1 

        #13. Heal the fault triggered in step 7
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)        
       
        # Wait until fault is propagated into DEM
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  

        # 14. check state machine state
        currentStateAddress = t32_api.get_variable_value(
            "scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")
        inSpecStateInfo = t32_api.get_variable_info(
            "scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")
        inSpecStateAddress = inSpecStateInfo['vaddr'].value

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1

        # 15. check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar(
            "ROS_LGP_Client", "SensorStateInfo_Output", "SenStInfo_SenSt")

        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest,
                                                 sensorState, g_inSpecificationSensorState, "Check sensor state on bus")

        #16. Clean up - deactivate 'ShadowCopy'
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", 0, 0)

        return CTestCaseResult(numberTest, numberFailedTests)

    ## @swtest_description This test case checks if the sensor state "Persistent Radar MMIC Failure" is sent out on the bus, if the state machine state is in "persistent state". 
    #  @swtest_step
    #    1.  Activate 'ShadowCopy' in DSP-Interface
    #    1.1 Check first if it is not already enabled
    #    1.2 Enable 'ShadowCopy' and check that it is enabled
    #    2.  Inject a  DSP-Fault which failure type is persistent ,category is RadarMmic and component from radar
    #    3   Check status of 2  in Dem_AllEventsStatusByte
    #    4.  Check that the current state of the state machine is the state "persistent".
    #    5.  Check SensorState 'Persistent Radar MMIC Failure' is sent on bus       
    #    6.  Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state
    #    7.  Heal the fault triggered in step 2. and check if the fault is "passed" in DEM
    #    8.  Check that the current state of the state machine is the state "in specification".
    #    9.  Check that the sensor state "inSpecification" is sent out on the bus
    #    10. Clean up and deactivate 'ShadowCopy'
    #  @swtest_expResult All test steps are executed and passed.    
    #  @sw_requirement{SDC-R_SW_SESM_142, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-142-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_146, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-146-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_154, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-154-00159bc1?doors.view=00000004}
    def swTest_checkPersistentstate(self, t32_api):
    # The software shall send out the sensor state "Persistent Radar MMIC Failure" and "Temporary Failure" as a sensor reaction only in the "PersistentState“ managed by the state machine.
    
        numberFailedTests = 0
        numberTest = 1
                        
           
        #   1. Activate 'ShadowCopy' in DSP-Interface
        dspFaultActivation = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        
        # 1.1 Check DspFaultActivation is not enabled
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivation['vvalue'].value, 0, "Check rbDsp::DspFaultEventsTestActivation not enabled")
        numberTest += 1
            
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", rbSysEvmConstant.g_dspFaultEventsTestActivation, 0)
    
        time.sleep(1) # number of seconds execution to be suspended
    
        # 1.2 Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivationSet['vvalue'].value, rbSysEvmConstant.g_dspFaultEventsTestActivation, "Check rbDsp::DspFaultEventsTestActivation is enabled")
        numberTest += 1                                                                    
         
        # 2. Inject Fault in DSP-ShadowCopy              
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultIdRbMstMmic5MissingFactoryData}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
               
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.36)
        
        # 3. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultIdRbMstMmic5MissingFactoryData}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 4. Check that the current state of the state machine is the state "persistent".
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        persistentStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStatePersistent")     
        persistentStateAddress = persistentStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, persistentStateAddress, "Check state machine state: current - persistentstate")
        numberTest += 1 
        
        # 5. Check SensorState 'Persistent Radar MMIC Failure' is sent on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_oosPersistentRadarMmicFailure, "Check sensor state on bus - persistent")
        numberTest += 1
        
        # 6. Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state 
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
       
        # 7. Heal the fault triggered in step 2
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultIdRbMstMmic5MissingFactoryData}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultIdRbMstMmic5MissingFactoryData}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 8. check state machine state 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1
    
        # 9. check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_inSpecificationSensorState, "Check sensor state on bus")
                
        # 10. Clean up - deactivate 'ShadowCopy'
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", 0, 0)  
         
        return CTestCaseResult(numberTest, numberFailedTests)   
    
    ## @swtest_description This test case checks if the sensor state "Persistent Radar Failure" is sent out on the bus, if the state machine state is in "persistent state". 
    #  @swtest_step
    #    1.  Activate 'ShadowCopy' in DSP-Interface
    #    1.1 Check first if it is not already enabled
    #    1.2 Enable 'ShadowCopy' and check that it is enabled
    #    2.  Inject Fault in DSP-ShadowCopy which failuretype is persistent ,category is RadarRif and component from Radar
    #    2.1 Inject Fault in DSP-ShadowCopy which failuretype is persistent ,category is RadarSpu and component from Radar 
    #    3   Check status of 2  in Dem_AllEventsStatusByte
    #    3.1 Check status of 2.1  in Dem_AllEventsStatusByte
    #    4.  Check that the current state of the state machine is the state "persistent".    
    #    5.  Check SensorState 'Persistent Radar Failure' is sent on bus
    #    6.  Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state 
    #    7.  Heal the fault triggered in step 2. and check if the fault is "passed" in DEM
    #    7.1 Heal the fault triggered in step 2.1 and check if the fault is "passed" in DEM
    #    8.  Check that the current state of the state machine is the state "in specification".
    #    9.  Check that the sensor state "inSpecification" is sent out on the bus
    #    10. Clean up and deactivate 'ShadowCopy'
    #  @swtest_expResult All test steps are executed and passed.    
    #  @sw_requirement{SDC-R_SW_SESM_142, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-142-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_146, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-146-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_154, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-154-00159bc1?doors.view=00000004}
    def swTest_sendPersistentstateTriggerfromMultiplecategory(self, t32_api):
    # The software shall send out the sensor state "Persistent Radar Failure" and "Temporary Failure" as a sensor reaction only in the "PersistentState“ managed by the state machine.
    
        numberFailedTests = 0
        numberTest = 1
                        
        #1. Activate 'ShadowCopy' in DSP-Interface
        dspFaultActivation = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        
        # 1.1 Check DspFaultActivation is not enabled
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivation['vvalue'].value, 0, "Check rbDsp::DspFaultEventsTestActivation not enabled")
        numberTest += 1
            
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", rbSysEvmConstant.g_dspFaultEventsTestActivation, 0)
    
        time.sleep(1) # number of seconds execution to be suspended
    
        # 1.2 Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivationSet['vvalue'].value, rbSysEvmConstant.g_dspFaultEventsTestActivation, "Check rbDsp::DspFaultEventsTestActivation is enabled")
        numberTest += 1                                                                    
         
        # 2. Inject Fault in DSP-ShadowCopy which failuretype is persistent ,category is RadarRif and component from Radar             
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_RIF0_HW_REGISTER}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
        
        # 2.1 Inject Fault in DSP-ShadowCopy which failuretype is persistent ,category is RadarSpu and component from Radar               
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_SPU_EXEC_TIME}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
            
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.72)
        
        # 3. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_RIF0_HW_REGISTER}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 3.1 Check status in Dem_AllEventsStatusByte
        demStatus1 = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_SPU_EXEC_TIME}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus1['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1 
        
        # 4. Check that the current state of the state machine is the state "persistent".
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        persistentStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStatePersistent")     
        persistentStateAddress = persistentStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, persistentStateAddress, "Check state machine state: current - persistentstate")
        numberTest += 1 
        
        # 5. Check SensorState 'Persistent Radar Failure' is sent on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_PersistentRadarFailure, "Check sensor state on bus - persistent")
        numberTest += 1
        
        # 6. Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state 
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)

        # 7. Heal the fault triggered in step 2
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_RIF0_HW_REGISTER}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_RIF0_HW_REGISTER}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 7.1 Heal the fault triggered in step 2.1
        #t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_RIF0_HW_REGISTER}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_SLV_SPU_EXEC_TIME}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_SLV_SPU_EXEC_TIME}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 8. check state machine state 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1
    
        # 9. check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_inSpecificationSensorState, "Check sensor state on bus")
                
        # 10. Clean up - deactivate 'ShadowCopy'
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", 0, 0)  
                
        return CTestCaseResult(numberTest, numberFailedTests)   

    ## @swtest_description This test case checks the state transition from 'inSpecification' state to  state 'temporary' based on the triggered fault which is temporary in nature.  
    #  @swtest_step
    #    1. Check current state to be 'inSpecification' 
    #    2. Activate DEM test sequence 
    #    3. Inject fault which failure type is temporary,category and component is from software application 
    #    4. Check status in Dem_AllEventsStatusByte
    #    5. Check that the current state of the state machine is the state "state Temporary".
    #    6. Check that the sensor state "Temporary Software Application Failure" is sent out on the bus
    #    7. Heal the fault triggered in step 2. and check if the fault is "passed" in DEM
    #    8. Check that the current state of the state machine is the state "in specification".
    #    9. Check that the sensor state "inSpecification" is sent out on the bus
    #  @swtest_expResult All test steps are executed and passed. 
    #  @sw_requirement{SDC-R_SW_SESM_144, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-144-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_147, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-147-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_150, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-150-00159bc1?doors.view=00000004}
    def swTest_stateTransitionInspecTemporaryState(self, t32_api): 
        numberFailedTests = 0
        numberTest = 1
                                              
        # sleep some time to make sure, the sensor is in "InSpecification" state
        time.sleep(1) 
    
        # 1. Check current state to be 'inSpecification' 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - inSpecification")
        numberTest += 1
         
         # 2. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Check DEM Test Sequence activation")
        numberTest += 1

        # 3. Inject fault which failure type is temporary,category and component is from software application                                      
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)
        
        # 4. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 5. Check that the current state of the state machine is the state "state Temporary". 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        temporaryStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStateTemporary")     
        temporarystateAddress = temporaryStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, temporarystateAddress, "Check state machine state: current - temporarystate")
        numberTest += 1       
        
        # 6. Check that the sensor state "Temporary Software Application Failure" is sent out on the bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_oosTemporaryL4pfswFailure, "Check sensor state on bus - temporarystate")
        numberTest += 1
        
        # 7. Heal the fault triggered in step 2. and check if the fault is "passed" in DEM
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)        
        #t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.demRbRadarModPermanentOff}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        
        # Wait until fault is propagated into DEM
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 8. Check that the current state of the state machine is the state "in specification"
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1
    
        # 9. check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_inSpecificationSensorState, "Check sensor state on bus")
        
        return CTestCaseResult(numberTest, numberFailedTests)     

    ## @swtest_description This test case checks the transition into "Persistent" from "inSpecification" of the state machine. 
    #  @swtest_step
    #    1.  Check current state to be 'inSpecification' 
    #    2.  Activate 'ShadowCopy' in DSP-Interface
    #    2.1 Check first if it is not already enabled
    #    2.2 Enable 'ShadowCopy' and check that it is enabled
    #    3.  Inject a  DSP-Fault which failure type is persistent ,category is RadarMmic and component from radar
    #    4.  Check status of 3  in Dem_AllEventsStatusByte
    #    5.  Check that the current state of the state machine is the state "persistent".
    #    6.  Check SensorState 'Persistent Radar MMIC Failure' is sent on bus       
    #    7.  Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state
    #    8.  Heal the fault triggered in step 3. and check if the fault is "passed" in DEM
    #    9.  Check that the current state of the state machine is the state "in specification".
    #    10. Check that the sensor state "inSpecification" is sent out on the bus
    #    11. Clean up and deactivate 'ShadowCopy'
    #  @swtest_expResult All test steps are executed and passed.    
    #  @sw_requirement{SDC-R_SW_SESM_144, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-144-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_146, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-146-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_150, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-150-00159bc1?doors.view=00000004}
    def swTest_stateTransitionInspecPersistentstate(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        # sleep some time to make sure, the sensor is in "InSpecification" state
        time.sleep(1) 
    
        # 1. Check current state to be 'inSpecification' 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - inSpecification")
        numberTest += 1
                              
        # 2. Activate 'ShadowCopy' in DSP-Interface
        dspFaultActivation = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        
        #2.1 Check DspFaultActivation is not enabled
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivation['vvalue'].value, 0, "Check rbDsp::DspFaultEventsTestActivation not enabled")
        numberTest += 1
            
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", rbSysEvmConstant.g_dspFaultEventsTestActivation, 0)
    
        time.sleep(1) # number of seconds execution to be suspended
    
        # 2.2 Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivationSet['vvalue'].value, rbSysEvmConstant.g_dspFaultEventsTestActivation, "Check rbDsp::DspFaultEventsTestActivation is enabled")
        numberTest += 1                                                                    
         
        # 3. Inject a  DSP-Fault which failure type is persistent ,category is RadarMmic and component from radar             
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultIdRbMstMmic5MissingFactoryData}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
                 
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.36)
        
        # 4. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultIdRbMstMmic5MissingFactoryData}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 5. Check that the current state of the state machine is the state "persistent"
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        persistentStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStatePersistent")     
        persistentStateAddress = persistentStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, persistentStateAddress, "Check state machine state: current - persistentstate")
        numberTest += 1 
        
        # 6. Check SensorState 'Persistent Radar MMIC Failure' is sent on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_oosPersistentRadarMmicFailure, "Check sensor state on bus - persistent")
        numberTest += 1
        
        #7. Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
    
        # 8. Heal the fault triggered in step 3. and check if the fault is "passed" in DEM
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultIdRbMstMmic5MissingFactoryData}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultIdRbMstMmic5MissingFactoryData}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 9. check state machine state 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1
    
        # 10. check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_inSpecificationSensorState, "Check sensor state on bus")
                
        # 11. Clean up - deactivate 'ShadowCopy'
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", 0, 0)  
        
        # 6. clean up and reset sensor
       # lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)   
    
    ## @swtest_description This test case checks the transition into "Persistent" from "temporary" of the state machine. 
    #  @swtest_step
    #    1.  Check current state to be 'inSpecification' 
    #    2.  Activate 'ShadowCopy' in DSP-Interface
    #    2.1 Check first if it is not already enabled
    #    2.2 Enable 'ShadowCopy' and check that it is enabled
    #    3.  Inject Fault in DSP-ShadowCopy which failuretype is temporary ,category is RadarMmic and component from Radar
    #    4.  Check status of fault triggered in step 3  in Dem_AllEventsStatusByte
    #    5.  Check that the current state of the state machine is the state "temporary".  
    #    6.  Check SensorState 'Temporary Radar MMIC Mismatch' is sent on bus
    #    7.  Check 'ShadowCopy'  that it is enabled
    #    8.  Inject a  DSP-Fault which failure type is persistent ,category is RadarMmic and component from radar
    #    9.  Check status of fault triggered in step 8  in Dem_AllEventsStatusByte
    #    10. Check that the current state of the state machine is the state "persistent".
    #    11. Check SensorState 'Persistent Radar MMIC Failure' is sent on bus       
    #    12. Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state
    #    13. Heal the fault triggered in step 3. and check if the fault is "passed" in DEM
    #    14. Heal the fault triggered in step 8. and check if the fault is "passed" in DEM
    #    15. Check that the current state of the state machine is the state "in specification".
    #    16. Check that the sensor state "inSpecification" is sent out on the bus
    #    17. Clean up and deactivate 'ShadowCopy'
    #  @swtest_expResult All test steps are executed and passed. 
    #  @sw_requirement{SDC-R_SW_SESM_146, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-146-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_150, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-150-00159bc1?doors.view=00000004} 
    #  @sw_requirement{SDC-R_SW_SESM_147, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-147-00159bc1?doors.view=00000004}      
    def swTest_stateTransitionTemporaryPersistentState(self, t32_api): 
        numberFailedTests = 0
        numberTest = 1
                                              
        # sleep some time to make sure, the sensor is in "InSpecification" state
        time.sleep(1) 
    
        # 1. Check current state to be 'inSpecification' 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - inSpecification")
        numberTest += 1
         
        # 2. Activate 'ShadowCopy' in DSP-Interface
        dspFaultActivation = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        
        # 2.1 Check DspFaultActivation is not enabled
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivation['vvalue'].value, 0, "Check rbDsp::DspFaultEventsTestActivation not enabled")
        numberTest += 1
            
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", rbSysEvmConstant.g_dspFaultEventsTestActivation, 0)
    
        time.sleep(1) # number of seconds execution to be suspended
    
        # 2.2 Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivationSet['vvalue'].value, rbSysEvmConstant.g_dspFaultEventsTestActivation, "Check rbDsp::DspFaultEventsTestActivation is enabled")
        numberTest += 1                                                                    
         
        # 3. Inject Fault in DSP-ShadowCopy which failuretype is temporary ,category is RadarMmic and component from Radar          
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultId_RB_MST_MMIC1_SNR_ER}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
            
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.36)
        
        # 4. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_MST_MMIC1_SNR_ER}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
                                     
        # 5.  Check that the current state of the state machine is the state "temporary".
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        temporaryStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStateTemporary")     
        temporarystateAddress = temporaryStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, temporarystateAddress, "Check state machine state: current - temporarystate")
        numberTest += 1       
        
        # 6. check SensorState 'Temporary Radar MMIC Mismatch' is sent on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_TemporaryRadarMmicMismatch, "Check sensor state on bus - temporarystate")
        numberTest += 1
        
        time.sleep(1) # number of seconds execution to be suspended
    
        # 7. Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivationSet['vvalue'].value, rbSysEvmConstant.g_dspFaultEventsTestActivation, "Check rbDsp::DspFaultEventsTestActivation is enabled")
        numberTest += 1                                                                    
         
        # 8. Inject a  DSP-Fault which failure type is persistent ,category is RadarMmic and component from radar          
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultIdRbMstMmic5MissingFactoryData}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)
        
        # 9. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultIdRbMstMmic5MissingFactoryData}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 10. Check that the current state of the state machine is the state "persistent".
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        persistentStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStatePersistent")     
        persistentStateAddress = persistentStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, persistentStateAddress, "Check state machine state: current - persistentstate")
        numberTest += 1 
        
        # 11. Check SensorState 'Persistent Radar MMIC Failure' is sent on bus   
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_oosPersistentRadarMmicFailure, "Check sensor state on bus - persistent")
        numberTest += 1
        
        # 12. Reset sensor as persistent fault will active in complete ignition cycle,reset the sensor to revert to inspec state
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        #13. Heal the fault triggered in step 3. and check if the fault is "passed" in DEM
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusPassed, 0)  
        
        #14. Heal the fault triggered in step 8. and check if the fault is "passed" in DEM
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultIdRbMstMmic5MissingFactoryData}]", rbSysEvmConstant.g_demFaultStatusPrePassed, 0)
       
        # Wait until fault is propagated into DEM
        # At least one fault has debounce of 5 DSP cycles -> 5x66 ->  330 ms + some buffer rbSysEvM runnable + sdm
        time.sleep(0.5)
        
        # Check status in Dem_AllEventsStatusByte of 
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")
        
        # Check status in Dem_AllEventsStatusByte
        demStatus1 = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultIdRbMstMmic5MissingFactoryData}]")
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte for temporaryfault")
        numberTest += 1  
        
        numberFailedTests += testasserts.TEST_LE(self.logger, self.number_of_test, numberTest, demStatus1['vvalue'].value, rbSysEvmConstant.g_demEventStatusPassedFailedThisCycleDTCLastClear, "Check Dem_AllEventsStatusByte for temporaryfault")
        numberTest += 1  
        
        # 15. check state machine state 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - in spec")
        numberTest += 1
    
        # 16. check SensorState 'inSpecification' on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_inSpecificationSensorState, "Check sensor state on bus")
        
        # 17. Clean up - deactivate 'ShadowCopy'
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", 0, 0)        
                    
        return CTestCaseResult(numberTest, numberFailedTests)     

    ## @swtest_description This test case checks the state transition from 'inSpecification' state to safe state 'failedSilent' based on the triggered fault.
    #  @swtest_step
    #    1. Check that the current state of the state machine is the state 'inSpecification'.    
    #    2. Activate DEM Test sequence. 
    #    3. Inject fault which triggered failed silent. 
    #    4. Check status in Dem_AllEventsStatusByte.
    #    5. Clean up and reset the sensor.        
    #  @swtest_expResult All test steps are executed and passed.
    #  @sw_requirement{SDC-R_SW_SESM_144, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-144-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_173, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-173-00159bc1?doors.view=00000004}
    def swTest_stateTransitionInSpecSilent(self, t32_api):   
    # in spec - triggered reaction class which lead to - safe state failed silent      
    
        numberFailedTests = 0
        numberTest = 1
                               
        # 1. Check current state to be 'inSpecification' 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - inSpecification")
        numberTest += 1

        # 2. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Check DEM Test Sequence activation")
        numberTest += 1

        # 3. Inject fault which leads to failedSilent                                      
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demFaultId_RB_UC_MCU_CONFIG, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)   
        
        # 4. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_UC_MCU_CONFIG}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        
        # 5. clean up and reset sensor
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
                    
        return CTestCaseResult(numberTest, numberFailedTests)    
    
    ## @swtest_description This test case checks the state transition from 'temporary' state to safe state 'failedSilent' based on the triggered fault.
    #  @swtest_step
    #    1. Check current state to be 'inSpecification' 
    #    2. Activate DEM test sequence 
    #    3. Inject fault which failure type is temporary,category and component is from software application 
    #    4. Check status in Dem_AllEventsStatusByte
    #    5. Check that the current state of the state machine is the state "state Temporary".
    #    6. Check that the sensor state "Temporary Software Application Failure" is sent out on the bus
    #    6. Check that the current state of the state machine is the state "in specification".
    #    7. Inject fault which triggered failed silent. 
    #    8. Check status in Dem_AllEventsStatusByte.
    #    9. Clean up and reset the sensor.  
    #  @swtest_expResult All test steps are executed and passed. 
    #  @sw_requirement{SDC-R_SW_SESM_147, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-147-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_173, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-173-00159bc1?doors.view=00000004}      
    def swTest_stateTransitionTemporarySilentState(self, t32_api): 
        numberFailedTests = 0
        numberTest = 1
                                              
        # sleep some time to make sure, the sensor is in "InSpecification" state
        time.sleep(1) 
    
        # 1. Check current state to be 'inSpecification' 
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        inSpecStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_inSpecState")     
        inSpecStateAddress = inSpecStateInfo['vaddr'].value
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, inSpecStateAddress, "Check state machine state: current - inSpecification")
        numberTest += 1
         
        # 2. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Check DEM Test Sequence activation")
        numberTest += 1

        # 3. Inject fault which failure type is temporary,category and component is from software application                                
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demRbRadarModPermanentOff, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)
        
        # 4. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demRbRadarModPermanentOff}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  

        # 5. Check that the current state of the state machine is the state "state Temporary".
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        temporaryStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStateTemporary")     
        temporarystateAddress = temporaryStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, temporarystateAddress, "Check state machine state: current - temporarystate")
        numberTest += 1       
        
        # 6. Check that the sensor state "Temporary Software Application Failure" is sent out on the bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_oosTemporaryL4pfswFailure, "Check sensor state on bus - temporarystate")
        numberTest += 1
        
        # 7. Inject fault which leads to failedSilent                                      
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demFaultId_RB_UC_MCU_CONFIG, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)  
        
        # 8. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_UC_MCU_CONFIG}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
                
        #9. Clean up and reset the sensor
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
                    
        return CTestCaseResult(numberTest, numberFailedTests)     
    
    
    ## @swtest_description This test case checks the transition into "Persistent" from "inSpecification" of the state machine. 
    #  @swtest_step
    #    1.  Activate DEM Test sequence 
    #    2.  Activate 'ShadowCopy' in DSP-Interface
    #    2.1 Check first if it is not already enabled
    #    2.2 Enable 'ShadowCopy' and check that it is enabled
    #    3.  Inject a  DSP-Fault which failure type is persistent ,category is RadarMmic and component from radar
    #    4.  Check status of fault triggered in step 3  in Dem_AllEventsStatusByte
    #    5.  Check that the current state of the state machine is the state "persistent".
    #    6.  Check SensorState 'Persistent Radar MMIC Failure' is sent on bus 
    #    7.  Inject fault which triggered failed silent. 
    #    8.  Check status in Dem_AllEventsStatusByte. 
    #    9.  Clean up - deactivate 'ShadowCopy'.          
    #    10. Clean up and reset the sensor.
    #  @swtest_expResult All test steps are executed and passed.    
    #  @sw_requirement{SDC-R_SW_SESM_146, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-146-00159bc1?doors.view=00000004}
    #  @sw_requirement{SDC-R_SW_SESM_173, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-173-00159bc1?doors.view=00000004}
    def swTest_stateTransitionPersistentSilentState(self, t32_api):
        numberFailedTests = 0
        numberTest = 1
                        
        # 1. Activate DEM test sequence        
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation", rbSysEvmConstant.k_demTestActicationSequence, 0)                
        demTestFaultActivation = t32_api.get_variable_value_unsigned("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestActivation")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, demTestFaultActivation['vvalue'].value, rbSysEvmConstant.k_demTestActicationSequence, "Check DEM Test Sequence activation")
        numberTest += 1
        
        # 2. Activate 'ShadowCopy' in DSP-Interface
        dspFaultActivation = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        
        # 2.1 Check DspFaultActivation is not enabled
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivation['vvalue'].value, 0, "Check rbDsp::DspFaultEventsTestActivation not enabled")
        numberTest += 1
            
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", rbSysEvmConstant.g_dspFaultEventsTestActivation, 0)
    
        time.sleep(1) # number of seconds execution to be suspended
    
        # 2.2 Check DspFaultActivation is enabled
        dspFaultActivationSet = t32_api.get_variable_value("rbDsp::DspFaultEventsTestActivation")
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dspFaultActivationSet['vvalue'].value, rbSysEvmConstant.g_dspFaultEventsTestActivation, "Check rbDsp::DspFaultEventsTestActivation is enabled")
        numberTest += 1                                                                    
         
        # 3. Inject a  DSP-Fault which failure type is persistent ,category is RadarMmic and component from radar            
        t32_api.set_variable_value(f"rbDsp::DspFaultEventsTestShadowCopy.m_faultEvent[{self.dspFaultIdRbMstMmic5MissingFactoryData}]", rbSysEvmConstant.g_demFaultStatusPreFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)
        
        # 4. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultIdRbMstMmic5MissingFactoryData}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        numberTest += 1  
        
        # 5. Check that the current state of the state machine is the state "persistent"
        currentStateAddress = t32_api.get_variable_value("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.sdm::CTopState::sdm::CStateBase::m_currState_p")        
        persistentStateInfo = t32_api.get_variable_info("scom::g_ad_radar_apl_component_sdm_x_CSdmRunnable.m_stateMachine.m_outOfSpecStatePersistent")     
        persistentStateAddress = persistentStateInfo['vaddr'].value
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, currentStateAddress['vvalue'].value, persistentStateAddress, "Check state machine state: current - persistentstate")
        numberTest += 1 
        
        # 6. Check SensorState 'Persistent Radar MMIC Failure' is sent on bus
        sensorState = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SenSt")        
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, sensorState, g_oosPersistentRadarMmicFailure, "Check sensor state on bus - persistent")
        numberTest += 1
        
        # 7. Inject fault which leads to failedSilent                                      
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventId", self.demFaultId_RB_UC_SAFE_STATE_Failure, 0)
        t32_api.set_variable_value("scom::g_ad_radar_apl_component_rbSysEvM_x_SysEvMRunnable.m_demAdapter.m_demTestEventStatus", rbSysEvmConstant.g_demFaultStatusFailed, 0)
        
        # Wait until fault is propagated into DEM
        # Some debounce + some buffer rbSysEvM runnable and sdm runnable
        time.sleep(0.3)  
        
        # 8. Check status in Dem_AllEventsStatusByte
        demStatus = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{self.demFaultId_RB_UC_SAFE_STATE_Failure}]")    
        
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, demStatus['vvalue'].value, rbSysEvmConstant.g_demEventStatusFailedFailedThisCycleLastClear, "Check Dem_AllEventsStatusByte")
        
        # 9. Clean up - deactivate 'ShadowCopy'
        t32_api.set_variable_value("rbDsp::DspFaultEventsTestActivation", 0, 0)  
        
        # 10. Clean up and reset the sensor
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        return CTestCaseResult(numberTest, numberFailedTests)   
