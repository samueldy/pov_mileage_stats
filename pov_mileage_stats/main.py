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

import load_data
import calculate_statistics
import make_plots
import results_export
import html_template_render

# Global return statuses
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
    # parser.add_argument("-i", "--input_rates", help="The location of the input rates file",
    #                     default=DEF_IRATE_FILE, type=read_input_rates)
    parser.add_argument("-n", "--no_attribution", help="Whether to include attribution",
                        action='store_false')
    parser.add_argument("-i", "--input-file", required=True, help="Path to the Excel workbook containing mileage data.", type=str)
    parser.add_argument("-s", "--skiprows", help="Number of header rows to skip before reading your table.", required=False, default=0)
    parser.add_argument("-c", "--usecols", help="A:B-style range of columns to include.", default="A:B",required=False)
    
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

    # Perform calculations

    # Make Plots

    # Export results to Python objects and SVG images

    # Render Jinja templates

    # Open results in browser

    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
