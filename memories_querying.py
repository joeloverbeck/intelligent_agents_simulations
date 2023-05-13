

from math_utils import custom_score


def retrieve_description_from_scored_results_entry(vector_id, memories_raw_data):
    return f"{memories_raw_data[str(vector_id[0])]['description']}\n"


def search_memories(query_vector, index, number_of_results, memories_raw_data):
    # Get nearest neighbors from the Annoy index
    nearest_neighbors = index.get_nns_by_vector(
        query_vector, number_of_results, include_distances=True
    )

    # Calculate the custom scores
    scores = []
    for idx, distance in zip(nearest_neighbors[0], nearest_neighbors[1]):
        relevance = 1 - distance
        recency = memories_raw_data[str(idx)]["recency"]
        importance = memories_raw_data[str(idx)]["importance"]
        score = custom_score(relevance, recency, importance)
        scores.append((idx, score))

    # Sort the results by the custom scores in descending order
    sorted_results = sorted(scores, key=lambda x: x[1], reverse=True)

    return sorted_results
