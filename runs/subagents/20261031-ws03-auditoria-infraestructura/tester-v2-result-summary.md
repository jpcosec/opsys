# Informe del Tester — segunda ronda (WS03)

Entregable: `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, sha256 `8b3fed6a…13bc1` (dato del Supervisor; no puedo recalcularlo). No leí kimun.

## 1. Hallazgos de la ronda 1 (A, B, C)

| Objeto | Evidencia real leída | Veredicto |
|---|---|---|
| A — `docs update --help` muestra `--format` | `../sldb/src/sldb/cli/parsers/docs1.py:37` (`add_format(u)`), tras `_update` en `:31-36`; `--help` con `--format {text,json,yaml}` en `tester-v2-facts.log` (dato del Supervisor) | **PASS**. El entregable ya cita `:37`; la ronda 1 acertó el síntoma pero se quedó en `:32-36`. |
| B — ausencia de CLI de corpus | `grep -rn corpus ../sldb/src/sldb/cli/parsers`: 0 coincidencias; `corpus_routes.py:18,39` | **PASS**. Corregido: ahora separa «0 coincidencias» de «existe `graph similar`». |
| C — lock y refresco de `pron serve` | `../pron/src/pron/serve.py:55` (`self.lock = threading.Lock()`), `:101-119` (`handle`, `with self.lock`, `_settle`), `:121-130` (`_settle`) | **PASS**. Las citas nuevas son exactas; C queda resuelto. |
| Fila ViewDoc con `notation_view.py:238-239` | `../spec2viz/spec2viz/notation_view.py:238-239`: «Sirve, por ejemplo, para evaluar una `ViewDoc`…»; `resolve_documents` en `:228`; `ViewDoc` en `sldb_models.py:348`, `__all__` en `:433`; `grep ViewDoc` en sldb y pron: 0 | **PASS**. |

## 2. Muestreo nuevo (concurrencia y búsquedas)

| Fila | Evidencia real leída | Veredicto |
|---|---|---|
| Lock del journal | `store/journal/lock.py:14-24` (`lockf LOCK_EX`); `journal/append.py:24-25` (`SLDB_JOURNAL_OFF`), `:38-42` (`max(seq)+1`) | **PASS** (menor: la cita `:25` cae en `return None`, no en la comprobación). |
| Guardado parcial en lote | `save_routes.py:25` (`_ACTION_ORDER`), `:74-82` (`apply_batch`, 500 con `completed`), `:77` (`sorted`) | **PASS** (menor: cita `:79-87` y `:90-91` imprecisas; el contenido es correcto). |
| Antes-de-imagen en `selfdoc` | `cli/selfdoc_write.py:20` (llamada), `:41-43` (`current != plan.previous` → `ValueError`), escritura en `:56`/`:59` | **PASS** (menor: `:61` no es la escritura). |
| Borrado | `api/documents/delete_document.py:35` (`unlink`); `untrack_document.py:65` (`with store_lock, rollback_on_error`) | **PASS** |
| Escritura atómica de índices | `store/io/utils.py:40-48` (`_atomic_write`, `mkstemp`, `os.replace`); frente a `payload_save_steps.py:75` (`write_text`) | **PASS** |
| Escritura a disco en pron | `pron/world/storage/payload_editor.py:30-32` (`save_document_payload`) | **PASS** (menor: la llamada empieza en `:30`, no `:31`). |
| Deshacer en pron | `move_undo.py:38` (`expected_hash.pop`), `:54-82` (`_checked`/`_changed_since`: compara `hash_c` actual con el dejado y omite la escritura); `write.py:41-48` | **FAIL**: la fila afirma «No comprueba que el campo siga como lo dejó la jugada», pero `_changed_since` sí lo comprueba a nivel de documento y no toca el que cambió. |
| Locks propios de spec2viz | `grep -rE "fcntl|flock|filelock|threading\.(R)?Lock" ../spec2viz/spec2viz`: 0 | **PASS** |
| Detección de cambio del spec | `sldb_sync.py:649` (`sha256`), `catalog_views.py:29-40` (compara `sha256`), `:43-55` (store temporal) | **PASS** |
| Búsqueda por término | `api/search.py:26` (`def search`), `query_engine/where_parse.py:30` (`compile_where`) | **PASS** |
| Consulta de grafo | `api/graph/execute.py:13` (`execute_query`), `relation_filter.py:10` (`RelationFilter`) | **PASS** |
| Corpus | `api/corpus/corpus.py:24,47,58,67` (`Corpus`, `index_path`, `refresh_if_stale`, `rank`); `matcher.py:1-2` (difflib sin embedder); `corpus_routes.py:18,39` (409) | **PASS** |
| Campos, secciones y explore | `commands/fields.py:11,16` (`query_field`); `commands/sections_find.py:8-24`; `commands/explore.py:18-21` | **PASS** |
| Consultas guardadas ausentes | `grep -rniE "saved.?quer|saved_view|consulta guardada"` en los tres repos: 0 | **PASS** |

## 3. Hallazgos

- **FAIL (contenido):** la fila «Deshacer» de §2.2 dice que no se comprueba que el documento siga como lo dejó la jugada; `move_undo.py:54-82` hace exactamente esa comprobación comparando `hash_c` y omitiendo la escritura. Contradice su fuente.
- **Menores (no cambian conclusión):** citas imprecisas en lote (`save_routes.py`), journal (`append.py:25`), selfdoc (`:61`) y `payload_editor.py:31`; ninguna altera lo afirmado.
- A, B y C quedan resueltos; la fila ViewDoc con `notation_view.py:238-239` es correcta.
- HEADs y líneas de `git status` 4/0/0: dato del Supervisor (`tester-v2-facts.log`), no verificado por mí.

RESULTADO: FAIL
