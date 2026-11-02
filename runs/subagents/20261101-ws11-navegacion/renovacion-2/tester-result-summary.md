## LECTURA PROPIA (no ejecuté nada)

### 1. Alcance del diff
Solo dos hunks: §2.2 (línea 53) y §4 (línea 120). **PASS**

### 2. Citas nuevas del diff

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| `read_bytes` para hash de revisión | Propia | `GU/workspace_routes.py:196` (`hashlib.sha256(file_path.read_bytes())`) | PASS |
| `read_text` del respaldo solo para frontmatter | Propia | `GU/workspace_routes.py:326-336` (lee, parte por `---`, `yaml.safe_load(parts[1])`, compara `id`; no devuelve el texto) | PASS |
| «dos puntos internos» en graph_ui | Propia | grep `read_text|read_bytes|open(` en el archivo: solo `:196`, `:326`, `:539` (`:539` es Code referenciado, no archivo propio) | PASS con salvedad |
| Enumeración de lecturas en `SL/cli/serve/` | Propia | solo `document_routes.py:62` y `sections_routes.py:46`; ninguna `read_bytes` | PASS |
| Enumeración de lecturas en `SL/api/documents/` | Propia | faltan `api/documents/track_document_file.py:47,48,68` y `api/documents/provenance_stamp.py:31` | **FAIL** |
| ¿Alguna devuelve el texto crudo? | Propia | las 4 omitidas devuelven validación `stamped`/roundtrip, no texto; `document_ast.py:22`→IR; `payload_save.py:54`→payload | PASS |

### 3. Negaciones absolutas del contrato (12 cotejadas)

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| §2.2 «ninguna ruta entrega el texto» + dos lecturas internas | Propia | `GU/workspace_routes.py:196`, `:326-336` | PASS |
| §2.4 «no aparece `anchors`» | Propia | grep `anchors` en `workspace_routes.py`: 0 coincidencias | PASS |
| §3.1 «un solo store por proceso» | Propia | `workspace_routes.py:68-71`, `:612-617`; `serve.py:506-515` | PASS |
| §3.1 «workspace no existe en remote: 501» | Propia | `serve.py:320-322` | PASS |
| §3.3 «extensiones desconocidas se leen como `text` (:553)» | Propia | `workspace_routes.py:553` (`TEXT_EXTENSIONS.get(suffix, 'text')`) | PASS |
| §3.3 «`check-ignore` no existe fuera de repo git» | Propia | `workspace_routes.py:460-464` (sin `.git` → `False, ""`) | PASS |
| §4 enumeración de lecturas sldb | Propia | faltan `track_document_file.py:47,48,68`, `provenance_stamp.py:31` | **FAIL** |
| §4 «no hay operación pública que devuelva bytes» | Propia | revisados `cli/serve` (2 lecturas, ninguna raw) y `api/documents` (todas derivadas) | PASS |
| §6 «no hay estado de foco; único `selectedId`» | Propia | grep `focus` en `workspace_routes.py` y `views/workspace/`: 0; `workspace-view.js:57` | PASS |
| §7.3 «sin forma normalizada de sin-respuesta» | Propia | `shell/api.js:4-13` (timeout 60000, `error.body`) | PASS |
| §7.4 «importmap esm.sh; sin `onerror`» | Propia | `index.html:7-8`; grep `onerror|onError` en `GU/`: 0 | PASS |
| §8.3 «`doc_status` no escribe; enlace solo directo» | Propia | `doc_status.py:1-5`; `doc_ref.py:1-8` | PASS |
| §9 «vistas solo en local: 501» | Propia | `serve.py:147-150` | PASS |

### 4. Citas de §7-§10 no abiertas antes

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| §7.1 códigos 200/405/400/404/500/503 | Propia | `workspace_routes.py:92`, `:94`, `:74-75`, `:84-91`, `:96`, `:99-100`, `:104-105`, `:108-109` | PASS |
| §8.3 referencias `alias:ref` | Propia | `doc_ref.py:28-40` (`split_doc_ref`, `find_link`) | PASS |
| §9 rutas `/api/views*` | Propia | `views_routes.py:69-86` (`dispatch`) | PASS |
| §9 `save_view` escribe bajo `store.parent/sldb/views`, sin `expected` | Propia | `views_routes.py:56-66` | PASS |
| §9 `evaluate_view` / `list_views` | Propia | `projection_views.py:107`, `:127`, `:41-62` | PASS con salvedad: `:107-124` desborda 1-2 líneas |
| §5.1/§7.5 «Actualizar → `loadNode`; catálogo solo al montar» | Propia | `workspace-view.js:296`, `:196` | PASS |

## DATO DEL SUPERVISOR (no verificado por mí)
- `tester-v2-facts.log`: HEAD deskops `76155db9`; graph_ui `134a665`; sldb `77bd6d00`; sha256 `2375d695…`; 4 checks exit 0. No los ejecuté.

## No pude verificar
- Commits y árbol limpio: sin acceso a git.
- Dos lecturas del archivo del documento en `api/documents` fuera de la lista (§4): `track_document_file.py:47,48,68`, `provenance_stamp.py:31`; ambas internas y derivadas, no raw.

RESULTADO: FAIL
