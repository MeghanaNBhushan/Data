""" Utils for pull request statistics """

from datetime import timedelta


def days_list(start_date, end_date, delta=timedelta(days=1)):
    current_date = start_date
    time_span = []
    while current_date <= end_date:
        time_span.append(current_date)
        current_date += delta
    return time_span


def fill_dates_with_zero(spacetime, dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week):
    """ Fill dates with zeros if no dates exist """
    if not dates_year:
        dates_year = [spacetime.this_year_start_d, spacetime.this_year_end_d]
        n_pr_year = [0, 0]

    if not dates_this_week:
        dates_this_week = [spacetime.last_monday, spacetime.last_sunday]  # this mondays
        n_pr_this_week = [0, 0]
    else:
        # Fill up
        weekdays = [dates.weekday() for dates in dates_this_week]
        for i in range(7):
            if i not in weekdays:
                dates_this_week.append(spacetime.last_monday + timedelta(days=i))
                n_pr_this_week.append(0)

    if not dates_last_week:
        dates_last_week = [spacetime.last_last_monday, spacetime.last_last_sunday]  # this mondays
        n_pr_last_week = [0, 0]
    else:
        # Fill up
        weekdays = [dates.weekday() for dates in dates_last_week]
        for i in range(7):
            if i not in weekdays:
                dates_last_week.append(spacetime.last_last_monday + timedelta(days=i))
                n_pr_last_week.append(0)
    return dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week
