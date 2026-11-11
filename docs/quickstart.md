---
atoms:
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-deskops-owns-workflow-not-document-infrastructure
  role: documents
- id: atom-routine-based-task-execution
  role: documents
- id: atom-phase-gates-prevent-agent-skipping
  role: documents
- id: atom-phases-are-dependency-layers-of-tasks
  role: documents
- id: atom-code-changes-close-with-tests-and-commit
  role: documents
- id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
  role: documents
---
# deskops Quickstart

Source atoms are declared in the YAML frontmatter.

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

Create a first task with a concrete goal, a validation command, and the evidence it will close with:

```bash
deskops add task \
  --title "Try deskops quickstart" \
  --task-type task.docs \
  --goal "Complete one task lifecycle" \
  --scope "Documentation walkthrough only" \
  --implementation-path "docs/quickstart.md" \
  --done-when "The quickstart task is validated and closed" \
  --validation "pytest"
```

Every task's type declares how it closes. `--task-type task.docs` declares `commit` and `document`: this walkthrough changes no code, so a resolvable commit and an existing document are what closeout will check. A code task uses `--task-type task.code` (tests, commit, and an atom or materialization link). `--evidence <kind>...` (`tests`, `commit`, `atom`, `materialization`, `document`, `external`) only adds kinds to the type's, never removes one. Without `--task-type` the type is `task.code`.

This creates:

- `desk/tasks/task-try-deskops-quickstart.md`
- a board entry in `desk/tasks/Board.md`

Check the task:

```bash
deskops list tasks
deskops show task task-try-deskops-quickstart
```

## Review The Contract

A task leaves `ritual-execution` only with the review receipts its type asks for (`deskops show task` names them under "Lifecycle gates"). A `task.docs` task needs an accepted `preflight` receipt; a `task.code` task needs `preflight` and `bundle`. On a desk where the reviewer model runs, `deskops review preflight task-try-deskops-quickstart` writes it. Where no model is available, as in this walkthrough, you review the task's contract yourself and record a human receipt that names you as the operator, then dispose of it:

```bash
deskops review record task-try-deskops-quickstart --kind preflight --operator "Your Name" \
  --evidence desk/tasks/task-try-deskops-quickstart.md --reason "Read the contract; nothing ambiguous"
deskops review dispose review-task-try-deskops-quickstart-preflight-1 --verdict accepted --reason "Contract reviewed by the operator"
```

The receipt keeps `engine: human` and says `no model available`, so nobody mistakes it for a model review.

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

`advance` stops at the closeout node and exits 1 there. It never closes the task: while the declared closeout evidence is missing it names the blocked gate; once the evidence verifies, it reports that the task closes with `deskops closeout commit`.

## Test

Run the validation command named by the task:

```bash
pytest
```

The validation command is the task's own check; it is not what the closeout gate reads. The gate asks for a test file reference only when the task's type declares `tests` (every `task.code` task does). This docs task's type declares none, so the `pytest` run above is validation, not closeout evidence.

For CLI changes, also run the affected command directly. For graph or store work, prefer semantic checks such as:

```bash
deskops graph missing
```

See `docs/how-to-test-ux-cli.md` and `desk/rituals/testing.md` for deeper testing guidance.

## Close Out

`deskops advance task ...` moves the task to the `ritual-closeout` node and stops there. A task closes only through `deskops closeout`: `closeout commit` for work that was done, `closeout supersede` when the task's subject no longer exists, and `closeout retire` for a task that was already resolved before the ritual lifecycle (both take `--reason` and `--ref`, skip the evidence gates, and still make one closing commit).

Before calling a task done:

- Confirm validation passed.
- Confirm bound pills and guardrails were satisfied.
- Set the task's `files` field to every changed path.
- Set the task's `references` field to the evidence the task declared: here a commit id that already exists and the document that changed (`docs/quickstart.md`).
- Remove or update stale task/context docs.

First verify. `deskops closeout verify` checks the evidence the task declared and writes one `ReviewDoc` evidence receipt per kind, anchored to the task's contract:

```bash
deskops closeout verify --task task-try-deskops-quickstart
```

Then close with the run-linked route, using evidence under `runs/subagents/`:

```bash
deskops closeout commit --task task-try-deskops-quickstart \
  --run-dir runs/subagents/<run-dir>
```

Or close without a subagent run and say why:

```bash
deskops closeout commit --task task-try-deskops-quickstart \
  --no-run --reason "<why the task closes without a run>"
```

`closeout commit` does not write receipts: it evaluates the task type's closeout rule over the receipts `closeout verify` wrote. If one is missing, not accepted, or no longer intact (the task changed after verify), the commit stops, names the rule's clause, and tells you to run `deskops closeout verify` again. Verify checks exactly what the task's type declares (plus what `--evidence` added), nothing more and nothing less, and prints `esta tarea declaró X; encontré Y` (declared X; found Y). The vocabulary:

- `tests`: an existing `.py` file under `tests/`, optionally with a `::node`, or the `pytest <path>` form;
- `commit`: a lowercase hex commit id that resolves to `HEAD` or an ancestor;
- `atom` / `materialization`: one gate with two ways to pass it: an atom reference, or a link for every path in the task's `files` (a materialization/graph link to an atom, or a routed follow-up reference under `desk/tasks`, `desk/drawer/tasks`, or `desk/drawer/issues`). It is exempt in a desk without local atom documents;
- `document`: an existing document file (`.md`, `.rst`, `.txt`, `.adoc`, `.yaml`) in `references` or `files`, outside `tests/` and `desk/tasks/`;
- `external`: an `http(s)` URL in `references`, for work tracked outside the repository.

The task's type declares the evidence: `task.code` and `task.debug` declare tests, commit, and atom|materialization; `task.docs` and `task.decision` declare commit and document; `task.external` declares external. `--evidence` only adds kinds to the type's. Changed `.py` files in a task whose type did not declare `tests` do not block closeout, but the gate prints a visible alert. A task created before the types existed is gated as code, with an alert asking its owner to declare the evidence (`deskops edit task <id> closeout_evidence '["commit", "document"]'`).

The commit reference must point at an earlier commit that already exists, for example the task's authoring commit. The closing commit is made by `closeout commit` and cannot reference itself.

`closeout commit` then removes the task from `desk/tasks/Board.md`, untracks it from the store, deletes the resolved task document, and makes the one atomic closing commit with the route's trailers.

See `desk/rituals/phase.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, and `desk/rituals/closeout.md` for the full phase-gated workflow.

## Next References

- `docs/faq.md` - first-use questions and CLI orientation.
- `docs/how-to-test-ux-cli.md` - CLI UX testing guidance.
- `docs/workflow-policy-reference.md` - workflow policy details.
- `desk/contexts/pills.md` - pill taxonomy and subagent context rules.
- `desk/tasks/Board.md` - active task routing.
