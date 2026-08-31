# Implementation Plan

## Goal
Make task closeout verify that durable knowledge surfaced through bound pills is graduated into atoms before the pill/task context is deleted, with traceable evidence rather than prose.

## Context Findings
- Note: the requested `context.md` at repo root does not exist (ENOENT). Planning proceeded from the task doc and its two bound pills only, as instructed.
- The task (`desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md`) is in `current_node: checklist-...-execution-ready` and validates with `pytest`.
- Two bound pills:
  - `pill-durable-pill-knowledge-graduates-to-atoms-at-closeout` (guardrail: review bound pills at closeout, atomize durable residue before retiring the pill; do NOT force atom updates when a pill only routed existing knowledge).
  - `pill-closeout-knowledge-gates-require-traceable-evidence` (guardrail: closeout gates are evidence checks over real atoms/materializations/graph/tests/commits, must fail clearly when a link is missing).
- Existing closeout enforcement lives in `deskops/operations.py`:
  - `_has_verified_task_closeout_evidence` (line ~975) already checks that `references` point to a real atom (`_reference_points_to_atom`), test, or commit.
  - `condition-<task>-has-closeout-evidence` + `checklist-<task>-closeout-ready` (in `_default_condition_payloads` / `_default_checklist_payloads`, lines ~747-800) already gate closeout on `closeout_evidence_verified`.
  - `advance_task` (line ~482) computes `payload["closeout_evidence_verified"]` before running the routine.
- Pill binding: `bind_pill_to_task` maintains `payload["pills"]`; board pills merge into `effective_pills` (lines 295-327, 1069).
- Human-facing ritual text is `desk/rituals/closeout.md`; there is also an embedded closeout template in `deskops/workspace.py` (`_closeout_template`, line ~189).
- `AGENTS.md` boundary: substantive rules must first be captured as atoms under `desk/atoms/`, then reflected in docs. This task itself will likely need a new atom.

## Tasks
1. **Define the graduation rule as an atom** (satisfies AGENTS.md "atom-first" boundary).
   - File: new `desk/atoms/workflow-model/atom-durable-pill-knowledge-graduates-to-atoms-at-closeout.md`
   - Changes: capture the durable rule (closeout audits bound pills; durable residue must be promoted to an atom; pills that only routed existing knowledge require no new atom) as a single atom, tagged consistently with sibling atoms.
   - Acceptance: `sldb stores check --store .sldb` (or `deskops graph missing`) resolves the atom; atom is discoverable.

2. **Add a pill-audit closeout evidence check in operations**.
   - File: `deskops/operations.py`
   - Changes: add a helper (e.g. `_pill_knowledge_graduation_verified(payload)`) that, when the task has bound `pills`/`effective_pills`, requires closeout evidence that references at least one atom (reuse `_reference_points_to_atom`). Expose the result as a new payload field (e.g. `payload["pill_graduation_verified"]`) computed in `advance_task` alongside `closeout_evidence_verified` (line ~482). Preserve the pill exemption: if the task has no bound pills, the check passes trivially.
   - Acceptance: unit test shows a task with bound pills but no atom reference fails the gate; a task with an atom reference (or no pills) passes.

3. **Wire the new check into the closeout gate primitives**.
   - File: `deskops/operations.py`
   - Changes: in `_default_condition_payloads` add `condition-<task>-pill-knowledge-graduated` (subject `pill_graduation_verified`, predicate `truthy`); in `_default_checklist_payloads` add it to `checklist-<task>-closeout-ready` `condition_refs` and `items`.
   - Acceptance: generated task graph shows the new condition referenced by the closeout checklist; closeout blocks until satisfied.

4. **Reflect the rule in the closeout ritual doc and template**.
   - Files: `desk/rituals/closeout.md` and `deskops/workspace.py` (`_closeout_template`).
   - Changes: add a step and matching failure mode stating that bound-pill durable knowledge must be graduated into atoms (with traceable evidence) before pill/task deletion. Keep wording aligned with the new atom.
   - Acceptance: ritual step list and template both mention pill-to-atom graduation; wording traces to the atom from Task 1.

