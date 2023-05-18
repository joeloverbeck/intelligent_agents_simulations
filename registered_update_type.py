from enum import Enum


class RegisteredUpdateType(Enum):
    """Identifies the update types to register in the simulation to trigger observations"""

    SANDBOX_OBJECT_UPDATED = 1
    AGENT_MOVED_TO_LOCATION = 2
    AGENT_USING_OBJECT = 3
