""" Helper component for warnings parser. """

import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()

def write_json(warnings_file, warnings):
    """Create a json report containing the compiler warnings.

    :param warnings_file: output file
    :param warnings: list containing the compiler warnings
    """
    LOGGER.debug("Preparing to write new json file '%s'", warnings_file)

    with open(warnings_file, 'w', newline='') as json_file:
        json_file.write(json.dumps(warnings, default=lambda warning: warning.__dict__))
