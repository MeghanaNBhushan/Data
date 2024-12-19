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

k_buildCommitIdShortRegex = "RBBUILD_VERSION_COMMITIDSHORT\s\{([a-fA-F0-9\s',]*)"
k_replaceCharacters = ["'", ",", " "]

k_internalVersionLength = 5
k_shortCommitIdLength = 6


class CTestCaseOutputhandlerInternalVersion(CTestBase):

    def __init__(self, logger_api, canoe_api, t32_api):
        super().__init__(logger_api, canoe_api , t32_api)        
        self.m_parsedShortCommitId = None
        
        
    def setUp(self):
        self.logger.debug("SetUp test case: Extracting information from rbBuild_Version.h")
        
        # provided by the Unstash.py script   
        with open('./../../../generatedFiles/rbBuild_Version.h', 'r') as reader:
            # Read and print the entire file line by line
            for line in reader:
                if re.search(k_buildCommitIdShortRegex, line):
                    self.m_parsedShortCommitId = re.search(k_buildCommitIdShortRegex, line).group(1)                
                    self.logger.debug(f"commitIdShort of rbBuild_Version.h: {self.m_parsedShortCommitId}")
    
        if self.m_parsedShortCommitId != None:             
            for character in k_replaceCharacters:
                self.m_parsedShortCommitId = self.m_parsedShortCommitId.replace(character, "")


    def tearDown(self):
        pass


    ## @swtest_description This test case checks that the sent commmit id has a size of 5 bytes, is encoded in hexadecimal values and used the big endian format.
    #  @swtest_step
    #    1. Retrieve the internal version from the bus and check that the length is 5 bytes.
    #    2. Check that the parsed commit id of build_version_info.h during setup has a length of 6 bytes.
    #    3. Check that each byte of the commit id is send as specified in build_version_info.h on the bus.
    #  @swtest_expResult All test steps are executed and passed. 
    #  @sw_requirement{SDC-R_SW_COMA_1229, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1229-00159bc3?doors.view=00000005}       
    #  @sw_requirement{SDC-R_SW_COMA_1230, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1230-00159bc3?doors.view=00000005}
    #  @sw_requirement{SDC-R_SW_COMA_1231, https://rb-alm-13-p-dwa.de.bosch.com:8443/dwa/rm/urn:rational::1-4147106800294823-O-1231-00159bc3?doors.view=00000005}    
    def executeTests(self, t32_api, testCaseNumber):
    # 1229: The software shall send a 5 byte commit information based on the commit id on the bus.
    # 1230: The software shall encode the commit information in hexadecimal values.
    # 1231: The software shall send the commit information in big endian format.                
        numberFailedTests = 0
        number_test = 1        
                                             
        # 1. retrieve internal version from the bus and check length
        internalVersion = self.canoe_api.getSysVar("ROS_LGP_Client","SensorStateInfo_Output", "SenStInfo_SwNu_Int")
        self.logger.debug(f"InternalVersion retrieved from the bus: {self.getHexFromInt(internalVersion[0])} {self.getHexFromInt(internalVersion[1])} {self.getHexFromInt(internalVersion[2])} {self.getHexFromInt(internalVersion[3])} {self.getHexFromInt(internalVersion[4])}")
       
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, number_test, len(internalVersion), k_internalVersionLength, "Check bus internal version length")
        number_test += 1       
        
        # 2. check length of parsed values
        shortCommitIdArray = bytearray.fromhex(self.m_parsedShortCommitId)
        
        # parsed short commit id is one byte bigger than used internally for versioning
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, number_test, len(shortCommitIdArray), k_shortCommitIdLength, "Check parsed internal version length")
        number_test += 1        
        
        # 3. compare it with the BUILD_VINFO_COMMIT_ID_SHORT in build_version_info.h, only the first 5 bytes are used of the short commit id       
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, number_test, shortCommitIdArray[0] , (ctypes.c_uint8(internalVersion[0])).value, "Check short commit id byte 0")
        number_test += 1        
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, number_test, shortCommitIdArray[1] , (ctypes.c_uint8(internalVersion[1])).value, "Check short commit id byte 1")
        number_test += 1        
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, number_test, shortCommitIdArray[2] , (ctypes.c_uint8(internalVersion[2])).value, "Check short commit id byte 2")
        number_test += 1                
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, number_test, shortCommitIdArray[3] , (ctypes.c_uint8(internalVersion[3])).value, "Check short commit id byte 3")
        number_test += 1                
        numberFailedTests += testasserts.TEST_EQ(self.logger, testCaseNumber, number_test, shortCommitIdArray[4] , (ctypes.c_uint8(internalVersion[4])).value, "Check short commit id byte 4")        
                    
        return CTestCaseResult(number_test, numberFailedTests)
         

    def getHexFromInt(self, intValue):
        return hex((ctypes.c_uint8(intValue)).value)

