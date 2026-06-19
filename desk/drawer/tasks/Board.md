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
- `task-wire-closeout-knowledge-gates`
- `task-define-materialization-contract-slice` (deskops surface only)
- `task-add-drift-check-review-loop`
- `task-design-operational-cli-grammar`
- `task-add-desk-health-and-recovery-surface` (deskops slice only)
- `task-define-atom-lifecycle-operations`
- `task-write-end-to-end-operator-manual`
- `task-establish-horizontal-desk-discovery-and-identity`
- `task-make-cross-desk-inbox-delivery-verifiable`
- `task-add-per-project-desk-config-and-version-contract`
- `task-detect-and-migrate-legacy-desk-workspaces`

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
- `task-make-task-lifecycle-runnable-end-to-end` → atomized as active child tasks

## Pills

- `desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md`
- `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md`
- `desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md`
- `desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md`
- `desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md`
- `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`
- `desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md`
- `desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md`
- `desk/contexts/pill-drift-checks-are-review-surfaces-not-mutators.md`
- `desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md`
- `desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md`
- `desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md`
- `desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md`

## Rituals

- `desk/drawer/rituals/triage.md`
- `desk/drawer/rituals/knowledge-distillation-pass.md`

## Notes

Promote work from `desk/drawer/` into the active surfaces of `desk/` before implementation starts.

The current deferred board has been atomized at the guardrail level: config/version policy, horizontal desk identity, cross-desk inbox delivery, list integrity, machine-readable output contracts, materialization contracts, atom lifecycle provenance, drift review, desk health boundaries, CLI grammar, closeout knowledge gates, and manual sequencing now each have explicit pills.
