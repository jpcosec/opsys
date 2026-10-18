---
atoms:
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-deskops-owns-workflow-not-document-infrastructure
  role: documents
- id: atom-cli-should-match-spoken-workflow-language
  role: documents
- id: atom-inbox-is-coordination-intake
  role: documents
- id: atom-drawers-feed-tasks-through-promotion
  role: documents
- id: atom-available-tasks-are-board-routed-work
  role: documents
---
# deskops FAQ

Source atoms are declared in the YAML frontmatter.

This FAQ is the first-use orientation layer for `deskops`.

`deskops` is the workflow-domain layer that sits on top of `sldb`. It owns the operational workspace surfaces in `desk/`, including tasks, pills, rituals, inbox notes, deferred drawer work, and the repo registry helpers.

## How do I run the CLI correctly?

Use the installed console script `deskops ...`.

You can also run the module form `python -m deskops ...` from this repo checkout.

Do not run `bash deskops ...`. `deskops` is a CLI entrypoint, not a shell script.

Examples:

```bash
deskops --help
deskops faq
python -m deskops --help
```

## What does this repo provide today?

deskops provides a spec-driven artifact pipeline: YAML specs under `deskops/spec/` define every artifact model, fields, and operational behavior. The compiler turns specs into sldb docs at runtime. The CLI is partially derived from specs.

### Core CLI commands

- `deskops about` — short overview and first-use orientation
- `deskops bootstrap` — machine-level sldb and global-store setup
- `deskops init` — initialize a repo-local `.sldb/` plus `desk/`
- `deskops faq` — first-use help (this document)
- `deskops message` — send, list, read, and acknowledge cross-desk messages (`deskops inbox` is a deprecated alias)
- `deskops promote` — move inbox messages and drawer task candidates through explicit workflow promotion steps
- `deskops bind pill` — bind a context pill to an active task through the modeled task surface
- `deskops graph` — build graph snapshots, inspect neighbors, check missing references, and write review-only reflection reports
- `deskops repo register` — canonical repository registration in the ecosystem desk registry, tracked through SLDB
- `deskops desk install` — scaffold a desk surface in a target repository

### Spec-driven artifact commands

**Add artifacts** — `deskops add <artifact> [--flags...]`

Creates structured artifact docs from spec templates. Spec fields populate the artifact model's own fields; they do not create separate desk field-instance documents.

Supported artifact types:

| Subject | Description | Key flags |
|---|---|---|
| `task` | Actionable task, walked through the desk's lifecycle graph | `--title`, `--goal`, `--scope` |
| `pill` | Reusable context document | `--title`, `--what`, `--why` |
| `ritual` | Repeatable procedure template | `--title`, `--purpose`, `--steps` |
| `board` | Task coordination surface | `--title`, `--scope`, `--purpose` |
| `atom` | Durable architectural concept | `--title`, `--five-wh-one-plus`, `--answer` |
| `repository` | Local repository artifact doc; not canonical ecosystem registration | `--name`, `--path`, `--status` |
| `inbox-note` | Incoming project message | `--kind`, `--title`, `--body` |
| `faq-doc` | FAQ entry | (spec-defined flags) |
| `step` | Procedure step | `--title`, `--action`, `--outcome` |

**List artifacts** — `deskops list <artifacts>`

Lists all docs of a given type:

```
deskops list tasks
deskops list atoms
deskops list pills
deskops list inbox-notes
deskops list repositories
...
```

**Show artifacts** — `deskops show <artifact> <doc-id>`

Displays one artifact doc with its model fields:

```
deskops show atom atom-001
deskops show task task-021
deskops show repository repo-deskops
```

**Advance tasks** — `deskops advance task <task-id>`

Fires the next lifecycle transition for the task. The lifecycle is part of the desk's sldb graph: the states are the rituals `ritual-execution`, `ritual-testing` and `ritual-closeout`, and each transition is an sldb `RelationDoc` between two rituals with a `--where` condition on the task (`deskops init` and `deskops desk update --apply` write them under `desk/lifecycle/`). `advance` fires the first transition leaving the task's `current_node` whose condition holds, sets the status it declares, and stops with the blocked gate named when none holds. It stops at `ritual-closeout`: it never closes the task. The only close is `deskops closeout commit --task <task-id> --run-dir <runs/subagents/dir>` or `deskops closeout commit --task <task-id> --no-run --reason <why>`. `deskops show task` lists those gates and whether each holds; `deskops next --diagram` draws the graph.

