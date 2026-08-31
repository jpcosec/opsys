# Implementation Plan

## Goal
Prove and close the gaps in the executable `deskops` task lifecycle (intake → drawer → active task bundle → execution/testing/closeout gates → deletion + evidence) so an operator can drive a task from an inbox/drawer item to a closing commit using only real CLI commands.

## Context Findings (what already exists)

The lifecycle machinery is largely built. Concretely:

- **Intake → drawer**: `deskops promote inbox-to-drawer-task <selector>` — `deskops/cli/commands/promote.py::_inbox_to_drawer_task`. Creates `desk/drawer/tasks/task-<slug>.md`, deletes the source note.
- **Drawer → active bundle**: `deskops promote drawer-task-to-active-task <selector>` — `promote.py::_drawer_task_to_active_task` → `DeskopsOperations.create_task_bundle` (`deskops/operations.py:211`). Emits task + routine + checklists + conditions + operators + edges.
- **Gate advance**: `deskops advance task <task-id>` — `deskops/cli/commands/operations.py:238` → `operations.py::advance_task` (`operations.py:457`). Walks routine `execution-ready → activate(status=active) → testing-ready → ready-for-testing(status=ready_for_testing) → closeout-ready → close(status=closed) → complete`.
- **Gate conditions** (this task's own bundle):
  - testing-ready: `validation` not_empty (`condition-...-has-validation.md`).
  - closeout-ready: `status == ready_for_testing` (`condition-...-ready-for-closeout.md`) AND `closeout_evidence_verified` truthy (`condition-...-has-closeout-evidence.md`).
  - Evidence is computed at advance time by `operations.py::_has_verified_task_closeout_evidence` (`operations.py:975`): a `references[]` entry must resolve to a real atom under `desk/atoms/`, a real `*.py` test path, or a real git commit.
- **Closure + deletion**: on reaching `status=closed, current_node=complete`, `operations.py::_auto_commit_task_closure` (`operations.py:914`) stages files, removes the task doc + routine + task-scoped primitives (`_remove_task_runtime_artifacts`, `operations.py:949`), unlinks the task from `desk/tasks/Board.md`, and makes a `chore(task): ...` commit.
- **Tool-made evidence commit**: separate `deskops closeout commit --run-dir <runs/subagents/...> --task <id>` — `deskops/cli/commands/closeout.py`, requires `board.txt/task.txt/git-status.txt/result-summary.md` and writes trailers + `runs/subagents/index.jsonl`.

Because the machinery already exists, this task is most coherently a **dogfooding + gap-closing + regression-locking** task, not a greenfield build. That interpretation is driven by the four bound pills (see Risks for the ambiguity).

## Tasks

1. **Dry-run the full lifecycle in a sandbox desk (no repo `desk/` mutation).**
   - Surface: disposable desk root, e.g. `.tmp/deskops-cli-test` (per AGENTS.md CLI-mutation rule and `atom-cli-mutation-testing-uses-sandbox-desk-roots`).
   - Steps: `deskops desk install --path .tmp/deskops-cli-test`; seed an inbox note; run `promote inbox-to-drawer-task`, `promote drawer-task-to-active-task`, then repeated `advance task` calls; observe where advancement stalls.
   - Acceptance: capture per-command exit code + stdout for each stage into a run-evidence note.

2. **Record every observed gap as structured evidence.**
   - Surface: `runs/subagents/<ts>-task-lifecycle/result-summary.md` (and the required `board.txt`, `task.txt`, `git-status.txt` if a tool-made closeout commit will be used).
   - Changes: for each failing/blocking command record `command / expected / actual / affected surface` per `pill-cli-gaps-become-tracked-work`.
   - Acceptance: every stall in step 1 has a written expected-vs-actual entry.

3. **Fix the minimal blocking gap(s) found, without widening scope.**
   - Likely candidate surfaces (confirm against step 1 output before editing):
     - `deskops/cli/commands/promote.py` — bundle default `validation`/`references` so the testing and closeout gates are actually satisfiable end to end (note: default `references` points at the deleted drawer source, which is not an atom/test/commit, so `closeout_evidence_verified` is `False` by default — the closeout gate cannot pass without an operator adding real evidence).
     - `deskops/operations.py` — `advance_task` / `_has_verified_task_closeout_evidence` / `_auto_commit_task_closure` if a stage misbehaves.
   - Changes: smallest change that unblocks the path; do not redesign the routine grammar.
   - Acceptance: after the fix, the sandbox run in step 1 advances cleanly from intake to `status=closed, current_node=complete` (given real evidence is supplied), and the task doc + routine + task-scoped primitives are deleted and unlinked from the sandbox Board.

4. **Add an end-to-end regression test for the runnable lifecycle.**
   - File: new `tests/test_lifecycle_end_to_end.py` (no existing lifecycle E2E test; `test_operational.py` only covers `create_task_bundle` rollback and an in-memory `advance`).
   - Changes: build a temp git repo + scaffolded desk, drive promote → promote → advance (xN) through the real CLI entrypoints (mirror the `_git` + `SimpleNamespace(args)` pattern in `tests/test_closeout.py`), assert final `status=closed`, task/routine/primitive files removed, Board unlinked, and a closing commit present.
   - Acceptance: `pytest tests/test_lifecycle_end_to_end.py` passes; full `pytest` stays green.

5. **Graduate durable knowledge into atoms and satisfy the closeout evidence gate for this task itself.**
   - Files: new atom(s) under `desk/atoms/workflow-model/` capturing the runnable-lifecycle ruling; update this task's `references:` to point at the new atom and/or the new test file so `_has_verified_task_closeout_evidence` returns truthy.
   - Rationale: `pill-durable-pill-knowledge-graduates-to-atoms-at-closeout` + `pill-closeout-knowledge-gates-require-traceable-evidence`.
   - Acceptance: `deskops advance task task-make-task-lifecycle-runnable-from-intake-to-closeout` passes the closeout-ready checklist without a forced `--to`.

6. **Route any non-blocking gaps to tracked work; close the task with a real commit.**
   - Files: new drawer tasks under `desk/drawer/tasks/` for deferred gaps; closing commit via the auto-commit path (or `deskops closeout commit`).
   - Acceptance: no discovered gap left only in run notes; task closes with its own atomic commit per `pill-001-task-closure-commit`.

## Files to Modify
- `deskops/cli/commands/promote.py` — only if step 1 shows the generated bundle cannot satisfy the testing/closeout gates end to end (default `validation`/`references`).
- `deskops/operations.py` — only if `advance_task`, evidence verification, or auto-commit/cleanup misbehaves during the sandbox run.
- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md` — populate `references:` with real atom/test evidence so its own closeout gate passes.

## New Files
- `tests/test_lifecycle_end_to_end.py` — real-CLI intake→closeout regression test.
- `desk/atoms/workflow-model/atom-<...>.md` — durable ruling that the lifecycle is CLI-runnable end to end (exact id TBD from findings).
- `runs/subagents/<ts>-task-lifecycle/` — run evidence (`result-summary.md`, `board.txt`, `task.txt`, `git-status.txt`) if using the tool-made closeout commit.
- `desk/drawer/tasks/task-<...>.md` — for any deferred, non-blocking gaps.

## Dependencies
- 2 depends on 1 (need observed output to record).
- 3 depends on 2 (fix only confirmed blockers).
- 4 depends on 3 (test locks the working path).
- 5 depends on 3/4 (atom + reference point at the proven behavior/test).
- 6 depends on 5 (closeout gate must pass, or gaps routed, before commit).

## Risks
- **Primary ambiguity — deliverable scope is underspecified.** The task rationale is "Not provided" and the machinery already exists. It is not stated whether the deliverable is (a) a dogfooding validation + regression test, (b) net-new CLI glue, or (c) documentation of the runnable path. This plan assumes (a)+(b-minimal). **Needs confirmation before step 3 code edits.**
- **Closeout evidence gate is a real blocker by construction.** `create_task_bundle` defaults `references` to the (now-deleted) drawer source path, which is neither atom, test, nor commit, so `closeout_evidence_verified` is `False` and the closeout-ready checklist cannot pass on a freshly promoted task without an operator manually adding real evidence. Decide whether that is intended (operator must supply evidence) or a gap to fix. This directly determines whether step 3 touches `promote.py`/`operations.py`.
- **`advance_task --to` bypass.** `advance_task` honors a `target_node`/`--to` that force-sets status/current_node with no gate check (`operations.py:465-472`). An E2E test must exercise the *gated* path (no `--to`) to actually prove the contract; using `--to` would give a false green.
- **Auto-commit vs. tool-made closeout commit overlap.** `_auto_commit_task_closure` (auto commit on complete) and `deskops closeout commit` (run-evidence commit) are two different closing mechanisms. Clarify which one the "runnable path" should standardize on; the task's `Done When` says "closed with a commit" but not which.
- **Sandbox discipline.** All mutating exploration must target a disposable desk (`.tmp/deskops-cli-test`), not the tracked `desk/`, except the final intentional edits to this task's own doc/atom. Accidental mutation of the real Board via auto-commit cleanup is a live hazard.
- **Test git side effects.** Lifecycle E2E and auto-commit invoke real `git` in the temp repo; the test must `git init` + set user config (as `test_closeout.py` does) and assert against temp state only.
- **Status vocabulary coupling.** The closeout condition hardcodes `expected: ready_for_testing`; any change to operator status values must stay consistent across conditions/operators or advancement silently stalls.

## Verdict
**NECESITA-ACLARACIÓN** — the machinery to run the lifecycle already exists, so the concrete deliverable (validate/dogfood vs. build new glue vs. fix the closeout-evidence-by-default blocker vs. document) must be confirmed before writing code. Steps 1–2 (sandbox dry-run + gap capture) and step 4 (E2E regression test) are safe to execute regardless of that decision; steps 3, 5, 6 depend on the scope answer.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Produced a read-only implementation plan scoped to the requested task and its 4 referenced pills; no code or desk files were modified."
    }
  ],
  "changedFiles": [
    "runs/planning/task-lifecycle-runnable.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Planning-only run; no build/test executed. Read task doc, 4 pills, routine, 3 checklists, 4 conditions, 3 operators, promote.py, closeout.py, operations.py (advance_task, evidence, auto-commit), parser.py, Board.md, and tests dir."
  ],
  "residualRisks": [
    "Deliverable scope is underspecified (task rationale 'Not provided'); lifecycle machinery already exists so concrete work must be confirmed.",
    "Freshly promoted tasks cannot pass the closeout-evidence gate by default because default references point at the deleted drawer source path.",
    "advance_task --to bypasses gates; an E2E test must use the gated path to avoid false-green."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added one planning document at runs/planning/task-lifecycle-runnable.md; no source or desk changes.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "Verdict is NECESITA-ACLARACIÓN: promote/advance/closeout CLI path already implemented, so parent should confirm whether this task means dogfood+regression-test, fix the closeout-evidence-by-default blocker, add new glue, or document the path before code edits (steps 3/5/6)."
}
```
