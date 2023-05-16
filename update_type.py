from enum import Enum


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
