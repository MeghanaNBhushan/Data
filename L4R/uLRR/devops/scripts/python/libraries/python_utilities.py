__copyright__ = """
@copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""

"""
Terminal color definition
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

"""
This function prints a new line in the terminal
"""
def ConsoleOutput(color_s_=bcolors.OKBLUE, node_name_s_ ="Not Specified", msg="", verbose_mode=True, verbose_level="debug_mode"):
    """Controls the feedback printed to the console
        It is controlled by the global variable g_verbose_mode
        If True all messages will printed
        If False all output will be suppressed (unless in main function) 
    Parameters
    ----------
    msg
        Msg. to be printed
    verbose_mode
        Current verbose mode
    verbose_level
        Verbose level
    Returns
    -------
    None
    """
    if verbose_mode == True and verbose_level == "debug_mode":
        print(color_s_ + "["+node_name_s_+"]" + msg + bcolors.ENDC)
    elif verbose_level == "run_mode":
        print(color_s_ + "["+node_name_s_+"]" + msg + bcolors.ENDC)
