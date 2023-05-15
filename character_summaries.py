from api_requests import request_response_from_ai_model
from defines import NUMBER_OF_RESULTS_FOR_QUERY
from logging_messages import log_debug_message
from memories_querying import (
    retrieve_description_from_scored_results_entry,
    search_memories,
)
from vector_storage import process_raw_data
from wrappers import validate_agent_type


def generate_summary_description_segment(
    agent, current_timestamp, query, prompt, memories_raw_data, index
):
    """Genererates a segment of a character summary

    Args:
        agent (Agent): the agent to whom the summary description corresponds
        current_timestamp (datetime): the current timestamp
        query (str): the query that will be made to the agent's memories
        prompt_header (str): the header for the prompt
        memories_raw_data (dict): the raw data of the agent's memories
        index (AnnoyIndex): the index of the Annoy library

    Returns:
        str: the response from the AI model
    """
    scored_results = search_memories(
        agent,
        current_timestamp,
        process_raw_data(query),
        NUMBER_OF_RESULTS_FOR_QUERY,
        memories_raw_data,
        index,
    )

    for _, vector_id in enumerate(scored_results):
        prompt += "- " + retrieve_description_from_scored_results_entry(
            vector_id, memories_raw_data
        )

    log_debug_message(f"{prompt}")

    return request_response_from_ai_model(prompt)


@validate_agent_type
def request_character_summary(agent, current_timestamp, memories_raw_data, index):
    """Produces the agent's character summary through the AI model

    Args:
        agent (Agent): the agent to whom the memories belong
        current_timestamp (datetime): the current timestamp
        memories_raw_data (dict): the raw data of the agent's memories
        index (AnnoyIndex): the index of the Annoy database

    Returns:
        str: the generated summary description for the agent involved
    """
    # First of all we perform a retrieval on the query "[name]'s core characteristics"
    prompt = f"How would one describe {agent.name}'s core characteristics given the following statements? "
    prompt += f"Start the sentence by saying either '{agent.name} is' or '{agent.name} has':\n"
    core_characteristics = generate_summary_description_segment(
        agent,
        current_timestamp,
        f"{agent.name}'s core characteristics",
        prompt,
        memories_raw_data,
        index,
    )

    prompt = f"How would one describe {agent.name}'s current daily occupation given the following statements? "
    prompt += f"Start the sentence by saying either '{agent.name} is' or '{agent.name} has':\n"

    current_daily_occupation = generate_summary_description_segment(
        agent,
        current_timestamp,
        f"{agent.name}'s current daily occupation",
        prompt,
        memories_raw_data,
        index,
    )

    prompt = f"How would one describe {agent.name}'s feeling about his recent progress in life given the "
    prompt += f"following statements? Start the sentence by saying either '{agent.name} is' or '{agent.name} has':\n"

    recent_progress_in_life = generate_summary_description_segment(
        agent,
        current_timestamp,
        f"{agent.name}'s feeling about his recent progress in life",
        prompt,
        memories_raw_data,
        index,
    )

    innate_traits = generate_summary_description_segment(
        agent,
        current_timestamp,
        f"{agent.name}'s innate traits",
        f"How would one describe {agent.name}'s innate traits given the following statements? Write it solely as a series of adjectives:\n",
        memories_raw_data,
        index,
    )

    summary_description = f"Name: {agent.name} (age: {agent.age})\n"
    summary_description += f"Innate traits: {innate_traits}\n"
    summary_description += (
        f"{core_characteristics}\n{current_daily_occupation}\n{recent_progress_in_life}"
    )

    log_debug_message(
        f"Function {request_character_summary.__name__}:\n{summary_description}"
    )

    return summary_description
