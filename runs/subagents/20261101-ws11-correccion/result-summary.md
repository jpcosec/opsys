# Resultado del Executor: corrección del contrato de navegación de WS11

Executor, 2026-11-01. Escribí solo en `desk/drawer/plans/workspace-documental/contratos/navegacion.md`, en la celda «Renderer existente o requerido» de F18a (`desk/drawer/plans/workspace-documental/borradores/vistas.md:367`) y en este archivo. No ejecuté revisiones, tests ni CLIs; usé únicamente lectura de código y `grep`/`sed`/`awk` de solo lectura, más `sed -i` sobre `navegacion.md` para reordenar una lista y ajustar una cita. Sin commits. Prefijos: GU = `../UIs/graph_ui/frontends/mindmap/` (en el árbol real: `/home/jp/proyectos/SLDB_1/UIs/graph_ui/frontends/mindmap/`), SL = `/home/jp/proyectos/SLDB_1/sldb/src/sldb/`, DK = raíz deskops. Líneas del contrato: las actuales (421 líneas); sha256 tras editar: `navegacion.md` e27f7290c63ef9530169c4d7e6c6ab6b6894f8bd047625ecf16673d515543aaf, `vistas.md` 6f0f249e0f9775a3c75e104f8fa1e5933f6558c04d596fb2dd6a02bd09e40e30.

Commits comprobados con git de solo lectura: graph_ui `134a665` (árbol con untracked ajenos, entre ellos `frontends/workspace/`, que no usé), sldb `77bd6d00`.

## 1. Resolución por decisión y punto

Evidencia «abierta» = archivo y líneas que leí en el código real.

### Decisiones root

| Decisión | Dónde quedó | Evidencia abierta |
|---|---|---|
| 1. No reducir WS13.1 a C1-C4; foco interno distinto de navegación | §6 intro (líneas 176-181), §6.1 (203-214), §6.2 (216-218), §13 punto 2; H-03b/H-05b en §11 | `GU/views/workspace/node/workspace-view.js:15-39,222-226,454-456`; `dag.yaml:850-871`, `933-973` |
| 2. Enlaces entre desks por composición en graph_ui dentro de WS41; sin ampliar sldb; H-16 pasa a integración/API graph_ui de WS41 | §5.2 (148-158, orden obligatorio en 153), §8.4 (294), H-06/H-16/H-17 en §11 | `SL/links/parser.py:6-20`, `SL/links/resolver.py:8-36`, `SL/links/recovery.py:10-31`, `SL/links/sections.py:15-37`, `SL/api/stores/doc_ref.py:1-45`, `SL/api/stores/doc_status.py:18-54`; `dag.yaml:2712-2744` |
| 3. WS18 detenida, opcional, no bloquea, sin pregunta nueva al humano | §9 (línea 318, frase añadida), §12.3 sin cambios | `dag.yaml:1212-1246` |
| 4. Aliases reales = configuración confiable del operador | §3.2 punto 2 (90-99), §3.1 (open_store, 83-85), §8.4, §8.5 E-MD1, §8.6, H-10/H-11 | `DK/deskops/identity.py:65-88,256-262`; `DK/deskops/operations.py:1190-1210`; `SL/api/stores/store_discovery.py:58-76`; `SL/api/stores/doc_ref.py:17-19`; `dag.yaml:2683-2698,2725-2731` |

### Punto A (§§4 y 6, H-03 a H-05b)

