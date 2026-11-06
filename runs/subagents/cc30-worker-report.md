# CC30: informe del worker

Nodo CC30 del plan `deskops-como-config`. Rama `wt/cc30`, base `origin/main` 09b5075c; medición base q3 en main dc1d2834 (idénticos en `deskops/operations.py` y `deskops/services/`). Fecha: 2026-11-06.

## Aceptación, línea por línea

1. **`tests/test_output_goldens.py` verde sin `--update-golden`.** `7 passed, 1 warning in 336.10s`. `git status -- tests/fixtures` vacío: los 120 goldens de ayuda y los de salida no cambiaron.
2. **`grep -rn "spec/artifacts\|spec/fields\|SpecRegistry\|_ARTIFACT_DEFAULTS" deskops/`** → vacío.
3. **`grep -rn "DeskopsOperations(" deskops/services/`** → solo `deskops/services/desk_view.py:67: self.ops = operations or DeskopsOperations(self.root)` (q9).
4. **`grep -rn "def _normalize_task_payload\|def compile_task_spec" deskops/`** → una sola definición: `deskops/specs/compiler.py:26:def compile_task_spec(`.
5. **Helpers privados pedidos por los servicios** (`grep -rhoE "operations\._[a-z_]+|ops\._[a-z_]+" deskops/services/ | sort -u`):
   - Antes (17): `ops._add_closeout_facts ops._append_task_to_board ops._coerce_list ops._hydrate_task ops._normalize_task_payload ops._read_doc ops._reference_points_to_atom ops._remove_created_file ops._resolve_artifact_selector ops._resolve_artifact_selector_multi ops._resolve_glob ops._resolve_task_payload ops._track_created_artifact ops._track_created_document ops._transitions_from ops._write_doc ops._write_new_doc`.
   - Después: vacío (desk_view.py tampoco pide ninguno: sus lecturas privadas pasaron a `doc_access`/`lifecycle`).
6. **`wc -l deskops/operations.py deskops/services/*.py`**:

   | archivo | antes (dc1d2834) | después |
   |---|---|---|
   | operations.py | 1524 | 276 |
   | services/__init__.py | 6 | 6 |
   | services/atoms.py | 862 | 891 |
   | services/closeout_gates.py | 278 | 278 |
   | services/closure.py | 658 | 1104 |
   | services/desk_view.py | 542 | 543 |
   | services/drawer.py | 278 | 278 |
   | services/issues.py | 373 | 373 |
   | services/replace.py | 116 | 116 |
   | services/retire.py | 234 | 233 |
   | services/review.py | 865 | 865 |
   | services/tasks.py | 236 | 330 |
   | **total** | **5972** | **5293** |
   | doc_access.py (nuevo) | — | 716 |

   Borrados además: `specs/loader.py`, `specs/mermaid.py`, `spec/artifacts/*.yaml` (10) y `spec/fields/*.yaml` (49). Diff total: 92 archivos, +1094/−2417.
7. **Tests, uno a la vez** (`systemd-run --scope -p MemoryMax=2G`, `TMPDIR=/dev/shm`, `PYTHONPATH=$PWD`):
   - test_specs 5 passed · test_extension_points 5 passed · test_desk_view 9 passed, 1 skipped (el cruce con graph_ui `:132` se salta con `importorskip` porque `frontends.mindmap.deskops_routes` no es importable en este PYTHONPATH; es el mismo skip que en main).
   - test_atoms_transactions 2 · test_board_portable_references 1 passed, 1 failed (la falla previa conocida en main: `test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`) · test_cli 101 · test_closeout_gates 7 · test_desk_replace 7 · test_doc_io 8 · test_materialization_contract 5 · test_packaging 5 · test_registry_robustness 5 · test_review_doc 13 passed, 1 xfailed · test_cli_help_examples 11 · test_task_types 16 · test_closeout_declared_evidence 19 · test_review_command 12.
   - Importan módulos tocados y también corrieron: test_operational 10 · test_lifecycle_end_to_end 5 · test_lifecycle_graph 15 · test_taskdoc_read_without_overlay 1 · test_closeout_skill_links 3 · test_promotion_nesting 2 · test_graph_snapshot 9 · test_graph_extract_docs 2 · test_graph_extract_edges 3 · test_graph_extract_sources 16. Todos verdes.
   - En la primera pasada test_task_types y test_lifecycle_end_to_end fallaron por `ImportError: cannot import name 'ConflictError' from 'sldb.core.exceptions'` en el subproceso `python -m deskops`: el repo hermano `sldb` estaba a mitad de una edición ajena. Repetidos después, verdes (16 y 5 passed).
