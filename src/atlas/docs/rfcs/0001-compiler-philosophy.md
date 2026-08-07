# RFC 0001 - Atlas Compiler Philosophy

Status: Accepted

## Summary

Atlas is a mechanical compiler, not a CAD application.

The purpose of Atlas is to transform a machine definition into one or more outputs such as:

- OpenSCAD
- STEP
- STL
- BOM
- Wiring
- Firmware configuration
- Documentation

Geometry is an output, not the source of truth.

## Goals

- Backend independent
- Modular
- Interface driven
- Extensible
- Machine agnostic

## Non-goals

Atlas is not:

- a slicer
- a CAD editor
- a firmware
- a simulation package

Those can integrate with Atlas but are not part of its core.

## Architecture

Machine Definition

↓

Compiler

↓

Mechanical IR

↓

Exporters

## Rationale

Separating engineering from geometry allows Atlas to support multiple CAD backends and machine types without changing the compiler core.