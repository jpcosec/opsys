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

## Suggested Pills

- `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`
- `desk/contexts/pill-002-test-real-cli-surfaces.md`
- `desk/contexts/pill-012-deskops-cli-artifact-contract.md`
