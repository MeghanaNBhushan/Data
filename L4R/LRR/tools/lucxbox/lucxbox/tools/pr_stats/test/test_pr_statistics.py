""" Test for a pr_stats """

from datetime import datetime
import unittest
from lucxbox.lib.bitbucket import PullRequest
import lucxbox.tools.pr_stats.pr_statistics as pr_statistics


class TestPrStatistics(unittest.TestCase):

    def setUp(self):
        pr_open = datetime(2019, 1, 1)
        pr_closed = datetime(2019, 1, 5)
        time_open = pr_closed - pr_open

        self.prs = [
            PullRequest(1, "title1", pr_open, datetime(2019, 1, 4), time_open, "MERGED", 100),
            PullRequest(2, "title2", pr_open, datetime(2019, 1, 5), time_open, "MERGED", 200),
            PullRequest(3, "title3", pr_open, datetime(2050, 1, 1), datetime(2050, 1, 1) - pr_open, "OPEN", 200)
        ]

    def test_pr_duration_in_time(self):
        merged_times = pr_statistics.get_duration_of_prs(
            self.prs, datetime(2019, 1, 1), datetime(2019, 12, 31))

        self.assertEqual(len(merged_times[1]), 2)
        self.assertEqual(merged_times[1][0], 4.0)

    def test_pr_duration_not_in_time(self):
        merged_times = pr_statistics.get_duration_of_prs(
            self.prs, datetime(2018, 1, 1), datetime(2018, 12, 31))

        self.assertEqual(len(merged_times[1]), 0)

    def test_get_merged_loc_by_duration(self):
        loc_prs, duration_prs = pr_statistics.get_merged_loc_by_duration(
            self.prs, datetime(2019, 1, 1), datetime(2019, 12, 31))

        self.assertEqual(loc_prs[0], 100)
        self.assertEqual(duration_prs[0], 4)

    def test_get_merged_prs(self):
        merged_prs = pr_statistics.get_merged_prs(
            self.prs, datetime(2019, 1, 1), datetime(2019, 12, 31))

        self.assertEqual(len(merged_prs[0]), 2)
        self.assertTrue(datetime(2019, 1, 4) in merged_prs[0])
        self.assertTrue(1 in merged_prs[1])

    def test_get_open_prs(self):
        open_prs = pr_statistics.get_open_prs(
            self.prs, datetime(2019, 1, 1), datetime(2019, 12, 31))

        self.assertTrue(datetime(2019, 1, 1) in open_prs[0])
        self.assertTrue(3 in open_prs[1])

    def test_get_opened_prs(self):
        opened_prs = pr_statistics.get_opened_prs(
            self.prs, datetime(2019, 1, 1), datetime(2019, 12, 31))

        self.assertTrue(datetime(2019, 1, 1) in opened_prs[0])
        self.assertTrue(3 in opened_prs[1])
        self.assertEqual(len(opened_prs[0]), 1)

    def test_get_diff_prs(self):
        diff_prs = pr_statistics.get_diff_prs(
            self.prs, datetime(2019, 1, 1), datetime(2019, 12, 31))

        self.assertTrue(datetime(2019, 1, 1) in diff_prs[0])
        self.assertTrue(3 in diff_prs[1])
        self.assertTrue(-1 in diff_prs[1])


if __name__ == "__main__":
    unittest.main()
