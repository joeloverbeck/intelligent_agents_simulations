"""This module handles operations related to loading and saving environment trees.
"""
import json

from anytree import Node, find
from errors import AlgorithmError, InvalidParameterError
from file_utils import ensure_full_file_path_exists
from location import Location

from sandbox_object import SandboxObject


def find_node_by_identifier(root_node, identifier):
    """Returns the node in the environment tree that matches the identifier passed

    Args:
        root_node (Node): the root node
        identifier (str): the identifier of the Location or SandboxObject to locate

    Returns:
        Node: the node that contains either a Location or SandboxObject that has the passed identifier
    """
    matching_node = find(root_node, lambda node: node.name.identifier == identifier)

    if matching_node is None:
        error_message = f"The function {find_node_by_identifier.__name__} couldn't find a node by the identifier '{identifier}' in the environment tree."
        error_message += f"\nEnvironment tree:{root_node}"
        raise AlgorithmError(error_message)

    return matching_node


def build_environment_tree(node_data, observer, parent=None):
    """Builds the environment tree from the json data

    Args:
        node_data (dict): the data loaded from a json file
        parent (Node, optional): the parent Node. Defaults to None.

    Returns:
        Node: the root of the environment tree
    """
    instance = None

    if node_data["type"] == "Location":
        # needs to create an instance of the class Location
        instance = Location(
            node_data["identifier"], node_data["name"], node_data["description"]
        )
    elif node_data["type"] == "SandboxObject":
        instance = SandboxObject(
            node_data["identifier"], node_data["name"], node_data["description"]
        )

        # the observer needs to subscribe to the sandbox object's updates
        instance.subscribe(observer)

        instance.set_action_status(node_data["action_status"])

    node = Node(instance, parent=parent)

    for child_data in node_data["children"]:
        build_environment_tree(child_data, observer, parent=node)

    return node


def load_environment_tree_from_json(simulation_name, observer):
    """Loads the environment tree of a simulation from its json file.

    Args:
        simulation_name (str): the name of the simulation (no extension, no directories)

    Raises:
        DirectoryDoesntExistError: if the directory 'simulations' doesn't exist
        DirectoryDoesntExistError: if the directory 'simulations/{name}' doesn't exist
        FileDoesntExistError: if the file 'simulations/{name}/environment.json' doesn't exist

    Returns:
        Node: the root of the environment tree
    """
    full_path = ensure_full_file_path_exists(simulation_name, "environment")

    with open(full_path, "r", encoding="utf8") as file:
        data = json.load(file)

    return build_environment_tree(data, observer)


def serialize_environment_tree(node):
    if not isinstance(node, Node):
        raise InvalidParameterError(
            f"The function {serialize_environment_tree.__name__} expected 'node' to be a Node, but it was: {node}."
        )

    dict_obj = node.name.to_dict()
    dict_obj["children"] = [
        serialize_environment_tree(child) for child in node.children
    ]

    return dict_obj