For a board-routed task, `closeout commit` runs `deskops closeout verify` first. The gate requires test evidence, a link for every path in the task's `files` (an atom reference, a materialization/graph link, or a routed follow-up reference under `desk/tasks`, `desk/drawer/tasks`, or `desk/drawer/issues`), and a commit reference that resolves to `HEAD` or an ancestor. The commit reference must already exist when the gate runs, so point it at an earlier commit such as the task's promotion commit; the closing commit does not exist yet.

**Promote inbox notes** — `deskops promote inbox-to-drawer-task <selector>`

Moves a project-addressed message into the drawer as a loose, deferred candidate, and removes it from the inbox and from the store:

```
deskops promote inbox-to-drawer-task <inbox-note-selector>
```

There is no promotion from the drawer to an active task. The drawer holds loosely shaped material; an active task is a fully authored task document routed by the board. A drawer item becomes active work only when someone authors the task explicitly. `--from-drawer` records the drawer file in the task's own `from_drawer` field, which later edits to `references` cannot overwrite; the drawer file itself is kept and cleaned up by hand:

```
deskops add task --root . --from-drawer <drawer-selector> --title "..." --goal "..." --scope "..." --validation "..."
```

### Generated CLI surface

The `add`, `list`, and `show` subcommands for spec-driven artifacts (atoms, pills, rituals, boards, repositories, inbox-notes, faq-docs, steps) are automatically generated from the artifact registry. When a new artifact type is added to `ARTIFACT_SUBJECTS` in `deskops/operations.py`, subcommands and `--flag` generation follow automatically.

For repository registration, prefer `deskops repo register`. It is the canonical ecosystem registration path because it anchors the repository document in the configured SLDB store. `deskops add repository` only creates a local `desk/registry/repo-*.md` artifact through the generic spec-driven add path.

The models under `deskops.models` and the materializers under `deskops.materializers` are also importable from Python.

Durable workflow guidance lives under `docs/`, including:

- `docs/operator-manual.md`
- `docs/how-to-report.md`
- `docs/how-to-test-ux-cli.md`
- `docs/quickstart.md`
- `docs/faq.md` (this file)

## What is the relationship between `deskops` and `sldb`?

`sldb` is the infrastructure layer.

`deskops` is the workflow-domain layer built on top of that infrastructure. It depends on `sldb` for structured document contracts, validation, store resolution, and tracked-document operations.

## How do I install it for local use?

Install `deskops` from this repo checkout.

```bash
pip install -e .[dev]
```

If `sldb` is not already installed, keep the sibling checkout at `../sldb` and run:

```bash
deskops bootstrap
```

That bootstrap flow installs or repairs `sldb`, creates `~/.sldb` when needed, and registers the deskops model set there.

If you only need the runtime package instead of the dev extras, `pip install -e .` is enough.

## Do I need `--root .` when I am already in the repo?

Usually no.

When you run `deskops` from the target repo root, the local desk is the implied default. Prefer the shorter local form in human-facing examples:

```bash
deskops list tasks
deskops show task task-fix-thing
deskops advance task task-fix-thing
```

Use `--root` when you are intentionally overriding the local default, for example in cross-repo commands, sandbox tests, scripts, or unusual working-directory setups.

## What should I run first in a repo?

Use `deskops init` from the target repo root.

```bash
deskops init .
```

This command ensures `sldb` is available, creates a local `.sldb/` store if it does not already exist, and scaffolds `desk/` if needed.

## Is a store required?

Not for every command.

- `deskops faq` does not require a store.
- `deskops message` can write directly into a repo-local `desk/inbox/` without a store if you pass `--desk-root` or run it from the target project.
- `deskops bootstrap` creates or repairs the global `~/.sldb` store and registers the deskops models there.
- `deskops repo register` and any auto-tracking behavior depend on a resolvable `sldb` store.

