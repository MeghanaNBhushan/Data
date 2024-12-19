""" Test for a pr_stats """

import unittest
from datetime import date, timedelta
import lucxbox.tools.pr_stats.spacetime as spacetime
import lucxbox.tools.pr_stats.pr_utils as pr_utils


def get_date_range(date1, date2):
    date_range = []
    for count in range(int((date2 - date1).days) + 1):
        date_range.append(date1 + timedelta(count))
    return date_range


class TestPrUtils(unittest.TestCase):

    def test_days_list(self):
        start_date = date(year=2019, month=1, day=1)
        end_date = date(year=2019, month=1, day=31)

        span = pr_utils.days_list(start_date=start_date, end_date=end_date)
        self.assertTrue(len(span) == 31)
        self.assertTrue(span[0] == start_date)
        self.assertTrue(span[len(span) - 1] == end_date)

    def test_fill_dates_wo_dates(self):
        defined_today = date(year=2019, month=1, day=31)
        space = spacetime.Spacetime(date=defined_today)

        d_y, pr_y, d_tw, pr_tw, d_lw, pr_lw = pr_utils.fill_dates_with_zero(
            spacetime=space,
            dates_year=[], n_pr_year=[],
            dates_this_week=[], n_pr_this_week=[],
            dates_last_week=[], n_pr_last_week=[])

        self.assertTrue(len(d_y) == 2)
        self.assertTrue(d_y[0] is space.this_year_start_d)
        self.assertTrue(d_y[1] is space.this_year_end_d)
        self.assertTrue(len(pr_y) == 2)
        self.assertTrue(len(d_tw) == 2)
        self.assertTrue(d_tw[0] is space.last_monday)
        self.assertTrue(d_tw[1] is space.last_sunday)
        self.assertTrue(len(pr_tw) == 2)
        self.assertTrue(len(d_lw) == 2)
        self.assertTrue(d_lw[0] is space.last_last_monday)
        self.assertTrue(d_lw[1] is space.last_last_sunday)
        self.assertTrue(len(pr_lw) == 2)

    def test_fill_dates_w_dates(self):
        defined_today = date(year=2019, month=1, day=25)
        space = spacetime.Spacetime(date=defined_today)

        d_y = get_date_range(date(2019, 1, 1), defined_today)
        d_tw = get_date_range(date(2019, 1, 21), defined_today)
        d_lw = get_date_range(date(2019, 1, 14), date(2019, 1, 20))

        d_y, pr_y, d_tw, pr_tw, d_lw, pr_lw = pr_utils.fill_dates_with_zero(
            spacetime=space,
            dates_year=d_y, n_pr_year=list(range(25)),
            dates_this_week=d_tw, n_pr_this_week=list(range(5)),
            dates_last_week=d_lw, n_pr_last_week=list(range(7)))

        self.assertTrue(len(d_y) == 25)
        self.assertTrue(d_y[0] == date(2019, 1, 1))
        self.assertTrue(d_y[24] == defined_today)
        self.assertTrue(len(pr_y) == 25)
        self.assertTrue(len(d_tw) == 7)
        self.assertTrue(d_tw[0] == space.last_monday)
        self.assertTrue(d_tw[len(d_tw) - 1] == date(2019, 1, 27))
        self.assertTrue(len(pr_tw) == 7)
        self.assertTrue(len(d_tw) == 7)
        self.assertTrue(d_lw[0] == space.last_last_monday)
        self.assertTrue(d_lw[len(d_lw) - 1] == space.last_last_sunday)
        self.assertTrue(len(pr_lw) == 7)


if __name__ == "__main__":
    unittest.main()
