""" Tests for swq.common/export/csv_exporter.py """

from unittest.mock import patch
from unittest import TestCase
from swq.common.export.sheet import Sheet
from swq.common.export.csv_exporter import CsvExporter


class TestCsvExporter(TestCase):
    """Test CsvExporter Class"""
    def setUp(self):
        self.filepath = "path/to/file"
        self.title = "title"
        with patch('builtins.super') as mock_super:
            mock_super.return_value = 0
            self.csv_exporter = CsvExporter(self.filepath)
            mock_super.assert_called()

    @patch("swq.common.export.csv_exporter.CsvSheet")
    def test_create_sheet(self, csv_sheet):
        """Test create_sheet() method"""

        csv_sheet_sample = Sheet(self.title)
        csv_sheet.return_value = csv_sheet_sample

        return_value = self.csv_exporter.create_sheet(self.title)

        csv_sheet.assert_called_with(self.filepath, self.title)
        self.assertEqual(return_value, csv_sheet_sample)

    def test_save(self):
        """Test save() method"""

        return_value = self.csv_exporter.save()
        self.assertEqual(return_value, self.filepath)
