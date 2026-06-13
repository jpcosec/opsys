# Stabilize show selector behavior

ID: task-stabilize-show-selector-behavior
Status: deferred
Priority: high

## Goal

Make `deskops show` deterministic and safe across nested artifact directories.

## Scope

- exact filename and stem matching
- nested artifact directories, especially atoms
- prefix fallback behavior
- duplicate and ambiguous matches

## Done When

- Exact matches win over prefix matches.
- Nested exact matches work deterministically.
- Ambiguous matches return a clear error instead of silently choosing one file.
- Tests cover root exact, nested exact, prefix fallback, and duplicate nested exact matches.
