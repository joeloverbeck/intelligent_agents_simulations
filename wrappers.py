from agent import Agent
from errors import InvalidParameterError, MissingCharacterSummaryError
from anytree import Node


def validate_agent_type(func):
    def wrapper(agent, *args, **kwargs):
        if agent is None:
            raise InvalidParameterError(
                f"The function {func.__name__} received a None agent."
            )
        if not isinstance(agent, Agent):
            raise InvalidParameterError(
                f"The function {func.__name__} should have received an agent of type Agent, but it was: {agent}"
            )
        return func(agent, *args, **kwargs)

    return wrapper


def validate_agent_has_character_summary(func):
    def wrapper(agent, *args, **kwargs):
        if not agent.has_character_summary():
            raise MissingCharacterSummaryError(
                f"The function {func.__name__} required the agent {agent.name} to have the character summary set."
            )
        return func(agent, *args, **kwargs)

    return wrapper
