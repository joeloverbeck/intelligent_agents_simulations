"""This module contains all the custom Enums used throughout the library
"""
from enum import Enum


class UpdateMessageKey(Enum):
    TYPE = 1
    SANDBOX_OBJECT = 2
    AGENT = 3
    OBSERVED_AGENT_NAME = 4
    ACTION = 5


class ProcessObservationParametersKey(Enum):
    """The keys to the dict of parameters for the process_observation function

    Args:
        Enum (Enum): the base Enum class
    """

    AGENT = 1
    OBSERVATION = 2
    CURRENT_TIMESTAMP = 3
    LOAD_AGENT_MEMORIES_FUNCTION = 4
    UPDATE_MEMORIES_DATABASE_FUNCTION = 5
    REQUEST_IF_SHOULD_STOP_ACTION_FUNCTION = 6
    REQUEST_APPROPRIATE_REACTION_FOR_OBSERVATION_FUNCTION = 7
    OBSERVATION_DATA = 8


class ObservationType(Enum):
    """The type of observation

    Args:
        Enum (Enum): the base Enum class
    """

    SANDBOX_OBJECT_CHANGED_ACTION_STATUS = 1
    AGENT_MOVED_TO_LOCATION = 2
    AGENT_USING_OBJECT = 3


class ObservationDataKey(Enum):
    """The keys of the observation data dict

    Args:
        Enum (Enum): the base Enum class
    """

    TYPE = 1
    OBSERVED_AGENT_NAME = 2
    OBSERVED_AGENT_ACTION_STATUS = 3
    OBSERVED_SANDBOX_OBJECT_IDENTIFIER = 4


class RegisteredUpdateDataKey(Enum):
    """Identifies the key names of the dict that contains the registered update data"""

    IDENTIFIER = 1
    UPDATE_AGENT_NAME = 2


class UpdateType(Enum):
    """Identifies the update types that are sent to observers"""

    SANDBOX_OBJECT_CHANGED_ACTION_STATUS = 1
    AGENT_CHANGED_CURRENT_LOCATION_NODE = 2
    AGENT_CHANGED_ACTION_STATUS = 3
    AGENT_CHANGED_CHARACTER_SUMMARY = 4
    AGENT_CHANGED_USING_OBJECT = 5
    AGENT_CHANGED_DESTINATION_NODE = 6
    AGENT_REACHED_DESTINATION = 7
    AGENT_PRODUCED_ACTION = 8
    AGENT_NEEDS_TO_MOVE = 9
    AGENT_WILL_USE_SANDBOX_OBJECT = 10
    AGENT_CHANGED_PLANNED_ACTION = 11
    AGENT_CONTINUES_USING_OBJECT = 12
    AGENT_CHANGED_OBSERVATION = 13
