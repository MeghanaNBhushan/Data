""" Test for tccw """

import logging
import unittest
from unittest import mock

from lucxbox.tools.retryw import retryw


class TestRetryw(unittest.TestCase):
    """ Test class for retry wrapper """

    @mock.patch("lucxbox.tools.retryw.retryw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.retryw.retryw.lucxutils.execute")
    def test_main(self, mock_execute, _):
        mock_execute.return_value = "The eagle has landed!", "", 0
        return_code = retryw.main(["retry.py", "-s", "test", "--", "echo"])
        self.assertEqual(0, return_code)
        self.assertEqual(1, mock_execute.call_count)

    @mock.patch("lucxbox.tools.retryw.retryw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.retryw.retryw.lucxutils.execute")
    def test_retry_loop(self, mock_execute, mock_logger):
        mock_execute.return_value = "The eagle has landed!", "", 0
        return_code = retryw.retry_loop(["echo", "true"], 1, ["AFFEAFFE"])
        self.assertEqual(0, return_code)
        self.assertEqual(1, mock_execute.call_count)

        ref_call = mock.call.info("SUCCESS")
        self.assertEqual(ref_call, mock_logger.mock_calls[0])


    @mock.patch("lucxbox.tools.retryw.retryw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.retryw.retryw.lucxutils.execute")
    def test_retry_loop_fail(self, mock_execute, mock_logger):
        mock_execute.return_value = "", "Huston we have a problem.", 1
        return_code = retryw.retry_loop(["echo", "true"], 1, ["AFFEAFFE"])
        self.assertEqual(1, return_code)
        self.assertEqual(1, mock_execute.call_count)

        ref_call = mock.call.error("Unkown error seen, stopping retry wrapper.")
        self.assertEqual(ref_call, mock_logger.mock_calls[0])
        ref_call = mock.call.log(logging.ERROR, "stdout:\n%s", "")
        self.assertEqual(ref_call, mock_logger.mock_calls[1])
        ref_call = mock.call.log(logging.ERROR, "stderr:\n%s", "Huston we have a problem.")
        self.assertEqual(ref_call, mock_logger.mock_calls[2])

    @mock.patch("lucxbox.tools.retryw.retryw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.retryw.retryw.lucxutils.execute")
    def test_retry_loop_fail_once(self, mock_execute, mock_logger):
        mock_execute.side_effect = [["", "Huston we have a problem.", 1], ["The eagle has landed!", "", 0]]
        return_code = retryw.retry_loop(["echo", "true"], 1, ["Huston we have a problem."])
        self.assertEqual(0, return_code)
        self.assertEqual(2, mock_execute.call_count)

        ref_call = mock.call.info("Found known issue in output, starting retry...")
        self.assertEqual(ref_call, mock_logger.mock_calls[0])
        ref_call = mock.call.log(logging.DEBUG, "stdout:\n%s", "")
        self.assertEqual(ref_call, mock_logger.mock_calls[1])
        ref_call = mock.call.log(logging.DEBUG, "stderr:\n%s", "Huston we have a problem.")
        self.assertEqual(ref_call, mock_logger.mock_calls[2])

    @mock.patch("lucxbox.tools.retryw.retryw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.retryw.retryw.lucxutils.execute")
    def test_retry_loop_fail_twice(self, mock_execute, mock_logger):
        mock_execute.return_value = "", "Huston we have a problem.", 1
        return_code = retryw.retry_loop(["echo", "true"], 1, ["Huston we have a problem."])
        self.assertEqual(1, return_code)
        self.assertEqual(2, mock_execute.call_count)

        ref_call = mock.call.info("Found known issue in output, starting retry...")
        self.assertEqual(ref_call, mock_logger.mock_calls[0])
        ref_call = mock.call.error("Found known issue in output in retry '%s', stopping retry wrapper.", '1')
        self.assertEqual(ref_call, mock_logger.mock_calls[3])

    @mock.patch("lucxbox.tools.retryw.retryw.LOGGER", create=True)
    @mock.patch("lucxbox.tools.retryw.retryw.lucxutils.execute")
    def test_retry_loop_two_strings(self, mock_execute, mock_logger):
        mock_execute.return_value = "", "Huston we have a problem.", 1
        return_code = retryw.retry_loop(["echo", "true"], 1, ["Huston we have a problem.", "AFFEAFFE"])
        self.assertEqual(1, return_code)
        self.assertEqual(2, mock_execute.call_count)

        ref_call = mock.call.info("Found known issue in output, starting retry...")
        self.assertEqual(ref_call, mock_logger.mock_calls[0])
        ref_call = mock.call.error("Found known issue in output in retry '%s', stopping retry wrapper.", '1')
        self.assertEqual(ref_call, mock_logger.mock_calls[3])


if __name__ == "__main__":
    unittest.main()
