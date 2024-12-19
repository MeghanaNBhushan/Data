# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: ncf_config_merger.py
# ----------------------------------------------------------------------------
"""Defines a NCF configuration merger"""
from swq.qac.config.text_config_merger import TextConfigMerger


class NcfConfigMerger(TextConfigMerger):
    """Defines a NCF configuration merger class"""

    _merged_filename = 'merged_ncf.ncf'

    def merge_contents(self, parsed_content: list):
        """Merges NCF configuration files content"""
        return '\n'.join(parsed_content)
