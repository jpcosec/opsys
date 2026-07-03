# Task traceability for diagnosis tree

This note maps the diagnosis atoms under `desk/drawer/issues/diagnosis/` back to active tasks and identifies task themes that still suggest missing diagnosis coverage.

## Diagnosis atoms supported by active tasks

| Diagnosis atom | Related active tasks |
|---|---|
| `atom-diagnosis-deskops-subutilizes-sldb` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-define-materialization-contract-slice-deskops-surface`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-reading-atoms-through-markdown-bypasses-sldb-composition` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-drift-check-review-loop` |
| `atom-deskops-still-operates-too-directly-on-files` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-define-materialization-contract-slice-deskops-surface`, `task-design-operational-cli-grammar` |
| `atom-hooks-are-modeled-but-not-a-general-runtime` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-wire-closeout-to-knowledge-gates` |
| `atom-tasks-are-not-yet-atomized-to-execution-actions` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-frontmatter-becomes-reading-noise-when-sldb-is-underused` | `task-define-materialization-contract-slice-deskops-surface`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-documentation-growth-compensates-for-weak-semantic-access` | `task-write-end-to-end-deskops-operator-manual`, `task-add-drift-check-review-loop`, `task-design-operational-cli-grammar` |
| `atom-deskops-should-read-through-sldb-compositions` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents` |
| `atom-materializations-are-projections-not-primary-read-surfaces` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-drift-check-review-loop`, `task-wire-closeout-to-knowledge-gates` |
| `atom-tasks-should-compile-to-execution-compositions` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-gap-between-current-file-reading-and-composed-reading` | `task-define-materialization-contract-slice-deskops-surface`, `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-add-drift-check-review-loop` |
| `atom-workline-introduce-deskops-compose-operations` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents`, `task-design-operational-cli-grammar` |
| `atom-workline-activate-a-general-hook-runtime` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-wire-closeout-to-knowledge-gates`, `task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout` |
| `atom-workline-add-execution-plan-to-task-model` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-use-case-read-atom-without-reading-full-markdown` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents` |
| `atom-use-case-auto-dispatch-executor-on-execution-ready` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-wire-closeout-to-knowledge-gates` |
| `atom-hook-automation-can-be-powerful-but-opaque` | `task-wire-closeout-to-knowledge-gates`, `task-make-task-lifecycle-runnable-from-intake-to-closeout` |
| `atom-over-atomized-tasks-can-fragment-coherent-work` | `task-make-task-lifecycle-runnable-from-intake-to-closeout`, `task-write-end-to-end-deskops-operator-manual` |
| `atom-criterion-deskops-uses-sldb-as-primary-read-path` | `task-define-materialization-contract-slice-deskops-surface`, `task-add-json-output-for-modeled-documents`, `task-design-operational-cli-grammar` |

## Active tasks that suggest diagnosis themes not yet captured in this tree

These active tasks point to additional diagnosis lines that are either missing or only weakly implied by the current diagnosis atoms.

### 1. Desk health, recovery, and migration surfaces

Related tasks:

- `task-add-desk-health-and-recovery-surface-deskops-slice`
- `task-detect-and-migrate-legacy-desk-workspaces`
- `task-add-per-project-desk-config-and-version-contract`

Likely missing diagnosis themes:

- deskops lacks a strong diagnosis model for workspace health and recoverability
- the current workspace contract is still fragile across legacy desks, stale runtime state, and mixed-version surfaces
- per-project desk identity/config/version rules are not yet explicit enough to support safe recovery and migration

### 2. Cross-desk identity and transport diagnosis

Related tasks:

- `task-establish-horizontal-desk-discovery-and-canonical-identity`
- `task-make-cross-desk-inbox-delivery-verifiable-and-actionable`

Likely missing diagnosis themes:

- horizontal desk identity is not yet canonical enough for reliable cross-repo operations
- cross-desk delivery and acknowledgment are not yet modeled as a trustworthy operational transport
- deskops still lacks a clean diagnosis subtree for multi-repo coordination contracts

### 3. CLI surface and scriptability diagnosis

Related tasks:

- `task-design-operational-cli-grammar`
- `task-add-json-output-for-modeled-documents`

Likely missing diagnosis themes:

- the current CLI surface still exposes internal architecture too directly instead of a spoken workflow language
- modeled document output is not yet shaped enough for scriptable and composable machine use
- compose/query-first deskops usage may require a broader diagnosis about command surface design, not only about SLDB reading path

### 4. Atom lifecycle and provenance diagnosis beyond reading path

Related tasks:

- `task-define-atom-lifecycle-operations`
- `task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout`
- `task-wire-closeout-to-knowledge-gates`

Likely missing diagnosis themes:

- atom lifecycle operations still need a more explicit diagnosis around provenance preservation, mutation safety, and reversible atom evolution
- closeout knowledge gates imply a broader diagnosis about how durable knowledge mutates under workflow pressure, not just how it is read

### 5. Drift review as its own diagnosis line

Related tasks:

- `task-add-drift-check-review-loop`

Likely missing diagnosis themes:

- the system lacks a unified diagnosis of multi-surface drift across atoms, materializations, tests, diagrams, and implementation
- drift is currently present in the tree as a symptom, but not yet as a first-class diagnosis/workline cluster

## Interpretation

The current diagnosis tree explains the SLDB-composition, hook-runtime, and execution-composition direction fairly well. But the active board also suggests at least five additional diagnosis families:

1. workspace health and migration
2. cross-desk identity and transport
3. CLI grammar and machine-readable output
4. atom lifecycle mutation and provenance
5. drift detection and reconciliation

Those can either become new diagnosis subtrees or be attached to the current tree through additional atoms if this issue is meant to stay broader.

## Follow-up status

These missing diagnosis families have now been scaffolded under:

- `10-workspace-health/`
- `11-cross-desk-identity/`
- `12-cli-surface/`
- `13-atom-mutation-provenance/`
- `14-drift/`
