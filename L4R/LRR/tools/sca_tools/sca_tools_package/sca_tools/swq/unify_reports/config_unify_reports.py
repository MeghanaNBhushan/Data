# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config_unify_reports.py
# ----------------------------------------------------------------------------
"""Shared unify reports project variables"""
from swq.common.config.common_config import CommonConfig
from swq.common.params.parameter_collector import ParameterCollector


def create_unify_reports_config(params, args=None):
    """Parse configuration and creates config object"""
    parameter_collector = ParameterCollector(args, params)

    return UnifyReportsConfig(parameter_collector)


class UnifyReportsConfig(CommonConfig):
    """Class that abstracts the three hierarchical levels of configuration. \
    Read-only access to the variables themselves. \
    This is immutable by design"""
    @property
    def datastore_target(self):
        """Gets the property datastore_target"""
        return self._get_parameter_value('DATASTORE_TARGET')

    @property
    def unify_report_variant_input(self):
        """Gets the property unify_report_variant_input"""
        return self._get_or_read_list_of_paths('UNIFY_REPORT_VARIANT_INPUT')

    @property
    def unify_report_output(self):
        """Gets the property unify_report_output"""
        filepath = self._get_parameter_value('UNIFY_REPORT_OUTPUT')
        return self.get_path_relative_to_project_root(filepath)

    @property
    def unify_report_type(self):
        """Gets the type of unified reports, either qac or coverity"""
        return self._get_parameter_value('UNIFY_REPORT_TYPE')
