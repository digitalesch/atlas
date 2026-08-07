# RFC 0003 - Module API

Status: Draft

## Summary

Everything in Atlas is a Module.

A printer is a collection of modules.

A CNC is a collection of modules.

A laser cutter is a collection of modules.

## Lifecycle

Configure

↓

Validate

↓

Resolve Interfaces

↓

Generate IR

↓

Export

## Responsibilities

Modules should:

- declare interfaces
- declare constraints
- generate Mechanical IR

Modules should not:

- generate OpenSCAD
- generate STEP
- write files
- communicate directly with other modules

## Design Principles

- Composition over inheritance
- Explicit interfaces
- Stateless where possible
- Deterministic outputs