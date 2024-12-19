# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.abspath('../../framework/helper'))
sys.path.append(os.path.abspath('../../framework/scheduling'))
sys.path.append(os.path.abspath('../../framework/interface'))
sys.path.append(os.path.abspath('../rbSysEvM'))

import time
import pandas as pd
import AD_lauterbach_test_helper as lauterbachTestHelper
import atf_toolbox as testHelper
import atf_testasserts as testasserts
import testsuite
from testrunner import CTestRunner
import atf_globalconstants as globalConstants
import rbSysEvM_testsuiteconstants as rbSysEvmConstant
from testbase import CTestCaseResult

k_locationNumberGtZeroMin = 5
k_locationNumberDifferenceMin = 3
k_expectedDspOperationMode = 20
k_locationNumberSamplingAmount = 100

g_currentFr5CuUcVariant = globalConstants.k_atf_hardwareLrrUc2

class CTestSuiteInt(testsuite.CTestSuite, CTestRunner):
    
    def __init__(self, logger_api, canoe_api , t32_api, relay_api, hw, globalTestcaseFilter):
        super().__init__(logger_api.get_logger("CTestSuiteInt"), canoe_api , t32_api, relay_api, hw, globalTestcaseFilter, self.getComponentName())

    def printAllFailedFaultEvents(self, t32_api):
        self.logger.debug("DEBUG - Printing all FAILED DEM FaultEvents")
        
        demInfo = t32_api.get_variable_info("Dem_AllEventsStatusByte")    
        self.logger.debug(f"Dem_AllEventsStatusByte array size: {demInfo['vsize'].value}")
       
        for i in range(demInfo['vsize'].value):                                   
            dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{i}]")            
            compare = dem_event_value['vvalue'].value & rbSysEvmConstant.g_demEventStatusFailedFailedThisCycle

            if compare > 0:                        
                self.logger.debug(f"\tFAILED Dem_AllEventsStatusByte[{i}] with status: {dem_event_value['vvalue'].value}")


    def check_dsp_error_table(self, t32_api) :        
        numberFailedTests = 0
        numberTest = 1
    
        dsp_error_table_info = t32_api.get_variable_info("rbDsp::DspErrorTable")
        
        self.logger.info(f"RQM ID : {self.rqm.loc['DspErrorTable','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['DspErrorTable','LINK']}")
        
        array_size = int(dsp_error_table_info['vsize'].value/16)
        
        self.logger.debug(f"DspErrorTable array size: {array_size}")
        
        for i in range(array_size):                                    
            dsp_error_value = t32_api.get_variable_value(f"rbDsp::DspErrorTable[{i}].errorFlag")
            
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, dsp_error_value['vvalue'].value, 0, 
                                                       f"Check DspErrorTable[{i}] errorFlag")
                                
            if (array_size > numberTest):
                numberTest += 1
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    def check_dsp_opmode(self, t32_api) :        
        numberFailedTests = 0
        numberTest = 1
        
        opmode_info = t32_api.get_variable_value(f"rbDsp::FepMainDataPacket_st.OpMode")
    
        self.logger.info(f"RQM ID : {self.rqm.loc['OpMode','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['OpMode','LINK']}")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, opmode_info['vvalue'].value, k_expectedDspOperationMode, 
                                                       "Check OpMode in rbDsp::FepMainDataPacket_st.OpMode")
                    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    def check_dsp_spu_status(self, t32_api) :
        numberFailedTests = 0
        numberTest = 1
        
        spu_status_info = t32_api.get_variable_value(f"rbDsp::DspMeasurementData.SpuStatus.Status")
    
        self.logger.info(f"RQM ID : {self.rqm.loc['SPU Status','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['SPU Status','LINK']}")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, spu_status_info['vvalue'].value, 0,
                                                   "Check dsp SpuStatus")    
    
        return CTestCaseResult(numberTest, numberFailedTests)

    
    def check_daddy_error_information(self, t32_api):    
        numberFailedTests = 0
        numberTest = 1
    
        Daddy_ErrorInformation_info = t32_api.get_variable_info("Daddy_ErrorInformation ")
        
        self.logger.info(f"RQM ID : {self.rqm.loc['Daddy Errors','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['Daddy Errors','LINK']}")
        
        array_size = int(Daddy_ErrorInformation_info['vsize'].value/16)
        
        self.logger.debug(f"Daddy_ErrorInformation array size: {array_size}")
        
        for i in range(array_size):
            Daddy_ErrorInformation_value = t32_api.get_variable_value(f"Daddy_ErrorInformation[{i}]")
            
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, Daddy_ErrorInformation_value['vvalue'].value, 
                                                       0, f"Check Daddy_ErrorInformation[{i}]")                        
            
            if (array_size > numberTest):
                numberTest += 1
    
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    def check_dem_events(self, t32_api):     
        numberFailedTests = 0
        numberTest = 1
    
        dem_info = t32_api.get_variable_info("Dem_AllEventsStatusByte")
    
        self.logger.info(f"RQM ID : {self.rqm.loc['DEM Events','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['DEM Events','LINK']}")
        
        self.logger.debug(f"Dem_AllEventsStatusByte array size: {dem_info['vsize'].value}")
    
        for i in range(dem_info['vsize'].value):
            dem_event_value = t32_api.get_variable_value(f"Dem_AllEventsStatusByte[{i}]")
            compare = dem_event_value['vvalue'].value & 0b00100011
            
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, compare, 0, 
                                                       f"Check Dem_AllEventsStatusByte[{i}]")
                    
            if (dem_info['vsize'].value > numberTest):
                numberTest += 1
    
        return CTestCaseResult(numberTest, numberFailedTests)

        
    # test case is currently disabled. Check ATR-13950 for further details.      
    def check_locations(self, t32_api):
        numberFailedTests = 0
        numberTest = 1        
        
        self.logger.info(f"RQM ID : {self.rqm.loc['Basic Canoe Tests','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['Basic Canoe Tests','LINK']}")
             
        locationNumberArray = []
        locationDataTimestampSecArray = []
        locationDataTimestampNsArray = []
        locationNumberDspMempool0Array = []
        locationNumberDspMempool1Array = []
        locationNumberDspMempool2Array = []
        locationNumberDspMempool3Array = []
        locationNumberDspMempool4Array = []
        locationNumDspArray = []
                        
        # sample some location numbers and stored them in an array
        for i in range(k_locationNumberSamplingAmount):
            locations = self.canoe_api.getSysVar("ROS_LGP_Client","Loc_Data", "xRR_LGU_LocData_NoLoc")               
            locationNumberArray.append(locations)

            # -------------------- Debugging information used for ATR-13950 ----            
            nsTimestamp = self.canoe_api.getSysVar("ROS_LGP_Client","Loc_Data", "xRR_LGU_LocData_TimeStns")
            locationDataTimestampNsArray.append(nsTimestamp)
            
            secTimestamp = self.canoe_api.getSysVar("ROS_LGP_Client","Loc_Data", "xRR_LGU_LocData_TimeSts")
            locationDataTimestampSecArray.append(secTimestamp)
                                            
            hw = list(self.t32_api.keys())
            if hw[0] == globalConstants.k_atf_hardwareLrrUc2 or hw[0] == globalConstants.k_atf_hardwareLrrUc1:
                # fr5cu variant
                if g_currentFr5CuUcVariant == globalConstants.k_atf_hardwareLrrUc2:                 
                    locNumMempool0 = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[0].elem.m_LocationList.NumLocs")
                    locationNumberDspMempool0Array.append(locNumMempool0['vvalue'].value)
                    
                    locNumMempool1 = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[1].elem.m_LocationList.NumLocs")
                    locationNumberDspMempool1Array.append(locNumMempool1['vvalue'].value)
                    
                    locNumMempool2 = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[2].elem.m_LocationList.NumLocs")
                    locationNumberDspMempool2Array.append(locNumMempool2['vvalue'].value)
                    
                    locNumMempool3 = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[3].elem.m_LocationList.NumLocs")
                    locationNumberDspMempool3Array.append(locNumMempool3['vvalue'].value)
                    
                    locNumMempool4 = t32_api.get_variable_value("scom::g_dsp_dspMain_uC2_m_LocationInterface_out_local.m_arrayPool[4].elem.m_LocationList.NumLocs")
                    locationNumberDspMempool4Array.append(locNumMempool4['vvalue'].value)                                                            
            
            locationNumDsp = t32_api.get_variable_value("rbDsp::g_locationInterface_st.m_LocationList.NumLocs")               
            locationNumDspArray.append(locationNumDsp['vvalue'].value)
            # ----------------------------------------------------
            
            # let some DSP cycles pass
            time.sleep(1)            
    
        self.logger.debug(f"\tlocationNumberArray: {locationNumberArray}")
        
        # -------------------- Debugging information used for ATR-13950 ----
        self.logger.debug(f"\tlocationDataTimestampSecArray: {locationDataTimestampSecArray}")
        self.logger.debug(f"\tlocationDataTimestampNsArray: {locationDataTimestampNsArray}")
        self.logger.debug(f"\tlocationNumberDspMempool0Array: {locationNumberDspMempool0Array}")
        self.logger.debug(f"\tlocationNumberDspMempool1Array: {locationNumberDspMempool1Array}")
        self.logger.debug(f"\tlocationNumberDspMempool2Array: {locationNumberDspMempool2Array}")
        self.logger.debug(f"\tlocationNumberDspMempool3Array: {locationNumberDspMempool3Array}")
        self.logger.debug(f"\tlocationNumberDspMempool4Array: {locationNumberDspMempool4Array}")
        self.logger.debug(f"\tlocationNumDspArray: {locationNumDspArray}")    
        
        self.logger.debug(f"measurement running: {self.canoe_api.canoe.Measurement.Running}")
        
        bus2 = (self.canoe_api.canoe.Configuration.SimulationSetup.Buses("MAIN_2"))
        self.logger.debug(f"MAIN_2: bus.Active: {bus2.Active}")
        bus1 = (self.canoe_api.canoe.Configuration.SimulationSetup.Buses("MAIN_1"))
        self.logger.debug(f"MAIN_1: bus.Active: {bus1.Active}")
        # ----------------------------------------------------
    
        locGtZeroCounter = 0
        locGtZeroNoDuplicateArray = []

        # Check if some location number of the sequence are greater than 0 and
        # store them with no duplicates 
        for locNumber in locationNumberArray:
            if (locNumber > 0):
                locGtZeroCounter += 1
                
                if locNumber not in locGtZeroNoDuplicateArray:
                    locGtZeroNoDuplicateArray.append(locNumber)
        
        # at least k_locationNumberGtZeroMin location number should be greater than 0 
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, locGtZeroCounter, k_locationNumberGtZeroMin, 
                                                 "Check number of locations in ROS_LGP_Client::Loc_Data.LRR_LGU_LocData_NoLoc sequence")
        numberTest += 1
   
        # at least k_locationNumberDifferenceMin different location numbers have to be there     
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, len(locGtZeroNoDuplicateArray), k_locationNumberDifferenceMin, 
                                                 "Check difference of number of locations sequence")                                                  
        numberTest += 1

        # Read OpMode out of LGP interface
        lgp_opmode = self.canoe_api.getSysVar("ROS_LGP_Client","Loc_Data", "xRR_LGU_LocData_OpMode")
            
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, lgp_opmode, k_expectedDspOperationMode, 
                                                       "Check ROS_LGP_Client::Loc_Data.xRR_LGU_LocData_OpMode")            

        return CTestCaseResult(numberTest, numberFailedTests)
                
            
    def check_trap_information (self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        self.logger.info(f"RQM ID : {self.rqm.loc['TrapInformation','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['TrapInformation','LINK']}")
    
        trap_info = t32_api.get_variable_info("rbTraHa_TrapInformation_ap")
        array_size = int(trap_info['vsize'].value/4)
    
        self.logger.debug(f"rbTraHa_TrapInformation_ap array size: {array_size}")
        
        
        for i in range(array_size):
            trap_info_core_id = t32_api.get_variable_value(f"(*(rbTraHa_TrapInformation_ap[{i}])).CoreId_u8")
            self.logger.debug(f"trap_info_core_id ................{trap_info_core_id}")
            
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, trap_info_core_id['vvalue'].value, 
                                                       0, f"Check rbTraHa_TrapInformation_ap[{i}].CoreId_u8")                        
            numberTest += 1
            
            trap_info_class = t32_api.get_variable_value(f"(*(rbTraHa_TrapInformation_ap[{i}])).Class_u8")

            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, trap_info_class['vvalue'].value, 
                                                       0, f"Check rbTraHa_TrapInformation_ap[{i}].Class_u8")                    
            numberTest += 1
            
            trap_info_tin = t32_api.get_variable_value(f"(*(rbTraHa_TrapInformation_ap[{i}])).Tin_u8")
            
            numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, trap_info_tin['vvalue'].value, 
                                                       0, f"Check rbTraHa_TrapInformation_ap[{i}].Tin_u8")                        
                     
        return CTestCaseResult(numberTest, numberFailedTests)

        
    def check_safe_state (self, t32_api):
        numberFailedTests = 0
        numberTest = 1
        
        self.logger.info(f"RQM ID : {self.rqm.loc['Safe State','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['Safe State','LINK']}")
    
        time.sleep (1)
        rbMonReact_State = t32_api.get_variable_value("rbMonReact_State")
            
        validStates = (0, 2)
        
        numberFailedTests += testasserts.TEST_CONTAINS(self.logger, self.number_of_test, numberTest, rbMonReact_State['vvalue'].value, validStates,
                                                         "Check rbMonReact_State")
        if (numberFailedTests > 0):
            self.printAllFailedFaultEvents(t32_api)                                                                                                                                               

        return CTestCaseResult(numberTest, numberFailedTests)
        
        
    def check_Location_Interface (self, t32_api):    
        numberFailedTests = 0
        numberTest = 1
    
        self.logger.info(f"RQM ID : {self.rqm.loc['LocationInterface','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['LocationInterface','LINK']}")

        locationNumberArray = []
        
        # sample some location numbers and stored them in an array
        for i in range(k_locationNumberSamplingAmount):
            locations = t32_api.get_variable_value("rbDsp::g_locationInterface_st.m_LocationList.NumLocs")               
            locationNumberArray.append(locations['vvalue'].value)
            # let some DSP cycles pass
            time.sleep(1)            
    
        self.logger.debug(f"\tlocationNumberArray: {locationNumberArray}")
    
        locGtZeroCounter = 0
        locGtZeroNoDuplicateArray = []

        # Check if some location number of the sequence are greater than 0 and
        # store them with no duplicates 
        for locNumber in locationNumberArray:
            if (locNumber > 0):
                locGtZeroCounter += 1
                
                if locNumber not in locGtZeroNoDuplicateArray:
                    locGtZeroNoDuplicateArray.append(locNumber)

        
        # at least k_locationNumberGtZeroMin location number should be greater than 0 
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, locGtZeroCounter, k_locationNumberGtZeroMin, 
                                                 "Check number of locations in rbDsp::g_locationInterface_st.m_LocationList.NumLocs")
        numberTest += 1
   
        # at least k_locationNumberDifferenceMin different location numbers have to be there     
        numberFailedTests += testasserts.TEST_GE(self.logger, self.number_of_test, numberTest, len(locGtZeroNoDuplicateArray), k_locationNumberDifferenceMin, 
                                                 "Check difference of number of locations sequence")         
    
        return CTestCaseResult(numberTest, numberFailedTests)

    
    def check_smu (self, t32_api):
        numberFailedTests = 0
        numberTest = 1
    
        self.logger.info(f"RQM ID : {self.rqm.loc['LocationInterface','ID']}")
        self.logger.debug(f"RQM LINK : {self.rqm.loc['LocationInterface','LINK']}")
    
        smu_info_id = t32_api.get_variable_value("rbAlmHa_SmuInformation_st.CoreId")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, smu_info_id['vvalue'].value, 
                                                       0, "Check rbAlmHa_SmuInformation_st.CoreId")            
        numberTest += 1
        
        smu_alarm_group = t32_api.get_variable_value("rbAlmHa_SmuInformation_st.AlarmGroup")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, smu_alarm_group['vvalue'].value, 
                                                       0, "Check rbAlmHa_SmuInformation_st.AlarmGroup")        
        numberTest += 1
        
        smu_alarm_signal = t32_api.get_variable_value("rbAlmHa_SmuInformation_st.AlarmSignal")
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, self.number_of_test, numberTest, smu_alarm_signal['vvalue'].value, 
                                                       0, "Check rbAlmHa_SmuInformation_st.AlarmSignal")        
    
        return CTestCaseResult(numberTest, numberFailedTests)
        
    
    def run_sw_int_test_common(self, t32_api):               
        # localFilterList = ("check_trap_information; check_smu; check_daddy_error_information;" 
                            # "check_dsp_error_table; check_dsp_opmode; check_dsp_spu_status;"
                            # "check_Location_Interface; check_locations; check_safe_state")
        # test case: check_locations is currently disabled as it fails sporadically. Check ATR-13950
        localFilterList = ("check_trap_information; check_smu; check_daddy_error_information;" 
                            "check_dsp_error_table; check_dsp_opmode; check_dsp_spu_status;"
                            "check_Location_Interface; check_safe_state")                            
        
        numberOfFailedMainTests = self.executeFilteredFunctionUser(t32_api, localFilterList)           
        
        return testsuite.TestSuiteResult(self.number_of_test, numberOfFailedMainTests)
    
    
    def runSwIntTestCommonUC1(self, t32_api):        
        # localFilterList = ("check_trap_information; check_smu; check_daddy_error_information;" 
                            # "check_dsp_error_table; check_dsp_opmode; check_dsp_spu_status;"
                            # "check_locations; check_safe_state")
        # test case: check_locations is currently disabled as it fails sporadically. Check ATR-13950
        localFilterList = ("check_trap_information; check_smu; check_daddy_error_information;" 
                            "check_dsp_error_table; check_dsp_opmode; check_dsp_spu_status;"
                            "check_safe_state")                            
        
        numberOfFailedMainTests = self.executeFilteredFunctionUser(t32_api, localFilterList)           
        
        return testsuite.TestSuiteResult(self.number_of_test, numberOfFailedMainTests)        


    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC1(self):
        # set current FR5CU variant 
        g_currentFr5CuUcVariant = globalConstants.k_atf_hardwareLrrUc1
        
        testResult = testsuite.TestSuiteResult(1, 0)
        
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc1]
        testResult += self.runSwIntTestCommonUC1(t32_api)
        
        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        testResult += self.runSwIntTestCommonUC1(t32_api)
        
        # only numberFailedTests are needed of testResult, number_of_test are counted as member
        return testsuite.TestSuiteResult(self.number_of_test, testResult.numberFailedTests)


    ## @brief Implementation of abstract function of the CTestRunner interface 
    #
    def executeFr5CuTestsUC2(self):
        # set current FR5CU variant 
        g_currentFr5CuUcVariant = globalConstants.k_atf_hardwareLrrUc2
        
        testResult = testsuite.TestSuiteResult(1, 0)
        
        t32_api = self.t32_api[globalConstants.k_atf_hardwareLrrUc2]
        testResult += self.run_sw_int_test_common(t32_api)
        
        numberOfFailedMainTests = testResult.numberFailedTests
        numberOfFailedMainTests += self.executeFilteredFunctionUser(t32_api, "check_dem_events")

        lauterbachTestHelper.resetLauterbach(self.t32_api, self.logger)
        
        #create new instance with numberOfFailedMainTests
        testResult = testsuite.TestSuiteResult(self.number_of_test, numberOfFailedMainTests)
        testResult += self.run_sw_int_test_common(t32_api)
        
        # only numberFailedTests are needed of testResult, number_of_test are counted as member
        return testsuite.TestSuiteResult(self.number_of_test, testResult.numberFailedTests)                       


    ## @brief Implementation of abstract function of the CTestRunner interface 
    #    
    def getComponentName(self):
        return "int"
        
