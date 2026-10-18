# deskops Quickstart

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-deskops-owns-workflow-not-document-infrastructure.md`
- `desk/atoms/workflow-model/atom-routine-based-task-execution.md`
- `desk/atoms/workflow-model/atom-phase-gates-prevent-agent-skipping.md`
- `desk/atoms/workflow-model/atom-phases-are-dependency-layers-of-tasks.md`
- `desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md`

Create and close your first desk task without learning SLDB internals first.

In this guide you will install deskops, initialize a repo, create one task, advance it through the workflow, run validation, and close it with `deskops closeout commit`.

## What deskops does

`deskops` manages repo-local workflow documents under `desk/`.

A desk task lives in `desk/tasks/`. A task has validation commands and moves through the desk's lifecycle (execution, testing, closeout), which lives in the desk's sldb graph. SLDB provides the modeled document layer underneath, but you do not need to understand SLDB to complete this first workflow.

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
- a board entry in `desk/tasks/Board.md`

Check the task:

```bash
deskops list tasks
deskops show task task-try-deskops-quickstart
```

## Advance The Task

Advance the task through the lifecycle:

```bash
deskops advance task task-try-deskops-quickstart
```

Then inspect the result:

```bash
deskops show task task-try-deskops-quickstart
```

The first advance moves the task into active execution. Later advances move it toward testing and then to the `ritual-closeout` node when the conditions of the lifecycle transitions hold (`deskops show task` lists them).

`advance` stops at the closeout node. It never closes the task: once the task reaches closeout, the command reports that the task closes with `deskops closeout commit`.

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

`deskops advance task ...` moves the task to the `ritual-closeout` node and stops there. `deskops closeout commit` is the only way to close a task.

Before calling a task done:

- Confirm validation passed.
- Confirm bound pills and guardrails were satisfied.
- Set the task's `files` field to every changed path.
- Set the task's `references` field to test evidence, a link for every changed file, and a commit id that already exists.
- Remove or update stale task/context docs.

Close with the run-linked route, using evidence under `runs/subagents/`:

```bash
deskops closeout commit --task task-try-deskops-quickstart \
  --run-dir runs/subagents/<run-dir>
```

Or close without a subagent run and say why:

```bash
deskops closeout commit --task task-try-deskops-quickstart \
  --no-run --reason "<why the task closes without a run>"
```

For a board-routed task, `closeout commit` runs the full `deskops closeout verify` gate before committing. The gate requires:

- a test evidence reference: an existing `.py` file under `tests/`, optionally with a `::node`, or the `pytest <path>` form;
- a link for every path in the task's `files`: an atom reference, a materialization/graph link to an atom, or a routed follow-up reference under `desk/tasks`, `desk/drawer/tasks`, or `desk/drawer/issues`;
- a commit reference: a lowercase hex commit id that resolves to `HEAD` or an ancestor.

The commit reference must point at an earlier commit that already exists, for example the task's promotion commit. The closing commit is made by `closeout commit` and cannot reference itself.

`closeout commit` then removes the task from `desk/tasks/Board.md`, untracks it from the store, deletes the resolved task document, and makes the one atomic closing commit with the route's trailers.

See `desk/rituals/phase.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, and `desk/rituals/closeout.md` for the full phase-gated workflow.

## Next References

- `docs/faq.md` - first-use questions and CLI orientation.
- `docs/how-to-test-ux-cli.md` - CLI UX testing guidance.
- `docs/workflow-policy-reference.md` - workflow policy details.
- `desk/contexts/pills.md` - pill taxonomy and subagent context rules.
- `desk/tasks/Board.md` - active task routing.
