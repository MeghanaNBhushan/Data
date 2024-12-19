""" Create a plot of the time a pr is open """

import os
import sys
import datetime
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.tools.pr_stats.pr_plot import plot
from lucxbox.tools.pr_stats.pr_utils import fill_dates_with_zero, days_list


def get_duration_of_prs(prs, start_date, end_date):
    merges_times = []
    for pull_request in prs:
        if pull_request.state == "MERGED":
            if start_date < pull_request.closed < end_date:
                merges_times.append(pull_request.time_open.total_seconds() / 60 / 60 / 24)

    merges_times.sort()
    return list(range(1, len(merges_times) + 1)), merges_times


def get_pr_duration(spacetime, prs, out):
    # Get Plot Data
    dates_year, n_pr_year = get_duration_of_prs(prs, spacetime.this_year_start_d, spacetime.this_year_end_d)
    dates_this_week, n_pr_this_week = get_duration_of_prs(prs, spacetime.last_monday, spacetime.last_sunday)
    dates_last_week, n_pr_last_week = get_duration_of_prs(prs, spacetime.last_last_monday, spacetime.last_last_sunday)

    plot("PR duration to develop", "duration in days", out, dates_year, n_pr_year, dates_last_week, \
         n_pr_last_week, dates_this_week, n_pr_this_week)


def get_merged_loc_by_duration(prs, start_date, end_date):
    match_prs = []
    days = days_list(start_date, end_date)
    for pull_request in prs:
        for day in days:
            if pull_request.state == "MERGED":
                if day.day == pull_request.closed.day and \
                        day.month == pull_request.closed.month and \
                        day.year == pull_request.closed.year:
                    match_prs.append(pull_request)
    sorted(match_prs, key=lambda pull_request: pull_request.loc)

    duration_prs = []
    loc_prs = []
    for pull_request in match_prs:
        duration_prs.append(pull_request.time_open.total_seconds() / 60 / 60 / 24)
        loc_prs.append(pull_request.loc)

    return loc_prs, duration_prs


def get_loc_by_duration(spacetime, prs, out):
    # Get Plot Data
    dates_year, n_pr_year = get_merged_loc_by_duration(prs, spacetime.this_year_start_d, spacetime.this_year_end_d)
    dates_this_week, n_pr_this_week = get_merged_loc_by_duration(prs, spacetime.last_monday, spacetime.last_sunday)
    dates_last_week, n_pr_last_week = get_merged_loc_by_duration(prs, spacetime.last_last_monday, spacetime.last_last_sunday)

    plot("PR duration by lines of code", "duration in days", out, dates_year, n_pr_year, dates_last_week, n_pr_last_week, dates_this_week,
         n_pr_this_week, True)


def get_merged_prs(prs, start_date, end_date):
    merged_prs = []
    days = days_list(start_date, end_date)
    for pull_request in prs:
        if pull_request.state == "MERGED":
            for day in days:
                if day.day == pull_request.closed.day and \
                        day.month == pull_request.closed.month and \
                        day.year == pull_request.closed.year:
                    merged_prs.append(day)
                    break
    c_merged_prs = Counter(merged_prs)
    return list(c_merged_prs.keys()), list(c_merged_prs.values())


def get_pr_merged(spacetime, prs, out):
    # Get Plot Data
    dates_year, n_pr_year = get_merged_prs(prs, spacetime.this_year_start_d, spacetime.this_year_end_d)
    dates_this_week, n_pr_this_week = get_merged_prs(prs, spacetime.last_monday, spacetime.last_sunday)
    dates_last_week, n_pr_last_week = get_merged_prs(prs, spacetime.last_last_monday, spacetime.last_last_sunday)

    dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week = fill_dates_with_zero(
        spacetime, dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week)

    plot("PR merges to develop", "# of merges", out, dates_year, n_pr_year, dates_last_week,
         n_pr_last_week, dates_this_week, n_pr_this_week)


def get_open_prs(prs, start_date, end_date):
    open_prs = []
    days = days_list(start_date, end_date)
    for pull_request in prs:
        for day in days:
            if day > datetime.datetime.today():
                continue
            if pull_request.created <= day <= pull_request.closed:
                open_prs.append(day)
    c_open_prs = Counter(open_prs)
    return list(c_open_prs.keys()), list(c_open_prs.values())


def get_pr_open(spacetime, prs, out):
    # Get Plot Data
    dates_year, n_pr_year = get_open_prs(prs, spacetime.this_year_start_d, spacetime.this_year_end_d)
    dates_this_week, n_pr_this_week = get_open_prs(prs, spacetime.last_monday, spacetime.last_sunday)
    dates_last_week, n_pr_last_week = get_open_prs(prs, spacetime.last_last_monday, spacetime.last_last_sunday)

    dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week = \
        fill_dates_with_zero(spacetime, dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week)

    plot("PR open to develop", "# of open prs", out, dates_year, n_pr_year, dates_last_week, \
         n_pr_last_week, dates_this_week, n_pr_this_week)


def get_opened_prs(prs, start_date, end_date):
    opened_prs = []
    days = days_list(start_date, end_date)
    for pull_request in prs:
        for day in days:
            if day > datetime.datetime.today():
                continue
            if pull_request.created.date() == day.date():
                opened_prs.append(day)
    c_open_prs = Counter(opened_prs)
    return list(c_open_prs.keys()), list(c_open_prs.values())


def get_pr_opened(spacetime, prs, out):
    # Get Plot Data
    dates_year, n_pr_year = get_opened_prs(prs, spacetime.this_year_start_d, spacetime.this_year_end_d)
    dates_this_week, n_pr_this_week = get_opened_prs(prs, spacetime.last_monday, spacetime.last_sunday)
    dates_last_week, n_pr_last_week = get_opened_prs(prs, spacetime.last_last_monday, spacetime.last_last_sunday)

    dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week = \
        fill_dates_with_zero(spacetime, dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week)

    plot("PR opened to develop", "# of opened prs", out, dates_year, n_pr_year, dates_last_week, \
         n_pr_last_week, dates_this_week, n_pr_this_week)


def get_diff_prs(prs, start_date, end_date):
    closed_prs = []
    days = days_list(start_date, end_date)
    for pull_request in prs:
        for day in days:
            if day.day == pull_request.closed.day and \
                    day.month == pull_request.closed.month and \
                    day.year == pull_request.closed.year:
                closed_prs.append(day)
    c_closed_prs = Counter(closed_prs)

    open_prs = []
    days = days_list(start_date, end_date)
    for pull_request in prs:
        for day in days:
            if day > datetime.datetime.today():
                continue
            if pull_request.created.date() == day.date():
                open_prs.append(day)
    c_open_prs = Counter(open_prs)

    c_open_prs.subtract(c_closed_prs)
    return list(c_open_prs.keys()), list(c_open_prs.values())


def get_pr_diff(spacetime, prs, out):
    # Get Plot Data
    dates_year, n_pr_year = get_diff_prs(prs, spacetime.this_year_start_d, spacetime.this_year_end_d)
    dates_this_week, n_pr_this_week = get_diff_prs(prs, spacetime.last_monday, spacetime.last_sunday)
    dates_last_week, n_pr_last_week = get_diff_prs(prs, spacetime.last_last_monday, spacetime.last_last_sunday)

    dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week = \
        fill_dates_with_zero(spacetime, dates_year, n_pr_year, dates_this_week, n_pr_this_week, dates_last_week, n_pr_last_week)

    plot("PR diff to develop", "# of prs", out, dates_year, n_pr_year, dates_last_week, n_pr_last_week, dates_this_week, n_pr_this_week)
