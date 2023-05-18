"""This module provides methods for determining action statuses of both agents and sandbox objects
"""
from anytree import Node
from agent import Agent
from enums import UpdateType
from environment import save_environment_tree_to_json
from errors import AlgorithmError, InvalidParameterError
from logging_messages import log_debug_message
from navigation import determine_agent_destination_node
from sandbox_object import SandboxObject
from vector_storage import load_agent_memories, update_memories_database
from wrappers import (
    validate_agent_has_character_summary,
    validate_agent_planned_action,
    validate_agent_type,
)


@validate_agent_type
@validate_agent_planned_action
def request_agent_action_status_for_using_object(agent):
    """Requests from the AI model what should be the agent's status given that he's using an object.

    Args:
        agent (Agent): the agent for whom the action status will be requested.

    Returns:
        str: the agent's action status for using an object
    """
    prompt = f"Write a summary of the action {agent.get_planned_action()} in a single sentence:"

    response = agent.get_request_response_function()(prompt)

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
    prompt += f" {agent.get_action_status()}. How has the {agent.get_using_object().name.name}'s status changed? "
    prompt += "For example: the state of a coffee machine would change from 'off' to 'brewing coffee'. "
    prompt += f"Write the {agent.get_using_object().name.name}'s new status in a single sentence:"

    response = agent.get_request_response_function()(prompt)

    log_debug_message(
        f"Object being used: {agent.get_using_object().name.name} --> Action status: {response}"
    )

    return response


@validate_agent_type
@validate_agent_planned_action
def produce_action_status_for_movement(agent):
    """Produces an action status related to the need of the agent to move to another location.

    Args:
        agent (Agent): the agent for whom the movement action status will be created
        action (str): the action that the agent will be heading to perform
    """
    log_debug_message(
        f"{agent.name} needs to move to {agent.get_destination_node().name.name}."
    )

    agent.set_action_status(
        f"{agent.name} is heading to use {agent.get_destination_node().name.name} ",
        silent=True,
    )
    agent.set_action_status(
        agent.get_action_status()
        + f"(located in {agent.get_destination_node().parent.name}), due to the following action: {agent.get_planned_action()}"
    )

    log_debug_message(f"{agent.name}: {agent.get_action_status()}")


@validate_agent_type
@validate_agent_planned_action
def determine_action_statuses_for_using_object(
    agent: Agent,
    simulation_name: str,
    request_agent_action_status_for_using_object_function,
    request_used_object_action_status_function,
    save_environment_tree_to_json_function,
):
    """Determines the action statuses that will be set for using a sandbox object

    Args:
        agent (Agent): the agent for whom the action status will be set
        simulation_name (str): the name of the simulation in which the agent is involved
        request_agent_action_status_for_using_object_function (function): the function that will request from the AI model the action status for using the sandbox object
        request_used_object_action_status_function (function): the function that will request the action status for the sandbox object being used

    Raises:
        AlgorithmError: if the current location node of the agent doesn't contain a SandboxObject; this function shouldn't have been called in that case
    """

    # This function should never be called if the current location node isn't a SandboxObject
    if not isinstance(agent.get_current_location_node().name, SandboxObject):
        message_error = f"The function {determine_action_statuses_for_using_object.__name__} was called even though the agent's current location "
        message_error += f"isn't a sandbox object: {agent.get_current_location_node()}"
        raise AlgorithmError(message_error)

    agent.set_using_object(agent.get_current_location_node())

    agent.set_action_status(
        request_agent_action_status_for_using_object_function(agent)
    )

    # One the agent has a status set, that agent is no longer "planning" an action.
    agent.set_planned_action(None)

    # Should ask the AI model what happens to the state of the object
    agent.get_using_object().name.set_action_status(
        request_used_object_action_status_function(agent), agent.name
    )

    # The state of the object has changed. The agent's environment tree needs to be saved to a file.
    save_environment_tree_to_json_function(
        simulation_name, f"{agent.name}_environment", agent.get_environment_tree()
    )


