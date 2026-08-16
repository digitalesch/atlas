# Atlas Mechanical Compiler — Project Memory & Architecture

> **Purpose of this document:** hand off the current Atlas project state to a future session without losing the architectural reasoning behind the decisions.

---

# 1. What Atlas is

Atlas is being designed as a **hardware/mechanical compilation framework**, not as a one-off 3D-printer generator.

The original experiment is a CoreXY printer with an intentionally oversized upper frame/gantry and smaller fixed bed:

```text
Upper frame / gantry: ~560 × 560 mm
Bed / workspace:      ~400 × 400 mm
```

The larger upper structure gives the moving XY system enough room to traverse the complete 400 × 400 workspace.

The printer is the **first target for the framework**, not the final product.

The bigger idea is:

> **Don't build one printer. Build a framework that can compile many machines.**

A user should eventually be able to compose a machine from modules, constraints, interfaces, and configuration without manually specifying every low-level detail whenever the machine changes.

---

# 2. The core Atlas vision

Atlas should eventually behave more like a traditional compiler/toolchain:

```text
User Machine Definition
        ↓
Parse / Load
        ↓
Machine Specification
        ↓
Validation
        ↓
Mechanical Resolution
        ↓
Mechanical IR
        ↓
Geometry / Assembly
        ↓
Exporters
   ┌────┼────┬────┐
   ↓    ↓    ↓    ↓
OpenSCAD STEP STL BOM
              ↓
       Documentation
```

The important idea is the **intermediate representation**.

The compiler should not directly turn every configuration option into OpenSCAD code.

Instead:

```text
Configuration
     ↓
Machine Model
     ↓
Mechanical IR
     ↓
OpenSCAD / STEP / STL / BOM / Docs
```

This allows multiple exporters to consume the same machine representation.

---

# 3. What "compiling hardware" means

Atlas is intended to take a high-level description of a physical machine and resolve it into a concrete, validated machine.

For example:

```yaml
workspace:
  x: 400
  y: 400
  z: 500

frame:
  architecture: boxed_tower
  width: 560
  depth: 560

motion:
  architecture: corexy

rails:
  type: mgn12
```

The user expresses **intent and architecture**, rather than manually specifying every bolt and coordinate.

Atlas eventually resolves:

```text
Frame
    ↓
Extrusions
    ↓
Bracing
    ↓
Mounting interfaces
    ↓
Rails
    ↓
Gantry
    ↓
Toolhead
    ↓
Constraints
```

and produces concrete artifacts.

For example:

```text
Atlas compile
    ↓
Machine model
    ↓
Validation
    ↓
OpenSCAD
STEP
STL
BOM
Assembly documentation
```

---

# 4. The most important abstraction: intent vs implementation

The framework should allow the user to say:

```text
Use MGN12 rails.
```

instead of:

```text
Put this exact rail at these exact coordinates.
Use these exact bolts.
Drill these exact holes.
```

Likewise:

```text
Use a boxed tower frame.
```

should cause Atlas to resolve the geometry needed for that architecture.

The compiler owns implementation details.

This is the same conceptual advantage as software abstractions:

```text
Interface
    ↓
Implementation
```

For hardware:

```text
Mechanical Interface
    ↓
Concrete Component
```

---

# 5. Mechanical interfaces

A long-term core concept is the **mechanical interface**.

Components should describe what they require/provide rather than being hardwired directly to other components.

Examples:

```text
Frame
    provides → mounting surfaces

Linear rail
    requires → compatible mounting surface

Motor
    provides → rotational drive interface

Pulley
    requires → compatible shaft

Toolhead
    requires → carriage interface

Bed
    requires → support/mounting interface
```

This allows Atlas to resolve compatible components.

The user should not need to change dozens of bolt definitions simply because a component implementation changed.

---

# 6. Constraints are part of compilation

A hardware compiler must understand that geometry has physical relationships.

Examples:

```text
Gantry must clear the bed.

Toolhead must reach the requested workspace.

Rails must fit their mounting surfaces.

Bed must fit inside the frame.

Moving parts must not collide.

Travel must satisfy requested dimensions.

Motor and pulley interfaces must be compatible.

Fasteners must fit available mounting geometry.
```

