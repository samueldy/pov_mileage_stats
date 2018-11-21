pov_mileage_stats
==============================
[//]: # (Badges)
[![Travis Build Status](https://travis-ci.org/samueldy/pov_mileage_stats.png)](https://travis-ci.org/samueldy/pov_mileage_stats)
[![codecov](https://codecov.io/gh/samueldy/pov_mileage_stats/branch/master/graph/badge.svg)](https://codecov.io/gh/samueldy/pov_mileage_stats/branch/master)

`gen_mileage_stats` (formerly `pov_mileage_stats`) is a small command-line tool to calculate mileage statistics for a personally-owned vehicle. It operates on a single Microsoft Excel workbook containing two columns: `Date` and `Miles`, where `Date` is formatted as a date in Excel, and `Miles` shows that day's mileage.

The program optionally produces a set of basic statistics, pivot table reports, plots, and HTML output of all of the above.

    usage: gen_mileage_stats.py [-h] -i INPUT_FILE [-s SKIPROWS] [-c USECOLS] [-b]
                                [-v] [-P] [-H]

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT_FILE, --input-file INPUT_FILE
                            Path to the Excel workbook containing mileage data.
    -s SKIPROWS, --skiprows SKIPROWS
                            Number of header rows to skip before reading your
                            table.
    -c USECOLS, --usecols USECOLS
                            A:B-style range of columns to include.
    -b, --basic-statistics
                            Print some basic statistics about the mileage log.
    -v, --pivot-tables    Print pivot table reports of the mileage to STDOUT.
    -P, --no-plots        Do not generate any plots. Plots are placed 
                            into .\img.
                            Because plot images are required for HTML output, this
                            option implies -H
    -H, --no-html         Do not generate any HTML output file.



### Copyright

Copyright (c) 2018, Samuel D. Young


#### Acknowledgements
 
Project based on the 
[Computational Chemistry Python Cookiecutter](https://github.com/choderalab/cookiecutter-python-comp-chem)
