#!/usr/bin/python
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This is a helper class containing a Copyright Result.

Author: Michael Engeroff
Department: CC-DA/ESI1 (ITK Engineering GmbH)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import re


def clean_file_name(file_name):
    """ clean the file name """
    result = file_name.replace("\n", "")
    result = result.replace("\\", "/")
    return result


class CopyrightResult:
    """ Class for holding results of on wrong copyright header """

    def __init__(self, root, file_name, repo_name, logger):
        self.__root = root.replace("\\", "/")
        self.__logger = logger
        self.__file_name = clean_file_name(file_name)
        self.__repo_name = repo_name
        self.__path = self.get_relative_path()
        self.__bitbucket_link = self.create_bitbucket_link()
        self.__flags = {}
        self.__flags["has_rb_copyright"] = False
        self.__flags["has_other_rb_copyright"] = False
        self.__flags["has_no_copyright"] = False
        self.__flags["has_other_copyright"] = False
        self.__flags["is_ignored"] = False

    def get_has_rb_copyright(self):
        return self.__flags["has_rb_copyright"]

    def set_has_rb_copyright(self, value):
        self.__flags["has_rb_copyright"] = value

    def get_has_other_rb_copyright(self):
        return self.__flags["has_other_rb_copyright"]

    def set_has_other_rb_copyright(self, value):
        self.__flags["has_other_rb_copyright"] = value

    def get_has_no_copyright(self):
        return self.__flags["has_no_copyright"]

    def set_has_no_copyright(self, value):
        self.__flags["has_no_copyright"] = value

    def get_has_other_copyright(self):
        return self.__flags["has_other_copyright"]

    def set_has_other_copyright(self, value):
        self.__flags["has_other_copyright"] = value

    def get_is_ignored(self):
        return self.__flags["is_ignored"]

    def set_is_ignored(self, value):
        self.__flags["is_ignored"] = value

    def get_root(self):
        return self.__root

    def get_file_name(self):
        return self.__file_name

    def get_full_path(self):
        if self.__root != "":
            return self.__root + "/" + self.__file_name
        else:
            return self.__file_name

    def get_path(self):
        return self.__path

    def get_relative_path(self):
        """ Get the relative path from the whole path. This strips all the irrelevant part from the string. """
        search_str = r"/" + self.__repo_name + "/"

        processed_path = self.get_full_path()
        search_result = re.search(search_str, processed_path, re.IGNORECASE)

        if search_result is not None:
            fvg3_pos_end = re.search(
                search_str, processed_path, re.IGNORECASE).regs[0][1]
            return processed_path[fvg3_pos_end:]
        else:
            return processed_path

    def create_bitbucket_link(self):
        """ Uses the relative link to the file and returns a html link to the respective file on bitbucket """
        return "<a target='_blank' href='https://sourcecode.socialcoding.bosch.com/projects/G3N/repos/fvg3/browse/" + \
               self.__path + "'>File</a>"

    def print_result(self, counter=1):
        """ Print the CopyrightResult object to console. """
        result_str = "#" + str(counter) + " - Path: " + \
            self.__path + " -- Copyright: "
        if self.__flags["has_rb_copyright"]:
            result_str += "RB"
        elif self.__flags["has_other_rb_copyright"]:
            result_str += "RB Other"
        elif self.__flags["has_other_copyright"]:
            result_str += "Other"
        elif self.__flags["has_no_copyright"]:
            result_str += "No Copyright"
        self.__logger.info(result_str)
