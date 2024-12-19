# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	constants.py
# ----------------------------------------------------------------------------
"""Defines constants for the swq.common.report module"""

from os import path
from swq.common.constants import SWQ_MODULE_PATH


REPORT_HTML_TEMPLATES_PATH = path.join(SWQ_MODULE_PATH, 'common', 'report',
                                       'templates')
REPORT_HTML_TEMPLATE_FILENAME = 'report.html'

LICENSE_WARNING = 'Working (fixing and triaging issues) with information' +\
    ' in this report is only allowed with a QAFramework license !!!' +\
    ' Otherwise a license violation is committed.' +\
    ' Using the information for Metric only purposes is fine.'