Therefore the compilation pipeline eventually becomes:

```text
Machine Definition
        ↓
Resolve components
        ↓
Resolve interfaces
        ↓
Apply constraints
        ↓
Validate
        ↓
Generate Mechanical IR
        ↓
Generate artifacts
```

A compilation failure should eventually be meaningful:

```text
ERROR: Insufficient X travel.

Required workspace: 400 mm
Available travel:   372 mm

Cause:
X-axis rail configuration is too short.
```

---

# 7. Modules are the building blocks

A machine should be assembled from modules.

Potential modules:

```text
Frame
Towers
Bracing
Motion System
X Axis
Y Axis
Z Axis
Gantry
Bed
Toolhead
Rails
Motors
Belts
Electronics
Fasteners
Exporter
```

The same compiler should support different architectures.

For example:

```text
Machine A

Frame
  ↓
CoreXY
  ↓
Bed
  ↓
Toolhead
```

versus:

```text
Machine B

Frame
  ↓
Cartesian Motion
  ↓
Bed
  ↓
Toolhead
```

The compiler should not be rewritten for Machine B.

---

# 8. Plugin architecture

This naturally leads to plugins.

Potential plugins:

```text
CoreXYPlugin
CartesianPlugin
BoxedTowerFramePlugin
MGN12Plugin
ToolheadPlugin
OpenSCADExporter
STEPExporter
BOMExporter
```

Registries can provide implementations:

```text
ComponentRegistry

CoreXY
    → CoreXYMotion

BoxedTowerFrame
    → BoxedTowerFrame

MGN12
    → MGN12Rail
```

and:

```text
ExporterRegistry

openscad
    → OpenSCADExporter

step
    → STEPExporter

stl
    → STLExporter

bom
    → BOMExporter
```

This keeps the compiler core independent from individual implementations.

---

# 9. Software architecture currently being built

The current software work is **Phase 1 / Sprint 1**.

The first architectural goal is an event-driven extension mechanism based on:

```text
Event
EventType
Subscription
Listener
ListenerRegistry
EventBus
Compiler
Application
```

The current focus is understanding and implementing the Observer pattern correctly.

---

# 10. Event mental model

The most important distinction discovered so far:

```text
Event
    = "What happened?"

Subscription
    = "What event am I interested in, and what should happen?"

Action
    = "What behavior should execute?"
```

These must remain separate.

An Event is a fact:

```python
Event(
    type=EventType.START_BUILD,
    message="Build started",
)
```

A Subscription is a relationship:

```python
Subscription(
    event_type=EventType.START_BUILD,
    action=module.start_build,
)
```

The Subscription means:

> When START_BUILD happens, call `module.start_build`.

This abstraction was a major design milestone.

---

# 11. EventType

`EventType` represents event categories.

Current examples:

```text
EMIT
SUBSCRIBE
UNSUBSCRIBE
ERROR
LOG
START_BUILD
END_BUILD
```

These are currently represented as an enum.

The exact list is still expected to evolve.

---

# 12. Event

Event represents an actual occurrence.

Conceptually:

```python
@dataclass
class Event:
    type: EventType
    message: str
```

Example:

```python
Event(
    EventType.START_BUILD,
    "Starting build",
)
```

The Event should not know which modules consume it.

---

# 13. Subscription

Subscription is the key dispatch abstraction.

Conceptually:

```python
@dataclass
class Subscription:
    event_type: EventType
    action: Callable
```

Example:

```python
Subscription(
    event_type=EventType.START_BUILD,
    action=module.start_build,
)
```

This makes a module's contract explicit.

For example:

```text
FrameModule

INPUT
START_BUILD

ACTION
start_build(event)

OUTPUT
possibly FRAME_BUILT
```

A Subscription should stay simple.

It should not be responsible for:

- retries
- queues
- logging
- plugin discovery
- module discovery
- concurrency
- error recovery

Those belong elsewhere.

---

# 14. Listener

A Listener is an object/module capable of reacting to events.

Examples:

```text
Compiler
Logger
FrameModule
GantryModule
Exporter
Plugin
```

A listener can have multiple subscriptions.

Example:

```text
Compiler
 ├── END_BUILD → on_end_build
 ├── ERROR     → on_error
 └── LOG       → on_log
```

The Listener should contain behavior.

The Subscription connects that behavior to an EventType.

---

# 15. ListenerRegistry

The ListenerRegistry stores subscriptions for dispatch.

Its main question is:

> **Who wants to hear this event?**

Therefore the preferred internal structure is:

```python
dict[EventType, list[Subscription]]
```

Conceptually:

```text
START_BUILD
    ├── ModuleA.start_build
    ├── ModuleB.start_build
    └── Logger.log

END_BUILD
    └── Compiler.on_end_build

ERROR
    ├── Logger.on_error
    └── Metrics.on_error
```

The registry should be inverted around EventType because `emit()` starts with an Event.

Avoid mixing unrelated key types.

Do not create a registry like:

```text
EventType.START_BUILD → [...]
EventType.END_BUILD → [...]
"compiler" → [...]
"module_a" → [...]
```

The registry should primarily answer:

```text
EventType → subscriptions
```

If we later need reverse lookup:

```text
Listener → subscriptions
```

that can be a separate structure/API.

---

# 16. EventBus

EventBus is responsible for dispatch.

It owns or receives the ListenerRegistry.

Conceptual API:

```python
subscribe(...)
unsubscribe(...)
emit(...)
```

The basic `emit()` flow should eventually be:

```python
def emit(self, event):
    subscriptions = self.listener_registry.get(event.type)

    for subscription in subscriptions:
        subscription.action(event)
```

The EventBus does not need to know what individual modules do.

It only knows:

```text
Event
  ↓
EventType
  ↓
Registry
  ↓
Subscriptions
  ↓
Actions
```

---

# 17. Compiler

Compiler should not know which modules are listening.

It receives the EventBus through dependency injection:

```python
class Compiler:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
```

It can then emit lifecycle events:

```python
self.event_bus.emit(
    Event(
        EventType.START_BUILD,
        "Starting build",
    )
)
```

The Compiler does not need:

```text
ModuleA
ModuleB
Logger
Exporter
```

hardcoded into its logic.

That is the decoupling we want.

---

# 18. Application / composition root

The application is responsible for wiring the runtime.

Conceptually:

```python
class Application:

    def __init__(self):
        self.listener_registry = ListenerRegistry()
        self.event_bus = EventBus(self.listener_registry)
        self.compiler = Compiler(self.event_bus)

    def compile(self):
        self.compiler.compile()
```

The CLI should remain thin:

```python
@app.command()
def compile():
    atlas_app = Application()
    atlas_app.compile()
```

The Application is the **composition root**.

It assembles Atlas.

It should not contain the mechanical compilation logic.

---

# 19. Event-driven workflow example

A possible future workflow:

```text
Compiler
    │
    │ emit START_BUILD
    ▼
Module A
    │
    │ performs work
    │ emit END_BUILD
    ▼
Compiler
```

For example:

```text
Compiler
    subscribes → END_BUILD
    emits      → START_BUILD

Module A
    subscribes → START_BUILD
    emits      → END_BUILD
```

This can eventually produce an event-driven workflow/state-machine-like system.

However:

**Do not make the entire compiler asynchronous or event-driven yet.**

For the first implementation, keep core compilation deterministic and synchronous.

Events should initially provide:

- lifecycle notifications
- extension points
- module communication
- observability

More complex orchestration can come later.

---

# 20. Relationship between EventBus and hardware compilation

The EventBus is **infrastructure**, not the mechanical compiler itself.

A future compilation pipeline might emit:

```text
BUILD_STARTED
        ↓
MACHINE_RESOLVING
        ↓
COMPONENT_RESOLVED
        ↓
INTERFACES_RESOLVED
        ↓
CONSTRAINTS_VALIDATED
        ↓
GEOMETRY_GENERATED
        ↓
EXPORT_STARTED
        ↓
EXPORT_FINISHED
        ↓
BUILD_FINISHED
```

