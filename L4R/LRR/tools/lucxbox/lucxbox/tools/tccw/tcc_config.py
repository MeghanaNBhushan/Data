"""Calls that holds tcc wrapper"""

import os
import platform
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxconfig

LOGGER = lucxlog.get_logger()

# Default paths for supported OS
TCC_SCRIPT_PATH = {"Windows": "C:\\TCC\\Base\\InstallToolCollection\\InstallToolCollection.ps1"}
TCC_BASE = {"Windows": "ITO\\TCC\\Base"}
TCC_INVOKER = {"Windows": "C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"}


class TccConfig:
    """TCC Config container class"""

    def __init__(self):
        self.config_file_tcc = None
        self.tcc_config = {}
        self.config_file_tcc = {}
        self.config_file = None

    @staticmethod
    def rchop(string, ending):
        if string.endswith(ending):
            return string[:-len(ending)]
        return string

    def set_local_file(self, config_file):
        self.tcc_config['tccxmlconfigpath'] = os.path.abspath(config_file)
        self.__default_setup__()

    def set_by_value(self, value):
        if platform.system() not in TCC_BASE:
            unsupported_os_error()
        project = None
        try:
            _, project, platform_name, _ = value.split("_")
            project = project.split('-')[0]
            config_file = value + ".xml"
            # Fix for toolcollection name from FVG3. Mistake in the tcc naming convention
            if "FVG3CI" in project:
                project = self.rchop(project, "CI")
        except ValueError:
            LOGGER.info("Cannot read TCC config, trying itc2...")
        if not project:
            try:
                project, version = value.split(":")
                platform_name = platform.system()
                config_file = f"TCC_{project}_{platform_name}_{version}.xml"
            except ValueError:
                LOGGER.error("Invalid value for TCC config '%s'", value)
                sys.exit(1)
        tcc_base = TCC_BASE[platform.system()]
        self.tcc_config['tccxmlconfigpath'] = os.path.join(tcc_base, project, platform_name, config_file)
        self.__default_setup__()

    def set_by_file(self, config_file):
        self.config_file = config_file
        self.__read_configfile__()
        self.__set_xml_config_path__()
        self.__default_setup__()

    def get(self, key):
        return self.tcc_config[key]

    def get_xml(self):
        return self.tcc_config['tccxmlconfigpath']

    def get_version(self):
        if "tccversion" in self.config_file_tcc:
            return self.config_file_tcc["tccversion"]
        else:
            xml_name = os.path.basename(self.tcc_config['tccxmlconfigpath'])
            return os.path.splitext(xml_name)[0]

    def get_script_path(self):
        return self.tcc_config['tccscriptpath']

    def get_invoker(self):
        return self.tcc_config['tccinvoker']

    def __default_setup__(self):
        LOGGER.debug("Checking for missing configuration parameters and setting defaults.")
        self.__set_script_path__()
        self.__set_invoker__()
        self.__set_default_install__()

    def __read_configfile__(self):
        LOGGER.debug("Reading config file '%s'", self.config_file)
        self.config_file_tcc = lucxconfig.parse(LOGGER, self.config_file, "[TCC]")

    def __set_xml_config_path__(self):
        if 'tccxmlconfigpath' in self.config_file_tcc:
            self.tcc_config['tccxmlconfigpath'] = self.config_file_tcc['tccxmlconfigpath']
        else:
            if 'tccconfigdir' not in self.config_file_tcc:
                LOGGER.error("Config file is missing 'TccConfigDir' or 'TccXMLConfigPath' in the 'TCC' section. "
                             "Please check the documentation.")
                sys.exit(1)
            self.tcc_config['tccxmlconfigpath'] = os.path.join(self.config_file_tcc["tccconfigdir"],
                                                               self.config_file_tcc["tccversion"] + ".xml")

    def __set_script_path__(self):
        if 'tccscriptpath' in self.config_file_tcc:
            self.tcc_config['tccscriptpath'] = self.config_file_tcc['tccscriptpath']
        else:
            if platform.system() not in TCC_SCRIPT_PATH:
                unsupported_os_error()
            self.tcc_config['tccscriptpath'] = TCC_SCRIPT_PATH[platform.system()]

    def __set_invoker__(self):
        if 'tccinvoker' in self.config_file_tcc:
            self.tcc_config['tccinvoker'] = self.config_file_tcc['tccinvoker']
        else:
            if platform.system() not in TCC_INVOKER:
                unsupported_os_error()
            self.tcc_config['tccinvoker'] = TCC_INVOKER[platform.system()]

    def __set_default_install__(self):
        if 'tccinstallxml' in self.config_file_tcc:
            self.tcc_config['tccinstall'] = self.config_file_tcc['tccinstallxml'] in ["true", "True"]
        else:
            # by default we want to check for missing tools and install them
            self.tcc_config['tccinstall'] = True


def unsupported_os_error():
    LOGGER.error("OS '%s' not supported. If you have knowledge how TCC is used on your OS please contact the LUCx team", platform.system())
    sys.exit(1)
