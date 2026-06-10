# Complete KGDB graph runtime slice

ID: task-complete-kgdb-graph-runtime-slice
Status: deferred
Priority: high

## Goal

Make KGDB graph build, query, missing checks, and traceability stable enough for routine deskops use.

## Scope

- authoritative graph output paths
- KG snapshot and NetworkX runtime compatibility
- relation serialization
- `graph trace` or equivalent atom/file query surface
- snapshot validation against KGDB contracts

## Done When

- Users can query atom/file/doc/test relationships without reading raw graph JSON.
