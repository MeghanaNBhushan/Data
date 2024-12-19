""" Store and load last run info """
import hashlib
import json
import os
import platform
import sys
import time
import atomicwrites

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog

HashAlgorithm = hashlib.md5

LOGGER = lucxlog.get_logger()


def get_file_name():
    return os.path.join(os.path.expanduser("~"), ".tccw")


def store_data(env, tcc_configuration):
    '''
    Store data about last run
    '''
    if not os.path.isfile(tcc_configuration.get('tccxmlconfigpath')):
        return

    with open(tcc_configuration.get('tccxmlconfigpath'), 'r') as config_file:
        if "<Mirror>Yes</Mirror>" in config_file.read():
            LOGGER.info("Not caching env since mirror feature used.")
            return

    data = load_data()
    if not data:
        data = {}

    config_hash = get_file_hash(tcc_configuration.get('tccxmlconfigpath'),
                                get_additional_data())
    data[config_hash] = env

    file_name = get_file_name()
    with atomicwrites.atomic_write(file_name, overwrite=True) as data_file:
        retries = 5
        for i in range(retries):
            try:
                data_file.write(json.dumps(data))
                break
            except OSError as perror:
                LOGGER.warning("Try #%d PermissionError while writing '%s'", retries, file_name)
                if i == retries - 1:
                    raise perror
                time.sleep(1)


def load_data():
    '''
    Load data about last run
    '''
    file_name = get_file_name()
    try:
        with open(file_name, 'r') as json_file:
            if sys.version_info > (3, 0, 0):
                data = json.loads(json_file.read())
            else:
                data = json_file.read()
        return data
    except IOError:
        return None


def get_env_from_cache(tcc_configuration):
    '''
    Check if last tcc run was in the last 24h
    '''
    if not os.path.isfile(tcc_configuration.get('tccxmlconfigpath')):
        return None

    data = load_data()
    if data:

        config_hash = get_file_hash(tcc_configuration.get('tccxmlconfigpath'),
                                    get_additional_data())
        if data.get(config_hash):
            return data[config_hash]
    return None


def get_additional_data():
    return platform.node() + platform.system() + platform.version()


def get_file_hash(file_path, additional_data=None):
    hasher = HashAlgorithm()
    with open(file_path, 'rb') as in_file:
        hasher.update(in_file.read())
    if additional_data is not None:
        # Encoding of this additional data does not really matter
        # as long as we keep it fixed, otherwise hashes change.
        # The string should fit into ASCII, so UTF8 should not change anything
        hasher.update(additional_data.encode("UTF-8"))
    return hasher.hexdigest()
