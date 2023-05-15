"""This module handles operations related to loading environment trees from json.
"""
import json

from anytree import Node
from file_utils import ensure_full_file_path_exists
from location import Location

from sandbox_object import SandboxObject


def build_environment_tree(node_data, parent=None):
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
        instance = Location(node_data["name"], node_data["description"])
    elif node_data["type"] == "SandboxObject":
        instance = SandboxObject(node_data["name"], node_data["description"])
        instance.set_action_status(node_data["action_status"])

    node = Node(instance, parent=parent)

    for child_data in node_data["children"]:
        build_environment_tree(child_data, parent=node)

    return node


def load_environment_tree_from_json(simulation_name):
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

    return build_environment_tree(data)
