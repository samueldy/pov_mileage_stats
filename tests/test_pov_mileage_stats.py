#!/usr/bin/env python3
"""
Unit and regression test for the pov_mileage_stats package.
"""

# Import package, test suite, and other packages as needed
import os
import sys
import errno
import unittest
import logging
from contextlib import contextmanager
from io import StringIO
import shutil
import time

import gen_mileage_stats
import load_data
import calculate_statistics
import make_plots
import results_export
import html_template_render

# Global test variables
CURRENT_DIR = os.path.dirname(__file__)
MAIN_DIR = os.path.join(CURRENT_DIR, '..')
TEST_DATA_DIR = os.path.join(CURRENT_DIR, 'test_data')
PROJ_DIR = os.path.join(MAIN_DIR, 'arthritis_proj')
DATA_DIR = os.path.join(PROJ_DIR, 'data')
SAMPLE_DATA_FILE = os.path.join(TEST_DATA_DIR, "test_data.xlsx")

# Debug switches
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)


# Tests for general command-line use
class GeneralCommandLineUse(unittest.TestCase):
    """
    These tests test general command-line operation of the program.
    """

    def test_normal_use_case(self):
        """
        Normal use case in which the user provides correct minimal input.
        :return:
        """

        args = ['-i', SAMPLE_DATA_FILE, '-b', '-H']

        if logger.isEnabledFor(logging.DEBUG):
            gen_mileage_stats.main(args)
        with capture_stdout(gen_mileage_stats.main, args) as output:
            self.assertTrue("Mean Mileage" in output)

    def test_run_with_no_args(self):
        """
        Trigger an error by attempting to run the program with no arguments.
        :return:
        """
        args = []
        if logger.isEnabledFor(logging.DEBUG):
            gen_mileage_stats.main(args)
        with capture_stderr(gen_mileage_stats.main, args) as output:
            self.assertTrue("You did not specify an Excel input file." in output)

    def test_run_with_pivot_tables(self):
        """
        See if the program correctly outputs pivot tables to STDOUT
        :return:
        """
        args = ['-i', SAMPLE_DATA_FILE, '-v', '-H']
        if logger.isEnabledFor(logging.DEBUG):
            gen_mileage_stats.main(args)
        with capture_stdout(gen_mileage_stats.main, args) as output:
            self.assertTrue("50.970968" in output)  # Specific value for this test file.
            self.assertTrue("56.922581" in output)
            self.assertTrue("Median Mileage" in output)
            self.assertTrue("Min Mileage" in output)
            self.assertTrue("==============" in output)  # Correct formatting?

    def test_run_html_but_no_plots(self):
        """
        Test by running the -P option only to see if the program warns the user to unsuppress plot generation.
        :return:
        """
        args = ['-i', SAMPLE_DATA_FILE, '-P']
        if logger.isEnabledFor(logging.DEBUG):
            gen_mileage_stats.main(args)

        with capture_stderr(gen_mileage_stats.main, args) as output:
            self.assertTrue("You must allow plots in order to generate HTML content" in output)


# Tests for data loading
class LoadDataTests(unittest.TestCase):
    """
    These tests ensure that the program correct loads data
    """

    def test_pass_wrong_file_name(self):
        """
        Trigger an FileNotFountError by passing an invalid path to the function
        :return:
        """
        args = ["-i", os.path.join(TEST_DATA_DIR, 'non-existent-file.xlsx'), '-H']
        if logger.isEnabledFor(logging.DEBUG):
            gen_mileage_stats.main(args)
        with capture_stderr(gen_mileage_stats.main, args) as output:
            self.assertTrue("Cannot find the input file" in output)

    def test_pass_corrupt_file(self):
        """
        Trigger a zlib.error by passing a file that is corrupt (eg., that can't be unzipped).
        :return:
        """
        args = ["-i", os.path.join(TEST_DATA_DIR, 'test_data_corrupted.xlsx'), '-H']
        if logger.isEnabledFor(logging.DEBUG):
            gen_mileage_stats.main(args)
        with capture_stderr(gen_mileage_stats.main, args) as output:
            self.assertTrue("Excel file appears to be corrupt." in output)

    def test_pass_invalid_data_file(self):
        """
        Trigger a AttributeError by passing a datafile that has text in one of the date cells.
        :return:
        """
        args = ["-i", os.path.join(TEST_DATA_DIR, 'test_data_invaliddata.xlsx'), '-H']
        if logger.isEnabledFor(logging.DEBUG):
            gen_mileage_stats.main(args)
        with capture_stderr(gen_mileage_stats.main, args) as output:
            self.assertTrue("Workbook contains invalid data" in output)


