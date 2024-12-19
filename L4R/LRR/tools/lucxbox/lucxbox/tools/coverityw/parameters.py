#!/usr/bin/python
""" coverity parameters checker and wrapper object """

import configparser
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.coverityw.compiler_coverity_configuration import CompilerCoverityConfiguration
from lucxbox.tools.coverityw.coverity_configuration import CoverityConfiguration
from lucxbox.tools.coverityw.tcc_configuration import TccConfiguration

LOGGER = lucxlog.get_logger()


class Parameters:

    """Aggregate and check file and user parameters"""

    def __init__(self, config_file, output_dir, build_command, user_name, user_password):
        LOGGER.info('Loading configuration')
        LOGGER.debug('Checking if configuration file exists: %s', config_file)
        if not os.path.isfile(config_file):
            LOGGER.error(
                'Config file does not exist or running user without permissions to open it: %s', config_file)
            sys.exit(1)

        LOGGER.debug('Parsing configuration')
        config = configparser.ConfigParser()
        config.read(config_file)
        sections = config.sections()

        LOGGER.debug('Checking configuration sections')
        if ('COVERITY' not in sections) or ('TCC' not in sections):
            LOGGER.error(
                'Config file not correct. Please check the documentation.')
            sys.exit(1)

        self.coverity_configuration = CoverityConfiguration()
        self.compiler_configuration = CompilerCoverityConfiguration()
        self.tcc_configuration = TccConfiguration()

        self.set_credentials(user_name, user_password)
        self.set_coverity_parameters(config['COVERITY'], output_dir)
        self.set_compiler_parameters(config['COVERITY'], build_command)
        self.set_tcc_parameters(config['TCC'])

        LOGGER.debug('Parameters collected: %s', self)

    def set_credentials(self, user_name, user_password):
        if 'COV_USER' in os.environ:
            self.user_name = os.environ['COV_USER']
        if 'COVERITY_PASSPHRASE' in os.environ:
            self.user_password = os.environ['COVERITY_PASSPHRASE']
        if user_name is not None:
            self.user_name = user_name
        if user_password is not None:
            self.user_password = user_password
        if self.user_name is None or self.user_password is None:
            LOGGER.error(
                'No user name or password set, either via environment variables or parameters.')
            sys.exit(1)

    def set_coverity_parameters(self, cov_config, output_dir):
        LOGGER.debug('Getting COVERITY section arguments')

        self.coverity_configuration.output_dir = output_dir
        self.coverity_configuration.dir = cov_config['CoverityDir']
        self.coverity_configuration.port = cov_config['CoverityPort']
        self.coverity_configuration.host = cov_config['CoverityServerName']
        self.coverity_configuration.stream = cov_config['CoverityStreamName']
        self.coverity_configuration.analyze_options = cov_config['CoverityAnalyzeOpts']

        for i in range(10):
            filter_name = 'FilterFilePattern{index}'.format(index=i)
            if filter_name in cov_config:
                self.coverity_configuration.filter.append(
                    cov_config[filter_name])

    def set_compiler_parameters(self, cov_config, build_command):
        self.compiler_configuration.build_command = build_command
        self.compiler_configuration.path = cov_config['CompilerPath']
        self.compiler_configuration.build_args = cov_config['CoverityBuildAditionalArgs']

        for i in range(10):
            config_name = 'CompilerConfigArgs{index}'.format(index=i)
            if config_name in cov_config:
                self.compiler_configuration.configs.append(
                    cov_config[config_name])

    def set_tcc_parameters(self, tcc_config):
        LOGGER.debug('Getting TCC section arguments')
        self.tcc_configuration.use_tcc = tcc_config.getboolean('UseTccTools')
        self.tcc_configuration.compiler_tool_name = tcc_config['CompilerToolName']
        self.tcc_configuration.compiler_relative_path = tcc_config['CompilerRelativePath']
        self.tcc_configuration.path = tcc_config['TccScriptPath']
        self.tcc_configuration.xml = tcc_config['TccXMLConfigPath']
        self.tcc_configuration.install = tcc_config.getboolean('TccInstallXML')
        self.tcc_configuration.invoker = tcc_config['TccInvoker']
