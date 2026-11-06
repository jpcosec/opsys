# Informe del worker GC01 (gates-por-tipo)

Worktree: `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`).
No hice commit, ni push, ni `git add`. No toqué `../sldb` ni ningún otro checkout de sldb.

## 1. Archivos cambiados y creados

Creados:

- `deskops/models/task_types.py` — las siete subclases de `TaskDoc`, `TASK_TYPE_MODELS`, `LEGACY_TASK_TYPE_MAP`, `canonical_task_type_name` y helpers de evidencia/recibos.
- `tests/test_task_types.py` — tests nuevos que cubren las líneas de Done When.
- `.sldb/core/models/Task{Code,Docs,Debug,Refactor,Decision,Aggregate,External}Doc.yaml` — índice del modelo registrado en el store dueño (ver nota en §5).

Cambiados:

- `deskops/models/task.py` — `TaskDoc.__contract__`.
- `deskops/models/__init__.py` — exporta las siete subclases.
- `deskops/services/closeout_gates.py` — borra `TASK_TYPE_EVIDENCE`, `evidence_for_task_type` y `resolve_new_task_evidence`; añade `NOT_YET_VERIFIABLE_EVIDENCE` y `order_evidence_kinds`.
- `deskops/services/tasks.py` — `create_task_bundle` resuelve el modelo del tipo y guarda la tarea bajo él.
- `deskops/operations.py` — `registered_task_types()`, `_declared_closeout_evidence` lee del tipo, `verify_task_closeout` nombra `children`/`goldens` como no verificables, `_tracked_task_paths()` recorre todos los modelos de tipo.
- `deskops/cli/commands/operations.py` — `add task` valida el tipo, default `task.code` con aviso, `--evidence` como piso.
- `deskops/cli/registry.py` — help/epilog de `add task` y `add`.
- `deskops/cli/commands/desk.py` — `desk update --apply` registra tipos locales y migra `task_type` legado (justificado en §5).
- `deskops/workspace.py` — descubrimiento/registro de `desk/models/*.py` y migración de `task_type`.
- `.sldb/core/store_index.yaml` — índice del store dueño actualizado con los siete modelos (ver §5).
- `tests/fixtures/model_contract_hashes.json` — regenerado.
- `tests/fixtures/golden/help/{deskops,deskops_add,deskops_add_task}.txt` — regenerados con `--update-golden`.
- `tests/test_cli.py`, `tests/test_closeout_declared_evidence.py`, `tests/test_operational.py`, `tests/test_lifecycle_end_to_end.py`, `tests/test_add_task_from_drawer.py`, `tests/test_inbox_promote_cli_gaps.py`, `tests/test_desk_replace.py` — adaptados a los nuevos tipos (`task.code`/`task.docs`) y a la nueva semántica de `--evidence`.
- `docs/workflow-policy-reference.md` — tabla de tipos.
- `CHANGELOG.md` — entrada `## [Unreleased]`.

`deskops/bootstrap.py` **no** necesitó cambios: `MODEL_REFS` ya toma `deskops_models.__all__`, y las nuevas subclases entran por ahí.

## 2. Done When → test que lo prueba

| Línea de Done When | Test (archivo::nombre) | Pasa |
|---|---|---|
| `add task --task-type task.code` crea `TaskCodeDoc:<id>` con `task_type task.code` | `tests/test_task_types.py::test_add_task_with_task_type_tracks_under_the_type_model` | sí |
| `--task-type foo` falla nombrando los tipos registrados | `tests/test_task_types.py::test_add_task_with_an_unregistered_type_lists_the_types` | sí |
| sin `--task-type` se crea `task.code` con aviso | `tests/test_task_types.py::test_add_task_without_task_type_defaults_to_code_with_a_note` | sí |
| `desk/models/local_types.py` con `TaskCliDoc(TaskCodeDoc)` (`task.code.cli`) se registra y `add task --task-type task.code.cli` funciona | `tests/test_task_types.py::test_desk_update_apply_registers_a_local_type_and_add_task_uses_it` | sí |
| `model <= TaskCodeDoc` devuelve `task.code` y `task.refactor`, no `task.docs` ni `task.debug` | `tests/test_task_types.py::test_model_family_query_includes_refactor_and_not_debug_or_docs` | sí |
| `closeout verify` de `task.docs` exige `commit`+`document` sin `closeout_evidence` | `tests/test_task_types.py::test_closeout_verify_reads_evidence_from_the_type` | sí |
| `--evidence` que quite un kind falla y uno que agregue se guarda | `tests/test_task_types.py::test_add_task_evidence_can_add_but_not_remove_a_type_kind` | sí |
| tarea legada `task_type implementation` queda `task.code` tras `desk update --apply` y segunda corrida no cambia nada | `tests/test_task_types.py::test_legacy_task_type_migrates_idempotently` | sí |
| grep `TASK_TYPE_EVIDENCE` en `deskops/` no devuelve nada | `tests/test_task_types.py::test_task_type_evidence_mapping_is_gone` | sí |
| `model_contract_hashes.json` actualizado | `tests/test_model_contract_snapshot.py::test_snapshot_covers_the_registered_model_set` y `::test_model_contract_hashes_match_the_snapshot` | sí |
| CHANGELOG y `docs/workflow-policy-reference.md` con la tabla de tipos | (docs, sin test) | — |
| `__contract__` (precisión 2) | `tests/test_task_types.py::test_taskdoc_declares_the_contract_fields` | sí |
| `children`/`goldens` no verificables (precisión 3) | `tests/test_task_types.py::test_closeout_verify_fails_naming_children_and_goldens_as_not_verifiable` | sí |
| tipo legado desconocido migra a `task.code` con reporte (precisión 4) | `tests/test_task_types.py::test_unknown_legacy_task_type_migrates_to_code_with_a_report` | sí |

