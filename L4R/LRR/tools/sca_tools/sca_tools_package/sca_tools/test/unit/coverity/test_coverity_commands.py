""" Tests for coverity/coverity_commands.py """

from os import path as os_path
from unittest import TestCase, mock
from unittest.mock import patch
from swq.common.return_codes import RC_MISSING_PARAMETER
from swq.coverity import coverity_commands


class TestCoverityCommands(TestCase):
    """ TestCoverityCommands class """
    def setUp(self):
        self.config = mock.Mock(coverity_bin_path='/foo/bar',
                                auth_key_filepath=None,
                                platform_command_extension='',
                                coverity_commit_url=None,
                                coverity_commit_stream='TestStream',
                                coverity_commit_host='localhost',
                                coverity_commit_dataport='8080',
                                coverity_project_path='/cov/project',
                                project_root='/cov',
                                cov_export_blacklist=None,
                                cov_export_whitelist=None,
                                cov_analyze_option_list=None,
                                cov_build_option_list=None,
                                build_command=None,
                                run_desktop_extra_options=None)
        self.fast_fail = True
        self.build_shell = False
        self.use_logger = True
        self.silent = False
        self.output_filepath = None
        self.cwd = None

    def test_get_os_command_exe(self):
        """ Test get_os_command_exe """
        executable_name = 'cov'
        expected_return = os_path.normpath('/foo/bar/cov')
        return_value = coverity_commands.get_os_command_exe(
            self.config, executable_name)
        self.assertEqual(expected_return, return_value)

        self.config.platform_command_extension = '.exe'
        expected_return = os_path.normpath('/foo/bar/cov.exe')
        return_value = coverity_commands.get_os_command_exe(
            self.config, executable_name)
        self.assertEqual(expected_return, return_value)

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    @patch.object(
        coverity_commands,
        'extend_coverity_command_with_connection_options')
    def test_cov_commit_defects(self, mock_extend, run_command,
                                get_os_command_exe):
        """ Test cov_commit_defects """
        self.fast_fail = False

        # output_path is not specified
        get_os_command_exe.return_value = 'cov-commit-defects'
        command_string = \
            "{} --stream {} --dir {}".format(
                get_os_command_exe.return_value,
                self.config.coverity_commit_stream,
                self.config.coverity_project_path)
        coverity_commands.cov_commit_defects(self.config, '')
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.config.project_root)
        mock_extend.assert_called_once_with(
            self.config, command_string.split(' '))

        # reset mocks
        run_command.reset_mock()
        mock_extend.reset_mock()

        # output_path is specified
        output_path = 'out'
        get_os_command_exe.return_value = 'cov-commit-defects'
        command_string = \
            "{} --stream {} --dir {} --preview-report-v2 {}".format(
                get_os_command_exe.return_value,
                self.config.coverity_commit_stream,
                self.config.coverity_project_path,
                output_path)

        coverity_commands.cov_commit_defects(self.config, output_path)
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.config.project_root)
        mock_extend.assert_called_once_with(
            self.config, command_string.split(' '))

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    def test_coverity_export_errors_json(
        self, run_command, get_os_command_exe):
        """ Test coverity_export_errors_json """
        self.fast_fail = False
        get_os_command_exe.return_value = 'cov-format-errors'
        json_file = 'foo.json'
        command_begins = "{} --dir {}".format(
            get_os_command_exe.return_value, self.config.coverity_project_path)
        with patch('swq.coverity.coverity_commands._get_version_of_json_format'
                   ) as json_version:
            json_version.return_value = 6
            command_ends = " --json-output-v6 {}".format(json_file)
            command_string = command_begins + command_ends
            coverity_commands.coverity_export_errors_json(
                self.config, json_file)
            run_command.assert_called_once_with(
                command_string,
                fast_fail=self.fast_fail,
                build_shell=self.build_shell,
                use_logger=self.use_logger,
                silent=self.silent,
                output_filepath=self.output_filepath,
                cwd=self.config.project_root)
            run_command.reset_mock()

            json_version.return_value = 8
            command_ends = " --json-output-v8 {}".format(json_file)
            self.config.cov_export_blacklist = 'blacklist.txt'
            command_string = command_begins
            command_string += " --exclude-files {}".format(
                self.config.cov_export_blacklist)
            command_string += command_ends
            coverity_commands.coverity_export_errors_json(
                self.config, json_file)
            run_command.assert_called_once_with(
                command_string,
                fast_fail=self.fast_fail,
                build_shell=self.build_shell,
                use_logger=self.use_logger,
                silent=self.silent,
                output_filepath=self.output_filepath,
                cwd=self.config.project_root)
            run_command.reset_mock()

            self.config.cov_export_whitelist = 'whitelist.txt'
            command_string = command_begins
            command_string += " --exclude-files {} --include-files {}".format(
                self.config.cov_export_blacklist,
                self.config.cov_export_whitelist)
            command_string += command_ends
            coverity_commands.coverity_export_errors_json(
                self.config, json_file)
            run_command.assert_called_once_with(
                command_string,
                fast_fail=self.fast_fail,
                build_shell=self.build_shell,
                use_logger=self.use_logger,
                silent=self.silent,
                output_filepath=self.output_filepath,
                cwd=self.config.project_root)
            run_command.reset_mock()

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    def test_coverity_export_errors_html(
        self, run_command, get_os_command_exe):
        """ Test coverity_export_errors_html """
        self.fast_fail = False
        get_os_command_exe.return_value = 'cov-format-errors'

        cov_errors_html_dirpath = 'dir'
        self.config.cov_export_blacklist = 'blacklist.txt'
        self.config.cov_errors_html_dirpath = cov_errors_html_dirpath

        command_begins = "{} --dir {}".format(
            get_os_command_exe.return_value, self.config.coverity_project_path)
        command_ends = " --html-output {}".format(cov_errors_html_dirpath)

        command_string = command_begins
        command_string += " --exclude-files {}".format(
            self.config.cov_export_blacklist)
        command_string += command_ends
        coverity_commands.coverity_export_errors_html(self.config)
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.config.project_root)
        run_command.reset_mock()

        self.config.cov_export_whitelist = 'whitelist.txt'
        command_string = command_begins
        command_string += " --exclude-files {} --include-files {}".format(
            self.config.cov_export_blacklist,
            self.config.cov_export_whitelist)
        command_string += command_ends
        coverity_commands.coverity_export_errors_html(self.config)
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.config.project_root)
        run_command.reset_mock()

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    def test_run_coverity_analyze(self, run_command, get_os_command_exe):
        """ Test run_coverity_analyze """
        self.fast_fail = False
        get_os_command_exe.return_value = 'cov-analyze'
        command_string = "{} --dir {} --strip-path {}".format(
            get_os_command_exe.return_value, self.config.coverity_project_path,
            os_path.normpath(self.config.project_root))
        coverity_commands.run_coverity_analyze(self.config)
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.config.project_root)
        run_command.reset_mock()

        self.config.cov_analyze_option_list = ['option1', 'option2']
        for item in self.config.cov_analyze_option_list:
            command_string += " {}".format(item)
        coverity_commands.run_coverity_analyze(self.config)
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.config.project_root)

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    def test_list_coverity_translation_units(self, run_command,
                                             get_os_command_exe):
        """ Test list_coverity_translation_units """
        self.fast_fail = False
        get_os_command_exe.return_value = 'cov-manage-emit'
        command_string = "{} --dir {} --tus-per-psf=latest list".format(
            get_os_command_exe.return_value, self.config.coverity_project_path)
        coverity_commands.list_coverity_translation_units(self.config)
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.cwd)

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    def test_create_coverity_config_for_compiler(self, run_command,
                                                 get_os_command_exe):
        """ Test create_coverity_config_for_compiler """
        self.fast_fail = False
        get_os_command_exe.return_value = 'cov-configure'
        with patch('os.chdir'), patch('os.path.normpath') as normpath:
            coverity_config = '/cov/config/coverity_config.xml'
            compiler = '--gcc'
            normpath.return_value = coverity_config
            command_string = "{} --config {} {}".format(
                get_os_command_exe.return_value, coverity_config, compiler)
            coverity_commands.create_coverity_config_for_compiler(
                self.config, compiler)
            run_command.assert_called_once_with(
                command_string,
                fast_fail=self.fast_fail,
                build_shell=self.build_shell,
                use_logger=self.use_logger,
                silent=self.silent,
                output_filepath=self.output_filepath,
                cwd=self.config.project_root)

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    def test_coverity_filter_translation_unit(self, run_command,
                                              get_os_command_exe):
        """ Test coverity_filter_translation_unit """
        self.fast_fail = False
        get_os_command_exe.return_value = 'cov-manage-emit'
        filter_line = 'line1\nline2'
        command_string = "{} --dir {} --tu-pattern \"file('{}')\" delete".\
            format(
                get_os_command_exe.return_value,
                self.config.coverity_project_path,
                filter_line
            )
        with patch('swq.coverity.coverity_commands.LOGGER'):
            coverity_commands.coverity_filter_translation_unit(
                self.config, filter_line)
            run_command.assert_called_once_with(
                command_string,
                fast_fail=self.fast_fail,
                build_shell=self.build_shell,
                use_logger=self.use_logger,
                silent=self.silent,
                output_filepath=self.output_filepath,
                cwd=self.cwd)

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    def test_run_coverity_build(self, run_command, get_os_command_exe):
        """ Test run_coverity_build """
        self.fast_fail = False
        get_os_command_exe.return_value = 'cov-build'
        self.config.build_command = 'build.sh'
        coverity_config = os_path.normpath(
            os_path.join(self.config.project_root,
                         self.config.coverity_project_path, 'config',
                         'coverity_config.xml'))
        command_string = "{} --dir {} --config {} {}".format(
            get_os_command_exe.return_value, self.config.coverity_project_path,
            coverity_config, self.config.build_command)
        with patch('os.chdir'):
            coverity_commands.run_coverity_build(self.config,
                                                 self.config.build_command)
            run_command.assert_called_once_with(
                command_string,
                fast_fail=self.fast_fail,
                build_shell=self.build_shell,
                use_logger=self.use_logger,
                silent=self.silent,
                output_filepath=self.output_filepath,
                cwd=self.config.project_root)
            run_command.reset_mock()
            self.config.cov_build_option_list = ['option']
            command_string = "{} --dir {} option --config {} {}".format(
                get_os_command_exe.return_value,
                self.config.coverity_project_path, coverity_config,
                self.config.build_command)
            coverity_commands.run_coverity_build(self.config,
                                                 self.config.build_command)
            run_command.assert_called_once_with(
                command_string,
                fast_fail=self.fast_fail,
                build_shell=self.build_shell,
                use_logger=self.use_logger,
                silent=self.silent,
                output_filepath=self.output_filepath,
                cwd=self.config.project_root)

    @patch('swq.common.command.command_decorator.run_command')
    def test_git_rev_parse(self, run_command):
        """ Test git_rev_parse """
        self.fast_fail = False
        command_string = \
            f'git -C {self.config.project_root} rev-parse --verify HEAD'

        coverity_commands.git_rev_parse(self.config)
        run_command.assert_called_once_with(
            command_string,
            fast_fail=self.fast_fail,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.cwd)

    def test_get_version_of_json_format(self):
        """ Test _get_version_of_json_format """
        self.config.cli_version_string = 'Coverity Analysis 2021.02 mock mock'
        expected_version = 8
        actual_version = coverity_commands._get_version_of_json_format(
            self.config)
        self.assertEqual(expected_version, actual_version)

        self.config.cli_version_string = 'Coverity Analysis 2019.12 mock mock'
        expected_version = 6
        actual_version = coverity_commands._get_version_of_json_format(
            self.config)
        self.assertEqual(expected_version, actual_version)

    @patch.object(coverity_commands, 'get_os_command_exe')
    @patch('swq.common.command.command_decorator.run_command')
    @patch.object(
        coverity_commands,
        'extend_coverity_command_with_connection_options')
    def test_run_cov_run_desktop(
        self, mock_extend, run_command, get_os_command_exe):
        """ Test run_cov_run_desktop """
        cov_run_desktop_binary = 'cov-run-desktop'
        get_os_command_exe.return_value = cov_run_desktop_binary

        # config is not specified
        self.config.coverity_config_filepath = ''

        command_string = \
            "{} --stream {} --dir {} --analyze-captured-source".format(
                cov_run_desktop_binary,
                self.config.coverity_commit_stream,
                self.config.coverity_project_path)

        coverity_commands.run_cov_run_desktop(self.config)

        run_command.assert_called_once_with(
            command_string,
            fast_fail=False,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.cwd)

        mock_extend.assert_called_once_with(
            self.config, command_string.split(' '))

        # reset mocks
        run_command.reset_mock()
        mock_extend.reset_mock()

        # config is specified
        self.config.coverity_config_filepath = 'config'
        command_string += ' --config {}'.format(
            self.config.coverity_config_filepath)

        coverity_commands.run_cov_run_desktop(self.config)

        run_command.assert_called_once_with(
            command_string,
            fast_fail=False,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.cwd)

        mock_extend.assert_called_once_with(
            self.config, command_string.split(' '))

        # reset mocks
        run_command.reset_mock()
        mock_extend.reset_mock()
        self.config.coverity_config_filepath = None

        # coverity_run_desktop_extra_options is specified
        self.config.run_desktop_extra_options = ['--foo', '--bar']

        command_string = \
            "{} --stream {} --dir {} --analyze-captured-source --foo --bar".\
                format(
                    cov_run_desktop_binary,
                    self.config.coverity_commit_stream,
                    self.config.coverity_project_path)

        coverity_commands.run_cov_run_desktop(self.config)

        run_command.assert_called_once_with(
            command_string,
            fast_fail=False,
            build_shell=self.build_shell,
            use_logger=self.use_logger,
            silent=self.silent,
            output_filepath=self.output_filepath,
            cwd=self.cwd)

        mock_extend.assert_called_once_with(
            self.config, command_string.split(' '))

    def test_extend_coverity_command_with_connection_options(self):
        with patch.object(coverity_commands, '_ensure_cov_env_parity') \
            as mock_ensure_parity, \
            patch.object(coverity_commands, 'log_and_exit') \
            as mock_log_and_exit:
            self.config.coverity_commit_host = ''
            self.config.coverity_commit_dataport = None

            # coverity_commit_url is specified
            command_string = []
            coverity_commit_url = 'coverity_connect.com'
            self.config.coverity_commit_url = coverity_commit_url

            coverity_commands.\
                extend_coverity_command_with_connection_options(
                    self.config, command_string
                )

            expected_command_string = ['--url', coverity_commit_url]
            self.assertEqual(command_string, expected_command_string)

            mock_ensure_parity.assert_called_once_with(self.config)
            mock_log_and_exit.assert_not_called()

            # reset mocks
            mock_ensure_parity.reset_mock()
            self.config.coverity_commit_url = ''

            # coverity_commit_host and coverity_commit_dataport are specified
            command_string = []
            coverity_commit_host = 'coverity_connect.com'
            coverity_commit_dataport = 9090

            self.config.coverity_commit_host = coverity_commit_host
            self.config.coverity_commit_dataport = coverity_commit_dataport

            coverity_commands.\
                extend_coverity_command_with_connection_options(
                    self.config, command_string
                )

            expected_command_string = \
                ['--host', coverity_commit_host,
                 '--dataport', coverity_commit_dataport]
            self.assertEqual(command_string, expected_command_string)
            mock_ensure_parity.assert_called_once_with(self.config)
            mock_log_and_exit.assert_not_called()

            # reset mocks
            mock_ensure_parity.reset_mock()
            self.config.coverity_commit_url = ''
            self.config.coverity_commit_host = ''
            self.config.coverity_commit_dataport = ''

            # auth_key_filepath is specified
            command_string = []
            auth_key_filepath = 'somepath'
            self.config.auth_key_filepath = auth_key_filepath

            coverity_commands.\
                extend_coverity_command_with_connection_options(
                    self.config, command_string
                )

            expected_command_string = \
                ['--auth-key-file', auth_key_filepath]
            self.assertEqual(command_string, expected_command_string)
            mock_ensure_parity.assert_not_called()
            mock_log_and_exit.assert_not_called()

            # reset mocks
            mock_ensure_parity.reset_mock()
            self.config.auth_key_filepath = None

            # username and password are specified
            command_string = []
            self.config.webapi_coverity_user = 'user'
            self.config.webapi_coverity_passcode = 'password'

            coverity_commands.\
                extend_coverity_command_with_connection_options(
                    self.config, command_string
                )

            expected_command_string = []
            self.assertEqual(command_string, expected_command_string)
            mock_ensure_parity.assert_called_once_with(self.config)
            mock_log_and_exit.assert_not_called()

            # reset_mocks
            self.config.webapi_coverity_user = ''
            self.config.webapi_coverity_passcode = ''

            # no credentials are specified
            expected_exception = Exception('no login data found')
            mock_log_and_exit.side_effect = expected_exception

            with self.assertRaises(Exception) as actual_exception:
                coverity_commands.\
                    extend_coverity_command_with_connection_options(
                        self.config, command_string
                    )
                self.assertEqual(expected_exception, actual_exception)
                mock_log_and_exit.assert_called_once_with(RC_MISSING_PARAMETER)
