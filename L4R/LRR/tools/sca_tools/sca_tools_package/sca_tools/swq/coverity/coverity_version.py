# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	coverity_version.py
# ----------------------------------------------------------------------------
"""Parses information about the helix version and provides helper methods"""

import re
from swq.common.logger import LOGGER

_REGEX_FOR_MAJOR_MINOR = (
    r'(?P<major>\d+)'    # Major version
    r'\.(?P<minor>\d+)'    # Minor version
)


class CoverityVersion:
    """Coverity version related utils"""
    def __init__(self, cli_version_string):
        self._cli_version_string = cli_version_string

    def major_minor(self):
        """Gets the major and minor versions"""
        for match in re.finditer(_REGEX_FOR_MAJOR_MINOR,
                                 self._cli_version_string, re.MULTILINE):
            major = match.group('major')
            minor = match.group('minor')
            if major and minor:
                return (int(major), int(minor))

        # Unknown major and minors
        LOGGER.warning('Unknown major and minor. Version string = %s',
                       self._cli_version_string)
        return (0, 0)
