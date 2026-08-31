# Implementation Plan

## Goal
Make task closeout gate on traceable knowledge evidence (tests, atom/materialization links, generated-artifact provenance, stale-doc cleanup, dedicated commit) before a task leaves the active desk.

## Context Read
- Task: `desk/tasks/task-wire-closeout-to-knowledge-gates.md` (status active, phase 1, routed on Board).
- Pills: closeout-knowledge-gates-require-traceable-evidence, durable-pill-knowledge-graduates-to-atoms-at-closeout, materialization-contracts-declare-source-intent-and-target, atom-lifecycle-preserves-provenance-and-materialization-links.
- Ritual: `desk/rituals/closeout.md`.
- Current code surfaces that already exist:
  - `deskops/operations.py:975 _has_verified_task_closeout_evidence` — passes if **any one** reference resolves to an atom, test, or git commit (`_reference_points_to_atom/_test/_commit`, lines ~988-1035).
  - Default primitives synthesized in `operations.py`: `condition-<task>-has-closeout-evidence` (line ~747), `condition-<task>-ready-for-closeout` (line ~758), `checklist-<task>-closeout-ready` (line ~792), and the closeout edges (~873-887).
  - `deskops/cli/commands/closeout.py CloseoutCLI` — tool-made closing commit that requires run evidence files (`board.txt`, `task.txt`, `git-status.txt`, `result-summary.md`) and writes `runs/subagents/index.jsonl`.
  - Materialization/graph surfaces: `deskops/graph/extract_edges.py` (materialization edges), `deskops/graph/extract_coverage.py`, `deskops/graph/self_reflection.py`, `deskops/materializers/atoms.py`.
- Tests: `tests/test_closeout.py`, `tests/test_operational.py`, `tests/test_specs.py` already assert current closeout-evidence behavior.

## Tasks
1. **Confirm scope boundary vs sibling tasks (blocking pre-step).**
   - Read `desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md` and `desk/tasks/task-add-drift-check-review-loop.md`.
   - Changes: none (analysis only).
   - Acceptance: written note stating which gates this task owns vs the two siblings. See Risks — this likely needs supervisor/human decision before code.

2. **Strengthen the closeout evidence predicate.**
   - File: `deskops/operations.py` (`_has_verified_task_closeout_evidence` ~975 and helpers ~988-1035).
   - Changes: decide and implement whether evidence must include *each* required gate (test AND atom/materialization link AND commit) rather than any-one-of. Add a helper to detect materialization links on changed files (reuse `graph/extract_edges.py` materialization parsing) and/or a "routed follow-up" reference form. Keep helpers pure/testable.
   - Acceptance: new unit tests in `tests/test_operational.py` cover pass/fail for each gate; existing tests updated intentionally, not silently.

3. **Extend synthesized closeout conditions/checklist to cover new gates.**
   - File: `deskops/operations.py` (`_default_condition_payloads` ~725, `_default_checklist_payloads` ~770 with `checklist-<task>-closeout-ready` ~792).
   - Changes: add condition(s) for the new subjects (e.g. `changed_files_have_links`, `generated_artifacts_declare_sources`, `stale_docs_resolved`) and wire them into the closeout-ready checklist `condition_refs`. Ensure `advance()` populates the corresponding `payload[...]` booleans alongside `closeout_evidence_verified` (~482, ~752).
   - Acceptance: `tests/test_specs.py` and `tests/test_operational.py` assert the new conditions compile and gate advancement.

4. **Regenerate / update this task's primitive docs to match the new defaults.**
   - Files: `desk/primitives/conditions/condition-task-wire-closeout-to-knowledge-gates-*.md`, `desk/primitives/checklists/checklist-task-wire-closeout-to-knowledge-gates-closeout-ready.md`, `desk/routines/routine-task-wire-closeout-to-knowledge-gates.md`.
   - Changes: add any new condition docs and reference them from the closeout checklist, matching the code-synthesized IDs.
   - Acceptance: `deskops graph missing` / `sldb stores check --store .sldb` report no dangling refs.

5. **(If in scope) surface a verify path in the closeout CLI.**
   - File: `deskops/cli/commands/closeout.py`, `deskops/cli/parser.py` (`_add_closeout_command` ~700).
   - Changes: optionally add a `closeout verify`/pre-commit check that runs the evidence predicate before allowing the tool-made commit, so the gate is enforced at commit time, not only during `advance`.
   - Acceptance: `tests/test_closeout.py` covers a rejected commit when a required gate is unmet; `deskops closeout --help` shows the surface.

