# Informe del worker CC33a: recibos de evidencia del closeout

Worker: cc33a-worker (robocop2). Worktree `deskops-wt-cc33a`, rama `wt/cc33a`, base `a63142d1`. Sin push.
TaskDoc: `desk/tasks/task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador.md`.
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/cc33a/`.

## Qué cambió

- `deskops/models/review.py`:
  - `ReviewKind` suma `evidence`.
  - Hay un Literal nuevo, `EvidenceFact` (`tests|commit|atom|materialization|document|external`, o vacío).
  - Dos campos opcionales, `fact` y `value`, con default `""`. Están en el template justo después de `kind`.
  - El validador exige `fact` cuando `kind = evidence` y prohíbe `fact` y `value` en los demás kinds (a2).
  - Un `model_validator(mode="before")` lee como vacíos los `fact`/`value` ausentes, igual que `TaskDoc._apply_absent_frontmatter_defaults`. Así los recibos existentes se leen sin cambiar en disco.
  - `REVIEW_ID_PATTERN` admite `review-<task>-evidence-<fact>-<n>`.
- `deskops/services/closure.py`:
  - `verify_task_closeout(selector, *, write_receipts=False)` queda como orquestador. Corre los productores igual que antes, arma el mismo envelope y, con `write_receipts`, llama a `_write_evidence_receipts`.
  - Helpers nuevos, todos en closure.py:
    - `_evidence_facts`: kind → veredicto, value y reason (b1, r4, r7).
    - `_link_documents`: ids de atom y de materialization a partir de la evidencia del link gate.
    - `_normalized_reference`: POSIX relativo, conserva `::node`.
    - `_evidence_input_sha256` (r3).
    - `_evidence_receipts`: recibos previos del mismo fact.
    - `_not_intact_documents`, con `check_doc_anchors` (r5).
    - `_task_model` (r6, la misma lectura `doc_status` que `services/review.py`).
    - `_closeout_identity`.
  - Constante `EVIDENCE_ENGINE = "deskops-closeout"`.
  - No toqué ningún `close_*` ni `_gate_outcome`.
- `deskops/services/closeout_gates.py`: un solo método nuevo, `full_commit_sha(reference)`. Reusa `reference_points_to_commit` y devuelve el id de 40 caracteres que va en el `value` de commit (b2).
- `deskops/cli/commands/closeout.py`: `_verify` llama a `ops.closure.verify_task_closeout(task, write_receipts=True)`. La salida (JSON en stdout, línea de gate y alertas en stderr) no cambia.
- `tests/test_closeout_evidence_receipts.py` (nuevo) y `tests/test_review_doc.py` (+6 tests del modelo).
- `CHANGELOG.md`: una entrada en Added.

### wc -l

| archivo | antes (a63142d1) | después |
|---|---:|---:|
| deskops/services/closeout_gates.py | 293 | 306 |
| deskops/services/closure.py | 1215 | 1435 |

## Mapa kind → productor → recibo

| fact | productor (el que ya corre verify) | accepted si | value (ordenado, unido con `\n`) | hash de archivos en input_sha256 | reason si rejected |
|---|---|---|---|---|---|
| tests | `CloseoutGatesService.reference_points_to_test` (vía `closeout_reference_evidence`) | alguna referencia pasa | las referencias, ruta POSIX relativa, conserva `::node` | sí, por cada ruta de archivo | `No resolvable test evidence reference found.` |
| commit | `reference_points_to_commit` (+ `full_commit_sha`) | alguna referencia pasa | id completo de 40 caracteres | no (r3) | `No resolvable commit reference found.` |
| atom | `_closeout_link_gate` (`graph:…->atom:<id>`, `atom-doc:<path>`, referencia a atom) | gate ok y hay enlace desde un átomo | ids `atom-…` | no (value son ids) | mensajes de los findings del gate, unidos con `; ` |
| materialization | `_closeout_link_gate` (`materialization:materialization:<id>->path`) | gate ok y hay enlace desde una materialization | ids `materialization-…` | no | igual que atom |
| document | `reference_points_to_document` | alguna referencia o archivo pasa | rutas POSIX relativas | sí | `No existing document (…) found in references or files.` |
| external | `reference_points_to_url` | alguna referencia es una URL | URLs | no | `No http(s) URL found in references.` |

Cada recibo:

- Ruta: `desk/reviews/<task>/evidence-<fact>-<n>.md`, id `review-<task>-evidence-<fact>-<n>`.
- `kind: evidence`, `engine: deskops-closeout`.
- `actor`/`disposed_by`: la identidad del desk.
- `created_at` = `disposed_at`.
- `subject: doc:<Modelo>:<task>`, pinneado por sldb en la reescritura.
- `reason` si accepted: `verified: <fact> <value>` (r7).

Lo escribe `desk_transaction` de `doc_access`, con `tx.create` y después `tx.update` del mismo payload en la misma transacción (c1). Ese segundo guardado es el que pinnea `@sha256` (GO07). No usé `_write_review`: hacía falta el `update` en la misma transacción y los campos `fact`/`value`, y eso cambia su comportamiento más allá de agregar parámetros opcionales (r9). Por eso el helper vive en closure.py, como permite c3.

Cuándo no se escribe (c2):

- Se salta el recibo si ya hay uno del mismo fact con el mismo `input_sha256` y su id no aparece entre las alertas de `sldb.api.anchors.check_doc_anchors(store)`, es decir, si está intacto.
- Usé `check_doc_anchors` (r5), no el campo `subject__anchor_state`.
- `check_doc_anchors` solo corre si hay algún candidato con el mismo hash.
- Si el contrato cambió, se escribe `n+1` y el viejo queda igual.

## Aceptación, línea por línea

| línea (a7 / Done When) | evidencia |
|---|---|
| verify sobre task.code con commit en HEAD, test existente y atom enlazado → tres recibos accepted y el mismo envelope | `test_verify_writes_three_accepted_pinned_receipts_and_the_same_envelope`: compara el JSON del CLI con `verify_task_closeout` sin escritura (`==`); `evidence-{tests,commit,atom}-1` accepted, `subject` con `@sha256:`, `input_sha256` según r3 y anclas intactas. Pasa. |
| sin commit → recibo commit rejected | `test_without_a_commit_the_commit_receipt_is_rejected`: reason `No resolvable commit reference found.`, value vacío; tests y atom accepted. Pasa. |
| segunda verify sin cambios → sin recibos nuevos | `test_a_second_verify_without_changes_writes_no_receipt`. Pasa. |
| goal editado → recibos changed (anchor_state) | `test_editing_the_goal_leaves_the_receipts_changed_and_verify_writes_new_ones`: `check_doc_anchors` da `anchors/doc_changed` para los tres; la verify siguiente escribe `-2` con el mismo `input_sha256`, intactos, y los `-1` no cambian. Pasa. |
| (extra) sin store no hay recibos | `test_verify_without_a_store_writes_no_receipt`. Pasa. |
| ReviewDoc admite kind evidence con fact y value | `test_review_doc.py`: roundtrip con value multilínea, evidence sin fact falla, fact fuera del vocabulario falla, fact/value fuera de evidence fallan, un recibo sin las claves nuevas se sigue leyendo. 19 passed, 1 xfailed (el xfail ya estaba). |
| test_closeout.py | 49 passed |
| test_closeout_atomless.py | 15 passed |
| test_closeout_declared_evidence.py | 19 passed |
| test_closeout_skill_links.py | 3 passed |
| test_closeout_gates.py | 7 passed |
| test_closeout_test_paths.py | 31 passed |
| test_review_doc.py | 19 passed, 1 xfailed |
| test_closeout_evidence_receipts.py (nuevo) | 5 passed |
| test_cli (desde /dev/shm, worktree detach en 273dc44f) | 101 passed |
| test_output_goldens (desde /dev/shm, sin --update-golden) | 7 passed: goldens de ayuda y de salida idénticos (a4/r10, ninguno cambió) |
| wc -l antes y después | tabla de arriba |
| CHANGELOG | entrada en `### Added` |

