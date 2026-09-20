# Plan de implementación: deskops sobre pron

Reemplaza el plan anterior (refactor CRUD en 6 lanes), que quedó obsoleto
cuando la arquitectura pasó a **formas** (s-expressions) y a **contrato
primero**.

Arquitectura: `docs/architecture-deskops-on-pron.md`, `docs/workflow-deskops-on-pron.md`,
`docs/taxonomy-deskops.md`, `docs/contract-first.md`.
Declaración: `spec/world/deskops-world.yaml`.

## Reglas de ejecución (para todo worker)

1. **Env obligatorio**: `cd <worktree> && export PYTHONPATH=$PWD`. Hay un
   `deskops` 0.1.0 rancio en site-packages que secuestra los subprocess.
2. **Una tarea por dispatch.** Cada tarea de abajo es un dispatch.
3. **El worker NO commitea.** Implementa, corre su gate, reporta. El
   coordinador revisa el diff y commitea.
4. **Nunca `git add -A`.** Solo los archivos de la tarea.
5. Baseline: **250 pass / 9 known-red** (medido en F3 T3.4 sobre `deskops-pron`).
   Ninguna tarea sube el rojo. Los 9 rojos están en la tabla de abajo, con la
   fase que los cierra: son consequence de F2 (modelos) y los cierra F4/F6.
6. Todo gap de pron va a `desk/pron-gap-log.md`, no se parchea alrededor.

## Estado actual

- **F0 hecho**: worktree, branch, baseline medido, 9 vistas spec2viz, world
  declarado, seam `deskops/world.py`.
- **F1 hecho** (`cd3db56`): plan viejo eliminado, `PythonSymbolDoc` registrado,
  store y transcript de herdr saneados.
- **F2 hecho** (`915ea13`, `a0d3f88`, `ece9f32`, `306f516`): `TaskDoc` partido en
  núcleo + intent/acceptance/binding, planificación y contrato modelados,
  modelos derivados de código, dormidos instanciados, absorbidos borrados.
- **F3 hecho** (`eef7e47`, `fefa147`, `d014d9e`, `79c6bc4`): 23 relation types
  declarados, condiciones derivadas, status derivado, bootstrap in-process.
  - Gate F3, parte store: **cumplido**. `World.refresh()` no levanta error
    después del bootstrap y `deskops.derived_status.tasks_in_status(world,
    "planning")` responde con las tasks en planning.
  - Gate F3, parte `pron say`: **no cumplido**, y no es de esta fase:
    `pron say "which tasks are in planning?"` contesta `I don't have "in"`
    porque la proyección operacional todavía no tiene vocabulario para un
    status derivado. Eso es F4 T4.2 (lectura sobre `World.store`/`World.graph`)
    y queda registrado en el gap-log.
- **F4 sigue sin empezar**: `deskops/operations.py` (2.703 líneas) y sus
  `advance_task` siguen siendo el runtime viejo.

### Los 9 known-red

| Test | Causa | Fase que lo cierra |
| --- | --- | --- |
| `test_cli.py::test_cli_help_uses_deskops_name` | superficie de verbos pedida distinta a la del parser | F6 T6.1 |
| `test_cli.py::test_edit_task_updates_modeled_field_from_cli` | escribe `current_node`, campo que T2.6 borró | F4 T4.3 |
| `test_cli.py::test_show_list_and_advance_task_uses_operational_runtime` | `Current node` / status lineales | F4 T4.4 |
| `test_cli.py::test_advance_task_blocks_testing_and_closeout_without_required_evidence` | guardas del runtime viejo | F4 T4.4 |
| `test_cli.py::test_advance_task_accepts_atom_reference_as_closeout_evidence` | evidencia del runtime viejo | F4 T4.5 |
| `test_lifecycle_end_to_end.py::test_task_lifecycle_runs_from_intake_to_closeout_via_real_cli` | ciclo completo sobre el runtime viejo | F4 T4.5 |
| `test_promotion_nesting.py::...flattens_nested_structured_sections...` | promoción contra el `TaskDoc` viejo | F4 T4.3 |
| `test_atom_folder_axis.py::test_reorganize_moves_flat_atoms_and_updates_store` | reorganización de átomos no actualiza el store | F6 T6.3 |
| `test_atoms_cli.py::test_atoms_delete_force_removes_file_and_untracks_store` | delete de átomo no destrackea | F6 T6.3 |

- Pendiente de limpieza histórica: `3c041ee` arrastró la migración del store y
  el transcript de herdr (ya separado en F1).

### Qué hay hoy en el store (medido 2026-09-20)

- `TaskDoc` 1, `BoardDoc`/`PillDoc`/`RitualDoc`/`CrossroadDoc` 0, `AtomDoc` 92,
  `RelationTypeDoc` 34, `PythonSymbolDoc` 0, `PlanDoc`/`SymbolContractDoc` 0.
