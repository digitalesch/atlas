# Atlas — Event Bus Architecture

A lightweight pub/sub system powering Atlas's compiler pipeline. Modules react to
events (build stages, logs, errors) without needing direct references to each other.

## Project layout

```
atlas/
├── pyproject.toml
├── uv.lock
└── src/
    └── atlas/
        ├── __init__.py
        ├── __main__.py
        ├── cli/
        │   └── app.py
        ├── core/
        │   ├── atlas.py          # composition root
        │   └── wrappers.py       # @auto_register, @subscribe decorators
        ├── compiler/
        │   └── compiler.py
        ├── events/
        │   ├── event.py          # Event, EventType
        │   ├── event_bus.py      # EventBus.publish/subscribe
        │   ├── subscription.py   # Subscription dataclass
        │   └── listener_registry.py
        └── modules/
            └── ...                # ModuleA, ModuleB, etc.
```

## Core concepts

### `Event` / `EventType`

An `Event` pairs an `EventType` (enum) with a human-readable `message`. `EventType`
enumerates every stage/signal in the system, e.g. `START_BUILD`, `END_BUILD`,
`ERROR`, `LOG`.

### `Subscription`

Links one `Event` (really, one `EventType`) to a callback. Each `Subscription` has
a unique `id` (UUID), generated automatically, used later for unregistering.

```python
@dataclass
class Subscription:
    event: Event
    callback: Callable[[Event], None]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
```

### `ListenerRegistry`

Stores subscriptions in a flat `dict[uuid, Subscription]`. Chosen over a nested
`dict[EventType, dict[uuid, Subscription]]` deliberately — at Atlas's current
scale (a handful of modules and event types), the O(n) scan on publish is
negligible, and the flat structure keeps `register`/`unregister` trivially simple
(callers only ever need a subscription's `uuid`, nothing else).

```python
class ListenerRegistry:
    def register(self, subscription: Subscription) -> str: ...
    def unregister(self, sub_id: str) -> None: ...
    def get_subscribers(self, event_type: EventType) -> list[Subscription]: ...
```

### `EventBus`

Owns a `ListenerRegistry` and exposes `publish()`. Dispatch is **synchronous**:
`publish()` loops through matching subscribers and calls each callback in order,
blocking until every one returns before control goes back to the caller.

```python
class EventBus:
    def __init__(self, listener_registry: ListenerRegistry):
        self.listener_registry = listener_registry

    def publish(self, event: Event, message: str = ""):
        for subscriber in self.listener_registry.get_subscribers(event.type):
            subscriber.callback(event)
```

This is intentional, not a limitation to "fix" later: compiler stages generally
need deterministic ordering (parsing must finish before validation starts), and
synchronous dispatch means `publish()` returning *is* the completion signal — no
extra bookkeeping needed to know "is everyone done reacting yet."

## Declarative module registration

Rather than manually calling `listener_registry.register(...)` inside every
module's `__init__`, modules declare their event handlers with `@subscribe` and
the class itself is decorated with `@auto_register`:

```python
from atlas.core.wrappers import auto_register, subscribe
from atlas.events.event import EventType, Event

@auto_register
class ModuleA:
    @subscribe(EventType.END_BUILD, "Listen to end build")
    def on_end_build(self, event: Event):
        print("ModuleA reacting to end build")
```

### How it works

- **`@subscribe(event_type, message)`** — a parameterized decorator that tags a
  method with `_subscribe_event = Event(event_type, message)`. It does nothing
  by itself; it just marks metadata for `@auto_register` to find later.
- **`@auto_register`** — a class decorator that wraps `__init__`. On
  construction, it:
  1. Calls the class's original `__init__` (if one is defined — classes with no
     custom `__init__` are handled safely too, since `object.__init__` can't
     accept extra arguments).
  2. Stores `self.event_bus`.
  3. Scans the class for any method tagged with `_subscribe_event` and
     registers it against the shared `EventBus`.
  4. Enforces **single instantiation** — raises `RuntimeError` if the class is
     constructed more than once, preventing accidental duplicate subscriptions
     (a real bug hit during development: constructing the same module twice
     silently double-registered its callbacks, causing every event to fire
     twice).

This means construction *is* wiring — no separate registration step, no way to
forget it, and no way for a module to end up subscribed twice by accident.

## Dependency injection, not a singleton

Early on, a classic Python singleton (`__new__` override) was considered for
`EventBus`, but dropped in favor of plain dependency injection:

