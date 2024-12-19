import ctypes
import os
import subprocess
import time
import logging

from enum import Enum


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

class ETrace32State(Enum):
    DEBUG_SYSTEM_DOWN        = 0 # 0: Debug system is down
    DEBUG_SYSTEM_HALTED      = 1 # 1: Debug system is halted, CPU makes no cycles (no access). Halted
    TARGET_EXECUTION_STOPPED = 2 # 2: Target execution is stopped (Break)
    TARGET_EXECUTION_RUN     = 3 # 3: Target execution is running (Go)                                


class Trace32Api:
    """
    Base class using cAPI of the T32 via pyhton ctyps to make the libary funciton of the T32 cAPI avialable
    """
    api = None
    api_dll_path = None
    inst_path = None
    trace32_config_file = None
    startup_script_file = None
    host = None
    port = None
    dev_id = None
    power_view_instance = None
    packet_length = None
    rcl = None
    logger = None
    def __init__(self, logger_api, trace32_config_file, dev_id, startup_script_file="", host="localhost"):
        # Set class variables
        self.trace32_config_file = trace32_config_file
        self.startup_script_file = startup_script_file
        self.dev_id = dev_id
        self.host = host
        self.logger = logger_api.get_logger("Trace32Api")

        # Read config, start PowerView and connect Api to PowerView
        self.__read_trace32_config__()
        if startup_script_file == "":
            self.startup_script_file = os.path.join(self.inst_path, 'RadarGen5', 'StartupIfx.cmm')
        self.__start_power_view__()
        self.__connect_power_view__()

    def __read_trace32_config__(self):
        """
        Read the configuration for Trace32 PowerView as some parameters are needed to connect the api to the PowerView
        """
        if not os.path.isfile(self.trace32_config_file):
            raise Exception("Trace32 config file is not found")

        config_file_handle = open(self.trace32_config_file, "r")
        for line in config_file_handle:
            line = line.replace(" ", "").strip()
            if line.startswith("RCL="):
                self.rcl = line.replace("RCL=", "")
                self.logger.info(f"Remote configuration in trace32 config file: {self.rcl}")
            if line.startswith("PORT="):
                self.port = line.replace("PORT=", "")
                self.logger.info(f"PORT configured in trace32 config file: {self.port}")
            if line.startswith("PACKLEN="):
                self.packet_length = line.replace("PACKLEN=", "")
                self.logger.info(f"Packet-length configured in trace32 config file: {self.packet_length}")
            if line.startswith("SYS="):
                self.inst_path = line.replace("SYS=", "")
                self.logger.info(f"Installation path configured in trace32 config file: {self.inst_path}")

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
        self.logger.info("PowerView is starting up...")
        command = [os.path.join(self.inst_path, 'bin', 'windows64', 'T32mtc.exe'), '-c', self.trace32_config_file, '-s', self.startup_script_file]
        self.power_view_instance = subprocess.Popen(command)
        time.sleep(5)
        self.logger.info("PowerView started...")

    def __connect_power_view__(self):
        """
        Connect to local or remote Trace32 (in case of remote already started)
        """

        # Setting path to t32api64.dll and loading lib into handel
        path = os.path.join(self.inst_path, 'demo', 'api', 'capi', 'dll', 't32api64.dll')
        self.logger.info(f"Load t32api handle with {path}...")
        self.api = ctypes.cdll.LoadLibrary(path)

        # Configure the remote communication channel between api and PowerView
        self.api.T32_Config(b"NODE=", self.host.encode("ascii"))
        self.api.T32_Config(b"PORT=", self.port.encode("ascii"))
        self.api.T32_Config(b"PACKLEN=", self.packet_length.encode("ascii"))

        # Initialize the api
        rc = self.api.T32_Init()
        if rc != 0:
            raise ConnectionError(f"[E] Can't connect to Trace32 Debugger. Api call T32_Init() returned error: {rc}")

        # Attach the PowerView to the target HW
        rc = self.api.T32_Attach(self.dev_id)
        if rc != 0:
            raise ConnectionError(f"[E] Can't connect to Trace32 Debugger. Api call T32_Attach() returned error {rc}")

        # Ping to check if connection is working fine
        rc = self.api.T32_Ping()
        if rc != 0:
            raise ConnectionError(f"[E] Can't connect to Trace32 Debugger. Api call T32_Ping() returned error {rc}")

        self.logger.info("Initialized Trace32 handle successfully...")

    def disconnect_power_view(self):
        """
        Disconnect from local or remote Trace32
        """

        self.logger.info(f"Disconnecting API from PowerView with id: {self.dev_id}")
        rc = self.api.T32_Exit()
        if rc != 0:
            raise ConnectionError(f"[E] Can't disconnect Trace32. T32_Exit() api call returned: {rc}")

    def close_power_view(self):
        """
        Close the power view instance
        """

        self.logger.info("Terminating power view instance...")
        self.execute_t32_command("SYStem.Mode Down")
        self.api.T32_Cmd("quit".encode("ascii"))

    def execute_t32_command(self, command):
        """
        Executes a single given Trace32 practice command
        """

        # Execute command
        self.logger.debug(f"Executing : {command}")
        self.api.T32_Cmd(command.encode("ascii"))

        # Gathering result status and message from power view about the executed command
        api_return_status = ctypes.c_int32(-1)
        area_win_message = ctypes.create_string_buffer(256)
        rc = self.api.T32_GetMessage(ctypes.byref(area_win_message), ctypes.byref(api_return_status))

        # Reaction based onf result status
        if rc == 0 \
                and not api_return_status.value == MessageLineState.ERROR \
                and not api_return_status.value == MessageLineState.ERROR_INFO:
            self.logger.debug(f"Command '{command}' finished successfully with message: '{area_win_message.value}'")
        else:
            raise Exception(f"[E] Command '{command}' returned error: '{area_win_message.value}")

    def execute_t32_script(self, script_name):
        """
        Executes a given Trace32 practice script. As parameter the the absolut path to the
        script including the script name is required
        """

        # Execute Script
        self.logger.debug(f"Execute script: {script_name}")
        self.api.T32_Cmd(b"CD.DO " + script_name.encode("ascii"))

        # Wait until PRACTICE script is done
        script_exe_state = ctypes.c_int(PracticeInterpreterState.UNKNOWN)
        rc = 0
        while rc == 0 and not script_exe_state.value == PracticeInterpreterState.NOT_RUNNING:
            rc = self.api.T32_GetPracticeState(ctypes.byref(script_exe_state))

        # Gathering result status and message form power view about the executed script
        api_return_status = ctypes.c_uint16(-1)
        area_win_message = ctypes.create_string_buffer(256)
        rc = self.api.T32_GetMessage(ctypes.byref(area_win_message), ctypes.byref(api_return_status))

        # Reaction based on result status
        if rc == 0 \
                and not api_return_status.value == MessageLineState.ERROR \
                and not api_return_status.value == MessageLineState.ERROR_INFO:
            self.logger.debug(f"Script '{script_name}' finished successfully with message: '{area_win_message.value}'")
        else:
            raise Exception(f"[E] Script '{script_name}' returned error: '{area_win_message.value}'")

    def flash_hex_and_load_sym(self, elf_file, hex_file):
        """
        Flash and loads a given hex & elf. As parameter the absolute path to the hex and elf is required.
        """

        # Using subroutines flash and load
        try:
            self.flash_hex(hex_file)
            self.load_elf(elf_file)
            return 0

        # Error handling in case the upper calles through an exception
        except Exception as fetched_ex:
            raise Exception(f"[E] Flashing hex or loading elf failed with error: '{fetched_ex}'")

    def flash_hex(self, hex_file):
        """
        Flash a given hex. As parameter the absolut path to the hex is required.
        """

        # Check if file exist
        if not os.path.exists(hex_file):
            raise Exception(f"Can't find {hex_file}")

        # Try flashing
        try:
            self.logger.debug("start flashing hex...")
            # Set reset-behavior to halt and reset target to ensure the SW is halted before flashing
            self.execute_t32_command("SYStem.Option RESetBehavior halt")
            self.execute_t32_command("SYSTEM.RESETTARGET")
            # Set global variable to the hex-file path
            self.execute_t32_command(f"&fileToFlash_global=\"{hex_file}\"")
            # Call the FlashRoutine script
            area_win_message = self.execute_t32_script("CallFlashRoutine.cmm")
            self.logger.debug(f"Routine flash_hex() finished successfully with message: '{area_win_message}'")
        # Error handling in case the upper calls through an exception
        except Exception as fetched_ex:
            raise Exception(f"[E] Routine flash_hex() failed with error: '{fetched_ex}'")

    def load_elf(self, elf_file):
        """
        Flash a given elf. As parameter the absolute path to the elf is required.
        """

        # Check if file exist
        if not os.path.exists(elf_file):
            raise Exception(f"Can't find {elf_file}")

        try:
            # Set reset-behavior to halt and reset target to ensure the SW is halted before loading
            self.logger.debug("start loading elf...")
            self.execute_t32_command("SYStem.Option RESetBehavior halt")
            self.execute_t32_command("SYSTEM.RESETTARGET")
            # Loading given elf with /NOCODE option as no file debugging is required for the API
            self.execute_t32_command("Break")
            area_win_message = self.execute_t32_command(f"data.load.elf {elf_file} /NOCODE /GHS")
            self.logger.debug(f"Routine load_elf() fished successfully with message: '{area_win_message}'")

        # Error handling in case the upper calls through an exception
        except Exception as fetched_ex:
            raise Exception(f"[E] Routine load_elf() failed with error: '{fetched_ex}'")

    def reset(self, mode, behavior):
        """
        Reset the target and the debuger interface based on the given mode and behavior.
        For further details about modes and behavior: check Trace32 manual
        """

        # Defining allowed options for reset mode and behavior
        allowed_modes = ["SYS", "PORST", "EPORST", "APP"]
        allowed_behavior = ["Halt", "RestoreGo", "RunRestore"]

        # Check passed parameters are in the allowed options
        if mode not in allowed_modes:
            raise Exception(f"parameter '{mode}' is not in '{allowed_modes}'")
        if behavior not in allowed_behavior:
            raise Exception(f"parameter '{behavior}' is not in '{allowed_behavior}'")

        # Setting the mode and behavior and executing target reset (similar to system.up and register.reset)
        try:
            self.logger.debug(f"trigger target reset -{mode}- and {behavior}...")
            self.execute_t32_command(f"SYStem.Option ResetMode {mode}")
            self.execute_t32_command(f"SYStem.Option RESetBehavior {behavior}")
            self.execute_t32_command(f"SYSTEM.RESETTARGET")
            if behavior in ["RestoreGo", "RunRestore"]:
                self.execute_t32_command("GO")
            self.logger.debug(f"target reset done")

        # Error handling in case the the upper calls through an exception
        except Exception as fetched_ex:
            raise Exception(f"[E] Routine reset() failed with error: '{fetched_ex}'")

    def get_variable_info(self, variable):
        """
        Read a variable information by a given symbol name and returns addr, size and access type in the given order
        """
        # Defining the return values
        vaddr = ctypes.c_int32(0)
        vsize = ctypes.c_int32(0)
        vaccess = ctypes.c_int32(0)
        self.logger.debug(f"Reading info of {variable}")
        rc = self.api.T32_GetSymbol(variable.encode("ascii"), ctypes.byref(vaddr), ctypes.byref(vsize), ctypes.byref(vaccess))
        self.logger.debug(f"vaddr: {vaddr}, vsize: {vsize}, vaccess: {vaccess}")
        # Reaction based on result status
        if rc == 0:
            if vaddr == -1 and vsize == -1:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to access error (e.g. symbol does not exist)")
            else:
                return {'vaddr': vaddr, 'vsize': vsize, 'vaccess': vaccess}
        else:
            raise Exception(f"[E] Reading variable: '{variable}' not possible due to a communication error")

    def get_variable_value(self, variable, isUnsigned = False):
        """
        Read a variable by a given symbol name and returns higher and lower 32bit separately
        """
        # Defining the return values
        if isUnsigned == True:        
            vvalue = ctypes.c_uint32(0)
            vvalueh = ctypes.c_uint32(0)
        else :
            vvalue = ctypes.c_int32(0)
            vvalueh = ctypes.c_int32(0)

        self.logger.debug(f"Reading value of {variable}")
        rc = self.api.T32_ReadVariableValue(variable.encode("ascii"), ctypes.byref(vvalue), ctypes.byref(vvalueh))
        self.logger.debug(f"vvalue= {vvalue}, vvalueh= {vvalueh}")

        # Reaction based on result status
        if rc == 0:
            self.logger.debug(f"Lower 4 byte value: {vvalue}, upper 4 byte value: {vvalueh}")
            return {'vvalue': vvalue, 'vvalueh': vvalueh}
        else:
            if rc < 0:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a communication error")
            else:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a access error (e.g. symbol does not exist)")

    def set_variable_value(self, variable, value, valueh):
        """
        Sets a variable by a given symbol name. Parameters: lower and higher 32bit wide value
        """
        # Defining the return values
        vvalue = ctypes.c_int32(value)
        vvalueh = ctypes.c_int32(valueh)

        self.logger.debug(f"vvalue= {vvalue}, vvalueh= {vvalueh}")

        rc = self.api.T32_WriteVariableValue(variable.encode("ascii"), vvalue, vvalueh)

        # Reaction based on result status
        if rc == 0:
            self.logger.debug(f"Writing Lower 4 byte value: {value}, upper 4 byte value: {valueh} to {variable} is done")
        else:
            if rc < 0:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a communication error")
            else:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a access error (e.g. symbol does not exist)")
    
    def get_variable_value_as_string(self, variable):
        """
        Read a variable by a given symbol name and returns higher and lower 32bit saperatly
        """
        
        string = ctypes.create_string_buffer(256)
        size = ctypes.c_int32(256)
        self.logger.debug(f"Reading value of {variable}") 
        rc = self.api.T32_ReadVariableString(variable.encode("ascii"), string, ctypes.byref(size))

        # Reaction based on result status
        if rc == 0:
            self.logger.debug(f"value: {string.strip(string.value)}")
            return {string.value}
        else:
            if rc < 0:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a communication error")
            else:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a access error (e.g. symbol does not exist)")

    def set_variable_value_as_string(self, variable, value):
        """
        Sets a variable by a given symbol name. Parameters: lower and higher 32bit wide value
        """
        string = ctypes.create_string_buffer(256)
        string.value = value
        self.logger.debug(f"Writing value= {string.strip(string.value)} to {variable}......")
        rc = self.api.T32_WriteVariableString(variable.encode("ascii"), string)
        # Reaction based on result status
        if rc == 0:
            self.logger.debug(f"Writing value: {value} to {variable} is done")
        else:
            if rc < 0:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a communication error")
            else:
                raise Exception(f"[E] Reading variable: '{variable}' not possible due to a access error (e.g. symbol does not exist)")
    
    def get_state(self):
        """
        Returns the state of the target (running/ halt / down / up)
        """
        # Defining the return value
        trace32State = ctypes.c_int16(-1)

        self.logger.debug(f"Reading state of ICE/ICD of Trace32")
        rc = self.api.T32_GetState(ctypes.byref(trace32State)) #int T32_GetState (int *pstate);                              
                
        # Reaction based on result status
        # 0 for ok, otherwise Error value. Note that pstate is not modified if an error has occurred.
        if rc == 0:
            self.logger.debug(f"state= {trace32State}")
            return ETrace32State(trace32State.value)
        else:
            raise Exception(f"[E] Getting Trace32 state not possible due to a communication error")
    