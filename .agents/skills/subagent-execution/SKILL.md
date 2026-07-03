---
name: subagent-execution
description: Use when launching a bounded execution subagent for a deskops task in this repository. Recover desk state first, create run evidence, launch one task-scoped execution lane, and keep execution separate from closeout.
---

# Subagent Execution

Use this skill when launching an execution subagent for one bounded task.

## Non-negotiables

- Launch only one bounded task.
- Recover desk state first.
- Snapshot evidence directly from deskops and git.
- Keep execution separate from retirement.
- Treat terminal orchestration tools as optional outer layers, not workflow logic.

## Preconditions

```bash
deskops show board Board --root .
deskops list tasks --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
git status --short --branch
```

Do not launch if:

- the task is not active
- scope is unclear
- allowed files are unclear
- the worktree is contaminated with unrelated generated junk

## Create run evidence

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

Also write a short brief:

```bash
cat > "$RUN_DIR/brief.md" <<'EOF'
Role: executor
Task: <task-id>
Rules:
- stay within task scope
- do not expand into other tasks
- persist evidence
- run focused validation first
- hand off instead of self-retiring
EOF
```

## Launch contract

The launched lane should be told to:

- read the task and bound references
- recover desk state before edits
- implement only task scope
- save `stdout.log` and `stderr.log`
- write `result-summary.md`
- save `validation.log` when tests are run

## Required outputs

- `board.txt`
- `task.txt`
- `next.txt`
- `graph.txt`
- `git-status.txt`
- `brief.md`
- `stdout.log`
- `stderr.log`
- `result-summary.md`
- `validation.log` when applicable

## Anti-patterns

Do not:

- launch from hidden chat context alone
- run multiple tasks in one execution burst
- mutate board state from the execution lane
- close or delete the task from the execution lane
