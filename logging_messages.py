import json
import os

from defines import DEBUGGING


def log_debug_message(debug_message):
    """Logs the debug message into a text file.

    Args:
        debug_message (str): the message that may be written to file
    """
    if DEBUGGING:
        with open("logging/debug_messages.txt", "a", encoding="utf8") as file:
            file.write(json.dumps(debug_message, default=str))
            file.write(os.linesep)
