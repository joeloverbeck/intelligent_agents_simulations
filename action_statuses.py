from api_requests import request_response_from_ai_model
from anytree import Node
from errors import AlgorithmError, InvalidParameterError
from logging_messages import log_debug_message
from sandbox_object import SandboxObject
from vector_storage import load_agent_memories, update_memories_database
from wrappers import validate_agent_has_character_summary, validate_agent_type


def request_agent_action_status_for_using_object(agent, action):
    """Requests from the AI model what should be the agent's status given that he's using an object.

    Args:
        agent (Agent): the agent for whom the action status will be requested.

    Returns:
        str: the agent's action status for using an object
    """
    prompt = f"Write a summary of the action {action} in a single sentence:"

    response = request_response_from_ai_model(prompt)

    log_debug_message(f"Agent {agent.name} --> Action Status: {response}")

    return response


def request_used_object_action_status(agent):
    """Requests from the AI model what action status the used object should have.

    Args:
        agent (Agent): the agent who uses the sandbox object

    Raises:
        InvalidParameterError: if the agent's 'using_object' attribute doesn't have a node set.
        InvalidParameterError: if the agent's 'using_object' doesn't contain a node with a SandboxObject

    Returns:
        str: the action status that should be used for the object being used
    """
    # at this point, the agent should have a node in 'using_object'
    if agent.get_using_object() is None:
        raise InvalidParameterError(
            f"The function {request_used_object_action_status.__name__} expected 'agent.get_using_object()' to have an object node at this point."
        )
    if not isinstance(agent.get_using_object().name, SandboxObject):
        raise InvalidParameterError(
            f"The function {request_used_object_action_status.__name__} expected 'agent.get_using_object()' to be a node containing a SandboxObject."
        )

    prompt = f"Given the following action that {agent.name} is performing on {agent.get_using_object().name.name}:"
    prompt += f" {agent.get_action_status()}. What should be the object's {agent.get_using_object().name.name} status now? Write it in a single sentence:"

    response = request_response_from_ai_model(prompt)

    log_debug_message(
        f"Object being used: {agent.get_using_object().name.name} --> Action status: {response}"
    )

    return response


def produce_action_status_for_movement(agent, action):
    """Produces an action status related to the need of the agent to move to another location.

    Args:
        agent (Agent): the agent for whom the movement action status will be created
        action (str): the action that the agent will be heading to perform
    """
    log_debug_message(f"{agent.name} needs to move to {agent.get_destination_node().name.name}.")

    agent.set_action_status(f"{agent.name} is heading to use {agent.get_destination_node().name.name} ")
    agent.set_action_status(agent.get_action_status() + f"(located in {agent.get_destination_node().parent.name}), due to the following action: {action}")

    log_debug_message(f"{agent.name}: {agent.get_action_status()}")


def determine_action_statuses_for_using_object(agent, destination_node, action):
    """Determines the action statuses that will be set for both the agent and the object being used.

    Args:
        agent (Agent): the agent for whom the relevant action statuses will be created
        destination_node (Node): the node to whom the agent will move
    """
    if not isinstance(destination_node, Node):
        raise InvalidParameterError(
            f"The function {determine_action_statuses_for_using_object.__name__} expected 'destination_node' to be a Node."
        )

    agent.set_using_object(destination_node)

    agent.set_action_status(request_agent_action_status_for_using_object(agent, action))

    # Should ask the AI model what happens to the state of the object
    agent.get_using_object().name.set_action_status(request_used_object_action_status(agent))


@validate_agent_type
@validate_agent_has_character_summary
def produce_action_statuses_for_agent_and_sandbox_object(
    agent,
    current_timestamp,
    create_action_function,
    determine_sandbox_object_destination_from_root_function,
):
    """Produces action statuses for a agent and for the sandbox object involved if it's used.

    Args:
        agent (Agent): the agent for whom the action will be produced.
        current_timestamp (datetime): the current timestamp
        create_action_function (function): the function responsible for creating an action
        determine_sandbox_object_destination_from_root_function (function): the function that determines what sandbox object gets used
    """
    action = create_action_function(
        agent, current_timestamp, load_agent_memories, update_memories_database
    )

    destination_node = determine_sandbox_object_destination_from_root_function(
        agent, action, agent.environment_tree
    )

    # Now we have both the action and the destination node.
    # If the destination node is the current node, the agent doesn't move.
    if destination_node == agent.get_current_location_node():
        agent.set_destination_node(None)
        log_debug_message(
            f"{agent.name} is at destination {destination_node.name.name}."
        )
    else:
        agent.set_destination_node(destination_node)

    # If at this point the agent still has a destination, then the action status should
    # represent that.
    if agent.get_destination_node() is not None:
        produce_action_status_for_movement(agent, action)

        return

    # At this point, the agent does not have a destination, and is already able to start using the sandbox object
    determine_action_statuses_for_using_object(agent, destination_node, action)

    # Sanity check:
    if agent.get_action_status() is None:
        raise AlgorithmError(
            f"In the function {produce_action_statuses_for_agent_and_sandbox_object.__name__}, the agent's action status should be set at this point."
        )
    if agent.get_using_object().name.get_action_status() is None:
        raise AlgorithmError(
            f"In the function {produce_action_statuses_for_agent_and_sandbox_object.__name__}, the used object's action status should be set at this point."
        )