| Condición | Dónde quedó | Evidencia abierta |
|---|---|---|
| Separar datos, interacción existente, futuro comprometido | §6 intro (línea 178) y columna «Estado» de C1-C14 | `workspace-view.js:15-39,41-52,222-226,351-363,419,454-456,518,537` |
| C1-C3: navegación, no foco | §6 filas C1-C3 (186-188), §6.1 | `workspace-view.js:222-226,260-264,419,518,537`; `workspace_routes.py:118,200-201,387-413` |
| C4: tarjeta derivada pasiva, `CodeFileView` sin callback | §6 fila C4 (189) | `workspace-view.js:15-39` (firma `{file}`), `:454-456` (solo `file`); `workspace_routes.py:441-451,487-493,565-571` |
| Dominio futuro de WS13.1 con procedencia real | §6.1 (207-214) | `build_ir.py:39,64,68-78`; `extract.py:41-59`; `declared_references.py:64-71`; `composition_edges.py:55`; `flatten.py:3-10` |
| H-03: preservar `fields`/`references` y posición antes de concatenar; no atribuir archivo a nodo del grafo | §2.4 (línea 73), fila C4b, H-03, C11b | `workspace_routes.py:441-451` (concatena y omite no-str/vacíos), `:481-575` (la tarjeta solo lleva `reference`) |
| C5b: sin la negación absoluta | fila C5b (192) | `extract.py:6-13`; `records/__init__.py:12,28`; `api/__init__.py:14`; `build_ir.py:9-24`; `workspace_routes.py:151-165`; `sldb_adapter.py:178-215` |
| C6: `owning_section` opcional | fila C6 (193) | `core/ir/meaning_node.py:12-14`; `build_ir.py:68-78`; `map_fields.py:15-26,39-40,43-74`; `document-ir.mjs:8-17` |
| C7: span exacto sin soporte, no bloquea | fila C7 (194) | `build_ir.py:68-78`; `meaning_node.py:15`; `document-ir.mjs:18-22` |
| C8/C9: multiplicidad; deduplicación | filas C8/C9 (195-196), §2.3 (66), H-03b | `workspace_routes.py:379-393` (clave `:384`); `document_edge.py:13-18`; `document_edges.py:30-41`; `declared_references.py:64-71`; `declared_resolution.py:45`; `composition_edges.py:55`; `edge_record.py:16` |
| C11/C12: foco de la referencia explícita vs mapeo semántico de líneas externas | filas C11/C12 (198-199) | `workspace_routes.py:431-458`; `dag.yaml:857-859,860-871` |
| C14: rango local de Code vs traslado al Markdown | fila C14 (201) | `workspace_routes.py:565-571`; `workspace.mjs:31-61`; `vistas.md:345,349,351` |
| H-05b: no agrupar como una sola capacidad imposible | H-05b (350) separa (a), (b), (c) | las de C11 y C14 |
| «Mismo origen»: misma lectura o revisión; reserva de `surface.text` | §4 (131-136) | `sldb_adapter.py:201-203` (lectura del IR), `workspace_routes.py:156,196` (dos lecturas distintas), `records/utils.py:10-19`, `core/ir/document_ir.py:8-14` |
| `RitualDoc.steps` tiene orden sin `StepDoc` ni progreso | H-21 (366) y §13 punto 6 | `DK/deskops/models/ritual.py:57-82` (`steps: list[str]`, «Ordered prose steps… not document references», `:65-68`); `models/step.py:31-38` |

### Punto B (§3.3, H-06, enlaces)

| Elemento | Dónde quedó | Evidencia abierta |
|---|---|---|
| Guardias generales separadas de las específicas de TaskDoc | §3.3: tabla general (103-113) y párrafo «Guardias específicas» (116) | `GU/deskops_routes.py:31-56` (la guardia está dentro de `board()`, condición `:39`); `DK/deskops/operations.py:1196-1210`; `workspace_routes.py:481-575` (sin comparación con `desk/tasks`) |
| H-06: autorizar y resolver antes de cualquier lectura o recursión | §3.3 viñeta de resolución (124), §5.2 (152-153) | `recovery.py:13-14` (lee destino con `#ancla`), `:28` (lee el documento), `:29-30` (recursión), `:11` (resuelve antes); `resolver.py:33-35` (prueba `Path(tgt)` contra cwd) |
| Sintaxis y tratamiento fijados | §5.2 (149-153), H-16, H-17 | `parser.py:6-7,11,15,17-20`; `sections.py:15-18,30-37`; `doc_ref.py:17-19,22-45`; `doc_status.py:25-33`; `doc_ref_status.py:16`; `api/__init__.py:64,66,126` |
| Sintaxis admitida por el parser | §5.2 (152) y fila C10 | `parser.py:6`: `[[([^\]]+)]]`, cualquier destino sin `]`. El parser admite `alias:Model/name`, `alias:name` y `alias:ruta#Sección`; el resolutor no tiene rama de alias. **No hay obstáculo sintáctico que exponer a root**; ver §5 de este resumen para dos matices |

