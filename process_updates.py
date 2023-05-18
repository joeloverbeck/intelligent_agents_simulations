from anytree import Node
from agent_utils import save_agents_to_json, substitute_agent
from enums import ObservationType, RegisteredUpdateDataKey, UpdateMessageKey, UpdateType
from environment import save_environment_tree_to_json
from errors import AlgorithmError
from logging_messages import log_simulation_message
from sandbox_object import SandboxObject
from simulation_utils import save_agent_changes
from update_location_in_environment_tree import update_node_in_environment_tree


def handle_case_sandbox_object_changed_action_status(simulation, update_message: dict):
    """Handles the case that a sandbox object changed action status

    Args:
        simulation (Simulation): the simulation involved
        update_message (dict): the data of the update message

    Raises:
        AlgorithmError: if the object received in the update wasn't a SandboxObject
    """
    if not isinstance(update_message[UpdateMessageKey.SANDBOX_OBJECT], SandboxObject):
        error_message = f"The function {handle_case_sandbox_object_changed_action_status} received a supposed sandbox object that wasn't one: "
        error_message += f"{update_message[UpdateMessageKey.SANDBOX_OBJECT]}"
        raise AlgorithmError(error_message)

    message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.SANDBOX_OBJECT].name} "
    message += f"changed action status to: {update_message[UpdateMessageKey.SANDBOX_OBJECT].get_action_status()}"
    log_simulation_message(simulation.name, message)

    # Set the update in the dict
    simulation.register_update(
        ObservationType.SANDBOX_OBJECT_CHANGED_ACTION_STATUS,
        {
            RegisteredUpdateDataKey.IDENTIFIER: update_message[
                UpdateMessageKey.SANDBOX_OBJECT
            ].get_identifier(),
            RegisteredUpdateDataKey.UPDATE_AGENT_NAME: update_message[
                UpdateMessageKey.OBSERVED_AGENT_NAME
            ],
        },
    )

    # Update the data of the corresponding sandbox object in the main environment tree
    update_node_in_environment_tree(
        Node(update_message[UpdateMessageKey.SANDBOX_OBJECT]),
        simulation.get_environment_tree(),
        update_message[UpdateMessageKey.OBSERVED_AGENT_NAME],
    )

    save_environment_tree_to_json(
        simulation.name, "environment", simulation.get_environment_tree()
    )


def handle_case_agent_changed_current_location_node(simulation, update_message: dict):
    """Handles the case that an agent changed his or her current location node

    Args:
        simulation (Simulation): the simulation involved
        update_message (dict): the data of the update message
    """
    message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} changed "
    message += f"the current location node to: {update_message[UpdateMessageKey.AGENT].get_current_location_node()}"
    log_simulation_message(simulation.name, message)

    # Set the update in the dict
    simulation.register_update(
        ObservationType.AGENT_MOVED_TO_LOCATION,
        {RegisteredUpdateDataKey.UPDATE_AGENT_NAME: update_message["agent"].name},
    )

    save_agent_changes(update_message["agent"], simulation)


def handle_case_agent_changed_action_status(simulation, update_message: dict):
    """Handles the case that an agent changed action status

    Args:
        simulation (Simulation): the simulation involved
        update_message (dict): the data of the update message
    """
    message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} changed the action status to: "
    message += f"{update_message[UpdateMessageKey.AGENT].get_action_status()}"
    log_simulation_message(simulation.name, message)

    save_agent_changes(update_message["agent"], simulation)


def handle_case_agent_changed_character_summary(simulation, update_message: dict):
    """Handles the case that an agent changed the character summary

    Args:
        simulation (Simulation): the simulation involved
        update_message (dict): the data of the update message
    """
    message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} changed the character "
    message += (
        f"summary to: {update_message[UpdateMessageKey.AGENT].get_character_summary()}"
    )
    log_simulation_message(simulation.name, message)


