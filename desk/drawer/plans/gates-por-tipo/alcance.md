# Alcance y estado de partida

## Estado de partida de deskops (verificado 2026-11-04, `deskops/`)

- **`task_type` es un string libre.** `TaskDoc.task_type: str = ""` con una descripción que enumera "design, implementation, test, reflection, or closeout" (`deskops/models/task.py:144-147`). Se usa solo al crear, para rellenar `closeout_evidence` desde `TASK_TYPE_EVIDENCE`, un diccionario plano `code|implementation|test → CODE_EVIDENCE; docs|spec|design → DOCUMENT_EVIDENCE; external → EXTERNAL_EVIDENCE` (`deskops/services/closeout_gates.py:30-38`, `deskops/services/tasks.py:85-86`). Un tipo desconocido no falla si trae `--evidence` (`closeout_gates.py:77-96`). No hay jerarquía ni gates por tipo.
- **La evidencia de cierre vive en la tarea.** `closeout_evidence: list[str]` con vocabulario cerrado `tests, commit, atom, materialization, document, external` (`task.py:165-172`, `closeout_gates.py:23`); una tarea sin el campo se gatea como código (`deskops/operations.py:580-588`).
- **Herencia reimplementada en Python.** `inherits_from` e `inherit_acceptance_context` (`task.py:148-154`) los resuelve `_resolve_task_payload` recursivamente, calculando `effective_references`, `effective_pills`, `effective_tags`, `effective_atoms`, `effective_validation`, `effective_done_when` (`operations.py:1028-1071`), aunque `inherits_from` ya es una arista `references` del grafo (`task.py:29-36`). El gate de cierre lee `references` crudo, no `effective_references` (`closeout_gates.py:129`, vía `operations.py:725-731`).
- **`depends_on` no tiene efecto.** Es referencia a `TaskDoc` (`task.py:29-36`, `:120-123`) y ninguna condición del ciclo de vida la lee.
- **Ciclo de vida con dos fuentes.** Estados = `RitualDoc`; transiciones = `RelationDoc` con `condition` evaluada por sldb (`deskops/lifecycle.py:1-13`). Pero `sets_status` y `terminal` salen del YAML (`lifecycle.py:48-49`, `:62-66`, `:137-150`; `deskops/spec/workflows/task_lifecycle.yaml:17-18`, `:27`, `:34`, `:41-42`). El grafo se escribe una vez y no se actualiza (`lifecycle.py:280`, `:328`, `:354`: "Existing documents are left as they are"). `advance` evalúa `condition_holds` transición por transición (`lifecycle.py:176-178`) y no usa `edges_holding`.
- **Gates como hechos inyectados.** `task_activates` tiene `condition: ""` (`task_lifecycle.yaml:26`): toda tarea activa. `task_completes` exige `has(closeout_evidence_verified)` (`:40`), un hecho que `_add_closeout_facts` escribe en el payload antes de evaluar y `advance_task` borra después (`operations.py:441-450`, `tasks.py:196-199`).
- **Dos vías de escape.** `advance --to`: si el destino es `draft|open|in_progress|blocked` escribe `status`, si no escribe `current_node`, sin condición alguna; solo `complete` y `closed` se rechazan (`tasks.py:179-192`). `edit task <campo>`: cualquier campo del modelo salvo `id`, incluidos `status`, `current_node`, `task_type`, `closeout_evidence` e `history` (`operations.py:271-282`; `deskops/cli/registry.py:225-239`).
- **Sin composición.** No existen `parent_id` ni `children` en ningún modelo de `deskops/models/`; la composición vive en scripts del drawer (`desk/drawer/plans/workspace-documental/build_plan.py`, `dag.yaml` por plan).
- **`deskops graph` construye su propio snapshot.** Nodos y aristas salen de extractores propios con regex para tareas, issues, rutas y átomos en prosa (`deskops/graph/extract_edges.py:22-34`, `:631`), además de leer el índice de aristas de sldb (`:245-310`); el snapshot tiene esquema propio (`deskops/graph/snapshot.py:17-21`).
- **Revisiones en frío por script.** `desk/rituals/context-review.md` fija el protocolo (perfil pi deepseek-flash, paso 3; dos roles antes de despachar, paso 8); `desk/rituals/execution.md` exige preflight y cold-bundle (pasos 5 a 9) y guarda la reformulación en `runs/subagents/<run-dir>/preflight.md`. Lo ejecutan dos scripts distintos: `desk/drawer/plans/workspace-documental/context_review.py` (modos `run`, `status`) y `sldb/desk/drawer/plans/grafo-operable/context_review.py` (modos `node`, `preflight`, `bundle`, `status`; tope `--max-attempts 2`; un nodo con input sin cambios no se vuelve a revisar). Ninguno escribe un documento en el desk: la disposición se escribe a mano en `reviews/rN.md`.
- **Modelos que ya sirven de base.** `RunDoc` (`deskops/models/run.py`: `run_dir`, `session_sha256`, `outcome`, `commit_sha`) y `RuntimeProfileDoc` (`deskops/models/runtime_profile.py`: binario, flags de modelo y de system prompt) son el molde de `ReviewDoc` y del perfil del motor. Los modelos se registran por `MODEL_REFS` y se heredan en cada desk desde el store de deskops (`deskops/bootstrap.py:26`, `:118-160`); sldb ya conoce `base_models` y el predicado `model <= X` (`sldb/src/sldb/store/query_engine/where_parse.py:125`).
- **Nota de sldb ya en el inbox**: `desk/inbox/20261104-213901-suggestion-sldb-eval-a-reglas-declaradas-plan-grafo-operable-...md` nombra este plan como lo que queda para deskops.

