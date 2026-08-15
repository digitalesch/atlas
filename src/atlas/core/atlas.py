from atlas.compiler.compiler import Compiler
from atlas.events.event_bus import EventBus
from atlas.events.listener_registry import ListenerRegistry


class Atlas:
    def __init__(self):
        self.listener_registry = ListenerRegistry()
        self.event_bus = EventBus(self.listener_registry)
        self.compiler = Compiler(self.event_bus)

    def compile(self):
        """Compile and creates the modules."""
        self.compiler.compile()
