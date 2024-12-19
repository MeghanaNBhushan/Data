# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath('../../framework/scheduling'))

import atf_globalconstants as globalConstants

# DEM fault interface
k_demTestActicationSequence = 0xCCDA4EFF

# DEM fault status
g_demFaultStatusPassed = 0
g_demFaultStatusFailed = 1
g_demFaultStatusPrePassed = 2
g_demFaultStatusPreFailed = 3


# DEM fault status
g_demEventStatusPassedAllBits                  = 0
# 0x01 = 1 (bit 0: TestFailed 1)
g_demEventStatusFailedFailedTest = 0x1
# 0x03 = 3 (bit 0: TestFailed 1, bit 1: TestFailedThisOperationCycle 2)
g_demEventStatusFailedFailedThisCycle = 0x3
# 0x22 = 34 (bit 1: TestFailedThisOperationCycle 2 and Bit 5: TestFailedSinceLastClear 32)    
g_demEventStatusPassedFailedThisCycleLastClear = 0x22
# 0x23 = 35 (bit 0: TestFailed 1, bit 1: TestFailedThisOperationCycle 2 and bit 5: TestFailedSinceLastClear 32)
g_demEventStatusFailedFailedThisCycleLastClear = 0x23
# 0x2F = 47 (bit 0: TestFailed 1, bit 1: TestFailedThisOperationCycle 2, bit 2: PendingDTC 4, bit 3: ConfirmedDTC 8, bit 5: TestFailedSinceLastClear 32)
g_demEventStatusFailedFailedThisCyclePendingConfirmedLastClear = 0x2F
# 0x2E = 46 (bit 1: TestFailedThisOperationCycle 2, bit 2: PendingDTC 4, bit 3: ConfirmedDTC 8, bit 5: TestFailedSinceLastClear 32)
g_demEventStatusPassedFailedThisCycleDTCLastClear = 0x2E
# 0x26 = 38 (bit 1: TestFailedThisOperationCycle 2, bit 2: PendingDTC 4, bit 5: TestFailedSinceLastClear 32)
g_demEventStatusPassedFailedThisCyclePendingDTCLastClear = 0x26
# 0x2A = 42 (bit 1: TestFailedThisOperationCycle 2, bit 3: ConfirmedDTC 8, bit 5: TestFailedSinceLastClear 32)
g_demEventStatusPassedFailedThisCycleConfirmedDTCLastClear = 0x2A


# DspFault Interface tests
g_dspFaultEventsTestActivation = 0x7E57C0DE

# FIM permission
g_fimPermissionDenied = 0 # FId is denied and function should be inhibited
g_fimPermissionGranted = 1 # FId is granted and function can be executed                   
