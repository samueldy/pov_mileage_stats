# --- coding: utf-8 ---
"""
calculateStatistics.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles statistics calculation.
"""
import numpy as np


def calculate_basic_stats(df):
    """
    Performs basic statistics calculations for car data.

    Arguments:
    ----------
    data: a DataFrame containing at least two columns: a 'Date' column and a 'Miles' column.

    Returns:
    -------=
    results: a dict containing some basic statistics:
                mean miles driven
                median miles driven

    """
    # First, drop records with mileage = NA.
    df.dropna(axis=0, how='any', subset=['Miles'])  # Look only in the Miles column for NA values.

    # Now, we can calculate basic statistics
    basic_stats = {
        'mean_mileage': {'Name': 'Mean Mileage', 'units': 'miles', 'data': df['Miles'].mean(axis=0)},
        'med_mileage': {'Name': 'Median Mileage', 'units': 'miles', 'data': df['Miles'].median(axis=0)},
        'first_day': {'Name': 'First Day of Recorded Mileage', 'units': '',
                      'data': df['Date'].min().strftime("%d %b %Y")},
        'last_day': {'Name': 'Last Day of Recorded Mileage', 'units': '',
                     'data': df['Date'].max().strftime("%d %b %Y")},
        'record_low': {'Name': 'Record Low Miles Driven', 'units': 'miles', 'data': df['Miles'].min(axis=0)},
        'record_high': {'Name': 'Record High Miles Driven', 'units': 'miles', 'data': df['Miles'].max(axis=0)},
    }

    return basic_stats


def print_basic_stats(basic_stats):
    """
    Print basic stats to stdout
    :param basic_stats: a dict containing mean mileage, median mileage,
        the first day, the last day, the record low mileage, and the record high mileage.
    :return:
    """
    print("""
    
    Basic Statistics
    ================
    """)
    for _, data in basic_stats.items():
        print("{0:s}: {1:s} {2:s}".format(data['Name'], str(data['data']), data['units']))


# The pivot tables we will retrieve:
PVT_TABLES = {'Mean': np.mean, 'Median': np.median, 'Max': np.max, 'Min': np.min}


# Print string representation of pivot table.
def print_pvt_table(df, aggfunc):
    return print(
        df.pivot_table(values='Miles', index='Month', columns='Year', aggfunc=aggfunc, fill_value=0)
    )


# Produce HTML representation of styled pivot table
def pvt_table_to_html(df, aggfunc):
    return df.pivot_table(values='Miles', index='Month', columns='Year', aggfunc=aggfunc, fill_value=0).style.format(
        "{:.1f}").background_gradient(cmap='RdBu_r', low=1, high=1).render()


# Produce dictionary of pivot table HTML code for template rendering:
def gen_pvt_table_reports(df, aggfuncdict):
    return {key: pvt_table_to_html(df, val) for key, val in aggfuncdict.items()}
