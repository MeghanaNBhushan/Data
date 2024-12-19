""" Test for a the mapping of components """
import os
import unittest
from unittest import mock

from lucxbox.lib.component_mapping import ComponentMapper


class TestComponentMapping(unittest.TestCase):
    """Test class for the component mapper"""

    def setUp(self):
        self.mock_logger = mock.patch("lucxbox.lib.component_mapping.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_process_components_success(self):
        components_file = os.path.dirname(os.path.realpath(__file__)) + "/test_components"
        component_mapper = ComponentMapper(components_file)

        self.assertEqual(len(component_mapper.components), 8)
        self.assertEqual(component_mapper.components[0].team, "a")
        self.assertEqual(component_mapper.components[1].team, "b")
        self.assertEqual(component_mapper.components[2].team, "a")
        self.assertEqual(component_mapper.components[3].team, "c")

    def test_process_components_fail(self):
        components_file = "i_do_not_exist.file"

        with self.assertRaises(SystemExit) as exception:
            _ = ComponentMapper(components_file)

        self.assertEqual(exception.exception.code, -1)

    def test_get_teams_for_path(self):
        components_file = os.path.dirname(os.path.realpath(__file__)) + "/test_components"
        component_mapper = ComponentMapper(components_file)

        test_path = os.path.join(components_file, 'ws', "test.py")
        self.assertEqual(component_mapper.get_teams_for_path(path=test_path), ["a", "f"])
        test_path = os.path.join(components_file, 'ws', "test.cmd")
        self.assertEqual(component_mapper.get_teams_for_path(path=test_path), ["b", "a", "f"])
        test_path = os.path.join(components_file, 'ws', "test.undefined")
        self.assertEqual(component_mapper.get_teams_for_path(path=test_path), ["f"])
        test_path = os.path.join(components_file, 'ws', "some/other/abc/test.py")
        self.assertEqual(component_mapper.get_teams_for_path(path=test_path), ["a", "f"])
        self.assertEqual(component_mapper.get_teams_for_path(path="D:/tools/something.undefined"), ["undefined"])

    def test_components_for_path(self):
        components_file = os.path.dirname(os.path.realpath(__file__)) + "/test_components"
        component_mapper = ComponentMapper(components_file)

        test_path = os.path.join(components_file, 'ws', 'test.py')
        components = component_mapper.get_components_for_path(path=test_path)
        self.assertEqual(len(components), 2)
        self.assertEqual(components[0].team, "a")
        self.assertEqual(components[1].team, "f")

        test_path = os.path.join(components_file, 'ws', 'test.cmd')
        components = component_mapper.get_components_for_path(path=test_path)
        self.assertTrue(len(components) == 3)
        self.assertTrue(components[0].team == "b")
        self.assertTrue(components[1].team == "a")
        self.assertTrue(components[2].team == "f")
