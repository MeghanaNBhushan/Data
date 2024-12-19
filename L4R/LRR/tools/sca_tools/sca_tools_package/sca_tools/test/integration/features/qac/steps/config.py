# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: config.py
# ----------------------------------------------------------------------------

import steps_utils

from os import path as os_path
from behave import given, then
from swq.common.logger import LOGGER
from test.integration.utils import common_utils
from test.integration.constants import TABLE_PROVIDED_MESSAGE


@given(u'a clean qac project with defined configuration')
def read_configuration(context):
    """ Creates Coverity project """
    common_utils.read_configurations(context)


@given(u'those helix versions and specifications')
def read_in_helix_versions(context):
    """ Creates json configuration """
    assert context.table, TABLE_PROVIDED_MESSAGE

    for row in context.table.rows:
        LOGGER.info('Found Helix version: %s', row)
        steps_utils._add_qac_version(row, context)


@given(u'these options for config generation')
def read_in_base_options(context):
    """ Store synctypes to the context """
    assert context.table, TABLE_PROVIDED_MESSAGE
    context.base_config = common_utils.generate_json_config_from_table(
        context.table)


@given(u'these synctypes')
def read_in_synctypes(context):
    """ Reads in the possible sync types """
    assert context.table, TABLE_PROVIDED_MESSAGE

    df_comb_templates = context.config_combinations.copy()
    index = context.config_combinations.index
    context.config_combinations.drop(index, inplace=True)

    for row in context.table.rows:
        LOGGER.info('read_in_synctypes got this config row %s', row)
        steps_utils._add_synctype(df_comb_templates, row, context)
    steps_utils._log_combinations('after read_in_synctypes', context)


@given(u'the codeowners information')
def generate_qac_team_component_information(context):
    """ Gets the team/components """
    codeowners_filepath = common_utils.generate_codeowners_file(context)
    LOGGER.info('Codeowners file path is: %s', codeowners_filepath)


@then(u'configurations are generated for those compilers')
def read_in_compiler_settings(context):
    """ Generates the configuration file """
    assert context.table, TABLE_PROVIDED_MESSAGE

    df_compilers = steps_utils._get_compilers(context)
    LOGGER.info('Created df_compilers %s', df_compilers)

    steps_utils._merge_compilers(context, df_compilers)
    LOGGER.info('Compilers merged to context.combinations')
    steps_utils._log_combinations('after read_in_compiler_settings', context)

    context.config_combinations.apply(
        lambda row: steps_utils._create_config(context, row), axis=1)


@given(u'a json config for {config_key}')
def get_config_for_create(context, config_key):
    """ Gets the config for the given qac version """
    LOGGER.info('Get config for: %s', config_key)
    target_options = {}
    target_options = common_utils.map_target_options(context, target_options)
    LOGGER.info('Add create options to config: %s', target_options)
    context.configs[config_key][config_key] = target_options
    steps_utils.modify_config(context, context.configs[config_key],
                              context.configs[config_key], config_key)

    common_utils.save_json_config(context, config_key,
                                  context.configs[config_key])

    json_filepath = os_path.join(context.json_path, f'{config_key}.json')
    LOGGER.info('Modified config (qac.json) for: %s', json_filepath)
