""" Test for lib modules """
import unittest
from os import path, remove

import pytest

from lucxbox.lib import finder
from  lucxbox.lib import lucxargs
from lucxbox.lib import portal
from lucxbox.lib import wildcards
from lucxbox.lib.lucxtest import TestCaseWithTempFile
from lucxbox.lib.lucxutils import zipfile_extractall_subdirectory, NoSubDirectoryZipFile
from lucxbox.lib.lucxio import download
from lucxbox.lib.lucxutils import hash_file


class TestStringMethods(TestCaseWithTempFile):

    def test_get_files_with_ending(self):
        with open(path.join(self.test_dir, 'test.txt'), 'w') as test_file:
            test_file.write("Spam! Spam! Spam! Spam! Lovely spam! Wonderful spam!")
        with portal.In(self.test_dir):
            result = finder.get_files_with_ending([".txt"])
            self.assertEqual([path.join(".", "test.txt")], result)
        with portal.In(self.test_dir):
            result = finder.get_files_with_ending([".txt"], excludes=[".txt"])
            self.assertEqual([], result)

    def test_wildcard_double_star_match(self):
        pattern = "../something/otherthing/component/src/x.h"
        wildcard = "**/component/**"
        self.assertTrue(wildcards.matches_wildcard_pattern(pattern, wildcard))

    def test_wildcard_no_match(self):
        pattern = "../something/otherthing/component/src/x.h"
        wildcard = "**/component/*"
        self.assertFalse(wildcards.matches_wildcard_pattern(pattern, wildcard))

    def test_wildcard_wrong_start(self):
        pattern = "../something/otherthing/component/src/x.h"
        wildcard = "component/**"
        self.assertFalse(wildcards.matches_wildcard_pattern(pattern, wildcard))

    def test_wildcard_single_star_match(self):
        pattern = "../something/otherthing/component/src/x.h"
        wildcard = "../something/otherthing/component/src/*.h"
        self.assertTrue(wildcards.matches_wildcard_pattern(pattern, wildcard))
        pattern2 = "../something/otherthing/component/src/x.hpp"
        self.assertFalse(wildcards.matches_wildcard_pattern(pattern2, wildcard))

    def test_split_args(self, ):
        main_argv, build_argv = lucxargs.split_argv(["mspdbsrv_wrapper.py", "-v", \
                                                 "10", "--", "python", "build_cmake.py"])
        self.assertEqual(["-v", "10"], main_argv)
        self.assertEqual(["python", "build_cmake.py"], build_argv)


@pytest.mark.usefixtures('mock_tqdm', 'suppress_logging')
def test_creates_dir_if_needed(tmpdir, session_with_empty_response, robots_txt_filename):
    download_directory = tmpdir.join('download')
    assert not download_directory.check()

    download(url='http://www.example.com/{}'.format(robots_txt_filename),
             directory=download_directory.strpath,
             filename=robots_txt_filename,
             session=session_with_empty_response)

    assert download_directory.check()


@pytest.mark.usefixtures('mock_tqdm', 'suppress_logging')
def test_download_creates_file(tmpdir, session_with_empty_response, robots_txt_filename):
    download_directory = tmpdir.mkdir('download')

    actual_filename = download(url='http://www.example.com/{}'.format(robots_txt_filename),
                               directory=download_directory.strpath,
                               filename=robots_txt_filename,
                               session=session_with_empty_response)

    expected_filename = download_directory.join(robots_txt_filename)
    assert expected_filename == actual_filename
    assert expected_filename.check()


@pytest.mark.usefixtures('mock_tqdm', 'suppress_logging')
def test_download_writes_content(tmpdir, session_with_byte_stream, robots_txt_filename, robots_txt_allow_all):
    download_directory = tmpdir.mkdir('download')

    download(url='http://www.example.com/{}'.format(robots_txt_filename),
             directory=download_directory.strpath,
             filename=robots_txt_filename,
             session=session_with_byte_stream)

    path_ = download_directory.join(robots_txt_filename)
    assert path_.check()
    assert path_.read() == robots_txt_allow_all


@pytest.mark.usefixtures('suppress_logging')
def test_correctly_extracts_subdir(zipfile_path, extract_directory, subdirectory_path, example_filename, example_text):
    zipfile_extractall_subdirectory(zipfile_path, extract_directory, subdirectory_path + '/')

    example_file_extracted = extract_directory / example_filename
    assert example_file_extracted.exists()
    assert example_file_extracted.read_text() == example_text


@pytest.mark.usefixtures('suppress_logging')
def test_throws_if_no_subdir(zipfile_path, extract_directory):
    with pytest.raises(NoSubDirectoryZipFile):
        zipfile_extractall_subdirectory(zipfile_path, extract_directory, 'non/existent/sub/directory/')


def test_hash_file():
    with open('test_windows', 'wb') as file_:
        file_.write(b'a\r\n')
    with open('test_unix', 'wb') as file_:
        file_.write(b'a\n')
    try:
        assert hash_file('test_windows') == hash_file('test_unix')
    finally:
        remove('test_windows')
        remove('test_unix')

if __name__ == "__main__":
    unittest.main()
