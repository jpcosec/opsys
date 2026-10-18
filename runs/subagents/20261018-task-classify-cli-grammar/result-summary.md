# Result summary: task-classify-cli-grammar

## Changed files

- Added `tests/test_cli_grammar.py`.
  - `TOP_LEVEL_GRAMMAR`: `dict[str, frozenset[str]]` with the five categories and exact nouns specified by the task.
  - `test_top_level_nouns_are_classified_exactly_once`: asserts no noun is classified twice and the classified set equals every `command.path[0]` from `command_registry()`.
  - `test_operational_mutates_guards`: asserts `("next",)` and `("show",)` are non-mutating; `("advance",)` and `("closeout",)` are mutating.

No production code changed. `deskops/cli/registry.py` untouched.

## Validation commands and results

- `PYTHONPATH=/tmp/rw/wt/grammar python -m pytest tests/test_cli_grammar.py -q`
  - `2 passed in 0.73s`
- `PYTHONPATH=/tmp/rw/wt/grammar python -m pytest tests/test_command_registry.py -q`
  - `3 passed in 0.57s`
- `PYTHONPATH=/tmp/rw/wt/grammar python -m pytest -q`
  - `462 passed, 3 skipped in 798.51s (0:13:18)`
- `PYTHONPATH=/tmp/rw/wt/grammar python -m pytest tests -q`
  - `462 passed, 3 skipped in 815.94s (0:13:35)`

## Tests against unfixed/unmodified code

- No pre-existing `tests/test_cli_grammar.py`. The new test file was run against the unmodified registry and passed (`2 passed`).
- Drift check: loaded the test module, monkeypatched `command_registry` to add a fake top-level `("newthing",)` command, and called the classification test. Result: `EXPECTED FAILURE: unclassified ('newthing',) rejected`. The guard fails on a new unclassified noun.

## Task inaccuracies / ambiguities

- The task references "the line numbers it cites", but `desk/tasks/task-classify-cli-grammar.md` cites no line numbers.
- The task's expected runtime note in the executor instructions (~3 min for the full suite) does not match this environment: the full suite took ~13.5 minutes, and un-timed runs exceeded 600 s / 900 s before completing. A diagnostic run with `--timeout=60` produced two failures only because `tests/test_output_goldens.py` needs more than 60 s; with no artificial timeout both full runs were green.
- No missing top-level noun was found; the task's mapping already matched all 26 registry top-level nouns.

## sldb issues

None observed or recorded.
