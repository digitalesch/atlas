import pytest

from atlas.compiler.compiler import Compiler
from atlas.events.event_bus import EventBus
from atlas.events.listener_registry import ListenerRegistry
from atlas.machines.machine import Machine
from atlas.machines.machine_registry import MachineRegistry


@pytest.fixture
def return_compiler():
    def _create_compiler(machine_name: str):
        registry = ListenerRegistry()
        bus = EventBus(registry)

        machine_registry = MachineRegistry()
        machine_registry.register(Machine(machine_name))

        return Compiler(bus, machine_registry)

    return _create_compiler