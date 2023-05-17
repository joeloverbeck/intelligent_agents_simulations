def end_string_with_period(text):
    text = text.rstrip()  # removes trailing whitespaces
    special_chars = ["\n", "\t", "\r"]  # list of special characters to check

    for char in special_chars:
        if text.endswith(char):
            text = (
                text[: -len(char)] + "." + char
            )  # inserts period before special character
            break
    else:
        if not text.endswith("."):
            text += "."  # if no special character at the end, add period

    return text


def replace_spaces_with_underscores(text):
    lower_text = text.lower()
    result = lower_text.replace(" ", "_")

    return result