6. **Update ritual + atomize durable rule; validate and close.**
   - Files: `desk/rituals/closeout.md` (reflect the enforced gates), one or more atoms under `desk/atoms/workflow-model/` capturing the durable ruling behind the 4 bound pills (per pill-durable-pill-knowledge-graduates-to-atoms-at-closeout).
   - Changes: docs materialize the atoms, not vice versa.
   - Acceptance: `pytest` green; task references point to real atom/test/commit; dedicated closing commit via `deskops closeout commit`.

## Files to Modify
- `deskops/operations.py` — evidence predicate, synthesized closeout conditions/checklist, payload population.
- `deskops/cli/commands/closeout.py` — optional verify gate before commit.
- `deskops/cli/parser.py` — optional new closeout subcommand/flags.
- `desk/primitives/conditions/*wire-closeout*`, `desk/primitives/checklists/*wire-closeout*closeout-ready.md`, `desk/routines/routine-task-wire-closeout-to-knowledge-gates.md` — match new IDs.
- `desk/rituals/closeout.md` — reflect enforced gates.
- `tests/test_operational.py`, `tests/test_specs.py`, `tests/test_closeout.py` — cover new behavior.

## New Files
- `desk/atoms/workflow-model/atom-*.md` — durable ruling distilled from the 4 bound pills (graduation, materialization contract, atom provenance, closeout traceability). Exact count/names depend on Task 1 boundary decision.

## Dependencies
- Task 1 gates everything: the scope boundary decision determines how much of Tasks 2-5 belongs here vs the two sibling closeout/drift tasks.
- Task 3 depends on Task 2 (payload booleans must exist before conditions reference them).
- Task 4 depends on Tasks 2-3 (IDs must be final).
- Task 5 depends on Task 2 (reuses the predicate).
- Task 6 depends on all prior tasks.

## Risks
- **Underspecified task (primary blocker).** Rationale is "Not provided" and Goal/Scope are broad ("check tests, atoms, graph links, materialization status, cleanup, commit evidence"). No acceptance criteria beyond `pytest`.
- **Heavy overlap with two active phase-1 tasks:** `task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout` (pill→atom graduation gate) and `task-add-drift-check-review-loop` (atoms/materializations/graph/tests/diagrams comparison). This task's scope currently subsumes both. Without a boundary decision, implementation will duplicate or collide with sibling work. Needs explicit decision.
- **Behavior change to existing gate.** Current `_has_verified_task_closeout_evidence` is any-one-of; tightening to all-of will break the current green path (`tests/test_operational.py`, `tests/test_closeout.py`, `tests/test_specs.py`) and could block real closeouts. Must be intentional and test-updated.
- **"Stale tasks/pills deleted or promoted" and "generated artifacts declare sources" are hard to verify automatically** — needs a concrete, resolvable check surface (graph query? filesystem scan?) or it degrades into a narrative claim, which the guardrail pill explicitly forbids.
- **Doc/code ID drift.** Synthesized default IDs in `operations.py` must stay in lockstep with the checked-in `desk/primitives/*` docs, or `graph missing`/`stores check` will flag dangling refs.

## Verdict
**NECESITA-ACLARACIÓN.** The mechanics are clear and the code surfaces are known, but the scope boundary against the two sibling closeout/drift tasks and the concrete definition of the non-trivial gates (materialization link check, generated-artifact provenance, stale-doc cleanup, all-of vs any-of evidence) are unspecified. Resolve Task 1 (ideally via supervisor decision) before implementing Tasks 2-6.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Planning-only output; no code changed and scope kept to the requested closeout-to-knowledge-gates task plus its four bound pills and directly related surfaces."
    }
  ],
  "changedFiles": [
    "runs/planning/task-wire-closeout.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "No tests run: planning subagent, read-only analysis of task, pills, ritual, operations.py, closeout.py, and desk primitives."
  ],
  "residualRisks": [
    "Scope overlaps with task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout and task-add-drift-check-review-loop; boundary must be decided before coding.",
    "Task lacks rationale and acceptance criteria beyond pytest; several gates are not yet automatable as specified.",
    "Tightening the existing any-of evidence predicate will change current green behavior and must be test-updated intentionally."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added implementation plan document at runs/planning/task-wire-closeout.md.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "Referenced routine/checklist/condition docs DO exist under desk/routines and desk/primitives (task frontmatter names resolve). Task 1 boundary decision is the gating item; recommend supervisor decision on scope split across the three closeout/drift tasks."
}
```
