# Stabilize first-use CLI and data-integrity path

ID: task-stabilize-first-use-cli-data-integrity
Status: deferred
Priority: high

## Goal

Make first-use deskops commands trustworthy enough for normal workflow adoption.

## Scope

- `deskops init` model registration and local store setup
- exact-match `show` behavior across nested artifact directories
- robust `list` behavior
- invalid YAML and partial-write rollback behavior
- user-safe error output
- JSON serialization for modeled documents

## Done When

- First-use commands can be exercised from a fresh repo without corrupting `desk/` or `.sldb/`.
- Failures leave no orphaned partial artifacts.
- Relevant CLI regression tests pass.
