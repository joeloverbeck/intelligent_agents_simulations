from anytree import Node

from environment import find_node_by_identifier
from errors import AlgorithmError, NodeTypeUnhandledError
from location import Location
from sandbox_object import SandboxObject


def update_node_name_and_description(matching_node: Node, updated_node: Node):
    """Updates the name and description of the matching node with those of the updated node

    Args:
        matching_node (Node): the matching node that will have its values changed
        updated_node (Node): the node that has the updated values
    """
    matching_node.name.name = updated_node.name.name
    matching_node.name.description = updated_node.name.description


def handle_sandbox_object_child(
    child: Node, updated_node: Node, triggering_agent_name: str
):
    """Handles the case that one of the children of the matching Location is a SandboxObject

    Args:
        child (Node): the node containing a SandboxObject
        updated_node (Node): the node with the updated values
        triggering_agent_name (str): the name of the agent that triggered this update

    Raises:
        AlgorithmError: if the matching sandbox object node in the updated node is None
    """
    matching_sandbox_object_node = find_node_by_identifier(
        updated_node, child.name.get_identifier()
    )

    if matching_sandbox_object_node is None:
        raise AlgorithmError(
            f"Could not find a matching sandbox object node in the updated node's children for the identifier {child.name.get_identifier()}."
        )

    update_node_name_and_description(child, matching_sandbox_object_node)

    child.name.set_action_status(
        matching_sandbox_object_node.name.get_action_status(), triggering_agent_name
    )


def handle_case_matching_node_in_environment_tree_is_location(
    matching_node: Node, updated_node: Node, triggering_agent_name: str
):
    """Handles the case when the matching node in the environment tree is a Location

    Args:
        matching_node (Node): the matching node, which contains a Location
        updated_node (Node): the updated node that contains updated values
    """
    update_node_name_and_description(matching_node, updated_node)

    for child in matching_node.children:
        if isinstance(child.name, SandboxObject):
            handle_sandbox_object_child(child, updated_node, triggering_agent_name)


def handle_case_matching_node_in_environment_tree_is_sandbox_object(
    matching_node: Node, updated_node: Node, triggering_agent_name: str
):
    """Handle the case that the matching node in the environment tree is a SandboxObject

    Args:
        matching_node (Node): the matching node that contains a SandboxObject
        updated_node (Node): the node that contains the updated values
        triggering_agent_name (str): the name of the agent that triggered this update.
    """
    # Update the values of the matching node sandbox object with those of the updated node
    update_node_name_and_description(matching_node, updated_node)

    matching_node.name.set_action_status(
        updated_node.name.get_action_status(), triggering_agent_name, silent=True
    )


def update_node_in_environment_tree(
    updated_node: Node, environment_tree: Node, triggering_agent_name: str
):
    """Updates a node in an environment tree

    Args:
        updated_node (Node): the node that contains the updated values
        environment_tree (Node): the environment tree where a matching node will be searched, and updated
        triggering_agent_name (str): the name of the agent that triggered this update

    Raises:
        AlgorithmError: if the updated node doesn't have a valid identifier
        AlgorithmError: if the algorithm is unable to find a matching node in the environment tree
        NodeTypeUnhandledError: if the matching node contains neither a Location nor a SandboxObject
    """
    if not isinstance(updated_node, Node):
        raise AlgorithmError(
            f"The function {update_node_in_environment_tree.__name__} received an updated_node that wasn't a node: {updated_node}"
        )

    # Ensure that the updated_node has an identifier, because otherwise we won't be able
    # to locate a matching node
    if updated_node.name.get_identifier() is None:
        raise AlgorithmError(
            f"The function {update_node_in_environment_tree.__name__} received a updated_node without an identifier: {updated_node}"
        )

    # Locate in environment_tree the equivalent node (by the updated_node's identifier)
    matching_node = find_node_by_identifier(
        environment_tree, updated_node.name.get_identifier()
    )

    # If the matching node is None, we have a problem: there should always be a matching identifier
    # in all environment trees of a given simulation.
    if matching_node is None:
        error_message = f"The function {update_node_in_environment_tree.__name__} was unable to retrieve a matching node for the identifier "
        error_message = f"{updated_node.name.get_identifier()}. This should be impossible. Check if there is a problem in the json files for the environments."
        raise AlgorithmError(error_message)

    # Now we know that we have a matching node to updated node.
    # If the matching node contains a Location, then we need to modify the values of that Location,
    # and then modify the values of all the children of that location that are SandboxObjects
    if isinstance(matching_node.name, Location):
        handle_case_matching_node_in_environment_tree_is_location(
            matching_node, updated_node, triggering_agent_name
        )
    elif isinstance(matching_node.name, SandboxObject):
        handle_case_matching_node_in_environment_tree_is_sandbox_object(
            matching_node, updated_node, triggering_agent_name
        )
    else:
        raise NodeTypeUnhandledError(
            f"The function {update_node_in_environment_tree.__name__} couldn't handle node type {matching_node.name}."
        )
