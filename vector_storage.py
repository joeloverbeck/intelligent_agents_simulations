"""This module contains many operations related to storing and retrieving agent memories
"""
import datetime
import json
import os

from annoy import AnnoyIndex
from api_requests import request_response_from_ai_model
from defines import (
    DECAY_RATE,
    MODEL,
    METRIC_ANGULAR,
    NUMBER_OF_TREES,
    VECTOR_DIMENSIONS,
    get_database_filename,
    get_json_filename,
)

from errors import (
    DatabaseDoesntExistError,
    DisparityBetweenDatabasesError,
    FailedToDeleteFileError,
    UnableToSaveVectorDatabaseError,
)
from math_utils import calculate_recency, normalize_value
from regular_expression_utils import extract_rating_from_text
from wrappers import validate_agent_type


def delete_memories_database(agent):
    database_filename = get_database_filename(agent)
    json_filename = get_json_filename(agent)

    if os.path.isfile(json_filename):
        try:
            os.remove(json_filename)
        except Exception as exception:
            raise FailedToDeleteFileError(
                f"Was unable to delete file {json_filename}. Error: {exception}"
            ) from exception

    if os.path.isfile(database_filename):
        try:
            os.remove(database_filename)
        except Exception as exception:
            raise FailedToDeleteFileError(
                f"Was unable to delete file {database_filename}. Error: {exception}"
            ) from exception


def process_raw_data(raw_text):
    vector_representation = MODEL.encode(raw_text)
    return vector_representation


def insert_text_in_vector_index(text, index):
    vector_index = index.get_n_items()

    index.add_item(vector_index, process_raw_data(text))

    return vector_index


def create_memory_dictionary(memory_description, current_timestamp):
    most_recent_access_timestamp = current_timestamp

    recency = calculate_recency(
        current_timestamp, most_recent_access_timestamp, DECAY_RATE
    )

    importance_prompt = "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) "
    importance_prompt += "and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely importance "
    importance_prompt += "of the following piece of memory."
    importance_prompt += f" Memory: {memory_description}"
    importance_prompt += "\nRating: <fill in>."

    importance_response = request_response_from_ai_model(importance_prompt)

    extracted_importance = extract_rating_from_text(
        importance_response, importance_prompt
    )

    normalized_importance = normalize_value(extracted_importance)

    # We must create a whole memory dict.
    return {
        "description": memory_description,
        "creation_timestamp": current_timestamp.isoformat(),
        "most_recent_access_timestamp": most_recent_access_timestamp.isoformat(),
        "recency": recency,
        "importance": normalized_importance,
    }


def create_vectorized_memory(memory_description, current_timestamp, index):
    vector_index = insert_text_in_vector_index(memory_description, index)

    memory = create_memory_dictionary(memory_description, current_timestamp)

    return vector_index, memory


def create_vector_database(database_filename, new_index):
    new_index.build(NUMBER_OF_TREES)

    try:
        new_index.save(database_filename)
    except OSError as exception:
        message_error = f"The function {create_vector_database.__name__} was unable to save the database at {database_filename}."
        message_error += f" Error: {exception}"

        raise UnableToSaveVectorDatabaseError(message_error) from exception


def create_json_file(json_filename, raw_text_mapping):
    with open(json_filename, "w", encoding="utf8") as json_file:
        json.dump(raw_text_mapping, json_file)


def load_contents_of_json_file(json_filename):
    with open(json_filename, "r", encoding="utf8") as json_file:
        return json.load(json_file)


def ensure_parity_between_databases(memories_raw_data, index):
    if index.get_n_items() != len(memories_raw_data):
        raise DisparityBetweenDatabasesError(
            f"The length of the index contents ({index.get_n_items()}) doesn't match the length of the raw memory data ({len(memories_raw_data)})"
        )


def append_to_previous_json_memories_if_necessary(json_filename, memories):
    """This function will prevent squashing the previous json memories file
    if one exists, because it will load the contents of that file
    and add the new memories to that raw mapping.

    Args:
        json_filename (str): the full path to the json file
        memories (dict): new memories that need to be saved to disk

    Returns:
        dict: either the original memories or the previous memories + the new ones
    """
    # Remember to load all the memories in the json file,
    # or else you'll just overwrite the file with "create_json_file"
    if os.path.isfile(json_filename):
        raw_text_mapping = load_contents_of_json_file(json_filename)

        for index, entry in memories.items():
            raw_text_mapping[index] = entry

        return raw_text_mapping

    return memories


@validate_agent_type
def save_memories(agent, current_timestamp, new_memories, new_index):
    memories = {}

    for memory_description in new_memories:
        vector_index, memory = create_vectorized_memory(
            memory_description, current_timestamp, new_index
        )

        memories.update({vector_index: memory})

    database_filename = get_database_filename(agent)
    json_filename = get_json_filename(agent)

    create_vector_database(database_filename, new_index)

    memories = append_to_previous_json_memories_if_necessary(json_filename, memories)

    create_json_file(json_filename, memories)

    # ensure that there is parity between the length of both the json
    ensure_parity_between_databases(
        load_contents_of_json_file(json_filename), new_index
    )


def create_memories_database(agent, current_timestamp, seed_memories):
    new_index = create_new_index(METRIC_ANGULAR)

    save_memories(agent, current_timestamp, seed_memories, new_index)


def load_index_items_into_new_index(index, metric):
    new_index = create_new_index(metric)

    for i in range(index.get_n_items()):
        new_index.add_item(i, index.get_item_vector(i))

    # Vital to unload the original index, which should free up the database file.
    index.unload()

    return new_index


def update_memories_database(agent, current_timestamp, new_memories, index):
    new_index = load_index_items_into_new_index(index, METRIC_ANGULAR)

    save_memories(agent, current_timestamp, new_memories, new_index)


def create_new_index(metric):
    return AnnoyIndex(VECTOR_DIMENSIONS, metric)


def load_vector_database_index(database_name, metric):
    index = create_new_index(metric)

    try:
        index.load(database_name)
    except OSError as exception:
        raise DatabaseDoesntExistError(
            f"I failed to load the index of a vector database because the file doesn't seem to exist. The filename is '{database_name}'. Error: {exception}"
        ) from exception

    return index


def format_json_memory_data_for_python(memories_raw_data):
    for memory_key in memories_raw_data:
        memories_raw_data[memory_key] = {
            "description": memories_raw_data[memory_key]["description"],
            "creation_timestamp": datetime.datetime.fromisoformat(
                memories_raw_data[memory_key]["creation_timestamp"]
            ),
            "most_recent_access_timestamp": datetime.datetime.fromisoformat(
                memories_raw_data[memory_key]["most_recent_access_timestamp"]
            ),
            "recency": memories_raw_data[memory_key]["recency"],
            "importance": memories_raw_data[memory_key]["importance"],
        }

    return memories_raw_data


def load_agent_memories(agent):
    database_filename = get_database_filename(agent)
    json_filename = get_json_filename(agent)

    index = load_vector_database_index(database_filename, METRIC_ANGULAR)

    memories_raw_data = load_contents_of_json_file(json_filename)

    ensure_parity_between_databases(memories_raw_data, index)

    # Note: the timestamps stored in the JSON are strings. We need to convert them to proper timestamps
    memories_raw_data = format_json_memory_data_for_python(memories_raw_data)

    return index, memories_raw_data
