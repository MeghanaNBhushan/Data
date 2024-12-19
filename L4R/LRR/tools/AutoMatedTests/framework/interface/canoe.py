# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 03:36:49 2020

@author: YAH3KOR
"""

import win32com.client 
import os
import subprocess
import sys 
import logger
import time
from win32com.client import CastTo
from enum import Enum


class EConnectionStatus(Enum):
    STATE_UNKNOWN = 0 # The statistic signal is not available (e.g. in working mode "Simulated bus" or in offline mode)
    LINK_DOWN     = 1 # The network cable is not connected or the remote station cannot be detected. 
                      # This might be caused by different transfer rates of the Ethernet interfaces.
    LINK_UP       = 2 # A network cable is connected and the connection to a remote station is available.


class CANoe:
    
    logger = None
    
    def __init__(self, logger_api):
        self.logger = logger_api.get_logger("CANoe")
        self.canoe = None


    def initAndOpenConfig(self, cfgFile):
        output = subprocess.check_output('tasklist', shell=True)
        
        if "CANoe64.exe" in str(output):
            self.logger.debug("Terminate CANoe64.exe via taskkill...")
            os.system("taskkill /im CANoe64.exe /f 2>nul >nul")        
        
        self.logger.debug("Initialising CANoe COM object...")       
        
        self.canoe = win32com.client.Dispatch("CANoe.Application")
        self.logger.debug("Loading CANoe cfg file...")        
        
        if os.path.exists(cfgFile):
            # object.Open(path[, autoSave[, promptUser]])
            # autoSave (optional): A boolean value that indicates whether the active configuration should be saved if it has been changed.
            # promptUser (optional): A boolean value that indicates whether the user should intervene in error situations.
            self.canoe.Open(cfgFile, False, False)
            self.logger.info("SUCCESS - The CANoe Cfg loaded successfully!")
        else:
            self.logger.error(f"ERROR - The given path for the CANoe Cfg does not exist - {cfgFile}")
            raise RuntimeError


    def setupCANoeEnvironment(self, tollnerPS_port):
        self.EnableNode("Doip_DiagTester_Dhcp_client_AutoIP")
        self.EnableNode("Toellner_rs232")
        self.DisableNode("EA_PS_rs232")
        self.DisableNode("Toellner_LAN")

        self.logger.info("Toellner Port Usage: " + str(tollnerPS_port))
        self.setSysVarNested("RBS_PS","Toellner","RS232_comport", tollnerPS_port)  
        
        # switch on Auto IP
        self.setEnvVar("Env_Doip_Set_AutoIP", 1)        
        # set reconnect time of Doip Diag T Panel to 3 seconds
        self.setEnvVar("Env_DoipConnectVeh_waitTime", 3000)        

        self.startMeasurement()
        self.connectPowerSupply()

    
    def startMeasurement(self):
        self.logger.debug(f"Starting measurement ....")
        retry = 0
        retryRate = 200
        while not self.canoe.Measurement.Running and ( retry < retryRate )  :
            self.canoe.Measurement.Start()
            time.sleep(2)
            retry +=1
            if retry == (retryRate + 1) :
                self.logger.error(f"ERROR - Unable to start measurement")
                raise RuntimeError
        if self.canoe.Measurement.Running and ( retry <= retryRate ) :
           self.logger.info(f"SUCCESS - Measurement running") 
            
    def stopMeasurement(self):
        self.logger.debug(f"Stopping measurement ....")
        if self.canoe.Measurement.Running:
            self.canoe.Measurement.StopEx()
            self.canoe.Quit()
            del self.canoe
            self.canoe = None            
            self.logger.info(f"SUCCESS - Measurement stopped!")
            
        else:
            self.logger.error(f"ERROR - Unable to stop measurement")
            raise RuntimeError
           
            
    def setSysVarValue(self, namespace, variable, variableValue):
        self.logger.debug(f"Setting System Variable {variable} with value {variableValue}")
        
        try:
            self.canoe.System.Namespaces.Item(namespace).Variables.Item(variable).Value = variableValue
            time.sleep(1)
        
            if (self.canoe.System.Namespaces.Item(namespace).Variables.Item(variable).Value == variableValue) : 
                self.logger.info(f"Set System Variable {variable} with value {variableValue} successfully")
            else : 
                self.logger.error(f"Failed setting System Variable {variable} with value {variableValue}")
        except Exception as exception:
            self.logger.error(f"Error in setting System Variable {variable} with value {variableValue} with {exception}")
            raise RuntimeError
            
    def setSysVarValue_withoutDelay(self, namespace, variable, variableValue):
        self.logger.debug(f"Setting System Variable {variable} with value {variableValue}")
        
        try:
            self.canoe.System.Namespaces.Item(namespace).Variables.Item(variable).Value = variableValue
            
        except Exception as exception:
            self.logger.error(f"Error in setting System Variable {variable} with value {variableValue} with {exception}")
            raise RuntimeError

    def getSysVarValue(self, namespace, variable):
        self.logger.debug(f"Getting System Variable {variable} value")
        try: 
            sysVarValue = self.canoe.System.Namespaces.Item(namespace).Variables.Item(variable).Value
            self.logger.info(f" Successfully got System Variable {variable} with value {sysVarValue}")
            return sysVarValue
        except Exception as exception:
            self.logger.error(f"Error in Getting System Variable {variable} value with {exception}")
            raise RuntimeError

    def setSysVarMemberValue(self, namespace, variable, member, variableValue):
        self.logger.debug(f"Setting System Variable {variable} for member {member} with value {variableValue}")
        
        try:
            sysVar = self.canoe.System.Namespaces.Item(namespace).Variables.Item(variable)
            sysVar11 = CastTo(sysVar,"IVariable11")       
            sysVar11.Members.Item(member).Value = variableValue
            time.sleep(1)
            
            if ((sysVar11.Members.Item(member).Value) == variableValue) :                                             
                self.logger.info(f"Set System Variable {variable} for member {member} with value {variableValue} successfully")
            else : 
                self.logger.error(f"Error failed setting System Variable {variable} for member {member} with value {variableValue}")            
        except:
            self.logger.error(f"Error in setting System Variable {variable} for member {member} with value {variableValue}")
            raise RuntimeError
            
    def getSysVar(self, namespace, variable, member):
        self.logger.debug(f"Getting System Variable {variable} value for  member {member}")
        try: 
            sysVarValue = self.canoe.System.Namespaces.Item(namespace).Variables.Item(variable)
            sysVar11 = CastTo(sysVarValue,"IVariable11")
            sysVarMemberValue = sysVar11.Members.Item(member).Value
            self.logger.info(f" Successfully got System Variable {variable} member {member} value")
            return sysVarMemberValue
        except:
            self.logger.error(f"Error in Getting System Variable {variable} member {member} value")
            raise RuntimeError
            
    def getSysVarNested(self, outerNamespaceOuter, innerNamespace, variable):
        self.logger.debug(f"Setting nested System Variable {variable} value of outer namespace {outerNamespaceOuter} and inner namespace {innerNamespace}")
        try: 
            sysVarValue = ((self.canoe.System.Namespaces(outerNamespaceOuter + "::" + innerNamespace))).Variables(variable).Value            
            
            self.logger.info(f" Successfully got nested System Variable: {variable} value")
            return sysVarValue
        except:
            self.logger.error(f"Error in Getting nested System Variable {variable} value")
            raise RuntimeError            
            
    def setSysVarNested(self, outerNamespaceOuter, innerNamespace, variable, variableValue):
        self.logger.debug(f"Getting nested System Variable {variable} value of outer namespace {outerNamespaceOuter} and inner namespace {innerNamespace}")
        try: 
            ((self.canoe.System.Namespaces(outerNamespaceOuter + "::" + innerNamespace))).Variables(variable).Value = variableValue

            
            if ((self.canoe.System.Namespaces(outerNamespaceOuter + "::" + innerNamespace))).Variables(variable).Value == variableValue :
                self.logger.info(f" Successfully set nested System Variable: {variable} with value {variableValue}")
            else : 
                self.logger.error(f"Error failed setting System Variable {variable} with value {variableValue}")            
        except:
            self.logger.error(f"Error in setting nested System Variable {variable} with value {variableValue}")
            raise RuntimeError            
 
    def isSignalOnline(self, bus, channel, namespace, signalName):
        self.logger.debug(f"Checking if signal {signalName} is being received")
        try: 
            signal = ((self.canoe.GetBus(bus)).GetSignal(channel, namespace, signalName))
            self.logger.debug(f"Obtained signal {signalName} Object")
            return signal.IsOnline
        except:
            self.logger.error(f"Failed obtaining signal object for signal {signalName}. Check if measurement is running and signal name is correct")
            raise RuntimeError

    def deactivateBus(self, busName):
        self.logger.debug(f"Checking if bus {busName} exists")
        try: 
            bus = (self.canoe.Configuration.SimulationSetup.Buses(busName))
            self.logger.debug(f"Obtained bus {bus} Object")
        except:
            self.logger.error(f"Failed obtaining bus object for bus {busName}. Check if measurement is running and bus name is correct")
            raise RuntimeError

        bus.Active = False
        time.sleep(2)
        if bus.Active == False:
            self.logger.info(f"Bus {busName} successfully deactivated")
        else:
            self.logger.error(f"Failed to deactivate Bus {busName}")
            raise RuntimeError


    def activateBus(self, busName):
        self.logger.debug(f"Checking if bus {busNameS} exists")
        try: 
            bus = (self.canoe.Configuration.SimulationSetup.Buses(busName))
            self.logger.debug(f"Obtained signal {bus} Object")
        except:
            self.logger.error(f"Failed obtaining bus object for bus {busName}. Check if measurement is running and bus name is correct")
            raise RuntimeError

            bus.Active = True
            time.sleep(2)
            if bus.Active == True:
                self.logger.info(f"Bus {busName} successfully activated")
            else:
                self.logger.error(f"Failed to activate Bus {busName}")
                raise RuntimeError

    def getSignalVal(self, bus, channel, namespace, signalName):
        self.logger.debug(f"Checking signal {signalName} value")
        try:
            signal = ((self.canoe.GetBus(bus)).GetSignal(channel, namespace, signalName))
            self.logger.debug(f"Obtained signal {signalName} Object")
            signalVal = signal.Value
            self.logger.info(f"Signal {signalName} value : {signalVal}")
            return signalVal
        except:
            self.logger.error(f"Failed obtaining signal object for signal {signalName}. Check if measurement is running and signal name is correct")    
            raise RuntimeError
    
    def setEnvVar(self, EnVar, EnVarValue):
        self.logger.debug(f"Setting Environment Variable {EnVar} value {EnVarValue}")
        try:
            EnvironmentVar = self.canoe.Environment.GetVariable(EnVar)  
            EnvironmentVar.Value = EnVarValue
        except:
            self.logger.error(f"Failed in setting Environment Variable {EnVar}.")
            raise RuntimeError
            
    def getEnvVar(self, EnVar):
        self.logger.debug(f"Getting Environment Variable {EnVar} value")
        try:
            EnvironmentVar = self.canoe.Environment.GetVariable(EnVar)
            value = EnvironmentVar.Value
            self.logger.info(f"Environment Variable {EnVar} value : {value}")
            return (value)
        except:
            self.logger.error(f"Failed obtaining Environment Variable {EnVar}")
            raise RuntimeError
            
    def EnvVarButton(self, button):
        self.logger.debug(f"clicking {button}")
        EnvironmentVar = self.canoe.Environment.GetVariable(button)  
        EnvironmentVar.Value = 1
        time.sleep(1)
        EnvironmentVar.Value = 0 
        
    def EnableNode(self, node) :
        self.logger.debug(f"Enabling node {node}")
        getNode = self.canoe.Configuration.SimulationSetup.Nodes(node)
        if getNode.Active == False :
            getNode.Active = True
            self.logger.debug(f"Node {node} Enabled")
        elif getNode.Active == True :
            self.logger.debug(f"Node {node} already enabled")
        else:
            self.logger.error(f"Node {node} not enabled")
            raise RuntimeError
            
    def DisableNode(self, node):
        self.logger.debug(f"Disabling node {node}")
        getNode = self.canoe.Configuration.SimulationSetup.Nodes(node)
        if getNode.Active == True :
            getNode.Active = False
            self.logger.debug(f"Node {node} disabled")
        elif getNode.Active == False :
            self.logger.debug(f"Node {node} already disabled")
        else:
            self.logger.error(f"Unable to disable {node}")          
            raise RuntimeError

    # Presses "Connect" button of Power Supply Unit "Toellner" in the Rest Bus Simulation to enable control of the Power Supply Unit
    def connectPowerSupply(self):
        self.EnvVarButton("voltage_reset_btn")
        time.sleep(1)
        self.disableSwitchButton("voltage_remote_btn")
        self.disableSwitchButton("voltage_power_btn")
        time.sleep(3)
        self.enableSwitchButton("voltage_remote_btn")
        self.enableSwitchButton("voltage_power_btn")
        time.sleep(3)
        

    # enable function for the switchable buttons (e.g. In/Output of Power Supply,...)
    def enableSwitchButton(self, button):
        self.logger.debug(f"Enable Switch Button {button}")
        EnvironmentVar = self.canoe.Environment.GetVariable(button)  
        EnvironmentVar.Value = 1
        time.sleep(2)
        if EnvironmentVar.Value == 1:
            self.logger.debug(f"Successfully enabled button {button}")
        elif EnvironmentVar.Value == 0:
            self.logger.error(f"Failed to enable button {button}")
            raise RuntimeError
    # disable function for the switchable buttons (e.g. In/Output of Power Supply,...)
    def disableSwitchButton(self, button):
        self.logger.debug(f"Disable Switch Button {button}")
        EnvironmentVar = self.canoe.Environment.GetVariable(button)  
        EnvironmentVar.Value = 0
        time.sleep(2)
        if EnvironmentVar.Value == 0:
            self.logger.debug(f"Successfully disabled button {button}")
        elif EnvironmentVar.Value == 1:
            self.logger.error(f"Failed to disable button {button}")
            raise RuntimeError

    # Wrapper for the system variable ConnectionStatus on Eth1
    # EConnectionStatus is returned
    def getConnectionStatus(self):
        return EConnectionStatus(self.getSysVarNested("_Statistics", "Eth1", "ConnectionStatus"))
