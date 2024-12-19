"""Test for a the map_teams/map_teams.py"""
from os import linesep
from unittest import mock, TestCase
from unittest.mock import patch, call

from pandas import DataFrame
from swq.map_teams import map_teams
from swq.common.constants import IS_WINDOWS

INPUT_WARNINGS_REPORT = 'input_warnings_report'

_CSV_FILE_CONTENT = [['file1.c', 'bar'], ['file2.c', 'foobar']]
_CSV_FILE_COLUMNS = ['Filename', 'foo']


class TestMapTeams(TestCase):
    """Test class for the map_teams/map_teams.py"""
    def setUp(self):
        self.config = mock.Mock(input_warnings_report='report.csv',
                                codeowners_file='codeowners.txt',
                                teams_report='report_teams.csv',
                                field_delimiter=',',
                                mapping_column='Filename',
                                only_last_team=False)
        self.mock_logger = patch("swq.map_teams.map_teams.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)
        self.teams = [['core_team', 'developers'], ['core_dev']]
        self.components = ['core']

    def test_map_teams(self):
        """Test map_teams()"""
        with patch.object(map_teams, 'ComponentMapper') \
            as mock_component_mapper,\
            patch.object(map_teams, 'read_csv') as mock_read_csv, \
            patch('builtins.open') as mock_open:

            mock_read_csv.return_value = DataFrame(data=_CSV_FILE_CONTENT,
                                                   columns=_CSV_FILE_COLUMNS,
                                                   dtype=str)

            # Test case config.only_last_team = False
            mapper = mock_component_mapper.return_value
            mapper.get_teams_for_path.return_value = self.teams
            mapper.get_component_names_for_path.return_value = self.components

            expected_read_csv_calls = \
                [call(self.config.input_warnings_report,
                      delimiter=self.config.field_delimiter,
                      quotechar='"',
                      keep_default_na=False,
                      dtype=str)]

            expected_write_calls = [
                mock.call().write(
                    f'Filename,foo,Team,Components{linesep}'),
                mock.call().write(
                    f'file1.c,bar,core_dev core_team developers,\
core{linesep}'),
                mock.call().write(
                    f'file2.c,foobar,core_dev core_team developers,\
core{linesep}')
            ]

            map_teams.map_teams(self.config)
            mock_read_csv.assert_has_calls(expected_read_csv_calls)
            mock_open.assert_has_calls(expected_write_calls)
            mock_open.reset_mock()

            # Test case config.only_last_team = True
            self.config.only_last_team = True

            map_teams.map_teams(self.config)

            expected_write_calls = [
                mock.call().write(
                    f'Filename,foo,Team,Components{linesep}'),
                mock.call().write(
                    f'file1.c,bar,core_dev,core{linesep}'),
                mock.call().write(
                    f'file2.c,foobar,core_dev,core{linesep}')
            ]
            mock_open.assert_has_calls(expected_write_calls)
