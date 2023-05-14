import anytree

from sandbox_object import SandboxObject
from wrappers import validate_agent_type


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
