from atlas.core.wrappers import auto_register, subscribe
from atlas.events.event import Event, EventType


@auto_register
class ModuleA:
    @subscribe(EventType.END_BUILD, "Listen to end build")
    def on_end_build(self, event: Event):
        print(f"ModuleA reacting to {event.type} with {event.message}")


@auto_register
class ModuleB:
    @subscribe(EventType.END_BUILD, "Listen to end build")
    def on_end_build(self, event: Event):
        print(f"ModuleB reacting to {event.type} with {event.message}")

    @subscribe(EventType.START_BUILD, "Listen to start build")
    def on_start_build(self, event: Event):
        print(f"ModuleB reacting to {event.type} with {event.message}")
