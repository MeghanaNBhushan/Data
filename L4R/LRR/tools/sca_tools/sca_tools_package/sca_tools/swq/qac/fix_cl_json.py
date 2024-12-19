# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	fix_cl_json.py
# ----------------------------------------------------------------------------
"""Fixes json file that contain special characters"""

from swq.common.file.file_utils import apply_fix_to_cl_compile_commands


def fix_cl_json_entrypoint(config):
    """ Entrypoint method for fix_cl_json functionality """
    apply_fix_to_cl_compile_commands(config.input_cl_json)