## Qué consume este plan de sldb (rev 9 de `grafo-operable/dag.yaml`)

| Nodo sldb | Qué entrega | Gate de este plan | Lo usan |
|---|---|---|---|
| GO02 | sintaxis `__contract__` y hash de contrato; firma de `eval` | (documento, sin gate) | GC01 declara `__contract__` |
| GO05 | lenguaje unificado: `and/or/not`, caminos, `any/all/none/count`, `^campo`, `+`, `anchor_state` | `G_SLDB_LANG` | GC05, GC07, GC09 |
| GO06 | `RuleDoc` (subject `model <= X`, `where`, `condition`, `severity`, `moment`), `rules check`, `rules explain` | `G_SLDB_RULES` | GC05 |
| GO07 | anclas `doc:Model:name@sha256:<hash>` en campos `__doc_anchors__`, pinneado al guardar, estados `intact/changed/lost`, `anchors check` | `G_SLDB_ANCHORS` | GC02 (acepta), GC05 |
| GO08 | evaluación `on_write/on_transition/on_check`, `edges_holding` con `findings`, `edges_blocked`, caché en `.sldb_cache` | `G_SLDB_EVAL` | GC05 |
| GO09 | `RelationDoc.attributes.sets/terminal`, `effects` en `edges_holding`, `apply_effects` | `G_SLDB_EFFECTS` | GC04 |

Cada gate `G_SLDB_*` se satisface cuando el nodo de sldb cerró en `main` de sldb y deskops pinnea en `pyproject.toml` una versión de sldb que lo contiene. Hasta entonces los nodos que lo requieren no se promueven; los que ni lo requieren ni dependen de uno que lo requiera (GC01, GC02, GC03, GC06) pueden avanzar.

## Qué produce este plan para sldb

`G_CONSUMER` (sldb `dag.yaml` rev 9, `gates.G_CONSUMER`): "en un desk temporal, una tarea sin recibo de revisión no se activa y la explicación nombra la cláusula; con recibo atado al hash de contrato vigente, se activa; con el contrato editado, el recibo queda `changed` y vuelve a bloquear". Lo produce GC05 como test de integración y lo informa a sldb con `deskops message send --to sldb` (D3).

## Reglas comunes de ejecución

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Mientras GC03 no exista, con el script gobernado de sldb apuntado a este plan; después, con `deskops review`. Una revisión en frío está aceptada cuando quien opera el desk de deskops (D3) escribe su disposición y no queda ninguna ambigüedad abierta según la guía.
2. Tope de rondas: dos a nivel de plan; una preflight y una cold-bundle por promoción, y solo se repite si el input (hash del bundle o hash de contrato del TaskDoc) cambió o con `--force` y razón escrita.
3. La validación corre con `pytest tests` en el host que el dueño indique. Un nodo no cierra con tests rojos ni saltados.
4. Toda capacidad nueva entra con: modelo o documento, comando CLI con envelope, pruebas, entrada en `CHANGELOG.md` y doc en `docs/` (manual de operador o referencia de workflow). Los rituales del desk que nombran el comportamiento cambiado se actualizan en el mismo nodo o en GC08, nunca después.
5. Nada de Python supliendo una regla: si rev 9 no fija lo que un nodo necesita, el nodo registra la hipótesis en su TaskDoc y, si bloquea, manda la nota a sldb.
6. Compatibilidad: los desks existentes migran con `deskops desk update --apply`; cada nodo que cambia un documento del desk (tipos, aristas, reglas) hace que `desk update` lo escriba o reescriba de forma idempotente y lo prueba.
7. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.
8. Las cuatro restricciones de D2 no admiten excepción por nodo: ningún nodo agrega una bandera para saltar un gate.