- Consecuencia: el status derivado de la task activa da `drawer` ("no BoardDoc
  routes this task") porque el desk todavía no está migrado al store — eso es
  F7 T7.1 — y los símbolos de código no están poblados (F5 T5.1). La derivación
  es correcta para lo que hay; los saltos de status se prueban en
  `tests/test_derived_status.py` sobre un store armado a mano.

---

## F1 — Limpieza y base (3 tareas)

**T1.1 Sanear `3c041ee`**
Separar el seam y el gap-log de la migración del store y del transcript.
`.herdr-coordination.md` al ignore, `HERDR_TRANSCRIPT` fuera del repo.
Gate: `git show --stat HEAD` solo toca `deskops/world.py`, `desk/pron-gap-log.md`, `.gitignore`.

**T1.2 Borrar el plan obsoleto** (hecho)
El plan anterior (refactor CRUD en lanes) quedó eliminado; este documento es el
único plan y la task activa apunta acá.
Gate: ningún `*.md` del repo contiene el nombre del plan viejo (grep da 0).

**T1.3 Registrar los modelos de sldb que se usan**
`PythonSymbolDoc` de sldb registrado en el store del worktree.
Gate: `python -c "from deskops.world import get_world; print('PythonSymbolDoc' in get_world('.').store.model_names())"` → True.

---

## F2 — Modelos (6 tareas)

Cada tarea: escribir el modelo pydantic con `__template__`, registrarlo,
y un test de round-trip (render → extract → payload idéntico).

**T2.1 Partir `TaskDoc`** → núcleo + `TaskIntentDoc` + `AcceptanceDoc` + `TaskBindingDoc`.
**T2.2 Planificación** → `PlanDoc`, `PlanTargetDoc`, `PlanIterationDoc`.
**T2.3 Contrato** → `SymbolContractDoc`.
**T2.4 Código derivado** → `CommitDoc`, `ChangeDoc`, `TestCoverageDoc`.
**T2.5 Instanciar los dormidos** → `BoardDoc`, `PillDoc`, `RitualDoc`, `StepDoc`, `InboxNoteDoc`, `ProtoAtomDoc`, `HookDoc`, `RunDoc` (+ `move_id`, `model`, `tokens_in`, `tokens_out`, `cost_usd`).
**T2.6 Borrar los absorbidos** → `ConditionDoc`, `OperatorDoc`, `EdgeDoc`, `ChecklistDoc`, `RoutineDoc`; `AtomDoc` baja a `PrimitiveDoc`; fuera `current_node`/`history`.

Gate por tarea: `pytest tests/test_model_templates.py` + registro OK.

---

## F3 — El mundo (4 tareas)

**T3.1 `RelationTypeDoc`** — las 23 relaciones del grafo declaradas y `init_relations`. (hecho)
**T3.2 Status derivado** — `deskops/derived_status.py`: la escalera del spec
sobre las condiciones; `status` nunca se escribe. (hecho)
**T3.3 Condiciones derivadas** — `deskops/derived_conditions.py`: los predicados
calculados sobre los documentos y las aristas `contracts`/`evidences`/`verifies`. (hecho)
**T3.4 Bootstrap del mundo** — `deskops init` construye todo lo anterior desde
`spec/world/deskops-world.yaml`, in process. (hecho; commit `79c6bc4`)

Gate: `World.refresh()` sin error; el status derivado responde qué tasks están
en planning (`pron say` queda para F4 T4.2, ver gap-log).

---

## F4 — Capa de formas (5 tareas)

El reemplazo real de `operations.py`.

**T4.1 Constructores base** — `(create …)`, `(change …)`, `(assert …)`, `(move …)`.
**T4.2 Lectura** — board, `next`, `list`, `show` sobre `World.store`/`World.graph`.
**T4.3 Escritura de task** — promote, add, edit, bind como movimientos atómicos.
**T4.4 Advance** — `deskops advance` = evaluar una transición con guarda. Aquí muere `advance_task`.
**T4.5 Closeout** — evidencia desde el ledger, no desde heurísticas de archivos.

Gate: los tests de lifecycle y promoción pasan contra la nueva capa.

---

## F5 — Código, AST y contratos (4 tareas)

**T5.1 Poblar símbolos** — `sldb selfdoc python-sync` sobre `deskops/` y `tests/`.
**T5.2 `TestCoverageDoc`** — derivar de los imports declarados de los tests (granularidad módulo).
**T5.3 git → documentos** — `CommitDoc`/`ChangeDoc`, hunk resuelto a símbolo por rango.
**T5.4 Gate de contrato** — `planning → execution` exige `SymbolContractDoc` completo.

Gate: desde una task, listar qué cambió, cuándo, qué símbolo y qué tests correr.

---

## F6 — CLI (3 tareas)

**T6.1 Handlers a la capa de formas** — parser 1:1, handlers vaciados.
**T6.2 `next` y `advance`** sobre el mundo, con `--diagram` desde el store.
**T6.3 Resto** — doctor, drift, materialize, repo, graph, runtime.

Gate: `python -m deskops --help` idéntico; suite completa verde.

---

## F7 — Cierre (3 tareas)

**T7.1 Migrar el desk** — 137 átomos, 34 pills, 12 rituales, 21 crossroads al store.
**T7.2 Gap-log a pron** — nota al inbox de pron (incluye `calls` en selfdoc).
**T7.3 Closeout** — docs, skills, commit de fase.

Gate final: suite verde, CLI operativo, desk migrado, ledger con movimientos reales.

---

## Diferido (decidido, no ahora)

- Hooks a pron: se quedan en deskops hasta estabilizarse.
- Deriva de conocimiento (átomos vs símbolos borrados): necesita F5 poblado.
- Impacto cruzado entre repos: necesita F5 en más de un repo.
- Métricas de velocidad: no cambian ninguna decisión del harness.

## Orden

F1 → F2 → F3 → F4 → F5 → F6 → F7. Dentro de F2 las tareas son casi
independientes; el resto es secuencial por archivos compartidos.
