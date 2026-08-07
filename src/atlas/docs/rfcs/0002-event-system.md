# RFC 0002 - Event System

Status: Draft

## Summary

Atlas uses an event-driven architecture.

Modules communicate through events rather than direct references.

## Motivation

This reduces coupling and enables plugins.

Instead of

Machine → Logger

Machine → Exporter

Machine → GUI

Atlas does

Machine

↓

emit(Event)

↓

Subscribers

## Initial Events

- CompilerStarted
- CompilerFinished
- MachineLoaded
- ModuleAdded
- ModuleValidated
- InterfacesResolved
- IRGenerated
- ExportStarted
- ExportFinished

## Benefits

- Loose coupling
- Plugin friendly
- Easier testing
- Better logging
- Easier debugging