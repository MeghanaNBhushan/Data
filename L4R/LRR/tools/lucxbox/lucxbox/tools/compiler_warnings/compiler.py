""" CompilerBase Class """
import sys
import os
import glob
import re
from multiprocessing.pool import ThreadPool

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()


class CompilerBase:
    """ CompilerBase class """

    def __init__(self, name, regex, regex_unknown_warning=None, multiline_regex=False, warning_id_regex=None, linker_warning_regex=None):
        self.name = name
        self.compiled_regex = re.compile(regex)
        self.multiline_regex = multiline_regex
        if regex_unknown_warning:
            self.compiled_regex_unknown_warning = re.compile(regex_unknown_warning)
        else:
            self.compiled_regex_unknown_warning = regex_unknown_warning
        if warning_id_regex:
            self.warning_id_regex = re.compile(warning_id_regex)
        else:
            self.warning_id_regex = warning_id_regex
        if linker_warning_regex:
            self.compiled_regex_linker_warning = re.compile(linker_warning_regex)
        else:
            self.linker_warning_regex = linker_warning_regex

    def __str__(self):
        return self.name

    def get_warnings_from_file(self, file_pattern, number_of_threads, filemapping):
        """ Function to extract all warnings from a given file

            Return value:
            A list with entries of the type CompilerWarning

            Arguments:
            file_pattern - the file pattern of the compiler log to extract warnings from
            number_of_threads - how many number_of_threads to use to extract warnings from file_pattern
                   NOTE: for some compilers (like greenhills) it's not possible to extract
                   all kind of information of a warning from one line and therefore it is quite hard
                   to divide the file into chunks and put them into threads.
                   Instead, the whole file-content needs to be searched, which can take some time depending on
                   the size of the compiler log
            filemapping - a dictionary with file and path mapping used in linker warning for compilers (like greenhills)
                   NOTE: As the file path cannot be extracted from the warning message in linker warnings this parameter is used
        """

        expanded_file_names = glob.glob(file_pattern)
        if len(expanded_file_names) > 1:
            LOGGER.error("Filename has more than one match: '%s'",
                         str(expanded_file_names))
            sys.exit(-1)
        elif not expanded_file_names:
            LOGGER.error("Filename not found: '%s'", str(file_pattern))
            sys.exit(-1)

        file_name = expanded_file_names[0]

        LOGGER.debug("Trying to extract warnings from file '%s' and compiler type of '%s'", file_name, self.name)
        warnings = []
        LOGGER.debug("Reading file")
        with open(file_name, 'r') as compiler_logfile:
            compiler_log_lines = compiler_logfile.readlines()
            LOGGER.debug("File has '%d' lines", len(compiler_log_lines))
        LOGGER.debug("Finished reading file")

        if self.multiline_regex:
            LOGGER.warning(
                "Compiler '%s' does not support thread analysis because regex is multiline", self.name)
            LOGGER.warning("'number_of_threads' argument has no effect")
            warnings = self.get_warnings_from_lines(
                [''.join(compiler_log_lines)], filemapping)
        else:
            line_chunks = chunkify(compiler_log_lines, number_of_threads)
            thread_pool = ThreadPool(number_of_threads)

            threads = []
            LOGGER.debug(
                "Spawning '%d' threads for compiler log parsing", number_of_threads)
            for i in range(0, number_of_threads):
                threads.append(thread_pool.apply_async(
                    self.get_warnings_from_lines, (line_chunks[i],)))

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
        number_of_chunks - integer value of in how many parts the lst should be divided into
    """
    return [lst[i::number_of_chunks] for i in range(number_of_chunks)]
