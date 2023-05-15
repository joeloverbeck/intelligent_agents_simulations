import anytree
from errors import InvalidParameterError

from location import Location
from sandbox_object import SandboxObject
from scoring import (
    determine_highest_scoring_node,
    request_rating_from_agent_for_sandbox_object_node,
)
from wrappers import validate_agent_has_character_summary, validate_agent_type


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
def determine_sandbox_object_node_to_use(agent, action, location_node):
    if not isinstance(location_node.name, Location):
        raise InvalidParameterError(
            f"The function {determine_sandbox_object_node_to_use.__name__} expected 'location_node' to be a node that contains a Location, but it was: {location_node}"
        )

    # first gather all the sandbox objects in the location passed
    all_sandbox_objects_in_location = [
        node for node in location_node.children if isinstance(node.name, SandboxObject)
    ]

    highest_scoring_node = determine_highest_scoring_node(
        agent,
        action,
        all_sandbox_objects_in_location,
        request_rating_from_agent_for_sandbox_object_node,
    )

    return highest_scoring_node


def node_children_contain_sandbox_object(node):
    return any(isinstance(child.name, SandboxObject) for child in node.children)
