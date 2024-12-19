""" Testing the qacw_xml """

import os
import unittest

from lucxbox.tools.qacw import qacw_xml


class TestQACXMLParsing(unittest.TestCase):

    def setUp(self):
        self.severity_files = qacw_xml.get_severity_files_from_xml(os.path.join(os.path.dirname(__file__), 'test.xml'))

    def test_xml_read_in(self):
        self.assertEqual(2, len(self.severity_files))

    def test_severity_file_filter(self):
        severity_1_2_3_files = qacw_xml.get_files_with_severity_levels(self.severity_files, [1, 2, 3])
        self.assertEqual(2, len(severity_1_2_3_files))
        severity_3_files = qacw_xml.get_files_with_severity_levels(self.severity_files, [3])
        self.assertEqual(1, len(severity_3_files))

    def test_right_number_of_findings(self):
        severity_3_files = qacw_xml.get_files_with_severity_levels(self.severity_files, [3])
        self.assertEqual(4, len(severity_3_files[0].get_all_findings()))

    def test_severity_count(self):
        severity_3_files = qacw_xml.get_files_with_severity_levels(self.severity_files, [3])
        self.assertEqual(80, severity_3_files[0].count_severity(3))

    def test_get_findings_w_severity(self):
        severity_3_files = qacw_xml.get_files_with_severity_levels(self.severity_files, [3])
        self.assertEqual(4, len(severity_3_files[0].get_findings_w_severity_levels([3, 4])))
        self.assertEqual(2, len(severity_3_files[0].get_findings_w_severity_levels([3])))

    def test_has_findings_w_severity(self):
        severity_3_files = qacw_xml.get_files_with_severity_levels(self.severity_files, [3])
        self.assertTrue(severity_3_files[0].has_finding_w_severity_levels([3]))
        self.assertTrue(severity_3_files[0].has_finding_w_severity_levels([4]))
        self.assertFalse(severity_3_files[0].has_finding_w_severity_levels([1]))

    def test_filter_findings(self):
        severity_3_file = qacw_xml.get_files_with_severity_levels(self.severity_files, [3])[0]
        severity_3_file.filter_findings([3, 4])
        self.assertEqual(4, len(severity_3_file.get_all_findings()))
        severity_3_file.filter_findings([3])
        self.assertEqual(2, len(severity_3_file.get_all_findings()))

    def test_add_finding(self):
        severity_3_file = qacw_xml.get_files_with_severity_levels(self.severity_files, [3])[0]
        new_finding = qacw_xml.SeverityFinding(level=3, total=1, active=1, qac_rule='qac-42',
                                               text='violation 42 is the most evil of the evil')
        self.assertEqual(4, len(severity_3_file.get_all_findings()))
        severity_3_file.add_finding(new_finding)
        self.assertEqual(5, len(severity_3_file.get_all_findings()))


if __name__ == "__main__":
    unittest.main()
