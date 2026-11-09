# CC35a worker report: toda escritura por sldb.api.transaction; doc_io.py se borra

Worktree `deskops-wt-cc35a`, rama `wt/cc35a`, base `origin/main` 7bb0f168. Logs en
`~/proyectos/SLDB_1/coord2-ccconfig/cc35a/` (un `.log` por archivo de test, `summary-batch*.txt`,
`doctor/`).

## Qué se hizo

- `deskops/doc_io.py` (319 líneas) borrado. Sus 17 usuarios pasan a `sldb.api`.
- `deskops/doc_access.py` concentra la escritura: `desk_transaction(root)` abre
  `sldb.api.transaction` sobre `.sldb` del desk con `package_pythonpath()`; los servicios envuelven
  sus operaciones compuestas en un bloque y escriben con `create`, `update`, `delete`, `track`,
  `untrack`, `write_file` y `record` de esa transacción.
- Guarda: `read_doc` guarda, al leer, el `source_hash` que el índice del store tiene para el
  documento (`_READ_HASHES`); `update_tracked_doc` lo pasa como `expected_source_hash` a
  `Transaction.update`; `ConflictError` se traduce al mensaje de deskops (a5) como `DomainError`.
- `message send` escribe la nota (`write_file`) y la trackea (`track`) dentro de la transacción del
  store destino; `message ack` es un `update` con guarda de la nota trackeada. El rollback manual
  (`note.write_text(original)`) y las seams `track_document`/`untrack_document` se borraron.
- `tests/test_transaction.py` (432 líneas) reemplaza `test_doc_io.py` y
  `test_atoms_transactions.py`.

## Mapa doc_io → sldb.api

| doc_io (main 7bb0f168) | Ahora | Dónde |
|---|---|---|
| `DocTransaction(root)` (re-entrante, rollback propio de bytes + entradas) | `doc_access.desk_transaction(root)` = `sldb.api.transaction(root/.sldb, pythonpath=package_pythonpath())`; anidado se une al abierto; sin store cede `None` | atoms (split, merge, retarget), tasks (create_task_bundle), closure, drawer, issues, replace, retire, doc_access |
| `DocTransaction.write(path, model, payload)` (untrack + write + re-track con force) | `doc_access.write_doc`: trackeado → `Transaction.update(ref, payload, expected_source_hash=…)`; no trackeado → `Transaction.write_file`; sin store → escritura plana | write_doc (todos los servicios), review.dispose, scion (run.md existente), message ack (vía `update_tracked_doc`) |
| `DocTransaction.write` + `track` para documentos nuevos | `doc_access.create_doc` = `Transaction.create(model, name, payload, path)` | create_artifact (atom, pill, materialization), create_task_bundle, atoms split/create_from_source, review (receipt), scion (run.md nuevo) |
| `write_new_doc` (plano) | `doc_access.write_new_doc` = `Transaction.write_file` (lo usa `domain_tree.py`, fuera de scope, seguido de `track_created_document`) | doc_access |
| `DocTransaction.track` / `doc_io.track(force=True)` | `Transaction.track(path, model, name)` (`doc_access.track_created_document`, replace, issues, atoms retarget, message, repo register) o `sldb.api.track_document_file(…, force=True)` fuera de transacción (workspace.migrate_task_types, desk.migrate_legacy_faq_model) | |
| `DocTransaction.untrack` / `doc_io.untrack` (no trackeado → False) | `doc_access.untrack_doc(root, path\|name)` = `Transaction.untrack(name)` si el índice lo tiene (closure, drawer, atoms); `sldb.api.untrack_document` directo (workspace, desk missing docs) | |
| `DocTransaction.delete` | `doc_access.delete_doc` = `Transaction.delete(ref)` si trackeado, si no `record` + unlink | atoms.delete_atom, retire, drawer.remove_entry, repo remove |
| `DocTransaction.record` | `Transaction.record(path)` | atoms._rewrite_inbound_atom_references, replace, retire (drawer board), drawer, issues |
| `is_tracked` | `doc_access.index_entry(root, path) is not None` (atoms.delete_atom); tests: `sldb.api.doc_exists` | |
| `register_model` | `sldb.api.add_model(store, ref, pythonpath=…)` | bootstrap, workspace.register_local_task_type_models, desk.migrate_legacy_faq_model |
| `link_store_alias` | `sldb.api.link_store(store, other, name, replace=…)` | bootstrap |
| `inherit_model_from` | `sldb.api.inherit_model(store, ref, pythonpath=…)` | bootstrap |
| `init_store_at` | `sldb.api.init_store(path=…)` | bootstrap |
| `init_relations_in` | `sldb.api.init_relations(store, pythonpath=…)` | bootstrap, lifecycle |
| `update_store_indexes_in` | `sldb.api.update_store_indexes(store, pythonpath, wait=…)` | bootstrap, workspace.seed_desk, desk update |
| `remove_model_from` | `sldb.api.remove_model(store, name, pythonpath=…, untrack_documents=…)` | desk.migrate_legacy_faq_model |
| `PRIVATE_SLDB_IMPORTS` (`sldb.runtime.validation.render_model_markdown`) | sin equivalente: `doc_access` ya importaba `render_model_markdown` para sus refusals y la escritura plana | |

