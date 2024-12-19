"""
PRQA Installation helper class
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxutils

LOGGER = lucxlog.get_logger()


class PrqaInstallation:
    """Helper class containing information concerning the local PRQA installation"""

    def __init__(self, path_prqa):
        if path_prqa:
            self._home = path_prqa
            self._path_to_qacli = self.get_qacli_path(path_prqa)
        else:
            self._home = "C:\\tools\\"
            self._path_to_qacli = None
            self.setup_cli()

        self.check_licenses()

    @property
    def cli(self):
        return self._path_to_qacli

    @property
    def home(self):
        return self._home

    def setup_cli(self):
        """This method sets up the CLI as it initializes the prqa home and checks the cli_path."""

        try:
            home = os.environ['PRQA_HOME']
            self._home = home
        except KeyError:
            LOGGER.warning("'PRQA_HOME' environment variable not existing. Using default path C:\\Tools\\")
            home = self._home

        if not os.path.exists(home):
            LOGGER.critical("'PRQA_HOME' environment variable existing but content path does not exist.")
            sys.exit(-11)

        path_to_qacli = self.get_qacli_path(home)

        if not os.path.exists(path_to_qacli):
            LOGGER.critical("'%s' is not existing.", path_to_qacli)
            sys.exit(-12)

        self._path_to_qacli = path_to_qacli

    @staticmethod
    def get_qacli_path(prqa_path):
        """
        Get the os-dependent path to teh prqa executable

        :param prqa_path: The root path to the PRQA installation
        :return: The path to the qacli executable
        """
        if os.name == "nt":
            exe_name = 'qacli.exe'
        else:
            exe_name = 'qacli'
        path_to_exe = os.path.abspath(os.path.join(prqa_path, 'common', 'bin', exe_name))
        return path_to_exe

    def check_licenses(self):
        """
        Check license servers and licenses themselves
        """
        cmd_check_prqa_version = self.cli + ' --version'
        cmd_check_servers = self.cli + ' admin --list-license-servers'
        cmd_check_licenses = self.cli + ' admin --check-license'

        for cmd in [cmd_check_prqa_version, cmd_check_servers, cmd_check_licenses]:
            out, _, code = lucxutils.execute(cmd)
            if "not available" in out.lower():
                LOGGER.warning("One or more components were found to be \"Not Available\" required by the project!\n%s", out)
            if "none" in out:
                LOGGER.critical("Error: no license server name received for this command (none configured?) '%s'", cmd)
                sys.exit(-12.1)
            if code != 0:
                LOGGER.critical("License check exited with code %s. Error happened during execution of command '%s'", code, cmd)
                sys.exit(-12.2)
