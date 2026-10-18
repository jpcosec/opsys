# Result summary: end-to-end deskops operator manual

## What changed

- `docs/operator-manual.md` (new): end-to-end operator playbook for people and agents. Covers every top-level CLI verb and every subcommand: setup/bootstrap/init, orientation, doctor/status, lifecycle inspection, repo identity/registration, desk install/migrate/update, all `add`/`edit`/`list`/`show` artifact subjects, pills/binding, message/inbox/promote/drawer, tasks, closeout, issues, the full `atoms` family, `graph`, `materialize`, `drift check`, and `runtime`/Herdr. 27 blocks are marked `bash runnable`; expected-failure and Herdr-only examples are plain `bash`.
- `tests/test_operator_manual.py` (new): extracts `^```bash runnable` blocks in document order and runs each through `bash --noprofile --norc -eo pipefail -c` in one sandbox repository under `tmp_path`. The sandbox has its own `HOME`, `XDG_CACHE_HOME`, git identity, seed commit, and a `deskops` shim that runs `sys.executable -m deskops` from this checkout. A failure reports block index, block text, stdout and stderr. Requires at least 15 runnable blocks.
  - Helpers: `_runnable_blocks`, `_git`, `_sandbox`; test: `test_operator_manual_runnable_examples_execute_in_order`.
- `README.md`: added `docs/operator-manual.md` to the durable-guides list.
- `docs/faq.md`: added `docs/operator-manual.md` to the durable-workflow-guidance list.
- `deskops/data/faq.md`: synchronized byte-for-byte with `docs/faq.md` (required by `tests/test_packaging.py`).

No production code changed. No commit, no `git add`, and no desk-mutating command was run against this worktree.

## Validation commands and results

Baseline (new test before the manual existed, same checkout):

```text
PYTHONPATH=/tmp/rw/wt/manual python -m pytest tests/test_operator_manual.py -q
1 failed in 0.03s
Failed: operator manual is missing: /tmp/rw/wt/manual/docs/operator-manual.md
```

Manual test alone after implementation:

```text
PYTHONPATH=/tmp/rw/wt/manual python -m pytest tests/test_operator_manual.py -q
1 passed in 102.49s (0:01:42)
```

After the final test-helper cleanup:

```text
PYTHONPATH=/tmp/rw/wt/manual python -m pytest tests/test_operator_manual.py -q
1 passed in 107.00s (0:01:47)
```

Full suite (first run, before the final helper cleanup):

```text
PYTHONPATH=/tmp/rw/wt/manual python -m pytest tests -q
461 passed, 3 skipped in 1037.19s (0:17:17)
```

Full suite (rerun after the final test-helper cleanup):

```text
PYTHONPATH=/tmp/rw/wt/manual python -m pytest tests -q
461 passed, 3 skipped in 881.25s (0:14:41)
```

CLI and semantic checks:

```text
PYTHONPATH=/tmp/rw/wt/manual python -m deskops --help
EXIT=0

PYTHONPATH=/tmp/rw/wt/manual python -m deskops faq
EXIT=0

sldb stores check --store .sldb
EXIT=0
# exit 0 with pre-existing informational "headings sin declarar" notes for inbox/atom docs

PYTHONPATH=/tmp/rw/wt/manual python -m deskops graph missing
EXIT=1
# 2 missing, 113 informational
# both failing findings are pre-existing source-file references from
# task:task-message-delivery-resolves-unregistered-desks to tests/test_message_delivery.py
```

## Findings, ambiguities, and out-of-scope observations

- The task document cites no line numbers, so there were none to re-verify. All examples were verified against `python -m deskops --help` and each subcommand's `--help`.
- `deskops closeout verify` intentionally has a non-runnable failure example: the runner requires every runnable block to exit 0.
- The materialization example targets `desk/tasks/Board.md` because `--target-identity` must resolve to an existing graph node in the sandbox. Targeting a not-yet-created `docs/operator-manual.md` makes `graph missing` exit 1, which is correct but would break the runnable sequence.
- Pre-existing deskops behavior, not fixed (out of scope): generic `deskops add <subject>` only tracks `artifact.atom` in SLDB. `DeskopsOperations._track_created_artifact` (`deskops/operations.py:1131`) returns for every other subject, so `deskops doctor` after adding pills/rituals/boards/FAQ/step/repository reports "Untracked desk documents". `deskops desk update --apply` tracks them but can still exit 1 while atom hash drift remains. The manual therefore runs `doctor` before bulk artifact creation and does not promise a green doctor after it.
- Pre-existing graph drift in this repo is unrelated to the change: `deskops graph missing` reports two missing `tests/test_message_delivery.py` targets from `desk/tasks/task-message-delivery-resolves-unregistered-desks.md`.
- No SLDB bug found. `sldb stores check --store .sldb` exited 0; its output contained only informational heading warnings.