### Punto C (§§3, 5.4, 8, H-14)

| Elemento | Dónde quedó | Evidencia abierta |
|---|---|---|
| Retirado «doc_status no escribe» | §8.3 (289) | `doc_status.py:3-4,25`; `open_store.py:35-38`; `migration.py:72-80` |
| `readonly` no garantiza cero escrituras; `load_edge_index` no evita la migración transitiva | §3.1 (85), §5.4 (168-174) | `edge_reading.py:14-28`; `open_store.py:26-27,35-41`; `rebuild_edges.py:17-38`; `document_edges.py:30`; `workspace_routes.py:356-359,584`; `document_history.py:26` |
| Stores preparados fuera del request y comprobación al ejecutar consumidores; criterio observable | §5.4 «Obligación» (174) | idem; el criterio es «tras la lectura el store no cambió», medio a los consumidores (`preflight-disposition.md`) |
| Hueco con dueño si la API pública no lo sostiene, sin workaround ni API inventada | §5.4 (174), H-14 | idem |
| Store propio en WS13.1/WS24; segundo desk en WS41 | §5.4 (174), §8.4 (296), H-14 | `ui.md:69` (base de WS24 en `_build_graph_neighborhood`) |

### Punto D (§7, H-09)

| Elemento | Dónde quedó | Evidencia abierta |
|---|---|---|
| `shell/api.js:5-11` descarta `response.status`; delta de WS15.1 en el wrapper cliente | §7.3 (245-249), E2 en §7.5, H-09 | `GU/shell/api.js:4-13` (`response.json()` en `:6` va antes de `:7`; el error solo lleva `.body`) |
| E2 muestra el estado | §7.5 fila E2 (260) | idem |
| E7: IR no construible, `is_degraded` y 422 no identifican modelo no importable; mostrar causa recibida | §7.5 fila E7 y párrafo (265, 269) | `sldb_adapter.py:196-205` (`except Exception` → 422), `workspace_routes.py:162-164,309-346` |

### Punto E (§10)

Regla 5 nueva (336) y filas Authored/Derivado (326-327): authored no equivale a modelado; SpecDoc/SpecNodeDoc derivados del YAML; el manifiesto generado de WS40 es derivado aunque se versione; plantillas, generador y definición del corpus son authored; sin modelo nuevo. Evidencia: `vistas.md` F18a (líneas 363, 373) e `infraestructura.md:35` por referencia (no los reabrí); `dag.yaml:2683-2698`.

### Punto F

`vistas.md:367`, solo ese campo. Citas añadidas: `GU/views/specs/notation/notation-view.js:356` (`export const notationView = {id: 'notation', …}`) y `GU/shell/registry.js:16` (`VIEWS=[… notationView …]`). Lo que leí: esas dos líneas, la importación en `registry.js:6` y `notation-view.js:350-356`; no leí el resto del renderer. No afirma aceptación. Integrarla al lector sigue como candidatura sin productor. Contradicción menor que dejo expuesta sin editar (la disposición lo exige): el campo «Evidencia» de F18a (`vistas.md:375`) no lista las dos citas nuevas.

### Clave de sesión con alias

§5.3 (línea 163): componentes alias del desk + identidad local (`Model:name`, o ruta relativa al root para no modelados), que viajan juntos y no colisionan; sin sintaxis de cadena (`preflight-disposition.md`). H-12 la incorpora. Evidencia de que hoy no existe: `workspace-view.js:57-59,71-85` (solo `?id=&depth=&tab=`).

## 2. Tabla por fila C y H

