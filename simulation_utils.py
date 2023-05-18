from agent import Agent
from agent_utils import save_agents_to_json, substitute_agent


def save_agent_changes(agent_to_save: Agent, simulation):
    substitute_agent(simulation.get_agents(), agent_to_save)
    save_agents_to_json(simulation.name, simulation.get_agents())
