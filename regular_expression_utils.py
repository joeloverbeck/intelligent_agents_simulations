import re

from errors import log_error


def extract_rating_from_text(text):
    """Extracts a rating from 1 to 10 from a text.
    Note: if no rating is found in the text, a 5 is returned.

    Args:
        text (str): the text from where a rating should be extracted

    Returns:
        int: the rating
    """
    numbers = re.findall(r"\d+", text)
    if numbers:
        num = int(numbers[0])
        if 1 <= num <= 10:
            return num

    # If at this point we haven't found a number, then the AI has responded
    # some nonsense. Log it and return 5.
    log_error(
        f"ERROR: Function {extract_rating_from_text.__name__}, the text should have contained a number, but it was: {text}"
    )

    return 5
