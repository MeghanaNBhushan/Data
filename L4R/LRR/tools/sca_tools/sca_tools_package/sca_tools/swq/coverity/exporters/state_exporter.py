# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	state_exporter.py
# ----------------------------------------------------------------------------
"""Exports Coverity project state reports"""

import urllib.request
import ssl

from json import load, loads, dump
from os import path
from requests import get
from swq.coverity.constants import \
    PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX, \
    ERROR_EXPORT_TABLE_MAIN_EVENT_FILEPATH_INDEX, \
    MAIN_EVENT_LINE_NUMBER_COLUMN_INDEX, \
    CHECKER_INDEX_COLUMN_INDEX, \
    IMPACT_COLUMN_INDEX, SUBCATEGORY_LONG_DESCRIPTION_COLUMN_INDEX, \
    MERGE_KEY_COLUMN_INDEX
from swq.coverity.coverity_utils import get_filtered_report_name
from swq.common.component_mapping import no_regex_matches, ComponentMapper
from swq.common.constants import IS_WINDOWS
from swq.common.logger import LOGGER
from swq.common.file.file_utils import escape_line_breaks_in_string
from swq.common.filesystem.filesystem_utils import open_t
from swq.common.return_codes import log_and_exit, RC_WEB_API_CALL_FAILED
from swq.common.export.xlsx_exporter import XlsxExporter
from swq.common.export.csv_exporter import CsvExporter
from swq.common.export.stdout_exporter import StdOutExporter
from swq.common.export.zipped_csv_exporter import ZippedCsvExporter
from swq.map_teams.map_teams import add_team_components_to_row, \
    TEAM_REPORT_EXTRA_FIELDNAMES, SENSITIVE_INFO_WARNING_MESSAGE

COVERITY_FORMAT_ERRORS_ISSUES_HEADER = [
    "strippedMainEventFilePathname", "mergeKey", "occurrenceCountForMK",
    "occurrenceNumberInMK", "checkerName", "subcategory", "type", "subtype",
    "code-language", "extra", "domain", "language", "mainEventLineNumber",
    "functionDisplayName", "functionMangledName", "category",
    "categoryDescription", "cweCategory", "impact", "impactDescription",
    "subcategoryLocalEffect", "subcategoryShortDescription",
    "subcategoryLongDescription", "mainEventFilePathname"
]

COVERITY_COMMIT_DEFECTS_ISSUES_HEADER = [
    "cid", "mergeKey", "presentInComparisonSnapshot", "firstDetectedDateTime",
    "severity", "triage_owner", "triage_externalReference", "triage_legacy",
    "triage_fixTarget", "triage_action", "triage_classification",
    "customTriage_SeverityLevel", "first_occurence_checker",
    "first_occurence_file", "first_occurence_function",
    "first_occurence_extra", "first_occurence_mergeWithLowercaseFile",
    "first_occurence_subcategory", "first_occurence_mainEventLineNumber",
    "first_occurence_mainEventDescription", "first_occurence_componentName",
    "first_occurence_componentDefaultOwner"
]

SUDS_IMPORTED = True

try:
    from suds.client import Client
    from suds.transport.http import HttpTransport
    from suds.wsse import Security, UsernameToken
except ImportError:
    LOGGER.warning("\nTriage history isn't enabled. "
                   "Please install suds module\n")
    SUDS_IMPORTED = False
else:

    class UnverifiedHttpsTransport(HttpTransport):
        """UnverifiedHttpsTransport class"""

        # pylint warnings W0235 & W0231
        # useless super delegation
        # __init__ is not called
        # def __init__(self, *args, **kwargs):
        #   super(UnverifiedHttpsTransport, self).__init__(*args, **kwargs)

        def u2handlers(self):
            handlers = super(UnverifiedHttpsTransport, self).u2handlers()
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            handlers.append(urllib.request.HTTPSHandler(context=context))
            return handlers

    class WebServiceClient:
        """WebServiceClient class"""
        def __init__(self, config, webservice_type):
            self.__config = config

            if webservice_type == 'configuration':
                self.wsdl_file = self.__config.webapi_url + \
                    '/ws/v9/configurationservice?wsdl'
            elif webservice_type == 'defect':
                self.wsdl_file = self.__config.webapi_url + \
                    '/ws/v9/defectservice?wsdl'
            else:
                raise "unknown web service type: " + webservice_type

            self.client = Client(self.wsdl_file,
                                 transport=UnverifiedHttpsTransport())
            self.security = Security()
            self.token = UsernameToken(self.__config.webapi_coverity_user,
                                       self.__config.webapi_coverity_passcode)
            self.security.tokens.append(self.token)
            self.client.set_options(wsse=self.security)

        def get_wsdl(self):
            """Prints client data"""
            print(self.client)

    class DefectServiceClient(WebServiceClient):
        """DefectServiceClient class"""
        def __init__(self, config):
            WebServiceClient.__init__(self, config, 'defect')

    class ConfigServiceClient(WebServiceClient):
        """ConfigServiceClient class"""
        def __init__(self, config):
            WebServiceClient.__init__(self, config, 'configuration')