Leyenda: «sostiene» = la afirmación y sus citas son correctas tal cual; «corregida» = alguna afirmación o cita no se sostenía o era demasiado fuerte; «no se sostiene» = la afirmación principal no se sostenía.

### Filas C

| id | Citas abiertas | Resultado | Cambio |
|---|---|---|---|
| C1 | `workspace_routes.py:118,395-413`; `workspace-view.js:222-226,419` | sostiene (las citas); la clasificación «soportado» era inexacta para foco | Reclasificada como navegación; tres columnas datos/interacción/futuro |
| C2 | `workspace_routes.py:200-201,387-393`; `workspace-view.js:518,537` | sostiene; faltaba `:518` (relaciones salientes) | Navegación; se agrega `:518` |
| C3 | `workspace-view.js:260-264` | sostiene | Navegación, no foco |
| C4 | `workspace_routes.py:441-451,487-493,565-571`; `workspace-view.js:15-39,351-363,454-456` | corregida: «soportado texto→Code» no se sostenía | Tarjeta derivada pasiva, sin callback; se registra que se omiten elementos vacíos |
| C4b | `workspace_routes.py:441-451`; `flatten.py:3-10` | sostiene; además se pierde la posición | Se agrega posición, H-03 la preserva |
| C5 | `build_ir.py:39,64`; `extract.py:41-59`; `utils.py:10-19`; `workspace-view.js:41-52` | sostiene | Se separa datos/interacción/futuro; el fin de sección se extiende (`extract.py:52-59`) |
| C5b | `extract.py:6-13`; `records/__init__.py:12,28`; `api/__init__.py:14`; `build_ir.py:17-24`; `workspace_routes.py:151-165`; `sldb_adapter.py:178-215`; `ui.md:55` | corregida: «No hay IR sin modelo» demasiado absoluto; `ui.md:55` no lo sostiene (solo dice que falta Markdown sin modelo en el workspace) | Reformulada; reutilización por verificar; sin modelo inventado |
| C6 | `build_ir.py:68-78`; `meaning_node.py:12-14`; `map_fields.py:15-26,39-74`; `document-ir.mjs:8-17` | corregida: `owning_section` es opcional | Dato opcional, derivado de plantilla, no rango exacto |
| C7 | `build_ir.py:68-78`; `meaning_node.py:15`; `document-ir.mjs:18-22` | sostiene | Se agrega que no bloquea foco de campo/contenedor |
| C8 | `declared_references.py:64-71`; `composition_edges.py:55`; `document_edge.py:13-18`; `edge_reading.py:14`; `edge_record.py:16`; `declared_resolution.py:45`; `workspace_routes.py:379-393` | corregida: faltaba la deduplicación (`:384`) y los campos de composición | Multiplicidad; solo las aristas `schema` llevan campo |
| C9 | idem | corregida: «inverso de C8» no era uno a uno | No se elige un campo arbitrario |
| C10 | `parser.py:6-7`; `resolver.py:33-35`; `recovery.py:13-14,29-30` | corregida: la cita era `32-37` (es `33-35`) y «existe `recover_links`» induce a usarlo | Composición de 5.2 |
| C11 | `workspace_routes.py:431-458`; `dag.yaml:857-871` | corregida: mezclaba dos casos | (a) foco de la referencia explícita, comprometido; (b) mapeo semántico, sin soporte |
| C12 | `dag.yaml:857-859` | sostiene | Sin cambio de fondo |
| C13 | `workspace_routes.py:68-71` | sostiene | Sin cambio |
| C14 | `workspace_routes.py:565-571`; `workspace.mjs:31-61`; `vistas.md:345,349,351` | corregida: mezclaba rango local y traslado | (a) rango local de Code; (b) traslado, no comprometido |

### Filas H

