#!/usr/bin/python
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Unittest for copyright_result class

Author: Michael Engeroff
Department: CC-DA/ESI1
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import unittest

from lucxbox.tools.copyright_checker import copyright_result


class TestCopyrightResult(unittest.TestCase):
    """ Test class for copyright result """

    def test_relative_path_with_fvg3(self):
        """ Test if relative path is created correctly """
        root = "../../../fvg3/folder1/folder2"
        file_name = "testfile.txt"
        repo_name = "fvg3"
        result = copyright_result.CopyrightResult(root, file_name, repo_name, None)

        self.assertTrue(result.get_relative_path(), "folder1/folder2/testfile.txt")

    def test_relative_path_with_nrcs(self):
        """ Test if relative path is created correctly """
        root = "../../../nrcs/folder1/folder2"
        file_name = "testfile.txt"
        repo_name = "nrcs"
        result = copyright_result.CopyrightResult(root, file_name, repo_name, None)

        self.assertTrue(result.get_relative_path(), "folder1/folder2/testfile.txt")

    def test_relative_path_without_repo(self):
        """ Test if relative path is created correctly """
        root = "../../../folder1/folder2"
        file_name = "testfile.txt"
        repo_name = ""
        result = copyright_result.CopyrightResult(root, file_name, repo_name, None)

        self.assertTrue(result.get_relative_path(), "folder1/folder2/testfile.txt")

    def test_get_bitbucket_link(self):
        """ Test if link to file on bitbucket is created correctly """
        root = "../../../fvg3/folder1/folder2"
        file_name = "testfile.txt"
        repo_name = "fvg3"
        result = copyright_result.CopyrightResult(root, file_name, repo_name, None)
        expected_html_string = "<a target='_blank' " \
                               "href='https://sourcecode.socialcoding.bosch.com/projects/G3N/repos/fvg3/browse/" + \
                               "folder1/folder2/testfile.txt'>File</a>"

        self.assertTrue(result.create_bitbucket_link(), expected_html_string)

    def test_filename_with_linebreak(self):
        """
        This tests the case when there is a line break "\n" at the end of the file name.
        The scenario might occur when the script reads in a text file containing a list
        of files to check.
        """
        root = "../../../fvg3/folder1/folder2"
        file_name = "testfile.txt\n"
        repo_name = "fvg3"
        result = copyright_result.CopyrightResult(root, file_name, repo_name, None)
        expected_path = "folder1/folder2/testfile.txt"

        self.assertTrue(result.get_path(), expected_path)


if __name__ == '__main__':
    unittest.main(exit=False)
