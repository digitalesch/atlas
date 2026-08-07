# Contributing to Atlas

First of all, thank you for taking the time to contribute.

Atlas is not just another CAD project. It is an attempt to build a reusable engineering framework capable of describing and generating entire classes of mechanical systems.

Our goal is to prioritize architecture, maintainability, and engineering principles over rapid feature development.

---

# Core Principles

## 1. Engineering First

Atlas models engineering concepts before geometry.

Good:

Machine → Module → Mechanical IR → Exporter

Avoid:

Machine → OpenSCAD

---

## 2. Interfaces Over Implementations

Modules communicate through well-defined interfaces.

A module should never depend on another module's implementation details.

---

## 3. Composition Over Inheritance

Whenever possible, build larger systems by composing smaller modules rather than creating deep inheritance hierarchies.

---

## 4. Backend Independence

Atlas Core must never depend on a specific CAD backend.

The following are considered plugins:

- OpenSCAD
- CadQuery
- STEP Exporter
- STL Exporter
- BOM Generator

---

## 5. Small, Focused Changes

Each pull request should introduce one concept.

Examples:

- Event Bus
- Registry
- Mechanical IR
- Module API

Avoid introducing multiple architectural ideas in a single change.

---

## 6. Document Architectural Decisions

Significant architectural changes should be accompanied by an RFC under:

docs/rfcs/

---

# Code Style

- Use type hints.
- Prefer dataclasses where appropriate.
- Keep functions small and focused.
- Avoid global state.
- Favor readability over cleverness.

---

# Testing

Every new feature should include tests whenever practical.

The compiler should remain deterministic.

Given the same machine definition, Atlas should always produce the same Mechanical IR.

---

# Project Vision

Atlas aims to become a mechanical compiler rather than a traditional CAD application.

Its responsibilities include:

- Defining machines
- Validating engineering constraints
- Resolving interfaces
- Generating Mechanical IR
- Exporting to multiple backends

Geometry is an output.

Engineering is the source of truth.

---

Thank you for helping build Atlas.