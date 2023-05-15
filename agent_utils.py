

import json
from file_utils import ensure_full_file_path_exists
from agent import Agent


def load_agents(simulation_name):
    """Loads the agents of a simulation

    Args:
        simulation_name (str): the name of the simulation

    Returns:
        list: all the agents loaded from the simulation json file
    """
    full_path = ensure_full_file_path_exists(simulation_name, "agents")

    with open(full_path, "r", encoding="utf8") as file:
        agents_data = json.load(file)

    agents = []

    for key in agents_data.keys():
        agents.append(Agent(key, int(agents_data[key]["age"]), None, None))

    return agents
