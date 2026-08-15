from atlas.events.event import Event, EventType
from atlas.events.event_bus import EventBus
from atlas.events.subscription import Subscription
from atlas.modules.logger import Logger
from atlas.modules.teste import ModuleA, ModuleB

class Compiler():
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.listener_registry.register(
            Subscription(event=Event(EventType.LOG, "Log"), callback=Logger.teste)
        )

        self.module_a = ModuleA(self.event_bus)   # self-registers internally
        self.module_b = ModuleB(self.event_bus)   # self-registers internally

    def compile(self):
        self.event_bus.publish(Event(EventType.START_BUILD, "Starting build"))
        self.event_bus.publish(Event(EventType.END_BUILD, "Ending build"))
        # self.event_bus.listener_registry.register(Listener(name="module_a",events=[Event(EventType.START_BUILD, "Listen to start build")]))
