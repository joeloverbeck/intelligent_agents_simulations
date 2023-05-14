"""This module contains many operations related to storing and retrieving agent memories
"""
import datetime
import json
import os

from annoy import AnnoyIndex
from api_requests import request_response_from_ai_model
from defines import (
    DECAY_RATE,
    INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING,
    INSTRUCT_WIZARDLM_PROMPT_HEADER,
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
)
from math_utils import calculate_recency, normalize_value
from regular_expression_utils import extract_importance_from_text


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

    importance_prompt = f"{INSTRUCT_WIZARDLM_PROMPT_HEADER}On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) "
    importance_prompt += "and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy "
    importance_prompt += "of the following piece of memory."
    importance_prompt += f" Memory: {memory_description}"
    importance_prompt += (
        "\nRating: <fill in>." + INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING
    )

    importance_response = request_response_from_ai_model(importance_prompt)

    extracted_importance = extract_importance_from_text(importance_response)

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

    new_index.save(database_filename)


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


def create_memories_database(agent, current_timestamp, seed_memories):
    new_index = create_new_index(METRIC_ANGULAR)

    memories = {}

    for memory_description in seed_memories:
        vector_index, memory = create_vectorized_memory(
            memory_description, current_timestamp, new_index
        )

        memories.update({vector_index: memory})

    database_filename = get_database_filename(agent)
    json_filename = get_json_filename(agent)

    create_vector_database(database_filename, new_index)
    create_json_file(json_filename, memories)

    # ensure that there is parity between the length of both the json
    ensure_parity_between_databases(
        load_contents_of_json_file(json_filename), new_index
    )


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
