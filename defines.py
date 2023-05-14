"""This module contains basic definitions for the behavior of the whole library.

Returns:
    _type_: _description_
"""
from sentence_transformers import SentenceTransformer

from wrappers import validate_agent_type

MODEL = SentenceTransformer("paraphrase-MiniLM-L6-v2")

VECTOR_DIMENSIONS = 384
NUMBER_OF_TREES = 10
METRIC_ANGULAR = "angular"
DECAY_RATE = 0.99
NUMBER_OF_RESULTS_FOR_QUERY = 50
SCORE_ALPHA = 1.0
SCORE_BETA = 1.0
SCORE_GAMMA = 1.0

INSTRUCT_WIZARDLM_PROMPT_HEADER = ""
INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING = "\n### Response:"


def get_seed_memories_filename(agent):
    """Returns the standarized filename for the seed_memories text file.

    Args:
        agent (Agent): the agent to whom the seed memories belong

    Returns:
        str: the full path to the corresponding seed_memories text file.
    """
    return f"agents/{agent.name.lower()}/seed_memories.txt"


@validate_agent_type
def get_database_filename(agent):
    """Returns the full path of the vector database.

    Args:
        agent (Agent): the agent to whom the memories belong.

    Returns:
        str: the full path of the vector database.
    """
    return f"agents/{agent.name.lower()}/memory_stream.ann"


@validate_agent_type
def get_json_filename(agent):
    """Returns the full path of the json file that contains or will contain an agent's memories.

    Args:
        agent (Agent): the agent to whom the memories belong.

    Returns:
        str: the full path of the json file that contains the agent's memories.
    """
    return f"agents/{agent.name.lower()}/memory_stream.json"
