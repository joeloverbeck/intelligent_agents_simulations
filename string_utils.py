def end_string_with_period(text):
    text = text.strip()
    if not text.endswith("."):
        text += "."

    return text
