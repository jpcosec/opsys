# CC33b: reglas de cierre (informe del worker)

Worker: `cc33b-worker`. Worktree: `deskops-wt-cc33b`, rama `wt/cc33b`, base `5ccc29a3`. Contrato: el TaskDoc `20c10312` y su copia `eebd2077`, que solo cambia la redacción de c3. Sin push.

Commits:
- `5f52f42b`: RuleDocs de cierre por tipo, tabla `closeout-evidence.yaml`, semillas declaradas y borrado de los hechos y gates viejos.
- `f4452205`: test nuevo `tests/test_closeout_rules.py`, `docs/workflow-policy-reference.md`, CHANGELOG y ritual closeout (vía `deskops edit ritual`).
- `fb62fda5`: tests de cierre adaptados al contrato nuevo, más el helper `tests/closeout_desk.py`.
- `2ceb4888`: `test_cli.py` y el helper de closeout adaptados.
- `47dd4e06`: goldens de scaffold, autorizado por el coordinador (b8).
- El último commit trae este informe.

Logs en `~/proyectos/SLDB_1/coord2-ccconfig/cc33b/`: `test-*.log`, `doctor-{before,after}-*.log`, `view-board-{before,after}-*.log`, `rules-explain-*.log`.

## Qué se hizo

- **RuleDoc de cierre por tipo (c2):** `deskops/data/rules/rule-closeout-task-<tipo>.md`, siete archivos.
  - Forma: `subject: model <= <Clase>`, `where: current_node = "ritual-closeout"`, `moment: on_transition`, `severity: error`, mensaje en español que nombra el tipo.
  - Cláusulas: una por kind, `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")`. atom|materialization va como `or` de dos `any`.
  - task.refactor solo suma `any(^subject: kind = "goldens" and anchor_state = "intact" and verdict = "accepted")` (b4). Las cláusulas de task.code le llegan por la familia.
  - task.aggregate pide solo `commit`, sin cláusula de hijos (b4).
- **Semillas (a4):** `deskops/data/desk_declaration.yaml` las declara como seeds `managed` y agrega el include `RuleDoc` del glob `desk/lifecycle/rule-closeout-*.md`. El coordinador sumó ese archivo a files. `desk update --apply` las escribe y una segunda corrida dice `Desk is up to date.` (sandbox y `test_desk_update_writes_the_closeout_rules_and_a_second_run_changes_nothing`).
- **Arista:** `closeout-task_completes.md` queda con `condition: status = "ready_for_testing"`, sin `has(closeout_evidence_verified)`.
- **Tabla (c3):** `deskops/data/rules/closeout-evidence.yaml` (task_type → kinds).
  - La leen `closure.py` (qué productores corre verify) y `cli/commands/operations.py` (el piso de `--evidence`), a través de `task_types.closeout_evidence_kinds(model)`.
  - Un subtipo del desk lee la entrada de su ancestro de fábrica más cercano.
  - `test_the_rules_ask_for_exactly_the_kinds_of_the_table` compara, por tipo, la unión de las cláusulas de las reglas de su familia contra la tabla.
- **closeout commit (b2):**
  - No escribe recibos. Corre verify en solo lectura para imprimir la línea declaró/encontré y las alertas, y evalúa las reglas `on_transition` de la tarea leída en `ritual-closeout` (`ClosureService.closeout_rule_findings`).
  - Con un error, la salida es: `Closeout gate blocked <task>; the closing commit was not made.`, una línea `- error: [rules/rule-closeout-<tipo>] ...` por finding y `Run 'deskops closeout verify --task <task>' ...`.
  - Una tarea que el store no trackea no se puede evaluar y queda bloqueada con esa razón.
- **Recibo exento (b3):** cuando el link gate pasa sin documento enlazante, verify escribe un recibo `atom` accepted con `value: exempt: <evidencia del gate>`, por ejemplo `exempt: knowledge-coverage-exempt: no local atom documents`.
- **`--evidence` solo suma (c5):**
  - Un kind agregado se verifica y recibe su recibo. Si falla, es la alerta `added_closeout_evidence_not_verified` y no bloquea.
  - Un kind agregado fuera del vocabulario es la alerta `unknown_closeout_evidence`.
  - `goldens` lo lee la regla y `children` ya no se declara, así que se fue `closeout_evidence_not_verifiable`.
