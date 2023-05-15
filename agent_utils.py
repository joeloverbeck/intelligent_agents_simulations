import json
from environment import find_node_by_identifier
from file_utils import ensure_full_file_path_exists
from agent import Agent


def load_agents(simulation_name, environment_tree, observer):
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
        # need to retrieve the current location node, if it isn't set as null
        # in the json data.
        current_location_node = None

        if agents_data[key]["current_location_node"] is not None:
            current_location_node = find_node_by_identifier(
                environment_tree, agents_data[key]["current_location_node"]
            )

        agent = Agent(
            key,
            int(agents_data[key]["age"]),
            current_location_node,
            environment_tree,
        )

        agent.subscribe(observer)

        agents.append(agent)

    return agents
