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

from steps_utils import modify_coverity_config
from behave import given, then
from swq.common.logger import LOGGER
from test.integration.utils import common_utils
from test.integration.constants import TABLE_PROVIDED_MESSAGE


@given(u'a clean coverity project')
def read_configuration(context):
    """ Creates Coverity project """
    common_utils.read_configurations(context)


@given(u'the codeowners information')
def generate_cov_team_component_information(context):
    """ Gets the team/components """
    codeowners_filepath = common_utils.generate_codeowners_file(context)
    LOGGER.info('Codeowners file path is: %s', codeowners_filepath)


@given(u'a json config for {config_key}')
def parse_custom_config_table(context, config_key):
    """ Gets the config for the given coverity version """
    LOGGER.info('Get configutration for: %s', config_key)
    target_options = {}
    context.configs[config_key][config_key] = common_utils.map_target_options(
        context, target_options)
    LOGGER.info('Configuration was extended with %s', target_options)
    context.coverity_version = config_key.split('_')[-1]
    modify_coverity_config(context, context.configs[config_key],
                           context.configs[config_key], config_key)
    common_utils.save_json_config(context, config_key,
                                  context.configs[config_key])


@given(u'those coverity versions')
def parse_coverity_versions(context):
    """ Creates configurations """
    assert context.table, TABLE_PROVIDED_MESSAGE
    for row in context.table.rows:
        coverity_version = row['coverity_version']
        LOGGER.info('Got following coverity version %s', coverity_version)
        context.coverity_versions.append(coverity_version)


@given(u'these options for config generation')
def parse_base_options(context):
    """ Store options to the context """
    assert context.table, TABLE_PROVIDED_MESSAGE

    context.base_config = common_utils.generate_json_config_from_table(
        context.table)


@then(u'configurations are generated for those compilers')
def parse_compiler_options(context):
    """ Generates the configuration file """
    assert context.table, TABLE_PROVIDED_MESSAGE
    for row in context.table.rows:
        compiler = row["key"]
        compiler_option = row["value"]
        context.compilers[compiler] = []
        context.compilers[compiler].extend(f'{compiler_option}'.split(','))

        for coverity_version in context.coverity_versions:
            config_key = f'coverity_{compiler}_{coverity_version}'
            old_config = context.base_config
            new_config = context.configs[config_key] = {}
            context.coverity_version = coverity_version
            context.configs[config_key] = modify_coverity_config(
                context, old_config, new_config, config_key)
            context.configs[config_key]['COMPILER_LIST'] = context.compilers[
                compiler]
            common_utils.save_json_config(context, config_key,
                                          context.configs[config_key])