- **Reglas de campo (b7):** van como RuleDocs `on_write` de severidad alert, con `subject: model <= TaskDoc`:
  - `rule-closeout-alert-implicit-code`: `has(task_type) or nonempty(closeout_evidence)`, con el mismo texto de la alerta `closeout_evidence_not_declared`, que se borró de verify.
  - `rule-closeout-alert-pill-graduation`: `not nonempty(pills) or any(references: model <= AtomDoc)`. El chequeo viejo no tenía mensaje (era un hecho).
  - Quedan en código, con hipótesis H1: el vocabulario de `closeout_evidence`, `python_changes_without_declared_tests` y la forma de URL de `external`. "graduación de pills (operations.py)" no existe en `deskops/operations.py`; el chequeo vivía en `closure.has_verified_task_pill_graduation`.
- **Borrado (a5/c4):**
  - Los `__closeout_evidence__` de `task_types.py`.
  - `closeout_evidence_verified` y `pill_graduation_verified`.
  - `TasksService.add_closeout_facts` (el `_add_closeout_facts` del contrato), `ClosureService.has_verified_task_closeout_evidence` y `has_verified_task_pill_graduation`.
  - `task_type_closeout_evidence`, que quedó sin uso, y `NOT_YET_VERIFIABLE_EVIDENCE`.
  - Los productores de `closeout_gates.py` se quedan (c4).
- **Ritual (c9):** `deskops edit ritual closeout steps ...` reescribe tres pasos: verify escribe los recibos, la evidencia es la del tipo más lo que `--evidence` sumó, y commit evalúa la regla sin escribir recibos. El commit incluye el `.sldb` que escribió deskops.
- **Doc y CHANGELOG:** `docs/workflow-policy-reference.md` tiene la sección "Closeout rules" con la tabla de reglas, el orden verify→commit, el recibo exento, DA5 y las alertas de campo; también se actualizaron la tabla de tipos y el ritual. CHANGELOG suma entradas en Added, Changed y Removed.

## Correcciones del TaskDoc (no son desvíos del worker)

- **a4/c2:** el TaskDoc pedía `where current_node = "ritual-testing"`, pero `task_completes` sale de `ritual-closeout` (`source_id: RitualDoc:ritual-closeout`). Con `ritual-testing` la regla habría bloqueado `task_hands_to_closeout`. El coordinador confirmó `ritual-closeout`. Decisión revisable.
- **a7:** se agregó `deskops/data/desk_declaration.yaml` a files, solo para declarar las semillas `rule-closeout-*.md`, autorizado por el coordinador. Decisión revisable.
- **b8, golden de scaffold:** `tests/fixtures/golden/scaffold/init.json` y `update.json` cambian. Solo se suman las 9 semillas `rule-closeout-*.md` (escritas y trackeadas) y cambia el hash de `closeout-task_completes.md`. Paré, le pasé el diff al coordinador (`scaffold-golden.diff`) y él autorizó. Commit propio `47dd4e06`. Antes de commitear comprobé que el diff es idéntico al aprobado, y después `test_scaffold_golden.py` pasa sin `--update-golden`. Los goldens de ayuda y de salida no cambian.

## Aceptación línea por línea

