"""This module handles operations related to loading and saving environment trees.
"""
import json
import os

from anytree import find, Node
from errors import AlgorithmError, InvalidParameterError
from file_utils import ensure_full_file_path_exists
from location import Location

from sandbox_object import SandboxObject
from string_utils import replace_spaces_with_underscores
from vector_storage import create_json_file


def find_node_by_identifier(root_node: Node, identifier: str):
    """Returns the node in the environment tree that matches the identifier passed

    Args:
        root_node (Node): the root node
        identifier (str): the identifier of the Location or SandboxObject to locate

    Returns:
        Node: the node that contains either a Location or SandboxObject that has the passed identifier
    """
    try:
        matching_node = find(
            root_node, lambda node: node.name.get_identifier() == identifier
        )
    except AttributeError as exception:
        error_message = (
            f"In the function {find_node_by_identifier.__name__}, the code was unable "
        )
        error_message += f"to find a matching node for '{identifier}'. Error: {exception}\nEnvironment tree: {root_node}"
        raise AlgorithmError(error_message) from exception
    except RecursionError as exception:
        error_message = f"In the function '{find_node_by_identifier.__name__}', trying to find a node with the identifier '{identifier}' "
        error_message += f"caused a recursion error given the environment tree: {root_node} | amount of nodes in the tree: ({1 + len(root_node.descendants)})"
        raise AlgorithmError(error_message) from exception

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

        instance.set_action_status(node_data["action_status"], silent=True)

    node = Node(instance, parent=parent)

    for child_data in node_data["children"]:
        build_environment_tree(child_data, observer, parent=node)

    return node


def load_environment_tree_from_json(simulation_name, file_name, observer):
    """Loads the environment tree of a simulation from its json file.

    Args:
        simulation_name (str): the name of the simulation (no extension, no directories)
        file_name (str): the name of the file in the simulation's directory (without the extension)
        observer (Object): an instance that implements the observer pattern

    Raises:
        DirectoryDoesntExistError: if the directory 'simulations' doesn't exist
        DirectoryDoesntExistError: if the directory 'simulations/{name}' doesn't exist
        FileDoesntExistError: if the file 'simulations/{name}/{file_name}.json' doesn't exist

    Returns:
        Node: the root of the environment tree
    """
    # Ensure that the file name has the expected format
    full_path = ensure_full_file_path_exists(simulation_name, replace_spaces_with_underscores(file_name))

    with open(full_path, "r", encoding="utf8") as file:
        data = json.load(file)

    return build_environment_tree(data, observer)


def save_environment_tree_to_json(simulation_name: str, file_name: str, root_node: Node):
    """Saves an entire environment tree to json

    Args:
        simulation_name (str): the name of the simulation
        file_name (str): the name of the json file, without the extension
        root_node (Node): the root node of the environment tree that will saved to a json file
    """
    json_str = serialize_environment_tree(root_node)

    full_path = f"simulations/{simulation_name.lower()}/{replace_spaces_with_underscores(file_name)}.json"

    if os.path.isfile(full_path):
        os.remove(full_path)

    create_json_file(full_path, json_str)


def serialize_environment_tree(node):
    """Serializes the environment tree starting from the passed node

    Args:
        node (Node): the root of the environment tree

    Raises:
        InvalidParameterError: if the node passed isn't a Node

    Returns:
        dict: a serialized version of the environment tree
    """
    if not isinstance(node, Node):
        raise InvalidParameterError(
            f"The function {serialize_environment_tree.__name__} expected 'node' to be a Node, but it was: {node}."
        )

    dict_obj = node.name.to_dict()
    dict_obj["children"] = [
        serialize_environment_tree(child) for child in node.children
    ]

    return dict_obj