`bootstrap.py` (P4): solo el import y las 7 llamadas, sin otro cambio de lógica (a3, c2).

### Funciones que viven en `doc_access` porque agregan lógica de deskops (a2)

- `desk_transaction(root)`: pythonpath por defecto del paquete y "sin store → sin transacción"
  (desks de test sin `deskops init`; `has_store` usa `sldb.store.layout.store_exists`, porque un
  `.sldb/` que solo tiene `runtime/` no es un store).
- `index_entries(root)` / `index_entry(root, path)` / `forget_index(root)`: el mapa ruta relativa →
  (model, name, source_hash) de lo que el store trackea, leído de los índices (mecanismo c5, abajo).
- `read_doc` (existente) + `_note_read`: guarda el hash del índice al leer. `_store_root_of(path)`
  encuentra el root con store del documento leído.
- `update_tracked_doc(tx, root, path, entry, payload)`: la guarda y la traducción de
  `ConflictError` al mensaje de a5.
- `conflict_error(root, path)`: el mensaje de a5 (b1: ruta relativa a la raíz con `/`).
- `write_doc` (existente): refusals de deskops (campos ilegibles, ruido estructural que se borraría)
  y la elección update / write_file / plano.
- `create_doc(root, path, model, payload, name)`: refusal de sobreescritura + `Transaction.create`
  (sin store: archivo plano).
- `write_new_doc` / `track_created_document` / `remove_created_file`: se mantienen con su firma
  porque `deskops/domain_tree.py` (fuera del scope) los llama; `track_created_artifact` decide qué
  kinds se trackean al crear.
- `delete_doc(root, path)`: "no trackeado se borra igual" y "sin store → unlink".
- `untrack_doc(root, ref)`: "no trackeado o sin store → False", por ruta o por nombre.
- `relative_path`, `has_store`, `store_path`, `_model_name`, `_write_text`: utilidades de ruta.

## Mecanismo de la guarda (b3, c5)

Elegido: **(i) vía pública de `sldb.api`**: `store_fingerprint(store).documents["Model:name"].source_hash`
para el hash del índice, y `tracked_documents(store, ["Model/name", …])` para la ruta trackeada de
cada entrada. Las dos leen solo los índices (sin importar modelos ni extraer documentos):
0.1 s en frío y ~5 ms en caliente en el desk de deskops (344 documentos), contra 1.1 s / 0.2 s
de `load_runtime_documents` (que además salta los documentos cuyo modelo no importa).
Descartado (ii) `expected=` con el payload: compara contra el payload que sldb extrae del disco,
y rompería b3 cuando un documento editado a mano no re-extrae igual que lo que leyó deskops; y
(iii) `sldb.store.*`: no hizo falta.

Caché: `index_entries` se guarda por proceso con la firma (mtime_ns, size) de
`.sldb/core/store_index.yaml`, que cada escritura de sldb mueve (`cascade_store_hash`) y una
edición a mano no; además `forget_index(root)` tras cada escritura de deskops.

