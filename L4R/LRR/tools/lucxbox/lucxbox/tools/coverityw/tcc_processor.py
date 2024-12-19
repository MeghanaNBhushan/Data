#!/usr/bin/python
""" coverity tcc processor """

import os
import sys
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.coverityw.process import run_command

LOGGER = lucxlog.get_logger()


class TccProcessor:

    """TCC Processor for Coverity module"""

    def __init__(self, tcc_configuration):
        self.tcc_configuration = tcc_configuration

    def install_xml(self):
        LOGGER.info('Calling TCC tools deploy for XML %s',
                    self.tcc_configuration.xml)

        if not os.path.isfile(self.tcc_configuration.path):
            LOGGER.error(
                'TCC tool scripting not found or user do not have access to it: %s', self.tcc_configuration.path)
            sys.exit(1)

        if not os.path.isfile(self.tcc_configuration.xml):
            LOGGER.error(
                'TCC XML not found or user do not have access to it: %s', self.tcc_configuration.xml)
            sys.exit(1)

        command = '{invoker} {tcc_script} {xml}'.format(
            invoker=self.tcc_configuration.invoker,
            tcc_script=self.tcc_configuration.path,
            xml=self.tcc_configuration.xml)
        run_command(command)

    def check_tool_dir(self, tcc_tool_name):
        LOGGER.info('Discovering latest version of %s', tcc_tool_name)

        temp_path = tempfile.mkdtemp()
        temp_file_name = os.path.join(
            temp_path, 'TCCPATH_{}.txt'.format(tcc_tool_name))
        command = '{invoker} {tcc_script} -GetLocalToolPath {tool} -ToolPathFile {file} -XmlFile {xml}'.format(
            invoker=self.tcc_configuration.invoker,
            tcc_script=self.tcc_configuration.path,
            xml=self.tcc_configuration.xml,
            file=temp_file_name,
            tool=tcc_tool_name)
        run_command(command)

        LOGGER.debug('Openning file: %s', temp_file_name)
        with open(temp_file_name, 'r') as temp_file:
            path = temp_file.read().strip()
        LOGGER.debug('Path discovered: %s', path)

        os.remove(temp_file_name)
        os.removedirs(temp_path)
        return path
