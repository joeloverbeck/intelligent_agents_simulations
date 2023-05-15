from errors import AlgorithmError
from location import Location
from logging_messages import log_debug_message

from sandbox_object import SandboxObject
from sandbox_object_utils import node_children_contain_sandbox_object
from scoring import (
    determine_highest_scoring_node,
    request_rating_from_agent_for_location_node,
    request_rating_from_agent_for_sandbox_object_node,
)
from wrappers import validate_agent_has_character_summary, validate_agent_type


@validate_agent_type
def get_node_one_step_closer_to_destination(agent):
    """Returns the node one step closer from the agent's current location to the destination.
    Note: it can return None if no next step exists (such as when the agent is already at destination.)

    Args:
        agent (Agent): the agent whose route this function will track.

    Returns:
        Node: the node one step closer to the agent's destination
    """
    current_location = agent.current_location
    destination = agent.destination

    # If the current_location and destination are the same, we return None;
    # there is no next node in the route
    if current_location == destination:
        return None

    # If there is no destination, there is no next node.
    if destination is None:
        return None

    # If the current location is a descendant of the destination, move up the tree
    if current_location in destination.descendants:
        return current_location.parent

    # If the current location is an ancestor of the destination, move down the tree
    if current_location in destination.ancestors:
        # Find the child of the current location that is also an ancestor of the destination
        for child in current_location.children:
            if child in destination.path:
                return child

    # If the current location is neither a descendant nor an ancestor of the destination,
    # this means they are on separate branches. In this case, move one step up the tree.
    else:
        return current_location.parent


@validate_agent_type
@validate_agent_has_character_summary
def determine_sandbox_object_destination_from_root(agent, action, root_node):
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
            action,
            root_node.children,
            request_rating_from_agent_for_location_node,
        )

        return determine_sandbox_object_destination_from_root(
            agent, action, highest_scoring_node
        )

    else:
        # in this case, root_node has nodes that contain sandbox objects
        return determine_highest_scoring_node(
            agent,
            action,
            root_node.children,
            request_rating_from_agent_for_sandbox_object_node,
        )


@validate_agent_type
def perform_agent_movement(agent):
    if agent.current_location == agent.destination:
        # Agent is already at destination. No movement is needed.
        agent.destination = None
        return

    next_node_closer_to_destination = get_node_one_step_closer_to_destination(agent)

    agent.current_location = next_node_closer_to_destination

    # After moving one step, it could be that this location contains the destination
    # sandbox object node.
    if isinstance(agent.current_location.name, Location) and isinstance(
        agent.destination.name, SandboxObject
    ):
        for child in agent.current_location.children:
            if child.name == agent.destination.name:
                agent.current_location = child
                break
