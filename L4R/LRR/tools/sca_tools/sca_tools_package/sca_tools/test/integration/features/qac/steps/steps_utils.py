# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: steps_utils.py
# ----------------------------------------------------------------------------

import pandas as pd

from csv import DictReader
from json import loads as json_loads
from os import path as os_path, environ as os_environ, getcwd
from xml.etree.ElementTree import parse as etree_parse
from sys import executable as python_executable
from hamcrest import assert_that, equal_to
from xml.dom.minidom import parse
from swq.common.logger import LOGGER
from test.integration.utils import common_utils
from test.integration.constants import BEHAVE_FOLDER_NAME
from test.integration.run_behave_tests import SWQ_MODULE_PATH
from swq.common.constants import IS_WINDOWS


def _check_qacli_summary_csv(qac_project_path):
    qacli_summary_csv_report_filepath = os_path.join(qac_project_path,
                                                     'sca_tools', 'export',
                                                     'qacli-view-summary.csv')
    assert_that(os_path.exists(qacli_summary_csv_report_filepath),
                equal_to(True), 'qacli-view-summary.csv was not created')


def _check_qacli_view_csv(qac_project_path, expected_total_warnings):
    qacli_view_csv_report_filepath = os_path.join(qac_project_path,
                                                  'sca_tools', 'export',
                                                  'qacli-view-analysis.csv')

    assert_that(os_path.exists(qacli_view_csv_report_filepath), equal_to(True),
                'qacli-view-analysis.csv not created')

    actual_project_total_warnings = 0

    with open(qacli_view_csv_report_filepath, newline='') as csv_file:
        csv_rows = DictReader(csv_file)
        for row in csv_rows:
            if int(row['Suppression type bitmask']) == 0:
                actual_project_total_warnings += 1

    assert_that(actual_project_total_warnings,
                equal_to(expected_total_warnings),
                'Number of warnings in qacli-view-analysis.csv '
                'is not as expected')


def _check_qacli_view_xlxs(qac_project_path, expected_total_warnings):
    qacli_view_xlsx_report_filepath = os_path.join(qac_project_path,
                                                   'sca_tools', 'export',
                                                   'qacli-view.xlsx')

    assert_that(os_path.exists(qacli_view_xlsx_report_filepath),
                equal_to(True), 'qacli-view.xslx was not created')
    df_summary = pd.ExcelFile(qacli_view_xlsx_report_filepath).parse(
        'analysis')
    actual_project_total_warnings = \
        len(df_summary[df_summary['Suppression type bitmask'] == 0])

    assert_that(
        actual_project_total_warnings, equal_to(expected_total_warnings),
        'Number of total warnings in qacli-summary.xslx is not as expected')


def _get_expected_total_warnings_from_severity_summary(qac_project_path):
    summary_xml_filepath = os_path.normpath(
        os_path.join(qac_project_path, 'severity_summary.xml'))
    LOGGER.info("Parsing XML file = %s", summary_xml_filepath)
    xml_tree = etree_parse(summary_xml_filepath)
    xml_root = xml_tree.getroot()
    expected_total_warnings = int(
        xml_root.find("./Summary/SeverityTotal").text)
    return expected_total_warnings


def _check_qacli_view_summary_html(qac_project_path):
    qacli_view_summary_path = os_path.join(qac_project_path, 'sca_tools',
                                           'export', 'qacli-view-summary.html')
    assert_that(os_path.exists(qacli_view_summary_path), equal_to(True),
                'qacli-view-summary.html was not created')

    # with open(qacli_view_summary_path) as summary:
    #     summary_html = BeautifulSoup(summary, 'html.parser')

    # num_headline = 1
    # actual_project_total_warnings = len(
    #     summary_html.find_all("tr")) - num_headline

    # assert_that(int(actual_project_total_warnings),
    #             equal_to(expected_total_warnings),
    #             'number of total warnings not as expected')


def _get_expected_total_warnings(context, config_key, qac_project_path):
    # create the qacli summary in order to get the expected number of warnings
    qacli_summary_command = get_qacli_summary_command(context, config_key)
    return_value = common_utils.execute_command(qacli_summary_command)
    assert_that(return_value, equal_to(True), 'qacli summary command failed')

    expected_total_warnings = \
        _get_expected_total_warnings_from_severity_summary(qac_project_path)
    LOGGER.info('expected_total_warnings found: %s', expected_total_warnings)
    return expected_total_warnings


