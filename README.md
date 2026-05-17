# Opsys

Workflow-domain instance built on top of `sldb`.

This repo owns the operational surfaces that should not live inside generic `sldb` infrastructure: `desk/`, deferred drawer work, workflow-native models, pills, rituals, atoms, and materializers.

## Layout

- `desk/` - active and deferred workflow surfaces
- `docs/` - durable opsys-specific documentation
- `tests/` - workflow-domain tests

## Dependency

`opsys` depends on `sldb` as infrastructure. In a local sibling checkout:

```bash
pip install -e ../sldb
pip install -e .[dev]
```

Or run tests directly with the sibling checkout available.

## Testing

```bash
pytest
```
