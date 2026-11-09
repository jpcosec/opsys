# CC35b worker report: selectores por `sldb.api.select_documents`

Worker: `cc35b-worker` (robocop2). Rama `wt/cc35b`, base `a865bbcf`. Sin push.
TaskDoc: `desk/tasks/task-cc35b-selectores-resolución-de-documentos-por-sldb-api-select-documents.md`
(precisiones a1-a9, b1-b6, c1-c3; d1 la decide el coordinador del plan durante la ejecución).
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/cc35b/`.

## Commits

| commit | contenido |
|---|---|
| `28faa7e2` | selectores de superficies trackeadas por `select_documents`; tests nuevos; CHANGELOG |
| `55539b9d` | tests a7: `test_task_types`, `test_promotion_nesting` |
| `3859b296` | d1: el `include` trackea el Board y el ritual de fase sembrados; golden `scaffold/update.json` |
| `b910c332` | tests a7: dos casos de `test_cli` |
| `94aa656a` | d1: `test_desk_sync` espera el Board y el ritual de fase en el `include` |
| (este) | el informe |

## Aceptación, línea por línea

### 1. grep `resolve_selector|_tracked_task_paths` en `deskops/`

Filtro b3 (`coord2-ccconfig/cc35b/grep-accept.sh`): un acierto queda aceptado si su línea, o la anterior, es la marca
`# CC34: alias for graph_ui, removed by CC34` o `# CC35b-a3: untracked surface, resolved on disk`.

```
$ grep -rnI "resolve_selector\|_tracked_task_paths" deskops/
deskops/desk_paths.py:27:def resolve_selector(
deskops/doc_access.py:53:from deskops.desk_paths import resolve_selector
deskops/doc_access.py:614:        return resolve_selector(desk_root(root), [directory], selector, pattern, what, recursive=recursive)
deskops/services/issues.py:24:from deskops.desk_paths import resolve_selector
deskops/services/issues.py:105:    return resolve_selector(
$ grep-accept.sh .      # aciertos sin marca
(vacío)
```

Las cinco líneas llevan la marca `# CC35b-a3: untracked surface, resolved on disk` en la línea anterior
(`desk_paths.py:26`, `doc_access.py:52`, `doc_access.py:613`, `issues.py:23`, `issues.py:104`).
`_tracked_task_paths` y `frontmatter_id` ya no existen.
Los alias `_resolve_glob` y `_registered_repositories` de `operations.py` llevan `# CC34: alias for graph_ui, removed by CC34`.
`docs/` y `README.md` no nombran `resolve_selector`, `_tracked_task_paths` ni `frontmatter_id`, así que no hay seguimiento por b4.

### 2. Mensajes de no encontrado y de ambigüedad iguales a los de hoy

- Disco: `tests/test_desk_paths.py` sigue verde sin cambios (10 passed).
- Store: `tests/test_tracked_selector_resolution.py` (nuevo) fija el texto exacto en los tres casos:
  - `No artifact.atom file found for selector 'atom-cc35b-missing'`;
  - `Ambiguous artifact.atom selector 'atom-cc35b-shared': atoms/atom-cc35b-shared-alpha.md, atoms/b/atom-cc35b-shared-beta.md` (ambigüedad por prefijo de nombre);
  - `Ambiguous artifact.ritual selector 'cc35b-gate': rituals/cc35b-gate-two.md, rituals/cc35b-gate.md` (ambigüedad en la segunda consulta, por nombre de archivo).
- Goldens de salida y de ayuda iguales: `test_output_goldens` 7 passed (dos corridas) y `test_cli_help_examples` 11 passed, sin `--update-golden`.

### 3. Nombre contra stem en rituales (a6)

`test_ritual_execution_resolves_by_name_and_by_stem` cubre el ritual sembrado, trackeado como `ritual-execution` en `desk/rituals/execution.md`: resuelven `ritual-execution` y `execution`.
`test_ritual_resolves_by_its_tracked_name_and_by_its_file_stem` cubre lo mismo con `ritual-handoff` en `handoff.md`.

### 4. Tests de a uno

Corridos uno por vez con `pt.sh`, que espera con el patrón anclado `pgrep -f '^(\S*/)?python[0-9.]* -m pytest'`.
Los livianos corrieron desde el worktree; los pesados, desde `/dev/shm/deskops-cc35b` con `PYTHONPATH` apuntando a esa copia.

Desde el worktree:

| archivo | resultado |
|---|---|
| test_tracked_selector_resolution (nuevo) | 10 passed |
| test_desk_paths | 10 passed |
| test_issue_cli | 9 passed |
| test_review_command | 12 passed |
| test_review_doc | 13 passed, 1 xfailed |
| test_promotion_nesting (a7) | 2 passed |
| test_transaction | 11 passed |
| test_desk_view | 9 passed, 1 skipped |
| test_cli_help_examples | 11 passed |
| test_add_task_from_drawer | 3 passed |
| test_registry_robustness | 5 passed |
| test_closeout | 49 passed |
| test_retire_cli | 11 passed (tras d1) |
| test_desk_replace | 7 passed |
| test_inbox_promote_cli_gaps | 20 passed |
| test_task_types (a7) | 16 passed |
| test_scaffold_golden | 3 passed (tras d1 y la actualización de `update.json`; incluye la idempotencia) |

Desde `/dev/shm`:

| archivo | resultado |
|---|---|
| test_output_goldens | 7 passed (antes y después de d1) |
| test_atoms_cli / create_from_source / merge / split | 4 / 3 / 5 / 3 passed |
| test_lifecycle_end_to_end / graph | 5 / 9 passed |
| test_cli (a7) | 101 passed |
| test_operational | 10 passed |
| test_closeout_gates | 7 passed |
| test_closeout_declared_evidence | 19 passed |
| test_desk_sync (d1) | 8 passed |
| test_message_cli / test_message_delivery | 10 / 6 passed |
| test_doctor_alerts / model_registration / unmodeled_surfaces | 5 / 8 / 4 passed |
| test_atom_folder_axis / atom_materialization / materialization_contract | 13 / 2 / 5 passed |
| test_extension_points / cli_escape_hatches / migrate_desk_stores | 5 / 9 / 16 passed |
| test_domain_tree / taskdoc_read_without_overlay / graph_atom_trace / supervise | 5 / 1 / 2 / 7 passed |
| test_board_portable_references | 1 failed, 1 passed: **falla previa**, también falla sobre la base `a865bbcf` (log `base-board_portable.log`). Copia el `desk/tasks/Board.md` real del repo, que ya en la base rutea `desk/rituals/context-review.md` (no está en su lista de contexto), y no usa resolvers de deskops |

Ningún test de estos recorre `.venv` ni `runs/`.

### 5. `deskops doctor` en los 6 desks (a9)

`coord2-ccconfig/cc35b/doctor6.sh` es la plantilla de CC35a con las rutas de cc35b.
Corre doctor con el código de main (`bce196e1`, el origin/main actual) y con el de la rama (`b910c332`), sobre copias en `/mnt/ssd/proyectos/SLDB_1/.tmp-cc35b-doctor` y con cwd neutro.
Las copias se borraron al terminar.

```
deskops: identical   sldb: identical   spec2viz: identical
scion: identical     pron: identical   graph_ui: identical
```

No hay hallazgos nuevos.
Los `exit=1` de graph_ui, pron, scion, sldb y spec2viz salen igual con main, así que vienen de antes.

### 6. `wc -l` antes y después (b5)

Antes es `a865bbcf`; después, `HEAD`.

| archivo | antes | después |
|---|---|---|
| `deskops/desk_paths.py` | 64 | 67 |
| `deskops/doc_access.py` | 948 | 940 |
| `deskops/operations.py` | 276 | 278 |
| `deskops/services/issues.py` | 375 | 377 |
| `deskops/services/review.py` | 860 | 856 |
| `deskops/data/desk_declaration.yaml` (d1) | 178 | 185 |
| `CHANGELOG.md` | 162 | 163 |
| `tests/test_tracked_selector_resolution.py` | — | 138 |
| `tests/test_task_types.py` | 371 | 374 |
| `tests/test_promotion_nesting.py` | 106 | 113 |
| `tests/test_cli.py` | 3134 | 3138 |
| `tests/test_desk_sync.py` | 276 | 280 |
| `tests/fixtures/golden/scaffold/update.json` | 83 | 85 |

### 7. CHANGELOG

Hay una entrada nueva en `## [Unreleased]` / `### Changed`, con la frase de d1 incluida.

## Mapa de resolvers a `select_documents`

Todos pasan por `doc_access.resolve_document(root, directory, selector, what, pattern, recursive, model)`:

1. Un selector vacío da el mismo `ValueError` de siempre.
2. Si la superficie no está trackeada, se resuelve en disco con `desk_paths.resolve_selector` (CC35b-a3). No está trackeada cuando el directorio cae bajo `desk/drawer` o `desk/issues`, o cuando la raíz no tiene store.
3. Consulta 1 (c3): `{"prefix": selector, "path_glob": "<dir>/[**/]<pattern>"}` (más `model` si se da), con `expect="one"`.
4. Consulta 2, solo si la 1 no encontró nada: `{"path_glob": "<dir>/[**/]<selector>*.md"}`, con `expect="one"`.
5. Una ambigüedad corta ahí y da `ValueError("Ambiguous <what> selector '<s>': ...")`. Los candidatos son las filas de la misma consulta con `expect="many"` cuyo `export_id` está en `AmbiguousSelectionError.candidates`, como rutas relativas a `desk/` y ordenadas (`desk_paths.relative_candidates`, antes `_relative_candidates`).
6. Si ninguna consulta encuentra nada: `FileNotFoundError("No <what> file found for selector '<s>'")`.

| resolver | antes | ahora |
|---|---|---|
| `resolve_glob(root, dir, id)` | `resolve_selector(..., f"{id}*.md", "task", recursive=False)` | `resolve_document(..., "task", recursive=False)` |
| `resolve_artifact_selector(root, art, dir, s)` | disco con `artifact_glob_pattern`, más el fallback legacy por `_tracked_task_paths` (leía `.sldb/core/documents/*/*.yaml` crudo) | `resolve_document(pattern=artifact_glob_pattern(art))`; para `artifact.task` en superficie trackeada, si no encuentra, `resolve_document(model="TaskDoc")` (la familia del modelo) |
| `resolve_artifact_selector_multi` | un solo conjunto de candidatos entre directorios, más el fallback de review por `frontmatter_id` (rglob) | `resolve_artifact_selector` por directorio, en orden; la review resuelve por su nombre trackeado (= su id) |
| `resolve_ritual_selector` | artefacto, más el fallback por `frontmatter_id` | `resolve_artifact_selector("artifact.ritual")`: la consulta 1 encuentra `ritual-x`, la 2 encuentra `x.md` |
| `registered_repositories` | `glob("repo-*.md")` | con store: `select_documents({"path_glob": "desk/registry/repo-*.md"})`; sin store: glob (CC35b-a3) |
| `ReviewService._task_path` / `_resolve_pill` | `resolve_selector` directo | `doc_access.resolve_document` |
| `issues.find_issue` / `list_issues` | disco | sin cambio, con marca CC35b-a3 (a3/b1/c1) |
| `drawer.resolve_drawer_source` / `_resolve_unique` | disco, sin `resolve_selector` | sin cambio (a3/b1/c1) |
| `editable_artifact` (`edit task`, cae al drawer) | `resolve_artifact_selector` sobre `drawer/tasks` | igual; el drawer resuelve en disco dentro de `resolve_document` |
| callers de `services/` (atoms, tasks, closure, desk_view) | `doc_access.resolve_*` | sin cambio de código (a8: `tasks.py` no se tocó) |

`model`: no se pasa a ninguna consulta principal (c2). El `path_glob` reproduce el patrón que se globbeaba antes, incluido `*.md` para los artefactos de nombre libre. La única excepción es el fallback legacy de tareas (ver desvío 2).

## d1: el `include` trackea el Board y el ritual de fase sembrados

`deskops init` dejaba sin trackear `desk/tasks/Board.md` y `desk/rituals/phase.md`.
Con los selectores en el store, `deskops edit board Board` fallaba en un desk nuevo; lo mostró `test_retire_cli`.
El coordinador del plan decidió la opción (1) de forma revisable: trackearlos por `include`, sin tocar el seed del Board, que sigue con `track: false`.

Inventario de lo que `init` escribe:

- **Board.md**: entra como `BoardDoc:Board`. El nombre es el stem, el mismo con que ya está trackeado en deskops, sldb y graph_ui.
- **phase.md**: entra como `RitualDoc:ritual-phase`, con el nombre explícito, igual que en esos mismos desks.
- **Fuera del include**:
  - `contexts/pills.md`: no tiene modelo y ningún selector lo resuelve.
  - `runtimes/runtime-pi-deepseek-flash.md`: no es superficie de estos selectores. Queda como seguimiento.
  - `drawer/README.md`, `config.json` y `tag-namespaces.yaml`.

Efecto:

- `update.json` suma solo `Tracked desk/rituals/phase.md as RitualDoc.` y `Tracked desk/tasks/Board.md as BoardDoc.`.
- `init.json` no cambia.
- La segunda `desk update --apply` no cambia nada (`test_a_second_desk_update_apply_changes_nothing`).
- `test_desk_sync` fija el contenido del `include`, así que se actualizó con las dos entradas.
- En spec2viz y scion, que no tenían el Board ni la fase trackeados, los trackeará la próxima `desk update --apply`.
- Conflicto con CC32, que también agrega un include: lo resuelve el coordinador.

## Tests adaptados (a7)

Ninguna aserción cambió, salvo `test_desk_sync`, que verifica el propio `include` que cambia d1.

| test | qué escribía a mano | adaptación |
|---|---|---|
| `test_task_types::test_closeout_verify_reads_evidence_from_the_type` | tarea `task.docs` sin trackear | `doc_access.track_created_document(root, TaskDocsDoc, ...)` (b6) |
| `test_promotion_nesting::test_advance_task_keeps_nested_h3_sections_inside_scope` | tarea con `###` anidados sin trackear | `sldb.api.track_document_file(..., "TaskDoc", force=True)`, como `desk update --apply`; el track sin `force` la rechaza por ruido estructural, que es justo lo que prueba el test |
| `test_cli::test_edit_task_resolves_tracked_task_with_legacy_file_name` | editaba a mano el registro `.sldb/core/documents/TaskCodeDoc/<n>.yaml`, que `select_documents` no lee (lee el índice) | `doc_access.untrack_doc` antes del rename y `track_created_document(TaskCodeDoc, 001-legacy-task.md, "task-legacy-task")` |
| `test_cli::test_edit_ritual_accepts_frontmatter_id` | ritual en un desk sin store, resuelto por el id del frontmatter | `deskops init` y `track_created_document(RitualDoc, ..., "ritual-closeout-like")`; el id resuelve como nombre trackeado |
| `test_desk_sync` (2 tests, d1) | — | se esperan `BoardDoc: [desk/tasks/Board.md]` y `ritual-phase` en el `include`, y `Board.md` entre los pendientes |

## Hipótesis para sldb

1. **`select_documents` sobre archivos no trackeados de un `path_glob`** (a3). Permitiría resolver el drawer y los issues con la misma API, sin el camino en disco.
2. **Selector con extensión** (`atom-x.md`): ninguna de las dos consultas de c3 lo resuelve en una superficie trackeada; el disco aceptaba `path.name`. Hipótesis: que `ref` o `prefix` acepten el nombre de archivo, o que sldb exponga una regla de nombre o stem del path.
3. **`AmbiguousSelectionError.candidates` trae `export_id` y no filas.** deskops repite la consulta con `expect="many"` para obtener las rutas. Una excepción con las filas evitaría esa segunda lectura.
4. **Doble criterio nombre/stem.** La consulta 2 por `path_glob` no aplica "exacto antes que prefijo" sobre el nombre de archivo: `execution.md` junto a `execution-extra.md` resulta ambiguo, mientras el disco elegía el exacto. Hipótesis: un tier exacto sobre el stem del path en `select_documents`.

## Desvíos

1. **Raíces sin store → disco, con la marca CC35b-a3.** Sigue el precedente de `desk_transaction` (CC35a): sin store no hay nada trackeado. Unos 40 archivos de tests arman desks sin store. En ese camino ya no hay fallbacks por id del frontmatter, y por eso se adaptó `test_edit_ritual_accepts_frontmatter_id`.
2. **Fallback legacy de tareas con `model="TaskDoc"`.** c2 pide no pasar `model` para tareas, pero sin él el `*.md` del directorio también incluye `Board.md` y otros documentos que no son tareas. Como `model` filtra la familia (el modelo y los que lo extienden), `TaskDoc` cubre TaskCodeDoc, TaskDocsDoc y los demás. La consulta principal de tareas va sin `model`, como pide c2.
3. **`resolve_artifact_selector_multi` recorre los directorios en orden** en lugar de armar un solo conjunto de candidatos. Afecta a las pills: si `contexts` y `drawer/pills` tienen el mismo selector, gana la activa en vez de dar ambigüedad. Va en el CHANGELOG.
4. **d1** amplía los archivos de la tarea a `deskops/data/desk_declaration.yaml` (solo `include`) y a `tests/fixtures/golden/scaffold/update.json`, por decisión del coordinador del plan.
5. **Guarda de pytest.** La guarda original del brief se encontraba a sí misma en la línea de comando de `bash -c`. Se usó el patrón anclado, que confirmó el coordinador.
