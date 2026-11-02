## Separación de fuentes

- **LECTURA PROPIA:** abrí completos `contratos/navegacion.md`, `review-source.md`, `review-source-2.md`, `patch-final.diff`, `patch-3.diff`, `renovacion-1/tester-result-summary.md`, `vistas.md` (F18a y contexto), y el código citado en cada fila. No ejecuté nada; no declaro comportamiento en runtime.
- **DATO DEL SUPERVISOR (no verificado):** `tester-v2-facts.log`: HEAD deskops `0fd6118e`, graph_ui `134a665`, sldb `77bd6d00`, sha256 de `navegacion.md` y `vistas.md`, «Generated … match dag.yaml», `stale: WS09`.

## Tabla de verificación

| Sub-punto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| Decisión 1: no reducir WS13.1 a C1-C4; foco interno distinto de navegación | R1 | `navegacion.md:196-231`; `dag.yaml:857-859`, `:865-867` | PASS |
| Decisión 2: enlaces entre desks por composición graph_ui/WS41; no ampliar sldb | R1 | `navegacion.md:152-157`, `:307`, `:372`; `parser.py:6`; `resolver.py:33-35` | PASS |
| Decisión 3: WS18 detenida, opcional, sin nueva pregunta humana | R1 | `navegacion.md:299-303`, `:418` | PASS |
| Decisión 4: aliases = configuración confiable del operador; WS11 input/WS41 consumo/WS40 instancia | R1 | `navegacion.md:91-97` | PASS |
| Punto 1: `local:` antes que aliases, retirado una vez, wrapper único, `local:foo:bar` literal | R2 | `navegacion.md:153-157`; `doc_ref.py:38-40`; `doc_status.py:25-29` | PASS |
| Punto 2: C5b sin modelo obligatorio ni API lista; `extract_sections`/builder exportados; `model=None` | R2 | `navegacion.md:205`; `extract.py:6-13`; `build_ir.py:10-22`; `meaning_node.py:9`; `document_context.py:6`; `api/__init__.py:14`; `records/__init__.py:12,28` | PASS |
| Punto 3: E5 solo para literal 3c; E-MD1 solo parámetro explícito; no mismo caso | R2 | `navegacion.md:94`, `:316`; `doc_ref.py:40` | PASS |
| Punto 4: H-11 fuera de las cinco clases; sin modelo/nodo nuevo | R2 | `navegacion.md:369` | PASS |
| Punto 5: citas Specs junto a F18a, no repetidas en Evidencia | R2 | `vistas.md:367`, `:375`; `patch-final.diff` | PASS |
| A: C1-C3 solo navegación, cambian `selectedId` | A | `navegacion.md:199-201`; `workspace-view.js:222-226`, `:260-264`, `:419`; `workspace_routes.py:118` | PASS |
| A: C4 tarjeta pasiva, `CodeFileView` sin callback | A | `navegacion.md:202`; `workspace-view.js:15`, `:455` | PASS |
| A: dominio futuro (sección+span, `field_path`, referencia documento/campo/posición/valor, arista schema) | A | `navegacion.md:204-209` | PASS |
| A: H-03 preservar campo/posición antes de concatenar | A | `navegacion.md:203`, `:362`; `workspace_routes.py:441-451` | PASS |
| A: archivo externo no atribuido a nodo del grafo | A | `navegacion.md:211` (C11b) | PASS |
| A: C6 `owning_section` opcional y mapa `{}` si no corresponde | A | `navegacion.md:205`; `meaning_node.py:12-14`; `build_ir.py:75`; `map_fields.py:22-26`, `:43-56` | PASS |
| A: C7 sin span por campo, `SourceSpan` por defecto, no bloquea C6 | A | `navegacion.md:206`; `meaning_node.py:15`; `build_ir.py:68-78`; `document-ir.mjs:18-22` | PASS |
| A: C8/C9 con deduplicación `(source,target,type,relation_doc)` y multiplicidad | A | `navegacion.md:207-209`; `workspace_routes.py:384`; `declared_references.py:64-71`; `composition_edges.py:55` | PASS |
| A: C5b ausencia de ruta graph_ui + reutilización por verificar | A | `navegacion.md:205`; `workspace_routes.py:151-165`; `sldb_adapter.py:178-215` | PASS |
| A: C11a comprometido / C11b sin compromiso; C12 declarado | A | `navegacion.md:211-212`; `dag.yaml:857-859` | PASS |
| A: C14 separa rango local de Code y traslado al Markdown; `:N±5` es contexto | A | `navegacion.md:214`; `workspace_routes.py:565-571`; `workspace.mjs:31-61`; `workspace-view.js:17`; `vistas.md:345-351` | PASS |
| A: H-05b tres capacidades distintas | A | `navegacion.md:363` | PASS |
| A: «mismo origen» = misma lectura/revisión; hoy no se cumple (IR :156, hash :196) | A | `navegacion.md:132-133`; `workspace_routes.py:156`, `:196`; `sldb_adapter.py:202-203` | PASS |
| A: reserva `surface.text` no prueba fuente íntegra | A | `navegacion.md:133`; `utils.py:10-19`; `document_ir.py:8-14` | PASS |
| A: `RitualDoc.steps` ordenada sin StepDoc ni progreso | A | `navegacion.md:375`; `ritual.py:65-68`, `:77-79`; `step.py:31-38` | PASS |
| B: guardias generales separadas de TaskDoc (`desk/tasks`, `.md`, no `Board.md`) | B | `navegacion.md:104`, `:115`; `deskops_routes.py:36-40` (condición `:39`); `operations.py:1196-1210` | PASS |
| B: `recovery.py` lee destino con ancla antes de retornar y recursa | B | `navegacion.md:124`, `:152`; `recovery.py:13-14`, `:29-30` | PASS |
| B: orden autorizar root antes de leer | B | `navegacion.md:154-157` (pasos 4-8) | PASS |
| B: composición `parse_links` + `split_anchor` + `doc_status` | B | `navegacion.md:153`; `parser.py:17-20`; `sections.py:15-18`; `doc_status.py:18` | PASS |
| B: distinción `alias:Model/name`, `alias:ruta` frente a `Model:name` de GUI | B | `navegacion.md:151-152`; `doc_ref.py:43-45` | PASS |
| B: contención del `path` del resultado antes de abrir | B | `navegacion.md:156`; `doc_ref_status.py:16` | PASS |
| B: `include_linked=False` y sin federación automática | B | `navegacion.md:157`, `:305`; `edge_reading.py:14`; `workspace_routes.py:288`, `:584` | PASS |
| B: no modelados sin modelo falso | B | `navegacion.md:157` | PASS |
| B/ejemplo `[[TaskDoc/x]]` → `local:TaskDoc/x`, solo A | B | `doc_ref.py:38-40`; `doc_status.py:26-29` | PASS |
| B/ejemplo `[[local:TaskDoc/x]]` → igual; nunca `local:local:` | B | `navegacion.md:150`; `doc_ref.py:38-39` | PASS |
| B/ejemplo `[[local:TaskDoc/x]]` en doc de B → busca en B | B | `navegacion.md:150-151` | PASS |
| B/ejemplo `[[local:foo:bar]]` → literal `foo:bar`, no salta al enlace `foo` | B | `doc_ref.py:38-40`; `doc_status.py:26-29` | PASS |
| B/ejemplo `[[foo:bar]]` → nombre local, E5, ni E-MD1 ni salto | B | `navegacion.md:149-151`; `doc_ref.py:40` | PASS |
| B/ejemplo `[[b:TaskDoc/x]]` → desk B autorizado | B | `navegacion.md:151`; `doc_status.py:26-29` | PASS |
| B/ejemplo `[[b:local:x]]` → `local:local:x`, resto no reinterpretado | B | `navegacion.md:152`; `doc_ref.py:38-39` | PASS |
| B/ejemplo `[[b:TaskDoc/x]]` sin configuración → literal en A, E5 | B | `navegacion.md:96`, `:152`; `doc_ref.py:40` | PASS |
| B/ejemplo parámetro explícito `zzz` → E-MD1 sin abrir nada | B | `navegacion.md:153`, `:311` | PASS |
| B: `local:foo:bar` no salta a enlace de store | B | `doc_ref.py:38-40`; `doc_status.py:26-29` | PASS |
| B: ningún camino del texto a store no autorizado | B | wrapper `local:` fuerza `split_doc_ref`→`(None,resto)` (`doc_ref.py:38-39`); `_lookup` solo usa `indexed_documents(store_path)` (`doc_status.py:46-52`; `indexed_documents.py:18-22`) | PASS |
| C: `doc_status.py:25` y `edge_reading.py:28` abren con `mode="readonly"` | C | `doc_status.py:25`; `edge_reading.py:28` | PASS |
| C: `open_store.py:38` migra layout fuera del caso canónico | C | `open_store.py:37-41`; `migration.py:72-76` | PASS |
| C: retirado «doc_status no escribe»; 8.3 explica alcance de la docstring | C | `navegacion.md:185`, `:302`; búsqueda sin resto contradictorio | PASS |
| C: obligación (a)(b)(c) y criterio observable «el store no cambió» | C | `navegacion.md:187` | PASS |
| C: store propio WS13.1/ruta WS24; segundo desk WS41 | C | `navegacion.md:187`, `:371` | PASS |
| D: `shell/api.js:5-11` descarta `response.status`; `json()` antes | D | `shell/api.js:5-11` | PASS |
| D: E2 debe mostrar el código; delta WS15.1 | D | `navegacion.md:265`, `:275`, `:367` | PASS |
| D: E7 = causa recibida; 422 no identifica modelo no importable | D | `navegacion.md:278-282`; `sldb_adapter.py:201-205`; `workspace_routes.py:163-164`, `:309-310` | PASS |
| D: ningún discriminante inventado | D | `navegacion.md:282` | PASS |
| D: no mismo caso como E5 y E-MD1 | D | `navegacion.md:276`, `:316` | PASS |
| E: authored ≠ modelado; SpecDoc/SpecNodeDoc y manifiesto WS40 derivados | E | `navegacion.md:340-349`, regla 5 `:347-349` | PASS |
| F: `vistas.md:367` cita `notation-view.js:356` y `registry.js:16`, sin aceptación | F | `vistas.md:367`; `notation-view.js:356`; `registry.js:16` | PASS |
| F: solo esa celda cambió en vistas | F | `patch-final.diff` (un `-`/`+` en vistas, hunk `@@ -364,7 +364,7 @@`) | PASS |
| Clave de sesión con alias + identidad local, sin colisión | — | `navegacion.md:168-169` | PASS |
| H-11 sin clase nueva ni modelo/nodo/productor de documento | — | `navegacion.md:369` | PASS |
| Estado borrador, sección 12 «sin acta registrada», sin actas inventadas | — | `navegacion.md:3`; `:395-408`; `:414`, `:418`; búsqueda «acta/recib» | PASS |
| Contradicción: resto de «doc_status no escribe» | — | Sin coincidencia contradictoria; `navegacion.md:185` corrige alcance | PASS |
| Contradicción: `recover_links` usado como resolutor | — | `navegacion.md:152`, `:210`, `:364` lo excluyen | PASS |
| Contradicción: «soportado» para C1-C4 | — | `navegacion.md:199-202` usan «Navegación»/«Tarjeta derivada pasiva» | PASS |
| Contradicción: H-16 con dueño sldb | — | `navegacion.md:372` dueño graph_ui | PASS |
| Contradicción: alias de sldb como autorización | — | `navegacion.md:83` («un alias de sldb no es una autorización»), `:95`, `:307` | PASS |

## Qué no pude verificar

- Los hashes/commits y `stale: WS09` del supervisor: solo leí el árbol actual, no `git show` ni cálculo de sha256.
- Comportamiento en ejecución: no ejecuté rutas, UI, `doc_status`, `open_store` ni pruebas.
- Contenido histórico de `dag.yaml`/auditorías más allá de las líneas abiertas.
- Que `surface` reconstruya el texto íntegro: el contrato mantiene la reserva y no lo afirma.
- Actas o aceptaciones fuera de las búsquedas declaradas en el contrato.

RESULTADO: PASS
