# Self-described store layout

ID: atom-001
5WH1+: what

## Answer

The `.sldb/` workspace separates durable shared state under `core/`, rebuildable execution-time state under `runtime/`, and machine-local overrides under `.config/` so contributors can tell what belongs in git, what can be regenerated, and what should remain local.

## Tags

- system:sldb
- topic:store
- layer:runtime
