# -*- coding: utf-8 -*-
"""
makePlots.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles data plotting.
"""

from matplotlib.pyplot import savefig


# Going to make relevant for the mileage charts:
# (1) Daily mileage usage for the last 30 days.
# (2) Barchart showing pivot report of median miles by month and day of week
# (3) Barchart showing pivot report of median miles by month and year

def save_daily_usage_plot(df, outpath):
    """
    Save a line chart showing the last 30 days of mileage usage.
    :param df: the data frame containing a datetime column and "mileage" column.
    :param outpath: path (including file extension) where plot should be saved
    :return:
    """
    plot1 = df.plot(x="Date", y="Miles", title="Daily Mileage Totals", grid=True, xlim=("2018-10", "2018-12"),
                    style="o-k")
    plot1.set(xlabel='Date', ylabel='Miles Driven')
    savefig("DailyMileageTotals.png", dpi=150)