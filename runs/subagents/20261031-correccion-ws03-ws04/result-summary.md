# Resultado del Executor: corrección WS03/WS04

Alcance: solo `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` (WS03, abreviada «infra») y `.../auditoria/ui.md` (WS04, «ui»). Lectura de ../sldb, ../pron, ../spec2viz, ../UIs/graph_ui y softfactory_spec sin escribir. No se ejecutó ningún test, servidor ni comando mutante; todo lo de abajo es lectura estática. Sin commits ni `git add`. Rutas de sldb relativas a `../sldb/src/sldb`, pron a `../pron/src/pron`, graph_ui a `../UIs/graph_ui` (HEAD 134a665). Las copias previas de ambos archivos quedaron en `/tmp/infra.before` y `/tmp/ui.before` (no son entregable).

Ningún punto de la revisión fue contradicho por la fuente. Matices que la fuente aporta (no contradicciones) están marcados «Matiz».

## Punto 1. Frescura del payload de `expected` (infra)

Afirmación previa (infra §2.1, fila «Verificación optimista en HTTP»): «se compara por igualdad el payload actual extraído del archivo con `expected`».
Afirmación nueva: el payload se obtiene por carga runtime sujeta a caché (`load_runtime_documents`), no se relee del archivo en cada petición; límite de frescura: una edición externa que no altere los índices puede preceder a `/save` y no observarse en `expected`. Marcado como deducción estática, no reproducida; sin afirmar caché fresca por defecto. Se mantienen los dos hechos: no hay CAS por hash, y `expected` es una comparación optimista pública por valor (409).
Filas/secciones tocadas por el mismo hecho: §1 «Payload (lectura)», §1 «Cache del payload», §2.1 «Verificación optimista en HTTP», §2.1 «Escritor externo del Markdown» (decía «revalida por mtime y tamaño» sin decir que es una vez por operación), §6 ítems 2 y 3, §7 primer punto.
Citas abiertas:
- `cli/serve/http_server.py:22-26` (`build_handler` llama una vez a `get_store_context`).
- `cli/serve/save_routes.py:38-40` (`batch_save`: `load_runtime_documents` sin `new_operation`); `save_plan.py:49-51,57-59` (comparación `existing.payload != change.get("expected")`).
- `store/query.py:64-73` (la carga con codec por defecto pasa por `cached_store`, `:71`).
- `store/runtime_cache.py:37-46` (`cached_store` devuelve el hit si la firma coincide).
- `store/runtime_cache_signature.py:39-43` (`new_operation` programa el barrido), `:56-66` (stats por operación), `:73-76` (`leaf`, `SLDB_TRUST_CHAIN`), `:79-86` (`_leaves` reutiliza `_LAST_LEAVES` salvo `_FORCE_SWEEP`).
- `new_operation`: llamado desde `api/stores/open_store.py:40`, que alcanza `get_store_context` (`cli/store_context.py:19-24`). No hay ninguna llamada en `cli/serve/` (grep de `new_operation|get_store_context|open_store|invalidate_runtime_cache` en `cli/serve/` y `cli/commands/serve.py`: solo `http_server.py:16,23`).
- Matiz (fuente, no estaba en la revisión): las escrituras de la API sí llaman `open_store` (`api/documents/payload_save.py:35`, `create_document.py:43`, `untrack_document.py:45`), por lo que tras un guardado aplicado por el mismo proceso la siguiente carga vuelve a barrer. La ventana de staleness va desde el arranque o el último guardado propio hasta la siguiente operación. Quedó escrito en la fila. Con `SLDB_TRUST_CHAIN` no hay barrido (`runtime_cache_signature.py:81-82`).
No verificado: el comportamiento real (no se reprodujo); prueba futura en sandbox propio: un `sldb serve` sobre store temporal con una edición externa previa a `/save`. Tampoco se verificó el orden de eventos con hilos concurrentes.

## Punto 2. `+ Add relation` frente al SPEC (ui)

