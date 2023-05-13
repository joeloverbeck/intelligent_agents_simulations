from agent import Agent
from errors import InvalidParameterError


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