| id | Citas abiertas | Resultado | Cambio |
|---|---|---|---|
| H-01 | `workspace_routes.py:431-458,196,326,539`; `sldb_adapter.py:202` | corregida: la negación «ninguna ruta entrega» mezclaba leer/exponer/devolver | §2.2 distingue; «mismo origen» agregado |
| H-02 | `workspace_routes.py:102-127` | sostiene | Sin cambio |
| H-03 | `workspace_routes.py:441-451` | sostiene | Se agrega posición |
| H-03b | `workspace_routes.py:384`; `declared_references.py`; `edge_reading.py:14` | corregida | De «candidato no comprometido» a delta futuro comprometido (decisión 1); multiplicidad |
| H-04 | IR en `workspace_routes.py:153-161`; `document-ir.mjs` | sostiene | Se agrega `owning_section` opcional y dependencia de C5b |
| H-05 | `build_ir.py:68-78` | sostiene | Se agrega «no bloquea» |
| H-05b | las de C11/C14 | corregida | Tres capacidades; (c) sin productor |
| H-06 | `recovery.py:13-14,23,29-30`; `audit.py:10`; `resolver.py:33-35`; búsqueda en GU | corregida: «graph_ui no consume recover_links» es cierto pero la solución no es consumirlo | Composición con autorización antes de leer; productores WS13.1/WS41/WS15.1 |
| H-07 | sin cita de código en la fila; WS13.3 en `dag.yaml:933-973` | sostiene | Sin cambio |
| H-08 | `GU/index.html:7-8`; búsqueda de `onerror/onError/import(` en `index.html`, `app.js`, `shell/*.js` | sostiene | Sin cambio |
| H-09 | `GU/shell/api.js:4-13` | corregida: «`request()` entrega los datos» era falso para el estado HTTP | Clase pasa a «API cliente + renderer» |
| H-10 | `dag.yaml:2683-2698` | sostiene (la fila); el texto de §3.2 se corrigió | Manifiesto = derivado |
| H-11 | `identity.py:65-88,256-262`; `operations.py:1190-1210`; `store_discovery.py:58-76`; `dag.yaml:2712-2744` | corregida por decisión 4 | De «instancia, deskops, sin productor» a configuración del operador |
| H-12 | `workspace_routes.py:68-71`; `workspace-view.js:57-59,71-85` | sostiene | Se agrega clave de sesión con alias |
| H-13 | `document_history.py:1-30` | sostiene | Sin cambio |
| H-14 | `workspace_routes.py:356-359,584`; `document_edges.py:30`; `rebuild_edges.py:17-38`; `open_store.py:26-41`; `edge_reading.py:14-28`; `migration.py:72-80`; `doc_status.py:25` | corregida | Ver §3 de este resumen |
| H-15 | sin cita de código | sostiene (no reabrí sus productores) | Sin cambio |
| H-16 | `resolver.py:33-35`; `parser.py:6`; `dag.yaml:2723-2731` | corregida por decisión 2 | De «sldb, sin productor, requiere decisión» a graph_ui/WS41 |
| H-17 | `dag.yaml:2692-2693` | sostiene | Se agrega la sintaxis de 5.2 |
| H-18 | `GU/deskops_routes.py:31-56,83-93` | sostiene | Sin cambio |
| H-19 | sin cita de código | sostiene (no reabrí WS23 salvo `dag.yaml:1536-1546`) | Sin cambio |
| H-20 | sin cita de código | sostiene (no reabrí WS24) | Sin cambio |
| H-21 | `ritual.py:57-82`; `step.py:31-38`; búsqueda de `progress/done` en `deskops/models/*.py`; `dag.yaml:1540-1546` | corregida: la búsqueda «sin resultados» era falsa en general (hay `done_when` en `task.py` e `in_progress` en `run.py`) | Búsqueda acotada a `ritual.py` y `step.py`; `steps` ordenado sin StepDoc |
| H-22 | `repository.py:35-52`; `inbox.py:37-61`; `materialization.py:31-61`; `pill.py:59-80`; `step.py:31-38`; `faq.py:19-22` | sostiene; los rangos citados estaban cortos | Rangos ampliados en §13 punto 5 |
| H-23 | `search.py:26`; `find_routes.py:1-25`; búsqueda en GU | corregida: «graph_ui consume search/GET /find» no se sostiene en estas rutas | Redactada como «sldb ofrece; graph_ui no consume en estas rutas» |
| H-24 | sin cita de código | sostiene (no reabrí WS15.2) | Sin cambio |
| H-25 | sin cita de código | sostiene (remisión a WS12) | Sin cambio |

