"""This module contains operations that allow agents to move in the environment tree
"""
from anytree import Node
from agent import Agent
from enums import UpdateType
from errors import AlgorithmError
from location import Location
from logging_messages import log_debug_message
from one_step_movement import get_node_one_step_closer_to_destination

from sandbox_object import SandboxObject
from sandbox_object_utils import node_children_contain_sandbox_object
from scoring import (
    determine_highest_scoring_node,
    request_rating_from_agent_for_location_node,
    request_rating_from_agent_for_sandbox_object_node,
)
from wrappers import (
    validate_agent_has_character_summary,
    validate_agent_planned_action,
    validate_agent_type,
)


@validate_agent_type
@validate_agent_planned_action
@validate_agent_has_character_summary
def determine_sandbox_object_destination_from_root(agent: Agent, root_node: Node):
    """Determines the sandbox object destination from the root of the environment tree

    Args:
        agent (Agent): the agent for whom will be determined what sandbox object will be used
        root_node (Node): the root of the environment tree

    Raises:
        AlgorithmError: if the root node received contains a SandboxObject

    Returns:
        Node: the highest-scoring node that should become the destination node of the agent
    """
    # We base all the calculations on the current 'root_node'

    log_debug_message(f"Checking root_node {root_node}")

    # The current root node can never be a sandbox object.
    if isinstance(root_node.name, SandboxObject):
        raise AlgorithmError(
            f"The function {determine_sandbox_object_destination_from_root.__name__} received a node that contained a SandboxObject. That shouldn't happen."
        )

    if root_node.children is None:
        log_debug_message(f"Found that node {root_node} didn't have children.")
        # the current root isn't a sandbox object, yet it doesn't have children
        # either.
        return root_node

    # We check if the children of root_node contain any sandbox object
    if not node_children_contain_sandbox_object(root_node):
        # Must rate the locations and call this function recursively,
        # because we still haven't located the last node that contains
        # a location with children
        highest_scoring_node = determine_highest_scoring_node(
            agent,
            root_node.children,
            request_rating_from_agent_for_location_node,
        )

        return determine_sandbox_object_destination_from_root(
            agent, highest_scoring_node
        )

    # in this case, root_node has nodes that contain sandbox objects
    return determine_highest_scoring_node(
        agent,
        root_node.children,
        request_rating_from_agent_for_sandbox_object_node,
    )


@validate_agent_type
@validate_agent_has_character_summary
def determine_agent_destination_node(agent: Agent, destination_node: Node):
    """Determines the agent's destination node depending on the destination node passed

    Args:
        agent (Agent): the agent for whom the destination node will be determined
        destination_node (Node): the destination node that will determine the agent's destination node
    """
    if destination_node == agent.get_current_location_node():
        agent.set_destination_node(None)

        agent.notify(
            {
                "type": UpdateType.AGENT_REACHED_DESTINATION,
                "agent": agent,
                "destination_node": destination_node,
            }
        )
        log_debug_message(
            f"{agent.name} is at destination {destination_node.name.name}."
        )
    else:
        agent.set_destination_node(destination_node)


@validate_agent_type
def move_agent_immediately_to_containing_location_if_necessary(agent: Agent):
    """Moves the agent to the current sandbox object's containing location if necessary

    Args:
        agent (Agent): the agent for whom the movement will be performed
    """
    # Note: if we have already decided that we need to move, if the agent is at
    # a SandboxObject, the agent should move immediately to the containing location.
    if isinstance(agent.get_current_location_node().name, SandboxObject):
        agent.set_current_location_node(agent.get_current_location_node().parent)


def crash_if_next_node_closer_to_destination_is_none(
    next_node_closer_to_destination: Node, agent: Agent
):
    """Crashes if the next node closer to destination is None, because that calculation
    shouldn't have been made if the agent was already at the destination,
    or if the agent didn't have a destination

    Args:
        next_node_closer_to_destination (Node): the next node closer to the destination node

    Raises:
        AlgorithmError: if the next_node_closer_to_destination is None
    """
    if next_node_closer_to_destination is None:
        error_message = f"The function {perform_agent_movement.__name__} was about to set a current location node None to an agent."
        error_message += f"\nAgent's current location node: {agent.get_current_location_node()}. Destination node: {agent.get_destination_node()}"
        error_message += f"\nAgent's environment tree: {agent.get_environment_tree()}"
        raise AlgorithmError(error_message)


@validate_agent_type
def set_current_location_as_destination_sandbox_object_if_in_same_location(
    agent: Agent,
):
    """Sets the agent's current location node as the destination sandbox object, if that object is in the agent's current location

    Args:
        agent (Agent): the agent for whom the current location node may be changed
    """
    if isinstance(agent.get_current_location_node().name, Location) and isinstance(
        agent.get_destination_node().name, SandboxObject
    ):
        for child in agent.get_current_location_node().children:
            if child.name == agent.get_destination_node().name:
                agent.set_current_location_node(child)
                break


@validate_agent_type
def set_agent_destination_as_none_if_already_at_destination(agent: Agent):
    """If the agent is already at the set destination, it sets the destination as None

    Args:
        agent (Agent): the agent for whom the change will be made
    """
    if agent.get_destination_node() is not None:
        if agent.get_current_location_node().name == agent.get_destination_node().name:
            agent.set_destination_node(None)


@validate_agent_type
def perform_agent_movement(agent: Agent):
    """Performs the agent's movement depending on his or her current attribute values.
    Ex. if an agent has a destination_node set, this function will move the agent
    a node closer to the destination.

    Args:
        agent (Agent): the agent that will be displaced
    """
    # Note that this function can be called when an agent doesn't need to move.
    if agent.get_destination_node() is None:
        return

    if agent.get_current_location_node() == agent.get_destination_node():
        # Agent is already at destination. No movement is needed.
        agent.set_destination_node(None)
        return

    move_agent_immediately_to_containing_location_if_necessary(agent)

    next_node_closer_to_destination = get_node_one_step_closer_to_destination(agent)

    # Note, the current location node should never be none.
    crash_if_next_node_closer_to_destination_is_none(
        next_node_closer_to_destination, agent
    )

    agent.set_current_location_node(next_node_closer_to_destination)

    # After moving one step, it could be that this location contains the destination
    # sandbox object node.
    set_current_location_as_destination_sandbox_object_if_in_same_location(agent)

    # if agent is already at destination, then set destination node as none
    set_agent_destination_as_none_if_already_at_destination(agent)
