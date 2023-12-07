"""
This file will be used to store commonly used operations
"""

import uuid
import datetime
import re


def create_id():
    return str(uuid.uuid4())


def get_datetime():
    datetime.datetime.now()


def cleaned_filename(input_string):
    """
    Return the input_string as Superset would name it

    @param input_string: the string to filter
    @return: the input string, without non-filename characters, replaced spaces with underscores, and remove leading _
    """
    only_file_char = re.sub(r'[^a-zA-Z0-9\s\-_]', '', input_string)
    no_spaces = only_file_char.replace(" ", "_").lstrip('_')
    return no_spaces
