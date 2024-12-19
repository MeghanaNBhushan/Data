""" CompilerBase Class """
import glob
import re

from os.path import splitext
from io import TextIOWrapper
from abc import ABC, abstractmethod
from multiprocessing.pool import ThreadPool
from sys import exit as sys_exit
from zipfile import BadZipFile, ZipFile

from swq.common.filesystem.filesystem_utils import open_t
from swq.common.logger import LOGGER
from swq.common.return_codes import log_and_exit, \
    RC_INVALID_OR_CORRUPTED_COMPRESSED_FILE


class CompilerBase(ABC):
    """ CompilerBase abstract base class """
    def __init__(self,
                 name,
                 regex,
                 regex_unknown_warning=None,
                 multiline_regex=False,
                 warning_id_regex=None,
                 linker_warning_regex=None):
        self.name = name
        self.compiled_regex = re.compile(regex)
        self.multiline_regex = multiline_regex
        if regex_unknown_warning:
            self.compiled_regex_unknown_warning = re.compile(
                regex_unknown_warning)
        else:
            self.compiled_regex_unknown_warning = regex_unknown_warning
        if warning_id_regex:
            self.warning_id_regex = re.compile(warning_id_regex)
        else:
            self.warning_id_regex = warning_id_regex
        if linker_warning_regex:
            self.compiled_regex_linker_warning = re.compile(
                linker_warning_regex)
        else:
            self.linker_warning_regex = linker_warning_regex

    def __str__(self):
        return self.name

    @abstractmethod
    def get_warnings_from_lines(self, lines, filemapping):
        """
        Extracts warnings from log lines and returns list of CompilerWarnings
        """

    def _get_compiler_logs_from_zip(self, file_name):
        compiler_log_lines = []
        try:
            with ZipFile(file_name) as logs_zip_file:
                files_in_zip = logs_zip_file.namelist()
                if len(files_in_zip) != 1:
                    LOGGER.error(
                        "%s file is empty or contains more than one file",
                        file_name)
                    log_and_exit(RC_INVALID_OR_CORRUPTED_COMPRESSED_FILE)
                with logs_zip_file.open(files_in_zip[0]) as compiler_logfile:
                    compiler_log_lines.extend(
                        TextIOWrapper(compiler_logfile).readlines())
        except BadZipFile as zip_exception:
            LOGGER.error(zip_exception)
            log_and_exit(RC_INVALID_OR_CORRUPTED_COMPRESSED_FILE)

        return compiler_log_lines

    def get_warnings_from_file(self, file_pattern, number_of_threads,
                               filemapping):
        """ Function to extract all warnings from a given file

            Return value:
            A list with entries of the type CompilerWarning

            Arguments:
            file_pattern - the file pattern of the compiler log to extract
                           warnings from
            number_of_threads - how many number_of_threads to use to extract
                                warnings from file_pattern
                   NOTE: for some compilers (like greenhills) it's not possible
                   to extract all kind of information of a warning from one
                   line and therefore it is quite hard to divide the file into
                   chunks and put them into threads. Instead, the whole
                   file-content needs to be searched, which can take some time
                   depending on the size of the compiler log
            filemapping - a dictionary with file and path mapping used in
                          linker warning for compilers (like greenhills)
                   NOTE: As the file path cannot be extracted from the warning
                   message in linker warnings this parameter is used
        """

        expanded_file_names = glob.glob(file_pattern)
        if len(expanded_file_names) > 1:
            LOGGER.error("Filename has more than one match: '%s'",
                         str(expanded_file_names))
            sys_exit(-1)
        elif not expanded_file_names:
            LOGGER.error("Filename not found: '%s'", str(file_pattern))
            sys_exit(-1)

        file_name = expanded_file_names[0]

        LOGGER.debug(
            "Trying to extract warnings from file '%s' and compiler"
            "type of '%s'", file_name, self.name)
        warnings = []
        LOGGER.debug("Reading file")
        if splitext(file_name)[1] == '.zip':
            compiler_log_lines = self._get_compiler_logs_from_zip(file_name)
        else:
            with open_t(file_name) as compiler_logfile:
                compiler_log_lines = compiler_logfile.readlines()

        LOGGER.debug("File has '%d' lines", len(compiler_log_lines))
        LOGGER.debug("Finished reading file")

        if self.multiline_regex:
            LOGGER.warning(
                "Compiler '%s' does not support thread analysis because regex "
                "is multiline", self.name)
            LOGGER.warning("'number_of_threads' argument has no effect")
            warnings = self.get_warnings_from_lines(
                [''.join(compiler_log_lines)], filemapping)
        else:
            line_chunks = chunkify(compiler_log_lines, number_of_threads)
            thread_pool = ThreadPool(number_of_threads)

            threads = []
            LOGGER.debug("Spawning '%d' threads for compiler log parsing",
                         number_of_threads)
            for i in range(0, number_of_threads):
                threads.append(
                    thread_pool.apply_async(self.get_warnings_from_lines,
                                            (line_chunks[i], )))

            for thread in threads:
                warnings += thread.get()

            thread_pool.close()
            thread_pool.join()

        return warnings


def chunkify(lst, number_of_chunks):
    """ Helper function to divide a given list into equally sized chunks

        Return value:
        A list of lists, containing the chunkyfied initial list

        Arguments:
        lst - the input list of entries any kind
        number_of_chunks - integer value of in how many parts the lst should be
        divided into
    """
    return [lst[i::number_of_chunks] for i in range(number_of_chunks)]
