# Change log of the AD_Radar_PF Automated Test Framework {#automatedTestFramework_changelog}
All notable changes in this Automated Test Framework are documented in this file.


## Sprint ATR\_SW\_SMF\_2202.IP

ATF Version: 0.14.0
### Features
* ATR-14262: Cleanup NR5CP related source/test code in sdm and rbSysEvM
    * Removed NR5CP test execution support


## Sprint ATR\_SW\_SMF\_2112.IP

ATF Version: 0.13.0
### Features
* ATR-13950: [ATF] Investigation on sporadic failed 'check_locations' test case
    * Introduced new 'testmode' for framework related test cases
* ATR-14216: [ATF] Create test mode in framework
    * New functions in CANoe interface: getSysVarNested(outerNamespaceOuter, innerNamespace, variable) and getConnectionStatus()
    * Testmode continued and first reset/bus test developed


## Sprint ATR\_SW\_SMF\_2112.2

ATF Version: 0.12.0
### Features
* ATR-13767: [ATF] Implement example ATF Test Summary Report
    * Replaced old test condition checks for 'int' tests by TEST_ASSERTS provided by the framework
    * Added new test assert 'TEST_GT'
    * Adapted some variable names according naming conventions


## Sprint ATR\_SW\_SMF\_2112.1

ATF Version: 0.11.0
### Features
* ATR-12362: Refactor Automated Test script output/summary
    * Adapted test results format
    * Renamed Assert function 'TEST_SEQ' to 'TEST_LE'

ATF Version: 0.10.0
### Features
* ATR-13532: [ATF] Separate framework from testcases - first step
    * Created one common 'framework' folder 
    

## Sprint ATR\_SW\_SMF\_2110.03

ATF Version: 0.9.0
### Features
* ATR-13588: [ATF] Update CANoe-API for SystemVar values
    * Added CANoe-API 'getSysVarValue'
    * Created config folder on top level
    * Moved test asserts into separate file (atf_testasserts.py)


## Sprint ATR\_SW\_SMF\_2110.02

ATF Version: 0.8.2
### Bugfixes
* ATR-13529: [Bugfix] ATF CTestBase return no failed test cases
    * Fixed return of no failed test cases and caught Trace32 test case exception

ATF Version: 0.8.1
### Bugfixes
* ATR-13505: [Bugfix] ATF get not failed on Jenkins if some tests are failed
    * Fixed that no exception was raised once a test case failed

ATF Version: 0.8.0
### Features
* ATR-13426: Execution time measurement for ATF components
    * Time measurement class added
    * Time measurement for component execution
    * Refactored test execution 


## Sprint ATR\_SW\_SMF\_2110.01
ATF Version: 0.7.0
### Others
* ATR-13338: Adapt ATF test case folder structure and names
    * Grouped test cases into component folder
    * Adapted test case file names
    * Initial unit tests added
* ATR-13138: Base class for test suites
    * Adapted class and file names


## Sprint ATR\_SW\_SMF\_2110.5
ATF Version: 0.6.0
### Features
* ATR-13118: Create filter mechanism for ATF-test
    * Implementation of filter mechanism
    * Update of sdm and rbSysEvM test cases
    * Adaption of documentation


## Sprint ATR\_SW\_SMF\_2110.2
ATF Version: 0.5.0
### Features
* ATR-12905: [LODM] Block Counter for Location Data - SWE3: Software detailed design and unit construction
    * Updated namespace name of CANoe system variables for all ATF test cases
* ATR-12998: Abstract interface for all test suites ("CTestRunner")
    * Implemented abstract interface 
    * Introduced semantic versioning


## Sprint ATR\_SW\_SMF\_2107.4
### Features
* ATR-12764: Come with timeline for ATF 
    * Updated documentation


## Sprint ATR\_SW\_SMF\_2105.5
### Features
* ATR-9894: [xRR] SWE6: Software (qualification) test for SDM
    * Initial SDM ATF test cases and documentation update    


