from atlas.compiler.compiler import Compiler
from atlas.events.event_bus import EventBus
from atlas.events.listener_registry import ListenerRegistry
from atlas.machines.machine import Machine
from atlas.machines.machine_registry import MachineRegistry

registry = ListenerRegistry()
bus = EventBus(registry)
machine_registry = MachineRegistry()
machine_registry.register(Machine("Falcon"))

instanced_compiler = Compiler(bus, machine_registry)