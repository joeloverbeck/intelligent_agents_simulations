"""This module contains exceptions as well as ways to log errors.
"""


import json
import os


class InvalidParameterError(Exception):
    """Exception to use when a parameter sent to a function is invalid.

    Args:
        Exception (Exception): the wrapped exception
    """


class MissingAgentAttributeError(Exception):
    pass


class MissingCharacterSummaryError(Exception):
    pass


class DisparityBetweenDatabasesError(Exception):
    pass


class DatabaseDoesntExistError(Exception):
    pass


class UnableToSaveVectorDatabaseError(Exception):
    pass


class UnableToConnectWithAiModelError(Exception):
    pass


class AlgorithmError(Exception):
    pass


class DirectoryDoesntExistError(Exception):
    pass


class FileDoesntExistError(Exception):
    pass


class NodeTypeUnhandledError(Exception):
    pass


def log_error(error_text):
    """Logs the error text into a text file.

    Args:
        error_text (_type_): _description_
    """
    with open("logging/errors.txt", "a", encoding="utf8") as file:
        file.write(json.dumps(error_text, default=str))
        file.write(os.linesep)
