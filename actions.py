from api_requests import request_response_from_ai_model
from datetime_utils import format_date
from defines import (
    INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING,
    INSTRUCT_WIZARDLM_PROMPT_HEADER,
    NUMBER_OF_RESULTS_FOR_QUERY,
)
from logging_messages import log_debug_message
from memories_querying import get_most_recent_memories
from string_utils import end_string_with_period
from wrappers import validate_agent_has_character_summary, validate_agent_type


@validate_agent_type
@validate_agent_has_character_summary
def request_what_action_to_take_now(agent, current_timestamp, most_recent_memories):
    """Requests to the AI model what action the agent should take now.

    Args:
        agent (Agent): the agent for whom the request will be made.
        current_timestamp (datetime): the current timestamp
        most_recent_memories (dict): the most recent memories of the agent

    Returns:
        str: the plan received from the AI model
    """
    prompt = INSTRUCT_WIZARDLM_PROMPT_HEADER + agent.get_character_summary() + "\n"
    prompt += "Most recent memories:\n"

    for most_recent_memory in most_recent_memories:
        prompt += f"- {most_recent_memory['description']}\n"

    prompt += f"Now it is {format_date(current_timestamp)}. Decide what single action {agent.name} should take right now. "
    prompt += f"Format: {agent.name} is going to <action>"
    prompt += INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING

    return request_response_from_ai_model(prompt)


@validate_agent_type
@validate_agent_has_character_summary
def request_for_what_length_of_time_the_action_should_take_place(
    agent, current_timestamp, action, most_recent_memories
):
    """Requests from the AI model for what length the plan should take place.

    Args:
        agent (Agent): the agent for whom the request will be made.
        current_timestamp (datetime): the current timestamp
        action (str): the action that the agent is going to take
        most_recent_memories (dict): the most recent memories of the agent

    Returns:
        str: for how long should the action take place
    """
    # Now determine for what length of time should the agent perform this action.
    prompt = INSTRUCT_WIZARDLM_PROMPT_HEADER + agent.get_character_summary() + "\n"
    prompt += "Most recent memories:\n"

    for most_recent_memory in most_recent_memories:
        prompt += f"- {most_recent_memory['description']}\n"
    prompt += f"Now it is {format_date(current_timestamp)}. {agent.name} is planning to take the following action: {end_string_with_period(action)}.\n"
    prompt += (
        "For how many minutes should this action take place?"
        + INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING
    )

    return request_response_from_ai_model(prompt)


@validate_agent_type
@validate_agent_has_character_summary
def create_action(
    agent,
    current_timestamp,
    load_agent_memories_function,
    update_memories_database_function,
):
    """Creates an action for the agent.

    Args:
        agent (Agent): the agent for whom the action will be created.
        current_timestamp (datetime): the current timestamp; the action will be created with it.
        load_agent_memories_function (fuction): the function responsible for loading agent memories
        update_memories_database_function (function): the function responsible for updating memories databases
    """
    index, memories_raw_data = load_agent_memories_function(agent)

    most_recent_memories = get_most_recent_memories(
        current_timestamp, NUMBER_OF_RESULTS_FOR_QUERY, memories_raw_data
    )

    action = request_what_action_to_take_now(
        agent, current_timestamp, most_recent_memories
    )

    length_of_time = request_for_what_length_of_time_the_action_should_take_place(
        agent, current_timestamp, action, most_recent_memories
    )

    action = f"{format_date(current_timestamp)}. {action} {length_of_time}"

    log_debug_message(f"Function {create_action.__name__}:\n{action}")

    # Save the memory in the file.
    update_memories_database_function(agent, current_timestamp, [action], index)

    return action