def _create_exporters(config, basename, export_path, default_sheet=""):
    def _xlsx_exporter_func():
        filename = '{}.xlsx'.format(basename)
        if default_sheet:
            filename = '{}-{}.xlsx'.format(basename, default_sheet)
        return XlsxExporter(path.join(export_path, filename))

    def _csv_exporter_func():
        return CsvExporter(path.join(export_path, basename))

    def _csv_zip_exporter_func():
        return ZippedCsvExporter(path.join(export_path, basename))

    def _stdout_exporter_func():
        return StdOutExporter()

    def _vscode_exporter_func():
        exporter = StdOutExporter()

        def _vscode_formatter(row: list):
            formatted_string = '{}:{}:0: {}, {}, {}, {}'.format(
                row[ERROR_EXPORT_TABLE_MAIN_EVENT_FILEPATH_INDEX],
                row[MAIN_EVENT_LINE_NUMBER_COLUMN_INDEX],
                row[CHECKER_INDEX_COLUMN_INDEX], row[IMPACT_COLUMN_INDEX],
                row[SUBCATEGORY_LONG_DESCRIPTION_COLUMN_INDEX],
                row[MERGE_KEY_COLUMN_INDEX])

            return formatted_string

        exporter.set_formatter(_vscode_formatter)

        return exporter

    export_formats_to_exporter = []
    for export_format in config.export_formats:
        if f"_{export_format}_exporter_func" in locals():
            export_formats_to_exporter.append(
                locals()[f"_{export_format}_exporter_func"]())

    return export_formats_to_exporter


def generate_sheet(exporter, sheet_name, rows, enable_filters: bool = False):
    """Creates sheet and appends it with provided rows"""
    sheet = exporter.create_sheet(sheet_name)
    sheet.append_rows(rows)

    if enable_filters:
        sheet.enable_filters()

    exporter.save()


def read_cov_format_errors(coverity_json_filepath):
    """Reads coverity format errors from filepath"""
    cov_format_errors_issues_list = []
    with open_t(coverity_json_filepath) as json_file:
        data = load(json_file)
        issues = data["issues"]
        issue_count = 0
        unique_issues = 0
        for issue in issues:
            checker_properties = issue["checkerProperties"]
            issue_row = [
                issue.get("strippedMainEventFilePathname", ""),
                issue.get("mergeKey", ""),
                issue.get("occurrenceCountForMK", ""),
                issue.get("occurrenceNumberInMK", ""),
                issue.get("checkerName", ""),
                issue.get("subcategory", ""),
                issue.get("type", ""),
                issue.get("subtype", ""),
                issue.get("code-language", ""),
                issue.get("extra", ""),
                issue.get("domain", ""),
                issue.get("language", ""),
                issue.get("mainEventLineNumber", ""),
                issue.get("functionDisplayName", ""),
                issue.get("functionMangledName", ""),
                checker_properties["category"],
                checker_properties["categoryDescription"],
                checker_properties["cweCategory"],
                checker_properties["impact"],
                checker_properties["impactDescription"],
                checker_properties["subcategoryLocalEffect"],
                checker_properties["subcategoryShortDescription"],
                checker_properties["subcategoryLongDescription"],
                issue.get("mainEventFilePathname", ""),
            ]
            # only append row if "occurrenceNumberInMK" is 1,
            # which means its entry point for a warning,
            # and not the complete trace
            if str(issue.get("occurrenceNumberInMK", "")) == "1":
                cov_format_errors_issues_list.append(issue_row)
                unique_issues += 1
            issue_count += 1
        LOGGER.info("Processed {} issues in {}".format(issue_count,
                                                       coverity_json_filepath))
    return cov_format_errors_issues_list


