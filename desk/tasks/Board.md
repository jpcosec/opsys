---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual.md
- desk/tasks/task-closeout-commit-leaves-the-run-index-clean.md
- desk/tasks/task-closeout-commit-accepts-directory-paths.md
- desk/tasks/task-close-a-task-as-superseded.md
- desk/tasks/task-ritual-steps-are-prose.md
- desk/tasks/task-message-delivery-resolves-unregistered-desks.md
- desk/tasks/task-init-repairs-a-broken-owner-link.md
- desk/tasks/task-canonical-atom-reference-metadata.md
- desk/tasks/task-classify-cli-grammar.md
- desk/tasks/task-classify-large-docs-materialization.md
- desk/tasks/task-derived-atom-trace-index.md
- desk/tasks/task-detect-and-clean-task-policy-leaks.md
- desk/tasks/task-guard-component-diagram-projection.md
- desk/tasks/task-guard-extension-points.md
- desk/tasks/task-link-skill-surfaces-through-guard-tests.md
- desk/tasks/task-next-guidance-without-active-task.md
- desk/tasks/task-next-why-explanation.md
# List of pill-xxx paths
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._

- Make role prompts sldb-tracked RoleDocs with pi-agent materialization [active] - Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Task Details

_Generated from the task references above._

- Write end-to-end deskops operator manual [active] - Consolidate the methodology into one operational playbook after runnable slices are stable.
- `closeout commit` leaves the run index clean [draft] - After `deskops closeout commit` (both --run-dir and --no-run) the working tree is clean, and runs/subagents/index.jsonl still records the closing commit's hash.
- `closeout commit` accepts a directory in --paths that contains the closing task [draft] - `closeout commit --paths desk/tasks ...` closes a task that was never committed, and a task that was, with one commit and a clean tree.
- A task whose subject no longer exists closes as superseded, with a reason and a reference [draft] - `deskops closeout supersede --task <id> --reason <text> --ref <commit-or-path> --root <repo>` closes a task from any lifecycle node. It requires the reason and at least one resolvable ref: a commit that is HEAD or an ancestor, or an existing path. The task's status and history record `superseded`, and the commit trailers say so (`Closeout-Mode: superseded`, `Closeout-Reason`, `Closeout-Ref`). It removes the task from the Board in one commit, the same way the closeout commit does, and the run index line marks it as superseded.
- Ritual steps are prose items, not StepDoc references [draft] - RitualDoc.steps is plain text, `sldb edges unresolved --local` reports no RitualDoc.steps findings, desk/rituals/phase.md is tracked as RitualDoc:ritual-phase, and every store migrates through `desk update --apply`.
- `message send` and `message ack` work when the target desk does not register the sender or itself [draft] - A note can always be delivered and acknowledged. The sender identity comes from the sender's own desk config or registry, never from the target's registry. A target desk without project_identity takes its id from the directory name, with a warning. `ack` falls back to the repo's own desk config when a local registry does not list the repo itself.
- `deskops init` repairs a broken `deskops` store link instead of skipping it [draft] - `deskops init` and `bootstrap`, on a store whose `deskops` link is broken, re-point the link at the current owner store with `replace=True` and register the models. A healthy link to a different store is still left alone, with the warning.
- Canonical atom reference field and role vocabulary [draft] - Make `atoms` the only structured artifact field for atom references, validate the five allowed
roles, and report legacy aliases and invalid roles through `deskops drift check` without adding
a hard closeout gate.
- Classify the CLI grammar by workflow noun [draft] - Record one explicit top-level noun classification and enforce it with a test, without removing or
renaming any command.
- Declare composed materialization metadata for large docs [draft] - Encode the audited inventory: every composed document declares `atoms:` frontmatter with role
`documents`, and `deskops/data/faq.md` is enforced as a byte-identical projection of
`docs/faq.md`.
- Add a derived atom use-site index [draft] - Provide a read-only `atom_use_sites(root, atom_id)` helper that derives reverse traceability from
`extract_declared_edges`, plus a test proving that no atom document is mutated.
- Detect and clean global policy leaks in task files [draft] - Add a review-only `task-policy-leak` finding to `deskops drift check`, then remove the current
leak from the active task set without changing any global policy text.
- Guard the SLDB components diagram projection [draft] - Add a focused test that the rendered Markdown block equals the `.mmd` source for the components
diagram, and fix the block from the source if the test fails.
- Guard the declared deskops extension points [draft] - Add one test that proves the public extension registries agree with each other and that every CLI
handler resolves, without changing runtime behavior.
- Link skill surfaces through atom-linked drift guard tests [draft] - Accept a changed skill file as linked only when a tracked test that reads that skill tree is itself
linked to an atom or materialization, and emit evidence naming both the guard test and the skill
path.
- Make deskops next guide the user when no board task is routable [draft] - `deskops next` returns a structured, non-mutating guidance report for zero or multiple board
tasks and exits 0, while preserving the current report for a single task or an explicit selector.
- Add --why to deskops next [draft] - `deskops next --why` prints a `Why:` section that names the selection route, the matched workflow
state, the merged pill sources, and the source files, without mutating the desk.
