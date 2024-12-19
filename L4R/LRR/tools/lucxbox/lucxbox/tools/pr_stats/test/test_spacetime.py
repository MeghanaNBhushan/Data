""" Test for a pr_stats """

import datetime
import unittest
import lucxbox.tools.pr_stats.spacetime as spacetime


class TestSpaceTime(unittest.TestCase):

    def test_constructor(self):
        defined_today = datetime.date(year=2019, month=1, day=1)
        expected_last_monday = datetime.date(year=2018, month=12, day=31)

        space = spacetime.Spacetime(date=defined_today)
        self.assertTrue(space.today == defined_today)
        self.assertTrue(space.last_monday == expected_last_monday)

    def test_get_last_mondays_week_0(self):
        last_monday = spacetime.get_last_mondays(week=0, date=datetime.date(year=2019, month=1, day=1))
        expected_last_monday = datetime.date(year=2018, month=12, day=31)
        self.assertTrue(last_monday == expected_last_monday)

    def test_get_last_mondays_week_1(self):
        last_monday = spacetime.get_last_mondays(week=1, date=datetime.date(year=2019, month=1, day=1))
        expected_last_monday = datetime.date(year=2018, month=12, day=24)
        self.assertTrue(last_monday == expected_last_monday)


if __name__ == "__main__":
    unittest.main()
