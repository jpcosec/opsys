# Pills

Pills are the reusable context documents of the desk routine.

They are temporary in the workspace but durable in git history.

## Base Shape

Pills currently use the base `PillDoc` model in `desk/models/pill.py`.

Required fields:

- `title`
- `id`
- `what`
- `why`
- `when`
- `where`
- `how`
- `how_not`
- `tags`

## Notes

- Task-to-pill binding lives in task documents, not in pills.
- The semantic cue that might later become a dedicated model kind lives in the title for now, for example `ADR: ...` or `Pattern: ...`.
- Tags go at the end and should use namespaced forms such as `language:python`, `library:pydantic`, or `system:sldb`.
- `where` may be either a general applicability description or a reference to already existing code or docs.
- A pill can be deleted once it is no longer needed in the active workspace; reuse remains available through git history.
- Coverage is only sufficient when the executor checks active board pills plus task-local pills against the task scope, touched files, and validation plan.
- For risky or non-trivial tasks, run at least one cold review through a fresh-context subagent before finalizing pill coverage.
- Non-trivial tasks should normally bind `pill-007` so the executor must pass through explicit initialization, testing, and closeout gates rather than treating them as implied follow-through.
- Bind a pill when its `when` matches the task state, its `where` matches the surfaces being touched, or its `how_not` describes a plausible failure mode for the task.
- If no existing pill covers a risky ambiguity, create or update a pill before continuing.
