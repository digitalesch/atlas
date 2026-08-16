from atlas.events.event import Event, EventType
from atlas.events.event_bus import EventBus
from atlas.machines.machine import Machine

class Compiler:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def compile(self, machine: Machine):
        self.event_bus.publish(Event(EventType.COMPILE_START, "Starting build"))
        # self.event_bus.publish(Event(EventType.END_BUILD, "Ending build"))