| Línea (ACCEPTANCE / Validation / Done When) | Evidencia |
|---|---|
| Sin recibo commit accepted, la arista task_completes aparece en edges_blocked con la cláusula fact = "commit" | `test_without_an_accepted_commit_receipt_task_completes_is_blocked_on_the_commit_clause`: verify escribe `evidence-commit-1` rejected y `lifecycle.transitions_blocked(..., "ritual-closeout", ...)` devuelve `[task_completes]` con findings `rules/rule-closeout-task-code` cuyo `what` contiene `fact = "commit"`. |
| Editar goal tras verificar vuelve a bloquear | `test_with_every_receipt_the_edge_holds_and_editing_the_goal_blocks_it_again`: con todos los recibos la arista se cumple (`transitions_holding` = `[task_completes]`); tras `edit task goal` vuelve a `edges_blocked` con la cláusula `anchor_state = "intact"`. En el sandbox, el caso malo de refactor sale `false` por lo mismo (`rules-explain-types.log`). |
| grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío | `grep -rn "closeout_evidence_verified\|pill_graduation_verified\|_add_closeout_facts\|__closeout_evidence__" deskops/` sale con exit 1, sin líneas. También se borró `add_closeout_facts`, el nombre real. |
| Los chequeos de CC38 como RuleDoc con su función vieja borrada | Ninguna de las 8 filas se expresa en el lenguaje de reglas sin filesystem, nombre de archivo, archivos que no son del store o la API de tags (DO7). Las 8 quedan en el código con su razón (tabla de abajo) y se eximen del grep por b6. Las reglas de campo de b7 que sí se expresan (código implícito y graduación de pills) pasaron a RuleDoc y su código viejo se borró. |
| Tests de closeout verdes | `test_closeout*.py` (8 archivos) y `test_closeout_gates.py` verdes; tabla de tests abajo. |
| Goldens idénticos | `test_output_goldens.py` (ayuda y salida): 7 passed, sin `--update-golden`, desde `/dev/shm`. Scaffold: única excepción, autorizada (b8). |
| deskops doctor sin hallazgos nuevos en los 6 desks | Antes y después: el mismo conjunto de líneas `- ...` en los 6 desks (diff vacío, sección de abajo). git status sin cambios en cada desk. `deskops view board`: salida byte a byte idéntica antes y después en los 6. |
| docs/workflow-policy-reference.md | Sección "Closeout rules", tabla de tipos, ritual 4 y regla de commit. |
| Ritual closeout vía deskops | `deskops edit ritual closeout steps ...` en `f4452205` (pasos de verify, evidencia y commit). |
| CHANGELOG | Entradas en Added (reglas de cierre), Changed (closeout commit y verify) y Removed. |
| Tests de a uno, test_cli y goldens desde /dev/shm | Cada archivo se corrió solo, con la guarda, `MemoryMax=2G` y `TMPDIR=/dev/shm`. `test_cli.py`, `test_output_goldens.py`, `test_scaffold_golden.py` y `test_desk_view.py` corrieron desde `/dev/shm/deskops-cc33b` (worktree efímero, ya removido). |
| 4 pasos del workflow en clon limpio | Los corre el coordinador (c7). |
| Cada RuleDoc nueva con `sldb rules explain`, caso bueno y malo (b5) | `rules-explain-code-alerts.log` y `rules-explain-types.log`. Las 7 de cierre dan `false` sin recibos (exit 1) y `true` con los recibos aceptados (exit 0). En refactor, el caso malo es goldens no intacto: tras editar goal da `false`. pill-graduation da `true` y `false`. implicit-code da `true` con task_type y `false` con una tarea sin task_type ni closeout_evidence (`TaskDoc:task-legacy`, `seen: {"closeout_evidence": null, "task_type": ""}`; esta salida es de la sesión y el log guarda solo el caso true). |

## Tests (último resultado de cada archivo, uno a la vez)

| Archivo | Resultado |
|---|---|
| `tests/test_activation_rules.py` | 10 passed |
| `tests/test_board_portable_references.py` | 3 passed |
| `tests/test_cli.py` | 101 passed |
| `tests/test_cli_contract.py` | 8 passed |
| `tests/test_cli_escape_hatches.py` | 9 passed |
| `tests/test_cli_grammar.py` | 2 passed |
| `tests/test_cli_help_examples.py` | 11 passed |
| `tests/test_closeout.py` | 49 passed |
| `tests/test_closeout_atomless.py` | 15 passed |
| `tests/test_closeout_declared_evidence.py` | 19 passed |
| `tests/test_closeout_evidence_receipts.py` | 5 passed |
| `tests/test_closeout_gates.py` | 7 passed |
| `tests/test_closeout_resolved_by.py` | 19 passed |
| `tests/test_closeout_rules.py` | 12 passed |
| `tests/test_closeout_skill_links.py` | 3 passed |
| `tests/test_closeout_test_paths.py` | 31 passed |
| `tests/test_command_registry.py` | 3 passed |
| `tests/test_composition.py` | 3 passed |
| `tests/test_desk_sync.py` | 8 passed |
| `tests/test_desk_view.py` | 9 passed, 1 skipped |
| `tests/test_doc_readability.py` | 6 passed |
| `tests/test_doctor_model_registration.py` | 8 passed |
| `tests/test_doctor_unmodeled_surfaces.py` | 4 passed |
| `tests/test_federated_models.py` | 2 passed |
| `tests/test_inbox_promote_cli_gaps.py` | 20 passed |
| `tests/test_lifecycle_end_to_end.py` | 5 passed |
| `tests/test_lifecycle_graph.py` | 9 passed |
| `tests/test_materialization_targets_outside_package.py` | 4 passed |
| `tests/test_operational.py` | 8 passed |
| `tests/test_output_goldens.py` | 7 passed |
| `tests/test_packaging.py` | 6 passed |
| `tests/test_promotion_nesting.py` | 2 passed |
| `tests/test_registry_robustness.py` | 5 passed |
| `tests/test_retire_cli.py` | 11 passed |
| `tests/test_review_command.py` | 21 passed |
| `tests/test_review_doc.py` | 19 passed, 1 xfailed |
| `tests/test_review_record.py` | 21 passed |
| `tests/test_scaffold_golden.py` | 3 passed |
| `tests/test_scion_runtime.py` | 30 passed |
| `tests/test_specs.py` | 5 passed |
| `tests/test_supervise.py` | 7 passed |
| `tests/test_task_lifecycle_validator.py` | 36 passed |
| `tests/test_task_policy_leaks.py` | 7 passed |
| `tests/test_task_types.py` | 16 passed |
| `tests/test_transaction.py` | 11 passed |

