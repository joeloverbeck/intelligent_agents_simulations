import math


def calculate_recency(current_timestamp, access_timestamp, decay_rate):
    time_difference = current_timestamp - access_timestamp
    time_difference_in_seconds = time_difference.total_seconds()

    recency = math.exp(-decay_rate * time_difference_in_seconds)

    return recency


def normalize_value(value):
    return (value - 1) / 9


def custom_score(relevance, recency, importance, alpha=0.33, beta=0.33, gamma=0.34):
    return alpha * relevance + beta * recency + gamma * importance
