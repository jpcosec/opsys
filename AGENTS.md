# Agent Onboarding

This file is the first stop for agents working in this repository. It is a routing document, not the full operator manual.

## Startup Route

Read in this order before changing files:

1. `README.md` for repository purpose, install flow, and tool boundaries.
2. `docs/faq.md` for first-use CLI orientation.
3. `desk/tasks/Board.md` for active routing, board pills, and rituals.
4. The board-routed pills under `desk/contexts/` that match the task.
5. `desk/rituals/execution.md`, `desk/rituals/testing.md`, and `desk/rituals/closeout.md` for phase gates.
6. Relevant atoms under `desk/atoms/`, preferably found through `sldb find` or graph commands rather than raw scanning.

If the active board does not route a task, do not treat fixture-looking files in `desk/tasks/` as real work by default. Use `desk/drawer/tasks/Board.md` for deferred backlog, and promote drawer work before implementation.

## Core Boundaries

- `deskops/` contains Python implementation code.
- `desk/` contains workflow document data: tasks, pills, rituals, atoms, inbox notes, drawer items, routines, and primitives.
- SLDB owns structured Markdown infrastructure, model contracts, reversible templates, stores, field queries, and safe document edits.
- KGDB owns graph contracts and graph runtime validation.
- Spec2viz owns structured diagram sources and generated diagram projections.

Do not add desk-local field documents to duplicate SLDB field behavior. If an expected SLDB path fails, capture the gap in the sibling `sldb` repo inbox first, then route an explicit desk task before building a deskops workaround.

## Working Rules

- Start with ambiguity review. If a task would require improvisation, record or resolve the ambiguity before implementation.
- Keep one coherent deliverable per task.
- For active desk tasks, run the execution-ritual fresh-context subagent review before implementation. Use additional subagents for broad exploration when the task is non-trivial.
- Bind relevant pills by checking `when`, `where`, and `how_not`, not just titles.
- Do not skip from implementation to closeout. Pass execution, testing, and closeout gates explicitly.
- Keep changes small and scoped. Do not clean unrelated dirty worktree changes.
- Every closed task ends with its own atomic commit.

## Validation

Minimum validation for code changes:

```bash
pytest
```

For CLI changes, also run the affected command directly, for example:

```bash
python -m deskops --help
deskops faq
```

For graph or store work, prefer semantic checks:

```bash
sldb stores check --store .sldb
deskops graph missing --root .
```

## Selected Source Documents

- `README.md`
- `docs/faq.md`
- `docs/workflow-policy-reference.md`
- `docs/how-to-test-ux-cli.md`
- `.skills/sldb/SKILL.md`
- `.opencode/skills/use-deskops/SKILL.md`
- `desk/tasks/Board.md`
- `desk/drawer/tasks/Board.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/contexts/pill-001-task-closure-commit.md`
- `desk/contexts/pill-005-subagent-execution.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/atoms/workflow-model/atom-first-safe-action-follows-read-route.md`
- `desk/atoms/workflow-model/atom-clean-agents-start-from-minimum-workflow-set.md`
- `desk/atoms/workflow-model/atom-agents-read-by-decision-need.md`
- `desk/atoms/workflow-model/atom-agents-read-through-semantic-tools.md`
- `desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md`
- `desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md`
- `desk/atoms/workflow-model/atom-phase-gates-prevent-agent-skipping.md`

The broader manual is deferred in `desk/drawer/tasks/task-write-end-to-end-operator-manual.md`.