```python
class Atlas:
    def __init__(self):
        self.listener_registry = ListenerRegistry()
        self.event_bus = EventBus(self.listener_registry)
        self.compiler = Compiler(self.event_bus)
```

`Atlas` is the **composition root** — the one place that constructs
`EventBus` and hands the *same instance* down to every module and subsystem
via their constructors. This gives every guarantee a singleton would (exactly
one bus, shared everywhere), while staying explicit, testable, and free of
hidden global state or `__new__`/`__init__` signature-mismatch footguns.

## Logging every publish

`EventBus.publish` is decorated with `Logger.log_publish`, which traces every
call: who published, what event, and (via `inspect.stack()`) which function
triggered it — including calls that originate from inside another callback,
so full causal chains are visible:

```
Publishing EventType.START_BUILD for [compile]
ModuleA reacting to end build
Publishing EventType.ERROR for [on_end_build]
ModuleB reacting to error
Finished EventType.ERROR
Finished EventType.START_BUILD
```

Application-level logging (`EventType.LOG`) is a separate, complementary
mechanism — code can explicitly `publish(Event(EventType.LOG, "..."))` to log
something meaningful, distinct from the decorator's automatic call tracing.

## Unsubscribing

A subscription does **not** expire after firing once — as long as it's in the
registry, it fires every time its event is published, for the life of the
program. That's the correct, intended behavior for persistent pipeline stages
(a linker, a logger, a validator should react to *every* build, not just the
first).

Unsubscribing matters in three cases:

| Situation | Unsubscribe? |
|---|---|
| Module is a live, ongoing part of the system | No — leave it subscribed |
| Module/object is being torn down or replaced | Yes — call `unsubscribe_all()` before discarding |
| Handler is explicitly meant to fire once | Yes — self-unsubscribe inside the handler |

`@auto_register` tracks every subscription ID it creates for a given instance,
so a generated `unsubscribe_all()` can clean them all up in one call when a
module is genuinely being discarded.

## Pipeline shape: chaining and fan-out

Individual stages publish the *next* stage's event when they finish, so a
`Compiler.compile()` call only needs to kick off the first event — the rest of
the pipeline advances itself:

```python
@auto_register
class Parser:
    @subscribe(EventType.START_BUILD, "Parse source")
    def on_start_build(self, event: Event):
        ...
        self.event_bus.publish(Event(EventType.PARSE_DONE, "Parsing complete"))

@auto_register
class Validator:
    @subscribe(EventType.PARSE_DONE, "Validate AST")
    def on_parse_done(self, event: Event):
        ...
```

Multiple modules can subscribe to the same event for independent fan-out (e.g.
a `Linter` and a `Validator` both reacting to `PARSE_DONE`) without knowing
about each other. Because dispatch is synchronous, this fan-out is **sequential
under the hood**, not concurrent — deterministic and easy to trace, at the cost
of not being true parallelism. Real parallel execution (e.g. compiling
independent source files concurrently) is a deliberate future addition, not
something baked into the bus itself — it would be scoped to a specific stage
internally (e.g. a thread pool inside one module) that still reports back to
the bus with a single "done" event, keeping the bus itself simple.

## Tooling

- **Package manager:** [`uv`](https://docs.astral.sh/uv/), `src/atlas` layout,
  entry point `atlas = "atlas.__main__:main"`.
- **`uv.lock`** is committed to version control — it pins exact resolved
  dependency versions for reproducible installs across machines/CI. Only
  `.venv/` and cache directories are gitignored.
- **Formatting/linting:** `black` (or `ruff format` as a faster, compatible
  alternative) for style; `ruff check` for actual linting (unused imports,
  import ordering, banning ambiguous relative imports via `TID252`).

```bash
uv sync                    # install locked dependencies
uv run atlas compile       # run via the CLI entry point
uv run black .              # format
uv run ruff check .         # lint
```

## Known open questions / future work

- **Ordering across independent subscribers** of the same event isn't
  currently guaranteed beyond registration order — fine while stages are
  independent, but would need an explicit priority field on `Subscription` if
  ordering ever becomes load-bearing.
- **Fan-out convergence** (e.g. "publish `END_BUILD` only once every parallel
  branch has finished") isn't solved yet — the current pipeline is linear
  enough that whichever stage finishes last just publishes the next event, but
  this gets fragile once genuine multi-branch fan-out is introduced. A step
  counter/barrier is the likely solution when this is needed.
- **Error propagation** between stages is currently just convention (a stage
  *can* publish `ERROR`, but nothing gates downstream stages from running
  regardless) — worth deciding explicitly once real build stages exist.
