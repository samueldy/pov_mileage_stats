#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pov_mileage_stats.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles the primary functions
"""

import os
import sys
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import xlrd

import load_data
import calculate_statistics
import make_plots
import results_export
import html_template_render


# Global return statuses
class RETVAL():
    SUCCESS = 0
    FAILURE = 1


# Other global variables
SAMPLE_DATA_PATH = "data/test_data.xlsx"


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input-file", required=True, help="Path to the Excel workbook containing mileage data.",
                        type=str)
    parser.add_argument("-s", "--skiprows", help="Number of header rows to skip before reading your table.",
                        required=False, default=0)
    parser.add_argument("-c", "--usecols", help="A:B-style range of columns to include.", default="A:B", required=False)

    args = None
    try:
        args = parser.parse_args(argv)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 2

    return args, 0


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret

    # Load data
    # xlrd date conversion trick: https://stackoverflow.com/a/51708561
    data, ret = load_data.import_excel_data(
        args.input_file,
        skiprows=args.skiprows,
        usecols=args.usecols,
        sheets=1,
        converters={
            'Date': lambda x: xlrd.xldate.xldate_as_datetime(x, 0)
        })
    print(data)

    # Perform calculations
    data = load_data.establish_relevant_columns(data)
    basic_stats = calculate_statistics.calculate_basic_stats(data)
    calculate_statistics.print_basic_stats(basic_stats)

    # Make Plots

    # Export results to Python objects and SVG images

    # Render Jinja templates

    # Open results in browser

    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)

# main(["-i",r"..\tests\test_data\test_data.xlsx"])