def _get_view_contents(config, view_type):
    headers = {"Accept": "application/json"}
    url = "{}/api/viewContents/{}/v1/{}?projectId={}&rowCount=-1".format(
        config.webapi_url, view_type, config.webapi_view_name,
        config.webapi_project_name)
    LOGGER.info("Making url request to %s", url)
    response = get(url,
                   auth=(config.webapi_coverity_user,
                         config.webapi_coverity_passcode),
                   headers=headers,
                   verify=False)

    if not response.ok:
        response.raise_for_status()
        LOGGER.error(
            "Error with url request url %s\n\n%headers=%s\n\nresponse=%s", url,
            headers, response)
        log_and_exit(RC_WEB_API_CALL_FAILED)

    return loads(response.content)


def _get_filtered_format_errors_rows(config, csv_values):
    filtered_csv_values = [
        csv_row for csv_row in csv_values if no_regex_matches(
            config.translation_units_blacklist,
            csv_row[ERROR_EXPORT_TABLE_MAIN_EVENT_FILEPATH_INDEX].replace(
                '\\', '/'))
    ]
    return filtered_csv_values


def _get_format_errors_rows(config, coverity_json_filepath):
    csv_values = [COVERITY_FORMAT_ERRORS_ISSUES_HEADER]
    cov_format_errors_issues_list = read_cov_format_errors(
        coverity_json_filepath)
    if config.codeowners_file:
        LOGGER.warning(SENSITIVE_INFO_WARNING_MESSAGE)
        component_mapper = ComponentMapper(config.codeowners_file)
        csv_values[0].extend(TEAM_REPORT_EXTRA_FIELDNAMES)
        csv_values.extend([
            add_team_components_to_row(
                row, ERROR_EXPORT_TABLE_MAIN_EVENT_FILEPATH_INDEX,
                component_mapper, config.only_last_team)
            for row in cov_format_errors_issues_list if row
        ])
    else:
        csv_values.extend(
            [row for row in cov_format_errors_issues_list if row])

    return csv_values


def _get_filtered_cov_commit_defects_rows(config, project_root,
                                          cov_commit_defects_issues_list):
    filtered_csv_values = [COVERITY_COMMIT_DEFECTS_ISSUES_HEADER.copy()]

    if config.codeowners_file:
        component_mapper = ComponentMapper(config.codeowners_file)
        filtered_csv_values[0].extend(TEAM_REPORT_EXTRA_FIELDNAMES)
        for filtered_issues_row in cov_commit_defects_issues_list:
            filepath_in_row = filtered_issues_row[
                PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX]
            if no_regex_matches(config.translation_units_blacklist,
                                filepath_in_row):
                filtered_issues_row[
                    PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX] = \
                        filepath_in_row.replace(project_root, '')
                filtered_issues_row = add_team_components_to_row(
                    filtered_issues_row,
                    PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX,
                    component_mapper, config.only_last_team)
                filtered_csv_values.extend([filtered_issues_row])
    else:
        for filtered_issues_row in cov_commit_defects_issues_list:
            filepath_in_row = filtered_issues_row[
                PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX]
            if no_regex_matches(config.translation_units_blacklist,
                                filepath_in_row):
                filtered_issues_row[
                    PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX] = \
                        filepath_in_row.replace(project_root, '')
                filtered_csv_values.extend([filtered_issues_row])

    return filtered_csv_values


def _get_cov_commit_defects_rows(config, project_root,
                                 cov_commit_defects_issues_list):
    csv_values = [COVERITY_COMMIT_DEFECTS_ISSUES_HEADER.copy()]
    if config.codeowners_file:
        LOGGER.warning(SENSITIVE_INFO_WARNING_MESSAGE)
        component_mapper = ComponentMapper(config.codeowners_file)
        csv_values[0].extend(TEAM_REPORT_EXTRA_FIELDNAMES)
        for issues_row in cov_commit_defects_issues_list:
            issues_row[PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX] = \
                issues_row[
                    PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX].replace(
                        project_root, '')
            issues_row = add_team_components_to_row(
                issues_row, PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX,
                component_mapper, config.only_last_team)
            csv_values.extend([issues_row])
    else:
        for issues_row in cov_commit_defects_issues_list:
            issues_row[PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX] = \
                issues_row[
                    PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX].replace(
                        project_root, '')
            csv_values.extend([issues_row])

    return csv_values


