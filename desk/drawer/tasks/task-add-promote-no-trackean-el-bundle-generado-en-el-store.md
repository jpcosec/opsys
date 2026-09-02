# add/promote no trackean el bundle generado en el store

ID: task-add-promote-no-trackean-el-bundle-generado-en-el-store
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260901-000500-unclear-add-promote-no-trackean-el-bundle-generado.md`.

## Scope

`deskops add task` y `deskops promote drawer-task-to-active-task` generan el bundle completo (task, routine, checklists, conditions, edges, operators) pero no lo trackean en el store sldb. Evidencia: en gemini_test (worktree vitali, 2026-08-31/09-01) una pasada de promotes dejo 22 docs untracked y un `add task` dejo 19; `deskops doctor` los reporta como "Untracked desk documents" y hay que correr `sldb docs track <path> --model <Model>` a mano por cada archivo. Repro: `deskops add task --root . --title X` en un desk con store `.sldb`, luego `deskops doctor --root .`. Esperado: el bundle queda trackeado al crearse, igual que hace `repo register` con su entry.

Nota entregada a mano en este inbox porque el camino CLI (`deskops inbox --repo deskops`) no fue posible desde gemini_test; ver la nota hermana sobre el registry.

## Source

- `desk/inbox/20260901-000500-unclear-add-promote-no-trackean-el-bundle-generado.md`

## Implementation Path

### Exact code pointers (resolved 2026-09-01, no guessing required)

- Bug site: `deskops/operations.py` -> `write_and_track()` (~line 247, inside the add-task bundle compile). It calls `self._write_new_doc(path, model, doc_payload)` for TaskDoc, RoutineDoc, ConditionDoc, ChecklistDoc, OperatorDoc, EdgeDoc but never calls `track_document`.
- Reuse pattern from `deskops/operations.py::_track_created_artifact` (~line 1821): load `store_index` via `sldb.store.io.load_store_index(self.root / ".sldb")`, resolve `model_entry` by `model.__name__`, call `sldb.store.ops.track_document(store_path, self.root, store_index, model, model_entry, path, doc_id, resolve_model_ref, ...)`. Working callers for reference: `deskops/cli/commands/repo.py:115`, `deskops/cli/commands/inbox.py:288`.
- Model mapping (do not invent): task->TaskDoc, routine->RoutineDoc, condition->ConditionDoc, checklist->ChecklistDoc, operator->OperatorDoc, edge->EdgeDoc (all already imported in `deskops/operations.py`).
- The promote path reuses the same add/compile machinery, so fixing `write_and_track` covers both; verify with a promote repro too.
- Guard: skip tracking silently when the `.sldb` store does not exist (same behavior as `_track_created_artifact`).

## Validation

- `pytest tests/test_cli.py -q`
- Repro in sandbox: `deskops add task --root .tmp/deskops-cli-test --title X`, then `deskops doctor --root .tmp/deskops-cli-test` -> zero untracked findings for the bundle.

## Done When

- add/promote bundle documents are tracked in the sldb store at creation time
- doctor reports zero untracked bundle docs after a fresh add+promote in a sandbox desk
