# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: environment.py
# ----------------------------------------------------------------------------
""" Setting up the environement before the features are started """
import os
import pandas as pd

from test.integration.constants import BEHAVE_FOLDER_NAME, OS_FOLDER
from test.integration.utils.common_utils import initialize_context


def before_all(context):
    """ Preparing the context used by the features """
    initialize_context(context)
    context.qac_versions = {}

    columns = [
        'synctype', 'qac_version', 'cr_version', 'qacpp_version', 'cct',
        'compiler'
    ]
    context.config_combinations = pd.DataFrame(columns=columns)
    context.filter_qac_version = os.environ.get("VERSION", "")
    context.features = f'{BEHAVE_FOLDER_NAME}/features/qac/{OS_FOLDER}'
