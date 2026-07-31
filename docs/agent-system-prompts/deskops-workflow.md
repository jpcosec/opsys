---
name: deskops-workflow
description: Use when operating on this repository through deskops. Recover state from the real board at desk/tasks/Board.md, use direct deskops CLI commands, choose one role at a time, and enforce execution, testing, and closeout gates.
---

# Deskops Workflow

Use this skill when doing desk-managed work in this repository.

## What this skill is for

This is an operational skill, not product logic.
It helps the agent recover real repo state from desk artifacts instead of improvising from chat memory.

## Non-negotiables

- The real board is `desk/tasks/Board.md`.
- Use the board selector `Board`.
- Use direct `deskops` CLI commands.
- Choose exactly one role before acting: supervisor, executor, or tester.
- Do not skip execution, testing, or closeout gates.
- Keep scope tight and avoid unrelated cleanup.

## Recovery

Start with:

```bash
deskops show board Board --root .
deskops list tasks --root .
git status --short --branch
```

If a task is active:

```bash
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
```

Read these repo sources as needed:

- `AGENTS.md`
- `README.md`
- `docs/faq.md`
- `desk/tasks/Board.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `.opencode/skills/use-sldb/SKILL.md`

## Core rules

- One bounded task at a time.
- Treat board-routed work as the source of truth.
- Use `sldb` for tracked structured-document operations when applicable.
- Prefer evidence on disk over unsupported claims.
- Do not retire tasks without a dedicated closing commit.

## Useful commands

Inspect state:

```bash
deskops show board Board --root .
deskops list tasks --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
```

Update routing:

```bash
deskops edit board Board tasks '["task-foo"]' --root .
```

Validation examples:

```bash
pytest
sldb stores check --store .sldb
```

## Anti-patterns

Do not:

- use hidden chat context instead of desk recovery
- operate against alternate board files
- bypass `sldb` with ad hoc edits when the document is tracked
- mix supervisor and executor behavior casually
- close from implementation alone without testing and closeout
