RESTATEMENT:

1. Confirm preconditions: current tree has `deskops/graph/snapshot.py` and `deskops/cli/main.py` importing `kgdb`; `pyproject.toml` `dependencies` contains `"structuredLanguageDB>=0.1.9"`; sibling `../sldb` checkout exists.
2. Edit `pyproject.toml` only: add `"kgdb>=0.1.0"` to the `dependencies` list, immediately after `"structuredLanguageDB>=0.1.9"` (line ~10). Change nothing else.
3. Create throwaway venv: `python -m venv /tmp/deskops-venv`.
4. Install: `/tmp/deskops-venv/bin/pip install ../sldb "git+https://github.com/jpcosec/kgdb.git@1247139" .`.
5. Check import: `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`.
6. In dev env run `python -m deskops --help`.
7. In dev env run `pytest tests`.
8. If step 4 exits non-zero, keep the `kgdb>=0.1.0` declaration and record the exact command + error for closeout.
9. Hand the diff and (if applicable) the recorded pip error to the supervisor; do not commit.

AMBIGUITIES:

1. `kgdb>=0.1.0` as a resolvable index requirement is unverified: task only proves a git-URL install works. Unknown whether `kgdb` is published to any index that a plain `pip install deskops` would use.
2. Depending on pip's resolution over the mixed args in step 4, the local git install may satisfy `kgdb>=0.1.0` incidentally; this does not prove a standalone `pip install .` resolves. No acceptance criterion distinguishes these.
3. Unknown whether the git commit 1247139 declares version `0.1.0` in its metadata; if it declares anything lower, `>=0.1.0` is wrong and the check in step 4 may still pass by coincidence or fail.
4. Task flags sldb metadata says `structuredLanguageDB 0.1.3` while `import sldb` resolves to 0.1.9. Unknown which metadata the local `../sldb` install in the throwaway venv produces; if 0.1.3, the existing `>=0.1.9` pin is itself unresolved and the venv check may fail for a reason unrelated to this task.
5. Which environment each Validation command runs in is unspecified: dev env vs `/tmp/deskops-venv`. Task says only the venv check "counts", leaving `python -m deskops --help` and `pytest tests` environment undefined.
6. "record the exact command and error in the closeout" has no defined artifact or location, and Resolved Decisions says the supervisor, not the executor, performs closeout. How the executor hands the error forward is unspecified.
7. Done When permits two outcomes (check succeeds OR error recorded), but no criterion states what counts as an acceptable recorded error, so completion is not objectively decidable in the failure branch.
8. Exact formatting/ordering/quoting of the added dependency entry is unspecified beyond "after it" (single line, trailing comma conventions).
9. Network availability for the `git+https://` fetch is not stated as a precondition; offline failure would be indistinguishable from a real dependency problem.
10. `pytest tests` assumes a `tests/` directory with a passing suite; not verified or listed in `files`.
11. Whether `../sldb` must be installed as editable (`-e`) for the check to be meaningful is unspecified; the given command installs it non-editable.
12. Step 1's "installed version" claim for kgdb (0.1.0) is asserted, not verifiable from the task alone.
