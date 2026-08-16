from atlas.compiler.compiler import Compiler
from atlas.events.event_bus import EventBus
from atlas.events.listener_registry import ListenerRegistry
from atlas.machines.machine import machine
from atlas.events.subscription import Subscription
from atlas.events.event import Event, EventType
from atlas.modules.module_test import ModuleA, ModuleB
from atlas.modules.logger import Logger

class Atlas:
    def __init__(self):
        self.listener_registry = ListenerRegistry()
        self.event_bus = EventBus(self.listener_registry)
        self.compiler = Compiler(self.event_bus)

        self.event_bus.subscribe(
            Subscription(event=Event(EventType.LOG, "Log"), callback=Logger.teste)
        )

        self.module_a = ModuleA(self.event_bus)  # self-registers internally
        self.module_b = ModuleB(self.event_bus)  # self-registers internally

    def compile(self):
        """Compile and creates the modules."""
        self.compiler.compile(machine)
