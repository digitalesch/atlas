from atlas.events.event import EventType, Event
from atlas.events.event_bus import EventBus
from atlas.events.subscription import Subscription

class ModuleA:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.listener_registry.register(
            Subscription(event=Event(EventType.END_BUILD, "Listen to end build"), callback=self.on_end_build)
        )

    def on_end_build(self, event: Event):
        print("ModuleA reacting to end build")
        self.event_bus.publish(Event(EventType.ERROR, "Error"))

class ModuleB:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.listener_registry.register(
            Subscription(event=Event(EventType.ERROR, "Error"), callback=self.on_error_build)
        )

    def on_error_build(self, event: Event):
        print("ModuleB reacting to end build")