RESTATEMENT:
1. Verify the 10 `depends_on` tasks are closed; if not, stop (task is `status: deferred`).
2. Read `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` and `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`; bind by `when`/`where`/`how_not`.
3. Read `runs/planning/deskops-rewrite-inventory.md` ("Contrato a preservar" item 2) to enumerate surfaces.
4. Read `tests/test_herdr_runtime.py` to copy its Herdr-client stubbing pattern.
5. Create `tests/test_cli_contract.py`.
6. Add a fixture using `tmp_path` that builds a sandbox desk via `deskops desk install`.
7. Write one test per surface, each calling `deskops.cli.main.main(argv)`, capturing stdout/stderr, asserting exit code + one stable output line:
   - `runtime *`
   - `closeout commit` (through `main`)
   - `atoms type`, `atoms list`, `atoms show`
   - `add board|faq-doc|ritual|step|operator|checklist|hook|edge`
   - `bind`
8. Stub the Herdr client in `runtime` tests (no real session).
9. For each failure/surprise: create a new drawer task under `desk/drawer/tasks/`, then mark the test `xfail(strict=True)` referencing that task id.
10. Run `pytest tests/test_cli_contract.py`.
11. Run `pytest tests`.
12. Confirm every listed surface appears in ≥1 test and suite is green.

AMBIGUITIES:
1. Dependencies listed but their statuses are not given; unclear whether I may proceed now.
2. `runtime *` wildcard is not enumerated; which subcommands count as "covered" is undefined.
3. Exact `argv` for each surface (subcommands, flags, positional args) is unspecified.
4. "Stable line of output" is undefined; no output contract is quoted.
5. Expected exit code per surface (0 vs. specific errors) not given.
6. `deskops desk install` invocation (arguments, target dir, git init, committed state) is unspecified.
7. Herdr stubbing described only by reference to a file I cannot read in zero-context.
8. `closeout commit` presumably needs git state/commits in the sandbox; requirements not stated.
9. "Contrato a preservar item 2" (inventory doc) is referenced but not provided.
10. Pill contents are not provided; binding criteria cannot be confirmed.
11. Drawer task format/path and how the resulting task id is embedded in the xfail marker are unspecified.
12. Granularity of coverage for grouped surfaces (`add ...`, `atoms ...`, `runtime *`) is ambiguous (one test vs. one per subcommand).
13. "Suite is green" is undefined when strict xfails are expected; pass/fail interpretation unclear.
14. Capture mechanism (`capsys` vs. monkeypatch) not specified.
15. Whether the repo's real `desk/` may be touched is not stated (AGENTS says sandbox, doc does not).
16. No acceptance threshold given for number of tests or per-surface assertions beyond "at least one."

NONE is not applicable.
