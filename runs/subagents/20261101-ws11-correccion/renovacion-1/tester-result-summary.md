## Separación de fuentes

- **LECTURA PROPIA (verificado abriendo archivos):** todas las filas de la tabla, `desk/drawer/plans/workspace-documental/contratos/navegacion.md`, `borradores/vistas.md`, `patch-final.diff`, `review-source.md`, `review-source-2.md` y el código citado.
- **DATO DEL SUPERVISOR (no verificado por mí):** `tester-facts.log` — HEAD `d61b3cd1`, graph_ui `134a665`, sldb `77bd6d00`, sha256 de `navegacion.md` y `vistas.md`, «Generated … match dag.yaml», `stale: WS09`. No ejecuté nada; no declaro comportamiento en runtime.

## Tabla de verificación

| Sub-punto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| Decisión 1: no reducir WS13.1 a C1-C4; foco interno distinto de navegación | R1 | `navegacion.md:196-210` (6.1), `:214-218` (6.2); `dag.yaml:856-866` | PASS |
| Decisión 2: enlaces entre desks por composición en graph_ui (WS41), no ampliar SLDB | R1 | `navegacion.md:152-156`, `:307`; `SL/links/parser.py:6`; `SL/links/resolver.py:33-35` | PASS |
| Decisión 3: WS18 detenida, opcional, sin nueva pregunta humana | R1 | `navegacion.md:299-303`, `:418` | PASS |
| Decisión 4: aliases = configuración confiable del operador; WS11 input, WS41 consumo, WS40 instancia | R1 | `navegacion.md:91-97` | PASS |
| Punto 1: `local:` antes que aliases, retirado una sola vez, wrapper único, `local:foo:bar` literal | R2 | `navegacion.md:154-157`; `SL/api/stores/doc_ref.py:38-40`; `SL/api/stores/doc_status.py:26-29` | PASS |
| Punto 2: C5b sin afirmar modelo obligatorio ni API lista; `extract_sections`/builder exportados; `model=None` | R2 | `navegacion.md:204`; `SL/api/records/extract.py:6-13`; `SL/api/records/build_ir.py:10-22`; `SL/core/ir/meaning_node.py:9`; `SL/core/ir/document_context.py:6`; `SL/api/__init__.py:14`; `SL/api/records/__init__.py:12,28` | PASS |
| Punto 3: E5 para literal 3c, E-MD1 solo parámetro explícito; no mismo caso en ambos | R2 | `navegacion.md:96`, `:276`, `:311`, `:149-151` (tabla, filas `foo:bar` y `zzz`) | PASS |
| Punto 4: H-11 fuera de las cinco clases, sin modelo/nodo nuevo | R2 | `navegacion.md:369` | PASS |
| Punto 5: citas de Specs junto a la afirmación F18a, sin repetirlas en Evidencia | R2 | `vistas.md:367` (única línea cambiada en vistas, `patch-final.diff`) | PASS |
| A: C1-C3 solo navegación (cambian `selectedId`), no foco | A | `navegacion.md:197-199`; `workspace-view.js:222-226`, `:260-264`, `:419`; `workspace_routes.py:118` | PASS |
| A: C4 tarjeta pasiva, `CodeFileView` sin callback | A | `navegacion.md:200`; `workspace-view.js:15`, `:455` | PASS |
| A: dominio futuro (sección+span, `field_path`, referencia documento/campo/posición/valor, arista schema) | A | `navegacion.md:204-209` | PASS |
| A: H-03 preservar campo/posición antes de concatenar | A | `navegacion.md:201`, `:362`; `workspace_routes.py:441-451` | PASS |
| A: archivo externo no atribuido a nodo del grafo | A | `navegacion.md:211` (C11b), `:209` | PASS |
| A: C6 `owning_section` opcional (`str\|None`, `get`) y mapa `{}` si no corresponde | A | `navegacion.md:205`; `SL/core/ir/meaning_node.py:12-14`; `SL/api/records/build_ir.py:75`; `SL/api/records/map_fields.py:22-26`, `:43-56` | PASS |
| A: C7 sin span por campo, con `SourceSpan` por defecto; no bloquea C6 | A | `navegacion.md:206`; `SL/core/ir/meaning_node.py:15`; `SL/api/records/build_ir.py:68-78`; `document-ir.mjs:18-22` | PASS |
| A: C8/C9 con deduplicación `(source,target,type,relation_doc)` y multiplicidad | A | `navegacion.md:207-208`; `workspace_routes.py:384`; `SL/store/edge_index/declared_references.py:64-71`; `composition_edges.py:55` | PASS |
| A: C5b ausencia de ruta graph_ui + reutilización por verificar | A | `navegacion.md:204`; `workspace_routes.py:151-165`; `sldb_adapter.py:178-215` | PASS |
| A: C11a futuro comprometido / C11b sin compromiso; C12 no soportado | A | `navegacion.md:211-212`; `dag.yaml:856-866` | PASS |
| A: C14 separa rango local de Code y traslado al Markdown; `:N` ±5 es contexto | A | `navegacion.md:214`; `workspace_routes.py:565-571`; `workspace.mjs:31-61`; `workspace-view.js:17`; `vistas.md:345,349,351` | PASS |
| A: H-05b tres capacidades distintas | A | `navegacion.md:366` | PASS |
| A: «mismo origen» = misma lectura/revisión; hoy no se cumple (IR :156 y hash :196) | A | `navegacion.md:132-133`; `workspace_routes.py:156`, `:196`; `sldb_adapter.py:202-203` | PASS |
| A: reserva `surface.text` no prueba fuente íntegra | A | `navegacion.md:130`; `SL/api/records/utils.py:10-19`; `SL/core/ir/document_ir.py:12` | PASS |
| A: `RitualDoc.steps` ordenada sin StepDoc ni progreso | A | `navegacion.md:375`; `deskops/models/ritual.py:65-68`, `:77-79`; `deskops/models/step.py:31-38`; búsqueda `progress/done/status/complete/checked` en ambos: solo `ritual.py:78` | PASS |
| B: guardias generales separadas de las de TaskDoc (`desk/tasks`, `.md`, no `Board.md`) | B | `navegacion.md:104`, `:115`; `deskops_routes.py:36-40` (condición `:39`) | PASS |
| B: `recovery.py` lee destino con ancla antes de retornar y recursa | B | `navegacion.md:124`, `:152`; `SL/links/recovery.py:13-14`, `:29-31` | PASS |
| B: orden autorizar root antes de leer/publicar | B | `navegacion.md:154-157` (pasos 4-8) | PASS |
| B: composición `parse_links` + `split_anchor` + `doc_status` | B | `navegacion.md:153-154`; `SL/links/parser.py:17-20`; `SL/links/sections.py:15-18`; `SL/api/stores/doc_status.py:18` | PASS |
| B: distinción `alias:Model/name`/`alias:ruta` frente a `Model:name` de GUI | B | `navegacion.md:151-152`, `:156`; `SL/api/stores/doc_ref.py:43-45` | PASS |
| B: contención del `path` del resultado antes de abrir | B | `navegacion.md:156`; `SL/api/stores/doc_ref_status.py:16` | PASS |
| B: `include_linked=False` y sin federación automática | B | `navegacion.md:157`, `:305`; `SL/api/edges/edge_reading.py:14`; `workspace_routes.py:288`, `:584` | PASS |
| B: no modelados sin modelo falso | B | `navegacion.md:157` | PASS |
| B/ejemplo `[[TaskDoc/x]]` → `doc_status(A,"local:TaskDoc/x")` busca solo A | B | `doc_ref.py:38-40`; `doc_status.py:29` | PASS |
| B/ejemplo `[[local:TaskDoc/x]]` → igual, nunca `local:local:…` | B | `navegacion.md:150`; `doc_ref.py:38-39` | PASS |
| B/ejemplo `[[local:TaskDoc/x]]` en doc de B → busca en B | B | `navegacion.md:150-151` | PASS |
| B/ejemplo `[[local:foo:bar]]` → literal `foo:bar`, no salta al enlace `foo` | B | `doc_ref.py:38-40`; `doc_status.py:26-29` | PASS |
| B/ejemplo `[[foo:bar]]` → nombre local, E5, ni E-MD1 ni salto | B | `navegacion.md:149-151`; `doc_ref.py:40` | PASS |
| B/ejemplo `[[b:TaskDoc/x]]` → desk B autorizado | B | `navegacion.md:151` | PASS |
| B/ejemplo `[[b:local:x]]` → `local:local:x`, resto no reinterpretado | B | `navegacion.md:152`; `doc_ref.py:38-39` | PASS |
| B/ejemplo `[[b:TaskDoc/x]]` sin configuración → literal en A, E5 | B | `navegacion.md:96`, `:152` | PASS |
| B/ejemplo parámetro explícito `zzz` → E-MD1 sin abrir nada | B | `navegacion.md:153`, `:311` | PASS |
| B: `local:foo:bar` no salta a enlace | B | `doc_status.py:25-29`; `doc_ref.py:38-40` | PASS |
| B: ningún camino del texto a store no autorizado | B | `doc_status.py:29` usa `_lookup` sobre el store abierto, sin `find_link`; wrapper `local:` fuerza `split_doc_ref` a `(None, resto)` en `doc_ref.py:38-39` | PASS |
| C: `doc_status.py:25` y `edge_reading.py:28` abren con `mode="readonly"` | C | `SL/api/stores/doc_status.py:25`; `SL/api/edges/edge_reading.py:28` | PASS |
| C: `open_store.py:38` migra layout fuera del caso canónico | C | `SL/api/stores/open_store.py:37-38`; `SL/store/migration.py:72-80` (`:75-76`) | PASS |
| C: retirado «doc_status no escribe»; 8.3 explica alcance de la docstring | C | `navegacion.md:184-186`, `:303` (búsqueda «no escribe»: solo citas de `rebuild_edges`/obligación) | PASS |
| C: obligación (a)(b)(c) y criterio observable «el store no cambió» | C | `navegacion.md:187` | PASS |
| C: store propio WS13.1/ruta WS24; segundo desk WS41 | C | `navegacion.md:187`, `:371` | PASS |
| D: `shell/api.js:5-11` descarta `response.status`; `json()` antes; E2 debe mostrarlo | D | `navegacion.md:263-265`, `:275`; `shell/api.js:5-11` (fetch :5, json :6, `response.ok` :7, error :8-10) | PASS |
| D: E7 = causa recibida; 422 de `sldb_adapter` no identifica modelo no importable | D | `navegacion.md:277-279`; `sldb_adapter.py:201-205` (`except Exception`, 422 `:205`); `workspace_routes.py:162-164`, `:309-310` | PASS |
| D: ningún discriminante inventado | D | `navegacion.md:279` | PASS |
| E: authored ≠ modelado; SpecDoc/SpecNodeDoc y manifiesto WS40 derivados | E | `navegacion.md:340-349` (regla 5), `:345-346` | PASS |
| F: `vistas.md:367` cita `notation-view.js:356` y `registry.js:16`, sin aceptación | F | `vistas.md:367`; `notation-view.js:356`; `shell/registry.js:16` | PASS |
| F: solo esa celda cambió en vistas | F | `patch-final.diff` (un `-`/`+` en vistas, hunk `@@ -364,7 +364,7 @@`) | PASS |
| Clave de sesión con alias + identidad local, sin colisión | — | `navegacion.md:168-169` | PASS |
| H-11 sin clase nueva ni modelo/nodo/productor de documento | — | `navegacion.md:369` | PASS |
| Estado borrador, sección 12 «sin acta registrada», sin actas inventadas | — | `navegacion.md:3`, `:395-408`, `:418`; búsqueda «sin acta registrada» = 14 filas + G_SPEC_VIEW | PASS |
| Contradicción: resto de «doc_status no escribe» | — | Sin coincidencias relevantes; `navegacion.md:303` corrige alcance | PASS |
| Contradicción: `recover_links` usado como resolutor | — | `navegacion.md:152`, `:210`, `:364` lo excluyen explícitamente | PASS |
| Contradicción: «soportado» para C1-C4 | — | `navegacion.md:197-200` usan «Navegación»/«Tarjeta derivada pasiva» | PASS |
| Contradicción: H-16 con dueño sldb | — | `navegacion.md:372` dueño graph_ui | PASS |
| Contradicción: alias de sldb como autorización | — | `navegacion.md:83` («un alias de sldb no es una autorización»), `:95`, `:307` | PASS |

## Observaciones (no bloqueantes para los puntos pedidos)

- **E4/E7:** `navegacion.md:272` y `:277` usan ambos `is_degraded`/`projections.document.ok=false` como reconocimiento; es un solapamiento de reconocimiento entre dos estados que la tabla dice distinguir. No es el caso E5/E-MD1 que el encargo prohíbe.
- **Precisión de rangos:** algunos rangos citan la línea vecina (p. ej. guardia de identificador `workspace_routes.py:134-135` frente a condición real en `:133`); el hecho citado es correcto en la línea contigua incluida en el bloque.

## Qué no pude verificar

- Los hashes/commits y el `stale: WS09` del supervisor (solo leí el árbol actual, no `git show`).
- Comportamiento en ejecución: no ejecuté rutas, UI, ni `doc_status`/`open_store`; solo leí código.
- Afirmaciones de aceptación/revisión y «no hay actas» fuera de la búsqueda declarada en el contrato.
- Contenido histórico de `dag.yaml` y auditorías más allá de las líneas abiertas.

RESULTADO: PASS
