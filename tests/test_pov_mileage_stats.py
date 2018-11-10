#!/usr/bin/env python3
"""
Unit and regression test for the pov_mileage_stats package.
"""

# Import package, test suite, and other packages as needed
import os
import sys
import unittest
from contextlib import contextmanager
from io import StringIO

from pov_mileage_stats import main
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
