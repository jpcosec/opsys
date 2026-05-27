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

## Dependency

`deskops` depends on `sldb` as infrastructure. In a local sibling checkout:

```bash
pip install -e ../sldb
pip install -e .[dev]
```

Or run tests directly with the sibling checkout available.

## CLI

Run the installed entrypoint as `deskops`, or use the module form from this repo checkout.

```bash
deskops --help
python -m desk.cli.main --help
```

Current commands:

- `deskops faq`
- `deskops inbox`
- `deskops repo register`
- `deskops desk install`

## Testing

```bash
pytest
```
