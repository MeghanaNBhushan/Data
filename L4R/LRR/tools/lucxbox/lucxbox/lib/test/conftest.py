import io
from pathlib import Path
from zipfile import ZipFile

import pytest


@pytest.fixture
def suppress_logging(mocker):
    mocker.patch("lucxbox.lib.lucxio.LOGGER")


@pytest.fixture
def mock_tqdm(mocker):
    mocker.patch('lucxbox.lib.lucxio.tqdm', side_effect=lambda iterable, *args, **kwargs: iterable)


@pytest.fixture
def session_with_empty_response(mocker):
    mock_response = mocker.Mock()
    mock_response.headers.get.return_value = 0
    mock_response.iter_content.return_value = []
    mock_session = mocker.Mock()
    mock_session.get.return_value.__enter__ = lambda _: mock_response
    mock_session.get.return_value.__exit__ = lambda *args, **kwargs: None
    return mock_session


@pytest.fixture
def robots_txt_allow_all():
    return '''User-agent: *
Disallow:'''


@pytest.fixture
def session_with_byte_stream(mocker, robots_txt_allow_all):
    mock_response = mocker.Mock()
    bytes_ = robots_txt_allow_all.encode('ascii')
    mock_response.iter_content.return_value = io.BytesIO(bytes_)
    mock_response.headers.get.return_value = len(bytes_)
    mock_session = mocker.Mock()
    mock_session.get.return_value.__enter__ = lambda _: mock_response
    mock_session.get.return_value.__exit__ = lambda *args, **kwargs: None
    return mock_session


@pytest.fixture
def subdirectory_path():
    return 'some/sub/directory'


@pytest.fixture
def robots_txt_filename():
    return 'robots.txt'


@pytest.fixture
def example_filename():
    return 'example.txt'


@pytest.fixture
def example_text():
    return u'This is an example text file.'


@pytest.fixture
def extract_directory(tmpdir):
    tmp_path = Path(tmpdir.strpath)
    directory = tmp_path / 'extract'
    directory.mkdir()
    return directory


@pytest.fixture
def zipfile_path(tmpdir, subdirectory_path, example_filename, example_text):
    tmp_path = Path(tmpdir.strpath)
    subdirectory = tmp_path / subdirectory_path
    subdirectory.mkdir(parents=True)
    example_file = subdirectory / example_filename
    example_file.write_text(example_text)
    zipfile_path_ = tmp_path / 'example.zip'
    with ZipFile(str(zipfile_path_), 'w') as zipfile:
        zipfile.write(filename=str(example_file), arcname='{}/{}'.format(subdirectory_path, example_filename))
    return zipfile_path_
