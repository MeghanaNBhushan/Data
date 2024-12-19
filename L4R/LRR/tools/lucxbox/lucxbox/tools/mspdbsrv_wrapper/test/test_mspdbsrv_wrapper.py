""" Test for a mspdbsrv wrapper """

import unittest
from unittest import mock

import lucxbox.tools.mspdbsrv_wrapper.mspdbsrv_wrapper as mspd


class TestStringMethods(unittest.TestCase):

    @mock.patch("lucxbox.tools.mspdbsrv_wrapper.mspdbsrv_wrapper.LOGGER", create=True)
    def test_main_wrong_version(self, _):
        with self.assertRaises(SystemExit):
            mspd.main(["mspdbsrv_wrapper.py", "-v", "99"])


if __name__ == "__main__":
    unittest.main()
