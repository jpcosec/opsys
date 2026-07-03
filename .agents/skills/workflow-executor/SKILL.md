---
name: workflow-executor
description: Use when acting as the executor for one bounded deskops task in this repository. Recover board and task state, implement only the assigned scope, persist run evidence, run the smallest relevant validation first, and hand off without self-retirement.
---

# Workflow Executor

Use this skill when your role is **executor**.

## Non-negotiables

- Implement one bounded task only.
- Recover state from `Board` before changing files.
- Keep evidence on disk under `runs/subagents/` when doing non-trivial work.
- Run the smallest relevant validation first.
- Do not self-retire the task.

## Recovery

```bash
deskops show board Board --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
git status --short --branch
```

## Executor duties

- read the assigned task
- read bound references, pills, and files
- confirm exact touched surfaces
- snapshot desk and git state into run evidence
- implement only task scope
- run focused validation first
- write a result summary for handoff

## Evidence snapshot pattern

```bash
TS="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="runs/subagents/$TS-<task-id>"
mkdir -p "$RUN_DIR"

deskops show board Board --root . > "$RUN_DIR/board.txt"
deskops show task <task-id> --root . > "$RUN_DIR/task.txt"
deskops next <task-id> --root . > "$RUN_DIR/next.txt"
deskops graph missing --root . > "$RUN_DIR/graph.txt"
git status --short --branch > "$RUN_DIR/git-status.txt"
```

## Validation discipline

Prefer the smallest meaningful proof first.

Examples:

```bash
pytest tests/<targeted-scope> -q
pytest
sldb stores check --store .sldb
```

If the change touches tracked structured docs or models, also use `.skills/sldb/SKILL.md`.

## Required outputs

- `board.txt`
- `task.txt`
- `next.txt`
- `graph.txt`
- `git-status.txt`
- `result-summary.md`
- `validation.log` when applicable

## Anti-patterns

Do not:

- expand into other tasks
- change board routing casually
- claim closeout is done
- skip validation evidence
- rewrite unrelated files because they are already dirty
