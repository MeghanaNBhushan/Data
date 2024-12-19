""" Different util functions """

import os
import shutil
import subprocess
import threading
import hashlib
from multiprocessing import Queue
from multiprocessing.pool import ThreadPool
from zipfile import ZipFile

try:
    from zipfile import BadZipFile
except ImportError:
    from zipfile import BadZipfile as BadZipFile  # deprecated since Python 3.2 in favour of the above

from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

def which(program):
    """ Command line 'which' like python method """
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def chunkify(lst, number_of_chunks):
    """ Helper function to divide a given list into equally sized chunks

        Return value:
        A list of lists, containing the chunkyfied initial list

        Arguments:
        lst - the input list of entries any kind
        number_of_chunks - integer value of in how many parts the lst should be divided into
    """
    return [lst[i::number_of_chunks] for i in range(number_of_chunks)]


# pylint: disable=simplifiable-if-statement, too-many-branches, too-many-locals, too-many-arguments, too-many-statements
def execute(cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            continuous_output_callback=None,
            env=None, cwd=None, encoding='latin1'):
    """ Wrapper for subprocess Popen to support python 2.7 and 3 return values """
    if not cwd:
        cwd = os.getcwd()

    def distinguish_shell_output(line_buffer, is_err) -> bool:
        if line_buffer[:1] == "+":
            return False
        else:
            return is_err

    def read_in_thread(is_err, pipe, queue):
        line_buffer = ''

        try:
            with pipe:
                while True:
                    bin_data = pipe.read(1)
                    if bin_data == b'':
                        break

                    data = bin_data.decode(encoding, errors='ignore')

                    line_buffer += data
                    if '\n' in line_buffer:
                        split = line_buffer.split('\n')
                        line_buffer = split[0].replace('\r', '')
                        queue.put((distinguish_shell_output(line_buffer, is_err), line_buffer))
                        line_buffer = split[1]

        finally:
            queue.put((is_err, None))

    LOGGER.debug("Executing '%s'", cmd)
    process = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, shell=shell, env=env, cwd=cwd)

    if continuous_output_callback is None:
        out, err = process.communicate()
        if out is not None:
            out = out.decode(encoding)
        if err is not None:
            err = err.decode(encoding)
        returncode = process.returncode
    else:
        queue = Queue()
        threading.Thread(target=read_in_thread, args=[False, process.stdout, queue]).start()
        threading.Thread(target=read_in_thread, args=[True, process.stderr, queue]).start()

        out = ''
        out_closed = False
        err = ''
        err_closed = False

        for is_err, line in iter(queue.get, None):
            if line is None:
                if is_err:
                    err_closed = True
                else:
                    out_closed = True

                if out_closed and err_closed:
                    break
            else:
                if is_err:
                    err += line + '\n'
                else:
                    out += line + '\n'

                continuous_output_callback(is_err, line)

        returncode = process.poll()
        while returncode is None:
            returncode = process.poll()

    return out, err, returncode


def parallel_execute(cmds, threads):
    """ Function to execute multiple commands in parallel and get results as dictionary """
    cmds_to_execute = Queue()
    result = {}  # used to store the results
    for cmd in cmds:
        cmds_to_execute.put(cmd)

    def worker():
        while True:
            cmd = cmds_to_execute.get()
            if cmd is None:  # EOF?
                return
            key = ' '.join(cmd)
            try:
                result[key] = execute(cmd)
            except OSError as exception:
                message = "Exception occurred executing '" + key + "': OSError: " + str(exception)
                result[key] = "", message, 1

    threads = [threading.Thread(target=worker) for _i in range(threads)]
    for thread in threads:
        thread.start()
        cmds_to_execute.put(None)  # one EOF marker for each thread
    for thread in threads:
        thread.join()
    return result


def get_env_from_file(file_path):
    """ Function to read in a dictionary of environment variables from a file
        similar to the unix command 'env' format, e.g.:
        KEY=VALUE
    """
    with open(file_path, 'r') as envfile:
        envfile_content = envfile.readlines()

    env = {}
    for line in envfile_content:
        tool, path = line.split("=")
        tool, path = tool.strip(), path.strip()
        env[tool] = path
    return env


def clear_os_environ():
    """ Function to clear the os environ and only keep system environment variables """
    keep = ['ALLUSERSPROFILE', 'ACLOCAL_PATH', 'ALLUSERSPROFILE', 'APPDATA', 'COMMONPROGRAMFILES', 'COMPUTERNAME', \
    'COMSPEC', 'CONFIG_SITE', 'COMMONPROGRAMFILES(X86)', 'COMMONPROGRAMW6432', 'DISPLAY', 'DRIVERDATA', \
    'EXEPATH', 'HOME', 'HOMEDRIVE', 'HOMEPATH', 'HOMESHARE', 'HOSTNAME', \
    'INFOPATH', 'LANG', 'LOCALAPPDATA', 'LOGONSERVER', 'LUCX', 'MANPATH', 'MINGW_CHOST', \
    'MINGW_PACKAGE_PREFIX', 'MINGW_PREFIX', 'ML_DP_SERVER_CL', 'ML_DP_SERVER_NG', 'ML_FORK', 'MSYSTEM', \
    'MSYSTEM_CARCH', 'MSYSTEM_CHOST', 'MSYSTEM_PREFIX', 'NUMBER_OF_PROCESSORS', 'OLDPWD', 'ORIGINAL_PATH', \
    'ORIGINAL_TEMP', 'ORIGINAL_TMP', 'OS', 'PATH', 'PATHEXT', 'PC_OS', \
    'PKG_CONFIG_PATH', 'PLINK_PROTOCOL', 'PROCESSOR_ARCHITECTURE', 'PROCESSOR_IDENTIFIER', 'PROCESSOR_LEVEL', 'PROCESSOR_REVISION', \
    'PROGRAMFILES', 'PS1', 'PSMODULEPATH', 'PUBLIC', 'PWD', 'PROGRAMDATA', \
    'PROGRAMFILES(X86)', 'PROGRAMW6432', 'SAPKM_USER_TEMP', 'SESSIONNAME', 'SHELL', 'SHLVL', \
    'SSH_ASKPASS', 'SYSTEMDRIVE', 'SYSTEMROOT', 'TEMP', 'TERM', 'TMP', \
    'TMPDIR', 'UATDATA', 'USERDNSDOMAIN', 'USERDOMAIN', 'USERDOMAIN_ROAMINGPROFILE', 'USERNAME', \
    'USERPROFILE', 'WINDIR']
    for key in list(os.environ.keys()):
        if key not in keep:
            del os.environ[key]


