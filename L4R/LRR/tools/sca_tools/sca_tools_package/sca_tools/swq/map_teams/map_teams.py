# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: map_teams.py
# ----------------------------------------------------------------------------
""" Creates teams report based on input CSV warnings report extended with teams
and components information from codeowners file """

from numpy import vectorize
from pandas import read_csv
from pandas.core.common import flatten

from swq.common.logger import LOGGER
from swq.common.component_mapping import ComponentMapper

TEAM_COLUMN_NAME = 'Team'
COMPONENT_COLUMN_NAME = 'Components'
TEAM_REPORT_EXTRA_FIELDNAMES = [TEAM_COLUMN_NAME, COMPONENT_COLUMN_NAME]
TEAMS_SEPARATOR = " "
SENSITIVE_INFO_WARNING_MESSAGE = 'Generated Teams/Components reports may \
contain sensitive information and MUST NOT be distributed outside'


def _get_teams_from_list_of_teams(teams):
    return TEAMS_SEPARATOR.join(sorted(set(flatten(teams))))


def _print_input_information(config):
    LOGGER.warning(SENSITIVE_INFO_WARNING_MESSAGE)
    LOGGER.info("Input csv report file is %s", config.input_warnings_report)
    LOGGER.info("Input codeowners files list %s", config.codeowners_file)
    LOGGER.info("Result csv report file is %s", config.teams_report)
    LOGGER.debug("Input csv report file delimiter is '%s'",
                 config.field_delimiter)


def add_team_components_to_row(row, filepath_index, component_mapper,
                               only_last_team):
    """Adds team/component information to a row"""
    try:
        filepath = row[filepath_index].replace('\\', '/')
        teams = component_mapper.get_teams_for_path(filepath)
        components = component_mapper.get_component_names_for_path(filepath)
        if only_last_team:
            result_team = TEAMS_SEPARATOR.join(teams[-1]) if teams else ''
            result_components = components[-1] if components else ''
        else:
            result_team = _get_teams_from_list_of_teams(teams)
            result_components = TEAMS_SEPARATOR.join(components)
        return row + [result_team, result_components]
    except AttributeError:
        return row


def map_teams_components_in_dataframe(dataframe, team_column_name,
                                      component_column_name, config,
                                      mapping_column=''):
    """Maps teams and components in pandas dataframe"""
    def _get_team(filepath):
        teams = component_mapper.get_teams_for_path(filepath)
        if config.only_last_team:
            return TEAMS_SEPARATOR.join(teams[-1]) if teams else ''

        return _get_teams_from_list_of_teams(teams)

    def _get_component(filepath):
        components = component_mapper.get_component_names_for_path(filepath)
        if config.only_last_team:
            component = components[-1] if components else ''
            return component

        return TEAMS_SEPARATOR.join(components)

    component_mapper = ComponentMapper(config.codeowners_file)
    _mapping_column = mapping_column \
                      if mapping_column else config.mapping_column

    dataframe.loc[:, team_column_name] = vectorize(_get_team)(
        dataframe[_mapping_column].str.replace('\\', '/', regex=False).values)

    dataframe.loc[:, component_column_name] = vectorize(_get_component)(
        dataframe[_mapping_column].str.replace('\\', '/', regex=False).values)


def map_teams(config):
    """ Entrypoint function for map_teams functionality """

    _print_input_information(config)

    report_dataframe = read_csv(config.input_warnings_report,
                                delimiter=config.field_delimiter,
                                quotechar='"',
                                keep_default_na=False,
                                dtype=str)

    LOGGER.debug("Input csv column names: %s",
                 report_dataframe.columns.tolist())

    map_teams_components_in_dataframe(report_dataframe, TEAM_COLUMN_NAME,
                                      COMPONENT_COLUMN_NAME, config)

    report_dataframe.to_csv(config.teams_report, index=False)
