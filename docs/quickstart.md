# deskops Quickstart

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-deskops-owns-workflow-not-document-infrastructure.md`
- `desk/atoms/workflow-model/atom-routine-based-task-execution.md`
- `desk/atoms/workflow-model/atom-phase-gates-prevent-agent-skipping.md`
- `desk/atoms/workflow-model/atom-phases-are-dependency-layers-of-tasks.md`
- `desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md`

Create and close your first desk task without learning SLDB internals first.

In this guide you will install deskops, initialize a repo, create one task, advance it through the workflow, run validation, and close it with a commit.

## What deskops does

`deskops` manages repo-local workflow documents under `desk/`.

A desk task lives in `desk/tasks/`. A task can have a routine, generated checklists, validation commands, and closeout steps. SLDB provides the modeled document layer underneath, but you do not need to understand SLDB to complete this first workflow.

For deeper context, read `README.md` and `docs/faq.md` after this guide.

## Install

From this repo checkout:

```bash
pip install -e .[dev]
```

If you only need the runtime package:

```bash
pip install -e .
```

Run the CLI as `deskops`, not `bash deskops`.

## Bootstrap This Machine

Run bootstrap once per machine when SLDB or the global store may not be ready:

```bash
deskops bootstrap
```

Bootstrap installs or repairs the sibling `../sldb` checkout when needed, creates `~/.sldb`, and registers deskops models in the global store.

## Initialize A Repo

From the target repo root:

```bash
deskops init .
```

This initializes a local `.sldb/` store when needed and scaffolds `desk/`.

If you only need the desk folders without local store setup, use:

```bash
deskops desk install .
```

## Create A Task

Create a first task with a concrete goal and validation command:

```bash
deskops add task \
  --title "Try deskops quickstart" \
  --goal "Complete one task lifecycle" \
  --scope "Documentation walkthrough only" \
  --implementation-path "docs/quickstart.md" \
  --done-when "The quickstart task is validated and closed" \
  --validation "pytest"
```

This creates:

- `desk/tasks/task-try-deskops-quickstart.md`
- a routine under `desk/routines/`
- primitive checklists, conditions, operators, and edges under `desk/primitives/`
- a board entry in `desk/tasks/Board.md`

Check the task:

```bash
deskops list tasks
deskops show task task-try-deskops-quickstart
```

## Advance The Task

Advance the task through its routine:

```bash
deskops advance task task-try-deskops-quickstart
```

Then inspect the result:

```bash
deskops show task task-try-deskops-quickstart
```

The first advance moves the task into active execution. Later advances move it toward testing and closeout when the generated checklist conditions pass.

## Test

Run the validation command named by the task:

```bash
pytest
```

For CLI changes, also run the affected command directly. For graph or store work, prefer semantic checks such as:

```bash
deskops graph missing
```

See `docs/how-to-test-ux-cli.md` and `desk/rituals/testing.md` for deeper testing guidance.

## Close Out

`deskops advance task ...` can move the runtime task status toward `closed` and `complete`, but closeout still requires human cleanup today.

Before calling a task done:

- Confirm validation passed.
- Confirm bound pills and guardrails were satisfied.
- Remove or update stale task/context docs.
- Remove closed tasks from `desk/tasks/Board.md`.
- Untrack the task from the local store if it is tracked.
- Commit the coherent closure.

Use one atomic commit for the completed task:

```bash
git status --short
git add <changed-files>
git commit -m "docs(desk): close quickstart task"
```

See `desk/rituals/phase.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, and `desk/rituals/closeout.md` for the full phase-gated workflow.

## Next References

- `docs/faq.md` - first-use questions and CLI orientation.
- `docs/how-to-test-ux-cli.md` - CLI UX testing guidance.
- `docs/workflow-policy-reference.md` - workflow policy details.
- `desk/contexts/pills.md` - pill taxonomy and subagent context rules.
- `desk/tasks/Board.md` - active task routing.
