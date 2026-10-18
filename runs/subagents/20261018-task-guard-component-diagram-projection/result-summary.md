# guard-component-diagram-projection — result summary

## Changes

- Added `tests/test_diagram_projections.py`.
  - `_normalize()` strips trailing whitespace per line and trailing newlines.
  - `_first_fenced_mermaid_block()` extracts the first ` ```mermaid ... ``` ` block with `re.DOTALL | re.MULTILINE`.
  - `test_components_diagram_markdown_matches_mmd_source()` compares the block in `docs/diagrams/codebase/sldb-primitives-docs-cli-components.md` against `docs/diagrams/codebase/sldb-primitives-docs-cli-components.mmd`.
  - Docstring records that spec2viz migration is deferred until a spec2viz source workflow exists in this repo.
- No diagram files changed: the `.md` block and `.mmd` source were already identical.
- No desk/ command was run and no desk file was edited.

## Validation

- `PYTHONPATH=/tmp/rw/wt/compdiag python -m pytest tests/test_diagram_projections.py -q`
  - `1 passed in 0.02s`
- `PYTHONPATH=/tmp/rw/wt/compdiag python -m pytest tests -q`
  - `461 passed, 3 skipped in 954.10s (0:15:54)` (exit 0)
  - `pyproject.toml` sets `testpaths = ["tests"]`, so this is the task's `pytest -q` command.

## Negative check against unfixed state

- Temporarily appended `    extra -->|drift| store` to the `.mmd` source, ran the new test, then restored the file byte-for-byte (verified with `git status`: only the new test is untracked).
  - Result: `1 failed` — `AssertionError: ... fenced mermaid block drifted from ... .mmd`.
  - The equality test therefore fails if either side changes alone.

## Task issues / ambiguity

- None. Task cites no line numbers, so no stale references.
- No sldb bug observed.
- Full-suite runtime was ~16 minutes rather than ~3, because several concurrent pytest runs from other worktrees were competing for CPU; per-test results were unaffected.