Afirmación previa (ui, §5 SPEC, fila `## 5`, Discrepancias): «5.1.3: SPEC dice que `+ Add relation` está fuera del plan; el plan sí cubre alta/baja de relaciones permitidas por contrato (WS19.2), aunque no con el nombre ni sobre aristas sin archivo.» y en Ausencias «5.1.3: aristas sin archivo físico, sin contraparte.»
Afirmación nueva: `SPEC.md:79-82` (§5.1) lista «Relaciones exclusivas de grafo (`+ Add relation`): creación de aristas semánticas sin archivo físico directo» (`:82`) entre lo no contemplado en el plan. `connect-dialog.js:9-17` modifica campos de referencia del documento origen (el ID destino se guarda en un campo del modelo; `map-view.js:80-83`, `applyConnection`, lo asigna a `payload[field]`). No equivalen. La comparación queda como capacidad no cubierta o no comprobada como arista autónoma, sin refutar al SPEC con WS19.2. Ausencias: «capacidad no cubierta o no comprobada, sin contraparte demostrada».
Citas: `/home/jp/proyectos/softfactory_spec/SPEC.md:79-82`; `frontends/mindmap/views/documents/map/connect-dialog.js:9-17`; `frontends/mindmap/views/documents/map/map-view.js:80-83`.
Matiz: el SPEC dice «no contemplados en el plan de producto», lo cual es consistente con la atribución previa de «fuera del plan»; lo incorrecto era la equivalencia con WS19.2, no la atribución. «Puente demostrado» = código que convierta lo editado en una arista sin archivo físico: no se encontró en `connect-dialog.js` ni `applyConnection`; no se auditó todo graph_ui (un grep de `RelationDoc|add_edge|create_edge|assert_edge` en graph_ui halló solo proyecciones/exportación y `frontends/workspace/serve.py`, sin abrirlos uno a uno).

## Punto 3. `task.txt` como estado vigente (ui)

Afirmación previa (ui, §2, párrafo «Discrepancia observada», ex línea 42): task.txt declara `Status: active` mientras Board/reconciliación la dan por cerrada; «es un snapshot de fecha no verificada… no se resuelve cuál es el estado vigente».
Afirmación nueva: «Estado histórico, sin discrepancia actual»: snapshot agregado por a1b2b22 (2026-10-31 05:19); f16fcd1 borra el TaskDoc y quita su entrada del Board; 134a665 actualiza las Notes del Board; no hay contradicción actual.
Comprobado con git en `../UIs/graph_ui`:
- `git show --stat f16fcd1` (2026-10-31, «closeout… Closeout-Reason: integrada: squash a1b2b22»): `.sldb/store.yaml`, `desk/tasks/Board.md`, el TaskDoc `task-workspace-multiproyeccion-documento-grafo-local-codigo-y-contexto.md` (76 líneas borradas) y `runs/subagents/index.jsonl`; 4 archivos, +4/−78. El diff de Board quita la entrada del TaskDoc.
- `git show --stat 134a665` (2026-10-31): solo `desk/tasks/Board.md`, +1/−1, Notes ahora dicen «integrada y cerrada».
- `git log -- runs/subagents/20261031-workspace-ui/task.txt`: único commit a1b2b22; `desk/tasks/` hoy contiene Board.md y los dos TaskDoc draft.
No verificado: la hora exacta de creación de task.txt fuera de git. El handoff no se tocó (rol del Supervisor).

## Punto 4. Consultas guardadas frente a `ProjectionDoc` (infra)

Afirmación previa (§4, fila «Consultas guardadas / vistas de búsqueda en el store»): ausente por un grep de `saved.?quer|consulta guardada|saved_view`, y «Lo más cercano es `ViewDoc`, que es un modelo sin evaluador». También §4 fila «Consulta estructurada…»: «no hay consultas guardadas en el store».
Afirmación nueva: sigue «ausente» solo para una consulta guardada con `where` en sldb; la fila declara que el grep niega esos nombres, no toda selección persistida, y delimita la capacidad vecina verificada. `ProjectionDoc` (`pron/models/projection.py:14`) es un documento persistido `projection-<name>` y evaluado: `world/projection_reader.py:22-38` (`ProjectionReader.__call__` lo lee por nombre o sintetiza `all`); `world/lexicon.py:33,46` lo recibe y `:137-148` (`projection_models`) filtra los modelos de sus stores por la lista `models`; `relations` filtra tipos de relación (`world/lexicon_parts/relation_words.py:27`), `aliases` anclas (`alias_words.py:24`), `actions` verbos (`kernel/kernel.py:45`). Selecciona qué stores, modelos, tipos de relación, alias y verbos puede nombrar una sesión; no tiene campo `where` y no selecciona documentos por condición sobre campos; no declara dirección, layout ni notación. Por eso no es un `where` guardado ni `ViewDoc`.
Matiz: la fila ya no dice «lo más cercano es ViewDoc, modelo sin evaluador» (ver punto 5); remite a §5.2.
No verificado: que pron no tenga otro mecanismo de selección persistida fuera de los tres archivos citados; no se ejecutó `pron lexicon`.

## Punto 5. ViewDoc: universo, §6 y base graph_ui

