import datetime
import unittest

from anytree import Node
from agent import Agent
from location import Location
from memories_querying import update_most_recent_access_timestamps


def fake_load_contents_of_json_file_function(_json_filename):
    return {
        "0": {
            "description": "Description 1",
            "creation_timestamp": "2023-05-11T10:30:45",
            "most_recent_access_timestamp": "2023-05-11T10:30:45",
            "recency": 1.0,
            "importance": 0.6,
        },
        "1": {
            "description": "Description 2",
            "creation_timestamp": "2023-05-11T10:30:45",
            "most_recent_access_timestamp": "2023-05-11T10:30:45",
            "recency": 1.0,
            "importance": 0.35,
        },
        "2": {
            "description": "Description 3",
            "creation_timestamp": "2023-05-11T10:30:45",
            "most_recent_access_timestamp": "2023-05-11T10:30:45",
            "recency": 0.8,
            "importance": 0.2,
        },
    }


def fake_create_json_file_function(_json_filename, _memories):
    pass


class TestUpdateMostRecentAccessTimestamp(unittest.TestCase):
    def test_when_passed_nearest_neighbors_of_query_their_most_recent_access_times_get_updated(
        self,
    ):
        current_time = datetime.datetime(2023, 5, 11, 10, 30, 45)

        memories_raw_data = {}
        memories_raw_data[0] = {
            "description": "Description 1",
            "creation_timestamp": current_time.isoformat(),
            "most_recent_access_timestamp": current_time.isoformat(),
            "recency": 0.9,
            "importance": 0.6,
        }
        memories_raw_data[1] = {
            "description": "Description 2",
            "creation_timestamp": current_time.isoformat(),
            "most_recent_access_timestamp": current_time.isoformat(),
            "recency": 0.9,
            "importance": 0.35,
        }

        nearest_neighbors = ([0, 1], [0.9, 1.2])

        # now advance the time.
        delta = datetime.timedelta(minutes=30)

        new_time = current_time + delta

        town = Node(Location("town", "town", "town"))

        agent = Agent("test", 22, town, town)

        memories_raw_data = update_most_recent_access_timestamps(
            agent,
            nearest_neighbors,
            new_time,
            fake_load_contents_of_json_file_function,
            fake_create_json_file_function,
        )

        self.assertEqual(
            datetime.datetime.fromisoformat(
                memories_raw_data[str(0)]["most_recent_access_timestamp"]
            ),
            new_time,
        )
        self.assertEqual(memories_raw_data[str(0)]["recency"], 1.0)
        self.assertEqual(
            datetime.datetime.fromisoformat(
                memories_raw_data[str(1)]["most_recent_access_timestamp"]
            ),
            new_time,
        )
        self.assertEqual(memories_raw_data[str(1)]["recency"], 1.0)
        self.assertEqual(
            datetime.datetime.fromisoformat(
                memories_raw_data[str(2)]["most_recent_access_timestamp"]
            ),
            current_time,
        )
        self.assertEqual(memories_raw_data[str(2)]["recency"], 0.8)


if __name__ == "__main__":
    unittest.main()