Por qué cumple b3: el hash del índice es el del texto que el store indexó. Un documento editado a
mano y no reindexado conserva ese hash en el índice; `read_doc` captura ese mismo valor y
`Transaction.update` lo compara contra el índice → sin conflicto; `save_document_payload` reindexa
después. Test: `test_a_document_edited_by_hand_still_takes_a_deskops_edit`.
Si otro escritor pasa por sldb entre la lectura y la escritura, el índice cambia y la guarda falla:
`test_a_document_the_store_rewrote_after_deskops_read_it_is_refused` (sin monkeypatch) y
`test_update_with_a_stale_source_hash_is_the_deskops_conflict` (hash viejo inyectado, texto exacto
de a5 en stderr, exit 1, stdout vacío, archivo intacto).

Qué updates llevan guarda (b4): todo `write_doc` sobre un documento trackeado pasa por
`update_tracked_doc`; el hash es el que `read_doc` capturó para esa ruta (si deskops no leyó el
documento en el proceso, se pasa el hash actual del índice: guarda neutra). `advance` escribe en
`services/tasks.advance_task` vía `write_doc` (c4). `message ack` captura `index_entry` antes de
leer la nota y pasa ese hash. Creaciones y `write_file` no llevan guarda.

## Punto del fallo inyectado (a6, b2)

`services/atoms.py:merge_atom` conserva el orden referrers → destino → origen, con las tres
escrituras dentro de `desk_transaction`. El test
`test_merge_failure_at_the_source_write_leaves_desk_and_store_as_they_were` reemplaza
`doc_access.write_doc` por una versión que lanza cuando `path == source_path` (la segunda
`_write_doc` del merge), tras comprobar que el destino ya cambió y el referrer ya apunta al destino;
luego compara el sha256 de todos los archivos de `desk/` y `.sldb/core/` y la salida de
`python -m sldb stores check` antes y después: iguales.

## Aceptación, línea por línea

1. **`grep -rn 'doc_io\|DocTransaction' deskops/` vacío.** Sí (exit 1 del grep, sin líneas). Lo fija
   además `tests/test_transaction.py::test_doc_io_is_gone`, y
   `test_no_deskops_module_imports_write_side_sldb_internals` mantiene la frontera (ningún módulo
   de deskops importa `sldb.store.ops`, `sldb.cli.commands` ni `sldb.api.documents.{create_,update_,delete_,track_,untrack_}*`).
2. **Fallo inyectado en atoms merge (a6, b2).**
   `test_merge_failure_at_the_source_write_leaves_desk_and_store_as_they_were`: sha256 de `desk/` y
   `.sldb/core/` y salida de `sldb stores check` iguales antes y después; el test comprueba que al
   fallar ya se habían escrito el destino y el referrer. Más:
   `test_merge_restores_referrers_and_atoms_when_the_target_update_fails` (falla
   `save_document_payload` de sldb), `test_split_restores_source_and_store_when_the_second_atom_create_fails`,
   `test_delete_failure_keeps_the_file_and_the_store_entry`,
   `test_a_conflict_inside_a_compound_write_writes_nothing`.
3. **Conflicto (a5, b1) y edición a mano (b3).**
   `test_update_with_a_stale_source_hash_is_the_deskops_conflict`: stderr exacto
   `Error: desk/tasks/<id>.md changed since deskops read it; nothing was written. Re-run the command.`,
   exit 1, stdout vacío, sin traza, archivo intacto.
   `test_a_document_the_store_rewrote_after_deskops_read_it_is_refused`: conflicto real sin
   monkeypatch. `test_a_document_edited_by_hand_still_takes_a_deskops_edit`: edición a mano +
   `deskops edit` → exit 0, las dos ediciones en el archivo, `doc_status` ok, `stores check` PASS.
4. **message send/ack sin rollback manual.** `grep -n "note.write_text(original" deskops/cli/commands/message.py`
   vacío; `_deliver_note` y `_ack_note` escriben dentro de `sldb.api.transaction(store_destino)`.
   `test_message_cli` 10 passed, `test_message_delivery` 6 passed; aserciones intactas (ver desvíos
   por el punto de inyección y la fixture).
