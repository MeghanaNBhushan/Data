# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: args_map_teams.py
# -----------------------------------------------------------------------------
"""The argument subparser for the map_teams subcommand of SCA tools"""

from swq.common.args.args_utils import add_common_config_args, \
    map_teams_common_configurable_args


def parse_args_map_teams(helper_sub, params, entrypoints):
    """ Parses map_teams subcommand arguments """
    map_teams_parser = helper_sub.add_parser('map_teams',
                                             help=params.get_description())

    add_common_config_args(map_teams_parser, params)

    map_teams_parser.add_argument(
        params.INPUT_WARNINGS_REPORT.flag_short,
        params.INPUT_WARNINGS_REPORT.flag_long,
        type=str,
        help=params.INPUT_WARNINGS_REPORT.description)

    map_teams_parser.add_argument(params.TEAMS_REPORT.flag_short,
                                  params.TEAMS_REPORT.flag_long,
                                  type=str,
                                  help=params.TEAMS_REPORT.description)

    map_teams_parser.add_argument(params.MAPPING_COLUMN.flag_short,
                                  params.MAPPING_COLUMN.flag_long,
                                  type=str,
                                  help=params.MAPPING_COLUMN.description)

    map_teams_parser.add_argument(params.FIELD_DELIMITER.flag_short,
                                  params.FIELD_DELIMITER.flag_long,
                                  type=str,
                                  choices=[',', ';', ':', '|'],
                                  help=params.FIELD_DELIMITER.description)

    map_teams_common_configurable_args(map_teams_parser, params)

    map_teams_parser.set_defaults(entrypoint='map_teams',
                                  func=entrypoints['map_teams'],
                                  subcommand=None)
