# deskops

Workflow-domain instance built on top of `sldb`.

This repo owns the operational surfaces that should not live inside generic `sldb` infrastructure: `desk/`, deferred drawer work, workflow-native models, pills, rituals, atoms, and materializers.

## Layout

- `desk/` - active and deferred workflow surfaces
- `docs/` - durable deskops-specific documentation
- `tests/` - workflow-domain tests

Durable guides currently include:

- `docs/how-to-report.md`
- `docs/how-to-test-ux-cli.md`

## Install

Install `deskops` from this repo checkout:

```bash
pip install -e .[dev]
```

If `sldb` is not already available on the machine, `deskops` can bootstrap it from the sibling checkout at `../sldb`.

Recommended first-use flow:

```bash
deskops bootstrap
deskops init .
```

`deskops bootstrap` will:

- install or repair `sldb` from the sibling checkout when it is missing
- initialize the global store at `~/.sldb` when needed
- register the `deskops` models into that global store

`deskops init <path>` will:

- ensure the bootstrap prerequisites are ready
- create a local `.sldb/` store under the target repo when missing
- scaffold `desk/` when missing

## CLI

Run the installed entrypoint as `deskops`, or use the module form from this repo checkout.

```bash
deskops --help
python -m deskops --help
```

Current commands:

- `deskops about`
- `deskops bootstrap`
- `deskops init`
- `deskops faq`
- `deskops inbox`
- `deskops repo register`
- `deskops desk install`

## Testing

```bash
pytest
```