Infra, afirmaciones previas:
- §5.2 filas: «ViewDoc: quién lo produce» («graph_ui… no comprobado»), «quién lo evalúa» (ausente), «renderers que lo aceptan» («Ninguno»).
- Párrafo «Qué existe en su lugar»: el cruce `where` «no está implementado en el repo».
- §6 ítem 1: «WS18 deberá construir la evaluación (o el dueño externo, graph_ui, aportarla)».
- §7: «graph_ui (consumidor declarado…): fuera de los tres repos; no leído».
Infra, nuevas: se añadió una introducción a §5.2 que acota el dictamen «solo modelo, sin evaluador» al universo sldb/pron/spec2viz y nombra por separado modelo (`spec2viz.sldb_models.ViewDoc`), notación (`NotationDoc` + `resolve_documents`), evaluador y renderer. Las filas conservan su estado («ausente» en evaluador y renderers) con la marca «dentro de sldb, pron y spec2viz» y un puntero a ui.md; el productor remite a `POST /api/views/save`. §6 ítem 1 ya no dice que WS18 deba construir un evaluador: dice que graph_ui ya es un consumidor y que WS18 parte de él antes de fijar alcance. §7 se actualizó.
Ui, nuevas: sección 3.1 «Base reutilizable: ViewDoc en graph_ui» (tabla con las piezas modelo, evaluador, rutas, conexión/límite, notación, renderer y pruebas, en el formato de tabla existente); fila WS18 de «solo referencia» (dueño spec2viz, no entra en los 35, conteo sin cambio) y nota en WS24; la lista del universo (§1) menciona WS18; §6 actualiza lo no leído/no ejecutado. Sin anunciar aceptación.
Citas leídas (graph_ui, todo trackeado: `git ls-files` lista los cuatro archivos):
- `frontends/mindmap/projection_views.py`: `evaluate_view` `:107-124`; `_selected` `:48-54`; `_relation_filter` `:57-62`; `relation_edges` usado en `:113-114`; `_notation` `:85-104`; `list_views` `:127-131`; `find_view` `:134-137`; docstring (graph_ui solo evalúa, dibujar queda en spec2viz) `:1-19`.
- `frontends/mindmap/sldb_adapter.py:384-436` (`runtime_documents`, `where_holds` vía `sldb.api.where.where_matches`, `relation_edges` vía `execute_query`, `notation_documents` vía `resolve_documents`, `ensure_model`, `write_document`).
- `frontends/mindmap/views_routes.py:1-7` (rutas), `:20,48-53` (registro del modelo, 501 si falta spec2viz), `:56-66` `save_view`, `:69-87` `dispatch`.
- `frontends/mindmap/serve.py:147-154` `_api_views` (501 en remote, `:149-150`), `:332-334` despacho GET, `:382-389` despacho POST con validación de origen (`:383-385`).
- Pruebas existentes, no ejecutadas: `tests/test_projection_views.py` (`importorskip("spec2viz")`, stores temporales; funciones en `:47-166`), `tests/e2e_review_workbench_views.py` (Playwright y servidores reales, se omite sin Playwright `:82-83`; `:154,215,319`).
- Commits (`git log -1`, `git show --stat`): 0eb7dd7 (2026-10-19, «views: graph_ui evalúa vistas de proyección con sldb.api.graph»; projection_views.py, serve.py, views_routes.py, tests/test_projection_views.py), b9ab83c (2026-10-19, «views: las llamadas a sldb pasan por sldb_adapter»; añade sldb_adapter.py), 2a15356 (2026-10-20, «Vistas (ViewDoc): la notación de la vista se aplica con resolve_documents y review-workbench la dibuja»; 17 archivos).
- dag.yaml: WS18 `:1158-1180` (`owner_repo: spec2viz`, `requires: G_SPEC_VIEW`); WS24 `:1492-1514` (ViewDoc opcional tras G_SPEC_VIEW, sin bloquear).
Matices de la fuente: (a) el `evaluate_view` de graph_ui lee con `load_runtime_documents`, así que hereda la caché del punto 1 (lo anoté en 3.1); (b) `save_view` guarda sin `expected` (por lectura: sin 409 en ese guardado); (c) el código de `apps/review-workbench` (renderer) no se abrió, solo el stat del commit 2a15356 y su asunto; la fila Renderer lo dice.
No verificado: que las pruebas pasen; que el evaluador funcione en runtime; el renderer de review-workbench; los HEAD de graph_ui y de los otros repos fueron los de la lectura de hoy.

## Punto 6. «Sin dueño», `/app.js` y «no ejecutado: fuera de alcance»

