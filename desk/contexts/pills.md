# Pills

Pills are the reusable context documents of the desk routine.

They are temporary in the workspace but durable in git history. A pill is not a task instance: it is a reusable atomic execution truth that may be rebound across many tasks and phases. A pill may either point at already-settled knowledge or carry transitional task knowledge that has not yet been incorporated into the durable atom base.

## Base Shape

Pills currently use the base `PillDoc` model in `deskops/models/pill.py`.

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
- The relationship is many-to-many: one task can bind many pills, and one pill can apply to many tasks.
- Pill type is a namespaced tag convention, not a modeled field. Use exactly one `pill-type:*` tag on active pills.
- Human-readable title prefixes such as `Guardrail:`, `Pattern:`, `Decision:`, and `Model:` should match the `pill-type:*` tag when practical.
- Tags go at the end and should use namespaced forms such as `language:python`, `library:pydantic`, or `system:sldb`.
- `where` may be either a general applicability description or a reference to already existing code or docs.
- Pills are allowed to carry not-yet-implemented bugfix/feature knowledge during execution, but that knowledge should not remain pill-only once it stabilizes.
- A pill can be deleted once it is no longer needed in the active workspace; reuse remains available through git history.
- Coverage is only sufficient when the executor checks active board pills plus task-local pills against the task scope, touched files, and validation plan.
- For risky or non-trivial tasks, run at least one cold review through a fresh-context subagent before finalizing pill coverage.
- Non-trivial tasks should normally bind `pill-007` so the executor must pass through explicit initialization, testing, and closeout gates rather than treating them as implied follow-through.
- Bind a pill when its `when` matches the task state, its `where` matches the surfaces being touched, or its `how_not` describes a plausible failure mode for the task.
- If no existing pill covers a risky ambiguity, create or update a reusable pill before continuing.
- If a context note only makes sense for one narrow task and cannot be reused, prefer the task doc unless the note should graduate directly into atoms.

## Pill Types

- `pill-type:guardrail` prevents known failure modes. Bind it when `how_not` describes a plausible task failure.
- `pill-type:pattern` describes a reusable way to perform work. Bind it when the task is doing the kind of work named by `when` or `how`.
- `pill-type:decision` records an active architectural or boundary decision. Bind it when the task touches that boundary or tradeoff.
- `pill-type:model` defines a conceptual shape or representation rule. Bind it when the task creates, extracts, validates, or changes that representation.
- `pill-type:index` points to existing atoms, docs, specs, or source surfaces that provide required context. Bind it when the task needs orientation but should not duplicate the referenced knowledge.

Avoid `pill-type:atom`. A pill that only surfaces durable knowledge should be an `index` pill and should reference the atom instead of copying it. A pill that captures in-flight implementation knowledge is valid during the task, but once that knowledge becomes durable project ruling it should be distilled into atoms, with docs/specs/code following from the atom base. Once no active task needs the transient context, delete the pill.

## Fresh Subagent Guidance

Fresh subagents should read only the context needed for the decision:

- Active task file.
- `desk/tasks/Board.md`.
- Board-routed pills under `desk/contexts/`.
- Task-local pills listed in the task.
- Relevant atoms only when a pill references them or ambiguity remains.

Fresh subagents should not read these by default:

- The whole `desk/contexts/` directory.
- Old or deferred drawer tasks unless the board routes them.
- All atoms by raw scanning.
- Generated graph/runtime outputs.
- Unrelated code just because a pill mentions a broad system.

Fresh subagents validate pill coverage by checking:

- Every bound pill has a matching `when`, `where`, or `how_not`.
- Every active pill has exactly one `pill-type:*` tag.
- The task is executable after reading task plus routed pills without improvisation.
- Pills reference atoms/docs/specs instead of copying durable knowledge.
- Testing handoff translates guardrail `how_not` clauses into concrete checks where applicable.

## Current Board-Routed Pills

- `pill-001`: `pill-type:guardrail` - close every task with its own commit.
- `pill-005`: `pill-type:pattern` - execute active tasks through fresh subagents.
- `pill-007`: `pill-type:guardrail` - force explicit phase gates.
- `pill-durable-pill-knowledge-graduates-to-atoms-at-closeout`: `pill-type:guardrail` - durable pill residue must graduate at closeout.
- `pill-phase-closeout-reconciles-pills-and-surfaces-next-work`: `pill-type:guardrail` - phase closeout must reconcile pills and prepare the next ready work.
- `pill-ready-phases-prove-dependencies-and-non-overlap`: `pill-type:guardrail` - ready phases must prove dependency satisfaction and non-overlap.
- `pill-board-routed-pills-stay-minimal-and-reusable`: `pill-type:guardrail` - board-routed pills should stay minimal and reusable.
