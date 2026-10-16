## RESTATEMENT

1. Open `/home/jp/proyectos/SLDB_1/deskops/pyproject.toml`.
2. In `[project].dependencies`, add `"structuredLanguageDB>=0.1.4"` and `"kgdb>=0.1.0"`; leave existing `pydantic` and `PyYAML` entries untouched.
3. Do not change publishing metadata, upper bounds, or `ensure_sldb_available` in `deskops/bootstrap.py`.
4. From the repo root, run `python -m venv /tmp/deskops-venv`.
5. Run `/tmp/deskops-venv/bin/pip install ../sldb "git+https://github.com/jpcosec/kgdb.git@1247139" .`.
6. Run `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`; expect exit 0.
7. If step 5 exits non-zero, keep the pyproject declaration and capture the exact command plus error text for the supervisor.
8. Run `python -m deskops --help` in the repo environment; expect success.
9. Run `pytest tests`; require green.
10. Do not commit. Report the pyproject diff, the venv command, and its result to the supervisor.

## AMBIGUITIES

1. Task header says `status: deferred` / `source:drawer`, but no on-disk path is given; I cannot tell whether the supervisor has already promoted it to `desk/tasks/` before dispatch.
2. Done When allows "or the missing kgdb source is reported," but Implementation Path supplies the kgdb source (`git+...@1247139`); the fallback condition is contradictory/unreachable.
3. "record the exact command and error in the closeout" conflicts with Resolved Decisions stating the executor does not commit and the supervisor writes closeout; the handoff channel is unspecified.
4. The venv path is only implied inside an example command (`/tmp/deskops-venv`), not stated as the required path.
5. `../sldb` and `.` in step 5 have no stated working directory.
6. Validation does not state which environment (`python`/`pytest` = repo env vs. throwaway venv), nor whether dependencies must be reinstalled first.
7. `pytest tests` assumes a `tests` directory exists in this repo; no instruction if it does not.
8. Non-zero pip exit is handled only for a missing source; behavior is unspecified for network/auth failure against `github.com/jpcosec/kgdb.git`.
9. Whether the venv check must also assert `import kgdb` is unspecified; Done When names only the deskops CLI import.
10. The target file is not explicitly qualified as the deskops pyproject (the doc also cites `../sldb/pyproject.toml:2`), and no check is defined for the exact dependency string format/ordering.
