import datetime
from action_statuses import produce_action_statuses_for_agent_based_on_destination_node
from actions import (
    create_action,
    request_for_what_length_of_time_the_action_should_take_place,
    request_what_action_to_take_now,
)
from navigation import determine_sandbox_object_destination_from_root
from seed_memories import create_database_of_memories_from_seed_memories
from vector_storage import load_agent_memories
from wrappers import validate_agent_type
from agent import Agent


@validate_agent_type
def set_initial_state_of_agent(
    agent: Agent,
    current_timestamp: datetime.datetime,
    request_character_summary_function,
    produce_action_statuses_for_agent_and_sandbox_object_function,
):
    """Sets the initial state of an agent in a simulation

    Args:
        agent (Agent): the agent for whom the initial state will be set
        current_timestamp (datetime): the current timestamp
        request_character_summary_function (function): the function that will request a character summary
        produce_action_statuses_for_agent_and_sandbox_object_function (function): the action that produces action statuses
    """
    create_database_of_memories_from_seed_memories(agent, current_timestamp)

    # Load the memories to create the character summary of the agent.
    index, memories_raw_data = load_agent_memories(agent)

    # set the character summary of the agent as long as it is None
    if not agent.has_character_summary():
        agent.set_character_summary(
            request_character_summary_function(
                agent, current_timestamp, memories_raw_data, index
            )
        )

    # be always careful to unload index when not using it
    index.unload()

    produce_action_statuses_for_agent_and_sandbox_object_function(
        agent,
        current_timestamp,
        create_action,
        determine_sandbox_object_destination_from_root,
        produce_action_statuses_for_agent_based_on_destination_node,
        request_what_action_to_take_now,
        request_for_what_length_of_time_the_action_should_take_place,
    )
