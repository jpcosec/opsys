# Informe del worker: seguimiento test_gitignore_policy (layout .sldb vigente)

Worktree: `~/proyectos/SLDB_1/deskops-wt-gitignore-policy` (rama `wt/gitignore-policy`).
TaskDoc: `desk/tasks/task-test-gitignore-policy-quedó-viejo-sldb-core-se-versiona-entero.md`.
Commit de implementación: `d99e110e` sobre `c4519136` (merge-base con origin/main). Sin push. No se tocó `.gitignore`, `desk/`, `.sldb/` ni otros tests. No se escribió en otros repos.

## 1. Qué se hizo

- `tests/test_gitignore_policy.py`: el test se renombra a `test_sldb_core_and_store_declaration_are_tracked_and_cache_is_ignored`, con docstring de la política vigente. Aserciones:
  - no ignorados (`assert not _is_ignored`): `.sldb/store.yaml`, `.sldb/core/store_index.yaml`, `.sldb/core/models/AtomDoc.yaml`, `.sldb/core/documents/AtomDoc.yaml`;
  - trackeados (`_is_tracked`, `git ls-files --error-unmatch`, rc 0): `.sldb/store.yaml`, `.sldb/core/store_index.yaml`;
  - ignorados: `.sldb_cache/semantic_index.yaml`, `.sldb_cache/locks/store.lock`;
  - `git ls-files .sldb/runtime` con stdout vacío (`_tracked_under`).
  - Se reusa `_is_ignored` tal cual (s3); todos los helpers usan `subprocess` con `cwd=ROOT`.
- `CHANGELOG.md`: la línea de s1, textual, en `## [Unreleased]` bajo una sección `### Fixed` creada (Unreleased solo tenía Added y Changed en esta rama).

Hechos verificados en el worktree antes de escribir (git check-ignore / git ls-files):

```
ignored? .sldb/store.yaml -> no          tracked? -> sí
ignored? .sldb/core/store_index.yaml -> no   tracked? -> sí
ignored? .sldb/core/models/AtomDoc.yaml -> no   tracked? -> sí
ignored? .sldb/core/documents/AtomDoc.yaml -> no   (no existe como archivo; documents/AtomDoc es un directorio)
ignored? .sldb_cache/semantic_index.yaml -> sí
ignored? .sldb_cache/locks/store.lock -> sí
ignored? .sldb/runtime/x -> no
git ls-files .sldb/runtime -> vacío
```

## 2. Validation

| Línea | Evidencia |
|---|---|
| `TMPDIR=/dev/shm pytest -q tests/test_gitignore_policy.py` verde | `1 passed, 1 warning in 0.12s` (bajo `systemd-run --scope -p MemoryMax=2G`, `-p no:cacheprovider`, `PYTHONPATH` del worktree; `deskops` importa desde `deskops-wt-gitignore-policy/deskops/__init__.py`) |
| `git diff --stat` contra la merge-base (s2) limitado a los dos archivos; `.gitignore` sin cambios | `git diff --stat c4519136`: `CHANGELOG.md` (+4) y `tests/test_gitignore_policy.py` (+40/-7); `git diff --quiet -- .gitignore` rc 0 |

El warning de pytest es `Unknown config option` del `pyproject`, preexistente.

## 3. Done When

| Condición | Evidencia |
|---|---|
| test verde con la política actual (core y store.yaml trackeados, `.sldb_cache` ignorada, nada trackeado en `.sldb/runtime`) | 1 passed; aserciones listadas arriba |
| `.gitignore` intacto | no está en el diff |
| CHANGELOG | línea s1 en Unreleased / Fixed |

## 4. Diff stat (`git show --stat d99e110e`)

```
 CHANGELOG.md                   |  4 ++++
 tests/test_gitignore_policy.py | 43 +++++++++++++++++++++++++++++++++++-------
 2 files changed, 40 insertions(+), 7 deletions(-)
```

## 5. Hipótesis y hallazgos

- Hallazgo ya anotado en el TaskDoc, confirmado aquí: `.sldb/runtime/` no está ignorado (`git check-ignore` rc 1). El test solo afirma que no hay nada trackeado ahí. Ignorarlo exige tocar `.gitignore`, fuera de alcance; va en otro nodo si el dueño lo quiere.
- `.sldb/core/documents/AtomDoc.yaml` no existe como archivo (`documents/AtomDoc` es un directorio). La aserción de "no ignorado" sigue siendo válida porque `git check-ignore` evalúa la ruta contra las reglas sin requerir el archivo; no se afirma tracking de esa ruta, como pide el paso 3.
- La sección `### Fixed` de Unreleased también la crea el nodo 1 (`wt/review-grammar`, ya en main como 04455a30). Al mergear esta rama habrá un conflicto trivial en `CHANGELOG.md`: se resuelve dejando una sola cabecera `### Fixed` con las dos líneas.
- El trailer del commit usa `Claude Opus 5.5` como manda el brief (el modelo que ejecutó fue Fable 5.1).
- La tarea sigue en `status: draft` / `ritual-execution`; los gates los corre el coordinador porque el brief prohíbe tocar `desk/` desde este worker.
