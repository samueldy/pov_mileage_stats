# --- coding: utf-8 ---
"""
calculateStatistics.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles statistics calculation.
"""


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
        'mean_mileage': {'Name': 'Mean Mileage', 'units': 'miles', 'data': df['Trip A'].mean(axis=0)},
        'med_mileage': {'Name': 'Median Mileage', 'units': 'miles', 'data': df['Trip A'].median(axis=0)},
        'first_day': {'Name': 'First Day of Recorded Mileage', 'units': '',
                      'data': df['Date'].min().strftime("%d %b %Y")},
        'last_day': {'Name': 'Last Day of Recorded Mileage', 'units': '',
                     'data': df['Date'].max().strftime("%d %b %Y")},
        'record_low': {'Name': 'Record Low Miles Driven', 'units': 'miles', 'data': df['Trip A'].min(axis=0)},
        'record_high': {'Name': 'Record High Miles Driven', 'units': 'miles', 'data': df['Trip A'].max(axis=0)},
    }

    return basic_stats


def print_basic_stats(basic_stats):
    """
    Print basic stats to stdout
    :param basic_stats: a dict containing mean mileage, median mileage,
        the first day, the last day, the record low mileage, and the record high mileage.
    :return:
    """
    for _, data in basic_stats:
        print("{0:s}: {1:.2f} {2:s}".format(data.Name, data.data, data.units))