Plugins/modules can subscribe to these events.

For example:

```text
Logger
    → all lifecycle events

Metrics
    → compilation events

OpenSCADExporter
    → geometry-ready event

DocumentationExporter
    → build-finished event
```

This lets Atlas add capabilities without hardcoding them into the compiler.

---

# 21. Important distinction: compiler pipeline vs event system

Do not confuse:

```text
Compiler
```

with:

```text
EventBus
```

The Compiler determines the **actual compilation process**.

The EventBus provides a mechanism for **communication and extension** around that process.

Think:

```text
Compiler
    ├── performs deterministic work
    └── emits lifecycle events

EventBus
    └── dispatches those events
```

This distinction will become important as Atlas grows.

---

# 22. Registries

Atlas will likely eventually contain multiple specialized registries.

Examples:

```text
ListenerRegistry
ComponentRegistry
ExporterRegistry
ConstraintRegistry
PluginRegistry
```

Each registry should have one responsibility.

Examples:

```text
ListenerRegistry
    EventType → Subscriptions

ComponentRegistry
    ComponentType → Component implementation

ExporterRegistry
    Format → Exporter implementation

PluginRegistry
    Plugin name/type → Plugin
```

The registry pattern is therefore part of the framework's extensibility strategy.

---

# 23. Mechanical Intermediate Representation

A future major architectural milestone is the Mechanical IR.

The goal is to avoid coupling the machine model directly to CAD output.

Potential structure:

```text
Machine IR
│
├── Components
├── Interfaces
├── Dimensions
├── Coordinate systems
├── Mounting points
├── Constraints
├── Materials
├── Fasteners
└── Assemblies
```

Then:

```text
Machine Configuration
        ↓
Machine Model
        ↓
Mechanical IR
        ↓
Exporter
```

Different exporters consume the same IR:

```text
Mechanical IR
      │
      ├── OpenSCAD
      ├── STEP
      ├── STL
      ├── BOM
      └── Documentation
```

This is one of the most important long-term design goals.

---

# 24. Desired configuration philosophy

Configurations should describe **intent**, not implementation trivia.

Prefer:

```yaml
workspace:
  x: 400
  y: 400
  z: 500

motion:
  architecture: corexy

frame:
  architecture: boxed_tower

rails:
  type: mgn12
```

over:

```yaml
bolt_1:
  x: ...
  y: ...
  size: M5

bolt_2:
  x: ...
  y: ...
  size: M5
```

The compiler should derive lower-level implementation details.

This directly supports the original idea:

> Users should be able to change a component or configuration without manually updating every dependent bolt/coordinate.

---

# 25. Original physical design direction

The first hardware experiment is a CoreXY architecture with:

```text
Upper frame: approximately 560 × 560 mm
Lower bed:   approximately 400 × 400 mm
```

The upper section is deliberately larger than the lower section.

The purpose is to provide enough XY travel for the toolhead to cover the entire 400 × 400 workspace.

The frame design direction evolved toward:

```text
Closed boxed towers
    ↓
Two vertical extrusions per corner
    ↓
Horizontal spacers/bracing
    ↓
Torsion-resistant structure
    ↓
Mounting surfaces for future linear rails
```

The design is intended to feel more like an industrial machine than a simple hobby frame.

Future physical concepts include:

- MGN12 Z rails
- oversized/moving CoreXY gantry
- boxed tower corners
- modular bracing
- offset bridge modules
- parametric OpenSCAD generation

---

# 26. Software-to-hardware mapping

The framework should eventually make a useful analogy:

```text
Software

Interface
Implementation
Dependency
Registry
Compiler
Plugin
Event
```

maps conceptually to:

```text
Hardware

Mechanical interface
Component
Connection
Component registry
Hardware compiler
Hardware plugin
Physical lifecycle/event
```

For example:

```text
MotionSystem
    interface

CoreXY
    implementation

Cartesian
    implementation
```

The compiler can consume either implementation.

Likewise:

```text
RailInterface
    interface

MGN12
    implementation

MGW15
    implementation
```

The goal is to let the framework reason about compatibility rather than hardcoding every combination.

