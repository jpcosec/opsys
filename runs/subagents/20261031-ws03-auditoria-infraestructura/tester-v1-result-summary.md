# Informe del Tester — WS03

Entregable: `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`. Contraste directo contra `../sldb`, `../pron`, `../spec2viz` (solo lectura). No leí kimun. Los HEAD del encabezado coinciden con `tester-facts.log` («dato del Supervisor»).

| # | Fila / afirmación | Evidencia leída | Veredicto |
|---|---|---|---|
| 1 | S1 Fuente sldb: `create_document` escribe el .md y `track` registra | `create_document.py:50` (`doc_path.write_text(...)`), `:51` (`_track_and_record`); `ops.py:25-29` (`track` → `_pre_check` → `with store_lock`) | PASS |
| 2 | S1 Fuente en bruto ausente | grep `raw.?source\|raw_source` en `../sldb/src/sldb/api`: 0 resultados; firmas toman `payload: dict` (`payload_save.py:16`, `create_document.py:22`) | PASS |
| 3 | S1 Cache: clave con `hash_c` y mtime/tamaño salvo `SLDB_TRUST_CHAIN` | `runtime_cache_signature.py:35-36` (`trust_chain`), `:73-76` (rama `hash_c` sola vs `hash_c,mtime,size`) | PASS |
| 4 | S1 pron: payload vía sldb, `update_field` read-modify-write | `payload_editor.py:12` (import `save_document_payload`), `:31`, `:39-49` (`update_field` → `replace`) | PASS |
| 5 | S1 spec2viz: spec YAML y `sha256` en `SpecDoc` | `sldb_sync.py:575` (`def sync`), `:644-649` (`spec_payload`, `"sha256": hashlib...`), `:390,393` (escrituras por `sldb.api`) | PASS |
| 6 | S2.1 lock de store: `fcntl.lockf`, `LOCK_NB`, error «busy… --wait» | `lock.py:32` (`acquire(wait=False)`), `:46` (`flags \|= fcntl.LOCK_NB`), `:48`, `:51` (mensaje); ruta `layout.py:46-47` (`locks/store.lock`) | PASS |
| 7 | S2.1 `--wait` solo en parser `stores` y oculto; `docs update` no lo expone | `parsers/stores.py:38`; `parsers/hidden.py:34`; `parsers/docs1.py:32-36` (`update`: doc, payload, `--store`, `--pythonpath`) | PASS |
| 8 | S2.1 el lock cubre solo índices; el .md se escribe antes y fuera | `payload_save.py:47` (`write_rendered_document`) antes de `:48` (`save_document_indexes` → `payload_save_steps.py:87 with store_lock`); `payload_save_steps.py:75 write_text`, `:81` def, `:87` lock | PASS |
| 9 | S2.1 `SAVE_LOCK` es `threading.RLock` de proceso | `save_routes.py:23` (`SAVE_LOCK = threading.RLock()`), `:28-32` (`with SAVE_LOCK`) | PASS |
| 10 | S2.1 HTTP compara payload completo con `expected`; 409 | `save_plan.py:50` (`existing.payload != change.get("expected")`), `:58` (delete), `:33,45` (409 create); lote `save_routes.py:38-43`, tope `:24` | PASS |
| 11 | S2.1 forma legacy sin `expected` | `save_single.py:13-20` (`doc`+`payload`, sin revisión); rama por ausencia de `changes` en `save_routes.py:30-32` | PASS |
| 12 | S2.1 escritor externo se pierde: no compara archivo con índice | `payload_save_steps.py:75`; `provenance_stamp.py:31` (solo lee previo para firma); `payload_save.py:52-57` (`_old_payload` para journal) | PASS |
| 13 | S2.1 `create_document` sobre archivo registrado: escribe y luego falla | `create_document.py:50` (`write_text`) precede a `:51`; `ops.py:34-36` (`_pre_check` → «already tracked») | PASS |
| 14 | S2.1 CAS/revisión ausente en API y CLI | `payload_save.py:16` (sin `expected`); `docs1.py:32-36` (sin flag de revisión); grep `expected_hash\|expected_revision\|expected_sha\|If-Match\|etag\|ETag` en `../sldb/src`: 0 resultados | PASS (con hallazgo A) |
| 15 | S2.2 pron: guarda por `hash_c` del índice antes de escribir | `kernel.py:49-50` (`expect` guarda `store.hash_c`), `:52-56` (compara y lanza); `document_reader.py:73-75` (`hash_c` desde entrada de índice), `:81-87` (`_indexed` lee `load_documents_index`) | PASS |
| 16 | S2.2 lock del daemon `pron serve` y refresco dentro del lock | `serve.py:55` (`self.lock = threading.Lock()`), `:106-119` (`handle` con `with self.lock`, `_settle`), `:121-130` (`_settle`). **Las líneas citadas `:72` y `:62-80` pertenecen a `_entries` y no tratan del lock ni del refresco** | **FAIL** |
| 17 | S2.2 pron sin `fcntl`/`flock`/`filelock` | grep en `../pron/src`: 0 resultados | PASS |
| 18 | S2.3 servidor de anotaciones: `TCPServer` de un hilo, `write_text` sin lock | `cli.py:581` (`SimpleHTTPRequestHandler`), `:608-615` (`do_POST`, `out_path.write_text`), `:626` (`socketserver.TCPServer`) | PASS |
| 19 | S3 enlaces `[[doc]]`, `[[doc#Sección]]` y `[pred:: [[doc]]]` | `links/parser.py:6` (`LINK_PATTERN`), `:7` (`INLINE_PREDICATE_LINK_PATTERN`); transclusión `links/composer.py:23-25` | PASS |
| 20 | S4 corpus: sin CLI y 409 si no hay índice | `corpus_routes.py:18` (`NOT_INDEXED`), `:38-39` (409); grep `corpus` en `cli/parsers`: 0 resultados | PASS (con hallazgo B) |
| 21 | S5 renderers: 9 y defaults | `renderers/__init__.py:22-31` (plantuml, vega, mermaid, d2, antonia-html, tree, graph, bpmn, json), `:46-54` (defaults: componente→graph, matriz→vega, `EnforcementArtifact`→json) | PASS |
| 22 | S5.2 ViewDoc: clase en spec2viz; ausente en sldb y pron; sin evaluador | `sldb_models.py:348` (`class ViewDoc`), `:362` (`__references__`), `:433` (`__all__`); grep `ViewDoc` en `../sldb` y `../pron`: 0; en `../spec2viz/spec2viz` solo `sldb_models.py:348,380,433`, `notation_view.py:238` (comentario), `sldb_sync.py:39`; sin documentos ViewDoc en `../spec2viz/.sldb` | PASS |
| 23 | Encabezado: HEADs de los tres repos | `tester-facts.log` (dato del Supervisor); coinciden los tres hashes | PASS (dato del Supervisor) |
| 24 | Encabezado: líneas de `git status --short` 4/0/0, sin cambios | No hay salida en `tester-facts.log`; sin bash no puedo ejecutarlo | NO VERIFICADO |

## Hallazgos

- **A (menor, misma fila 14):** la evidencia dice que `sldb docs update --help` muestra `--format`; `docs1.py:32-36` no define `--format` para `update`. La conclusión (sin revisión) sigue siendo correcta.
- **B (menor, fila 20):** el texto afirma que `grep -n "corpus"` «solo aparece `graph similar`»; el grep en `cli/parsers` no devuelve ninguna coincidencia con «corpus». La ausencia de CLI de corpus se sostiene.
- **C (fail):** fila 16 cita `serve.py:72` y `:62-80` como lock y refresco; esas líneas son `_entries`. La afirmación mecanismo es correcta, pero la evidencia citada no la respalda.
- Comportamientos de concurrencia no ejecutados: el entregable los marca «por lectura» y lista la causa en §7; no cuentan como comprobación ejecutada.
- Secciones 1–5 cubren todas las capacidades exigidas; no falta ninguna fila obligatoria.

RESULTADO: FAIL