5. **Add/extend tests**.
   - File: existing operations/closeout test module (locate under `tests/`; e.g. `tests/test_operations.py` or the closeout-evidence test) — verify exact path before editing.
   - Changes: cases for (a) bound pills + atom reference → passes, (b) bound pills + only commit/test reference → fails, (c) no bound pills → passes, (d) the new condition/checklist wiring is present in generated primitives.
   - Acceptance: `pytest` green.

6. **Closeout for this task itself**.
   - Changes: ensure the task's own `references` include the new atom + test so it satisfies the very gate it introduces; then run closeout ritual and single atomic commit.
   - Acceptance: `pytest` passes; task removed from board/`desk/tasks`; one closing commit.

## Files to Modify
- `deskops/operations.py` - new pill-graduation evidence helper, payload field in `advance_task`, new condition + closeout checklist wiring.
- `desk/rituals/closeout.md` - add graduation step + failure mode.
- `deskops/workspace.py` - mirror the ritual step in `_closeout_template`.
- The relevant `tests/` module for operations/closeout evidence - new coverage.
- The task doc's own `references` - add the new atom + test as closeout evidence.

## New Files
- `desk/atoms/workflow-model/atom-durable-pill-knowledge-graduates-to-atoms-at-closeout.md` - durable rule capture (atom-first boundary).

## Dependencies
- Task 1 (atom) precedes Task 4 (docs must reflect atoms per AGENTS.md).
- Task 2 precedes Task 3 (payload field must exist before condition references it).
- Task 3 precedes Task 5 (tests assert wiring).
- Task 5 precedes Task 6 (evidence + commit).

## Risks / Ambiguities

### Ambiguities that block clean implementation
1. **"Durable vs transitional" is not machine-detectable.** The scope wants closeout to "distinguish transitional pill context from durable residue" and to "avoid forcing atom updates when a pill only routed already-existing knowledge." No signal exists to auto-classify this. Decision needed: is a *heuristic gate* (any bound pill => require an atom reference in evidence) acceptable, or must it be a softer prompt/checklist item the agent affirms? A hard heuristic risks false positives (blocking tasks whose pills only routed existing knowledge). **This is the central unresolved design choice.**
2. **Task-type scoping.** Scope says apply to "bugfix, feature, and migration tasks." `TaskDoc` has a `task_type` field, but this task is untyped and most tasks may not set it. Decision needed: gate by `task_type` (and what default when unset?) or by presence of bound pills regardless of type?
3. **Evidence shape for graduation.** The existing gate accepts atom OR test OR commit. For *pill graduation* specifically, must evidence be an *atom* reference specifically (not just any evidence)? The pills imply atoms, but the exact required reference form (path to atom, `atom:` id, or a new dedicated task field like `graduated_atoms`) is unspecified.
4. **New field vs reuse of `references`.** Unclear whether graduation evidence should reuse the existing `references` list or a dedicated field. Reusing `references` is simplest but conflates general closeout evidence with pill-graduation evidence.
5. **Interaction with phase-level pill reconciliation.** AGENTS.md/phase ritual already handle "pill reconciliation" at phase close. Decision needed: does this rule live at task closeout only, or also touch phase ritual? Task scope says task closeout; keep it there unless told otherwise.
6. **No `context.md`.** The referenced context file is missing, so any additional constraints it carried are unknown.

### Execution risks
- Adding a hard condition to `checklist-closeout-ready` will affect **all newly generated tasks**, not just this one; existing in-flight tasks regenerated could suddenly block. Verify backward compatibility / migration behavior.
- Editing `_default_*_payloads` must stay in sync with any tests asserting exact primitive counts/shapes.
- `deskops/workspace.py` template and `desk/rituals/closeout.md` can drift; keep both edits identical in intent.

## Verdict
**NECESITA-ACLARACIÓN** — The core mechanism (how closeout decides that durable pill knowledge exists and must be atomized, without falsely blocking pills that only routed existing knowledge) is unspecified (ambiguities 1-4). Recommend resolving at minimum ambiguity 1 (heuristic hard-gate vs affirmed checklist item) and ambiguity 3 (atom-specific evidence vs any evidence) before implementation. The surfaces and wiring are otherwise clear and ready.
