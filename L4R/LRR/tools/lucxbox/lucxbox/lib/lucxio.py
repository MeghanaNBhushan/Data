""" Different io functions """

from pathlib import Path

import requests
from tqdm import tqdm

from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()

def download(url, directory, filename, session=None):
    directory_path = Path(directory)
    if not directory_path.exists():
        LOGGER.info('Create directory "%s"', directory_path)
        directory_path.mkdir()
    path = directory_path / filename

    session = session or requests.Session()
    with session.get(url, stream=True) as response:
        response.raise_for_status()
        size = int(response.headers.get('content-length', 0))  # in Bytes
        chunk_size = 1024
        with open(str(path), 'wb') as file_:
            LOGGER.info('Download "%s" to directory "%s"', url, directory_path)
            for chunk in tqdm(response.iter_content(chunk_size=chunk_size), total=size // chunk_size, unit='KB'):
                file_.write(chunk)
        if response.status_code == requests.codes.ok:
            LOGGER.info('Successfully downloaded "%s"', path)
        else:
            LOGGER.exception('Download of "%s" did not succeed.', path)
    return path
