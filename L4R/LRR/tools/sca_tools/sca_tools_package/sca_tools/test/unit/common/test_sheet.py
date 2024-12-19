""" Tests for swq.common/export/sheet.py """

from unittest.mock import patch
from unittest import TestCase, mock
from swq.common.export.sheet import Sheet


class TestSheet(TestCase):
    """Test Sheet Class"""
    def setUp(self):
        self.title = "title"
        self.sheet = Sheet(self.title)

    def test_title(self):
        """Test title() method"""
        return_value = self.sheet.title
        self.assertEqual(return_value, self.title)

    @patch.object(Sheet, 'append')
    def test_append_rows(self, append):
        """Test title() method"""
        append.return_value = 0
        rows = ['row1', 'row2', 'row3']
        self.sheet.append_rows(rows)
        append.assert_has_calls(
            [mock.call('row1'),
             mock.call('row2'),
             mock.call('row3')])