def handle_case_agent_changed_using_object(simulation, update_message: dict):
    """Handles the case that an agent changed using object

    Args:
        simulation (Simulation): the simulation involved
        update_message (dict): the data of the update message
    """
    message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} changed using object to: "
    message += f"{update_message[UpdateMessageKey.AGENT].get_using_object()}"
    log_simulation_message(simulation.name, message)

    simulation.register_update(
        ObservationType.AGENT_USING_OBJECT,
        {RegisteredUpdateDataKey.UPDATE_AGENT_NAME: update_message["agent"].name},
    )

    save_agent_changes(update_message["agent"], simulation)


def handle_case_agent_changed_observation(simulation, update_message: dict):
    """Handles the case in which an agent changed his or her set observation

    Args:
        simulation (Simulation): the simulation involved with this update
        update_message (dict): the data associated to the update message
    """
    message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} changed the observation to: "
    message += f"{update_message[UpdateMessageKey.AGENT].get_observation()}"
    log_simulation_message(simulation.name, message)

    save_agent_changes(update_message["agent"], simulation)


def process_updates(simulation, update_message: dict):
    """Process updates from a subscription

    Args:
        simulation (Simulation): the simulation that has subscribed to the updates
        update_message (dict): the data associated with the update
    """
    if (
        update_message[UpdateMessageKey.TYPE]
        == UpdateType.SANDBOX_OBJECT_CHANGED_ACTION_STATUS
    ):
        handle_case_sandbox_object_changed_action_status(simulation, update_message)
    elif (
        update_message[UpdateMessageKey.TYPE]
        == UpdateType.AGENT_CHANGED_CURRENT_LOCATION_NODE
    ):
        handle_case_agent_changed_current_location_node(simulation, update_message)
    elif (
        update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_CHANGED_ACTION_STATUS
    ):
        handle_case_agent_changed_action_status(simulation, update_message)
    elif (
        update_message[UpdateMessageKey.TYPE]
        == UpdateType.AGENT_CHANGED_CHARACTER_SUMMARY
    ):
        handle_case_agent_changed_character_summary(simulation, update_message)
    elif update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_CHANGED_USING_OBJECT:
        handle_case_agent_changed_using_object(simulation, update_message)
    elif (
        update_message[UpdateMessageKey.TYPE]
        == UpdateType.AGENT_CHANGED_DESTINATION_NODE
    ):
        message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} changed destination node to: "
        message += f"{update_message[UpdateMessageKey.AGENT].get_destination_node()}"
        log_simulation_message(simulation.name, message)

        substitute_agent(simulation.get_agents(), update_message["agent"])
        save_agents_to_json(simulation.name, simulation.get_agents())
    elif update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_REACHED_DESTINATION:
        message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} reached the destination: "
        message += f"{update_message['destination_node'].name}"
        log_simulation_message(simulation.name, message)
    elif update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_PRODUCED_ACTION:
        message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} produced action: {update_message[UpdateMessageKey.ACTION]}"
        log_simulation_message(simulation.name, message)
    elif update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_NEEDS_TO_MOVE:
        message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} needs to move to: "
        message += f"{update_message[UpdateMessageKey.AGENT].get_destination_node()}"
        log_simulation_message(simulation.name, message)
    elif (
        update_message[UpdateMessageKey.TYPE]
        == UpdateType.AGENT_WILL_USE_SANDBOX_OBJECT
    ):
        message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} will use sandbox object: "
        message += (
            f"{update_message[UpdateMessageKey.AGENT].get_current_location_node()}"
        )
        log_simulation_message(simulation.name, message)
    elif (
        update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_CHANGED_PLANNED_ACTION
    ):
        message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} changed planned action: "
        message += f"{update_message[UpdateMessageKey.AGENT].get_planned_action()}"
        log_simulation_message(simulation.name, message)

        substitute_agent(simulation.get_agents(), update_message["agent"])
        save_agents_to_json(simulation.name, simulation.get_agents())
    elif (
        update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_CONTINUES_USING_OBJECT
    ):
        message = f"{simulation.current_timestamp.isoformat()} {update_message[UpdateMessageKey.AGENT].name} continues using object: "
        message += f"{update_message[UpdateMessageKey.AGENT].get_using_object()}"
        log_simulation_message(simulation.name, message)
    elif update_message[UpdateMessageKey.TYPE] == UpdateType.AGENT_CHANGED_OBSERVATION:
        handle_case_agent_changed_observation(simulation, update_message)