---

# 27. Sprint 1 current goal

Sprint 1 is primarily about proving the software architecture.

The target is a minimal working Observer/EventBus system:

```text
Event
  ↓
EventBus.emit()
  ↓
ListenerRegistry
  ↓
Subscription
  ↓
Listener action
```

A minimal demonstration should prove:

1. A module can subscribe to an EventType.
2. Multiple modules can subscribe to the same EventType.
3. An Event can be emitted.
4. The EventBus finds the correct subscriptions.
5. The associated actions are called.
6. The Event is passed into the action.
7. An action can optionally emit another Event.
8. The Compiler does not need to know which listeners exist.

Once this works, the Observer portion of Sprint 1 is effectively complete.

---

# 28. Sprint 1 intentionally postponed

Do not solve these yet:

```text
Async dispatch
Parallel listeners
Message queues
Distributed events
Retries
Event persistence
Event replay
Complex failure recovery
Plugin discovery
CAD generation
Mechanical IR
Constraint solver
```

First prove the smallest useful architecture.

---

# 29. Current implementation state

Already established/implemented/experimented with:

```text
Typer CLI
Rich output
Application
Compiler
Event
EventType
Listener
ListenerRegistry
EventBus
Subscription
```

The user has successfully moved from thinking:

```text
"EventBus is a streaming loop"
```

to the more accurate model:

```text
EventBus
    ↓
dispatches
    ↓
subscriptions
    ↓
actions
```

The important current insight is:

> A ListenerRegistry should store **subscriptions**, not actual events that happened.

An Event is a runtime fact.

A Subscription is a declaration of interest.

---

# 30. Current project philosophy

Atlas is being developed as a software-engineering experiment as much as a mechanical project.

The architecture is intentionally exploring:

- Observer pattern
- Event-driven architecture
- Dependency Injection
- Composition Root
- Registry pattern
- Plugin architecture
- Interfaces
- Separation of Concerns
- Inversion of Control
- Intermediate representations
- Compiler architecture
- Constraint-based hardware design
- Extensible exporters

The goal is not to prematurely build the final system.

The goal is to establish **good abstractions that can survive the system becoming much larger**.

---

# 31. Current mental model to preserve

The most important mental model reached so far is:

```text
                        ATLAS
                          │
                 Machine Definition
                          │
                          ▼
                      Compiler
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
        Registries                  EventBus
             │                         │
             ▼                         ▼
       Components                 Lifecycle events
       Exporters                 Extensions
       Constraints               Plugins
             │                         │
             └────────────┬────────────┘
                          ▼
                   Mechanical IR
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
          OpenSCAD       STEP        BOM
```

And for the event subsystem:

```text
Event
  │
  │ emit
  ▼
EventBus
  │
  │ lookup
  ▼
ListenerRegistry
  │
  ▼
Subscription
  │
  │ action(event)
  ▼
Listener / Module
  │
  │ optional emit
  ▼
New Event
```

The fundamental Atlas principle is:

> **Describe the machine at a high level, resolve its mechanical relationships through interfaces and constraints, produce a normalized machine representation, and let interchangeable backends generate concrete artifacts.**

The CoreXY printer is the first machine used to prove that architecture.

# Sprint 1 — Status: Complete

All 8 original success criteria are proven by tests in
src/atlas/tests/test_sprint1.py (10 tests total, 8 mapping directly
to the criteria, 2 additional: type-only subscription matching, and
an Atlas end-to-end smoke test).

Real API (as implemented, differs slightly from early sketches):

    Subscription(event: Event, callback: Callable, id: str)
    EventBus(registry: ListenerRegistry)
    EventBus.publish(event: Event)   # not .emit()
    ListenerRegistry.get_subscribers(event_type) -> dict_values[Subscription]

Compiler(event_bus: EventBus) — publishes COMPILE_START only so far.
END_BUILD is stubbed but commented out, not yet implemented.

Atlas is the composition root (matches the doc's "Application"
concept from Section 30) — it owns Compiler, Logger, ModuleA, ModuleB,
and does the wiring the Compiler itself must not do.
