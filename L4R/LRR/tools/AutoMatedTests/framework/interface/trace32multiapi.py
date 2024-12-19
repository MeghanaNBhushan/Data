# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:02:02 2020

@author: YAH3KOR
"""

import argparse
import sys
import trace32api
import logger
import os
import time
import ctypes
import subprocess

class PracticeInterpreterState(object):
    """
    Return values of T32 practice script excutions:
       Used a class instead of an ENUM as ENUM is not no part of standard python used in BOSCH
    """
    UNKNOWN = -1
    NOT_RUNNING = 0
    RUNNING = 1
    DIALOG_OPEN = 2

class MessageLineState(object):
    """
    Return values of T32 practice commands:
       Used a class instead of an ENUM as ENUM is not no part of standard python used in BOSCH
    """
    OK = 0
    ERROR = 2
    ERROR_INFO = 16


class Trace32MultiApi(trace32api.Trace32Api):
    
    channel = None
    api = None
    logger = None

    def __init__(self, logger_api, trace32_config_file, dev_id, startup_script_file="", host="localhost"):
            self.trace32_config_file = os.path.abspath(trace32_config_file)
            self.startup_script_file = startup_script_file
            self.dev_id = dev_id
            self.host = host
            self.logger = logger_api.get_logger("Trace32MultiApi")
            trace32api.logger = logger_api.get_logger("Trace32Api")
            # Read config, start PowerView and connect Api to PowerView
            self.__read_trace32_config__()
            if startup_script_file == "":
                self.startup_script_file = os.path.join(self.inst_path, 'RadarGen5', 'StartupIfx.cmm')
            self.__start_power_view__()
            self.__connect_power_view_instance__()

            self.logger.debug(f"Channel {self.channel}")

    def __read_trace32_config__(self):
        """
        Read the configuration for Trace32 PowerView as some parameters are needed to connect the api to the PowerView
        """
        if not os.path.isfile(self.trace32_config_file):
            raise Exception(f"Trace32 config file is not found {self.trace32_config_file}")
        rcl = False
        config_file_handle = open(self.trace32_config_file, "r")
        for line in config_file_handle:
            line = line.replace(" ", "").strip()
            if line.startswith("RCL="):
                self.rcl = line.replace("RCL=", "")
                rcl = True
                self.logger.info(f"Remote configuration in trace32 config file: {self.rcl}")
            if line.startswith("PORT=") and rcl == True:
                self.port = line.replace("PORT=", "")
                rcl = False
                self.logger.info(f"PORT configured in trace32 config file: {self.port}")
            if line.startswith("PACKLEN="):
                self.packet_length = line.replace("PACKLEN=", "")
                self.logger.info(f"Packet-length configured in trace32 config file: {self.packet_length}")
            if line.startswith("SYS="):
                self.inst_path = line.replace("SYS=", "")
                self.logger.info(f"Installation path configured in trace32 config file: {self.inst_path}")
            # if line.startswith("NODE="):
                # self.host = line.replace("NODE=", "")
                # self.logger.info(f"Node configured in trace32 config file: {self.host}")

        # Check if all mandatory information could be found in config file
        if self.rcl != "NETASSIST":
            raise Exception(f"Class init failed as the given Trace32 config file is missing a / or has a wrong 'RCL' configuration")
        if self.port is None:
            raise Exception(f"Class init failed as the given Trace32 config file is missing 'PORT'")
        if self.packet_length is None:
            raise Exception(f"Class init failed as the given Trace32 config file is missing 'Packet Length'")
        if self.inst_path is None:
            raise Exception(f"Class init failed as the given Trace32 config file is missing 'SYS='")
        self.logger.info("All mandatory information found in *.t32 config file")


    def __start_power_view__(self):
        """
        Start the PowerView instance
        """
        # Setting path to t32api64.dll and loading lib into handel
        path = os.path.join(self.inst_path, 'demo', 'api', 'capi', 'dll', 't32api64.dll')
        self.logger.info(f"Load t32api handle with {path}...")
        self.api = ctypes.cdll.LoadLibrary(path)

        self.logger.info("PowerView is starting up...")
        command = [os.path.join(self.inst_path, 'bin', 'windows64', 'T32mtc.exe'), '-c', self.trace32_config_file, '-s', self.startup_script_file]
        self.power_view_instance = subprocess.Popen(command)
        time.sleep(10)
        channelSize = self.api.T32_GetChannelSize()
        self.channel = ctypes.create_string_buffer(channelSize)
        self.api.T32_GetChannelDefaults(ctypes.cast(self.channel, ctypes.c_void_p))
        self.logger.debug(f"Channel {self.channel}")
        self.logger.info("PowerView started...")


    def __connect_power_view_instance__(self):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        self.logger.debug(f"Connecting to instance {self.port}")
        self.api.T32_Config(b"NODE=", self.host.encode())
        self.api.T32_Config(b"PORT=", self.port.encode())
        self.api.T32_Config(b"PACKLEN=", self.packet_length.encode())

        # Initialize the api
        rc = self.api.T32_Init()
        if rc != 0:
            self.logger.error(ConnectionError(f"[E] Can't connect to Trace32 Debugger. Api call T32_Init() returned error: {rc}"))
            self.power_view_instance.kill()
            raise ConnectionError(f"[E] Can't connect to Trace32 Debugger. Api call T32_Init() returned error: {rc}")

        # Attach the PowerView to the target HW
        rc = self.api.T32_Attach(self.dev_id)
        if rc != 0:
            self.power_view_instance.kill()
            raise ConnectionError(f"[E] Can't connect to Trace32 Debugger. Api call T32_Attach() returned error {rc}")

        # Ping to check if connection is working fine
        rc = self.api.T32_Ping()
        if rc != 0:
            self.power_view_instance.kill()
            raise ConnectionError(f"[E] Can't connect to Trace32 Debugger. Api call T32_Ping() returned error {rc}")

        self.logger.info("Initialized Trace32 handle successfully...")
    def execute_t32_command(self, command):
        self.logger.debug(f"Executing : {command} in Multi")
        self.logger.debug(f"Setting channel {self.channel}")
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        self.logger.debug(f"Connecting powerview instance")
        self.logger.debug(f"Multi API {self.api}")
        # Execute command
        self.logger.debug(f"Executing : {command}")
        self.logger.debug(f"self.api {self.api}")
        self.api.T32_Cmd(b"PRINT")
        rc = self.api.T32_Cmd(command.encode())
        # Gathering result status and message from power view about the executed command
        api_return_status = ctypes.c_uint16(-1)
        area_win_message = ctypes.create_string_buffer(256)
        mrc = self.api.T32_GetMessage(ctypes.byref(area_win_message), ctypes.byref(api_return_status))
        self.logger.debug(f"rc.................{rc}")
        self.logger.debug(f"api_return_status.value.................{api_return_status.value}")
        self.logger.debug(f"area_win_message.value                 {area_win_message.value.decode()}")
        # Reaction based onf result status
        if rc == 0 and not api_return_status.value == MessageLineState.ERROR and not api_return_status.value == MessageLineState.ERROR_INFO:
            self.logger.debug(f"Command '{command}' finished successfully with message: '{area_win_message.value}'")
        else:
            self.logger.debug(f"[E] Command '{command}' returned error: '{area_win_message.value}")
            raise Exception(f"[E] Command '{command}' returned error: '{area_win_message.value}")

        
    def disconnect_power_view(self):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        super().disconnect_power_view()
    
    def close_power_view(self):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        super().close_power_view()
        
    def execute_t32_script(self,script_name):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        # Execute Script
        self.logger.debug(f"Execute script: {script_name}")
        rc = 0
        rc = self.api.T32_Cmd(b"CD.DO " + script_name.encode())

        # Wait until PRACTICE script is done
        script_exe_state = ctypes.c_int(PracticeInterpreterState.UNKNOWN)
        rc = 0
        while rc == 0 and not script_exe_state.value == PracticeInterpreterState.NOT_RUNNING:
            rc = self.api.T32_GetPracticeState(ctypes.byref(script_exe_state))

        # Gathering result status and message form power view about the executed script
        api_return_status = ctypes.c_uint16(-1)
        area_win_message = ctypes.create_string_buffer(256)
        mrc = self.api.T32_GetMessage(ctypes.byref(area_win_message), ctypes.byref(api_return_status))

        # Reaction based on result status
        if rc == 0 \
                and not api_return_status.value == MessageLineState.ERROR \
                and not api_return_status.value == MessageLineState.ERROR_INFO:
            self.logger.debug(f"Script '{script_name}' finished successfully with message: '{area_win_message.value}'")
        else:
            raise Exception(f"[E] Script '{script_name}' returned error: '{area_win_message.value}'")

    
    def flash_hex_and_load_sym(self, elf_file, hex_file):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        try:
            self.flash_hex(hex_file)
            self.load_elf(elf_file)
            return 0

        # Error handling in case the upper calles through an exception
        except Exception as fetched_ex:
            raise Exception(f"[E] Flashing hex or loading elf failed with error: '{fetched_ex}'")

    def synch_off(self):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        try:
            self.logger.debug("Turn SYnch off ...")
            # Set reset-behavior to halt and reset target to ensure the SW is halted before flashing
            self.execute_t32_command("SYnch.Connect")
            return 0

        # Error handling in case the upper calles through an exception
        except Exception as fetched_ex:
            raise Exception(f"[E] Error in turning synch off: '{fetched_ex}'")

    def synch_on(self):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        try:
            self.logger.debug("Turn SYnch on ...")
            # Set reset-behavior to halt and reset target to ensure the SW is halted before flashing
            absolutePathToScript = os.path.abspath('./framework/config/cmmScripts/SynchRemote.cmm')
            self.execute_t32_script(absolutePathToScript)

        # Error handling in case the upper calles through an exception
        except Exception as fetched_ex:
            raise Exception(f"[E] Error in turning synch on: '{fetched_ex}'")
        
    def flash_hex(self, hex_file):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        if not os.path.exists(hex_file):
            raise Exception(f"Can't find {hex_file}")

        # Try flashing
        try:
            self.logger.debug("start flashing hex...")
            # Set reset-behavior to halt and reset target to ensure the SW is halted before flashing
            self.execute_t32_command("Break")
            # Set global variable to the hex-file path
            self.execute_t32_command(f'&fileToFlash_global="{hex_file}"')
            # Call the FlashRoutine script
            self.execute_t32_script('CallFlashRoutine.cmm')
            # Error handling in case the upper calls through an exception
        except Exception as fetched_ex:
            self.logger.debug(f"{fetched_ex}")
            raise Exception(f"[E] Routine flash_hex() failed with error: '{fetched_ex}'")
    
    def load_elf(self, elf_file):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        super().load_elf(elf_file)
        
    def reset(self, mode, behaviour):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        self.execute_t32_command("System.Mode.Attach")
        self.execute_t32_command("System.Down")
        super().reset(mode, behaviour)

    
    def get_variable_info(self, variable):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        rv= super().get_variable_info(variable)
        return rv 

    def get_variable_value(self, variable):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        rv = super().get_variable_value(variable)
        return rv

    def get_variable_value_unsigned(self, variable):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        rv = super().get_variable_value(variable, True)
        return rv

    def set_variable_value(self, variable, value, valueh):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        super().set_variable_value(variable, value, valueh)
        
    def get_state(self):
        self.api.T32_SetChannel(ctypes.cast(self.channel, ctypes.c_void_p))
        rv = super().get_state()
        return rv