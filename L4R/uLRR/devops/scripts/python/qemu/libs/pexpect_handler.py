import pexpect
import sys
import time


class PexpectHandler:
  """
  PexpectHandler class for handling pexpect commands.

  This class provides a wrapper around the pexpect library to simplify the usage of pexpect commands.

  Attributes:
    runner (pexpect.spawn): The pexpect spawn object used for running commands.
  """

  def __init__(self):
    """
    Initializes a new instance of the PexpectHandler class.

    It sets up the pexpect handler by spawning a new bash process and sets the logfile to stdout.
    """
    self.runner = pexpect.spawn("bash", encoding='utf-8')
    self.runner.logfile = sys.stdout

  def command_request(self, command_str, expected_answer, feedback_delay=1):
    """
    Sends a command to the pexpect handler and waits for the expected answer.

    Args:
      command_str (str): The command to send.
      expected_answer (str or list): The expected answer(s) to wait for.
      feedback_delay (int, optional): The delay in seconds before checking for the expected answer. Defaults to 1.

    Returns:
      int: The index of the matched pattern in the expected answer list.

    Raises:
      pexpect.exceptions.TIMEOUT: If the expected answer is not found within the timeout period.
    """
    self.runner.sendline(command_str)
    if feedback_delay is not None:
      time.sleep(feedback_delay)
    return self.runner.expect(expected_answer, timeout=feedback_delay)
  
  def interact(self):
    """
    Starts the interactive mode of the pexpect handler.

    This method allows the user to interact with the spawned bash process.
    """
    logfile_read_bcpk = self.runner.logfile_read
    logfile_bcpk = self.runner.logfile

    self.runner.logfile_read = None
    self.runner.logfile = None
    self.runner.interact()
    self.runner.logfile_read = logfile_read_bcpk
    self.runner.logfile = logfile_bcpk