Otros archivos que leen tareas, reviews o closeout, de a uno:

- `test_closeout_resolved_by` 19 passed.
- `test_review_command` 12 passed.
- `test_activation_rules`, `test_review_record` y `test_desk_view` excedían el timeout de 900 s por archivo. Los corrí por nodo y todos pasan (`test_desk_view::…graph_ui…` sigue skipped, como antes). El detalle está en `batch2.txt`.
- `test_board_portable_references` 3, `test_cli_grammar` 2, `test_command_registry` 3, `test_desk_sync` 8, `test_inbox_promote_cli_gaps` 20, `test_materialization_targets_outside_package` 4, `test_doctor_unmodeled_surfaces` 4, `test_retire_cli` 11, `test_lifecycle_graph` 9, `test_operational` 10, `test_scion_runtime` 13, `test_task_lifecycle_validator` 36, `test_transaction` 11, `test_specs` 5, `test_task_types` 16 y `test_task_policy_leaks` 7: todos passed (`batch4.txt`).
- `test_cli_escape_hatches` (9) y `test_lifecycle_end_to_end` (5) excedían el timeout por archivo. Los corrí por nodo, y el parametrizado con `-k`: todos passed (`batch5.txt`, `escape-param.log`).
- `sldb stores check --store .sldb`: rc 0, sin errores; solo las 35 alertas contract-mutation de H-CC33a-2 (`stores-check.log`).

