RESTATEMENT:

1. Read the two bound pills (`desk/contexts/pill-010-graph-runtime-output-policy.md`, `desk/contexts/pill-009-source-file-graph-traceability.md`) before editing code.
2. Open `deskops/graph/extract_coverage.py`; locate the directory-walk sites reported at lines 27 and 295 (and any other `os.walk`/`glob`/`Path.rglob` call in the file).
3. Add a module-level constant, e.g. `EXCLUDED_DIRS = {"tools", ".tmp", ".venv", ".git", "node_modules"}`.
4. At each walk site, compute each candidate path relative to the walk root and skip when the first path segment (`Path(p).parts[0]`) is in `EXCLUDED_DIRS`; also prune excluded dirs from `os.walk`'s `dirnames` in-place where applicable.
5. Keep the change local to `deskops/graph/extract_coverage.py`; no behavior change to non-excluded paths.
6. Open `tests/test_graph_extract_coverage.py` (create if absent); add a test that builds a temp root containing `tools/x/desk/atoms/<atom>.md` plus a control atom under a normal path.
7. In that test, run the coverage extractor against the temp root and assert the produced nodes/paths contain nothing whose first segment is `tools` (and that the control atom is still extracted).
8. Run `pytest tests/test_graph_extract_coverage.py`.
9. Run `deskops graph build --root .` and confirm the rebuilt snapshot has zero nodes under `tools/`.
10. Run `pytest`.

AMBIGUITIES:

1. `status: deferred` and `source:drawer` — no statement that the task is promoted/active, so it is unclear whether implementation is authorized now.
2. Scope says add `.git` and `node_modules` to the excluded set, but Goal/Done When only require zero nodes under `tools/`, `.tmp/`, `.venv/` — no acceptance criterion covers the extra two.
3. "Every path walk" is unbounded; only two line numbers (27, 295) are named, and those may be stale. No list of actual walk sites.
4. "First path segment relative to the root" — "root" is undefined (repo root, `--root` value, walk arg, or cwd). Behavior differs if the walk receives absolute paths.
5. Nesting rule unclear: an atom at `desk/tools/...` (tools not in first segment) would not be excluded. Whether that is intended is unspecified.
6. Test assertion target unspecified: no snapshot path, store argument, or API/function name for querying produced nodes.
7. Test style unspecified: extractor-function call vs. invoking the `deskops graph build` CLI.
8. Atom format/fixture requirements unspecified ("an atom placed under `tools/x/desk/atoms/`" — valid SLDB model? frontmatter? extension?).
9. `tests/test_graph_extract_coverage.py` existing contents/fixtures unknown; whether to extend or create is not stated.
10. Symlink handling (e.g. `tools` symlink, or a symlinked repo) is not specified.
11. Validation step `deskops graph build --root .` writes to the repo's real tracked `desk/`/store, contradicting the AGENTS sandbox rule for mutating CLI runs; which to follow is unclear.
12. No acceptance criterion on the snapshot artifact itself (where it lives, whether it is committed, whether it mutates tracked files).
13. Closeout expectations (commit required per pill-001 / AGENTS "every closed task ends with its own atomic commit") are absent from Done When.
14. The "5 atoms" count in Rationale is not used as a check; no way to verify against it.
15. Dependency/scope boundary with `task-rw-f4-coverage-extractor-decision` is declared out of scope but no guard if that decision changes the file.
