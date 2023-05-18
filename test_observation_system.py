import datetime
from types import NoneType
import unittest
from anytree import Node
from agent import Agent
from location import Location
from observation_system import (
    ObservationSystem,
    ObservationTriggersResultKey,
    RegisteredUpdateDataKey,
)
from registered_update_type import RegisteredUpdateType
from sandbox_object import SandboxObject


class TestUpdateObservationSystem(unittest.TestCase):
    def test_updates_update_timestamp_properly(self):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        self.assertEqual(observation_system.last_update_timestamp, initial_timestamp)

        minutes_advanced_each_step = 30

        observation_system.check_timestamp(
            initial_timestamp, minutes_advanced_each_step
        )

        self.assertEqual(observation_system.last_update_timestamp, initial_timestamp)

        thirty_minutes_later_timestamp = initial_timestamp + datetime.timedelta(
            minutes=minutes_advanced_each_step
        )

        observation_system.check_timestamp(
            thirty_minutes_later_timestamp, minutes_advanced_each_step
        )

        self.assertEqual(observation_system.last_update_timestamp, initial_timestamp)

        hour_later_timestamp = thirty_minutes_later_timestamp + datetime.timedelta(
            minutes=minutes_advanced_each_step
        )

        observation_system.check_timestamp(
            hour_later_timestamp, minutes_advanced_each_step
        )

        self.assertEqual(observation_system.last_update_timestamp, hour_later_timestamp)

    def test_sandbox_object_action_status_change_triggers_properly(self):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("bill", 22, bedroom, house)

        agent_who_provoked_update = Agent("jill", 22, bed, house)

        bed.name.set_action_status(
            "action status", agent_who_provoked_update.name, silent=True
        )

        observation_system.register_update(
            RegisteredUpdateType.SANDBOX_OBJECT_UPDATED,
            {
                RegisteredUpdateDataKey.IDENTIFIER: bed.name.get_identifier(),
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_SANDBOX_OBJECT_IDENTIFIER
            )
        )
        self.assertEqual(
            observation_triggers_result[
                ObservationTriggersResultKey.UPDATE_SANDBOX_OBJECT_IDENTIFIER
            ],
            "bed",
        )
        self.assertEqual(
            observation_triggers_result[
                ObservationTriggersResultKey.UPDATE_SANDBOX_OBJECT_ACTION_STATUS
            ],
            "action status",
        )

    def test_sandbox_object_action_status_change_doesnt_trigger_if_it_doesnt_need_to(
        self,
    ):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("bill", 22, house, house)

        agent_who_provoked_update = Agent("jill", 22, bed, house)

        bed.name.set_action_status(
            "action status", agent_who_provoked_update.name, silent=True
        )

        observation_system.register_update(
            RegisteredUpdateType.SANDBOX_OBJECT_UPDATED,
            {
                RegisteredUpdateDataKey.IDENTIFIER: bed.name.get_identifier(),
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertFalse(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_SANDBOX_OBJECT_IDENTIFIER
            )
        )
        self.assertFalse(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_SANDBOX_OBJECT_ACTION_STATUS
            )
        )

    def test_agent_moved_into_location_triggers_properly(self):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("bill", 22, house, house)

        agent_who_provoked_update = Agent("jill", 22, house, house)

        agent_who_provoked_update.set_action_status("moving to bedroom", silent=True)

        observation_system.register_update(
            RegisteredUpdateType.AGENT_MOVED_TO_LOCATION,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            )
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            ),
            "moving to bedroom",
        )

    def test_agent_moved_into_location_triggers_properly_if_main_agent_is_using_object_at_containing_location(
        self,
    ):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        drawer = Node(SandboxObject("drawer", "drawer", "drawer"), parent=bedroom)

        agent = Agent("bill", 22, drawer, house)

        agent_who_provoked_update = Agent("jill", 22, house, house)

        agent_who_provoked_update.set_action_status("moving to bedroom", silent=True)

        observation_system.register_update(
            RegisteredUpdateType.AGENT_MOVED_TO_LOCATION,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            )
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            ),
            "moving to bedroom",
        )

    def test_agent_moved_into_location_doesnt_trigger_if_it_shouldnt(self):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("bill", 22, bedroom, house)

        agent_who_provoked_update = Agent("jill", 22, house, house)

        agent_who_provoked_update.set_action_status("moving to bedroom", silent=True)

        observation_system.register_update(
            RegisteredUpdateType.AGENT_MOVED_TO_LOCATION,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertFalse(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            )
        )
        self.assertFalse(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            )
        )

    def test_agent_using_object_triggers_observation_when_it_should(self):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("bill", 22, bedroom, house)

        agent_who_provoked_update = Agent("jill", 22, bed, house)

        agent_who_provoked_update.set_action_status("using bed", silent=True)

        observation_system.register_update(
            RegisteredUpdateType.AGENT_USING_OBJECT,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
                RegisteredUpdateDataKey.IDENTIFIER: bed.name.get_identifier(),
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            )
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            ),
            "jill",
        )
        self.assertEqual(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            ),
            "using bed",
        )

    def test_agent_using_object_triggers_observation_when_main_object_is_in_another_object_in_same_location(
        self,
    ):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        drawer = Node(SandboxObject("drawer", "drawer", "drawer"), parent=bedroom)

        agent = Agent("bill", 22, drawer, house)

        agent_who_provoked_update = Agent("jill", 22, bed, house)

        agent_who_provoked_update.set_action_status("using bed", silent=True)

        observation_system.register_update(
            RegisteredUpdateType.AGENT_USING_OBJECT,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
                RegisteredUpdateDataKey.IDENTIFIER: bed.name.get_identifier(),
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            )
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            ),
            "jill",
        )
        self.assertEqual(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            ),
            "using bed",
        )

    def test_agent_using_object_doesnt_trigger_observation_if_it_shouldnt(self):
        initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        observation_system = ObservationSystem(initial_timestamp)

        house = Node(Location("house", "house", "house"))
        bedroom = Node(Location("bedroom", "bedroom", "bedroom"), parent=house)
        bed = Node(SandboxObject("bed", "bed", "bed"), parent=bedroom)

        agent = Agent("bill", 22, house, house)

        agent_who_provoked_update = Agent("jill", 22, bed, house)

        agent_who_provoked_update.set_action_status("using bed", silent=True)

        observation_system.register_update(
            RegisteredUpdateType.AGENT_USING_OBJECT,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
                RegisteredUpdateDataKey.IDENTIFIER: bed.name.get_identifier(),
            },
        )

        observation_triggers_result = (
            observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertFalse(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_NAME
            )
        )
        self.assertFalse(
            observation_triggers_result.get(
                ObservationTriggersResultKey.UPDATE_AGENT_ACTION_STATUS
            )
        )


if __name__ == "__main__":
    unittest.main()