La copia de /dev/shm se borró con `git worktree remove --force` sin procesos dentro.

## Desvíos

1. **La escritura es opt-in, no un efecto de toda llamada a verify.** `verify_task_closeout` tiene `write_receipts=False` por defecto, y solo `deskops closeout verify` (CLI) pasa `True`. La misma función la llaman:
   - la vista del board (`services/desk_view.py`), que es solo lectura (`test_no_view_writes`);
   - `_gate_outcome` de `closeout commit`, donde los recibos ensuciarían el commit de cierre (el `.sldb` entra con `add -A` y el recibo no), y su ancla se perdería al destrackear la tarea.

   Como el gate de cierre no cambia hasta CC33b, dejé esas dos rutas sin escribir. CC33b decide si `closeout commit` escribe recibos antes de leerlos con las reglas.
2. **Link gate sin documento enlazante.** Hay casos en que el gate pasa sin nombrar ningún atom ni materialization: desk exento (`knowledge-coverage-exempt: no local atom documents`), solo follow-up o solo guard-test de skill. Ahí no se escribe recibo atom ni materialization, porque r4 pide como value el id del documento enlazante y no lo hay. Si el gate falla se escribe un rejected: por cada tipo de enlace que sí apareció, o uno solo del primer kind declarado (atom) si no apareció ninguno. CC33b tiene que contemplarlo al escribir la regla, o pedir otro value para esos casos.
3. **Sin store no hay recibos.** No hay ancla que pinnear ni anchor_state que leer.
4. **Nombre del recibo.** Es `evidence-<fact>-<n>` y no `evidence-<n>`, para que el `n+1` de a3 cuente por fact. `REVIEW_ID_PATTERN` lo admite solo con los seis facts.
5. **docs/.** La regla común 5 pide doc en `docs/`, pero `docs/` no está en los files del TaskDoc ni del brief. No lo toqué: queda para el nodo que cambie el gate (CC33b) o para una corrección del TaskDoc.

## Hipótesis para sldb

- **H-CC33a-1 (create no pinnea):** sigue siendo H-CC32-2. Pinnear al nacer exige un `update` sin cambios en la misma transacción. Si `Transaction.create` pinneara los `__doc_anchors__`, el segundo guardado sobraría.
- **H-CC33a-2 (contract-mutation al sumar campos opcionales):** con el modelo nuevo, `sldb stores check --store .sldb` da `store/contract-mutation` (alert, rc 0) en los 35 ReviewDoc existentes, con `fields: fact, value` y fix `sldb stores update`. No toqué `.sldb/`: lo resuelve el `sldb stores build/update` del integrador. Sumar un campo opcional con default no debería contar como mutación de contrato para los documentos que no lo tienen.
- **H-CC33a-3 (consulta de anclas por documento):** para el salto de c2 hace falta saber si un recibo concreto está intacto. Hoy solo hay `check_doc_anchors(store)`, que compone el índice de todo el store; por eso solo lo llamo cuando hay un candidato con el mismo hash. Una consulta por documento, `anchor_state(store, doc_id, field)`, abarataría la verify repetida.

## Commits

- `ad450183` CC33a: closeout verify escribe recibos ReviewDoc kind evidence (WIP)
- `a6544092` CC33a: tests del modelo evidence y CHANGELOG
- `273dc44f` CC33a: helper de test evidence sin kwargs duplicados
- (este informe)
