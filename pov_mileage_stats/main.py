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

import validate_input_file
import load_data
import calculate_statistics
import make_plots
import results_export
import html_template_render


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
    parser.add_argument("-r", "--data-range", help="R1C1-style range containing the data")
    
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
    
    # Validate the file
    validateInputfile.validateInputFile(args.input_file)

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