def _get_webapi_export_rows(config, data):
    export_triage_history_enabled = \
        config.include_triage_history and SUDS_IMPORTED
    export_triage_history = export_triage_history_enabled

    report_column_names = []
    unique_triage_column_names = ['userCreated', 'dateCreated', 'comment']
    custom_triage_column_names = ['triage_num', 'triage_total']
    triage_mandatory_column_name = 'status'

    if export_triage_history_enabled:
        if not config.triage_store:
            export_triage_history = False
            LOGGER.warning('Triage history will not be exported. '
                           'Check \'TRIAGE_STORE\' parameter in helper '
                           'configuration file.')

        if triage_mandatory_column_name not in list(
                column['name'] for column in data['columns']):
            export_triage_history = False
            LOGGER.warning(
                'Triage history will not be exported. '
                'Project view \'%s\' does not have mandatory column \'%s\'',
                config.webapi_view_name, triage_mandatory_column_name)

        defect_service_client = DefectServiceClient(config)
        config_service_client = ConfigServiceClient(config)

        triage_store_id_obj = \
            config_service_client.client.factory.create('triageStoreIdDataObj')
        triage_store_id_obj.name = config.triage_store

    for column_name in data['columns']:
        if export_triage_history and \
                (column_name['name'] == triage_mandatory_column_name):
            report_column_names.append(column_name['name'])
            report_column_names += custom_triage_column_names
            continue
        report_column_names.append(column_name['name'])

    if export_triage_history:
        for triage_column_name in unique_triage_column_names:
            report_column_names.append("triage_{}".format(triage_column_name))

    csv_values = []
    csv_values.extend([report_column_names])

    for row in data['rows']:
        csv_triage_values = []
        rows_in_view = []
        report_row_data = {}
        for column_name in report_column_names:
            if column_name in data['rows'][0]:
                report_row_data[column_name] = row[column_name]
            else:
                report_row_data[column_name] = None

        if export_triage_history and row['status'] in ('Triaged', 'Dismissed'):
            merged_defect_id_obj = defect_service_client.client.factory.create(
                'mergedDefectIdDataObj')
            merged_defect_id_obj.cid = row['cid']
            triage_history_data = \
                defect_service_client.client.service.getTriageHistory(
                    merged_defect_id_obj, triage_store_id_obj)

            if len(triage_history_data) == 0:
                LOGGER.warning(
                    'Issue %s has Triaged status, but no triage \
                    records obtained. '
                    'Check triage store name specified.', row['cid'])

            triage_total_records = len(triage_history_data)
            triage_record_number = triage_total_records
            report_row_data['triage_num'] = triage_record_number
            report_row_data['triage_total'] = triage_total_records
            for triage_records in triage_history_data:
                rows_in_triage = []
                triage_row_key_value = {}
                triage_row_key_value['cid'] = row['cid']
                triage_row_key_value['triage_num'] = triage_record_number
                triage_row_key_value['triage_total'] = triage_total_records
                for item_attributes in triage_records.attributes:
                    attribute_name = item_attributes.attributeDefinitionId.name
                    attribute_value = item_attributes.attributeValueId.name
                    triage_row_key_value[attribute_name] = attribute_value
                for column_name in report_column_names:
                    if column_name.startswith('triage_') and (
                            column_name not in custom_triage_column_names):
                        column_name = column_name[7:]
                    if column_name in triage_row_key_value:
                        rows_in_triage.\
                            append(triage_row_key_value[column_name])
                    else:
                        rows_in_triage.append(None)
                triage_record_number -= 1
                csv_triage_values.extend([rows_in_triage])
        for column_name in report_column_names:
            rows_in_view.append(report_row_data[column_name])
        csv_values.extend([rows_in_view])
        if csv_triage_values:
            csv_values.extend(csv_triage_values)
    return csv_values


def _get_os_formatted_project_root(config):
    project_root = ''

    if IS_WINDOWS:
        project_root = path.splitdrive(config.project_root)[1].replace(
            "\\", "/") + '/'
    else:
        project_root = path.normpath(config.project_root) + '/'

    return project_root


