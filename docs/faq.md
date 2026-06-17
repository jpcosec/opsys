# deskops FAQ

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

deskops provides a spec-driven artifact pipeline: YAML specs under `spec/` define every artifact model, fields, and operational behavior. The compiler turns specs into sldb docs at runtime. The CLI is partially derived from specs.

### Core CLI commands

- `deskops about` — short overview and first-use orientation
- `deskops bootstrap` — machine-level sldb and global-store setup
- `deskops init` — initialize a repo-local `.sldb/` plus `desk/`
- `deskops faq` — first-use help (this document)
- `deskops inbox` — write and browse desk inbox notes
- `deskops promote` — move inbox messages and drawer task candidates through explicit workflow promotion steps
- `deskops graph` — build graph snapshots, inspect neighbors, check missing references, and write review-only reflection reports
- `deskops repo register` — canonical repository registration in the ecosystem desk registry, tracked through SLDB
- `deskops desk install` — scaffold a desk surface in a target repository

### Spec-driven artifact commands

**Add artifacts** — `deskops add <artifact> [--flags...]`

Creates structured artifact docs from spec templates. Spec fields populate the artifact model's own fields; they do not create separate desk field-instance documents.

Supported artifact types:

| Subject | Description | Key flags |
|---|---|---|
| `task` | Actionable task bundle with routine | `--title`, `--goal`, `--scope` |
| `pill` | Reusable context document | `--title`, `--what`, `--why` |
| `ritual` | Repeatable procedure template | `--title`, `--purpose`, `--steps` |
| `board` | Task coordination surface | `--title`, `--scope`, `--purpose` |
| `atom` | Durable architectural concept | `--title`, `--five-wh-one-plus`, `--answer` |
| `repository` | Local repository artifact doc; not canonical ecosystem registration | `--name`, `--path`, `--status` |
| `inbox-note` | Incoming project message | `--kind`, `--title`, `--body` |
| `faq-doc` | FAQ entry | (spec-defined flags) |
| `step` | Procedure step | `--title`, `--action`, `--outcome` |
| `condition` | Primitive: predicate guard | `--title`, `--subject`, `--predicate` |
| `operator` | Primitive: state transition | `--title`, `--action`, `--target` |
| `checklist` | Primitive: completion items | `--title`, `--items`, `--mode` |
| `hook` | Primitive: side-effect trigger | `--title`, `--event`, `--target-ref` |
| `edge` | Primitive: routine graph edge | `--title`, `--source`, `--target-node` |
| `routine` | Primitive: procedure graph | `--title`, `--entrypoint`, `--decomposition` |

**List artifacts** — `deskops list <artifacts>`

Lists all docs of a given type:

```
deskops list tasks
deskops list atoms
deskops list pills
deskops list inbox-notes
deskops list repositories
deskops list conditions
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

Walks a task through its routine: evaluates current checklists, checks edge conditions, and transitions to the next node via the matching operator.

**Promote workflow items** — `deskops promote <promotion> <selector>`

Moves project-addressed messages and deferred drawer work through explicit steps without silently deleting the source artifact:

```
deskops promote inbox-to-drawer-task <inbox-note-selector>
deskops promote drawer-task-to-active-task <drawer-task-selector>
```

### Generated CLI surface

The `add`, `list`, and `show` subcommands for spec-driven artifacts (atoms, pills, rituals, boards, repositories, inbox-notes, faq-docs, steps) are automatically generated from the artifact registry. When a new artifact type is added to `ARTIFACT_SUBJECTS` in `deskops/operations.py`, subcommands and `--flag` generation follow automatically.

For repository registration, prefer `deskops repo register`. It is the canonical ecosystem registration path because it anchors the repository document in the configured SLDB store. `deskops add repository` only creates a local `desk/registry/repo-*.md` artifact through the generic spec-driven add path.

The models under `deskops.models` and the materializers under `deskops.materializers` are also importable from Python.

Durable workflow guidance lives under `docs/`, including:

- `docs/how-to-report.md`
- `docs/how-to-test-ux-cli.md`
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

## What should I run first in a repo?

Use `deskops init` from the target repo root.

```bash
deskops init .
```

This command ensures `sldb` is available, creates a local `.sldb/` store if it does not already exist, and scaffolds `desk/` if needed.

## Is a store required?

Not for every command.

- `deskops faq` does not require a store.
- `deskops inbox` can write directly into a repo-local `desk/inbox/` without a store if you pass `--desk-root` or run it from the target project.
- `deskops bootstrap` creates or repairs the global `~/.sldb` store and registers the deskops models there.
- `deskops repo register` and any auto-tracking behavior depend on a resolvable `sldb` store.

If no store is available, commands that depend on registry lookup or tracked-document registration will fail until you provide `--store` or run them from the right project context.

## What is the `desk/` directory for?

`desk/` is the operational workspace for the repo.

It holds active execution surfaces such as task docs, context pills, rituals, inbox notes, and deferred drawer work that should not become permanent documentation by default.

Durable knowledge should eventually land in code, tests, docs, or git history rather than staying only in `desk/`.

## How do I log an unclear point or suggestion?

Use `deskops inbox`.

Examples:

```bash
deskops inbox "The install flow still leaves a partial scaffold when registration fails" --kind unclear
deskops inbox "Add explicit install examples to the README" --kind suggestion --title "README install examples"
deskops inbox --list
deskops inbox --show readme-install-examples
```

Use `--kind unclear` for unresolved confusion and `--kind suggestion` for proposed improvements.

## How do I target another repo's desk?

There are three main targeting modes:

- run inside the target repo so the default local `desk/` is used
- pass `--desk-root` with an explicit desk path
- pass `--repo` to resolve a repository through the ecosystem registry, optionally with `--store`

If you use `--repo`, the target repository must already be registered and discoverable from the chosen store context.

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