Otras citas corregidas fuera de filas C/H, al revisar los bloques que toqué: `GU/serve.py:49` (es `view_file`) por `:507,:512` (§3.1); `SL/links/resolver.py:32-37` por `:33-35`; `SL/api/stores/store_links.py:15-36` por `:15-39`; §8.3 decía que `load_runtime_documents(include_linked=True)` «no se usa en graph_ui» (se usa sin federar, `sldb_adapter.py:386-388`, defecto `False` en `runtime_documents.py:17`; y el defecto de `load_edge_index` es `True`, `edge_reading.py:14`); §4 afirmaba que no había operación pública que devolviera texto del archivo (existe `compose_document`, `SL/links/composer.py:9-31`, exportada por `sldb.links`, no por `sldb.api`); §2.2 decía «dos puntos internos» que leen el archivo propio (hay además la lectura del IR en `sldb_adapter.py:202`, cuyo IR llega entero al cliente, y `:539` que devuelve texto de archivos referenciados); §5.4 afirmaba «reconstruye» sin matiz (la docstring de `rebuild_edges` dice que sobre un store al día no escribe nada, `:20-21`); `Contención del Board` figuraba entre las guardias generales.

## 3. Filas con productor o clasificación cambiados

| Fila | Antes | Ahora |
|---|---|---|
| C1, C2, C3 | «soportado» | Navegación, no foco |
| C4 | «soportado texto→Code» | Tarjeta derivada pasiva |
| C11 | «no soportado, requiere decisión de alcance» | (a) comprometido en WS13.1; (b) sin soporte |
| C14 | «no soportado» | (a) rango local, WS13.1; (b) traslado, sin productor |
| H-03b | «WS13.1 (candidato; no comprometido)» | WS13.1, delta futuro comprometido (decisión 1) |
| H-05b | WS13.1 «requiere decisión» o sin productor | (a) y (b) WS13.1; (c) sin productor ni compromiso |
| H-06 | WS13.1 y WS15.1 | + WS41 (entre desks); composición, no `recover_links` |
| H-09 | renderer, WS15.1 | API cliente + renderer, WS15.1 |
| H-10 | instancia, manifiesto «una vez generado» authored | instancia WS40; el manifiesto es derivado |
| H-11 | instancia, dueño deskops, sin productor | configuración del operador; WS11 fija el input, WS41 consume y valida; sin productor de documento. **La clase «instancia» no encaja y no inventé otra: la fila dice «no es una instancia a escribir»** (ver §5) |
| H-12 | WS41 | WS41, más clave de sesión con alias |
| H-14 | WS41; store propio sin productor | store propio: delta de lectura WS13.1 y ruta consumida por WS24; segundo desk: WS41 |
| H-16 | API, dueño sldb, sin productor | API/integración, dueño graph_ui, productor WS41 |
| H-17 | WS40; WS17 | igual, con la sintaxis de 5.2 |
| H-21 | sin cambio de productor | solo texto de evidencia |
| H-23 | sin cambio de productor | solo texto de evidencia |

## 4. Qué leí y qué no