## Sprint ATR\_SW\_SMF\_2105.4
### Features
* ATR-12452: [LRR] SWE6: Rework Architecture of Automated Test Framework 
    * Doxygen documentation created    

## Sprint ATR\_SW\_SMF\_2205.01
### Features
* ATR-14445: [LRR] SWE6: Tests Automation - Sensor mode request PDU
    * Initial COMA ATF test cases and documentation update      

## Sprint ATR\_SW\_LGC\_2205.03
### Features
* ATR-14439: [LRR] SWE6: Tests Automation - Measurement Program,Measurement Cycle Synchronization,Ego Vehicle PDU
    * Initial COMA ATF test cases and documentation update  

## Sprint ATR\_SW\_LGC\_2205.04
### Features
* ATR-14443: [LRR] SWE6: Tests Automation - Location Attribute PDU 
* ATR-14448: [LRR] SWE6: Tests Automation - Location Data PDU
    * Initial COMA ATF test cases for Validating communication parameters and documentation update  

## Sprint ATR\_SW\_LGC\_2205.05
### Features
* ATR-14444: [LRR] SWE6: Tests Automation - Variant Handling Local IP/Remote IP/Remote Port/DOIP
* ATR-15020: [LRR] SWE6: Tests Automation - Variant Handling MAC/Diag Source IP
    * Initial VAMA ATF test cases and documentation update 
* ATR-15105: [LRR] SWE6: Test automation - Location Header signals validation
* ATR-14441: [LRR] SWE6: Tests Automation - Sensor feedback channel
    * Added guard checks before SW tests are executed in-order to ensure TX PDUs are continuously sent from radar on bus
    * Communication parameters of sensor feedback PDU are present in coma test suite and feature are tested in lodm


## Sprint ATR\_SW\_LGC\_2207.01
### Features
* ATR-14442: [LRR] SWE6: Tests Automation - Mounting Position and Misalignment
    * Initial ATF test cases for mounting position and misalignment
    * Verification of diagnostic DID data for valid and invalid values
    * Validation of data sent over COM buffer

## Sprint ATR\_SW\_LGC\_2207.02
### Features
* ATR-15589: [LRR] SWE6: Ego Vehicle Data: Out Of Range Behavior - SWE6: Software (qualification) test
    * Test case update for Ego Vehicle PDU signals
	
## Sprint ATR\_SW\_LGC\_2207.04
### Features
* ATR-14449: [LRR] SWE6: Test Automation - Time Synchronization Feature  
    * Verification of STBM Switch is ON and OFF and check for timeBaseStatus
    * Verification of Leap Past and Leap Future
    * Verification of Reset condition     
    * Validation of data through trace32 and documentation updated

## Sprint ATR\_SW\_LGC\_2209.03
### Bugfixes
* ATR-16508: [LRR] DMP data not updating in same ignition cycle when changed by DID
    * Test case update for processing DMP in the same ignition cycle
    
## Sprint ATR\_SW\_SMF\_2212.04
### Bugfixes
* ATR-17795: [LRR] Test Case Update for NRC31 Usecase for Invalid MAC Address Data

## Sprint ATR\_SW\_LGC\_2212.04
### Features
* ATR-16239: [LRR] Ego Vehicle data in Feedback PDU - SWE6: Software (qualification) test
    * Validating the EgoVehicle Data updated in sensorfeedback PDU

## Sprint ATR\_SW\_LGC\_2212.04
### Bugfixes
* ATR-15755: [LRR] Variant handling for SensorBroadCast SW Tests
    * Test case update for Variant handling for SensorBroadCast
   

[//]: # (Please use the following template for new entries)
[//]: # (## Sprint ATR\_SW\_TEAM\_xxxx.x)
[//]: # (### Features  )
[//]: # (   none)
[//]: # (### Bugfixes)
[//]: # (   none)
[//]: # (### Known Limitations)
[//]: # (   none)
[//]: # (### Others)
[//]: # (   none)
[//]: # (### Integration hints)
[//]: # (none)
