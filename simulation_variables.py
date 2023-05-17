import datetime
import json
from file_utils import ensure_full_file_path_exists
from vector_storage import create_json_file


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


def save_current_timestamp(simulation_name: str, current_timestamp: datetime):
    """Saves the current timestamp of a simulation to the corresponding 'variables.json' file

    Args:
        simulation_name (str): the name of the simulation
        current_timestamp (datetime): the current timestamp
    """
    # first load the current simulation variables from file.
    simulation_variables_raw_data = load_simulation_variables(simulation_name)

    simulation_variables_raw_data["current_timestamp"] = current_timestamp.isoformat()

    create_json_file(
        f"simulations/{simulation_name.lower()}/variables.json",
        simulation_variables_raw_data,
    )
