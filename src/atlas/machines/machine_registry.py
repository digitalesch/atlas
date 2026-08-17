from .machine import Machine


class MachineRegistry:

    def __init__(self):
        self.machines: dict[str, Machine] = {}

    def register(self, machine: Machine):
        self.machines[machine.name] = machine

    def get(self, name: str) -> Machine:
        return self.machines[name]
