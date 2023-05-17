import re

from errors import log_error


def extract_rating_from_text(text, prompt_that_originated_text, silent=False):
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
    error_message = f"ERROR: Function {extract_rating_from_text.__name__}, the text should have contained a number, but it was: {text} "
    error_message += (
        f"The prompt that generated this error: {prompt_that_originated_text}"
    )

    if not silent:
        log_error(error_message)

    return 5


def remove_end_tag_from_ai_response(text):
    pattern = "</s>$"
    return re.sub(pattern, "", text)