Leí completos: `review-source.md`, `preflight-disposition.md`, la TaskDoc y el contrato (3 lecturas parciales por tamaño, todo cubierto). Leí en graph_ui completos: `workspace_routes.py`, `shell/api.js`, `deskops_routes.py`, `views/workspace/node/workspace-view.js`, `workspace.mjs`, `shared/document-ir.mjs`, `shell/registry.js` (1-20), `views/specs/notation/notation-view.js` (líneas 350-356), `views_routes.py` (25-70), partes de `sldb_adapter.py` (176-225, 380-390), de `serve.py` (40-60, 140-152, 236-246, 310-325, 500-520) y de `index.html` (líneas 7-8). En sldb leí completos: `links/parser.py`, `recovery.py`, `resolver.py`, `sections.py`, `audit.py`, `parsed_link.py`, `resolved_link.py`, `links/__init__.py`, `api/records/build_ir.py`, `utils.py`, `flatten.py`, `map_fields.py`, `extract.py`, `api/edges/document_edge.py`, `document_edges.py`, `edge_reading.py`, `api/stores/doc_ref.py`, `doc_ref_status.py`, `doc_status.py`, `open_store.py`, `store_links.py`, `indexed_documents.py`, `core/ir/meaning_node.py`, `store/edge_index/declared_references.py`, `composition_edges.py`, `store/models/edge_record.py`, `store/migration.py` (1-80), `rebuild_edges.py` (1-38). Parcialmente: `declared_resolution.py` (28-92), `store_discovery.py` (40-95), `document_serialization.py`, `document_render.py`, `document_ast.py`, `document_routes.py`, `sections_routes.py`, `payload_save.py`, `track_document_file.py`, `provenance_stamp.py`, `document_history.py`, `links/composer.py`, `links/render.py`, `cli/serve/render_routes.py` (1-60), `find_routes.py` (1-25), `lint_routes.py`, `iter_records_docs.py` (28-60), `build_document_segments.py` (60-95), `store/query.py` (70-104), `migration_legacy_layout.py` (35-60). En deskops: `identity.py` (60-92, 245-270), `operations.py` (360-398, 1190-1215), `models/repository.py`, `ritual.py`, `step.py`, `faq.py`, `inbox.py`, `materialization.py`, `pill.py` (rangos citados), `dag.yaml` (681-712, 836-875, 933-975, 1052-1093, 1212-1246, 1536-1548, 2668-2750), `vistas.md` (343-380), `ui.md` líneas 46, 55, 56, 69, 87, 158.

Búsquedas de solo lectura (`grep`): `read_text|read_bytes|open(` en GU (`*.py`) y en `SL/api`, `SL/links`, `SL/cli/serve`; `focus` en `workspace_routes.py` y `views/workspace`; `[[|wikilink|recover|/lint` en GU; `sldb.links`, `anchors`, `document_history`, `list_repo_task_routes`, `doc_status`, `open_store`, `edges_to|edges_from`, `render_document_markdown`, `/api/find|.search(` en GU (`*.py`, `*.js`, `*.mjs`, fuera de `fixtures/`); `progress|done` en `deskops/models/*.py`; `write|save|dump|mkdir|unlink` en cinco módulos de `SL/store/edge_index/`; existencia de `UIs/graph_ui/runs/subagents/workspace-documental-acceptance/` (no existe).

No leí: el resto de `serve.py`, `views_routes.py` (70 en adelante), `projection_views.py` (§9 no se tocó y sus citas no se reabrieron), `store/layout.py` (`store_exists`), `resolve_runtime_doc`, `compose_edge_index` completo (solo busqué escrituras en cinco módulos), el resto de `notation-view.js`, `auditoria/infraestructura.md`, `auditoria/deskops.md`, `decisiones.md`, `reconciliacion.md`, `user-flows.md`, `alcance.md`, `vision.md` y las filas del DAG de WS22, WS23 (salvo 1536-1548), WS24, WS15.2, WS43. No afirmo haber ejecutado nada: todo es lectura de código y de documentos. El diff vacío entre `215bf624` y `c19c6c0d` lo informa root (`review-source.md:7`); no lo repetí. Qué hace `compose_edge_index`/`resolve_runtime_doc` respecto de escrituras no está verificado más allá de las búsquedas citadas.

## 5. Decisiones de producto no cubiertas

Ninguna que impida el contrato. Quedan cuatro puntos que expongo para que root los vea; ninguno está decidido por mí fuera de lo derivable del código y los dejé redactados dentro de lo cubierto:

