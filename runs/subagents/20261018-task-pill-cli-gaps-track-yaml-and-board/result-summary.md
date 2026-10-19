# Result: task-pill-cli-gaps-track-yaml-and-board

## Changes

- `deskops/cli/registry.py` — `_add_subject_commands`: generated `add <artifact>` flags are no longer `required=True`; the model validates the merged (YAML + CLI) payload instead. This makes `--from-yaml` work without per-field flags for every generated artifact subject sharing this path (pill, board, ritual, atom, materialization, repository, inbox-note, faq-doc, step).
- `deskops/operations.py` — `DeskopsOperations._track_created_artifact`: now tracks `artifact.pill` in the local store in addition to `artifact.atom`, inside the creation transaction.
- `deskops/services/retire.py`:
  - `RetireResult` gained `boards: tuple[str, ...]`.
  - `retire_document` computes Board pill unroutings before the inbound-reference check, rewrites each Board through `DeskopsOperations._write_doc(board, BoardDoc, payload)` inside the same `DocTransaction`, then deletes the pill.
  - New helpers: `_pill_reference_matches`, `_board_pill_updates`, `_handled_boards`, `_write_board`.
  - `_inbound_references` gained a `skip` set so a Board whose rewrite removes every reference is not counted as a blocker.
  - Existing `_REQUIRED_STRUCTURE` guard from `4336837` is unchanged.
- `deskops/cli/commands/retire.py` — prints `Unrouted from <board>` for each rewritten Board.
- `tests/test_retire_cli.py` — added `test_add_pill_tracks_the_created_document`, `test_add_pill_from_yaml_needs_no_field_flags`, `test_retire_unroutes_a_board_routed_pill_and_keeps_the_store_green`; updated the existing tracked-pill retire test to drop the `desk update --apply` workaround.
- `tests/fixtures/golden/help/deskops_add_*.txt` — regenerated the `add` help goldens for the removed argparse-required markers.

## Validation

All commands run with `PYTHONPATH=/tmp/rw/wt/pillgaps`.

- `python -m pytest tests/test_retire_cli.py tests/test_cli.py -q`
  - `109 passed in 127.60s (0:02:07)`
- `python -m pytest tests -q`
  - `555 passed, 3 skipped in 735.37s (0:12:15)`
- `python -m pytest tests/test_output_goldens.py::test_help_goldens -q --update-golden` (to regenerate only-affected add help fixtures)
  - `1 passed in 105.89s (0:01:45)`
- Manual CLI flows (`python -m deskops`):
  - `add pill --from-yaml` with no field flags: rc 0, pill created and tracked.
  - `doctor` after `add pill`: rc 0, `Desk is healthy. No issues found.`
  - `retire` of a Board-routed pill: rc 0, printed `Unrouted from desk/tasks/Board.md`, Board pills list emptied, pill and store record removed.
  - `sldb stores check --store <root>/.sldb`: rc 0, `PASS: store integrity`.

## Unfixed-code checks

- Baseline before edits: `PYTHONPATH=/tmp/rw/wt/pillgaps python -m pytest tests/test_retire_cli.py tests/test_cli.py -q` -> `106 passed in 204.04s (0:03:24)`.
- Manual repro on unfixed code: `add pill` followed by `deskops doctor` returned 1 with `Untracked desk documents: desk/contexts/pill-old-guardrail.md`.
- `add pill --from-yaml` without field flags was not executed on unfixed code; the pre-change help golden declared `--what/--why/--when/--where/--how/--how-not` as required (argparse would exit before dispatch).

## Ambiguities / boundaries

- The task says "every Board's `pills` list". Only BoardDoc-modeled boards under `desk/tasks/` (`Board.md` and `board-*.md`) are discovered and rewritten. `desk/drawer/tasks/Board.md` is a free-form, unmodeled board and is not touched.
- "the other artifact subjects if they share the code path": the registry change removes argparse-required flags for all generated `add` artifact subjects, not only pill; their help goldens changed accordingly.
- Only `artifact.atom` and `artifact.pill` are tracked on creation. Other `add` artifacts (e.g. board, ritual) remain untracked as before; not widened.
- No sldb bug found.
