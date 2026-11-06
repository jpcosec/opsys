# Informe del worker: seguimiento del hash de RelationDoc tras sldb GO09

Worktree: `~/proyectos/SLDB_1/deskops-wt-model-contract` (rama `wt/model-contract`).
TaskDoc: `desk/tasks/task-test-model-contract-snapshot-actualizar-deliberadamente-el-hash-de-relationdoc-tras-go09.md`.
Commit de implementación: `24016695` sobre `586ecba2` (merge-base con origin/main). Sin push. No se tocó `.sldb/`, `desk/`, el test, otros hashes ni otros desks/repos.

## 1. Precondiciones (t2, t3) verificadas antes de escribir

| Check | Resultado |
|---|---|
| `git merge-base --is-ancestor 09b5075c HEAD` | rc 0: la migración del store está en la base |
| `contract_hash` en `.sldb/core/models/RelationDoc.yaml` | `a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6` |
| Salida 'New hashes' del test (antes del cambio) para RelationDoc | `a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6` |
| Modelos que fallaban antes del cambio | solo `RelationDoc` (`1 failed, 1 passed`); ningún otro hash se actualiza (paso 4) |

Los tres hashes coinciden, así que se escribió.

## 2. Qué se hizo

- `tests/fixtures/model_contract_hashes.json`: solo la entrada `RelationDoc`, de `e2ddf039…` a `a71cc045…`, sin reordenar ni tocar otras claves (sed sobre esa línea).
- `CHANGELOG.md`: la línea textual del paso 3 al final de la lista de `## [Unreleased]` / `### Changed`, antes de `### Fixed` (t4: no se crean secciones).
- `tests/test_model_contract_snapshot.py` no se toca (paso 2: `FIXTURE_UPDATE` intacto).

## 3. Validation

| Línea | Evidencia |
|---|---|
| `TMPDIR=/dev/shm pytest -q tests/test_model_contract_snapshot.py` verde (2 passed) | `2 passed, 1 warning in 1.30s` (bajo `systemd-run --scope -p MemoryMax=2G`, `-p no:cacheprovider`, `PYTHONPATH` del worktree; `deskops` importa desde `deskops-wt-model-contract/deskops/__init__.py`) |
| grep RelationDoc en el fixture = a71cc045… = contract_hash del store | fixture: `"RelationDoc": "a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6"`; store: `contract_hash: a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6` |
| diff contra la merge-base limitado a los dos archivos, una línea cambiada en el fixture | `git diff --stat 586ecba2`: `CHANGELOG.md` (+1), `tests/fixtures/model_contract_hashes.json` (+1/-1) |

El warning de pytest es `Unknown config option` del `pyproject`, preexistente.

## 4. Done When

| Condición | Evidencia |
|---|---|
| test verde con el hash de GO09 registrado deliberadamente, igual al del store migrado en 09b5075c | 2 passed; hashes iguales (tabla arriba) |
| CHANGELOG cita GO09 | línea en Changed cita GO09, 33b3c7a0, d39bf915 y 09b5075c |
| los cuatro desks pendientes quedan para el coordinador de proyecto | no se tocó spec2viz, scion, pron ni graph_ui (t1); sldb ya migrado en 96bcc5dd |

## 5. Diff stat (`git show --stat 24016695`)

```
 CHANGELOG.md                              | 1 +
 tests/fixtures/model_contract_hashes.json | 2 +-
 2 files changed, 2 insertions(+), 1 deletion(-)
```

## 6. Hipótesis

- El mensaje `FIXTURE_UPDATE` del test sigue citando `task-rw-f6-migrate-tracking-stores` como la tarea de migración; el TaskDoc pide no editarlo, así que queda como está aunque la migración real fue 09b5075c.
- El trailer del commit usa `Claude Opus 5.5` como manda el brief (el modelo que ejecutó fue Fable 5.1).
- La tarea sigue en `status: draft` / `ritual-execution`; los gates los corre el coordinador porque el brief prohíbe tocar `desk/` desde este worker.