1. **Alias de operador frente a nombres de enlace de store.** El prefijo `alias:` de una referencia pública de sldb es el nombre de un enlace directo del store de lectura (`doc_ref.py:3-7,40`); el alias de operador (decisión 4) es otra cosa. El contrato resuelve el prefijo contra el conjunto del operador y llama `doc_status(<directorio del store autorizado>, resto)` sin prefijo, así que no exige que coincidan. Si root quisiera que coincidan, sería una decisión nueva.
2. **Alias `local` reservado.** Lo derivé de que `local:` ya significa «el store local» en `doc_ref.py:18,38-39`. Lo escribí como «el contrato lo trata como reservado» (§3.2, línea 93). Es una consecuencia de la sintaxis pública, no un valor de alias; si root prefiere no reservarlo, hay que quitarlo.
3. **Prefijo no autorizado dentro de un enlace de texto.** El contrato dice que, si el prefijo no está en el conjunto autorizado, la cadena entera se trata como destino local (regla de `doc_ref.py:6-7`) y, si no resuelve, se informa como referencia rota con origen y causa (E5), no como E-MD1. La redacción exacta del mensaje queda a WS41/WS15.1. El criterio de aceptación de WS41 pide «alias no autorizado… error visible» (`dag.yaml:2728-2731`), que cubre la petición con alias, no el enlace de texto con prefijo; si root quiere E-MD1 también para el texto, hay que decidirlo.
4. **Clase de H-11.** La clasificación del contrato tiene cinco clases (instancia, vínculo, consulta, API, renderer) y la configuración confiable del operador no es ninguna; lo anoté en la propia fila sin añadir una sexta clase. Root puede querer ampliar la lista de clases o conformarse con la nota.

Dos observaciones que no son decisiones de producto: (a) la comprobación «no se escribe» queda como obligación con criterio observable y medio a los consumidores; no pude sostener con API pública que `doc_status` o `load_edge_index` no migren (no ejecuté nada), por eso el contrato lo deja como hueco con dueño si no se sostiene; (b) el campo «Evidencia» de F18a (`vistas.md:375`) no lista las dos citas nuevas; no lo edité por la disposición.

## Ajuste del Supervisor antes de congelar

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01, sin Executor. Leí el contrato completo y el diff de `vistas.md`. Por lectura, nada ejecutado.

- **§5.2, paso 6.** La redacción del Executor pasaba a `doc_status` el destino sin prefijo y prohibía `split_doc_ref`, pero `doc_status` lo llama por dentro (`doc_status.py:26`). Un destino con dos puntos seguiría un enlace directo del store que el operador no autorizó. `deskops/.sldb/store.yaml` declara enlaces, así que el caso es real. Ahora el paso exige `"local:" + resto`, sintaxis pública que deja el resto entero y solo busca en ese store (`doc_ref.py:38-39`).
- **`vistas.md:367`.** Usaba el prefijo `GU/`, no definido en ese archivo. Ahora lleva la ruta completa.

## Ajuste del Supervisor por la comprobación focal root

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01, sin Executor. Autoridad: `review-source-2.md`. Por lectura, nada ejecutado.

- §5.2: `local:` se reconoce antes que los aliases y se retira una vez; designa el desk de origen o de la petición; el resto no se reinterpreta. Tabla de ejemplos positivos y negativos.
- §3.2 y §8.5: `local` reservado, WS41 rechaza esa entrada. E-MD1 solo para el parámetro explícito de alias; el literal de texto del paso 3c es E5.
- C5b: el builder consume un descriptor y no consulta registro; reutilización con `model=None` por verificar en WS13.1.
- H-11: fuera de las cinco clases documentales, sin clase nueva.
- `vistas.md` no cambia respecto de `b4968374`: root resolvió que Evidencia de F18a no se toca.

## Ajuste del Supervisor tras la revisión fresca, ronda 1

Claude Opus 5.5, sin Executor. Tres frases: §5.2 `local:`, §3.2 soporte de la configuración, §7.5 E7 como caso de E4. Disposición en `contrato-review-disposition.md`.

## Ajuste del Supervisor tras la revisión fresca, ronda 2

Una frase en §3.2.1: sin alias configurado, el desk del proceso usa `local`. Decisión mía, declarada para root.