def get_qacli_summary_command(context, config_key):
    qac_bin_path = context.configs[config_key]['QAC_BIN_PATH']
    qacli_binary = 'qacli.exe' if IS_WINDOWS else 'qacli'
    qacli_executable = os_path.join(qac_bin_path, qacli_binary)
    qac_project_path = os_path.join(
        context.test_root, BEHAVE_FOLDER_NAME, 'bin',
        context.configs[config_key][config_key]['QAC_PROJECT_PATH'])

    qacli_summary_command = [
        qacli_executable, 'view', '--qaf-project', qac_project_path, '-t',
        'SUMMARY', '-m', 'XML', '-o', qac_project_path
    ]

    return qacli_summary_command


def get_command(context, config_key, session, options=None):
    json_filepath = os_path.join(context.json_path, f'{config_key}.json')
    project_root = os_path.join(context.project_root)
    qac_bin_path = os_environ.get('QAC_BIN_PATH') or \
        context.configs[config_key]['QAC_BIN_PATH'] or \
        context.configs[config_key][config_key]['QAC_BIN_PATH']
    nox_file_path = os_path.join(project_root, 'noxfile.py')

    command = [
        python_executable, '-m', 'nox', '-f', nox_file_path, '-s', session,
        '--', '--qac_json', json_filepath, '--qac_bin_path', qac_bin_path,
        '--project_root', project_root, '--variant', config_key, '--sca_tools',
        os_path.join(SWQ_MODULE_PATH.absolute(), 'sca_tools.py')
    ]

    common_utils.extend_command_with_options(command, options)

    return command


def get_amount_of_issues_from_csv_report(csv_filepath):
    with open(csv_filepath, newline='') as csv_file:
        csv_rows = DictReader(csv_file)
        return len(list(csv_rows))


def get_amount_of_issues_from_json_report(json_filepath):
    amount_of_issues = 0

    with open(json_filepath, 'r') as json_file:
        json_data = json_loads(json_file.read())
        for json_block in json_data['issues']:
            amount_of_issues += json_block['occurrenceNumberInMK'] == 1

    return amount_of_issues


def verify_reports(context, config_key):
    qac_project_path = os_path.join(
        context.test_root, BEHAVE_FOLDER_NAME, 'bin',
        context.configs[config_key][config_key]['QAC_PROJECT_PATH'])
    expected_total_warnings = _get_expected_total_warnings(
        context, config_key, qac_project_path)

    _check_qacli_view_summary_html(qac_project_path)
    _check_qacli_summary_csv(qac_project_path)
    _check_qacli_view_csv(qac_project_path, expected_total_warnings)
    _check_qacli_view_xlxs(qac_project_path, expected_total_warnings)


def modify_config(context, old_config, new_config, config_key, cr_qacpp=None):
    """ Writes the new qac json file """
    qacpp_version = ''
    cr_version = ''
    if cr_qacpp:
        cr_version = cr_qacpp[0]
        qacpp_version = cr_qacpp[1]

    project_root = os_path.join(context.project_root)

    _, _, synctype, qac_version = config_key.split('_')
    qac_version_min = qac_version.replace('helix', '', 1).strip()

    mapping = {
        "qac_version": qac_version,
        "qac_version_min": qac_version_min,
        "cr_version": cr_version,
        "qacpp_version": qacpp_version,
        "project_root": project_root,
        "test_root": context.test_root,
        "synctype": synctype,
        "config_key": config_key
    }

    common_utils.replace_pattern(old_config, new_config, mapping)
    return new_config


def read_parameter_table(context, config_key):
    """ Reads the parameter table given in a feature """
    LOGGER.info('For config key %s read in paramter table: %s', config_key,
                context.configs[config_key])
    json_file_id = config_key
    target_name = config_key
    target_options = context.configs[json_file_id][target_name]
    target_options = common_utils.map_target_options(context, target_options)
    common_utils.save_json_config(context, config_key,
                                  context.configs[config_key])
    modify_config(context, context.configs[config_key],
                  context.configs[config_key], config_key)


