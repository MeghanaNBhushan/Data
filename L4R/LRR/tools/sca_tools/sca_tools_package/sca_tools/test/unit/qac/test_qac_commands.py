# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac_commands.py
# ----------------------------------------------------------------------------
""" Tests for qac/qac_commands.py """

import os

from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac import qac_commands, qac_utils
from swq.common.constants import IS_WINDOWS


def _noop(argument):
    return argument


# pylint: disable=too-many-public-methods
@patch('swq.common.command.command_decorator.run_command')
class TestQacCommands(TestCase):
    """ TestQacCommands class """
    def setUp(self):
        self.config = mock.Mock(
            qacli='qacli',
            qagui='qagui',
            qac_logging_level=None,
            qac_project_path='qac/project/path',
            analyze_params=None,
            project_root='/project_root',
            project_reports_path='reports/',
            disable_optimization=False,
            optimization='--optimize',
            helper_remove_file_list='file',
            sync_build_command='build.bat',
            use_flist=None,
            analyze_file=None,
            project_sync_path_blacklist=None,
            qav_project_name='test',
            qav_project_snapshot='test',
            qav_upload_source='source',
            qav_server_url='localhost',
            qav_username='user',
            qav_password='password',
            ncf_file=mock.MagicMock(),
            get_absolute_path_or_relative_to_project_root=_noop,
            build_log_file=None,
            sync_json_file=None,
            target_baseline_filepath='target/baseline/path',
            qacli_view_extra_args=[])
        self.fast_fail = True
        self.build_shell = False
        self.use_logger = True
        self.silent = False
        self.output_filepath = None
        self.cwd = None

        self.config.ncf_file.get_result_filepath.return_value = 'ncf_file.ncf'

    def _assert_command_is_run_with_default_parameters(
        self, mock_run_command, command_string, cwd=None):
        cwd = self.cwd if not cwd else cwd
        mock_run_command.assert_called_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=cwd)

    def test_set_license_server(self, mock_run_command):
        """ Test set_license_server """
        with patch('swq.qac.qac_commands.LOGGER'):
            server_url = 'localhost'
            command_string = "{} admin --set-license-server {}".format(
                self.config.qacli, server_url)
            qac_commands.set_license_server(self.config, server_url)
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, command_string)

    def test_list_license_server(self, mock_run_command):
        """ Test list_license_server """
        command_string = "{} admin --list-license-servers".format(
            self.config.qacli)
        qac_commands.list_license_server(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_check_license_server(self, mock_run_command):
        """ Test check_license_server """
        command_string = "{} admin --check-license".format(self.config.qacli)
        qac_commands.check_license_server(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_set_debug_level(self, mock_run_command):
        """ Test set_debug_level """
        self.config.qac_logging_level = "ERROR"
        command_string = "{} admin --debug-level {}".format(
            self.config.qacli, self.config.qac_logging_level)
        qac_commands.set_debug_level(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_analyze_file(self, mock_run_command):
        """ Test analyze_file """
        self.fast_fail = False
        filepath = 'non/existing/path'
        output_log_file = 'output.csv'
        self.config.analyze_params = '--file-based-analysis'
        command_string = "{} analyze -P {} --output-progress {} {} {}".format(
            self.config.qacli, self.config.qac_project_path, output_log_file,
            self.config.analyze_params, filepath)
        qac_commands.analyze_file(self.config, filepath, output_log_file)
        self.cwd = self.config.project_root
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_set_default_config(self, mock_run_command):
        """ Test set_default_config """
        command_string = "{} admin --qaf-project {} --set-default-config \
--config Initial".format(self.config.qacli, self.config.qac_project_path)
        qac_commands.set_default_config(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_set_source_code_root(self, mock_run_command):
        """ Test set_source_code_root """
        command_string = \
            "{} admin --qaf-project {} --set-source-code-root {}".format(
                self.config.qacli, self.config.qac_project_path,
                self.config.project_root)
        qac_commands.set_source_code_root(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_list_config_files(self, mock_run_command):
        """ Test list_config_files """
        command_string = \
            "{} admin --qaf-project {} --list-config-files".format(
                self.config.qacli, self.config.qac_project_path)
        qac_commands.list_config_files(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    @patch('swq.qac.qac_commands.cpu_count')
    def test_export_report(self, mock_cpu_count, mock_run_command):
        """ Test export_report """
        mock_cpu_count.return_value = 4
        report_type = 'MDR'
        parallel = False
        ignore_dependencies = False
        command_string = "{} report -P \"{}\" --type {}".format(
            self.config.qacli, self.config.qac_project_path, report_type)
        qac_commands.export_report(self.config,
                                   report_type,
                                   parallel=parallel,
                                   ignore_dependencies=ignore_dependencies)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

        parallel = True
        ignore_dependencies = False
        command_string = "{} report -j 4 -P \"{}\" --type {}".format(
            self.config.qacli, self.config.qac_project_path, report_type)
        qac_commands.export_report(self.config,
                                   report_type,
                                   parallel=parallel,
                                   ignore_dependencies=ignore_dependencies)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

        ignore_dependencies = True
        command_string = "{} report --ignore -j 4 -P \"{}\" --type {}".format(
            self.config.qacli, self.config.qac_project_path, report_type)
        qac_commands.export_report(self.config,
                                   report_type,
                                   parallel=parallel,
                                   ignore_dependencies=ignore_dependencies)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_set_up_project(self, mock_run_command):
        """ Test set_up_project """
        with patch('swq.qac.qac_commands.LOGGER'):
            compiler_list = '--gcc'
            appendix = ['appendix']
            command_string = \
                "{} admin --qaf-project-config -P {} {} {}".format(
                    self.config.qacli,
                    self.config.qac_project_path,
                    compiler_list,
                    appendix[0])
            qac_commands.set_up_project(self.config, compiler_list, appendix)
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, command_string)

    def test_export_project_summary(self, mock_run_command):
        """ Test export_project_summary """
        self.fast_fail = False
        with patch.object(qac_utils, 'has_summary_export') as \
                mock_has_summary_export:
            mock_has_summary_export.return_value = False
            command_string = \
                "{} view --qaf-project \"{}\" -m XML -o \"{}\"".format(
                    self.config.qacli, self.config.qac_project_path,
                    self.config.project_reports_path)
            qac_commands.export_project_summary(self.config)
            self.silent = True
            self.use_logger = False
            self.cwd = self.config.project_root
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, command_string)

            mock_has_summary_export.return_value = True
            command_string = "{} view --qaf-project \"{}\" -t SUMMARY -m \
XML -o \"{}\"".format(self.config.qacli, self.config.qac_project_path,
                      self.config.project_reports_path)
            qac_commands.export_project_summary(self.config)
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, command_string)

    def test_export_formatted_project_analysis(self, mock_run_command):
        """ Test export_formatted_project_analysis """
        self.fast_fail = False
        self.use_logger = False
        self.silent = True
        format_sequence = [
            '%u', '%F', '%l', '%c', '%p:%N', '\\"%t\\"', '%Y', '%S',
            '\\"%j\\"', '\\"%G\\"', '\\"%r\\"'
        ]
        command_string = "{} view --qaf-project \"{}\" --suppressed-messages \
--rules --medium STDOUT --format {}".format(self.config.qacli,
                                            self.config.qac_project_path,
                                            ','.join(format_sequence))
        qac_commands.export_formatted_project_analysis(self.config)
        self.cwd = self.config.project_root
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_qac_suppress(self, mock_run_command):
        """ Test qac_suppress """
        self.fast_fail = False
        module = 'module_name'
        filepath = 'path/to/file'
        command_string = \
            "{} pprops --qaf-project \"{}\" -c {} -O {} --set-options".format(
                self.config.qacli, self.config.qac_project_path, module,
                filepath)

        qac_commands.qac_suppress(self.config, module, filepath)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_sync_project_json(self, mock_run_command):
        """ Test sync_project_json """
        self.fast_fail = False
        self.config.actual_sync_json = 'path/to/file'
        command_string_optimization = \
            "{} sync --qaf-project \"{}\" {} --type JSON {}".format(
                self.config.qacli, self.config.qac_project_path,
                self.config.optimization,
                self.config.actual_sync_json)
        command_string_no_optimization = \
            "{} sync --qaf-project \"{}\" --type JSON {}".format(
                self.config.qacli, self.config.qac_project_path,
                self.config.actual_sync_json)

        qac_commands.sync_project_json(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string_optimization)

        self.config.disable_optimization = True
        qac_commands.sync_project_json(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string_no_optimization)

    def test_delete_file_to_optimize_project(self, mock_run_command):
        """ Test delete_file_to_optimize_project """
        self.fast_fail = False
        self.silent = True
        optimization_workaround_path = 'some/path/'
        command_string = \
            "{} admin --qaf-project {} --optimize --remove-files {}".format(
                self.config.qacli, self.config.qac_project_path,
                optimization_workaround_path)
        qac_commands.delete_file_to_optimize_project(
            self.config, optimization_workaround_path)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_sync_project_build_log(self, mock_run_command):
        """ Test sync_project_build_log """
        self.fast_fail = False
        self.config.actual_build_log = 'path/to/file'
        command_string_optimization = \
            "{} sync --qaf-project \"{}\" {} --type BUILD_LOG {}".format(
                self.config.qacli, self.config.qac_project_path,
                self.config.optimization, self.config.actual_build_log)
        command_string_no_optimization = \
            "{} sync --qaf-project \"{}\" --type BUILD_LOG {}".format(
                self.config.qacli, self.config.qac_project_path,
                self.config.actual_build_log)
        qac_commands.sync_project_build_log(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string_optimization)

        self.config.disable_optimization = True
        qac_commands.sync_project_build_log(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string_no_optimization)

    def test_remove_files_from_project(self, mock_run_command):
        """ Test remove_files_from_project """
        self.fast_fail = False
        command_string = \
            "{} admin --qaf-project \"{}\" -D {}".format(
                self.config.qacli, self.config.qac_project_path,
                self.config.helper_remove_file_list)
        qac_commands.remove_files_from_project(self.config)
        mock_run_command.assert_called_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.config.project_root)

    def test_sync_project_monitor(self, mock_run_command):
        """ Test sync_project_monitor """
        self.fast_fail = False
        command_string = \
            "{} admin --qaf-project \"{}\" -b \"{}\"".format(
                self.config.qacli, self.config.qac_project_path,
                self.config.sync_build_command)
        qac_commands.sync_project_monitor(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string, self.config.project_root)

    def test_s101_gen(self, mock_run_command):
        """ Test s101_gen """
        self.fast_fail = False
        command_string = "{} upload --qaf-project {} --s101-upload \
--upload-location {}".format(
            self.config.qacli, self.config.qac_project_path,
            os.path.join(self.config.qac_project_path, "s101"))
        qac_commands.s101_gen(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_list_components(self, mock_run_command):
        """ Test list_components """
        command_string = \
            "{} pprops --qaf-project \"{}\" --list-components".format(
                self.config.qacli, self.config.qac_project_path)
        qac_commands.list_components(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_vscode_output(self, mock_run_command):
        """ Test vscode_output """
        self.fast_fail = False
        self.use_logger = False
        command_string = "{} view --qaf-project \"{}\" --format \
\"%F:%l:%c: %p-%N-%r %t\" -m STDOUT ".format(self.config.qacli,
                                             self.config.qac_project_path)
        qac_commands.vscode_output(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

        self.config.use_flist = True
        self.config.analyze_file = 'file'
        command_string = "{} view --qaf-project \"{}\" --format \
\"%F:%l:%c: %p-%N-%r %t\" -m STDOUT {}\
".format(self.config.qacli, self.config.qac_project_path,
         self.config.analyze_file)
        qac_commands.vscode_output(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_setup_baseline(self, mock_run_command):
        """ Test setup_baseline """
        baseline_path = 'some/path'
        command_string = "{} baseline -P \"{}\" --baseline-type LOCAL \
--set-baseline --local-source \"{}\"".format(self.config.qacli,
                                             self.config.qac_project_path,
                                             baseline_path)
        self.config.local_baseline_cache_filepath = baseline_path

        qac_commands.setup_baseline(self.config, baseline_path)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_create_baseline(self, mock_run_command):
        """ Test create_baseline """
        with patch('swq.qac.qac_commands.LOGGER'), \
            patch('swq.qac.qac_commands.'
                  'write_sha256_to_metadata') \
            as mock_create_hashsum, \
            patch('swq.qac.qac_commands.'
                  'move_file_to_target_folder') \
            as mock_move:
            command_string = "{} baseline -P \"{}\" --baseline-type LOCAL \
--generate-baseline".format(self.config.qacli, self.config.qac_project_path)
            qac_commands.create_baseline(self.config)
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, command_string)
            mock_create_hashsum.assert_called_once_with(
                self.config.target_baseline_filepath)
            mock_move.assert_called_once_with(
                self.config.local_baseline_cache_filepath,
                self.config.target_baseline_filepath)

    def test_apply_sync_filter(self, mock_run_command):
        """ Test apply_sync_filter """
        self.fast_fail = False
        sync_filter = 'filter'
        command_string = "{} pprops --qaf-project \"{}\" --sync-setting \
FILE_FILTER --set {}".format(self.config.qacli, self.config.qac_project_path,
                             sync_filter)
        qac_commands.apply_sync_filter(self.config, sync_filter)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_apply_path_blacklist(self, mock_run_command):
        """ Test apply_path_blacklist """
        self.fast_fail = False
        module = 'module_name'
        analysis_filters_file = 'filter_file'
        toolchain = 'C'
        command_string = "{} pprops --qaf-project \"{}\" -c {} \
-O {} --set-options --toolchain {}".format(self.config.qacli,
                                           self.config.qac_project_path,
                                           module, analysis_filters_file,
                                           toolchain)
        qac_commands.apply_path_blacklist(self.config, module,
                                          analysis_filters_file, toolchain)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_apply_sync_settings(self, mock_run_command):
        """ Test apply_sync_settings """
        self.fast_fail = False
        sync_option = 'INCLUDE_PATH'
        option = '-isystem'
        command_string = "{} pprops -P {} --sync-setting {} \
--set {}".format(self.config.qacli, self.config.qac_project_path, sync_option,
                 option)
        qac_commands.apply_sync_settings(self.config, sync_option, option)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_build_project_with_and_without_shell(self, mock_run_command):
        """ Test build_project_with_shell and build_project_without_shell"""
        self.fast_fail = False
        with patch('swq.qac.qac_commands.LOGGER'), patch('os.chdir'):
            self.config.project_sync_path_blacklist = ["some/path"]
            qac_commands.build_project_with_shell(self.config)
            self.build_shell = True
            self.cwd = self.config.project_root
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, self.config.sync_build_command)

            qac_commands.build_project_without_shell(self.config)
            self.build_shell = False
            self.cwd = self.config.project_root
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, self.config.sync_build_command)

    def test_launch_gui(self, mock_run_command):
        """ Test launch_gui """
        self.fast_fail = False
        command_string = [
            self.config.qagui, "--qaf-project", self.config.qac_project_path
        ]
        if IS_WINDOWS:
            command_string = "{} --qaf-project {}".format(
                self.config.qagui, self.config.qac_project_path)
        with patch('swq.qac.qac_commands.LOGGER'), \
                patch('swq.qac.qac_commands.Popen') \
                as mock_popen:
            qac_commands.launch_gui(self.config)
            mock_popen.assert_called_once_with(command_string)
            mock_run_command.assert_not_called()

    def test_upload_qaf_project(self, mock_run_command):
        """ Test upload_qaf_project """
        self.fast_fail = False
        format_string = " ".join([
            "{} upload", "--qaf-project {}", "--qav-upload",
            "--upload-project {}", "--snapshot-name {}", "--upload-source {}",
            "--url {}", "--username {}", "--password {}"
        ])
        command_string = format_string.format(
            self.config.qacli, self.config.qac_project_path,
            self.config.qav_project_name, self.config.qav_project_snapshot,
            self.config.qav_upload_source, self.config.qav_server_url,
            self.config.qav_username, self.config.qav_password)
        qac_commands.upload_qaf_project(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_git_rev_parse(self, mock_run_command):
        """ Test git_rev_parse """
        self.fast_fail = False
        command_string = \
            f"git -C {self.config.project_root} rev-parse --verify HEAD"

        qac_commands.git_rev_parse(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_cli_version(self, mock_run_command):
        """ Test cli_version """
        self.fast_fail = False
        command_string = "{} --version".format(self.config.qacli)
        with patch('os.chdir'):
            qac_commands.cli_version(self.config)
            self._assert_command_is_run_with_default_parameters(
                mock_run_command, command_string)

    def test_cli_config_folder(self, mock_run_command):
        """ Test cli_config_folder """
        self.fast_fail = False
        command_string = \
            "{} admin --get-user-data-location".format(self.config.qacli)
        qac_commands.cli_config_folder(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_set_namerule_config(self, mock_run_command):
        """ Test set_namerule_config """
        command_string = "{} pprops --qaf-project {} -c namecheck-2.0.0 \
-T C++ -o nrf --set {}".format(self.config.qacli, self.config.qac_project_path,
                               self.config.ncf_file.get_result_filepath())
        qac_commands.set_namerule_config(self.config)
        self._assert_command_is_run_with_default_parameters(
            mock_run_command, command_string)

    def test_setup_c_as_cpp_extensions(self, mock_run_command):
        """ Test setup_c_as_cpp_extensions """
        extensions = '.c'
        language = 'C'
        command_string = "{} admin --qaf-project {} --target-language {} \
--remove-source-extension {}".format(self.config.qacli,
                                     self.config.qac_project_path, language,
                                     extensions)
        qac_commands.setup_c_as_cpp_extensions(self.config)
        mock_called_commands = []
        for call in mock_run_command.call_args_list:
            args, _ = call
            mock_called_commands.append(args[0])
        self.assertIn(command_string, mock_called_commands)