5. **Tests de a uno** (`summary-batch1..3.txt`, logs por archivo):

   | archivo | resultado |
   |---|---|
   | test_transaction | 11 passed |
   | test_message_cli / test_message_delivery | 10 / 6 passed |
   | test_atoms_cli / test_atoms_merge / test_atoms_split / test_atoms_create_from_source | 4 / 5 / 3 / 3 passed |
   | test_retire_cli / test_issue_cli / test_desk_replace | 11 / 9 / 7 passed |
   | test_operational | 10 passed |
   | test_lifecycle_end_to_end / test_lifecycle_graph | 5 / 9 passed |
   | test_scaffold_golden | 3 passed |
   | test_cli | 101 passed |
   | test_output_goldens / test_cli_help_examples (sin `--update-golden`) | 7 / 11 passed |
   | test_closeout_gates / test_closeout / test_closeout_declared_evidence / test_closeout_atomless | 7 / 49 / 19 / 15 passed |
   | test_registry_robustness / test_review_doc / test_review_command / test_scion_runtime | 5 / 13 (+1 xfailed) / 12 / 13 passed |
   | test_desk_sync / test_add_task_from_drawer / test_task_types / test_repo_identity | 8 / 3 / 16 / 8 passed |
   | test_migrate_desk_stores / test_inbox_promote_cli_gaps / test_doctor_model_registration / test_federated_models | 16 / 20 / 8 / 2 passed |

   Tanda final tras el ajuste de `has_store` (`summary-batch4.txt`): test_atoms_merge 5,
   test_atoms_cli 4, test_message_cli 10, test_desk_view 9 (+1 skipped), test_inbox_promote_cli_gaps 20 passed.
   No corrí `test_board_portable_references` (falla conocida en main) ni `test_skill_cli_drift`
   (entorno). Ningún golden se actualizó.
6. **`deskops doctor` en los 6 desks (a8).** `doctor6.sh` (plantilla n7c): copias en
   `/mnt/ssd/proyectos/SLDB_1/.tmp-cc35a-doctor` (borradas), python con cwd neutro, PYTHONPATH =
   `origin/main` (7bb0f168, `git archive`) vs el worktree; stderr `deskops from …` confirma qué
   código se importó. `doctor/run.log`: deskops, sldb, spec2viz, scion, pron, graph_ui →
   **identical** (misma salida y mismo exit, con las rutas de las copias normalizadas). Los
   exit 1 de los cinco hermanos son hallazgos preexistentes, iguales con main.
7. **`wc -l` antes (origin/main) / después:**

   | archivo | antes | después |
   |---|---|---|
   | deskops/doc_io.py | 319 | 0 (borrado) |
   | deskops/doc_access.py | 709 | 948 |
   | deskops/bootstrap.py | 393 | 396 |
   | deskops/cli/commands/desk.py | 428 | 431 |
   | deskops/cli/commands/message.py | 509 | 505 |
   | deskops/cli/commands/repo.py | 205 | 187 |
   | deskops/lifecycle.py | 267 | 267 |
   | deskops/runtime/scion.py | 397 | 398 |
   | deskops/services/atoms.py | 875 | 869 |
   | deskops/services/closure.py | 1104 | 1103 |
   | deskops/services/drawer.py | 278 | 282 |
   | deskops/services/issues.py | 373 | 375 |
   | deskops/services/replace.py | 116 | 120 |
   | deskops/services/retire.py | 233 | 233 |
   | deskops/services/review.py | 865 | 860 |
   | deskops/services/tasks.py | 338 | 336 |
   | deskops/services/__init__.py | 6 | 6 |
   | deskops/workspace.py | 725 | 728 |
   | tests/test_doc_io.py | 248 | 0 (borrado) |
   | tests/test_atoms_transactions.py | 134 | 0 (borrado) |
   | tests/test_transaction.py | 0 | 432 |
   | tests/test_cli.py | 3140 | 3134 |
   | tests/test_message_cli.py | 273 | 274 |
   | tests/test_closeout_gates.py | 316 | 314 |
   | tests/test_registry_robustness.py | 231 | 217 |
   | tests/test_review_doc.py | 228 | 228 |
   | tests/test_desk_replace.py | 174 | 175 |
   | tests/test_operational.py | 200 | 204 |
   | CHANGELOG.md | 160 | 161 |

8. **CHANGELOG.** Una entrada en `## [Unreleased]` / `### Changed`.

## Hipótesis para sldb (no se escribió nada en sldb)

