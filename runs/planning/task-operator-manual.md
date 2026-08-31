# Implementation Plan

## Goal
Consolidate the deskops methodology into one end-to-end operator manual, written only after the underlying runnable workflow slices are stable and proven via real CLI surfaces.

## Context Read
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md` (the task)
- `desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md`
- `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md`
- `desk/contexts/pill-cli-gaps-become-tracked-work.md`
- Note: the requested `context.md` does not exist at the given path; planning proceeded from the task file + pills only.

## Tasks
1. **Confirm slice stability precondition** (blocking gate from pill-operator-manual-follows-stable-runnable-slices)
   - Surface: the 9 scope areas (first use, capture/triage, task execution, pill binding, atom/graph queries, materialization, drift/self-reflection, closeout/commit, CI integration).
   - Changes: Verify each area maps to a stable, runnable CLI path before documenting. If any area is unstable/undefined, defer it to backlog instead of smoothing over in prose.
   - Acceptance: Each of the 9 areas has an identified stable command path or an explicit deferral note.

2. **Establish real CLI evidence per scope area** (pill-real-cli-surfaces-prove-operator-contracts)
   - Surface: `deskops` CLI (`deskops/cli/`, `deskops/operations.py`), e.g. `python -m deskops --help`, `deskops faq`, capture/promote/closeout/status/doctor/graph commands.
   - Changes: Run each documented command path, capture actual user-visible output + exit behavior to quote in the manual (no invented output).
   - Acceptance: Every documented command block is backed by an actually-run command.

3. **Route discovered CLI gaps to tracked work** (pill-cli-gaps-become-tracked-work)
   - Surface: `desk/drawer/tasks/` (new drawer tasks) or `desk/inbox/` for cross-repo intake.
   - Changes: For any command that fails/behaves unexpectedly, record failing command, expected vs actual, affected surface as a routable item; do NOT claim the path works in the manual.
   - Acceptance: No manual section claims a path works if validation exposed a gap; each gap has a tracked item.

4. **Author the manual document**
   - File: target path UNSPECIFIED by task (`files: []`); likely `docs/operator-manual.md` — MUST be confirmed (see Ambiguities).
   - Changes: Write the end-to-end playbook covering the 9 scope areas in the stable runnable order; link out to existing narrower guides (`README.md`, `docs/faq.md`, `docs/workflow-policy-reference.md`, `docs/how-to-test-ux-cli.md`) rather than duplicating them; defer unresolved areas to explicit backlog links.
   - Acceptance: Manual covers all in-scope areas or explicitly defers, and cross-links durable guides instead of restating them.

5. **Capture substantive new rules as atoms first** (AGENTS.md doc-vs-atom rule)
   - Surface: `desk/atoms/` then reflect in the doc.
   - Changes: If the manual introduces a new durable rule (not just materializing existing atoms), create/adjust the atom(s) first, then have the manual reflect them.
   - Acceptance: No net-new substantive rule lives only in `docs/`.

6. **Validate and close**
   - Commands: `pytest`; plus affected CLI commands (`python -m deskops --help`, `deskops faq`, and each command referenced in the manual).
   - Changes: Ensure tests pass; run execution/testing/closeout rituals; single atomic closing commit.
   - Acceptance: `pytest` green, CLI paths confirmed, task closed with its own commit.

## Files to Modify
- `docs/operator-manual.md` (or task-confirmed path) - new/updated manual content
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md` - status/current_node progression at closeout
- Possibly `desk/atoms/**` - if new durable rules are introduced

## New Files
- `docs/operator-manual.md` - the consolidated end-to-end operator manual (path pending confirmation)
- `desk/drawer/tasks/task-*.md` - only if CLI validation exposes gaps that need routing

## Dependencies
- Task 1 gates everything: no manual sections for unstable slices.
- Task 2 feeds Task 4 (evidence before prose).
- Task 3 runs alongside Task 2 (gaps found during validation).
- Task 5 precedes finalizing Task 4 for any new rules.
- Task 6 depends on 4 and 5.

## Risks
- **BLOCKING — undefined output location**: task `files: []` names no target path/filename for the manual. `docs/operator-manual.md` is a guess.
- **BLOCKING — undefined stability criteria**: pill requires "stable runnable slices" but task has empty `depends_on` and no list of which slices must be stable or how stability is judged. Cannot cleanly decide what to document vs defer.
- **Scope depth unspecified**: 9 broad areas with no target length, audience level, or format contract.
- **Rationale is "Not provided"**: no business driver to arbitrate scope trade-offs.
- **Duplication/drift risk**: overlapping with `README.md`, `docs/faq.md`, `docs/workflow-policy-reference.md`, `docs/how-to-test-ux-cli.md`; must cross-link, not restate.
- **CI integration area**: no referenced CI surface/config in the task; may itself be an unstable slice to defer.

## Ambiguities (must resolve before clean implementation)
1. Exact output path/filename of the manual (task `files` is empty).
2. Definition of "stable runnable slices" and which specific slices/commands qualify as stable now (`depends_on` is empty, contradicting the governing pill).
3. Target audience, depth, and format/template for the manual.
4. What "CI integration" concretely refers to (which pipeline/config surface).
5. Whether unstable areas should be omitted or stubbed-with-deferral in this pass.
6. The referenced `context.md` was missing — confirm whether additional context was intended.

## Verdict
**NECESITA-ACLARACIÓN** — the governing pill makes slice stability a precondition, but the task provides no stability criteria, no `depends_on`, and no output path. Items 1 and 2 in Ambiguities block clean implementation.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Produced a planning-only document (3-6 concrete steps + affected surfaces, explicit ambiguities, and a verdict). No code or repo files edited; only the authoritative planning output path was written."
    }
  ],
  "changedFiles": [
    "runs/planning/task-operator-manual.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Read task file and its 3 referenced pills; context.md not found (ENOENT), noted in plan."
  ],
  "residualRisks": [
    "Manual output path unspecified in task (files: []).",
    "Slice-stability precondition undefined; depends_on empty contradicts governing pill.",
    "context.md referenced by prompt does not exist."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added planning document at runs/planning/task-operator-manual.md with 6-step plan, ambiguity list, and NECESITA-ACLARACIÓN verdict.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "Verdict is NECESITA-ACLARACIÓN: the operator manual depends on stable runnable slices, but the task lacks stability criteria, depends_on entries, and a target output path. Recommend resolving ambiguities 1 and 2 before executing."
}
```
