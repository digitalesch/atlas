from __future__ import annotations

import inspect

from atlas.events.event import Event, EventType
from atlas.events.subscription import Subscription


def test_compiler_does_not_reference_listeners(return_compiler):
    """Compiler only knows EventBus.publish(). It never references
    Logger, ModuleA, or ModuleB — those are wired up by Atlas
    (the composition root), not by Compiler itself."""
    from atlas.compiler.compiler import Compiler

    source = inspect.getsource(Compiler)
    for forbidden in ("Logger", "ModuleA", "ModuleB"):
        assert forbidden not in source

    build_events = []
    instanced_compiler = return_compiler("Falcon")

    instanced_compiler.event_bus.subscribe(
        Subscription(
            event=Event(EventType.COMPILE_START, "Starting build"),
            callback=lambda e: build_events.append(e),
        )
    )

    instanced_compiler.compile("Falcon")

    assert len(build_events) == 1
    assert build_events[0].message == "Starting compilation of Falcon"


def test_atlas_end_to_end_compile(return_compiler):
    """Smoke test: the real composition root wires Compiler + modules
    together and compile() runs without error."""
    instanced_compiler = return_compiler("Falcon")

    instanced_compiler.compile("Falcon")  # should not raise

def test_compilation_failure_publishes_error(return_compiler):
    instanced_compiler = return_compiler("Falcon")

    instanced_compiler.event_bus.publish(
        Event(EventType.COMPILE_ERROR, "completely different text")
    )

    subs = instanced_compiler.event_bus

    assert subs == {}

def test_registry_return_unknown_machine(return_compiler):
    instanced_compiler = return_compiler("Falcon")

    result = instanced_compiler.machine_registry.get("Test")

    assert result == None