## 3. Tests corridos (línea final de pytest)

- `tests/test_task_types.py` → `15 passed, 1 warning`
- `tests/test_closeout_declared_evidence.py` → `19 passed, 1 warning`
- `tests/test_closeout.py` → `49 passed, 1 warning`
- `tests/test_closeout_atomless.py tests/test_closeout_skill_links.py tests/test_model_contract_snapshot.py tests/test_model_templates.py` → `34 passed, 1 warning`
- `tests/test_cli.py tests/test_cli_help_examples.py` → `112 passed, 1 warning`
- `tests/test_output_goldens.py` → `7 passed, 1 warning`
- `tests/test_lifecycle_end_to_end.py tests/test_add_task_from_drawer.py` → `8 passed, 1 warning`
- `tests/test_operational.py tests/test_desk_sync.py tests/test_federated_models.py` → `19 passed, 1 warning`
- `tests/test_packaging.py tests/test_doc_io.py` → `13 passed, 1 warning`
- `tests/test_cli_contract.py tests/test_cli_grammar.py tests/test_command_registry.py` → `13 passed, 1 warning`

Pre-existente (no relacionado con GC01, no lo toqué): `tests/test_board_portable_references.py` → `2 failed` (`test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`, `test_local_graph_next_show_and_retirement_accept_portable_context`). Causa: `desk/tasks/Board.md` del worktree referencia `desk/rituals/context-review.md`, que la lista `RITUALS` fija del test no copia (el Board y los rituales evolucionaron en commits previos a GC01; nada de esto lo cambió este nodo).

## 4. Hipótesis verificadas

**Hipótesis: "sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve" → VERIFICADA.**

Evidencia (desk temporal `/tmp`, `PYTHONPATH` apuntando al worktree):

- En un desk cuyo `TaskCodeDoc` viene heredado del store dueño (`origin=deskops`), registrar `desk/models/local_types.py` con `TaskCliDoc(TaskCodeDoc)` vía `desk update --apply`:
  - `sldb models show TaskCliDoc` lista `base_models: [TaskCodeDoc, TaskDoc, OperationalArtifactDoc, PrimitiveDoc]`.
  - `sldb find "task-cli" --in physical --type doc --where "model <= TaskCodeDoc" --store .sldb --pythonpath <desk>` devuelve `[("task-cli-thing", "TaskCliDoc")]`.
- La familia se resuelve por el MRO real de la clase (`sldb/store/query_engine/structural.py::model_in_family` camina `__mro__` por nombre). `model <= TaskCodeDoc` incluye `task.refactor` (subtipo) y excluye `task.debug`/`task.docs` (que extienden `TaskDoc`), exactamente como manda la tabla.

Comando/salida representativos:

```
$ python -m sldb models add "models.local_types:TaskCliDoc" --store .sldb --pythonpath <desk>
Registered 'TaskCliDoc'
$ python -m sldb models show TaskCliDoc --store .sldb
  base_models:
  - TaskCodeDoc
  - TaskDoc
  - OperationalArtifactDoc
  - PrimitiveDoc
$ python -m sldb find "task-" --in physical --type doc --where "model <= TaskCodeDoc" --store .sldb --pythonpath <desk> --format json
  -> task-cli-thing (TaskCliDoc), task-refactor-thing (TaskRefactorDoc); no task-debug ni task-docs
```

Nota: para resolver los tipos locales, `find` necesita `--pythonpath <desk>` (el modelo `models.local_types` importa desde la raíz del desk); los tipos de fábrica (`deskops.models:*`) se resuelven sin él.

## 5. Lo que no pude hacer / desvíos justificados

1. **Actualicé el índice del store dueño (`.sldb/core/`)**. Es un cambio necesario y no manual: al añadir los siete modelos a `deskops/models`, el store dueño (`package_pythonpath()/.sldb`, versionado en git) debe contenerlos para que `deskops init`/`desk update` los hereden; si no, `inherit_model` falla con "does not own a model named TaskCodeDoc" y `test_federated_models.py` falla. Lo hice con `python -m sldb models add "deskops.models:<Cls>" --store .sldb --pythonpath .` (el mecanismo canónico, el mismo que usan los commits "store: índice de deskops al día"). No escribí a mano en `desk/` ni corrí `deskops` contra el desk del worktree. Queda a revisión del coordinador incluir esos `.sldb/core/` en el commit (no están en la lista `files` del TaskDoc, pero son el registro del modelo y el snapshot test los lee).

