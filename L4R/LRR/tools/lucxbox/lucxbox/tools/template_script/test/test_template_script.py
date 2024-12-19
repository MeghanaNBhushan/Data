""" Test for a python project """

import unittest

from lucxbox.tools.template_script import template_script


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        string = "foo"
        result = template_script.upper(string)
        self.assertEqual("FOO", result)


if __name__ == "__main__":
    unittest.main()
