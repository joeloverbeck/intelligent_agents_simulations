import anytree

from api_requests import request_response_from_ai_model
from defines import (
    INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING,
    INSTRUCT_WIZARDLM_PROMPT_HEADER,
)
from errors import InvalidParameterError
from regular_expression_utils import extract_rating_from_text
from sandbox_object import SandboxObject
from string_utils import end_string_with_period
from wrappers import validate_agent_has_character_summary, validate_agent_type


@validate_agent_type
@validate_agent_has_character_summary
def request_rating_from_agent_for_sandbox_object(agent, action, sandbox_object):
    """Requests the rating from an agent for a sandbox object

    Args:
        agent (Agent): the agent from whom the rating is made
        action (str): the action in natural English
        sandbox_object (SandboxObject): the sandbox object whose usefulness will be rated

    Raises:
        InvalidParameterError: if the sandbox_object passed isn't of type SandboxObject

    Returns:
        int: the rating/score for the sandbox object given the action passed
    """
    if not isinstance(sandbox_object, SandboxObject):
        raise InvalidParameterError(
            f"The function {request_rating_from_agent_for_sandbox_object.__name__} expected 'sandbox_object' to be a SandboxObject, but it was {sandbox_object}"
        )

    # create the prompt to send to the AI model
    prompt = INSTRUCT_WIZARDLM_PROMPT_HEADER + agent.get_character_summary() + "\n"
    prompt += f"Given the following object: {sandbox_object.name} ({sandbox_object.description}).\n"
    prompt += "On the scale of 1 to 10, where 1 is useless (isn't related to the action) and 10 is essential (best possible object to fulfill the action),"
    prompt += f" determine how {agent.name} would rate the likely usefulness of the {sandbox_object.name} for the following action: "
    prompt += f"{end_string_with_period(action)}\n"
    prompt += f"Rate the usefulness of the {sandbox_object.name} regarding the action above. Output a number from 1 to 10:" + INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING

    print(f"\nTest prompt: {prompt}\n")

    rating_response = request_response_from_ai_model(prompt)

    print(f"\nRating response: {rating_response}\n")

    return extract_rating_from_text(rating_response)


def find_all_sandbox_objects_in_environment_tree(environment_tree):
    """Finds and returns all nodes in an environment tree that contains sandbox objects

    Args:
        environment_tree (Node): the root of an environment tree

    Returns:
        list: a list with all the nodes in the passed environment tree that contain sandbox objects
    """
    return [
        node
        for node in anytree.PreOrderIter(environment_tree)
        if isinstance(node.name, SandboxObject)
    ]


@validate_agent_type
@validate_agent_has_character_summary
def determine_sandbox_object_node_to_use(agent, action):
    # first gather all the sandbox objects in the agent's environment tree
    all_sandbox_objects = find_all_sandbox_objects_in_environment_tree(
        agent.environment_tree
    )

    scored_nodes = {}

    for sandbox_object in all_sandbox_objects:
        # Note that the sandbox object itself is accessed through 'sandbox_object.name'
        scored_nodes[sandbox_object] = request_rating_from_agent_for_sandbox_object(
            agent, action, sandbox_object.name
        )

    # return the highest scoring node
    highest_scoring_node = max(scored_nodes, key=scored_nodes.get)

    return highest_scoring_node
