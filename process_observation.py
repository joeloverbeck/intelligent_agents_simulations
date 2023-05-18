import datetime
from agent import Agent
from enums import ProcessObservationParametersKey

from regular_expression_utils import does_text_contain_yes
from wrappers import validate_agent_has_character_summary, validate_agent_type


@validate_agent_type
@validate_agent_has_character_summary
def delegate_determining_appropriate_reaction_to_observation(
    agent: Agent,
    current_timestamp: datetime.datetime,
    load_agent_memories_function,
    update_memories_database_function,
    request_appropriate_reaction_for_observation_function,
):
    """Delegates determining the appropriate reaction to an observation

    Args:
        agent (Agent): the agent who received the observation
        current_timestamp (datetime.datetime): the current timestamp
        load_agent_memories_function (function): the function that loads an agent's memories
        update_memories_database_function (function): the function that updates the memories of an agent
        request_appropriate_reaction_for_observation_function (function): the function that requests an appropriate reaction for the observation
    """
    appropriate_reaction_for_observation = (
        request_appropriate_reaction_for_observation_function
    )

    # We store as a memory of the agent the AI's response about the appropriate reaction.
    index, _ = load_agent_memories_function(agent)

    update_memories_database_function(
        agent,
        current_timestamp,
        [appropriate_reaction_for_observation],
        index,
    )

    index.unload()


def process_observation(process_observation_parameters: dict):
    """Process an observation from the environment for an agent

    Args:
        process_observation_parameters (dict): the parameters of the function
    """
    # We set the observation as the agent's current observation, if necessary
    agent = process_observation_parameters[ProcessObservationParametersKey.AGENT]
    observation = process_observation_parameters[
        ProcessObservationParametersKey.OBSERVATION
    ]
    current_timestamp = process_observation_parameters[
        ProcessObservationParametersKey.CURRENT_TIMESTAMP
    ]
    load_agent_memories_function = process_observation_parameters[
        ProcessObservationParametersKey.LOAD_AGENT_MEMORIES_FUNCTION
    ]
    update_memories_database_function = process_observation_parameters[
        ProcessObservationParametersKey.UPDATE_MEMORIES_DATABASE_FUNCTION
    ]
    request_if_should_stop_action_function = process_observation_parameters[
        ProcessObservationParametersKey.REQUEST_IF_SHOULD_STOP_ACTION_FUNCTION
    ]
    request_appropriate_reaction_for_observation_function = process_observation_parameters[
        ProcessObservationParametersKey.REQUEST_APPROPRIATE_REACTION_FOR_OBSERVATION_FUNCTION
    ]
    observation_data = process_observation_parameters[
        ProcessObservationParametersKey.OBSERVATION_DATA
    ]

    if agent.get_observation() != observation:
        agent.set_observation(observation)

    # Save the observation to the agent's memories
    index, _ = load_agent_memories_function(agent)

    update_memories_database_function(
        agent,
        current_timestamp,
        [observation],
        index,
    )

    index.unload()

    # Request from the AI model if this observation should cause the agent
    # to stop his or her current action
    should_stop_action_response = request_if_should_stop_action_function(
        agent, observation_data
    )

    # Only in case that the AI model decided that the observation was enough
    # for the agent to stop his or her current action, then we ask
    # the model about what should be the appropriate reaction to that observation.
    if does_text_contain_yes(should_stop_action_response):
        delegate_determining_appropriate_reaction_to_observation(
            agent,
            current_timestamp,
            load_agent_memories_function,
            update_memories_database_function,
            request_appropriate_reaction_for_observation_function,
        )