@validate_agent_type
@validate_agent_planned_action
def determine_if_agent_will_use_sandbox_object(agent: Agent, simulation_name: str):
    """Determines if the agent will use a sandbox object

    Args:
        agent (Agent): the agent for whom the determination will be made
        simulation_name (str): the name of the simulation in which the agent is involved

    Raises:
        AlgorithmError: if the agent passed had a None current location node
    """
    # sanity check
    if agent.get_current_location_node() is None:
        raise AlgorithmError(
            f"The function {determine_if_agent_will_use_sandbox_object.__name__} was called with an agent that didn't have a current location node set."
        )

    if isinstance(agent.get_current_location_node().name, SandboxObject):
        agent.notify({"type": UpdateType.AGENT_WILL_USE_SANDBOX_OBJECT, "agent": agent})

        # At this point, the agent does not have a destination, and is already able to start using the sandbox object
        determine_action_statuses_for_using_object(
            agent,
            simulation_name,
            request_agent_action_status_for_using_object,
            request_used_object_action_status,
            save_environment_tree_to_json,
        )

        # sanity check
        if agent.get_action_status() is None:
            error_message = f"The function {determine_if_agent_will_use_sandbox_object.__name___} was going to exit after establishing what object the agent was using, "
            error_message += f"even though {agent.name}'s action status is None."
            raise AlgorithmError(error_message)


@validate_agent_type
@validate_agent_planned_action
@validate_agent_has_character_summary
def produce_action_statuses_for_agent_based_on_destination_node(
    agent: Agent, destination_node: Node, simulation_name: str
):
    """Produces action statuses for an agent based on the destination node passed

    Args:
        agent (Agent): the agent for whom the action statuses will be produced
        destination_node (Node): the destination node, of type Node
        simulation_name (str): the name of the simulation involved
    """
    # Now we have both the action and the destination node.
    # If the destination node is the current node, the agent doesn't move.
    determine_agent_destination_node(agent, destination_node)

    # If at this point the agent still has a destination, then the action status should
    # represent that.
    if agent.get_destination_node() is not None:
        agent.notify({"type": UpdateType.AGENT_NEEDS_TO_MOVE, "agent": agent})

        produce_action_status_for_movement(agent)

        return

    determine_if_agent_will_use_sandbox_object(agent, simulation_name)

    # Sanity check:
    if (
        agent.get_current_location_node() is not None
        and agent.get_destination_node() is not None
    ):
        error_message = f"The function {produce_action_statuses_for_agent_based_on_destination_node.__name__} failed: it was going to end when the agent's "
        error_message += f"current_location_node and destination_node were non-None: {agent.get_current_location_node()} | {agent.get_destination_node()}"
        raise AlgorithmError(error_message)


@validate_agent_type
@validate_agent_has_character_summary
def produce_action_statuses_for_agent_and_sandbox_object(
    agent,
    current_timestamp,
    create_action_function,
    determine_sandbox_object_destination_from_root_function,
    produce_action_statuses_for_agent_based_on_destination_node_function,
    request_what_action_to_take_now_function,
    request_for_what_length_of_time_the_action_should_take_place_function,
):
    """Produces action statuses for a agent and for the sandbox object involved if it's used.

    Args:
        agent (Agent): the agent for whom the action will be produced.
        current_timestamp (datetime): the current timestamp
        create_action_function (function): the function responsible for creating an action
        determine_sandbox_object_destination_from_root_function (function): the function that determines what sandbox object gets used
    """
    action = create_action_function(
        agent,
        current_timestamp,
        load_agent_memories,
        update_memories_database,
        request_what_action_to_take_now_function,
        request_for_what_length_of_time_the_action_should_take_place_function,
    )

    agent.notify(
        {"type": UpdateType.AGENT_PRODUCED_ACTION, "agent": agent, "action": action}
    )

    agent.set_planned_action(action)

    destination_node = determine_sandbox_object_destination_from_root_function(
        agent, agent.get_environment_tree()
    )

    produce_action_statuses_for_agent_based_on_destination_node_function(
        agent, destination_node
    )

    # Sanity checks:
    if agent.get_action_status() is None:
        raise AlgorithmError(
            f"In the function {produce_action_statuses_for_agent_and_sandbox_object.__name__}, the agent's action status should be set at this point."
        )

    if agent.get_using_object() is not None:
        # if the agent is using an object, the used object's action status should be set
        if agent.get_using_object().name.get_action_status() is None:
            raise AlgorithmError(
                f"In the function {produce_action_statuses_for_agent_and_sandbox_object.__name__}, the used object's action status should be set at this point."
            )
