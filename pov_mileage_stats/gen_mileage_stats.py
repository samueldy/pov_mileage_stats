#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pov_mileage_stats.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles the primary functions
"""

import argparse
import sys

import xlrd

import calculate_statistics
import load_data
import make_plots


# Global return statuses
class RETVAL():
    SUCCESS = 0
    FAILURE = 1


# Other global variables
SAMPLE_DATA_PATH = "data\\test_data.xlsx"


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

    parser.add_argument("-b", "--basic-statistics", action="store_const", const=True, required=False,
                        help="Print some basic statistics about the mileage log.")

    parser.add_argument("-p", "--pivot-tables", action="store_const", const=True, required=False,
                        help="Print pivot table reports of the mileage.")

    args = None

    # If user doesn't specify any arguments, print the help.
    if not len(sys.argv) > 1:
        parser.print_help()
        return args, RETVAL.SUCCESS

    try:
        args = parser.parse_args(argv)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 2

    return args, RETVAL.SUCCESS


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != RETVAL.SUCCESS:
        return ret

    # Load data
    # xlrd date conversion trick: https://stackoverflow.com/a/51708561
    data, ret = load_data.import_excel_data(
        args.input_file,
        skiprows=args.skiprows,
        usecols=args.usecols,
        sheets=1,
    )

    # Perform calculations
    data = load_data.establish_relevant_columns(data)
    basic_stats = calculate_statistics.calculate_basic_stats(data)

    if args.basic_statistics:
        calculate_statistics.print_basic_stats(basic_stats)

    if args.pivot_tables:
        print(calculate_statistics.fetch_pvttable_reports(data))

    # Make Plots

    # Export results to Python objects and SVG images

    # Render Jinja templates

    # Open results in browser

    return RETVAL.SUCCESS  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
# else:
#     main(["-i",r"..\tests\test_data\test_data.xlsx"])
