Entregable: `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, sha256 `6bcdbeefb7984aecbc14f25c08e449050f6e5054f253f5102a5636ad27804ed3` (dato de `tester-v3-facts.log`; no recalculado). No leí kimun.

## Comprobaciones 1-3 y 5

| Objeto | Evidencia real leída | Veredicto |
|---|---|---|
| §2.2 Deshacer: comportamiento, granularidad y límites | `move_undo.py:28-41` (`__call__`), `:35` (`self.left`), `:54-68` (`_checked`), `:61` (salta `forget`), `:70-84` (`_changed_since`), `:74` (`left and current`), `:86-89` (`_current_hash`), `:91-103` (`_refuse_orphans`); `write.py:41-48` (`restore_field`, sin `_guard`) | **PASS**. Compara `hash_c` por documento, omite la escritura con `done=False`, comprueba antes de invertir, no comprueba `forget` ni hashes ausentes, y no hay lock entre comprobación e inversión. |
| `sldb docs update` usa camino propio, sin journal y sin `save_document_payload` | `doc.py:62-70` (`update`), `:57-60` (`_write_and_rehash`; llamada real a `write_rendered_document` en `:60`), `:73-81` (`_save_updated`, `store_lock` en `:74`); sin `record`/`append_entry` en `doc.py`, `ops.py` ni `derived_rebuild.py`; `payload_save.py:16`; `fields_save.py:10` | **PASS**. No llama `save_document_payload` y no escribe entrada de journal. |
| `version` = `content_hash` en lecturas; `/save` solo compara `expected` | `document_serialization.py:8-9` (`version`), `:24-32` (`doc_version`); `journal.py:53-56` (`doc_hashes`); `document_entry.py:11-12,24-37` (`hash_c`=`source_hash`, `hash_d`=`content_hash`); `hashing.py:36`; `save_plan.py:49-50,57-58`; `save_routes.py:38-43`. Matiz: `document_routes.py:68-74` (`_flat`) y `docs.py:42-44` no incluyen `version`; sí `graph_payload.py:31` y las respuestas de `docs_routes.py` | **PASS** (matiz menor: no todas las lecturas entregan `version`; `/save` sí compara solo `expected`). |
| Citas corregidas de lote, `append.py:25-26` y `payload_editor.py:31-33` | `save_routes.py:25` (`_ACTION_ORDER`), `:79-87` (`apply_batch`), `:90-91` (`sort_key`), `:94-107` (`apply_change`); `append.py:25-26` (`SLDB_JOURNAL_OFF`); `payload_editor.py:31-33` (llamada a `save_document_payload`) | **PASS**. Citas exactas. |

## 4. Filas hueco/ausente de §2 y §3

§2 tiene 8 filas hueco/ausente; §3 no tiene ninguna. Verifico las 8 y añado 3 de §4 para llegar a 11.

| Fila | Evidencia real leída | Veredicto |
|---|---|---|
| Qué cubre el lock en un guardado (§2.1) | `payload_save.py:47-48`: `write_rendered_document` antes de `save_document_indexes`; `payload_save_steps.py:75` (`write_text`), `:87-96` (`store_lock` + índices) | **PASS**: el lock cubre índices, no el Markdown. |
| Escritura atómica de índices frente al Markdown (§2.1) | `utils.py:40-48` (`mkstemp`, `os.replace`, `fsync`); `payload_save_steps.py:75` y `create_document.py:50` (`write_text` directo) | **PASS**: el `.md` no usa la ruta atómica. |
| CAS/revisión en la API pública de escritura (§2.1) | Firmas `payload_save.py:16`, `create_document.py:22`, `delete_document.py:12`; `docs1.py:31-37` solo añade `--format`; `grep -rnE "expected_(hash|revision|sha)|If-Match|etag" ../sldb/src`: 0 | **PASS**: no hay revisión/hash esperado en la API ni en `docs update`. |
| Lock o motor de base de datos (§2.1) | `grep -rniE "sqlite|sqlalchemy|duckdb" ../sldb/src ../pron/src ../spec2viz/spec2viz`: 0 | **PASS**: estado en YAML/Markdown, sin DB. |
| Escritor externo del Markdown (§2.1) | `payload_save.py:45` (`_old_payload`), `:47` (escritura), `:52-57`; `payload_save_steps.py:74-75`; `provenance_stamp.py:29-32` (lee el previo solo para la firma) | **PASS**: no compara el contenido actual con `hash_c` antes de reescribir. |
| `create_document` sobre archivo existente (§2.1) | `create_document.py:28-29` (documenta sobrescritura), `:50` (escribe), `:51` (registra); `ops.py:33-36` (`_pre_check` → "already tracked") | **PASS**: el archivo ya fue reemplazado cuando salta el error. |
| Lock/CAS propio de archivo en pron (§2.2) | `grep -rnE "fcntl|flock|filelock" ../pron/src`: 0. El CAS de `kernel.py:49-56` es por índice/documento y está cubierto en la primera fila de §2.2 | **PASS**: pron no añade lock de archivo ni de DB. |
| Locks propios de spec2viz (§2.3) | `grep -rnE "fcntl|flock|filelock|threading\.(R)?Lock" ../spec2viz/spec2viz`: 0 | **PASS**: no define locks ni CAS propios. |
| Búsqueda por similitud de corpus (§4) | `corpus_routes.py:18,38-39` (409 `corpus no indexado`); `grep -rn corpus ../sldb/src/sldb/cli/parsers`: 0; `matcher.py:1-2` (difflib de reserva) | **PASS**: sin CLI de corpus; `graph similar` es otra cosa (`graph_analysis.py:57-58`). |
| Consultas guardadas / vistas de búsqueda (§4) | `grep -rniE "saved.?quer|saved_view|consulta guardada"` en `../sldb/src`, `../pron/src`, `../spec2viz/spec2viz`: 0 | **PASS**: ausente; `ViewDoc` es modelo sin evaluador (§5). |
| Búsqueda en spec2viz (§4) | `cli.py:97` y comandos: no hay comando `search`. Matiz: `orchestrator.py:477` genera un input `catalog-search` y `templates/default.html:1171` filtra en cliente, pero no es CLI/HTTP/función pública | **PASS** según la definición de la auditoría; hay búsqueda JS en el HTML generado, no una operación expuesta. |

## Hallazgos menores

- **Cita imprecisa:** `payload_save_steps.py:44-52` no contiene el round-trip; `render_checked` está en `:55-64`. No cambia la conclusión.
- **Citas imprecisas en §1:** `doc.py:55-58`, `:61-69`, `:71-81`; los rangos reales son `:57-60`, `:62-70`, `:73-81`. No cambian la conclusión.
- **Sobreafirmación:** «El journal solo registra `hash_c_before/after`» (`payload_save.py:49`): la línea también registra `hash_d`, `hash_a`, `previous_value` y `new_value`. La conclusión (no se comparan antes de escribir) sigue siendo correcta.
- **Evidencia imprecisa:** «`wait=True` solo en `rebuild_edges.py:34`, `index_commit.py:37`, `document_edges.py:30`»; los dos primeros usan `wait=wait`, no `wait=True`. La conclusión sobre `--wait` en parsers es correcta.
- **Matiz de alcance:** `version = content_hash` lo entrega `serialize_document` (GET `/graph`, respuestas de `/docs`), pero no `GET /document` (`document_routes.py:68-74`) ni `sldb docs show` (`docs.py:42-44`). No afecta a que `/save` solo compare `expected`.

## NO VERIFICADO

- sha256 del entregable, HEADs y líneas de `git status`: datos del Supervisor; no recalculados con estas herramientas.
- Salidas de `--help` de los CLIs y comportamientos de concurrencia real: no ejecutados.

RESULTADO: PASS
