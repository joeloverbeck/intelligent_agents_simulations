import datetime
from types import NoneType
import unittest
from anytree import Node
from agent import Agent
from enums import ObservationDataKey, ObservationType, RegisteredUpdateDataKey
from environment import find_node_by_identifier
from location import Location
from observation_system import (
    ObservationSystem,
)
from sandbox_object import SandboxObject


class TestUpdateObservationSystem(unittest.TestCase):
    def setUp(self):
        self.initial_timestamp = datetime.datetime(2023, 5, 11, 10, 30, 45)

        self.observation_system = ObservationSystem(self.initial_timestamp)

        self.house = Node(Location("house", "house", "house"))
        self.bedroom = Node(
            Location("bedroom", "bedroom", "bedroom"), parent=self.house
        )
        self.bed = Node(SandboxObject("bed", "bed", "bed"), parent=self.bedroom)

        self.drawer = Node(
            SandboxObject("drawer", "drawer", "drawer"), parent=self.bedroom
        )

    def test_updates_update_timestamp_properly(self):
        self.assertEqual(
            self.observation_system.last_update_timestamp, self.initial_timestamp
        )

        minutes_advanced_each_step = 30

        self.observation_system.check_timestamp(
            self.initial_timestamp, minutes_advanced_each_step
        )

        self.assertEqual(
            self.observation_system.last_update_timestamp, self.initial_timestamp
        )

        thirty_minutes_later_timestamp = self.initial_timestamp + datetime.timedelta(
            minutes=minutes_advanced_each_step
        )

        self.observation_system.check_timestamp(
            thirty_minutes_later_timestamp, minutes_advanced_each_step
        )

        self.assertEqual(
            self.observation_system.last_update_timestamp, self.initial_timestamp
        )

        hour_later_timestamp = thirty_minutes_later_timestamp + datetime.timedelta(
            minutes=minutes_advanced_each_step
        )

        self.observation_system.check_timestamp(
            hour_later_timestamp, minutes_advanced_each_step
        )

        self.assertEqual(
            self.observation_system.last_update_timestamp, hour_later_timestamp
        )

    def test_sandbox_object_action_status_change_triggers_properly(self):
        agent = Agent("bill", 22, self.bedroom, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.bed, self.house)

        self.bed.name.set_action_status(
            "action status", agent_who_provoked_update.name, silent=True
        )

        self.observation_system.register_update(
            ObservationType.SANDBOX_OBJECT_CHANGED_ACTION_STATUS,
            {
                RegisteredUpdateDataKey.IDENTIFIER: self.bed.name.get_identifier(),
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_SANDBOX_OBJECT_IDENTIFIER
            )
        )
        self.assertEqual(
            observation_triggers_result[
                ObservationDataKey.OBSERVED_SANDBOX_OBJECT_IDENTIFIER
            ],
            "bed",
        )

        matching_node = find_node_by_identifier(
            agent.get_environment_tree(),
            observation_triggers_result[
                ObservationDataKey.OBSERVED_SANDBOX_OBJECT_IDENTIFIER
            ],
        )

        self.assertEqual(
            matching_node.name.get_action_status(),
            "action status",
        )

    def test_sandbox_object_action_status_change_doesnt_trigger_if_it_doesnt_need_to(
        self,
    ):
        agent = Agent("bill", 22, self.house, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.bed, self.house)

        self.bed.name.set_action_status(
            "action status", agent_who_provoked_update.name, silent=True
        )

        self.observation_system.register_update(
            ObservationType.SANDBOX_OBJECT_CHANGED_ACTION_STATUS,
            {
                RegisteredUpdateDataKey.IDENTIFIER: self.bed.name.get_identifier(),
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertFalse(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_SANDBOX_OBJECT_IDENTIFIER
            )
        )

    def test_agent_moved_into_location_triggers_properly(self):
        agent = Agent("bill", 22, self.house, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.house, self.house)

        agent_who_provoked_update.set_action_status("moving to bedroom", silent=True)

        self.observation_system.register_update(
            ObservationType.AGENT_MOVED_TO_LOCATION,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME)
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            ),
            "moving to bedroom",
        )

    def test_agent_moved_into_location_triggers_properly_if_main_agent_is_using_object_at_containing_location(
        self,
    ):
        agent = Agent("bill", 22, self.drawer, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.bedroom, self.house)

        agent_who_provoked_update.set_action_status("moving to bedroom", silent=True)

        self.observation_system.register_update(
            ObservationType.AGENT_MOVED_TO_LOCATION,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME)
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            ),
            "moving to bedroom",
        )

    def test_agent_moved_into_location_doesnt_trigger_if_it_shouldnt(self):
        agent = Agent("bill", 22, self.bedroom, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.house, self.house)

        agent_who_provoked_update.set_action_status("moving to bedroom", silent=True)

        self.observation_system.register_update(
            ObservationType.AGENT_MOVED_TO_LOCATION,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertFalse(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME)
        )
        self.assertFalse(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            )
        )

    def test_agent_using_object_triggers_observation_when_it_should(self):
        agent = Agent("bill", 22, self.bedroom, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.bed, self.house)

        agent_who_provoked_update.set_action_status("using bed", silent=True)

        self.observation_system.register_update(
            ObservationType.AGENT_USING_OBJECT,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
                RegisteredUpdateDataKey.IDENTIFIER: self.bed.name.get_identifier(),
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME)
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME),
            "jill",
        )
        self.assertEqual(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            ),
            "using bed",
        )

    def test_agent_using_object_triggers_observation_when_main_object_is_in_another_object_in_same_location(
        self,
    ):
        agent = Agent("bill", 22, self.drawer, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.bed, self.house)

        agent_who_provoked_update.set_action_status("using bed", silent=True)

        self.observation_system.register_update(
            ObservationType.AGENT_USING_OBJECT,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
                RegisteredUpdateDataKey.IDENTIFIER: self.bed.name.get_identifier(),
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertTrue(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME)
        )
        self.assertTrue(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            )
        )

        self.assertEqual(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME),
            "jill",
        )
        self.assertEqual(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            ),
            "using bed",
        )

    def test_agent_using_object_doesnt_trigger_observation_if_it_shouldnt(self):
        agent = Agent("bill", 22, self.house, self.house)

        agent_who_provoked_update = Agent("jill", 22, self.bed, self.house)

        agent_who_provoked_update.set_action_status("using bed", silent=True)

        self.observation_system.register_update(
            ObservationType.AGENT_USING_OBJECT,
            {
                RegisteredUpdateDataKey.UPDATE_AGENT_NAME: agent_who_provoked_update.name,
                RegisteredUpdateDataKey.IDENTIFIER: self.bed.name.get_identifier(),
            },
        )

        observation_triggers_result = (
            self.observation_system.determine_if_observation_triggers(
                agent, [agent, agent_who_provoked_update], self.house
            )
        )

        self.assertFalse(isinstance(observation_triggers_result, NoneType))

        self.assertFalse(
            observation_triggers_result.get(ObservationDataKey.OBSERVED_AGENT_NAME)
        )
        self.assertFalse(
            observation_triggers_result.get(
                ObservationDataKey.OBSERVED_AGENT_ACTION_STATUS
            )
        )


if __name__ == "__main__":
    unittest.main()
