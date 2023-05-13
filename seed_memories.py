"""This module handles operations related to the seed memories that are stored in txt files.

"""

from defines import get_seed_memories_filename
from string_utils import end_string_with_period


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
