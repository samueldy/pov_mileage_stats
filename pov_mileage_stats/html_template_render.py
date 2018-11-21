# -*- coding: utf-8 -*-
"""
htmlTemplateRender.py
A small command-line tool to calculate mileage statistics for a personally-owned vehicle.

Handles rendering of results data into Jinja2 templates to create a nice web report.

Essential to this task is the construction of a dictionary containing all of the necessary data. It should be outline as follows:



"""

import jinja2 as jinja


def render_template(data, template_path, out_path):
    """
    Render the HTML template using items in the data dict and write the result to disk
    :param template_path:
    :param template_path:
    :param data: a dictionary containing all of the pertinent information needed for the full HTML report.
    :param out_path: the fully-qualified pathname of the HTML file that will contain the rendered, static report.
    :return:
    """
    # Read template file into string
    with open(template_path, 'r') as template_file:
        template_string = template_file.read()

    template = jinja.Template(template_string)

    with open(out_path, 'w') as out_file:
        out_file.write(template.render(data))

    print("HTML report rendered to {}".format(out_path))