import re

from errors import log_error


def extract_importance_from_text(text):
    numbers = re.findall(r"\d+", text)
    if numbers:
        num = int(numbers[0])
        if 1 <= num <= 10:
            return num

    # If at this point we haven't found a number, then the AI has responded
    # some nonsense. Log it and return 5.
    log_error(f"ERROR: In the function {extract_importance_from_text.__name__}, the text should have contained a number, but it was: {text}")

    return 5
