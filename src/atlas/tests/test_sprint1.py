"""
Each test below corresponds directly to one of the Sprint 1 success
criteria from the Atlas project memory (Section 27):

    1. A module can subscribe to an EventType.
    2. Multiple modules can subscribe to the same EventType.
    3. An Event can be emitted.
    4. The EventBus finds the correct subscriptions.
    5. The associated actions are called.
    6. The Event is passed into the action.
    7. An action can optionally emit another Event.
    8. The Compiler does not need to know which listeners exist.
"""

from __future__ import annotations

import inspect

import pytest

from atlas.events.event import Event, EventType
from atlas.events.event_bus import EventBus
from atlas.events.listener_registry import ListenerRegistry
from atlas.events.subscription import Subscription
from atlas.machines.machine import Machine
from atlas.machines.machine_registry import MachineRegistry


@pytest.fixture
def bus_and_registry() -> tuple[EventBus, ListenerRegistry]:
    registry = ListenerRegistry()
    bus = EventBus(registry)
    return bus, registry


def test_1_module_can_subscribe_to_event_type(bus_and_registry):
    bus, registry = bus_and_registry
    calls = []

    event_type = EventType.START_BUILD
    subscription = Subscription(Event(event_type, "Start build"), lambda e: calls.append(e), "a")

    bus.subscribe(subscription)

    subs = list(registry.get_subscribers(event_type))
    assert len(subs) == 1
    assert subs[0].event.type == event_type


def test_2_multiple_modules_can_subscribe_to_same_event_type(bus_and_registry):
    bus, registry = bus_and_registry

    event_type = EventType.START_BUILD
    bus.subscribe(Subscription(Event(event_type, "Start build"), lambda e: None, "ModuleA"))
    bus.subscribe(Subscription(Event(event_type, "Start build"), lambda e: None, "ModuleB"))

    subs = registry.get_subscribers(event_type)

    assert len(subs) == 2
    assert {s.id for s in subs} == {"ModuleA", "ModuleB"}


def test_3_an_event_can_be_emitted(bus_and_registry):
    bus, _ = bus_and_registry
    bus.publish(Event(EventType.START_BUILD, "go"))


def test_4_eventbus_finds_correct_subscriptions(bus_and_registry):
    bus, _ = bus_and_registry
    start_calls = []
    end_calls = []

    bus.subscribe(
        Subscription(
            Event(EventType.START_BUILD, "Start build"), lambda e: start_calls.append(e), "A"
        )
    )
    bus.subscribe(
        Subscription(Event(EventType.END_BUILD, "Start build"), lambda e: end_calls.append(e), "B")
    )

    bus.publish(Event(EventType.START_BUILD, "starting"))

    assert len(start_calls) == 1
    assert len(end_calls) == 0


def test_5_associated_actions_are_called(bus_and_registry):
    bus, _ = bus_and_registry
    was_called = {"flag": False}

    def action(event: Event) -> None:
        was_called["flag"] = True

    bus.subscribe(Subscription(Event(EventType.LOG, "Logging"), action, "A"))
    bus.publish(Event(EventType.LOG, "hello"))

    assert was_called["flag"] is True


def test_6_event_is_passed_into_the_action(bus_and_registry):
    bus, _ = bus_and_registry
    received = {}

    def action(event: Event) -> None:
        received["event"] = event

    bus.subscribe(Subscription(Event(EventType.LOG, "Logging"), action, "A"))
    emitted = Event(EventType.LOG, "payload check")
    bus.publish(emitted)

    assert received["event"] is emitted
    assert received["event"].message == "payload check"


def test_7_action_can_emit_another_event(bus_and_registry):
    bus, _ = bus_and_registry
    log_messages = []

    def on_log(event: Event) -> None:
        log_messages.append(event.message)

    def on_end_build(event: Event) -> None:
        bus.publish(Event(EventType.LOG, "chained from end_build"))

    bus.subscribe(Subscription(Event(EventType.LOG, "Logging"), on_log, "Logger"))
    bus.subscribe(Subscription(Event(EventType.END_BUILD, "Ended"), on_end_build, "Exporter"))

    bus.publish(Event(EventType.END_BUILD, "done"))

    assert log_messages == ["chained from end_build"]


def test_8_compiler_does_not_reference_listeners(bus_and_registry):
    """Compiler only knows EventBus.publish(). It never references
    Logger, ModuleA, or ModuleB — those are wired up by Atlas
    (the composition root), not by Compiler itself."""
    from atlas.compiler.compiler import Compiler

    source = inspect.getsource(Compiler)
    for forbidden in ("Logger", "ModuleA", "ModuleB"):
        assert forbidden not in source

    # Functional proof: an externally-registered listener, unknown to
    # Compiler at write-time, still receives the event Compiler publishes.
    bus, _ = bus_and_registry
    machine_registry = MachineRegistry()
    machine_registry.register(Machine("Falcon"))
    compiler = Compiler(bus, machine_registry)

    build_events = []
    bus.subscribe(
        Subscription(
            event=Event(EventType.COMPILE_START, "Starting build"),
            callback=lambda e: build_events.append(e),
        )
    )

    compiler.compile("Falcon")

    print(build_events)

    assert len(build_events) == 2
    assert build_events[0].message == "Starting compilation of Falcon"


def test_9_atlas_end_to_end_compile():
    """Smoke test: the real composition root wires Compiler + modules
    together and compile() runs without error."""
    from atlas.cli.app import Atlas  # adjust import path to match your file

    app = Atlas()
    app.compile("Falcon")  # should not raise


def test_10_subscription_matches_by_type_only_not_message(bus_and_registry):
    bus, _ = bus_and_registry
    calls = []
    bus.subscribe(
        Subscription(Event(EventType.LOG, "original text"), lambda e: calls.append(e), "A")
    )
    bus.publish(Event(EventType.LOG, "completely different text"))
    assert len(calls) == 1  # still matches — only type matters
