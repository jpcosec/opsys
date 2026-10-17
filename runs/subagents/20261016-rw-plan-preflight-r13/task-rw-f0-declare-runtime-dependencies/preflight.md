RESTATEMENT:

1. Confirm task has been promoted from `desk/drawer/tasks/` to `desk/tasks/` by the supervisor (resolved decision); do not commit.
2. Open `pyproject.toml`; locate the `dependencies` list (currently pydantic + PyYAML).
3. Append exactly `"structuredLanguageDB>=0.1.4"` and `"kgdb>=0.1.0"` to `dependencies`. Do not touch publishing config, add upper bounds, or modify `ensure_sldb_available` in `deskops/bootstrap.py`.
4. Run `python -m venv /tmp/deskops-venv`.
5. Run `/tmp/deskops-venv/bin/pip install ../sldb "git+https://github.com/jpcosec/kgdb.git@1247139" .`.
6. Run `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`.
7. If step 5 exits non-zero: keep the declaration unchanged, and record the exact command plus error output for the closeout.
8. Run `python -m deskops --help`.
9. Run `pytest tests`.
10. Report the diff and results to the supervisor; supervisor makes the closeout commit with `deskops closeout commit --task task-rw-f0-declare-runtime-dependencies --run-dir <dir>` (or `--no-run --reason <why>`), requiring `pytest tests` green.

AMBIGUITIES:

1. Task front-matter says `status: deferred`; resolved decisions say the supervisor promotes it first. Whether the executor proceeds against the drawer copy, the promoted copy, or waits is not stated in the task body.
2. No explicit statement of whether network access to `github.com` is available on this machine; step 5's git install may fail for that reason rather than the recorded packaging cause.
3. No stated behavior if the failure in step 5/6 is caused by the `../sldb` install or metadata conflict (`structuredLanguageDB 0.1.3` + stale `sldb 0.1.0` editable) rather than the missing kgdb source; the "record and close" fallback is only specified for the pip non-zero case.
4. `pytest tests` assumes a `tests` directory exists; AGENTS.md says plain `pytest`. Not confirmed which path is correct.
5. No acceptance criterion for unrelated failing tests; "pytest tests green" is required by resolved decisions but the task gives no rule if pre-existing failures are present.
6. Whether the throwaway venv at `/tmp/deskops-venv` should be removed afterward is not specified.
7. Whether any pyproject change beyond `dependencies` (e.g., a build-system entry for the git dep) is needed is not addressed, though scope explicitly limits changes to `dependencies`.
