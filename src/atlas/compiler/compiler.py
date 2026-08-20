from atlas.core.wrappers import auto_register, subscribe
from atlas.events.event import Event, EventType
from atlas.events.event_bus import EventBus
from atlas.machines.machine_registry import MachineRegistry


@auto_register
class Compiler:
    def __init__(
        self,
        event_bus: EventBus,
        machine_registry: MachineRegistry,
    ):
        self.event_bus = event_bus
        self.machine_registry = machine_registry

    @subscribe(EventType.END_BUILD, "Listen to end build")
    def on_end_compile(self, event: Event):
        print("[END] Ending build")

    @subscribe(EventType.COMPILE_ERROR, "Compile errors should raise")
    def on_compile_error(self, event: Event):
        print("Error compiling, will fail and unsubscribes all")
        self.event_bus = {}

    def compile(self, machine_name: str = ""):

        machine = self.machine_registry.get(machine_name)

        if machine:

            self.event_bus.publish(
                Event(
                    EventType.COMPILE_START,
                    f"Starting compilation of {machine.name}",
                    payload=machine,
                )
            )

            self.event_bus.publish(
                Event(
                    EventType.START_BUILD,
                    f"Building {machine.name}",
                    payload=machine,
                )
            )

            self.event_bus.publish(
                Event(
                    EventType.COMPILE_END,
                    f"Compilation finished: {machine.name}",
                    payload=machine,
                )
            )

            self.event_bus.publish(
                Event(
                    EventType.END_BUILD,
                    f"Finished building {machine.name}",
                    payload=machine,
                )
            )
