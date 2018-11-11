# --- coding: utf-8 ---
"""
calculateStatistics.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles statistics calculation.
"""

import pandas as pd

def calculate_basic_stats(data):
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
    # First, convert all NAs to zeros.
    