If no store is available, commands that depend on registry lookup or tracked-document registration will fail until you provide `--store` or run them from the right project context.

## What is the `desk/` directory for?

`desk/` is the operational workspace for the repo.

It holds active execution surfaces such as task docs, context pills, rituals, inbox notes, and deferred drawer work that should not become permanent documentation by default.

Durable knowledge should eventually land in code, tests, docs, or git history rather than staying only in `desk/`.

## How do I log an unclear point or suggestion?

Use `deskops message send`.

Examples:

```bash
deskops message send "The install flow still leaves a partial scaffold when registration fails" --kind unclear
deskops message send "Add explicit install examples to the README" --kind suggestion --title "README install examples"
deskops message list
deskops message read readme-install-examples
```

Use `--kind unclear` for unresolved confusion and `--kind suggestion` for proposed improvements.

The older `deskops inbox` flag grammar still works as a deprecated alias.

## How do I target another repo's desk?

There are three main targeting modes:

- run inside the target repo so the default local `desk/` is used
- pass `--desk-root` with an explicit desk path
- pass `--to` (or `--repo`) to resolve a repository through the ecosystem registry, optionally with `--store`

If you use `--to`/`--repo`, the target repository must already be registered and discoverable from the chosen store context.

## How do I route sibling repo tasks without copying them?

Register sibling repositories as local repository artifacts, then ask `list tasks` to include repo-routed boards:

```bash
deskops add repository --name "SLDB" --path ../sldb --description "Structured document infrastructure."
deskops list tasks --include-repos
```

`--include-repos` reads `desk/registry/repo-*.md`, resolves each registered repository path, opens that repo's `desk/tasks/Board.md`, and lists only the task files routed by that board. It does not copy sibling task files into the current repo and it does not require those task files to be tracked in SLDB.

This keeps the boundary clear: `deskops` is the current implementation of the broader `opsys` workflow layer, while SLDB remains the modeled Markdown/store layer. Cross-repo mutation, advancement, and closeout are intentionally separate future workflow decisions.

## What does `repo register` do?

It writes a repository registration document into the ecosystem desk registry and tracks it through `sldb` when the `RepositoryDoc` model is registered.

This command is for cross-repo discovery inside the workflow ecosystem, not for generic package publishing.

## What does `desk install` do right now?

It scaffolds a minimal repo-local `desk/` surface in a target repository.

The scaffold creates local `tasks/`, `contexts/`, `rituals/`, `inbox/`, and `drawer/` directories plus starter files for the board, pills, rituals, and drawer README.

It does not auto-register the repository in an ecosystem registry. If you want cross-repo registry discovery, run `deskops repo register ...` as a separate step once the target repo is ready.

## What does `deskops bootstrap` do?

It is the machine-level first-use repair command.

When `sldb` is missing, it installs or repairs it from the sibling `../sldb` checkout. It then initializes the global `~/.sldb` store if needed and registers the deskops model set there.

## What does `deskops init` do?

It is the repo-level first-use command.

It runs the bootstrap preflight, creates a local `.sldb/` store in the target repo if one does not already exist, and scaffolds `desk/` if it is missing.

## How do I organize atoms into folders by a tag namespace?

Set `atom_folder_axis` in `desk/config.json` to one registered tag namespace, for example:

```json
{ "atom_folder_axis": "object" }
```

Behavior (see `desk/atoms/atom-atom-folder-axis-is-one-configurable-tag-namespace.md`):

- `deskops add atom` with one `object:<value>` tag lands in `desk/atoms/<value>/`; dot-notation nests (`object:mepu.licitaciones` → `desk/atoms/mepu/licitaciones/`).
- Atoms without an axis tag, and desks without the config, stay flat (fully backwards compatible).
- Multiple axis values on one atom are rejected with an explicit error.
- `deskops list atoms --axis-value <value>` filters by the axis value; the axis value is shown in list output.
- `deskops atoms reorganize [--dry-run]` idempotently moves existing atoms into their axis folders and retargets tracked paths in the `.sldb` store.

## How do I validate changes in this repo?

Run the test suite from the repo root.

```bash
pytest
```

For CLI work, also run the relevant command directly, for example:

```bash
python -m deskops --help
deskops faq
```
