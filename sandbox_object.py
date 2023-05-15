class SandboxObject:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.action_status = None

    def __str__(self):
        return f"Sandbox object: {self.name}"

    def __repr__(self) -> str:
        return f"Sandbox object: {self.name}"