Tests adaptados al contrato nuevo, con la razón de cada cambio:
- `test_task_types.py`: los kinds se leen de la tabla. El subtipo local lee los de task.code, y aggregate declara solo `commit`.
- `test_closeout_declared_evidence.py`, `test_closeout_atomless.py` (un test) y `tests/closeout_desk.py` (helper nuevo): un repo con store, la tarea tipada y trackeada, y verify antes de commit. Antes la lista de la tarea reemplazaba a la del tipo; ahora DA5 dice que solo suma.
- `test_lifecycle_graph.py` y `test_cli.py` (3 tests): el bloqueo en `ritual-closeout` ahora lo da la regla y no la condición de la arista. El test "atom reference as evidence" ahora comprueba el recibo atom aceptado.
- `test_lifecycle_end_to_end.py` y `test_transaction.py`: `closeout verify` antes de `closeout commit`, en el orden del ritual.
- `test_operational.py`: se reemplazan los 3 tests de la función borrada por uno que prueba la condición de la RuleDoc.
- `test_desk_sync.py`: dos globs `RuleDoc`. `test_packaging.py`: 16 semillas de reglas.

## Inventario de CC38 asignado a CC33 (8 filas, b1/c1)

Fuente: `runs/subagents/cc38-worker-report.md`. Criterio de b5: pasa a RuleDoc lo que se expresa con campos del documento, referencias, any/all sobre aristas y has()/nonempty(), probado con `sldb rules explain`. Ninguna de las 8 filas cumple ese criterio, así que todas se quedan en el código con su razón. Por b6 quedan fuera del grep, igual que p10 de CC38. No se borró ninguna función de esas filas.