# Tests for plotting
class PlottingTests(unittest.TestCase):
    """
    These tests ensure that the plotting module works correctly.
    """

    def test_normal_plotting_routines(self):
        """Test that output images are correctly placed into the correct output file."""

        # First, silently remove the image output directory to see if the program can produce it.
        silent_remove(make_plots.IMG_DIR, DISABLE_REMOVE)

        args = ['-i', SAMPLE_DATA_FILE, '-H']
        with capture_stdout(gen_mileage_stats.main, args) as output:
            self.assertTrue("Plots saved to" in output)

        # Load plot config from the make_plots module
        plot_config = make_plots.plot_info

        # Check that all output files were successfully generated.
        for plotID, single_plot_info in plot_config.items():
            out_path = r"".join([os.path.join(make_plots.IMG_DIR, single_plot_info['filename']), make_plots.OUTPUT_EXT])
            self.assertTrue(os.path.isfile(out_path))

        # Finally, silently remove the image output directory to see if the program can produce it.
        silent_remove(make_plots.IMG_DIR, DISABLE_REMOVE)

    def test_no_plot_option(self):
        """
        Test that specifying the -P option does not produce any plots
        :return:
        """
        # First, silently remove the image output directory to ensure we're not polluting our test.
        silent_remove(make_plots.IMG_DIR, DISABLE_REMOVE)

        args = ['-i', SAMPLE_DATA_FILE, '-P', '-H']
        with capture_stdout(gen_mileage_stats.main, args) as output:
            self.assertFalse("Plots saved to" in output)

        # Load plot config from the make_plots module
        plot_config = make_plots.plot_info

        # Check that all output files were successfully generated.
        for plotID, single_plot_info in plot_config.items():
            out_path = r"".join([os.path.join(make_plots.IMG_DIR, single_plot_info['filename']), make_plots.OUTPUT_EXT])
            self.assertFalse(os.path.isfile(out_path))

        # Finally, silently remove the image output directory to see if the program can produce it.
        silent_remove(make_plots.IMG_DIR, DISABLE_REMOVE)

class HTMLRenderTests(unittest.TestCase):
    """
    Ensure that the HTML renderer works properly
    """

    def test_jinja_render(self):
        """
        Test the Jinja2 wrapper function
        :return:
        """
        args = ['-i', SAMPLE_DATA_FILE]
        try:
            with capture_stdout(gen_mileage_stats.main, args) as output:
                self.assertTrue("HTML report rendered to" in output)
                self.assertTrue(os.path.isfile(gen_mileage_stats.HTML_OUT_PATH))
                self.assertTrue(os.path.isdir(make_plots.IMG_DIR))
        finally:
            time.sleep(1)  # So that we have time to see the report show up in our browser
            silent_remove(gen_mileage_stats.HTML_OUT_PATH)

    def test_no_html_option(self):
        """
        Test the -H option to ensure that HTML is not rendered, but plots are
        :return:
        """
        # First, silently remove the image output directory and HTML output to ensure we're not polluting our test.
        silent_remove(make_plots.IMG_DIR, DISABLE_REMOVE)
        silent_remove(gen_mileage_stats.HTML_OUT_PATH)

        args = ['-i', SAMPLE_DATA_FILE, '-H']
        with capture_stdout(gen_mileage_stats.main, args) as output:
            self.assertFalse(os.path.isfile(gen_mileage_stats.HTML_OUT_PATH))

        # Load plot config from the make_plots module
        plot_config = make_plots.plot_info

        # Check that all output files were successfully generated.
        for plotID, single_plot_info in plot_config.items():
            out_path = r"".join([os.path.join(make_plots.IMG_DIR, single_plot_info['filename']), make_plots.OUTPUT_EXT])
            self.assertTrue(os.path.isfile(out_path))

        # Finally, silently remove the image output directory and HTML output to clean up.
        silent_remove(gen_mileage_stats.HTML_OUT_PATH)
        silent_remove(make_plots.IMG_DIR, DISABLE_REMOVE)


# Utility functions

# From http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
@contextmanager
def capture_stdout(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out


@contextmanager
def capture_stderr(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    err, sys.stderr = sys.stderr, StringIO()
    command(*args, **kwargs)
    sys.stderr.seek(0)
    yield sys.stderr.read()
    sys.stderr = err


# Silent remove function taken from Lecture 10 notes.
def silent_remove(filename, disable=False):
    """
    Removes the target file name, catching and ignoring errors that indicate that the
    file does not exist.

    @param filename: The file to remove.
    @param disable: boolean to flag if want to disable removal
    """
    if not disable:
        try:
            if os.path.isfile(filename):
                os.remove(filename)
            elif os.path.isdir(filename):
                # Careful!
                shutil.rmtree(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise


if __name__ == '__init__':
    unittest.main()
    sys.exit(0)
