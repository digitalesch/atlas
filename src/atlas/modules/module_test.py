from atlas.core.wrappers import auto_register, subscribe
from atlas.events.event import Event, EventType


@auto_register
class ModuleA:
    @subscribe(EventType.START_BUILD, "Listen to start build")
    def start_build(self, event: Event):
        print("[ModuleA] Starting build")

        self.event_bus.publish(
            Event(
                EventType.LOG,
                "ModuleA started the build",
            )
        )


@auto_register
class ModuleB:
    @subscribe(EventType.START_BUILD, "Listen to start build")
    def start_build(self, event: Event):
        print("[ModuleB] Starting build")

        self.event_bus.publish(
            Event(
                EventType.LOG,
                "ModuleB started the build",
            )
        )
