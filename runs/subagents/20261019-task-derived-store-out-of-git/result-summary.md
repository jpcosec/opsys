# result summary: task-derived-store-out-of-git

Done by the supervisor directly. Step 2 of the coordinator's order; sldb gave the go-ahead in note 20261019-130108 (clean clone of fadd3b59 PASS).

- `.sldb/store.yaml`: written with `sldb stores declare --write`, then the include rules were edited by hand. 17 models, no links, no absolute paths; RelationTypeDoc and RelationDoc come from the sldb package by model_ref only. Globs: AtomDoc `desk/atoms/atom-*.md`, PillDoc `desk/contexts/pill-*.md`, TaskDoc `desk/tasks/task-*.md`; BoardDoc only `desk/tasks/Board.md`. Each glob was checked to match exactly what the store tracked.
- `.gitignore` gains `.sldb/core/`, and `git rm -r --cached .sldb/core` takes out 227 files. Before removing, the rebuilt store was compared with the local one: the documents are identical. The only model lines that disappear are the absolute sldb paths and the `sections_index` pointers into `.sldb/runtime`; the rebuild adds `semantics` tags. Nothing irrecoverable was removed.
- CI (`.github/workflows/tests.yml`): `sldb stores build` before pytest and `sldb stores build --check` after it.
- `tests/test_gitignore_policy.py` and the README follow the new layout.
- Drawer tasks under `desk/drawer/tasks/` were never tracked in the store, so there is no TaskDoc glob for them; adding one would make `build --check` fail because the store would differ from the local one.

See validation.log.
