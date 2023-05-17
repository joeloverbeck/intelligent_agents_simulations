from anytree import Node
from environment import find_node_by_identifier
from environment_tree_integrity import calculate_number_of_nodes_in_tree

from errors import AlgorithmError, InvalidParameterError
from location import Location
from sandbox_object import SandboxObject


def crash_if_substitute_node_failed_to_maintain_integrity_of_environment_tree(
    initial_number_of_nodes_in_tree, final_number_of_nodes_in_tree, environment_tree
):
    """Crashes if the substitution failed to maintain the integrity of the environment tree

    Args:
        initial_number_of_nodes_in_tree (int): the initial number of nodes in the environment tree
        final_number_of_nodes_in_tree (int): the final number of nodes in the environment tree
        environment_tree (Node): the root node of the environment tree

    Raises:
        AlgorithmError: if the integrity of the environment tree wasn't maintained
    """
    if initial_number_of_nodes_in_tree != final_number_of_nodes_in_tree:
        error_message = f"The function {substitute_node.__name__} failed to maintain the integrity of the environment tree. Initial size: {initial_number_of_nodes_in_tree}"
        error_message += f" | Final size: {final_number_of_nodes_in_tree}. Resulting environment: {environment_tree}"

        raise AlgorithmError(error_message)


def sanity_checks_for_substitute_node(environment_tree: Node, new_object):
    """Checks basic contracts for the parameters to the function 'substitute_node'

    Args:
        environment_tree (Node): the root node of the environment tree
        new_object (Location or SandboxObject): the object that will be wrapped in a node and inserted into the environment tree

    Raises:
        InvalidParameterError: if 'environment_tree' was None
        InvalidParameterError: if 'new_object' was None
        InvalidParameterError: if 'new_object' was neither Location nor a SandboxObject
    """
    if environment_tree is None:
        raise InvalidParameterError(
            f"The function {substitute_node.__name__} received a None environment tree."
        )
    if new_object is None:
        raise InvalidParameterError(
            f"The function {substitute_node.__name__} expected the 'new_object' not to be None."
        )
    if not isinstance(new_object, Location) and not isinstance(
        new_object, SandboxObject
    ):
        raise InvalidParameterError(
            f"The function {substitute_node.__name__} expected the 'new_object' to be either a Location or a SandboxObject. It was: {new_object}"
        )


def insert_new_node_in_environment_tree(
    matching_node: Node, new_object, environment_tree
):
    """Inserts the new node in the environment tree, taking children and parent as necessary

    Args:
        matching_node (Node): the matching node that will be substituted
        new_object (Location or SandboxObject): the content that will be wrapped in a node and inserted into the environment tree

    Returns:
        Node: either the original root of the environment tree or a new root
    """
    new_node = Node(new_object)

    for child in list(matching_node.children):
        child.parent = new_node

    if matching_node.parent is not None:
        new_node.parent = matching_node.parent

        # ensure that the parent now considers the new_node as its child
        if new_node not in new_node.parent.children:
            raise AlgorithmError(
                f"The function {insert_new_node_in_environment_tree.__name__} failed to make the new parent of 'new_node' consider the new node its child."
            )
    else:  # handle case where matching_node is the root
        environment_tree = new_node

    matching_node.parent = None

    # Clear or update the matching_node's identifier, or explicitly delete the node if possible
    del matching_node

    return environment_tree  # return the potentially new root


def substitute_node(environment_tree: Node, new_object):
    """Substitutes a node in an environment tree by inserting a node wrapped in 'new_object'

    Args:
        environment_tree (Node): the environment tree in which the new object will be inserted
        new_object (Location or SandboxObject): the new object that will be inserted. Either a Location or a SandboxObject

    Raises:
        AlgorithmError: if the integrity of the environment tree couldn't be maintained.

    Returns:
        Node: the root node of the new environment tree
    """
    sanity_checks_for_substitute_node(environment_tree, new_object)

    initial_number_of_nodes_in_tree = calculate_number_of_nodes_in_tree(
        environment_tree
    )

    matching_node = find_node_by_identifier(
        environment_tree, new_object.get_identifier()
    )

    if matching_node is None:
        raise AlgorithmError(
            f"Was unable to find a matching node in {substitute_node.__name__}. This should be impossible."
        )

    environment_tree = insert_new_node_in_environment_tree(
        matching_node, new_object, environment_tree
    )

    final_number_of_nodes_in_tree = calculate_number_of_nodes_in_tree(environment_tree)

    crash_if_substitute_node_failed_to_maintain_integrity_of_environment_tree(
        initial_number_of_nodes_in_tree, final_number_of_nodes_in_tree, environment_tree
    )

    return environment_tree  # return the potentially new root
