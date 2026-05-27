# deskops FAQ

This FAQ is the first-use orientation layer for `deskops`.

`deskops` is the workflow-domain layer that sits on top of `sldb`. It owns the operational workspace surfaces in `desk/`, including tasks, pills, rituals, inbox notes, deferred drawer work, and the repo registry helpers.

## How do I run the CLI correctly?

Use the installed console script `deskops ...`.

You can also run the module form `python -m desk.cli.main ...` from this repo checkout.

Do not run `bash deskops ...`. `deskops` is a CLI entrypoint, not a shell script.

Examples:

```bash
deskops --help
deskops faq
python -m desk.cli.main --help
```

## What does this repo provide today?

The current public CLI surface is intentionally small:

- `deskops faq` for first-use help
- `deskops inbox` for writing and browsing desk inbox notes
- `deskops repo register` for registering repositories in the ecosystem desk registry
- `deskops desk install` for scaffolding a desk surface in a target repository

The models under `desk/models/` and the materializers under `desk/materializers/` are also importable from Python.

Durable workflow guidance lives under `docs/`, including:

- `docs/how-to-report.md`
- `docs/how-to-test-ux-cli.md`

## What is the relationship between `deskops` and `sldb`?

`sldb` is the infrastructure layer.

`deskops` is the workflow-domain layer built on top of that infrastructure. It depends on `sldb` for structured document contracts, validation, store resolution, and tracked-document operations.

## How do I install it for local use?

In the current workspace setup, install `sldb` first from a sibling checkout and then install `deskops`.

```bash
pip install -e ../sldb
pip install -e .[dev]
```

If you only need the runtime package instead of the dev extras, `pip install -e .` is enough.

## Is a store required?

Not for every command.

- `deskops faq` does not require a store.
- `deskops inbox` can write directly into a repo-local `desk/inbox/` without a store if you pass `--desk-root` or run it from the target project.
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

It scaffolds an initial `desk/` surface in a target repository and then tries to register that repository in the ecosystem registry.

This command currently assumes a compatible `sldb` store context for the registration step. If that prerequisite is missing, the scaffold step may succeed before registration fails.

## How do I validate changes in this repo?

Run the test suite from the repo root.

```bash
pytest
```

For CLI work, also run the relevant command directly, for example:

```bash
python -m desk.cli.main --help
deskops faq
```