8. **`deskops doctor --root .` y `deskops view board --root .`** en este worktree: rc 0 ambos; salida byte a byte idéntica a la de los mismos comandos corridos con el código de main (`PYTHONPATH=~/proyectos/SLDB_1/deskops`, f0a4a476) sobre este mismo desk. Doctor: "Desk is healthy, with 4 alert(s)" (las 4 preexistentes). `git status -- desk .sldb` vacío antes y después.
9. **CHANGELOG.** Una entrada en `## [Unreleased]` / `### Changed`.

## Adónde fue cada uno de los 17 helpers

| helper (en operations) | destino |
|---|---|
| `_read_doc` | `doc_access.read_doc(path, model)` (con la caché `_DOC_PAYLOADS`) |
| `_write_doc` | `doc_access.write_doc(root, path, model, payload)` |
| `_write_new_doc` | `doc_access.write_new_doc(root, …)` |
| `_remove_created_file` | `doc_access.remove_created_file(path)` |
| `_track_created_document` | `doc_access.track_created_document(root, …)` |
| `_track_created_artifact` | `doc_access.track_created_artifact(root, …)` |
| `_coerce_list` | `doc_access.coerce_list(value)` |
| `_resolve_glob` | `doc_access.resolve_glob(root, directory, doc_id)` |
| `_resolve_artifact_selector` | `doc_access.resolve_artifact_selector(root, …)` |
| `_resolve_artifact_selector_multi` | `doc_access.resolve_artifact_selector_multi(root, …)` |
| `_resolve_task_payload` | `doc_access.resolve_task_payload(root, task_id)`; normaliza con `compile_task_spec(raw, entry_node="")` (q13) |
| `_hydrate_task` | `doc_access.hydrate_task(payload)` (+ `doc_access.load_task(root, task_id)`) |
| `_normalize_task_payload` | borrado; absorbido por `specs.compiler.compile_task_spec` (q13) |
| `_append_task_to_board` | `TasksService._append_task_to_board` |
| `_add_closeout_facts` | `TasksService.add_closeout_facts` (llama a `closure.has_verified_task_closeout_evidence` / `has_verified_task_pill_graduation`) |
| `_reference_points_to_atom` | `services/atoms.py: reference_points_to_atom(root, reference)` (función de módulo; la usan AtomsService y ClosureService) |
| `_transitions_from` | `lifecycle.transitions_from(root, node, spec=None, *, snapshot=None)`; la caché del snapshot es `lifecycle.ReadSnapshot` |