def read_cov_commit_defects(coverity_json_filepath):
    """Reads coverity commit defects from filepath"""
    cov_commit_defects_issues_list = []
    with open_t(coverity_json_filepath) as json_file:
        data = load(json_file)
        issues = data["issueInfo"]
        issue_count = 0
        for issue in issues:
            issue_occurrences = issue["occurrences"]
            first_occurence = issue_occurrences[0]
            issue_triage = issue["triage"]
            issue_custom_triage = issue["customTriage"]
            issue_row = [
                issue.get("cid", ""),
                issue.get("mergeKey", ""),
                issue.get("presentInComparisonSnapshot", ""),
                issue.get("firstDetectedDateTime",
                          ""), issue_triage["severity"], issue_triage["owner"],
                issue_triage["externalReference"], issue_triage["legacy"],
                issue_triage["fixTarget"], issue_triage["action"],
                issue_triage["classification"],
                issue_custom_triage["Severity Level"],
                first_occurence.get("checker", ""),
                first_occurence.get("file", ""),
                first_occurence.get("function", ""),
                escape_line_breaks_in_string(first_occurence.get("extra", "")),
                first_occurence.get("mergeWithLowercaseFile", ""),
                first_occurence.get("subcategory", ""),
                first_occurence.get("mainEventLineNumber", ""),
                escape_line_breaks_in_string(
                    first_occurence.get("mainEventDescription", "")),
                first_occurence.get("componentName", ""),
                first_occurence.get("componentDefaultOwner", "")
            ]
            cov_commit_defects_issues_list.append(issue_row)
            issue_count += 1
        LOGGER.info("Processed {} issues in {}".format(issue_count,
                                                       coverity_json_filepath))
    return cov_commit_defects_issues_list


def cov_format_errors_export(config, coverity_json_filepath):
    """Exports coverity format errors to filepath"""
    basename = path.splitext(path.basename(coverity_json_filepath))[0]
    dirpath = path.dirname(coverity_json_filepath)
    format_errors_rows = _get_format_errors_rows(config,
                                                 coverity_json_filepath)

    if config.translation_units_blacklist:
        filtered_format_errors_rows = _get_filtered_format_errors_rows(
            config, format_errors_rows)
        filtered_report_name = get_filtered_report_name(coverity_json_filepath)

        exporters = _create_exporters(config, filtered_report_name, dirpath)
        for exporter in exporters:
            generate_sheet(exporter, 'export', filtered_format_errors_rows,
                           True)

    is_export_to_stdout = 'stdout' in config.export_formats or \
        'vscode' in config.export_formats
    if not (config.translation_units_blacklist and is_export_to_stdout):
        LOGGER.info('cov_format_errors_export')

        exporters = _create_exporters(config, basename, dirpath)
        for exporter in exporters:
            generate_sheet(exporter, 'export', format_errors_rows, True)


def cov_commit_defects_export(config, coverity_json_filepath):
    """Exports coverity commit defects to filepath"""
    LOGGER.info("cov_commit_defects_export")
    cov_commit_defects_issues_list = read_cov_commit_defects(
        coverity_json_filepath)

    basename = path.splitext(path.basename(coverity_json_filepath))[0]
    dirpath = path.dirname(coverity_json_filepath)
    project_root = _get_os_formatted_project_root(config)

    if config.translation_units_blacklist:
        filtered_report_name = \
            get_filtered_report_name(coverity_json_filepath)
        filtered_cov_commit_defects_rows = \
            _get_filtered_cov_commit_defects_rows(
                config, project_root, cov_commit_defects_issues_list)
        exporters = _create_exporters(config, filtered_report_name, dirpath)
        for exporter in exporters:
            generate_sheet(exporter, 'export',
                           filtered_cov_commit_defects_rows, True)

    cov_commit_defects_rows = _get_cov_commit_defects_rows(
        config, project_root, cov_commit_defects_issues_list)

    exporters = _create_exporters(config, basename, dirpath)
    for exporter in exporters:
        generate_sheet(exporter, 'export', cov_commit_defects_rows, True)


def coverity_connect_webapi_export(config):
    """Exports coverity webapi data"""
    LOGGER.info("coverity_connect_webapi_export")
    view_type = 'issues'
    jdata = _get_view_contents(config, view_type)
    data = jdata['viewContentsV1']

    with open_t(config.view_contents_export_filepath, mode='w') as opened_file:
        dump(data, opened_file, ensure_ascii=False, indent=4)

    basename = path.splitext(
        path.basename(config.view_contents_export_filepath))[0]
    dirpath = path.dirname(config.view_contents_export_filepath)
    webapi_export_rows = _get_webapi_export_rows(config, data)
    exporters = _create_exporters(config, basename, dirpath)

    for exporter in exporters:
        generate_sheet(exporter, config.webapi_view_name, webapi_export_rows,
                       True)
