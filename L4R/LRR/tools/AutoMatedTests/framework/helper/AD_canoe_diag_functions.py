import sys
import os
import time

sys.path.append(os.path.abspath('../scheduling'))

import AD_lauterbach_test_helper as lauterbachTestHelper
import atf_globalconstants as globalConstants
    
# Sends "Diagnostic Session Control: Extended Session (0x10 03)" service via the DoIP_DiagT Panel in the Rest Bus Simulation.
# Before sending the 10 03 service, connection to DiagT Panel is ensured.
def jumpToExtendedSession(canoe_api, logger):
    reestablishLostDiagTConnection(canoe_api, logger)   
    canoe_api.EnvVarButton("Env_DoipExtSession_AutoIP")        # trigger Extended session button
    time.sleep(1)

# Sends "Diagnostic Session Control: Default Session (0x10 01)" service via the DoIP_DiagT Panel in the Rest Bus Simulation.
# Before sending the 10 01 service, connection to DiagT Panel is ensured.
def jumpToDefaultSession(canoe_api, logger):
    reestablishLostDiagTConnection(canoe_api, logger)   
    canoe_api.EnvVarButton("Env_DoipDefaultSession_AutoIP")    # trigger Default session button
    time.sleep(1)
    
# Allows to send any specific diagnostic service via the DoIP_DiagT Panel in the Rest Bus Simulation
# Before sending the specified service, connection to DiagT Panel is ensured.
def sendSpecificDiagService(canoe_api, serviceString, logger):
    reestablishLostDiagTConnection(canoe_api, logger)   
    canoe_api.setEnvVar("Env_Doipsend_AutoIP", serviceString)  # write DID request
    time.sleep(1)
    canoe_api.EnvVarButton("Env_DoipSendBuf_AutoIP")           # trigger send button
    time.sleep(1)

# Performs a reset of the sensor via Lauterbach if the connection to the DoIPDiagT Panel in the Rest Bus Simulation is lost.
# After a Sensor Reset via Lauterbach, the DoIPDiagT Panel will automatically reestablish the connection to the sensor.
def reestablishLostDiagTConnection(canoe_api, logger):
    if canoe_api.getEnvVar("Env_DoipConnectVeh_status_AutoIP") == 0:
        time.sleep(2)
        # only do this time consuming part if the panel does not have connection after 2 seconds
        if canoe_api.getEnvVar("Env_DoipConnectVeh_status_AutoIP") == 0:
            logger.debug("Reestablish Diagnostic Connection... Restart Power Supply")
            canoe_api.disableSwitchButton("voltage_power_btn")
            time.sleep(2)
            canoe_api.enableSwitchButton("voltage_power_btn")
            time.sleep(4)

# Sends the Diagnostic Service "Diagnostic Session Control: Default Session (0x10 01)" via the DoIP_DiagT Panel in the Rest Bus Simulation.
# This function is required in addition to jumpToDefaultSession function because the jump from Programming Session to Default Session will 
# lead to a hard reset. Therefore, the same procedure as for the hard reset must be followed in this case.
def jumpToDefaultSessionFromProgramming(canoe_api, t32_api,  logger):
    delayAfterReset = 2
    handleDiagnosticSensorReset(canoe_api, t32_api, "Env_DoipDefaultSession_AutoIP", delayAfterReset, logger)

# Sends "Diagnostic Session Control: Programming Session (0x10 02)" service via the DoIP_DiagT Panel in the Rest Bus Simulation.
def jumpToProgrammingSession(canoe_api, uC1_t32_api, uC2_t32_api, logger):
    delayAfterReset = 3
    handleDiagnosticSensorReset(canoe_api, uC1_t32_api, uC2_t32_api, "Env_DoipProgSession_AutoIP", delayAfterReset, logger)
    
# Sends the Diagnostic Service "ECU Hard Reset (0x11 01)" via the DoIP_DiagT Panel in the Rest Bus Simulation.
def sendEcuHardReset(canoe_api,t32_api,logger):
    delayAfterReset = 2
    handleDiagnosticSensorReset(canoe_api,t32_api,  "Env_DoipEcuHardRest_AutoIP", delayAfterReset, logger)

# Sends the Diagnostic Service passed to the function as "resetType" via the DoIP_DiagT Panel in the Rest Bus Simulation.
# Sets Debugger to "NoDebug" mode before and to "Attach" afterwards. 
# Before sending the specified reset, connection to DiagT Panel is ensured.
def handleDiagnosticSensorReset(canoe_api, t32_api, resetType, delayAfterReset, logger):
    # without setting the debugger to NoDebug, there could be an influence on the reset behaviour
    hw = list(t32_api.keys())
    if hw[0] == globalConstants.k_atf_hardwareLrrUc2:
       lauterbachTestHelper.setSystemModeNoDebug(t32_api[globalConstants.k_atf_hardwareLrrUc2], logger, globalConstants.k_atf_hardwareLrrUc2)
      
    reestablishLostDiagTConnection(canoe_api, logger)   
    canoe_api.EnvVarButton(resetType) # trigger specified Reset 
    time.sleep(delayAfterReset)

    # attach Debugger again to be able to read symbols again. Only uC2 needs to be attached as debuggers are synched.
    if hw[0] == globalConstants.k_atf_hardwareLrrUc2:
       lauterbachTestHelper.setSystemModeAttach(t32_api[globalConstants.k_atf_hardwareLrrUc2], logger, globalConstants.k_atf_hardwareLrrUc2)


# Enables the sending of cyclic "Tester Present" (0x3E) services via the DoIP_DiagT Panel in the Rest Bus Simulation.
def sendCyclicTesterPresent(canoe_api, logger):
    reestablishLostDiagTConnection(canoe_api, logger)
    canoe_api.enableSwitchButton("Env_DoipTesterPresentOnOff_AutoIP")
    time.sleep(1)

# Disables the sending of cyclic "Tester Present" (0x3E) services via the DoIP_DiagT Panel in the Rest Bus Simulation.
def stopCyclicTesterPresent(canoe_api, logger):
    reestablishLostDiagTConnection(canoe_api, logger)
    canoe_api.disableSwitchButton("Env_DoipTesterPresentOnOff_AutoIP")
    time.sleep(1)
