# Drawer Board

This board routes deferred work only.

## Features

- `desk/drawer/use-cases/` — 15 use-case narratives covering all CLI surfaces
- `desk/drawer/stress-tests/` — 15 UX stress-tests derived from use-cases
- `desk/drawer/features/semantic-execution-adapter.md` — deferred adapter architecture for semantic execution via external agent platforms

## Tasks

Deferred task backlog:

- `task-make-list-behavior-data-integrity-safe`
- `task-add-json-output-for-modeled-documents`
- `task-make-task-lifecycle-runnable-end-to-end`
- `task-wire-closeout-knowledge-gates`
- `task-define-materialization-contract-slice` (deskops surface only)
- `task-add-drift-check-review-loop`
- `task-design-operational-cli-grammar`
- `task-add-desk-health-and-recovery-surface` (deskops slice only)
- `task-define-atom-lifecycle-operations`
- `task-write-end-to-end-operator-manual`

Promoted to active desk tasks:

- `task-improve-cli-help-progressive-disclosure`
- `task-write-human-quickstart-guide`
- `task-unify-repository-registration-surface`
- `task-add-why-rationale-fields`
- `task-add-artifact-edit-command`
- `task-unblock-advance-implementation-path`
- `task-formalize-pill-taxonomy`
- `task-consume-repo-local-desk-tasks`
- `task-add-next-action-workflow-state-command`

## Routed to sibling repos

SLDB inbox (`tools/sldb/desk/inbox/`):
- `20260614-000000` — stabilize `stores init` failure handling
- `20260614-000001` — stabilize `models add` error output
- `20260614-000002` — add store health-check API
- `20260614-000003` — add model registration query API

KGDB inbox (`tools/kgdb/desk/inbox/`):
- `20260614-000000` — stabilize graph snapshot validation
- `20260614-000001` — stabilize relation serialization
- `20260614-000002` — add graph trace query surface

Removed from this drawer (moved out):
- `task-stabilize-init-local-store-failures` → atomized as SLDB inbox items above
- `task-complete-kgdb-graph-runtime-slice` → atomized as KGDB inbox items above

## Pills

*No active drawer pills.*

## Rituals

- `desk/drawer/rituals/triage.md`
- `desk/drawer/rituals/knowledge-distillation-pass.md`

## Notes

Promote work from `desk/drawer/` into the active surfaces of `desk/` before implementation starts.
