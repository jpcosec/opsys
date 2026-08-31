---
id: task-establish-horizontal-desk-discovery-and-canonical-identity
status: active
references: []
depends_on: []
pills:
- desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md
- desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md
files: []
routine: routine-task-establish-horizontal-desk-discovery-and-canonical-identity
checklists:
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-execution-ready
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-testing-ready
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-closeout-ready
current_node: checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Establish horizontal desk discovery and canonical identity

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make desks discoverable to each other through one canonical per-project identity path, so cross-repo workflow commands can resolve sibling desks without ambiguous local heuristics.

## Scope

_State what is in scope and what is out of scope._

- define the minimal per-project desk identity contract
- decide how local desk identity relates to SLDB-backed ecosystem registration
- make repo self-discovery answer "who am I?" reliably at the current root
- make sibling desk discovery answer "where is that repo's desk?" reliably from canonical identity
- route duplicate-root and duplicate-id ambiguity into explicit failure instead of first-match guessing

## Resolved Decisions

Supervisor rulings:

- Canonical identity = `DeskConfig.project_identity`, which must equal `RepositoryDoc.id` for the registered repo (1:1). Sentinel `"unknown-project"` means "not established".
- Authority on conflict: if config identity and registry-derived identity disagree, FAIL loudly (do not pick one silently).
- Failure channel: raise `SLDBStoreError` / non-zero exit with an explicit duplicate/ambiguity message. No `--strict` flag.
- New command: `deskops repo whoami` prints canonical id or fails if unset/ambiguous.
- Shared resolver: add `deskops/identity.py` with load-registry -> match-by-id -> match-by-root -> detect-duplicates; consumed by inbox.py, repo.py, whoami.
- Registration guard: `repo register` rejects when id OR resolved root already maps to another entry.
- Config identity fields themselves are owned by the per-project-config task; this task only CONSUMES them. Legacy migration of `"unknown-project"` desks is OUT (owned by legacy-migrate task).

## Implementation Path

_Outline the expected implementation route or affected surface._

Add deskops/identity.py shared resolver; wire repo whoami in parser/main/repo.py; make inbox.py resolution fail-on-duplicate; guard repo register. Tests in tests/test_repo_identity.py.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
