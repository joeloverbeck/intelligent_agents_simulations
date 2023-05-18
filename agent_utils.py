import json
from anytree import Node
from api_requests import request_response_from_human
from environment import find_node_by_identifier, load_environment_tree_from_json
from errors import AlgorithmError, MissingAgentAttributeError
from file_utils import ensure_full_file_path_exists
from agent import Agent
from location import Location
from sandbox_object import SandboxObject
from update_location_in_environment_tree import update_node_in_environment_tree
from vector_storage import create_json_file


def load_agent_attributes_from_raw_data(key, agents_data, simulation_name, observer):
    """Loads into an instance of Agent the proper attribute values from the raw data

    Args:
        key (str): the name of the agent
        agents_data (dict): the raw data of agents loaded from json
        simulation_name (str): the name of the simulation with which this agent is involved
        observer (Object): the instance that wants to subscribe to an agent's updates

    Returns:
        Agent: the agent with all the correct attributes loaded
    """
    # need to retrieve the current location node, if it isn't set as null
    # in the json data.
    current_location_node = None

    # load the individual environment tree from the corresponding file
    agent_environment_tree = load_environment_tree_from_json(
        simulation_name, f"{key.lower()}_environment", observer
    )

    if agents_data[key]["current_location_node"] is not None:
        current_location_node = find_node_by_identifier(
            agent_environment_tree, agents_data[key]["current_location_node"]
        )

    agent = Agent(
        key,
        int(agents_data[key]["age"]),
        current_location_node,
        agent_environment_tree,
    )

    agent.set_planned_action(agents_data[key]["planned_action"], silent=True)

    agent.set_action_status(agents_data[key]["action_status"], silent=True)

    if "observation" not in agents_data[key]:
        raise MissingAgentAttributeError(
            f"Was unable to load the attribute 'observation' from the json file for agent {agent.name}."
        )

    agent.set_observation(agents_data[key]["observation"], silent=True)

    # check the using object entry
    if agents_data[key]["using_object"] is not None:
        using_object = find_node_by_identifier(
            agent_environment_tree, agents_data[key]["using_object"]
        )

        agent.set_using_object(using_object, silent=True)

    # check the destination entry
    if agents_data[key]["destination_node"] is not None:
        destination_node = find_node_by_identifier(
            agent_environment_tree, agents_data[key]["destination_node"]
        )

        agent.set_destination_node(destination_node, silent=True)

    # check whether or not the agent is a player
    if agents_data[key]["is_player"] is not None:
        if agents_data[key]["is_player"].lower() == "true":
            agent.set_is_player(True)
        else:
            agent.set_is_player(False)

    if agent.get_is_player():
        agent.set_request_response_function(request_response_from_human)

    # check the character summary
    if agents_data[key]["character_summary"] is not None:
        agent.set_character_summary(agents_data[key]["character_summary"], silent=True)

    agent.subscribe(observer)

    return agent


def load_agents(simulation_name, observer):
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
            key, agents_data, simulation_name, observer
        )

        agents.append(agent)

    return agents


def is_agent_in_same_location_as_another_agent(
    agent: Agent, second_agent_name: str, agents: list[Agent]
):
    """Checks if an agent is in the same containing location as a different agent

    Args:
        agent (Agent): the first agent whose containing location will be compared
        second_agent_name (str): the second agent whose containing location will be compared
        agents (list[Agent]): all the agents involved in the related simulation

    Raises:
        AlgorithmError: if the second agent's name wasn't found in the passed list of agents

    Returns:
        bool, Agent: returns whether or not the agents are in the same containing location, and if their are,
        the second element of the tuple also contains the data of the second agent in the comparison
    """
    # Create a dictionary for efficient lookup
    agents_dict = {a.name: a for a in agents}

    # Check if the second_agent_name exists in the dictionary
    if second_agent_name not in agents_dict:
        error_message = (
            f"The function {is_agent_in_same_location_as_another_agent.__name__} was unable to find "
            f"the second agent's name ({second_agent_name}) in the list of agents."
        )
        raise AlgorithmError(error_message)

    second_agent = agents_dict[second_agent_name]

    # Find the containing location of both agents involved
    agent_containing_location_identifier = (
        determine_agent_containing_location_identifier(agent)
    )

    second_agent_containing_location_identifier = (
        determine_agent_containing_location_identifier(second_agent)
    )

    is_in_same_location = (
        agent_containing_location_identifier
        == second_agent_containing_location_identifier
    )

    if is_in_same_location:
        return is_in_same_location, second_agent

    return False, None


def determine_agent_containing_location_identifier(agent: Agent):
    """Determines the identifier of the Location that contains the agent

    Args:
        agent (Agent): the agent whose containing location will be determined

    Raises:
        AlgorithmError: if the agent is in a location that is neither a SandboxObject nor a Location

    Returns:
        str: the identifier of the containing location
    """
    if isinstance(agent.get_current_location_node().name, Location):
        return agent.get_current_location_node().name.get_identifier()

    if isinstance(agent.get_current_location_node().name, SandboxObject):
        if agent.get_current_location_node().parent is None:
            error_message = f"The function {determine_agent_containing_location_identifier.__name__} detected that the SandboxObject "
            error_message += f"{agent.get_current_location_node()} didn't have a parent. Are you sure you have set up the environment correctly?"
            raise AlgorithmError(error_message)

        return agent.get_current_location_node().parent.name.get_identifier()

    error_message = f"In the function {determine_agent_containing_location_identifier.__name__}, the agent {agent.name} was currently in a location that was neither "
    error_message += f"a location nor a sandbox object. Current location node: {agent.get_current_location_node()}"
    raise AlgorithmError(error_message)


def update_agent_current_location_node(agent: Agent, environment_tree: Node):
    """Updates an agent's current location node with that of the main environment tree

    Args:
        agent (Agent): the agent whose current location node will be updated
        environment_tree (Node): the environment tree from which the matching node will be picked
    """
    matching_node = find_node_by_identifier(
        environment_tree,
        agent.get_current_location_node().name.get_identifier(),
    )

    update_node_in_environment_tree(
        matching_node, agent.get_environment_tree(), agent.name
    )


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
        agent.get_using_object().name.set_action_status("idle", agent.name)

        agent.set_using_object(None)
