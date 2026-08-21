from __future__ import annotations

from atlas.events.event import Event, EventType
from atlas.events.subscription import Subscription
from atlas.modules.module_test import ModuleA, ModuleB


def test_module_can_subscribe_to_event_type(return_compiler):
    calls = []
    instanced_compiler = return_compiler("Falcon")

    event_type = EventType.START_BUILD
    subscription = Subscription(Event(event_type, "Start build"), lambda e: calls.append(e), "a")

    instanced_compiler.event_bus.subscribe(subscription)

    subs = list(instanced_compiler.event_bus.listener_registry.get_subscribers(event_type))
    assert len(subs) == 1
    assert subs[0].event.type == event_type

    instanced_compiler.event_bus.unsubscribe(event_type, "a")

    print(instanced_compiler.event_bus.listener_registry.registry)


def test_multiple_modules_can_subscribe_to_same_event_type(return_compiler):
    event_type = EventType.START_BUILD
    instanced_compiler = return_compiler("Falcon")
    _ = ModuleA(instanced_compiler.event_bus)
    _ = ModuleB(instanced_compiler.event_bus)

    subs = instanced_compiler.event_bus.listener_registry.get_subscribers(event_type)

    assert len(subs) == 2  # since i'm using the compiler, it's 2 subscribers added + compiler
    assert {s.id for s in subs} == {"ModuleA", "ModuleB"}

def test_eventbus_finds_correct_subscriptions(return_compiler):
    start_calls = []
    end_calls = []

    instanced_compiler = return_compiler("Falcon")

    instanced_compiler.event_bus.subscribe(
        Subscription(
            Event(EventType.START_BUILD, "Start build"), lambda e: start_calls.append(e), "A"
        )
    )
    instanced_compiler.event_bus.subscribe(
        Subscription(Event(EventType.END_BUILD, "Start build"), lambda e: end_calls.append(e), "B")
    )

    instanced_compiler.event_bus.publish(Event(EventType.START_BUILD, "starting"))

    assert len(start_calls) == 1
    assert len(end_calls) == 0

def test_event_associated_actions_are_called(return_compiler):
    was_called = {"flag": False}

    def action(event: Event) -> None:
        was_called["flag"] = True

    instanced_compiler = return_compiler("Falcon")

    instanced_compiler.event_bus.subscribe(Subscription(Event(EventType.LOG, "Logging"), action, "A"))
    instanced_compiler.event_bus.publish(Event(EventType.LOG, "hello"))

    assert was_called["flag"] is True

def test_action_can_emit_another_event(return_compiler):
    log_messages = []
    instanced_compiler = return_compiler("Falcon")

    def on_log(event: Event) -> None:
        log_messages.append(event.message)

    def on_end_build(event: Event) -> None:
        instanced_compiler.event_bus.publish(Event(EventType.LOG, "chained from end_build"))


    instanced_compiler.event_bus.subscribe(Subscription(Event(EventType.LOG, "Logging"), on_log, "Logger"))
    instanced_compiler.event_bus.subscribe(Subscription(Event(EventType.END_BUILD, "Ended"), on_end_build, "Exporter"))

    instanced_compiler.event_bus.publish(Event(EventType.END_BUILD, "done"))

    assert log_messages == ["chained from end_build"]

def test_subscription_matches_by_type_only_not_message(return_compiler):
    calls = []
    instanced_compiler = return_compiler("Falcon")

    instanced_compiler.event_bus.subscribe(
        Subscription(Event(EventType.LOG, "original text"), lambda e: calls.append(e), "A")
    )
    instanced_compiler.event_bus.publish(Event(EventType.LOG, "completely different text"))
    assert len(calls) == 1  # still matches — only type matters