# -*- coding: utf-8 -*-
"""
loadData.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles data conversion into a pandas DataFrame.
"""

import os
import pathlib2 as pathlib
import pandas as pd
import main
import urllib
import zlib


def import_excel_data(path, **kwargs):
    """
    Imports a Microsoft Excel file into a pd.DataFrame object.
    :param
    path: The (relative) path to a Microsoft Excel workbook.

    :return
    df: A pd.DataFrame instance containing the pertinent data in the Excel Workbook.
    ret: A RETVAL status corresponding to the outcome of the function
    """

    # First, form the file's URI, which pandas needs in order to read the file.
    try:
        path = os.path.abspath(path)
        fname = pathlib.Path(path).as_uri()
    except IOError as e:
        main.warning("Cannot locate file. Please ensure you have specified the correct path.", e)
        return main.RETVAL.FAILURE

    # Now, pass along the file name to pandas, along with any options the user specified:
    try:
        df = pd.read_excel(fname, **kwargs)
    except ValueError as e:
        main.warning(
            "Workbook contains invalid data. Please check your column formatting and data range and try again.", e)
        return main.RETVAL.FAILURE
    except (FileNotFoundError, urllib.error.URLError) as e:
        main.warning("Cannot locate file. Please ensure that you have specified the correct path.", e)
        return main.RETVAL.FAILURE
    except zlib.error as e:
        main.warning("Excel file appears to be corrupt. Please try using a different file.", e)
        return main.RETVAL.FAILURE

    # If the above passes, then we have a valid DataFrame and can return it to the user.
    return df, main.RETVAL.SUCCESS


def establish_relevant_columns(df):
    """
    Creates a dataframe with columns that are useful for month/year pivoting.

    :param
    df: A pd.DataFrame object that has exactly two columns: 'Date' containing DateTime values, and 'Miles' containing floats.

    :return
    A pd.DataFrame instance with 'Date', 'Year', 'Month', 'DayOfWeek', and 'Miles' columns
    """

    # First, establish year, name-of-month, and name-of-day columns in the dataframe.
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year

    return df