def file_contains_setting(project_xml_path, file):
    """ Checks whether prqaproject.xml contains a synced file """
    pattern = f'<file target="C++" name="{file}"'

    if os_path.exists(project_xml_path):
        with open(project_xml_path) as project_xml_file:
            contents = project_xml_file.read()
            if pattern in contents:
                return True
    else:
        print('prqaproject.xml NOT found', project_xml_path)
    return False


def xml_contains_setting_in_attribute(project_xml_path, xml_tag,
                                      attribute_name):
    """ Checks whether prqaproject.xml contains a given attribute """
    if os_path.exists(project_xml_path):
        xml_dom = parse(project_xml_path)
        matched_tags = xml_dom.getElementsByTagName(xml_tag)
        return [tag.attributes[attribute_name].value for tag in matched_tags]

    print('prqaproject.xml NOT found', project_xml_path)
    return []


def get_number_of_synced_files(path_prqaproject_xml):
    """ Counts the number of synced files in prqaproject.xml """
    if path_prqaproject_xml.endswith('prqaproject.xml'):
        xml_tag = 'file'
        if not os_path.exists(path_prqaproject_xml):
            print('prqaproject.xml NOT found', path_prqaproject_xml)
            return 0
        xml_dom = parse(path_prqaproject_xml)
        matched_tags = xml_dom.getElementsByTagName(xml_tag)
        return len(matched_tags)
    return 0


def _log_combinations(message, context, info=False):
    if info:
        LOGGER.info(f'{message} %s', context.config_combinations)
        comb_path = os_path.join(getcwd(), 'combinations.csv')
        context.config_combinations.to_csv(comb_path, index=False)


def _add_qac_version(row, context):
    _combination = {
        'synctype': '',
        "qac_version": row['qac_version'],
        'cr_version': row['coding_rules_version'],
        'qacpp_version': row['component_version'],
        'rcf_file': row['rcf_file'],
        'cct': '',
        'compiler': ''
    }
    context.config_combinations = context.config_combinations.append(
        _combination, ignore_index=True)
    _log_combinations('_add_qac_version', context)


def _add_synctype(df_comb_templates, row, context):
    def _add_synctype_combination(combination_row, feature_row):
        if combination_row["synctype"] == '':
            combination_row["synctype"] = feature_row["synctype"]
        return combination_row

    df_comb_new = df_comb_templates.copy()
    df_comb_new.apply(lambda x: _add_synctype_combination(x, row), axis=1)
    # LOGGER.info('df_comb_new %s', df_comb_new)
    context.config_combinations = pd.concat(
        [context.config_combinations, df_comb_new])
    _log_combinations('_add_synctype', context)


def _create_config(context, row):
    cr_qacpp = [row.cr_version, row.qacpp_version]
    config_key = f'qac_{row.compiler}_{row.synctype}_{row.qac_version}'
    config_key = config_key.lower()
    old_config = context.base_config
    new_config = context.configs[config_key] = {}

    context.configs[config_key] = modify_config(context, old_config,
                                                new_config, config_key,
                                                cr_qacpp)

    context.configs[config_key]['COMPILER_LIST'] = row.cct
    context.configs[config_key]['RCF_FILE'] = row.rcf_file
    context.configs[config_key]['SYNC_TYPE'] = row.synctype
    LOGGER.info('Config created for %s', config_key)
    common_utils.save_json_config(context, config_key,
                                  context.configs[config_key])


def _get_compilers(context):
    df_compilers = pd.DataFrame(columns=['qac_version', 'cct', 'compiler'])
    for row in context.table.rows:
        _combination = {
            "qac_version":
            row['qac_version'],
            "cct":
            common_utils._get_value_field_as_single_value_or_list(row['cct']),
            "compiler":
            row['compiler']
        }
        df_compilers = df_compilers.append(_combination, ignore_index=True)
    return df_compilers


def _merge_compilers(context, df_compilers):
    context.config_combinations = pd.merge(context.config_combinations,
                                           df_compilers,
                                           how='outer',
                                           on='qac_version')
    cols_drop = ['cct_x', 'compiler_x']
    context.config_combinations.drop(columns=cols_drop, inplace=True)

    cols_rename = {"cct_y": "cct", "compiler_y": "compiler"}
    context.config_combinations.rename(columns=cols_rename, inplace=True)
