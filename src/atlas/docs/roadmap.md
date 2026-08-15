# Atlas Roadmap

> **Vision:** Atlas is a mechanical compiler that transforms engineering intent into manufacturable machines.

---

# Current Status

**Version:** 0.1.0-alpha.1

Current milestone:

* Project initialized
* CLI established
* Documentation created
* Compiler architecture defined

---

# Milestone 0 — Compiler Kernel

**Goal:** Build the foundation of Atlas.

## Features

* [x] UV project
* [x] Typer CLI
* [x] Rich console
* [x] README
* [x] Manifesto
* [x] RFC system
* [x] Changelog
* [x] Contributing guide
* [x] MIT License

## Deliverable

```bash
atlas doctor
atlas version
```

---

# Milestone 1 — Atlas Core

**Goal:** Build the compiler kernel.

## Components

* [ ] Event Bus
* [ ] Service Container
* [ ] Registry
* [ ] Machine
* [ ] Module
* [ ] Interface
* [ ] Compiler Context

## Deliverable

```python
machine = Machine("Demo")

machine.build()
```

---

# Milestone 2 — Mechanical IR (MIR)

**Goal:** Create the internal engineering language.

## Geometry Nodes

* [ ] Extrusion
* [ ] Plate
* [ ] Hole Pattern
* [ ] Rail
* [ ] Motor
* [ ] Pulley
* [ ] Interface Marker
* [ ] Transform

## Deliverable

```bash
atlas inspect mir
```

---

# Milestone 3 — Scene Graph

**Goal:** Build a complete geometry graph.

## Features

* [ ] Hierarchy
* [ ] Transform propagation
* [ ] Metadata
* [ ] Bounding boxes

## Deliverable

Visual scene inspection.

---

# Milestone 4 — Export System

**Goal:** Generate real outputs.

## Exporters

* [ ] OpenSCAD
* [ ] STEP (CadQuery)
* [ ] STL Preview
* [ ] JSON MIR

## Deliverable

```bash
atlas export openscad
```

---

# Milestone 5 — Module SDK

**Goal:** Allow external machine modules.

## Features

* [ ] Plugin discovery
* [ ] Version compatibility
* [ ] Dependency resolution
* [ ] Module metadata

---

# Milestone 6 — Hello Atlas

**Goal:** Generate the first mechanical object.

Generate one extrusion.

Then:

* two extrusions
* rectangular frame
* boxed frame

No printer yet.

---

# Milestone 7 — Falcon

**Goal:** First complete machine.

Modules:

* Base
* Towers
* Structural Nodes
* Torsion Ring
* CoreXY Motion
* Z System

---

# Milestone 8 — Constraint Solver

Compiler validates:

* collisions
* interface compatibility
* rail spacing
* belt routing
* structural constraints

---

# Milestone 9 — Engineering Platform

Atlas supports multiple machine families.

Examples:

* Falcon (CoreXY)
* Raven (IDEX)
* Hawk (Laser)
* Lynx (CNC)
* Custom machines

---

# Long-Term Vision

Atlas should compile:

* Mechanical Geometry
* STEP Models
* OpenSCAD
* BOM
* Wiring Harness
* Firmware Configuration
* Assembly Documentation

from a single machine definition.

---

# Guiding Principles

* Engineering first
* Interfaces over implementations
* Composition over inheritance
* Backend independence
* Deterministic builds
* Plugin-oriented architecture
* Machine agnostic

---

# Motto

> Design the engineering once. Generate the machine everywhere.