| # | Chequeo | Dónde vive | Destino | Razón |
|---|---|---|---|---|
| 3 | el namespace del tag está declarado en `tag-namespaces.yaml` | `atom_tags.validate_atom_tag_namespaces` | código | Lee `desk/atoms/tag-namespaces.yaml`, que es un archivo YAML y no un documento del store (b5). La familia `builtin:tag_namespace:*` de sldb lo haría si el store declarara `tag_namespaces`; eso es la API de tags de sldb, que corresponde a DO7 (CC35d cortado; H1-H2 en el drawer de sldb 6b34cd5f). |
| 5 | todo prefijo de un domain path tiene su crossroad escrito | `domain_tree.require_domain_parents`, `_domain_errors` | código (DO7) | Necesita que `anchored_by` acepte un valor sin namespace (H1 de sldb, drawer 6b34cd5f). Queda por DO7. |
| 13 | el nombre del archivo es igual al id (átomo, crossroad, protoatom) | `services/atoms.py` (validate), `domain_tree._check_crossroad`, `_check_protoatom` | código | Necesita el nombre del archivo, y el lenguaje de reglas solo ve el payload y el nombre en el store (b5). |
| 14 | `provenance` resoluble (URL o ruta existente) | `services/atoms.py` `_provenance_is_resolvable` | código | Lee el filesystem (b5). |
| 15 | el destino de `typed_as` existe | `domain_tree._check_protoatom` | código, con hipótesis | `typed_as` no es campo de referencia de `ProtoAtomDoc` (no está en `__references__`), así que el lenguaje no tiene arista que seguir. El chequeo actual es un `rglob` sobre el filesystem. Saldría como `not has(typed_as) or any(typed_as: has(id))` si `ProtoAtomDoc` declarara `typed_as` como referencia (`deskops/models/protoatom.py`, fuera de los files de este nodo) y los protoatoms estuvieran trackeados por nombre. Lo dejo como hipótesis para un nodo que toque el modelo. |
| 18 | un solo valor del eje de carpetas (`folder_axis_value`) | `atom_tags.py`, `services/atoms.py`, `doc_access.atom_doc_path` | código | Necesita `desk/config.json` (el eje), que no es documento del store (b5). |
| 24 | un artefacto renderizado declara `source_atoms` o `provenance` | `services/closure.py` `_generated_artifact_source_finding` | código | Lee el artefacto y su fuente hermana en disco (b5). |
| 25 | la referencia apunta a un documento existente | `services/atoms.reference_points_to_atom`, `closure._reference_points_to_existing_route` | código, con hipótesis | Las referencias son cadenas libres: rutas, `ruta::nodo`, ids pelados, commits y URLs. El lenguaje trabaja en mundo cerrado y descarta en silencio la referencia que no resuelve, así que no hay predicado para decir que una referencia no resuelve. Tampoco hay cuantificador sobre los elementos de una lista cruda. Además, las dos funciones son productoras de evidencia del cierre y no invariantes del documento. Va como hipótesis H4. |

## Hipótesis para sldb (para la nota de inbox; no escribí en sldb)

