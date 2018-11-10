# -*- coding: utf-8 -*-
"""
validateInputFile.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles input file validation.
"""
INPUT_FILE_EXT = ".xlsx"

import os
from pov_mileage_stats import main

def validate_input_file(path):
    """
    Validate the input file located at path.

    Parameters
    ----------
    path : The path to the file to be loaded.

    Returns
    -------
    RETURN_VAL : A return value, as specified in the main module.
    """

    print(path)
    return

def check_file_extension(path):
    """
    Checks to see if the file extension of the path represented by path is ".xlsx"
    
    Thanks to https://stackoverflow.com/a/541394.

    Parameters
    ----------
    path    The path to the file to be loaded.

    Returns
    -------
    RETURN_VAL  A return value, as specified in the main module.
    """
    try:
        _, ext = os.path.splitext(path)
        return ext == INPUT_FILE_EXT
    except IOError as e:
        main.warning("The path to the input file is invalid. Please try a different path.", e)