Otra lógica que salió de la fachada (q17): `verify_task_closeout` y sus helpers (`_declared_closeout_evidence`, `_closeout_reference_evidence`, `_closeout_link_gate`, `_reference_points_to_routed_follow_up`, `_reference_points_to_existing_route`, `_changed_file_link_evidence`, `_skill_guard_test_evidence`, `_atom_linked_test_paths`, `_generated_artifact_source_finding`, `_find_generated_artifact_source_sibling`, `_declares_materialization_sources`, `_normalize_repo_relative_path`, `_dedupe_preserve_order`, `_build_closeout_graph_context`, `CloseoutGateReport`) → `ClosureService`; `registered_task_types` → `services/tasks.py: registered_task_types(root)` + `TasksService.registered_task_types()` (con la caché por instancia); `create_task_bundle`, `bind_pill_to_task`, `list_tasks`, `show_task`, `_lifecycle_gates`, `render_next_action_diagram` → `TasksService`; `ensure_workspace`, `create_artifact`, `edit_artifact_field`, `list_artifacts`, `show_artifact`, `list_repo_task_routes`, `_editable_artifact`, `_resolve_ritual_selector`, `_frontmatter_id`, `_tracked_task_paths`, `_artifact_path`, `_artifact_glob_pattern`, `_registered_repositories`, `_repository_root`, `_resolve_repo_board_task_path`, `_task_route_summary`, `_merge_unique`, `_parse_field_value`, `ARTIFACT_MODELS/PATHS/SUBJECTS`, `_TASK_OWNED_FIELDS`, `slugify`, `DocumentRecord`, `RepoTaskRoute` → `doc_access` (operations los reexporta); `atom_folder_axis`/`_atom_doc_path` (de AtomsService) → `doc_access.atom_folder_axis/atom_doc_path`; `_declared_evidence_list` → `models/task_types.py: declared_evidence_list`; los dataclasses `Atom*Result` → `services/atoms.py`, `TaskBundle` → `services/tasks.py`, `CloseoutGateReport` → `services/closure.py` (todos reexportados desde `deskops.operations`).

## Métodos de la fachada que no quedaron en "una llamada" (q17)

- `__init__` y `_setup_logging`: construcción del objeto y del logger; no son operaciones.
- `read_snapshot()`: context manager que abre/cierra `self.snapshot` (un `lifecycle.ReadSnapshot`); es estado de la fachada, no una delegación. Los servicios lo leen por el atributo público `operations.snapshot`.
- Las propiedades `closeout_gates`, `closure`, `drawer`, `tasks`, `atoms`: construcción perezosa de cada servicio (una llamada al constructor, cacheada).
- Alias privados (comentario que nombra CC34): `_read_doc`, `_resolve_glob`, `_registered_repositories`, `_repository_root` (graph_ui) y, además, `_atom_doc_path`: lo llama `deskops/domain_tree.py:218,275`, archivo fuera del alcance de este nodo. Cada alias es una llamada a `doc_access`.
- Todo lo demás (35 métodos públicos) es armado de argumentos + una llamada + return.

## Módulos conservados (q10, q16)

- `specs/loader.py` (SpecRegistry) y `specs/mermaid.py`: borrados. Solo los importaban `tests/test_specs.py`, `test_extension_points.py`, `test_materialization_contract.py` y `test_packaging.py`; ninguno de `deskops/` los importaba fuera de `deskops/specs/`. El test de mermaid se borró con el módulo.
- `specs/compiler.py` y `specs/__init__.py`: se quedan (exportan `compile_task_spec`, `compile_artifact_spec` y los `Compiled*Spec`).
- `spec/workflows/task_lifecycle.yaml`: se queda (CC31). Se carga solo por `lifecycle.load_lifecycle_spec`; `workflow/next_actions.load_task_lifecycle_spec` fue borrado y `match_workflow_state`/`render_workflow_mermaid` reciben el `LifecycleSpec` (q15). `DeskopsOperations.spec_root` se queda (q12).
- `deskops/services/desk_view.py`: conserva su firma y su `DeskopsOperations(self.root)` por defecto (q9); solo cambió su acceso a documentos.
- `deskops/runtime/next_actions`: no existe; nada que conservar.

## Inventario para CC38 (q4)

Chequeos de UN documento que viven en Python fuera del modelo, encontrados al mover helpers; no se movieron:

- `doc_access.write_doc`: rechaza reescribir un documento cuyo modelo no puede leer un campo (`is_unreadable_by_model` / `unread_section_fields`) o que tiene headings/claves de frontmatter no declarados (`find_structural_noise`, `undeclared_frontmatter_keys`).
- `doc_access.edit_artifact_field`: campos propiedad del flujo (`_TASK_OWNED_FIELDS` de la tarea; `verdict`, `reason`, `disposed_at`, `disposed_by` de la review) rechazados en Python.
- `doc_access.frontmatter_id`, `_task_route_summary` y `deskops/workspace._frontmatter_task_type`: parsean el frontmatter a mano (YAML entre `---`) en vez de leer por el modelo; `_task_route_summary` exige `id` con prefijo `task-` y lee un `Status:` legado.
- `ClosureService._declares_materialization_sources` / `_generated_artifact_source_finding`: leen frontmatter/JSON de un artefacto renderizado para exigir `source_atoms` o `provenance`.
- `ClosureService._reference_points_to_existing_route` y `services/atoms.reference_points_to_atom`: existencia de un documento por `stem` recorriendo carpetas (`task-*.md`, `issue-*.md`, `atoms/**/*.md`).
- `services/tasks.registered_task_types`: filtra las entradas del store a subclases de `TaskDoc` con `task_type` por defecto no vacío.
- `doc_access._tracked_task_paths`: lee `.sldb/core/documents/<Modelo>/*.yaml` directamente para resolver nombres de archivo legados.

## Hipótesis y desvíos

- **`doc_access._tracked_task_paths` importa `deskops.services.tasks.registered_task_types` dentro de la función** (import perezoso): q17 manda la lógica del registro de tipos a `services/tasks.py`, y la resolución de selectores legados (en `doc_access`) la necesita. No hay ciclo en tiempo de import.
- **`__artifact__` en `ReviewDoc`: no se declara.** `spec/artifacts/` no tenía `review.yaml` ni `_ARTIFACT_DEFAULTS` lo listaba; `artifact.review` no es creable (`create: False`). `artifact_id_pattern("artifact.review")` sigue dando `"{slug}"` como antes. `test_specs` lo fija.
- **`compile_artifact_spec` con `status_default` None** (atom, materialization): conserva el `"active"` histórico (antes venía del `.get("status_default", "active")` sobre un YAML sin la clave); ninguno de los dos modelos tiene campo `status`, así que no es observable.
- **Orden de claves de `resolve_task_payload`**: al normalizar con `compile_task_spec(…, entry_node="")`, `current_node` queda al final del dict en vez de después de `files`. El contenido es idéntico; ningún consumidor serializa ese dict (hidrata `Task` o lee claves). El payload de `create_task_bundle` es el mismo de antes.
- **`ClosureService._is_under`** ya existía (no resuelve `path`); el helper movido de operations, que resuelve ambos lados, se llamó `_resolved_is_under` para no cambiar ninguno de los dos comportamientos.
- **Servicios `TasksService`, `AtomsService` y `ClosureService` exigen ahora el parámetro `operations`** (antes construían uno si faltaba). Los construye la fachada; `cli/commands/closeout.py` y `tests/test_doc_io.py` ya pasaban el suyo. Los servicios siguen usando la fachada solo por atributos públicos (`closure`, `closeout_gates`, `registered_task_types()`, `logger`, `snapshot`).
- **Tests adaptados a los nombres movidos** (fuera de los cuatro de specs): test_operational (`tasks._append_task_to_board`, `closure.has_verified_task_pill_graduation`, parches sobre `doc_access.track_created_*`), test_cli (`doc_access.resolve_artifact_selector_multi`), test_lifecycle_end_to_end (`closure.close_auto`), test_closeout_gates (parches sobre `closure.build_closeout_graph_context` y `lifecycle.transitions_from`).
- **`deskops/cli/model_introspection.py`** tenía dos imports sin uso (`dataclass_field`, `Collection`) ya en main; no se tocaron.
- **Docs**: `README.md`, `docs/knowledge-graph/desk-source-graph-vocabulary.md` y `docs/diagrams/process/current-agent-workflow-and-automation.{md,mmd}` mencionan `spec/artifacts`/`spec/fields`; `docs/` no está en los files del nodo, así que quedan para quien materialice el átomo correspondiente.
- **sldb**: no se escribió nada. La falla transitoria de import (`ConflictError`) vino de una edición ajena en curso en `~/proyectos/SLDB_1/sldb`; queda como hipótesis para el coordinador si reaparece en la suite integrada.
- Nada se tocó en `desk/` ni en `.sldb/`.
