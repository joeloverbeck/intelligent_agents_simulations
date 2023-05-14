import math

from defines import SCORE_ALPHA, SCORE_BETA, SCORE_GAMMA


def calculate_recency(current_timestamp, access_timestamp, decay_rate):
    time_difference = current_timestamp - access_timestamp
    time_difference_in_seconds = time_difference.total_seconds()

    recency = math.exp(-decay_rate * time_difference_in_seconds)

    return recency


def normalize_value(value):
    return (value - 1) / 9


def calculate_score(
    relevance,
    recency,
    importance,
    alpha=SCORE_ALPHA,
    beta=SCORE_BETA,
    gamma=SCORE_GAMMA,
):
    return alpha * relevance + beta * recency + gamma * importance
