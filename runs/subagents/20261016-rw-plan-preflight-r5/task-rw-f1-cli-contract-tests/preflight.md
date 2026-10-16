RESTATEMENT:

1. Create `tests/test_cli_contract.py`.
2. Add a fixture that builds a throwaway sandbox repo: `tmp_path`, `git init`, one seed commit, then scaffold `desk/` via `python -m deskops desk install <root>`.
3. Run that install step (in-process `main([...])` under `capsys`, or the subprocess `_cli` helper) — per Resolved Decisions the sandbox build stays as in `tests/test_lifecycle_end_to_end.py` (`_make_repo`, `_cli`), the in-process rule applies to the subcommand under test.
4. Add tests calling `deskops.cli.main.main([...])` in-process with `--root <sandbox>` and `capsys`, one per subcommand:
   - `add hook`
   - `add faq-doc`
   - `atoms list`
   - `atoms show`
   - `runtime init`
   - `runtime status`
   - `runtime attach`
   - `runtime stop`
   - `runtime supervise`
5. Parametrize only groupings whose invocation shape repeats.
6. Each test asserts the exit code and one stable line of stdout/stderr.
7. For the four `runtime` subcommands, stub the Herdr client the same way `tests/test_herdr_runtime.py` does so no Herdr process starts.
8. Run each subcommand first to observe actual behavior; any failure/surprise is out of scope to fix. For each surprise, create a new drawer task file under `desk/drawer/tasks/`, and mark that subcommand's test `@pytest.mark.xfail(strict=True, reason='<new task id>')` instead.
9. Verify no test mutates the repo's real `desk/`.
10. Run `pytest tests/test_cli_contract.py`, then `pytest tests`; both must be green. Do not commit (supervisor commits).

AMBIGUITIES:

1. "One stable line of output" is undefined: no target strings, no exit codes (presumably 0) given for any of the 9 subcommands.
2. Required arguments/flags for `add hook` and `add faq-doc` are not specified (positional names, `--root` only, other required options).
3. `atoms show` needs an atom id, and `atoms list`/`atoms show` need atoms to exist in the sandbox; which seed atom ids are guaranteed after `desk install` is not stated.
4. Whether `--root` is a global option accepted before the subcommand, after it, or supported at all by `add hook`, `add faq-doc`, `atoms list`, `atoms show`, and the `runtime` verbs is not stated.
5. Whether `main(argv)` returns an int or raises `SystemExit` (affects how exit codes are asserted) is not stated.
6. Tension between Implementation Path step 1 ("fixture ... runs `desk install`") and Resolved Decisions ("a task that says 'in-process' calls `main` ... with `capsys`") on whether the fixture's install step is in-process or subprocess.
7. Which of the four `runtime` verbs actually need the Herdr stub, and the exact monkeypatch target/symbol, is not stated ("the way tests/test_herdr_runtime.py does" is the only pointer).
8. Whether `runtime init|status` are expected to succeed in a bare sandbox or are expected to fail (thus xfail) is not stated.
9. Exact `desk/drawer/tasks/` filename convention and required frontmatter for the new surprise tasks are not stated.
10. Whether to xfail preemptively when behavior is guessed wrong vs. only after observing a real failing/surprising assertion is not stated, nor how the reason string ties to the new task id.
11. No criteria for "where the shape repeats" for parametrization, so the grouping is a guess.
12. Whether stderr is acceptable as the "stable line" (e.g. error output) is not stated.
13. Whether `--root` for `runtime` verbs points at the desk root or the repo root is not stated.
