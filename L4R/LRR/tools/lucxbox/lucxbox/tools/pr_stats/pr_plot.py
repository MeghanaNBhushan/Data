""" Helper module to plot pr stats """

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1)


def plot(title, legend, out, dates_year, n_pr_year, dates_last_week, n_pr_last_week, dates_this_week, n_pr_this_week, log=False):
    fig = plt.figure()
    subplot_pr(211, dates_year, n_pr_year, title, legend, log)
    subplot_pr(223, dates_last_week, n_pr_last_week, "Last week", legend, log)
    subplot_pr(224, dates_this_week, n_pr_this_week, "This week", legend, log)

    # Format subplots
    plt.subplots_adjust(hspace=0.8, wspace=0.4, bottom=0.2)  # format subplots

    fig.savefig(out)


def subplot_pr(pos, plot_dates, y_values, title, label, log):
    axis = plt.subplot(pos)
    axis.set_axisbelow(True)
    if log:
        axis.set_xscale('log')
        axis.scatter(plot_dates, y_values)
        plt.xlim(1, 10000)
    else:
        axis.bar(plot_dates, y_values, label=None)
    axis.yaxis.grid(True, linestyle='--')
    plt.setp(plt.xticks()[1], rotation=30, ha='right')
    plt.ylabel(label)
    plt.title(title)
    plt.figtext(.45, .02, "LUCxMon 1.0", fontsize=7)

    return axis
