# Informe del worker: seguimiento GC03, `review` en la gramática del CLI

Worktree: `~/proyectos/SLDB_1/deskops-wt-review-grammar` (rama `wt/review-grammar`).
TaskDoc: `desk/tasks/task-gc03-dejó-review-sin-clasificar-en-la-gramática-del-cli-test-cli-grammar-falla.md`.
Commit de implementación: `65fb65ae` sobre `fe83364a`. Sin push. No se tocó `desk/`, `.sldb/`, `deskops/cli/registry.py`, el parser, la ayuda ni los goldens. No se escribió en otros repos.

## 1. Qué se hizo

- `tests/test_cli_grammar.py`: `"review"` agregado a `TOP_LEVEL_GRAMMAR["operational"]`; en `test_operational_mutates_guards` se fijan `command_for_path(("review",)).mutates is True`, `("review", "status")` `is False` y `("review", "dispose")` `is True` (precisión r2 del preflight).
- `CHANGELOG.md`: una línea en `## [Unreleased]` bajo una sección `### Fixed` nueva (Unreleased solo tenía `Added` y `Changed`; se creó la sección, sin reescribir otras).

Verificación previa de r1 contra el registro del worktree (`PYTHONPATH=$PWD`, `deskops` importado desde `deskops-wt-review-grammar/deskops/__init__.py`):

```
('review',) True
('review', 'node') True
('review', 'preflight') True
('review', 'bundle') True
('review', 'status') False
('review', 'dispose') True
```

Coincide con r1: no hay contradicción registro/comportamiento, no hay hallazgo que anotar.

## 2. Validation

| Línea | Evidencia |
|---|---|
| `TMPDIR=/dev/shm pytest -q tests/test_cli_grammar.py` verde | `2 passed, 1 warning in 1.92s` (bajo `systemd-run --scope -p MemoryMax=2G`, `-p no:cacheprovider`) |
| `TMPDIR=/dev/shm pytest -q tests/test_cli_help_examples.py` verde (la ayuda no cambia) | `11 passed, 1 warning in 29.12s` (mismas condiciones) |
| `git diff --stat origin/main` limitado a los dos archivos | Contra la merge-base `fe83364a`: solo `CHANGELOG.md` y `tests/test_cli_grammar.py`. Un `git diff --stat origin/main` literal además muestra `desk/`/`.sldb/` porque `origin/main` avanzó un commit (`f2d6ca43`, seguimiento `test_gitignore_policy`) después de la base de esta rama; esos archivos no están en esta rama ni en el worktree (`git status` limpio salvo los dos archivos antes del commit). |

El warning de pytest es `Unknown config option` del `pyproject`, preexistente y ajeno a este cambio.

## 3. Done When

| Condición | Evidencia |
|---|---|
| `tests/test_cli_grammar.py` verde con `review` clasificado una sola vez en operational | `test_top_level_nouns_are_classified_exactly_once` pasa; `review` aparece una vez, en `operational`. |
| `mutates` fijado según el registro | Tres aserciones en `test_operational_mutates_guards`, con los valores leídos del registro (arriba). |
| Ayuda sin cambios | `tests/test_cli_help_examples.py` verde; goldens no tocados. |
| CHANGELOG | Línea en `Unreleased / Fixed`, nombra `test_cli_grammar` y `review`. |

## 4. Diff stat (`git show --stat 65fb65ae`)

```
 CHANGELOG.md              | 4 ++++
 tests/test_cli_grammar.py | 4 ++++
 2 files changed, 8 insertions(+)
```

## 5. Hipótesis

- El TaskDoc dice "Unreleased / Fixed"; como no existía la sección, la creé después de `### Changed` y antes de `## [0.2.0]`. Si el coordinador prefiere otra ubicación, es un cambio de una línea.
- El trailer del commit usa `Claude Opus 5.5` tal como lo manda el brief (el modelo que ejecutó fue Fable 5.1).
- La tarea sigue en `status: draft` / `ritual-execution`: los gates de execution, testing y closeout (`closeout verify`/`commit`) los corre el coordinador, porque el brief prohíbe tocar `desk/` desde este worker.
