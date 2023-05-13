"""This module contains exceptions as well as ways to log errors.
"""


import json
import os


class InvalidParameterError(Exception):
    """Exception to use when a parameter sent to a function is invalid.

    Args:
        Exception (Exception): the wrapped exception
    """

class MissingCharacterSummaryError(Exception):
    pass

class FailedToDeleteFileError(Exception):
    pass


class DisparityBetweenDatabasesError(Exception):
    pass


class DatabaseDoesntExistError(Exception):
    pass


def log_error(error_text):
    """Logs the error text into a text file.

    Args:
        error_text (_type_): _description_
    """
    with open("log.txt", "a", encoding="utf8") as file:
        file.write(json.dumps(error_text, default=str))
        file.write(os.linesep)