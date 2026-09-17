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
5. Baseline: **216 pass / 3 known-red**. Ninguna tarea sube el rojo.
6. Todo gap de pron va a `desk/pron-gap-log.md`, no se parchea alrededor.

## Estado actual

- F0 hecho: worktree, branch, baseline medido, 9 vistas spec2viz, world
  declarado, seam `deskops/world.py` (commit `3c041ee`, alcance sucio).
- Pendiente de limpieza: `3c041ee` arrastró migración del store y el
  transcript de herdr.

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

**T3.1 `RelationTypeDoc`** — las 24 relaciones del world declaradas y `kgdb init`.
**T3.2 Estados y transiciones** — documentos `State` con `machine: TaskDoc.status` y aristas `transitions_to` con sus guardas.
**T3.3 Condiciones derivadas** — los predicados calculados de las guardas
(`plan_targets_without_contract`, `contracts_implemented`, `tests_from_contracts_passing`).
**T3.4 Bootstrap del mundo** — `deskops init` construye todo lo anterior desde `spec/world/deskops-world.yaml`.

Gate: `World.refresh()` sin error; `pron say "which tasks are in planning?"` responde.

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
