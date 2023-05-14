import datetime


def substract_one_day_from_date(timestamp):
    return timestamp - datetime.timedelta(days=1)


def format_date(timestamp):
    # Get the different parts of the date
    weekday = timestamp.strftime("%A")
    month = timestamp.strftime("%B")
    day = timestamp.strftime("%d")
    year = timestamp.strftime("%Y")
    hour = timestamp.strftime("%I").lstrip("0")  # remove leading zero
    period = timestamp.strftime("%p")

    # Combine them into the desired format
    return f"{weekday} {month} {day} of {year}, {hour} {period}"
