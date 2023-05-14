from api_requests import request_response_from_ai_model
from defines import (
    INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING,
    INSTRUCT_WIZARDLM_PROMPT_HEADER,
)
from regular_expression_utils import extract_rating_from_text
from string_utils import end_string_with_period
from wrappers import validate_agent_has_character_summary, validate_agent_type


@validate_agent_type
@validate_agent_has_character_summary
def request_rating_from_agent_for_sandbox_object(agent, action, sandbox_object):
    """Requests from the AI model to rate the usefulness of a sandbox object for a given plan

    Args:
        agent (Agent): the agent who will perform the action
        action (str): the action that will be performed
        sandbox_object (SandboxObject): the sandbox object whose usefulness will be rated

    Returns:
        int: a rating from 1 to 10 regarding the usefulness of the sandbox object for the plan
    """
    # create the prompt to send to the AI model
    prompt = INSTRUCT_WIZARDLM_PROMPT_HEADER + agent.get_character_summary() + "\n"
    prompt += f"Given the following object: {sandbox_object.name} ({sandbox_object.description}).\n"
    prompt += f"On the scale of 1 to 10, where 1 is useless and 10 is vital, determine how {agent.name} "
    prompt += (
        "would rate the likely usefulness of the object for the following action.\n"
    )
    prompt += f" Action: {end_string_with_period(action)}\n"
    prompt += "Rating: <fill in>." + INSTRUCT_WIZARDLM_PROMPT_ANSWER_OPENING

    print(f"\nTest prompt: {prompt}\n")

    rating_response = request_response_from_ai_model(prompt)

    return extract_rating_from_text(rating_response)
