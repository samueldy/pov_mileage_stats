# -*- coding: utf-8 -*-
"""
validateInputFile.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles input file validation.
"""
INPUT_FILE_EXT = ".xlsx"

def validate_input_file(path):
    """
    Validate the input file located at path.

    Inputs
    ------
    path    The path to the file to be loaded.

    """
    print(path)
    return

def check_file_extension(path):
    """
    Checks to see if the file extension of the path represented by path is ".xlsx"
    
    Thanks to https://stackoverflow.com/a/541394.
    """
    try:
        _, ext = os.path.splitext(path)
        return ext == INPUT_FILE_EXT
    except IOError as e:
        warning("The path to the input file is invalid. Please try a different path.", e)