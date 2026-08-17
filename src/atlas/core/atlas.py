from atlas.compiler.compiler import Compiler
from atlas.events.event import Event, EventType
from atlas.events.event_bus import EventBus
from atlas.events.listener_registry import ListenerRegistry
from atlas.events.subscription import Subscription
from atlas.machines.falcon import Falcon
from atlas.machines.machine_registry import MachineRegistry
from atlas.modules.logger import Logger
from atlas.modules.module_test import ModuleA, ModuleB


class Atlas:

    def __init__(self):

        # -------------------------
        # Infrastructure
        # -------------------------

        self.listener_registry = ListenerRegistry()

        self.event_bus = EventBus(self.listener_registry)

        self.machine_registry = MachineRegistry()

        # -------------------------
        # Machines
        # -------------------------

        self.machine_registry.register(Falcon)

        # -------------------------
        # Global subscriptions
        # -------------------------

        self.event_bus.subscribe(
            Subscription(event=Event(EventType.LOG, "Teste"), callback=Logger.teste)
        )

        # -------------------------
        # Modules
        # -------------------------

        self.module_a = ModuleA(self.event_bus)

        self.module_b = ModuleB(self.event_bus)

        # -------------------------
        # Debug
        # -------------------------

        self.listener_registry.debug()

        # -------------------------
        # Compiler
        # -------------------------

        self.compiler = Compiler(
            event_bus=self.event_bus,
            machine_registry=self.machine_registry,
        )

    def compile(self, machine_name: str):

        return self.compiler.compile(machine_name)
