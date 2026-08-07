# RFC 0004 - Mechanical Intermediate Representation

Status: Draft

## Summary

Mechanical IR (MIR) is the internal representation used by Atlas.

Every exporter consumes MIR.

No exporter receives Module objects directly.

## Example

Machine

↓

Module

↓

Mechanical IR

↓

Exporter

## Goals

- CAD independent
- Serializable
- Easy to inspect
- Easy to validate
- Backend agnostic

## Typical Nodes

- Extrusion
- Plate
- Rail
- Motor
- Pulley
- Hole Pattern
- Coordinate System
- Interface Marker