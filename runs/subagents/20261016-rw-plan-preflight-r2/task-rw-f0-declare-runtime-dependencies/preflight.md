RESTATEMENT:
1. Open `pyproject.toml`, locate the `[project]` `dependencies` list.
2. Add the strings `"sldb>=0.1.4"` and `"kgdb>=0.1.0"` to that list.
3. Determine a kgdb install source: run `pip show -f kgdb`, read the `Location` field. Fall back to installing `kgdb` by name if an index provides it. If neither yields an installable source, stop and report instead of dropping the dependency.
4. Create a throwaway venv: `python -m venv /tmp/deskops-venv`.
5. From the deskops repo root, run `/tmp/deskops-venv/bin/pip install ../sldb <kgdb source> .`.
6. Run `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`.
7. Run `python -m deskops --help`.
8. Run `pytest tests`.
9. Do not commit. Report the diff plus the venv import result (or the missing-kgdb-source report) for supervisor closeout.

AMBIGUITIES:
1. Front matter says `status: deferred`; nothing states whether execution is authorized now.
2. `<kgdb source>` is undefined: there is no sibling kgdb checkout, and installing `kgdb` by name from an index does not verify the declared dependency against a local artifact. Whether that satisfies "Done When" is unstated.
3. "stop and report" vs "Done When … (or the missing kgdb source is reported)" contradict on whether reporting counts as completion or blocking.
4. The sibling `../sldb` checkout version is unknown; if it is `<0.1.4`, `pip install ../sldb` will either fail the lower bound or silently resolve sldb from the index. No rule given.
5. Relative paths (`../sldb`, `.`) assume cwd is the deskops repo root; unstated.
6. `pytest tests` (with path arg) differs from the repo-standard `pytest`; existence of a `tests` directory/path is unverified.
7. Placement/ordering of the two new entries within the `dependencies` list is unspecified.
8. Whether any lockfile, extras group, or `[project.optional-dependencies]` must also change is unspecified.
9. No criterion confirms the venv actually resolved the declared lower bounds (`>=0.1.4`, `>=0.1.0`) rather than different versions.
