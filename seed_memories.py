"""This module handles operations related to the seed memories that are stored in txt files.

"""

import os
from defines import get_database_filename, get_json_filename, get_seed_memories_filename
from errors import FileDoesntExistError
from string_utils import end_string_with_period
from vector_storage import create_memories_database


def create_database_of_memories_from_seed_memories(agent, current_timestamp):
    """Creates a database of memories for an agent from the seed memories

    Args:
        agent (Agent): the agent to whom the seed memories belong
        current_timestamp (datetime): the current timestamp

    Raises:
        FileDoesntExistError: if 'seed_memories.txt' doesn't exist for the given agent
    """
    database_filename = get_database_filename(agent)
    json_filename = get_json_filename(agent)

    if not os.path.isfile(database_filename) and not os.path.isfile(json_filename):
        # must create the memories from the seed_memories.txt
        seed_memories_filename = get_seed_memories_filename(agent)
        if not os.path.isfile(seed_memories_filename):
            raise FileDoesntExistError(
                f"The simulation needed to create the memories for '{agent.name}', but '{seed_memories_filename}' does not exist."
            )

        # at this point the file of seed memories exist, so we must load it
        # and create the memories
        seed_memories = load_seed_memories(agent)

        create_memories_database(agent, current_timestamp, seed_memories)


def load_seed_memories(agent):
    """Loads the seed memories of the passed agent from the text file.

    Args:
        agent (Agent): the agent to whom the seed memories belong.

    Returns:
        list: cleaned seed memories, which are str.
    """
    seed_memories_filename = get_seed_memories_filename(agent)

    with open(seed_memories_filename, "r", encoding="utf-8") as file:
        seed_memories = file.read().strip().split(";")

    return [end_string_with_period(seed_memory) for seed_memory in seed_memories]
