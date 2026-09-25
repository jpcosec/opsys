# Drawer Board

This board routes deferred work only.

## Layout

- `use-cases/` — 15 use-case narratives covering the CLI surfaces
- `stress-tests/` — 15 scripted UX tests, with every finding archived in
  `stress-tests/findings-archive.md`; what is left to fix is tracked in
  `issues/issue-stress-test-fix-backlog.md`
- `issues/` — 25 files: open work, closed and routed entries kept for the record, and
  `diagnosis-archive.md`, the 2026-08 architectural diagnosis whose durable part is
  now six atoms
- `questions/` — decisions that block implementation, with their status
- `features/` — six deferred design documents:
  - `workflow-execution-engine.md` — hooks, state machines, condition evaluators, gated pipeline
  - `feature-runtime-and-launcher.md` — how a task reaches an agent: tmux launcher, Herdr runtime, semantic execution adapter
  - `feature-agent-role-models.md` — the router/supervisor/executor models, now mostly RoleDocs
  - `feature-materialization-pipeline.md` — documents from atoms, artifacts for agents
  - `master-plan-deskops-knowledge-decouple-and-execution-runtime.md` — annotated: written against kgdb, which is gone
  - `feature-sldb-ui-surface-inspection.md` — routed elsewhere (sldb/spec2viz)
- `attention/` — empty; reviewed on 2026-09-24
- `rituals/` — the drawer triage and knowledge distillation passes


## Tasks

Deferred task backlog:

- `task-adhoc-subagent-launcher-tmux-multi-cli` — deskops launch: tmux + codex/agy/pi, sldb-compiled per-role context, tool limits by profile, disk-persisted output, deskops-mediated signals (ambiguities resolved; ready to promote)
- `task-doctor-crashes-on-deskless-roots` — doctor raises UnboundLocalError on roots without `desk/`; initialize finding variables on every code path (found during cold review of task-doctor-proposes-missing-model-registration)

Promoted to active desk tasks:

- `task-improve-cli-help-progressive-disclosure`
- `task-write-human-quickstart-guide`
- `task-unify-repository-registration-surface`
- `task-add-why-rationale-fields`
- `task-add-artifact-edit-command`
- `task-unblock-advance-implementation-path`
- `task-formalize-pill-taxonomy`
- `task-doctor-proposes-missing-model-registration`
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
- `task-bind-next-phase-pills-to-active-tasks`
- `task-prefer-implicit-local-desk-examples`

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

## Imports from paper_IEEE

Items imported from `paper_IEEE/desk/` on 2026-06-22, filtered for deskops relevance. The sender project is `paper_IEEE`.

### Attention (desk/drawer/attention/)

Items triaged into `desk/drawer/attention/` for human review before promotion:

- `20260621-034212-suggestion-clarify-atoms-vs-pills-and-knowledge-flow-in-deskops-docs.md` — epistemic flow documentation gap (overlaps drawer issue)
- `20260621-034342-unclear-clarify-inbox-model-for-inter-project-communication.md` — inter-project inbox model (overlaps drawer issue)
- `20260621-113406-note-tmux-usage-for-development-and-testing-only.md` — tmux boundary: external orchestration only, not runtime logic
- `20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md` — closeout gate: commit boundary required before retirement
- `20260621-160450-note-workflow-summary-so-far.md` — comprehensive workflow model documentation
- `20260621-160930-note-current-workflow-invariants.md` — 13 concise workflow invariants
- `20260621-164028-note-subagent-ready-task-standard-checklist.md` — 100% subagent-ready task checklist (13 sections)

### Features (desk/drawer/features/)

- `router.md`, `supervisor.md`, `executor.md` — agent role model files (overlaps drawer issue)

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

Reviewed 2026-09-24: the issue set was folded from 40 files to 24, the attention
pile was emptied, and the stress-test findings were archived into one file. See
the review notes in `attention/README.md` and the commit history for the merge
map. `issue-session-20260910-handoff-uncommitted-work-and-open-items.md` and
`issue-deskops-init-spawns-one-process-per-model.md` are both resolved.
