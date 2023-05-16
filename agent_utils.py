import json
from environment import find_node_by_identifier
from errors import AlgorithmError
from file_utils import ensure_full_file_path_exists
from agent import Agent
from vector_storage import create_json_file


def load_agent_attributes_from_raw_data(key, agents_data, environment_tree, observer):
    """Loads into an instante of Agent the proper attribute values from the raw data

    Args:
        key (str): the name of the agent
        agents_data (dict): the raw data of agents loaded from json
        environment_tree (Node): the root node of the environment tree
        observer (Object): the instance that wants to subscribe to an agent's updates

    Returns:
        Agent: the agent with all the correct attributes loaded
    """
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

    agent.set_planned_action(agents_data[key]["planned_action"], silent=True)

    agent.set_action_status(agents_data[key]["action_status"], silent=True)

    # check the using object node
    if agents_data[key]["using_object"] is not None:
        using_object = find_node_by_identifier(
            environment_tree, agents_data[key]["using_object"]
        )

        agent.set_using_object(using_object, silent=True)

    # check the destination node
    if agents_data[key]["destination_node"] is not None:
        destination_node = find_node_by_identifier(
            environment_tree, agents_data[key]["destination_node"]
        )

        agent.set_destination_node(destination_node, silent=True)

    agent.subscribe(observer)

    return agent


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
        agent = load_agent_attributes_from_raw_data(
            key, agents_data, environment_tree, observer
        )

        agents.append(agent)

    return agents


def substitute_agent(agents, agent):
    """Substitutes a specific agent in a list of agents with an updated version

    Args:
        agents (list): the list of agents that contain the one that will be substituted
        agent (Agent): the updated agent

    Raises:
        AlgorithmError: if a matching agent can't be found
    """
    # Now we must substitute the corresponding agent entry in the agents list of the simulation
    try:
        index = agents.index(agent)
    except ValueError as exception:
        error_message = f"The function {substitute_agent.__name__} was unable to find the index of agent {agent} "
        error_message += f"in the list of agents: {agents}. Exception: {exception}"

        raise AlgorithmError(error_message) from exception

    agents[index] = agent


def save_agents_to_json(simulation_name: str, agents: list):
    """Saves a list of agents to json

    Args:
        simulation_name (str): the name of the simulation
        agents (list): the list of agents that will be saved to a json file
    """
    # Save the agents to the agents json file
    agents_data = {}

    for agent in agents:
        agents_data.update({agent.name: agent.to_dict()})

    create_json_file(f"simulations/{simulation_name.lower()}/agents.json", agents_data)


def wipe_previous_action_attribute_values_from_agent(agent: Agent):
    """Wipes the attribute values in the agent relevant to an action being performed

    Args:
        agent (Agent): the agent whose attribute values will be wiped
    """
    if agent.get_planned_action() is not None:
        agent.set_planned_action(None)
    if agent.get_action_status() is not None:
        agent.set_action_status(None)
    if agent.get_destination_node() is not None:
        agent.set_destination_node(None)
    if agent.get_using_object() is not None:        
        # the action status of the corresponding used object should be defaulted
        agent.get_using_object().name.set_action_status("idle")

        agent.set_using_object(None)
