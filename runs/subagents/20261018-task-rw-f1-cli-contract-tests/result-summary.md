# Task rw-f1-cli-contract-tests — result

## Changed

- Added `tests/test_cli_contract.py` (new file, tests only; no production code changed).
- Helpers: `_run` (in-process `main([...])` + `capsys`), `_add_contract_atom`, `_fake_herdr_runner` (fake Herdr CLI runner in the style of `tests/test_herdr_runtime.py`), `_stub_herdr` (monkeypatches `deskops.cli.commands.runtime.HerdrClient` and, for init, `deskops.runtime.initializer.HerdrClient`).
- Tests, all using the `lifecycle_desk` fixture from `tests/conftest.py`:
  - `test_add_faq_doc` — `add faq-doc`; asserts `Created faq faq-cli-contract-faq` and the created file.
  - `test_atoms_list` — `atoms list`; asserts `atom-contract-rule | Contract rule`.
  - `test_atoms_show` — `atoms show atom-contract-rule`; asserts `Atom: atom-contract-rule` and `five_wh_one_plus: what`.
  - `test_runtime_init` — `runtime init`; asserts `DeskOps identity: repo; tasks discovered: 0` and `Created Herdr Space: w-1 (repo)`; `ensure_herdr_server` and `HerdrClient` are stubbed.
  - `test_runtime_status_attach_stop[status|attach|stop]` — parametrized; asserts `w-1 | repo | panes=3`, `Focused Herdr Space: w-1 (repo)`, `Closed Herdr Space: w-1 (repo)` and the focus/close calls.
  - `test_runtime_supervise` — `runtime supervise executor --max-iterations 1`; asserts the done lines and `herdr agent wait` call.
- 8 test items total (3 from the parametrized runtime status/attach/stop test).

## Validation

- `PYTHONPATH=/tmp/rw/wt/clicontract python -m pytest tests/test_cli_contract.py -q`
  - Final line: `8 passed in 6.26s` (exit 0).
- `PYTHONPATH=/tmp/rw/wt/clicontract python -m pytest tests -q`
  - Final line: `354 passed, 3 skipped in 284.06s (0:04:44)` (exit 0).

## Unfixed-code run

- Not applicable: the task is tests-only and no production code was modified. No test was run against an unfixed implementation.
- No `xfail` markers or new drawer tasks were needed; all eight surfaces behaved as expected.

## Task inaccuracies / ambiguities

- The task's `Implementation Path` cites `deskops/cli/parser.py:67-89` for the uncovered subcommands; that range covers only `runtime`. The `atoms` subcommands are at `parser.py:113+`, and `add faq-doc` is generated dynamically from `ARTIFACT_SUBJECTS` in `_add_add_commands` (`parser.py:648+`), not a literal parser entry.
- `add faq-doc` is reachable as a generated `add` subject (`artifact.faq` -> `faq-doc`) even though the top-level `faq` command is separate; the test targets the `add faq-doc` surface named in the task.
- `deskops add faq-doc` prints `Created faq <id>` (not `Created faq-doc <id>`); the test asserts the actual stable line.
- No sldb bug observed.
