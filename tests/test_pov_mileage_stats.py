#!/usr/bin/env python3
"""
Unit and regression test for the pov_mileage_stats package.
"""

# Import package, test suite, and other packages as needed
import os
import sys
import unittest
import logging
from contextlib import contextmanager
from io import StringIO

from gen_mileage_stats import main
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
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)


# Tests for general command-line use
class GeneralCommandLineUse(unittest.TestCase):
    """
    These tests test general command-line operation of the program.
    """

    def test_run_with_no_args(self):
        """
        Trigger an error by attempting to run the program with no arguments.
        :return:
        """
        args = []
        if logger.isEnabledFor(logging.DEBUG):
            main(args)
        with capture_stderr(main, args) as output:
            self.assertTrue("the following arguments are required: -i/--input-file" in output)


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
        args = ["-i", os.path.join(TEST_DATA_DIR, 'non-existent-file.xlsx')]
        if logger.isEnabledFor(logging.DEBUG):
            main(args)
        with capture_stderr(main, args) as output:
            self.assertTrue("Cannot locate file." in output)

    def test_pass_corrupt_file(self):
        """
        Trigger a zlib.error by passing a file that is corrupt (eg., that can't be unzipped).
        :return:
        """
        args = ["-i", os.path.join(TEST_DATA_DIR, 'test_data_corrupted.xlsx')]
        if logger.isEnabledFor(logging.DEBUG):
            main(args)
        with capture_stderr(main, args) as output:
            self.assertTrue("Excel file appears to be corrupt." in output)


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
