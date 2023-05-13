from errors import MissingCharacterSummaryError


class Agent:
    def __init__(self, name, age, current_location, environment_tree):
        self.name = name
        self.age = age
        self.current_location = current_location
        self.environment_tree = environment_tree

        self._character_summary = None

    def set_character_summary(self, character_summary):
        self._character_summary = character_summary


    def get_character_summary(self):
        if self._character_summary is None:
            raise MissingCharacterSummaryError(f"Requested the character summary of agent {self.name}, but it hadn't been set.")
        
        return self._character_summary
    