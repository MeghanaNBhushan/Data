import unittest
import re

from modules.functions import urljoin, url_param_join, compile_regex_from_list


class TestFunctions(unittest.TestCase):

    def test_urljoin(self):
        test_url = 'https://some.url'
        expected_url = 'https://some.url/test/1'
        self.assertEqual(
            urljoin(test_url, 'test', 1), expected_url)

    def test_url_param_join(self):
        test_url = 'https://some.url'
        expected_url_1 = 'https://some.url?start=0&limit=200'
        expected_url_2 = 'https://some.url?limit=200&start=0'
        params = {
            "start": 0,
            "limit": 200
        }
        self.assertTrue(
            url_param_join(test_url, params) == expected_url_1 or
            url_param_join(test_url, params) == expected_url_2
        )

    def test_compile_regex_from_list(self):
        test_regexps = ['^develop$', '^release/.*']
        expected_regexp = '(?:^develop$|^release/.*)'
        self.assertEqual(
            compile_regex_from_list(test_regexps), re.compile(expected_regexp))


if __name__ == '__main__':
    unittest.main()