Ui, afirmación previa (§4.2, `frontends/workspace/`): «sin atribución» y «`index.html` referencia `/app.js` y el directorio no contiene `app.js` (el handler sirve solo `frontends/workspace/`)». No existía la expresión literal «sin dueño».
Ui, nueva: «sin reclamo en Board ni TaskDoc observados (no es una afirmación de autoría desconocida)» y la ausencia de `/app.js` respaldada con citas: `frontends/workspace/index.html:145` (`<script type="module" src="/app.js">`), `serve.py:24,513` (`SimpleHTTPRequestHandler` con `directory=WORKSPACE_DIR`), `serve.py:563-566` (el único fallback a `index.html` es para nombres sin punto, por lo que `/app.js` no se resuelve) y no hay ruta JS (el `do_GET` solo maneja `/api/…`, `:524-561`). No es requisito previo de WS06 sino de adoptarlo como base ejecutable autorizada. `ls` del directorio: `index.html`, `__init__.py`, `serve.py`, `styles.css` (más un `__pycache__` ya presente, no creado por mí).
«No ejecutado: fuera de alcance» (sin sugerir imposibilidad, con test futuro en sandbox propio, sin diseñarlo): infra §1 convención «Por lectura», §1 filas de ViewDoc con pruebas (`tests/test_view_doc.py`), §5.2 apariciones no código, §7 (concurrencia, corpus, pruebas de ViewDoc/renderers, graph_ui, POSIX); ui fila WS15.1 y §6. Frases retiradas: «hacerlo exigía escribir en un repo ajeno», «prohibido», «crean cachés/índices».
No verificado: no se auditó cada `no se ejecutó` del documento, solo los que sugerían imposibilidad (grep de `hacerlo|prohibido|crean cach|crea índices` en infra queda vacío). Las menciones sueltas «por lectura, no ejecutado» en §2.1 se dejaron: no sugieren imposibilidad.

## Otras filas revisadas y dejadas sin cambio

- Infra §2.1: lock de store, qué cubre el lock, escritura atómica, lock del journal, lock del servidor HTTP, guardado parcial, forma legacy, CAS ausente, DB, `create_document`, `selfdoc`, borrado, historia; §2.2 y §2.3 completos; §3 (referencias; la fila «Referencia del ViewDoc a una notación» solo cambió «no se ejecutó» por «no ejecutada: fuera de alcance»); §4 salvo la fila «Consultas guardadas» y una frase de «Consulta estructurada…»; §5.1 completo; §5.2 filas de sldb, pron, definición, registro y apariciones (esta última solo la frase de no ejecución).
- Ui: §2 tablas de tareas y SHAs; §3 filas WS13 a WS42 salvo WS15.1 (frase de no ejecución) y WS24 (nota ViewDoc); WS19.2 (la fila usa «alta de relación sobre campos de referencia», que ya era exacta); §4.1, 4.3; §5 filas `## 1`, `## 2`, `## 3`, `## 4` y `## 6` y la nota final; §6 salvo los dos puntos mencionados. `dag.yaml`, `reconciliacion.md`, `brief.md`, WS02, handoff y WS06 no se tocaron.

## Otras filas que los hechos nuevos volvían falsas (corregidas dentro del alcance)

- Infra §5.2 fila «ViewDoc: quién lo produce»: decía que graph_ui es «no comprobado»; corregida (punto 5).
- Infra §5.2 fila «quién lo evalúa» y «renderers»: seguían válidas solo dentro del universo; acotadas y con puntero.
- Infra §5.2 párrafo «Qué existe en su lugar»: añadida la salvedad de graph_ui.
- Infra §4 «Consulta estructurada…»: «no hay consultas guardadas en el store» era demasiado amplio; ahora remite a la fila de consultas guardadas.
- Infra §2.1 «Escritor externo del Markdown»: «revalida por mtime y tamaño» omitía el límite por operación; corregida.
- Infra §1 «Payload (lectura)»: no mencionaba la caché; añadida.
- Ui §6: «No se ejecutó la UI ni sus pruebas» y «no se leyó el contenido de los commits» actualizados (excepción para los commits ViewDoc).
- Ui §1: la lista del universo ahora menciona WS18 (referencia).
Ninguna mención de frescura de caché en ui.md (grep sin coincidencias aparte de lo añadido en 3.1).

## Líneas de encabezado

Ambos archivos tienen una línea bajo el título con «Corrección 2026-10-31» y el motivo.

## Validaciones del contrato: no corridas por el Executor

`build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`, el `git diff --stat 2286b976..HEAD` y los `test -s` quedan para el Supervisor; este Executor no los ejecutó. Los archivos de auditoría son authored (no los reescribe `build_plan.py`).
