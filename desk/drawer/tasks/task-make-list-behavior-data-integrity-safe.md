# Make list behavior data-integrity-safe

ID: task-make-list-behavior-data-integrity-safe
Status: deferred
Priority: high

## Goal

Ensure `deskops list` commands do not silently hide malformed workflow documents.

## Scope

- `deskops list tasks`
- `deskops list routines`
- `deskops list <artifacts>`
- `deskops list <primitives>`
- invalid frontmatter and malformed model payloads

## Done When

- Missing desk roots still produce helpful first-use guidance.
- Empty initialized sections list cleanly.
- Malformed documents are reported clearly instead of silently skipped.
- Regression tests cover malformed docs in listed directories.

## Suggested Pills

- `desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md`
- `desk/contexts/pill-002-test-real-cli-surfaces.md`
- `desk/contexts/pill-012-deskops-cli-artifact-contract.md`
