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
from datetime import datetime

from xlrd import open_workbook
import zlib
import webbrowser

import calculate_statistics
import load_data
import make_plots
import html_template_render


# Global return statuses
class RETVAL:
    SUCCESS = 0
    FAILURE = 1


# Global Variables
CURRENT_DIR = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(os.path.join(CURRENT_DIR, 'html_templates'), 'base.htm')
HTML_OUTFILE_NAME = 'Mileage_Report.htm'
HTML_OUT_PATH = os.path.join(os.getcwd(), HTML_OUTFILE_NAME)
PROJ_DIR = os.path.join(CURRENT_DIR, '..')
TEST_DIR = os.path.join(PROJ_DIR, 'tests')
SAMPLE_DATA_PATH = os.path.join(TEST_DIR, 'test_data.xlsx')


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

    parser.add_argument("-v", "--pivot-tables", action="store_const", const=True, required=False,
                        help="Print pivot table reports of the mileage to STDOUT.", default=False)

    parser.add_argument("-P", "--no-plots", action="store_const", const=True, required=False, default=False,
                        help="Do not generate any plots. Plots are placed into {}. Because plot images are required "
                             "for HTML output, this option implies -H".format(
                            make_plots.IMG_DIR))

    parser.add_argument("-H", "--no-html", action="store_const", const=True, required=False, default=False,
                        help="Do not generate any HTML output file.")

    args = None

    # If user doesn't specify any arguments, print the help.
    if not len(argv) > 1:
        parser.print_help()
        warning("You did not specify an Excel input file. Please specify one using the -i option.")
        return args, RETVAL.FAILURE

    args = parser.parse_args(argv)

    return args, RETVAL.SUCCESS


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != RETVAL.SUCCESS:
        return ret

    # If the user specified -P, but not -H, fail and warn that they must allow plots to get HTML
    if args.no_plots and not args.no_html:
        warning("You must allow plots in order to generate HTML content. Please run the program without the -P switch.")
        return args, RETVAL.FAILURE

    # Load data
    try:
        # First try to locate the file. If this fails, quit the program.
        if not os.path.isfile(args.input_file):
            warning("Cannot find the input file. Please check the path you specified.")
            return args, RETVAL.FAILURE

        # Manually check for broken Excel file (because apparently pd.read_excel won't raise an Exception for it)
        # Thanks to https://stackoverflow.com/a/28645601
        workbook = open_workbook(args.input_file)
        workbook.release_resources()

        data, ret = load_data.import_excel_data(
            args.input_file,
            skiprows=args.skiprows,
            usecols=args.usecols,
            sheets=1,
        )

    except AttributeError as e:
        warning("You did not specify an Excel input file. Please specify one.")
        return args, RETVAL.FAILURE
    except zlib.error as e:
        warning("Excel file appears to be corrupt. Please try using a different file.", e)
        return RETVAL.FAILURE

    # Perform calculations
    try:
        data = load_data.establish_relevant_columns(data)
        basic_stats = calculate_statistics.calculate_basic_stats(data)
    except AttributeError as e:
        warning(
            "Workbook contains invalid data. Please check your column formatting and data range and try again.", e)
        return RETVAL.FAILURE

    if args.basic_statistics:
        calculate_statistics.print_basic_stats(basic_stats)

    if args.pivot_tables:
        # Print text representation of pivot tables to screen.
        calculate_statistics.gen_pvt_table_stdout_reports(data, calculate_statistics.PVT_TABLES)

    # Make Plots
    if not args.no_plots:
        make_plots.write_all_plots(data, make_plots.plot_info)
        print("Plots saved to {}".format(make_plots.IMG_DIR))

    # Render HTML report:
    # First, compile all the data into a huge dictionary:
    if not args.no_plots and not args.no_html:
        jinja_data = {
            'time_stamp': datetime.now().strftime('%c'),
            'basic_stats': basic_stats,
            'pvt_tables': calculate_statistics.gen_pvt_table_html_reports(data, calculate_statistics.PVT_TABLES),
            'plot_info': make_plots.plot_info,
            'plot_ext': make_plots.OUTPUT_EXT,
            'plot_dir': make_plots.IMG_DIR + os.sep,
        }

        # Then, render this template using Jinja
        html_template_render.render_template(jinja_data, template_path=TEMPLATE_PATH, out_path=HTML_OUT_PATH)

        # Open results in browser
        webbrowser.open(HTML_OUT_PATH)

    return RETVAL.SUCCESS  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
# else:
#     main(["-i",r"..\tests\test_data\test_data.xlsx"])
