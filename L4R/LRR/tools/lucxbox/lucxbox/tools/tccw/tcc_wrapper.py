"""Helper function for tcc wrapper"""

import os
import subprocess
import sys
import platform
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxutils
from lucxbox.tools.tccw.tcc_cache import get_env_from_cache, get_file_name, store_data

LOGGER = lucxlog.get_logger()
TCC_INIT = {"Windows": "C:/TCC/Tools/tcc_init"}


class TccError(Exception):
    def __init__(self, message, returncode):
        self.returncode = returncode
        Exception.__init__(self, message)


# This will add env variables create in "cmd" to exec_env
def setenv(exec_env, cmd):      # pragma: windows only
    keyword = "~~~~START_ENVIRONMENT_HERE~~~~"
    LOGGER.debug("Get environment from '%s'", cmd)
    cmd = cmd + ' && echo {} && set'.format(keyword)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=exec_env)
    out, _ = process.communicate()
    cli_output = out.decode('utf-8').splitlines()
    LOGGER.info(' \n'.join(cli_output))
    key_word_reached = False
    for line in cli_output:
        if key_word_reached:
            env_var = line.strip().split('=')
            exec_env[env_var[0]] = env_var[1]
        elif line.strip() == keyword:
            key_word_reached = True


# This function returns the environment variables after executing the TCC init.bat file
# The TCC init.bat redefines TCC env vars with generic names, e.g. 'CMAKE_EXE', so they can be used by build scripts
def init_tcc(tcc_configuration, no_install=False, exec_env=None):       # pragma: windows only
    if exec_env is None:
        exec_env = dict()
    version = tcc_configuration.get_version()
    if not no_install and tcc_configuration.get('tccinstall'):
        install_env(tcc_configuration)
    init_cmd = os.path.abspath("{}/{}/init.bat".format(TCC_INIT[platform.system()], version))
    # The following 4 env vars need to be set for init batch
    # If BUILD_DIR ist provided the TCC setup batch files will be created in there
    if 'BUILD_DIR' not in exec_env:
        LOGGER.warning("BUILD_DIR is not set in environment. Using temp directory!")
        exec_env['BUILD_DIR'] = tempfile.gettempdir()
        if not os.path.exists(exec_env['BUILD_DIR']):
            os.mkdir(exec_env['BUILD_DIR'])
    tcc_command = tcc_configuration.get_invoker() + ' -file ' + tcc_configuration.get_script_path()
    exec_env["TCC_COMMAND"] = tcc_command
    exec_env["TOOLCOLLECTION"] = version
    exec_env["TOOLCOLLECTION_XML"] = tcc_configuration.get_xml()
    setenv(exec_env, init_cmd)
    return exec_env


def run_tcc(tcc_configuration, no_install=False, no_cache=False):
    if not no_cache:
        cached_env = get_env_from_cache(tcc_configuration)
        if cached_env:
            LOGGER.info("Reading TCC env from cache")
            return cached_env

    if (not no_install and tcc_configuration.get('tccinstall')):
        install_env(tcc_configuration)
    env = get_env(tcc_configuration)
    return env


def install_env(tcc_configuration):
    """Installs all tools of the given tool collection"""
    tccxmlconfigpath = tcc_configuration.get('tccxmlconfigpath')
    LOGGER.info('Calling TCC tools deploy for XML %s', tccxmlconfigpath)

    invoker = tcc_configuration.get('tccinvoker')
    if not lucxutils.which(invoker) and not lucxutils.which(invoker + ".exe"):
        LOGGER.error("TCC invoker is not an executable: '%s'", invoker)
        sys.exit(1)

    tccscriptpath = tcc_configuration.get('tccscriptpath')
    if not os.path.isfile(tccscriptpath):
        LOGGER.error(
            "TCC tool scripting not found or user do not have access to it: '%s'", tccscriptpath)
        LOGGER.error(
            "This software requires TCC. If you do not have TCC on your machine yet, please get it from ismInstaller."
            "The package name is: 'TCC - ToolCollection for CC'.")
        sys.exit(1)

    command = [invoker,
               '-ExecutionPolicy', 'Bypass',  # INFO(fub2lr) Due to BTS-4216
               tccscriptpath,
               tccxmlconfigpath]
    safe_process(command)


def get_env(tcc_configuration):
    """Get an environment dict for all tools in the tool collection"""
    # tcc powershell will fail if only a filename is given
    # to fix it we start with ./
    tool_path_makefile = os.path.join('.', 'ToolPaths.make')
    command = [tcc_configuration.get('tccinvoker'),
               '-ExecutionPolicy', 'Bypass',  # INFO(fub2lr) Due to BTS-4216
               tcc_configuration.get('tccscriptpath'),
               tcc_configuration.get(
                   'tccxmlconfigpath'), "-GenerateToolPathMk",
               tool_path_makefile]
    safe_process(command)
    env = lucxutils.get_env_from_file(tool_path_makefile)
    os.remove(tool_path_makefile)
    store_data(env, tcc_configuration)
    return env


def execute(command, env):
    temp_env = os.environ
    temp_env.update(env)
    LOGGER.debug("Calling command: %s", command)
    if not command:
        LOGGER.error(
            "Trying to call empty command. See help message for usage.")
        sys.exit(1)

    expanded_command = []
    for entry in command:
        expanded_command.append(os.path.expandvars(entry))

    cmd = expanded_command[0]
    if not lucxutils.which(cmd) and not lucxutils.which(cmd + ".exe"):
        LOGGER.error("Can not find executable: '%s'", cmd)
        LOGGER.error("Common problem is a broken tccw cache. Please delete '%s' and run again.", get_file_name())
        sys.exit(1)
    try:
        subprocess.check_call(expanded_command, env=temp_env, shell=True)
    except subprocess.CalledProcessError as exception:
        LOGGER.error("Exception occured: %s", str(exception))
        sys.exit(exception.returncode)


def safe_process(command):
    LOGGER.debug("Command: %s", command)
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=sys.stdout.fileno())
    out, err = process.communicate()
    returncode = process.returncode
    if returncode != 0:
        if err is not None:
            print(err.decode("utf-8"))
        if out is not None:
            print(out.decode("utf-8"))
        raise TccError(
            "Error while running TCC script: Command '{}' returned non-zero exit status".format(
                command), returncode
        )
    LOGGER.debug("Output: %s", out)