- `Transaction.track` y `Transaction.create` no tienen `force`: un documento con headings dentro de
  un campo (lo que `atoms split` usa) no puede entrar al store por la transacción bajo la política
  por defecto (`structural-noise` → alert → refusal en `create`/`track`), aunque
  `track_document_file(force=True)` y `apply_includes` sí lo admiten. Pedir `force` en la
  transacción, o que `Policy.of_store` lo resuelva por modelo desde la declaración del desk.
- Un accesor público del índice por documento: hoy el `source_hash` sale de `store_fingerprint`
  (todos los documentos) + `tracked_documents` (todas las rutas). Un
  `sldb.api.document_entry(store, ref) -> DocumentEntry` evitaría cargar el índice entero por lectura.
- `DocRefStatus` podría traer `source_hash` (c1 señala que hoy no lo trae).

## Desvíos y observaciones

- **Documentos con bloque de proveniencia.** Todo documento trackeado que deskops crea
  (`Transaction.create`) o actualiza (`Transaction.update` → `save_document_payload`) sale con el
  bloque `sldb:` (by/at/via/authority) en el frontmatter, como cualquier documento que escribe
  sldb (cuatro archivos del desk ya lo traían). Un re-render sin cambios conserva el bloque y no
  mueve la fecha. Los goldens de salida y de scaffold quedan idénticos; un test de `test_cli`
  (`test_edit_task_refuses_to_erase_undeclared_content`) insertaba una clave con
  `replace("---\nid:", …)` y ahora la inserta con `replace("\nid:", …)`, misma aserción.
- **Refusals de sldb al crear.** `add atom` con headings `###` en `answer` ahora lo refusa sldb
  (ruido estructural); antes deskops lo escribía y trackeaba con `force=True`. En el desk de deskops
  no hay átomos así. El test de split sobre un desk con store escribe el átomo origen y lo trackea
  con `track_document_file(force=True)`, como hace `desk update --apply`.
- **Raíces sin store.** Sin `.sldb` no hay transacción: los servicios escriben archivos planos sin
  rollback (antes `DocTransaction` restauraba bytes también ahí). `deskops init` siempre crea el
  store; los tres tests de `test_operational` que probaban rollback en un `tmp_path` sin store
  pasan a `lifecycle_desk` con el fallo inyectado en `create_document` de sldb.
- **Fixtures que simulaban sldb.** `tests/test_cli.py::_setup_inbox_identity_env` creaba un
  `.sldb/` vacío y parcheaba `message.track_document`/`registered_model`; ahora inicializa un store
  real en el repo destino con `InboxNoteDoc` registrado. Lo mismo en
  `test_registry_robustness::test_repo_register_accepts_optional_path_flag…` (store real con
  `RepositoryDoc`; `assert tracked == […]` pasa a `doc_exists`). Las aserciones de los demás tests
  no cambian.
- **Punto de inyección de `test_message_ack_restores_note_when_tracking_fails`.** Parcheaba la seam
  `message.untrack_document` (borrada); ahora hace fallar `sldb.api.documents.transaction_ops.save_document_payload`.
  Aserciones (exit 1, bytes de la nota, `doc_status` ok, `stores check` PASS) intactas.
- **Mensaje de conflicto.** `main` imprime los `DeskopsError` tal cual (`str(exc)`), así que el
  `DomainError` lleva el prefijo `Error: ` en el mensaje. `deskops review …` captura `DomainError` y
  antepone otro `Error: ` (`cli/commands/review.py`, fuera de mis files): un conflicto en
  `review dispose` saldría como `Error: Error: …`.
- **`has_store`** usa `sldb.store.layout.store_exists` (módulo interno de solo lectura, ya
  importado por deskops para `project_root`): un `.sldb/` con solo `runtime/` (los goldens de
  salida lo crean con `graph build`) no es un store.
- **Tests parcheables.** `write_doc` sigue siendo el punto único de escritura de documentos; los
  tests de fallo lo interceptan ahí o en `sldb.api.documents.transaction_ops.*`.
- Las copias de desks (`.tmp-cc35a-doctor`, `.tmp-cc35a-timing`) se borraron. Nada se escribió a
  mano en `desk/` ni en `.sldb/`; `git status` no los muestra.
