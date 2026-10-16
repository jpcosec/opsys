RESTATEMENT:
1. Read `deskops/cli/parser.py` (1,100 lines) and `deskops/cli/main.py`; inventory every command, its help text, args, defaults, and handler.
2. Read `runs/planning/deskops-rewrite-inventory.md` phase F5 for the intended registry design.
3. Read the two pills (`desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md`, `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md`) for constraints on CLI grammar and surfaces.
4. Create `deskops/cli/registry.py` defining registry types: command descriptor (name, help, args, handler) and a shared-args definition mechanism.
5. Rewrite `deskops/cli/parser.py` into a walker that consumes the registry and builds the argparse tree; ensure shared args are declared once and reused.
6. Port commands group by group into the registry, running F1 CLI tests after each group to confirm unchanged behavior.
7. Update dispatch in `deskops/cli/main.py` to route through registry handlers.
8. Delete the old hand-built command builders from `parser.py` once ported.
9. Capture a `--help` baseline for every command before/after and record the diff proving it is unchanged.
10. Run validation: `pytest tests/test_cli.py tests/test_cli_contract.py`, `python -m deskops --help`, `deskops faq`, `pytest tests`.
11. Close when `--help` diffs are empty for every command and the full suite passes.

AMBIGUITIES:
1. Task status is `deferred`; unclear whether it is authorized to execute now.
2. `depends_on` (`task-rw-f3-atoms-service`, `task-rw-f4-single-snapshot-reader`) completion state is not given.
3. `runs/planning/deskops-rewrite-inventory.md` is referenced but not confirmed to exist; no path/contents provided.
4. Pill contents are not provided; unknown which constraints they impose.
5. `deskops/cli/registry.py` is listed as a file but not confirmed to exist; unknown whether to create or edit.
6. Registry "types" are unspecified: dataclass vs tuple vs dict; handler signature (`args` vs `(args, ns)`); arg-spec schema.
7. "Shared args defined once" conflicts with byte-identical `--help` per command; unclear how to preserve per-command ordering, defaults, and usage strings.
8. `--help` "diff recorded" — no baseline exists and no location/format for recording the diff is specified.
9. "F1 CLI contract tests" are named but not identified; unclear if `tests/test_cli.py` / `tests/test_cli_contract.py` are those, or whether they exist.
10. Dispatch change scope in `main.py` is unspecified (what currently calls parser vs registry).
11. Unknown whether argparse subcommands, prog name, error messages, and exit codes must be byte-identical or only help text.
12. No acceptance criteria for internal structure beyond "shrinks"; no line-count or API target.
13. "Delete the old builders" — unclear if any builders are public API used elsewhere.
14. No instruction on sandbox desk usage for mutating CLI UX checks.
15. Done condition ties to diff + passing suite, but no defined diff tooling, no pass threshold for flakiness, no commit requirement stated.
