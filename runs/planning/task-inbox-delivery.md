# Implementation Plan

## Goal
Make cross-desk inbox delivery verifiable (explicit sender/target/result) and actionable (recipient can discover, acknowledge, and reply/follow-up) instead of a write-only remote file drop.

## Context Read
- Task: `desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md`
- Pills: `pill-cross-desk-inbox-needs-delivery-verification-and-follow-up`, `pill-canonical-desk-identity-enables-horizontal-routing`, `pill-real-cli-surfaces-prove-operator-contracts`, `pill-cli-gaps-become-tracked-work`
- Code: `deskops/cli/commands/inbox.py`, `deskops/cli/parser.py` (`_add_inbox_commands`), `deskops/models/inbox.py` (`InboxNoteDoc`), `deskops/cli/model_introspection.py` (`artifact.inbox_note`), `tests/test_cli.py`

Note: the stated context file `context.md` does not exist at the repo root; proceeded with the task doc + pills as the authoritative brief.

## Current State (grounding)
- `deskops inbox <msg>` writes a note to a target desk `inbox/` dir. Target resolution already supports `--desk-root`, `--store`, `--repo` (registry lookup via `RepositoryDoc`), and default local store (`inbox.py:_desk_root`, `_resolve_repo_desk`).
- Sender is inferred from cwd against registered repo paths (`_sender_project`); falls back to `cwd().name` — this is the "ambiguous sender" gap the first pill warns about.
- Note frontmatter is fixed: `kind`, `sender_project`, `created_at`, `status: open` (`_render_note`, `InboxNoteDoc`). No `target`, no delivery-result field, no reply/ack linkage.
- Delivery "success" today = a file was written + optional auto-track (`_auto_track_note`). No returned verification contract beyond `Wrote {path}`.
- No acknowledgement / reply / follow-up command exists. `promote inbox-to-drawer-task` is the only downstream action.

## Tasks
1. **Define the delivery/verification contract (design decision, do first)**
   - File: new note under `desk/atoms/` (e.g. `desk/atoms/workflow-model/atom-cross-desk-inbox-delivery-contract.md`)
   - Changes: write down what counts as "successful delivery" (target desk resolved via canonical identity, note written, note tracked/validated, verification echoed to sender with resolved sender+target+path). Capture the acknowledgement/reply model before code.
   - Acceptance: atom exists and is referenced by the doc changes below; matches the four pills.

2. **Extend `InboxNoteDoc` with verifiable/actionable fields**
   - File: `deskops/models/inbox.py`; mirror defaults in `deskops/cli/model_introspection.py` (`artifact.inbox_note`).
   - Changes: add explicit `target_project` (recipient desk canonical id), and a follow-up field (e.g. `reply_to` / `thread_id` or `acknowledged_by`/`acknowledged_at`). Keep backward compatibility (optional fields, defaults) so existing notes still validate.
   - Acceptance: `tests/test_model_templates.py` round-trips the new fields; existing notes without them still parse.

3. **Make sender + target resolution explicit and fail-loud**
   - File: `deskops/cli/commands/inbox.py` (`_sender_project`, `_resolve_repo_desk`), `deskops/cli/parser.py`.
   - Changes: require canonical identity resolution; on ambiguous/duplicate registry match or unresolvable sender, fail clearly instead of silently falling back to `cwd().name`. Persist resolved `target_project` into the note. Consider a `--sender` override for explicit identity.
   - Acceptance: unit tests for (a) resolved sender+target written to frontmatter, (b) clear error on ambiguous/missing registry identity.

4. **Return a verifiable delivery result**
   - File: `deskops/cli/commands/inbox.py` (`run`, `_print`).
   - Changes: on write, emit a structured delivery result (sender, target, path, tracked bool) honoring `--format {text,json,yaml}`, with a non-zero exit if delivery cannot be verified (target unresolved / track+validate failed).
   - Acceptance: real CLI test (`tests/test_cli.py`) asserts JSON delivery payload and exit codes for success and failure paths.

