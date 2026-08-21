from __future__ import annotations

from atlas.events.event import Event, EventType
from atlas.events.subscription import Subscription


def test_event_can_be_emitted(return_compiler):
    instanced_compiler = return_compiler("Falcon")
    instanced_compiler.event_bus.publish(Event(EventType.START_BUILD, "go"))

def test_event_is_passed_into_the_action(return_compiler):
    received = {}

    def action(event: Event) -> None:
        received["event"] = event

    instanced_compiler = return_compiler("Falcon")

    instanced_compiler.event_bus.subscribe(Subscription(Event(EventType.LOG, "Logging"), action, "A"))
    emitted = Event(EventType.LOG, "payload check")
    instanced_compiler.event_bus.publish(emitted)

    assert received["event"] is emitted
    assert received["event"].message == "payload check"