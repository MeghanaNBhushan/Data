""" Module to hold all needed date parameters """

from datetime import datetime, timedelta


class Spacetime:
    def __init__(self, date=None):
        # Dates for Plots
        if date is None:
            self.today = datetime.now()
        else:
            self.today = date
        self.last_monday = get_last_mondays(week=0, date=self.today)
        self.last_sunday = self.last_monday + timedelta(days=6)
        self.last_last_monday = get_last_mondays(week=1, date=self.today)
        self.last_last_sunday = self.last_last_monday + timedelta(days=6)
        self.this_year_start_d = datetime.now() - timedelta(days=365)
        self.this_year_end_d = datetime.now()


def get_last_mondays(week=0, date=None):
    """
    Get last mondays from current date.
    :param week: Last n Mondays. 0 last Mondays. 1  Monday before last monday. And so on
    :param date: Date from which to determine last monday(s). This parameter is especially
    used for testing as in the usual use case the current date will be used.
    :return: Date of last monday beginning at 0 OClock
    """
    if date is None:
        today = datetime.now()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        today = date
    last_monday = today - timedelta(days=today.weekday())
    if week:
        for _ in range(week):
            last_monday = last_monday - timedelta(days=7)
    return last_monday