- **H1. Cuantificador sobre los elementos de un valor lista.** Hoy `"x" in f` prueba pertenencia, pero no hay forma de decir "todo elemento de `f` está en [...]" ni "algún elemento de `f` matchea /re/". Sin eso quedan en el código tres reglas de campo de b7: el vocabulario de `closeout_evidence`, `python_changes_without_declared_tests` (algún elemento de `files` termina en `.py`) y la forma http(s) de una referencia `external`. Un `~` sobre una lista funciona hoy por accidente, porque busca sobre `str(lista)`, el repr de Python. No me apoyé en eso porque el contrato del lenguaje no lo fija.
- **H2. Una RuleDoc sin la clave `where` rompe `stores check`.** El changelog de sldb dice que `where` es opcional, pero un archivo sin `where:` se extrae como `None` y el modelo lo rechaza: `1 validation error for RuleDoc / where / Input should be a valid string`. Con eso, `sldb stores check` falla entero, `deskops doctor` lo reporta como desk legacy y `deskops desk update --apply` no logra reescribir la semilla, así que el desk no se repara solo. Mi workaround fue poner `where: ''` en las dos reglas alert.
- **H3. Un id pelado en `references` no resuelve a arista.** Por ejemplo `atom-closeout-receipts`. La ruta (`desk/atoms/atom-x.md`) sí resuelve. Por eso la regla de graduación de pills solo ve los átomos referenciados por ruta o por `Model:name`, mientras que el chequeo Python viejo aceptaba también el id pelado.
- **H4. Falta un predicado de referencia no resuelta** (fila #25), por ejemplo `unresolved(field)` o `count(field) = len(field)`. Por el mundo cerrado, una referencia rota hoy es indistinguible de una lista vacía.

Otras observaciones, para el coordinador y no para sldb:
- **goldens de refactor:** el recibo goldens de la activación (antes) satisface también la cláusula de cierre mientras el contrato no cambie, porque la regla no distingue antes de después (b4 pide `any(...)`). Si hace falta distinguirlo, el `ReviewDoc` necesitaría un campo de fase. Queda como hipótesis.
- **Átomos:** AGENTS.md pide reflejar en átomos las reglas nuevas de `docs/`. El átomo `atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly` habla de evidencia "declarada al crear", y con DA5 ahora es la del tipo más lo agregado. No lo toqué: está en `desk/` y fuera de mis files. Queda como follow-up.

## Desvíos

- Ninguno sobre los files autorizados: `desk_declaration.yaml` y los goldens de scaffold se tocaron con autorización.
- `tests/closeout_desk.py` es un helper nuevo bajo `tests/`, que está en files.
- Las dos reglas alert llevan `where: ''`; sin esa clave fallan (H2).
- La guarda de pytest se cambió dos veces, por indicación del coordinador.
- Mi `pkill` mató por error mis propios shells de espera. No había ningún pytest mío corriendo y se re-corrió todo.

## Capturas de `deskops doctor` (código del worktree, solo lectura)

Mismo conjunto de hallazgos antes y después en los 6 desks:
- deskops: 10 → 10 (exit 0).
- sldb: 18 → 18.
- spec2viz: 7 → 7.
- scion: 4 → 4.
- pron: 5 → 5.
- graph_ui: 8 → 8.

Los cinco últimos salen con exit 1 por errores que ya existían. Las capturas completas están en `doctor-{before,after}-<desk>.log`. Línea base, antes de cambiar código:

### deskops

```text
Alerts (the store moved under an expected change; nothing is broken):
- Edited: desk/inbox/20261029-122044-suggestion-declare-write-ya-conserva-los-globs-autorados.md (edited since the store indexed it)
- Edited: desk/inbox/20261029-122115-suggestion-traspaso-de-sesi-n-scion-piloto-coordinador-de-deskops-en-marcha.md (edited since the store indexed it)
- Edited: desk/reviews/task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados/preflight-1.md (its model's contract changed since it was indexed)
- RelationDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- ReviewDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- AtomDoc:atom-desk-health-delegates-store-diagnostics-to-sldb: 4 heading(s) the model does not declare: ## Boundary Rationale, ## Delegation Pattern, ## Evidence, ## Tags
- AtomDoc:atom-desk-health-is-measured-by-cli-diagnostics: 4 heading(s) the model does not declare: ## Diagnostic Surface, ## Repairability, ## Evidence, ## Tags
- AtomDoc:atom-desk-health-is-workspace-integrity-state: 3 heading(s) the model does not declare: ## Evidence, ## Related Atoms, ## Tags
- AtomDoc:atom-desk-repair-is-owned-by-deskops: 4 heading(s) the model does not declare: ## Owned Operations, ## Not Owned, ## Evidence, ## Tags
- ReviewDoc:review-task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados-preflight-1: subject -> TaskRefactorDoc:task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados: lost (doc:TaskRefactorDoc:task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados)
  register edits, moves and new documents with: deskops desk update --apply
Desk is healthy, with 10 alert(s).
```

### sldb

```text
Errors (the desk is broken):
- ArchitectureDoc: the model's class cannot be imported here, so its fields were not re-extracted
- PackagingDoc: the model's class cannot be imported here, so its fields were not re-extracted
- PlanDoc: the model's class cannot be imported here, so its fields were not re-extracted
- SpecDoc: the model's class cannot be imported here, so its fields were not re-extracted
- RequestDoc: the model's class cannot be imported here, so its fields were not re-extracted
- ArchitectureNarrativeDoc: the model's class cannot be imported here, so its fields were not re-extracted
- StoreReadmeDoc: the model's class cannot be imported here, so its fields were not re-extracted
- AtomicDocumentDoc: the model's class cannot be imported here, so its fields were not re-extracted
- FAQDoc: the model's class cannot be imported here, so its fields were not re-extracted
- DeskStandardsDoc: the model's class cannot be imported here, so its fields were not re-extracted
- DeskSpecDoc: the model's class cannot be imported here, so its fields were not re-extracted
Alerts (the store moved under an expected change; nothing is broken):
- store_hash: a model node moved, or the set of models changed
- SpecDoc: another class under the name of the model the store linked as 'pron' owns
- ReviewDoc:review-task-gd23-preflight-1: subject -> TaskCodeDoc:task-gd23: lost (doc:TaskCodeDoc:task-gd23)
- ReviewDoc:review-task-gd24-preflight-1: subject -> TaskCodeDoc:task-gd24: lost (doc:TaskCodeDoc:task-gd24)
- ReviewDoc:review-task-gd26-preflight-1: subject -> TaskCodeDoc:task-gd26: lost (doc:TaskCodeDoc:task-gd26)
- ReviewDoc:review-task-go05-lenguaje-de-predicados-unificado-bundle-1: subject -> TaskCodeDoc:task-go05-lenguaje-de-predicados-unificado: lost (doc:TaskCodeDoc:task-go05-lenguaje-de-predicados-unificado)
- ReviewDoc:review-task-go05-lenguaje-de-predicados-unificado-preflight-1: subject -> TaskCodeDoc:task-go05-lenguaje-de-predicados-unificado: lost (doc:TaskCodeDoc:task-go05-lenguaje-de-predicados-unificado)
  register edits, moves and new documents with: deskops desk update --apply
Run with --repair to attempt automatic fixes.
```

### spec2viz

```text
Errors (the desk is broken):
- Unregistered models: ReviewDoc, TaskAggregateDoc, TaskCodeDoc, TaskDebugDoc, TaskDecisionDoc, TaskDocsDoc, TaskExternalDoc, TaskRefactorDoc. Register them with deskops desk update --apply.
Alerts (the store moved under an expected change; nothing is broken):
- TaskDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- RelationDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- SpecDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- NotationDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- RuntimeProfileDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- ViewDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
  register edits, moves and new documents with: deskops desk update --apply
Run with --repair to attempt automatic fixes.
```

### scion

```text
Errors (the desk is broken):
- Unregistered models: ReviewDoc, TaskAggregateDoc, TaskCodeDoc, TaskDebugDoc, TaskDecisionDoc, TaskDocsDoc, TaskExternalDoc, TaskRefactorDoc. Register them with deskops desk update --apply.
Alerts (the store moved under an expected change; nothing is broken):
- RuntimeProfileDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- TaskDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- RelationDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
  register edits, moves and new documents with: deskops desk update --apply
Run with --repair to attempt automatic fixes.
```

### pron

```text
Errors (the desk is broken):
- Missing desk structure: desk/tasks/Board.md, desk/drawer/, desk/rituals/phase.md
- .gitignore: git ignores `.sldb/core/`, `.sldb/store.yaml`: the store is versioned whole, its past is read from git
- Unregistered models: AtomDoc, BoardDoc, CrossroadDoc, DeskFAQDoc, InboxNoteDoc, MaterializationContractDoc, PillDoc, ProtoAtomDoc, RepositoryDoc, ReviewDoc, RitualDoc, RoleDoc, RunDoc, RuntimeProfileDoc, StepDoc, TaskAggregateDoc, TaskCodeDoc, TaskDebugDoc, TaskDecisionDoc, TaskDoc, TaskDocsDoc, TaskExternalDoc, TaskRefactorDoc. Register them with deskops desk update --apply.
Alerts (the store moved under an expected change; nothing is broken):
- RelationDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- ReadmeDoc:readme: 2 block(s) its model does not read would be lost on a rewrite (knowledge/readme.md)
  register edits, moves and new documents with: deskops desk update --apply
Run with --repair to attempt automatic fixes.
```

### graph_ui

```text
Errors (the desk is broken):
- Tracked document is gone: desk/tasks/task-corregir-ws13-2-frontera-api-raíces-identidad-visible-y-estado-de-carga.md (restore it, or untrack it with deskops desk update --apply)
- Unregistered models: ReviewDoc, TaskAggregateDoc, TaskCodeDoc, TaskDebugDoc, TaskDecisionDoc, TaskDocsDoc, TaskExternalDoc, TaskRefactorDoc. Register them with deskops desk update --apply.
Alerts (the store moved under an expected change; nothing is broken):
- RelationDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- TaskDoc: roster hash disagrees, and documents below are damaged too
- InboxNoteDoc: roster hash disagrees but all 8 documents present are clean: the list is incomplete or a document joined/left without reindexing — `stores update` recomputes it
- RitualDoc:ritual-closeout: 1 heading(s) the model does not declare: ## Step Details
- RitualDoc:ritual-execution: 1 heading(s) the model does not declare: ## Step Details
- RitualDoc:ritual-testing: 1 heading(s) the model does not declare: ## Step Details
  register edits, moves and new documents with: deskops desk update --apply
Run with --repair to attempt automatic fixes.
```


Después: `diff` de las líneas `- ...` contra la línea base vacío en los 6 desks (`doctor-after-*.log`).