5. **Add a recipient-side follow-up path (discover + acknowledge/reply)**
   - File: `deskops/cli/commands/inbox.py`, `deskops/cli/parser.py` (`_add_inbox_commands`), `deskops/cli/main.py` dispatch.
   - Changes: add at minimum an acknowledge/close-with-reply action (e.g. `deskops inbox --ack <selector>` or a reply that writes a linked note back to the sender's desk using the same identity contract). Reuse `_resolve_note`. Update `status` open→closed and record ack metadata.
   - Acceptance: CLI test shows a pending note is discoverable via `--list`, acknowledged, and status/metadata change is persisted; reply (if in scope) lands in sender desk.

6. **Docs + tracked-gap capture**
   - File: `docs/faq.md` and/or inbox help epilog in `deskops/cli/parser.py`; capture any discovered CLI gaps as drawer tasks per `pill-cli-gaps-become-tracked-work`.
   - Changes: document the delivery/ack/reply flow; ensure help examples show target + verification + follow-up.
   - Acceptance: `deskops inbox --help` reflects new flags; `tests/test_cli.py` help assertions updated.

## Files to Modify
- `deskops/models/inbox.py` — add `target_project` + follow-up/ack fields (optional, defaulted).
- `deskops/cli/model_introspection.py` — mirror new field defaults for `artifact.inbox_note`.
- `deskops/cli/commands/inbox.py` — explicit sender/target resolution, delivery-result output, ack/reply action.
- `deskops/cli/parser.py` — new flags (`--ack`/`--reply`/`--sender`) and updated help/epilog.
- `deskops/cli/main.py` — dispatch for any new subaction if not flag-based.
- `docs/faq.md` — operator-facing flow.
- `tests/test_cli.py`, `tests/test_model_templates.py` — coverage for new behavior.

## New Files
- `desk/atoms/workflow-model/atom-cross-desk-inbox-delivery-contract.md` — durable truth for the delivery/verification/follow-up contract (materialize before docs).

## Dependencies
- Task 1 (contract) gates 2–6; the delivery/ack/reply semantics must be decided first.
- Task 2 (model fields) gates 3, 4, 5 (they read/write the new fields).
- Task 3 (resolution) gates 4 (result includes resolved sender/target).
- Task 6 (docs) depends on 3–5 landing.

## Risks
- **Scope is design-heavy, not just implementation.** The task's own scope lists five open design questions (what proves delivery, how recipients discover/ack/pull, reply path, minimum slice). These are not yet decided anywhere I could read; picking them is a product decision, not a mechanical change.
- **"Minimum implementation slice" is undefined.** Task 5 (ack/reply) could be a small status flip or a full bidirectional threaded reply system. Building the larger version risks scope-widening beyond `criterion-1`.
- **Backward compatibility.** Existing tracked inbox notes and `InboxNoteDoc` round-trip validation (`validate_model_input_roundtrip` in `_auto_track_note`) will break if new fields are required. Must be optional/defaulted.
- **Canonical identity dependency.** Fail-loud sender/target resolution (pill-2) depends on registry uniqueness guarantees that may not exist yet; may surface a prerequisite gap in `RepositoryDoc` registration.
- **Cross-desk writes to sibling repos** (reply path) touch another repo's worktree — needs an explicit, verifiable, sandbox-tested contract per `pill-real-cli-surfaces` and AGENTS sandbox rule.
- **Missing `context.md`** referenced by the run brief — cannot confirm additional intent the parent may have assumed.

## Verdict
**NECESITA-ACLARACIÓN.**

Blocking decisions before clean implementation:
1. What is the authoritative definition of "successful delivery"? (file written vs. written+tracked+validated vs. sender-visible verification receipt.)
2. What is the recipient discovery/acknowledge model — pull-based (`--list` + `--ack`) only, or push/notify? Is a reply that writes back to the sender desk in scope for this task or deferred?
3. What is the intended **minimum slice** for this task (to respect no-scope-widening)? Likely: verifiable sender+target+result + a single ack action. Confirm before building reply threading.
4. Should the model changes be additive/optional (recommended for compat) and is a new atom the right home for the contract?

If decisions 1–3 are answered with "minimum slice = explicit sender/target + verifiable delivery result + status ack," the plan above is directly executable. Until then, implementation would require guessing the coordination model.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Produced a planning-only artifact (no code changed); plan scoped strictly to the assigned task file and its four referenced pills, with an explicit minimum-slice recommendation to avoid scope widening."
    }
  ],
  "changedFiles": [
    "runs/planning/task-inbox-delivery.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "No commands run; planning subagent, read-only analysis of task doc, pills, inbox.py, parser.py, models/inbox.py, model_introspection.py, tests/test_cli.py references."
  ],
  "residualRisks": [
    "Task is design-heavy with undecided coordination model; verdict is NECESITA-ACLARACION pending 4 decisions.",
    "Referenced context.md does not exist at repo root; parent intent beyond task doc not confirmed.",
    "Canonical-identity fail-loud resolution may expose a RepositoryDoc registry prerequisite gap."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added one planning document at runs/planning/task-inbox-delivery.md; no source or test files modified.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "context.md referenced in the task prompt was missing (ENOENT); planned from the task file and pills instead. Verdict is NECESITA-ACLARACION: minimum implementation slice and recipient follow-up model must be decided before clean execution."
}
```
