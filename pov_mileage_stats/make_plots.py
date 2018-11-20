# -*- coding: utf-8 -*-
"""
makePlots.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles data plotting.
"""

import matplotlib.pyplot as plt
import os
import numpy as np

# Going to make relevant for the mileage charts:
# (1) Daily mileage usage for the last 30 days.
# (2) Barchart showing pivot report of median miles by day of week and year
# (3) Barchart showing pivot report of median miles by month and year

# Global Options
CURR_DIR = os.getcwd()
IMG_DIR = os.path.join(CURR_DIR, 'img')
OUTPUT_DPI = 150
OUTPUT_EXT = '.png'
plt.style.use('seaborn')
plt.tight_layout()


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
    plt.savefig(outpath, dpi=OUTPUT_DPI, bbox_inches='tight')


def save_median_day_year(df, outpath):
    """
    Save a bar chart showing representing a pivot table report of median mileage usage by day of week and year
    :type df: pd.DataFrame
    :param df: the mileage data frame containing Month and Day columns (with each entry prepended with the appropriate month or day number) and "Miles" column.
    :param outpath: path (including file extension) where plot should be saved
    :return:
    """
    pvt_median_month_day = df.pivot_table(values='Miles', index='DayOfWeek', columns='Year', aggfunc=np.median
                                          )
    plot1 = pvt_median_month_day.plot(kind='bar', title='Median Mileage by Month and Day of Week', grid=True)
    plot1.set(xlabel='Day of Week', ylabel='Median Miles Driven')
    plt.savefig(outpath, dpi=OUTPUT_DPI, bbox_inches='tight')


def save_median_month_year(df, outpath):
    """
    Save a bar chart showing representing a pivot table report of median mileage usage by month and year
    :type df: pd.DataFrame
    :param df: the mileage data frame containing Month and Day columns (with each entry prepended with the appropriate month or day number) and "Miles" column.
    :param outpath: path (including file extension) where plot should be saved
    :return:
    """
    pvt_median_month_year = df.pivot_table(values='Miles', index='Month', columns='Year', aggfunc=np.median
                                           )
    plot1 = pvt_median_month_year.plot(kind='bar', title='Median Mileage by Month and Year', grid=True)
    plot1.set(xlabel='Day of Week', ylabel='Median Miles Driven')
    plt.savefig(outpath, dpi=OUTPUT_DPI, bbox_inches='tight')


plot_info = {
    'dailyUsage': {
        'Name': 'Daily Mileage Usage',
        'Desc': 'Daily mileage usage for the last 30 days',
        'filename': 'daily_mileage_totals',
        'func': save_daily_usage_plot,
    },
    'median_day_year': {
        'Name': 'Median Mileage By Day of Week and Year',
        'Desc': 'Median mileage driven by day of week and year',
        'filename': 'median_day_year',
        'func': save_median_day_year,
    },
    'median_month_year': {
        'Name': 'Median Mileage By Month and Year',
        'Desc': 'Median mileage driven by month and year',
        'filename': 'median_month_year',
        'func': save_median_month_year,
    },
}


def write_all_plots(df, plot_config):
    """
    Write out all configured plots to the appropriate place on disk
    :param df: the mileage dataframe containing at least Miles, Month, and Day columns (with each Month and Day value prepended with the appropriate month or day number).
    :return:
    """
    results = dict()

    # Make output directory if it doesn't already exist
    if not os.path.isdir(IMG_DIR):
        os.mkdir(IMG_DIR)

    for plotID, singleplot_info in plot_config.items():
        # Write out the plot to the correct location
        out_path = r"".join([os.path.join(IMG_DIR, singleplot_info['filename']), OUTPUT_EXT])
        singleplot_info['func'](df, out_path)  # Call plotter

        print("""Exported plot "{}" at {}""".format(singleplot_info['Name'], out_path))