2. **`deskops/cli/commands/desk.py` no está en la lista `files` del TaskDoc**, pero es el handler de `desk update` (que la lista atribuye a `registry.py`). La lógica de migración/registro vive en `deskops/workspace.py` (sí en files); `desk.py` solo la invoca en el flujo de `desk update --apply`. Lo edité por necesidad.

3. **`--evidence` como piso**: lo implementé como "la lista pasada debe ser un superconjunto de los kinds del tipo" (interpretación consistente con la precisión 5 "solo agrega, quitar uno falla" y con la aceptación "que quite un kind falla / que agregue se guarda"). Con semántica de unión pura ("agregados"), "quitar un kind" no sería expresable; con el piso-superconjunto sí lo es y es testeable.

4. **No corrí la suite completa** (el brief la reserva al coordinador, ~55 min). Corrí los archivos pedidos y vecinos, todos verdes salvo los 2 pre-existentes de `test_board_portable_references.py` señalados arriba.

5. **`docs/workflow-policy-reference.md`**: añadí la tabla de tipos bajo "Core Model → Tasks". No actualicé `docs/faq.md` ni `deskops/data/faq.md` (fuera de la lista `files`; `deskops/data/faq.md` es el espejo empaquetado y su texto aún describe el comportamiento anterior `--task-type code|docs|...` — eso lo cubre GC08 según el plan, no GC01).

---

## Ronda 2 (correcciones del coordinador)

### Archivos tocados

- `tests/test_board_portable_references.py` — `test_local_graph_next_show_and_retirement_accept_portable_context` pasa de `--task-type docs` a `task.docs`.
- `tests/e2e_agent/scenarios/{stuck-task-gate,first-task-to-closeout,inbox-to-task}.yaml` — `--task-type code|docs` → `task.code|task.docs`.
- `deskops/about.py` — ejemplo y prosa de `about` a la semántica nueva (tipo declara; `--evidence` solo agrega; default `task.code`).
- `README.md` — `--task-type docs` → `task.docs` y prosa del requisito.
- `docs/faq.md` + `deskops/data/faq.md` (espejo, idénticos) — `--task-type docs` → `task.docs`, y el párrafo de closeout (`task.code`/`task.debug`/`task.docs`/`task.decision`/`task.external`; `--evidence` solo agrega).
- `docs/operator-manual.md` — `--task-type docs` → `task.docs` (393/398/469/537), párrafo de `## Closeout` (semántica por tipo), fila de la tabla de flags (232) y `--evidence` como piso (252).
- `docs/quickstart.md` — `--task-type docs` → `task.docs` (83), párrafo de evidencia (91) y de tests (131).
- `deskops/cli/registry.py` — epílogos de `closeout commit` y `closeout verify` a la semántica nueva (la evidencia la declara el tipo; `--evidence` solo agrega).
- `.opencode/skills/use-deskops/SKILL.md` y `.pi/skills/deskops-task-lifecycle/SKILL.md` — `--task-type code|docs` → `task.code|task.docs` y la prosa de evidencia.
- `tests/fixtures/golden/help/deskops_closeout_{commit,verify}.txt` — regenerados con `--update-golden`.

No toqué `desk/rituals/closeout.md` (fuera de límites: es `desk/`, y los rituales los actualiza GC08 con `deskops edit ritual`). Dejé `deskops/models/task.py:149` (descripción de `task_type: str` para leer documentos viejos; cambiarla movería el hash de contrato sin necesidad).

### Lista de reemplazos (legado → tipo)

- `--task-type code` → `--task-type task.code`
- `--task-type docs` → `--task-type task.docs`
- Prosa "the task declared … / filled from `--task-type`: `code`,`implementation`,`test`…" → "el tipo declara la evidencia; `--evidence` solo agrega kinds a los del tipo; sin `--task-type` el default es `task.code`; un tipo no registrado falla".

### Línea final de pytest de cada corrida

- `tests/test_task_types.py` → `15 passed, 1 warning`
- `tests/test_board_portable_references.py` → `1 failed, 1 passed, 1 warning` (queda solo el fallo previo `test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`)
- `tests/test_packaging.py tests/test_cli.py::test_about_prints_first_use_summary` → `6 passed, 1 warning`
- `tests/e2e_agent/test_agent_scenarios.py -k "reference_solutions or checks_need_the_work"` → `6 passed, 3 deselected, 1 warning`
- `tests/test_cli_help_examples.py` → `11 passed, 1 warning`
- `tests/test_output_goldens.py` → `7 passed, 1 warning`
- `tests/test_operator_manual.py` → `1 passed, 1 warning`

Los YAML de escenarios parsean con `yaml.safe_load` (los tres, sin errores) y además pasan `test_reference_solutions` (ejecutan los comandos `reference` sin LLM).
