# Drawer Board

This board routes deferred work only.

## Features

- `desk/drawer/use-cases/` — 15 use-case narratives covering all CLI surfaces
- `desk/drawer/stress-tests/` — 15 UX stress-tests derived from use-cases
- `desk/drawer/features/semantic-execution-adapter.md` — deferred adapter architecture for semantic execution via external agent platforms

## Tasks

Deferred task backlog:

- `task-bind-next-phase-pills-to-active-tasks`

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
- `task-add-desk-health-and-recovery-surface-deskops-slice`
- `task-add-drift-check-review-loop`
- `task-add-json-output-for-modeled-documents`
- `task-add-per-project-desk-config-and-version-contract`
- `task-define-atom-lifecycle-operations`
- `task-define-materialization-contract-slice-deskops-surface`
- `task-design-operational-cli-grammar`
- `task-detect-and-migrate-legacy-desk-workspaces`
- `task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout`
- `task-establish-horizontal-desk-discovery-and-canonical-identity`
- `task-make-cross-desk-inbox-delivery-verifiable-and-actionable`
- `task-make-list-behavior-data-integrity-safe`
- `task-make-task-lifecycle-runnable-from-intake-to-closeout`
- `task-wire-closeout-to-knowledge-gates`
- `task-write-end-to-end-deskops-operator-manual`
- `task-formalize-phase-layer-workflow`
- `task-conciliate-active-pills-for-reuse-and-next-phase`

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
- `desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md`
- `desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md`

## Rituals

- `desk/drawer/rituals/triage.md`
- `desk/drawer/rituals/knowledge-distillation-pass.md`

## Notes

Promote work from `desk/drawer/` into the active surfaces of `desk/` before implementation starts.

The current deferred board has been atomized at the guardrail level: config/version policy, horizontal desk identity, cross-desk inbox delivery, list integrity, machine-readable output contracts, materialization contracts, atom lifecycle provenance, drift review, desk health boundaries, CLI grammar, closeout knowledge gates, and manual sequencing now each have explicit pills.

All currently routed drawer tasks have been promoted into active desk task bundles. New repo-local work should enter the drawer first before the next promotion wave.
