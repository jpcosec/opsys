# Make role prompts sldb-tracked RoleDocs with pi-agent materialization

ID: task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization
Status: deferred
Priority: high

## Anchoring Atom

- `desk/atoms/atom-role-prompts-are-tracked-documents-agent-files-are-materializations.md`

## Rationale

Role prompts (supervisor, executor, tester) live as loose markdown in `docs/agent-system-prompts/` while `~/.pi/agent/agents/` holds hand-made copies that already drifted: the installed `deskops-supervisor` agent lost the role-lock check, dispatch guidance, evidence expectations, and closeout checklist sections present in the repo source.

## Goal

Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Scope

- add `RoleDoc` model in `deskops/models/role.py` and register it in the store index
- move canonical role sources to `desk/roles/` as tracked RoleDocs
- implement the deferred `deskops materialize` surface for pi agent targets (renders RoleDoc + pi frontmatter into `~/.pi/agent/agents/deskops-*.md`)
- extend `deskops drift check` to compare renders vs installed agent files
- regenerate the three deskops role agents from the tracked sources
- relate each role doc to its agent file with the `materializes` edge role

## Non-goals

- redefining role contents beyond restoring parity with `docs/agent-system-prompts/`
- the broader atom review referenced by the operator (scheduled separately)

## Done When

- editing a tracked RoleDoc and running `deskops materialize` updates `~/.pi/agent/agents/deskops-*.md`
- `deskops drift check` flags manual edits to installed agent files
- no role content is edited outside the store

## Validation

- `pytest`
- `deskops materialize --root .`
- `deskops drift check --root .`
