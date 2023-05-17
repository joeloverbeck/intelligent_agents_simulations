from collections import deque
from anytree import Node
from agent import Agent
from wrappers import validate_agent_type


def bfs(current_location: Node, destination: Node):
    """Performs a breadth-first search from the current location to the destination.

    Args:
        current_location (Node): The starting node.
        destination (Node): The target node.

    Returns:
        Node: The next node on the shortest path from the current location to the destination, or None if no path exists.
    """
    visited = set()
    queue = deque([(current_location, [])])

    while queue:
        node, path = queue.popleft()
        if node not in visited:
            visited.add(node)
            if node == destination:
                # Return the second node in the path, which is the next step from the current location
                return path[1] if len(path) > 1 else None
            # Add the node's children to the queue
            for child in node.children:
                if child not in visited:
                    queue.append((child, path + [node, child]))
            # If the node has a parent and it's not in visited, add it to the queue
            if node.parent is not None and node.parent not in visited:
                queue.append((node.parent, path + [node, node.parent]))
    return None  # Return None if no path exists


@validate_agent_type
def get_node_one_step_closer_to_destination(agent: Agent):
    """Returns the node one step closer from the agent's current location to the destination.
    Note: it can return None if no next step exists (such as when the agent is already at destination.)

    Args:
        agent (Agent): the agent whose route this function will track.

    Returns:
        Node: the node one step closer to the agent's destination
    """
    current_location = agent.get_current_location_node()
    destination = agent.get_destination_node()

    if current_location is None or destination is None:
        return None
    if current_location == destination:
        return None

    # Use BFS to find the next step
    return bfs(current_location, destination)