def zipfile_extractall_subdirectory(file_, path, subdirectory_prefix):
    with ZipFile(str(file_)) as zipfile:
        files_in_zipfile = zipfile.namelist()
        if any(not filename.startswith(subdirectory_prefix) for filename in files_in_zipfile):
            raise NoSubDirectoryZipFile
        if not path.exists():
            path.mkdir(parents=True)
        files_in_zipfile_subdirectory = [filename[len(subdirectory_prefix):] for filename in files_in_zipfile if
                                         filename.startswith(subdirectory_prefix)]
        for source_path, target_path in zip(files_in_zipfile, files_in_zipfile_subdirectory):
            LOGGER.debug('Extract %s to %s', source_path, target_path)
            with zipfile.open(str(source_path)) as source, open(str(path / target_path), "wb") as target:
                shutil.copyfileobj(source, target)
    return path


def hash_file(file, large=False, universal_lineendings=True):
    if not os.path.exists(file):
        error_message = "File '{}' to hash does not exist.".format(file)
        error_message += f" Was looking in {os.getcwd()}"
        LOGGER.error(error_message)
        raise FileNotFoundError(error_message)

    blocksize = 65536
    if large:
        LOGGER.debug("Large file hashing using a blocksize of '%d'", blocksize)
    hasher = hashlib.md5()
    with open(file, 'rb') as hash_file:
        if large:
            buf = hash_file.read(blocksize)
        else:
            buf = hash_file.read()
        if universal_lineendings:
            buf = buf.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        if large:
            while buf:
                hasher.update(buf)
                buf = hash_file.read(blocksize)
        else:
            hasher.update(buf)
        hasher.update(buf)
    file_hash = hasher.hexdigest()
    LOGGER.debug("Hash %s:%s", file, file_hash)
    return file_hash


def hash_files(files_to_hash, large=False, universal_lineendings=True):
    files_hashes = ""
    for file_to_hash in files_to_hash:
        files_hashes += hash_file(file_to_hash, large, universal_lineendings)
    return files_hashes


def dir_hash(directory, exclude_file_ext=None, exclude_dirs=None, n_threads=4, exclude_files=None, universal_lineendings=True):
    """
        Return md5 hash of given directory
    """
    if not os.path.exists(directory):
        raise FileNotFoundError

    LOGGER.debug("Hashing directory '%s'", directory)
    hash_concat = ""
    hash_filepaths = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d[0] == '.']
        files[:] = [f for f in files if not f[0] == '.']
        for names in sorted(files):
            if exclude_dirs and any(exclude_dir in os.path.join(root, names) for exclude_dir in exclude_dirs):
                LOGGER.debug("Skipping '%s' (directory excluded)", os.path.join(root, names))
                continue
            if exclude_file_ext:
                if any(os.path.join(root, names).endswith(ending) for ending in exclude_file_ext):
                    LOGGER.debug("Skipping '%s' (extension excluded)", os.path.join(root, names))
                    continue
            if exclude_files:
                if any(os.path.join(root, names) == os.path.normpath(exclude_file) for exclude_file in exclude_files):
                    LOGGER.debug("Skipping '%s' (file explicitly excluded)", os.path.join(root, names))
                    continue
            hash_filepaths.append(os.path.join(root, names))

    hash_concat = get_threaded_hashes(hash_filepaths, n_threads, universal_lineendings)
    return hashlib.md5(hash_concat.encode()).hexdigest()


def get_threaded_hashes(hash_filepaths, n_threads, universal_lineendings=True):
    hash_filepaths_chunks = chunkify(hash_filepaths, n_threads)
    thread_pool = ThreadPool(n_threads)

    threads = []
    LOGGER.debug(
        "Spawning '%d' threads for file hashing", n_threads)
    for i in range(0, n_threads):
        threads.append(thread_pool.apply_async(
            hash_files, (hash_filepaths_chunks[i], False, universal_lineendings)))

    hash_concat = ""
    for thread in threads:
        hash_concat += thread.get()

    thread_pool.close()
    thread_pool.join()

    return hash_concat


def dirs_hash(directories, exclude_file_ext=None, exclude_dirs=None, n_threads=4, exclude_files=None, universal_lineendings=True):
    """
        Hashes a given list of directories
    """
    LOGGER.debug("Hashing directories %s", tuple(directories))
    hash_concat = ""
    for directory in directories:
        hash_concat += dir_hash(directory, exclude_file_ext, exclude_dirs, n_threads, exclude_files, universal_lineendings)
    if len(directories) == 1:
        return hash_concat
    return hashlib.md5(hash_concat.encode()).hexdigest()


class NoSubDirectoryZipFile(BadZipFile):
    pass
