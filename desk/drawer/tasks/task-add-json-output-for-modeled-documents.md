# Add JSON output for modeled documents

ID: task-add-json-output-for-modeled-documents
Status: deferred
Priority: medium

## Goal

Make modeled document `list` and `show` commands scriptable with JSON output.

## Scope

- `deskops list ... --format json`
- `deskops show ... --format json`
- modeled artifacts, tasks, routines, and primitives

## Done When

- Parser accepts `--format text|json|yaml` consistently for list and show surfaces.
- JSON serialization works for modeled payloads.
- Existing text output remains the default.
- Tests parse JSON output with `json.loads`.
