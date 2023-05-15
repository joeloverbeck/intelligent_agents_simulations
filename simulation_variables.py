import datetime
import json
from file_utils import ensure_full_file_path_exists


def load_simulation_variables(simulation_name):
    """Loads the variables of a simulation.
    Note: the corresponding 'variables.json' file should exist.

    Args:
        simulation_name (str): the name of the simulation. Corresponds to existing directory.

    Returns:
        dict: the loaded simulation variables
    """
    full_path = ensure_full_file_path_exists(simulation_name, "variables")

    with open(full_path, "r", encoding="utf8") as file:
        data = json.load(file)

    data["current_timestamp"] = datetime.datetime.fromisoformat(
        data["current_timestamp"]
    )

    data["minutes_advanced_each_step"] = int(data["minutes_advanced_each_step"])

    return data
