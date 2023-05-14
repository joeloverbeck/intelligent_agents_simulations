from defines import DECAY_RATE, get_json_filename
from math_utils import calculate_recency, calculate_score
from vector_storage import create_json_file, load_contents_of_json_file
from wrappers import validate_agent_type


def retrieve_description_from_scored_results_entry(vector_id, memories_raw_data):
    """Retrieves the description from an entry in scored results

    Args:
        vector_id (dict): entry from scored results
        memories_raw_data (dict): the memories of an agent in raw data format

    Returns:
        str: the description from a scored results entry
    """
    return f"{memories_raw_data[str(vector_id[0])]['description']}\n"


@validate_agent_type
def search_memories(
    agent, current_timestamp, query_vector, index, number_of_results, memories_raw_data
):
    """Searches the memories of an agent for the most relevant entries related to the query vector.

    Args:
        agent (Agent): the agent to whom the memories belong
        current_timestamp (datetime): the current timestamp
        query_vector (List[Tensor] | ndarray | Tensor): the query vector that will be used for the search
        index (AnnoyIndex): the index of the Annoy vector database
        number_of_results (int): how many results must be retrieved from the vector database
        memories_raw_data (dict): the raw data of the agent's memories

    Returns:
        list: the sorted results of the query
    """
    # Get nearest neighbors from the Annoy index
    nearest_neighbors = index.get_nns_by_vector(
        query_vector, number_of_results, include_distances=True
    )

    memories_raw_data = update_most_recent_access_timestamps(
        agent,
        nearest_neighbors,
        current_timestamp,
        load_contents_of_json_file,
        create_json_file,
    )

    # Calculate the custom scores
    scores = []
    for idx, distance in zip(nearest_neighbors[0], nearest_neighbors[1]):
        relevance = 1 - distance
        recency = memories_raw_data[str(idx)]["recency"]
        importance = memories_raw_data[str(idx)]["importance"]
        score = calculate_score(relevance, recency, importance)
        scores.append((idx, score))

    # Sort the results by the custom scores in descending order
    sorted_results = sorted(scores, key=lambda x: x[1], reverse=True)

    return sorted_results


@validate_agent_type
def update_most_recent_access_timestamps(
    agent,
    query_results,
    current_timestamp,
    load_contents_of_json_file_function,
    create_json_file_function,
):
    """Updates the most recent access timestamps of query results.

    Args:
        agent (Agent): the agent to whom the memories belong.
        query_results (list): the query results from the vector database. They come in tuples of (idx, distance)
        current_timestamp (datetime): the current date time when the query was made
        load_contents_of_json_file_function (function): the function responsible for loading the contents of a json file
        create_json_file_function (function): the function responsible for saving to a file the memories

    Returns:
        dict: the memories in raw data format, with updated 'most_recent_access_timestamp' and 'recency' values
    """

    json_filename = get_json_filename(agent)

    # should load the contents of the json database.
    memories_raw_data = load_contents_of_json_file_function(json_filename)

    # Update the 'most_recent_access_timestamp' as well as the 'recency' values of each entry
    for idx, _ in zip(query_results[0], query_results[1]):
        # locate in memories_raw_data which are those records

        memories_raw_data[str(idx)]["recency"] = calculate_recency(
            current_timestamp, current_timestamp, DECAY_RATE
        )
        memories_raw_data[str(idx)][
            "most_recent_access_timestamp"
        ] = current_timestamp.isoformat()

    # save the memories into the json database
    create_json_file_function(json_filename, memories_raw_data)

    return memories_raw_data
