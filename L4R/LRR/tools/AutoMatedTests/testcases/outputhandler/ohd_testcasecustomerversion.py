# -*- coding: utf-8 -*-

import sys
import os
import re
import ctypes

sys.path.append(os.path.abspath('../../framework/interface'))

import atf_toolbox as testHelper
import atf_testasserts as testasserts
from testbase import CTestBase
from testbase import CTestCaseResult

k_firstByteMask = ctypes.c_uint32(0x000000ff)
k_secondByteMask = ctypes.c_uint32(0x0000ff00)
k_thirdByteMask = ctypes.c_uint32(0x00ff0000)
k_fourthByteMask = ctypes.c_uint32(0xff000000)
k_maxOneByte = 0xff
k_maxThreeByte = 0xffffff

k_customerVersionMajorNumberRegex = 'SW_VERSION_MAJOR_NUMBER ([0-9]*)U'
k_customerVersionMinorNumberRegex = 'SW_VERSION_MINOR_NUMBER ([0-9]*)U'
k_customerVersionPatchNumberRegex = 'SW_VERSION_PATCH_NUMBER ([0-9]*)U'


class CTestCaseOutputhandlerCustomerVersion(CTestBase):        
    def __init__(self, logger_api, canoe_api, t32_api):
        super().__init__(logger_api, canoe_api , t32_api)       
        self.m_parsedCustomerVersionMajorNumber = None
        self.m_parsedCustomerVersionMinorNumber = None
        self.m_parsedCustomerVersionPatchNumber = None
        
        
    def setUp(self):
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
                      
    
    def tearDown(self):
        pass


    ## @swtest_description This test case checks that the software version consists of a major version, a minor version, the patch level and checks if the
    # version send on the bus match the version defined in sw_version_cfg.h 
    # @swtest_step
    #    1. Retrieve the customer version send on the bus 
    #    2. Check that the customer version value is within the defined boundaries
    #    3. Check that each byte of the customer version(unused, major, minor and patch) is send as specified in sw_version_cfg.h  
    # @swtest_expResult All test steps are executed and passed. 
    # @sw_requirement{SDC-R_SW_COMA_1221, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1221-00159bc3?doors.view=00000005}    
    def executeTests(self, t32_api, testCaseNumber):        
    # The software shall send a 4 byte software version which consist of a major version, a minor version and the patch level.        
        numberFailedTests = 0
        numberTest = 1                
        
        # 1. retrieve customer version from the bus
        customerVersionBus = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SwNu_Cust")        
        self.logger.debug(f"Customer version on bus: {hex(customerVersionBus)}")

        # 2. check bus value boundaries -> min and max
        numberFailedTests += testasserts.TEST_GE(self.logger, testCaseNumber, numberTest, customerVersionBus, 0, "Check customer version boundary")
        numberTest += 1        
        numberFailedTests += testasserts.TEST_LE(self.logger, testCaseNumber, numberTest, customerVersionBus, k_maxThreeByte, "Check customer version boundary")
        numberTest += 1
        
        # 3. check 4 byte for major version, minor version and patch level 
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
                      
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, numberTest, unusedByteBus.value, 0, "Check unused byte")
        numberTest += 1
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, numberTest, majorByteBus.value, majorByteParsed.value, "Check major version")
        numberTest += 1
        
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, numberTest, minorByteBus.value, minorByteParsed.value, "Check minor version")
        numberTest += 1

        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, numberTest, patchByteBus.value, patchByteParsed.value, "Check patch level")                    
        
        return CTestCaseResult(numberTest, numberFailedTests)
    
    
    def getUnusedByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_fourthByteMask.value) >> 24)
    
    def getMajorByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_thirdByteMask.value) >> 16)
    
    def getMinorByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_secondByteMask.value) >> 8)
    
    def getPatchLevelByteCustVersion(self, customerVersionCType):
        return ctypes.c_uint8((customerVersionCType.value & k_firstByteMask.value))    
    
    
