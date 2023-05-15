from anytree import Node
from api_requests import request_response_from_ai_model
from defines import (
    INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING,
    INSTRUCT_WIZARDLM_PROMPT_HEADER,
)
from errors import InvalidParameterError
from logging_messages import log_debug_message
from regular_expression_utils import extract_rating_from_text
from string_utils import end_string_with_period
from wrappers import validate_agent_has_character_summary, validate_agent_type


def determine_highest_scoring_node(
    agent, action, set_of_nodes, request_rating_from_agent_for_node_function
):
    scored_nodes = {}

    for node in set_of_nodes:
        scored_nodes[node] = request_rating_from_agent_for_node_function(
            agent, action, node
        )

    # return the highest scoring node
    return max(scored_nodes, key=scored_nodes.get)


@validate_agent_type
@validate_agent_has_character_summary
def request_rating_from_agent_for_sandbox_object_node(
    agent, action, sandbox_object_node
):
    """Requests the rating from an agent for a sandbox object

    Args:
        agent (Agent): the agent from whom the rating is made
        action (str): the action in natural English
        sandbox_object_node (Node): the sandbox object whose usefulness will be rated

    Raises:
        InvalidParameterError: if the sandbox_object passed isn't of type SandboxObject

    Returns:
        int: the rating/score for the sandbox object given the action passed
    """
    if not isinstance(sandbox_object_node, Node):
        raise InvalidParameterError(
            f"The function {request_rating_from_agent_for_sandbox_object_node.__name__} expected 'sandbox_object' to be a Node, but it was {sandbox_object_node}"
        )

    # create the prompt to send to the AI model
    prompt = INSTRUCT_WIZARDLM_PROMPT_HEADER + agent.get_character_summary() + "\n"
    prompt += f"Given the following object: {sandbox_object_node.name.name} ({sandbox_object_node.name.description}).\n"
    prompt += "On the scale of 1 to 10, where 1 is useless (isn't related to the action) and 10 is essential (best possible object to fulfill the action),"
    prompt += f" determine how {agent.name} would rate how essential the {sandbox_object_node.name.name} "
    prompt += f"(located in {sandbox_object_node.parent.name.name}) is for the following action: "
    prompt += f"{end_string_with_period(action)}\n"
    prompt += (
        f"Rate how essential the {sandbox_object_node.name.name} is regarding the action above. Output a number from 1 to 10:"
        + INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING
    )

    log_debug_message(f"{prompt}")

    rating_response = request_response_from_ai_model(prompt)

    log_debug_message(f"{rating_response}")

    return extract_rating_from_text(rating_response)


@validate_agent_type
@validate_agent_has_character_summary
def request_rating_from_agent_for_location_node(agent, action, location_node):
    """Request the rating from agent for the location node.

    Args:
        agent (Agent): the agent for whom the rating will be made
        action (str): the agent's action in plain English
        location_node (Node): the location node that will be rated

    Returns:
        int: the processed rating the AI gave for the location passed
    """
    if not isinstance(location_node, Node):
        raise InvalidParameterError(
            f"The function {request_rating_from_agent_for_location_node.__name__} expected 'location_node' to be a Node, but it was: {location_node}"
        )

    # Create the prompt to send to the AI model
    prompt = INSTRUCT_WIZARDLM_PROMPT_HEADER + agent.get_character_summary() + "\n"
    prompt = f"{agent.name} is currently in {location_node.name}.\n"
    prompt += (
        "* Prefer to stay in the current area if the activity can be done there.\n"
    )
    prompt += f"How absolutely necessary is the location {location_node.name.name} "
    prompt += f"({location_node.name.description}) for {agent.name}'s action: {action}. Rate the location {location_node.name.name} "
    prompt += (
        "for the action with a number in the range [1, 10]:"
        + INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING
    )

    log_debug_message(f"{prompt}")

    rating_response = request_response_from_ai_model(prompt)

    log_debug_message(f"{rating_response}")

    return extract_rating_from_text(rating_response)
