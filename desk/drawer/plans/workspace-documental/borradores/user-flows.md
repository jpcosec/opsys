# User-flows del workspace

Estado: borrador de intención. Los pasos son objetivos de UX, no afirmaciones de implementación. Cada flujo requiere mapa a operaciones reales y contrato de errores en WS08/WS07.

## Convención de los campos añadidos por WS08

Bajo cada UF se añaden seis campos. Citas: `deskops.md:N`, `infraestructura.md:N` y `ui.md:N` son líneas de `../auditoria/deskops.md` (WS02), `../auditoria/infraestructura.md` (WS03) y `../auditoria/ui.md` (WS04); `dag.yaml` se cita por nodo y solo para verificar IDs y alcance. «hueco» = la operación no existe o no está auditada; lleva repo dueño (`owner_repo` del nodo) y productor (ID de nodo del DAG, o «sin productor en el DAG»). En Error, «no definido» lleva su productor. Operación, Nodo y Gate admiten listas completas; ninguna es «principal». Las operaciones listadas son las auditadas, no un compromiso de que la UI las exponga: lo que la UI expone lo fija WS11/WS12. Gate humano = WS16, WS30, WS37, WS39 o «ninguno adicional» (`validacion-humana.md`); WS29 es prueba técnica propia, no gate humano. G_PRODUCT satisfecho es base de plan, no aceptación de producto. Taller es corpus futuro de WS40, no producto operativo. Estos campos no acreditan capacidades implementadas.

## UF01 — Entrar a un proyecto desconocido

Abrir entrada del ecosistema -> elegir proyecto -> leer entrada del desk -> seguir enlaces a conocimiento, trabajo y procedimientos -> abrir documentos al lado -> volver sin perder selección.

Aceptación: explicar propósito, superficies y trabajo actual sin rutas memorizadas. Ante proyecto no accesible o referencia rota, mostrar origen y conservar navegación.

**Entrada:** proyecto elegido en la entrada del ecosistema; entrada del desk (P09: `desk/README.md` + mapa authored, `decisiones.md` fila P09); enlaces `[[doc]]` y referencias de campo; selección actual y historia.
**Salida:** documento con su contexto (enlaces entrantes, vecindad), procedimientos y trabajo actual, abiertos al lado; error visible con origen cuando el proyecto o la referencia falla; navegación y selección conservadas.
**Operación:**
- Catálogo y lectura de nodo/contexto: `GET /api/workspace/nodes`, `workspace_node` (`ui.md:54-56`, base parcial).
- Vecindad 1-2 saltos y tarjetas que reorientan el workspace (`ui.md:69`); URL/`popstate` (`ui.md:57`).
- Payload y campos de un documento: `sldb docs show`, `sldb fields show` (`infraestructura.md:30`).
- Enlaces `[[doc]]`, `[[doc#Sección]]`: `sldb docs recover`, `GET /lint` (`infraestructura.md:88`); auditoría de enlaces (`infraestructura.md:91`); aristas por campo: `sldb edges show`, `GET /edges` (`infraestructura.md:92`).
- Trabajo y procedimientos: `deskops list tasks`, `show task`, `show board`, `list rituals`/`show ritual`, `next` (`deskops.md:76,87,90,78,89,74`); lectura Board/tarea en UI (`ui.md:67`, base parcial WS22).
- hueco: pestañas/divisiones por documento y foco compartido entre representaciones (`ui.md:57`); dueño graph_ui, productor WS13.3 (y WS13.1).
- hueco: Markdown no modelado del desk como documento navegable (`ui.md:55-56`; el universo tiene 118 archivos no modelados, `deskops.md:226`); dueño graph_ui, productor WS13.2.
- hueco: entradas/índices authored del desk; dueño deskops, productor WS17 (publicación real: WS43).
**Error:**
- Referencia rota: `sldb docs recover` informa los destinos (`infraestructura.md:88`); problemas por nodo en el panel Context (`WR._check_problems_for_node`, `WM.formatProblems`, `ui.md:60`).
- Store no disponible: la ruta de nodo responde 503 «El store no está disponible.» (`ui.md:61`).
- Errores de catálogo, nodo y proyección con mensaje propio (`ui.md:60`); fallo de carga CDN (`esm.sh`) sin manejo observado (`ui.md:60`).
- no definido: contrato de errores de API y estados de red/proyecto no accesible; productor WS11 (consumido por WS15.1).
**Nodo:** WS01, WS02, WS03, WS04, WS07, WS08, WS11 (preparación/contrato); WS13 (WS13.1, WS13.2, WS13.3), WS14, WS15 (WS15.1, WS15.2), WS17 (implementación o handoff); WS40 (corpus); WS43 (publicación real, no gate); WS16, WS30 (aceptación).
**Gate humano:** WS16; WS30 (prueba UF01 con las entradas enriquecidas de WS17, `validacion-humana.md`).

## UF02 — Capturar y aclarar una intención

Capturar idea interna en drawer o protoátomo según naturaleza; entrada externa en inbox -> consultar contexto -> ack local o respuesta dentro del mismo desk autorizado (sin envío interdesk) -> dar forma al material -> conservar como conocimiento o autorizar una tarea completa desde el drawer.

Aceptación: no exigir tarea ni ejecución para conservar una idea. El paso a tarea conserva procedencia; no inventa campos para suplir falta de claridad. No confundir ack con aceptación del trabajo.

**Entrada:** idea interna (drawer o protoátomo según naturaleza); nota externa recibida en el inbox; pregunta o respuesta dentro del mismo desk autorizado; borrador de drawer que se quiere autorizar.
**Salida:** idea conservada como conocimiento sin tarea ni ejecución; ack local o respuesta local registrados (ack no es aceptación del trabajo); tarea completa autorizada desde el drawer, con `from_drawer` como procedencia.
**Operación:**
- Leer el inbox: `deskops message list`, `message read` (`deskops.md:39-40`); `list inbox-notes`, `show inbox-note` (`deskops.md:83,94`).
- Consultar contexto: `sldb find`, `fields query` (`infraestructura.md:110-111`); `deskops list pills`/`show pill`, `list atoms` (`deskops.md:77,88,80`).
- Protoátomo/clasificación: `deskops atoms proto`, `atoms type`, `atoms crossroad`, `atoms tree` (`deskops.md:119,120,118,121`).
- Dar forma como conocimiento: `deskops add atom`, `edit atom`, `atoms create` (`deskops.md:55,66,114`).
- Promoción a drawer existente: `deskops promote inbox-to-drawer-task` crea la tarea diferida y borra la nota (`deskops.md:43`). El plan no la aprueba como canal de captura: WS12 compara `message send` + `promote` y no lo aprueba porque la promoción borra la nota (`dag.yaml`, nodo WS12, scope).
- Autorizar tarea completa desde el drawer: `deskops add task --from-drawer` (exige `closeout_evidence`, `deskops.md:51`); `resolve_drawer_source`, `attach_drawer_source` (`deskops.md:166,150`); `deskops drawer remove` rechaza si una tarea registra `from_drawer` (`deskops.md:45`).
- hueco: ack local en la UI. `deskops message ack` existe en CLI (`deskops.md:41`) pero su uso como ack local de esta UF queda pendiente del contrato WS12 y no se da por disponible; dueño deskops, productor WS12 (UI: WS25.1, graph_ui; `ui.md:70-71` ausente).
- hueco: responder dentro del mismo desk (local, sin envío interdesk). No hay operación auditada que lo defina; `message send` entrega a un desk destino (`deskops.md:38`) y no se afirma como respuesta local. Dueño deskops, productor WS12 (contrato) y WS25.1 (UI).
- hueco: captura directa a drawer y a protoátomo desde la UI; `quick-create-dialog.js` crea documentos en el KB map con destino distinto y no se afirma equivalente (`ui.md:72`). Dueño graph_ui, productor WS25.2, sobre contrato WS12.
**Error:**
- `message read` con nombre ambiguo = UsageError (`deskops.md:40`); `message ack` revierte el archivo si falla el tracking (`deskops.md:41`).
- `add task` sin evidencia declarada o inferible falla (`deskops.md:51`); edición de campo: id inmutable y el modelo se niega a reescribir lo que no puede leer (`deskops.md:62`).
- no definido: errores de captura, ack y respuesta local expuestos a la UI; productor WS12 (UI: WS25).
**Nodo:** WS02, WS08, WS12 (preparación/contrato); WS25 (WS25.1, WS25.2); WS30 (aceptación).
**Gate humano:** WS30.

## UF03 — Trabajar conocimiento

Buscar por texto/campos/significado -> abrir átomo y fuentes -> comparar con relacionados -> editar, vincular, dividir o reunir mediante operaciones públicas -> consultar materializaciones, validar contratos soportados y leer impacto.

Aceptación: fuente y representación apuntan al mismo documento; las composiciones escriben al origen correcto. El conflicto conserva la edición del usuario y permite revisar; el conocimiento no exige lanzar agentes.

**Entrada:** texto, campos o significado a buscar; documento/átomo elegido; edición del usuario; operación de dividir, reunir o vincular.
**Salida:** resultados navegables; átomo con fuentes y relacionados; documento editado o conflicto que conserva la edición para revisarla; materializaciones con procedencia, validación e impacto.
**Operación:**
- Búsqueda por texto/campos: `sldb find`, `sldb fields query`, `sldb sections find`, `sldb explore` (`infraestructura.md:110-113`); por forma/lenguaje natural: `pron say`, `pron eval` (`infraestructura.md:117`); filtro local de catálogo en UI (`ui.md:58`).
- hueco: búsqueda por significado (similitud): `Corpus.rank`/`GET /corpus/rank` sin CLI (`infraestructura.md:115`); dueño sldb, sin productor en el DAG.
- hueco: búsqueda por API desde la UI y estados sin resultado/error (`ui.md:58`); dueño graph_ui, productor WS14.
- Abrir átomo y fuentes: `deskops list atoms`, `show atom`, `atoms show`, `atoms tree` (`deskops.md:80,91,112,121`).
- Relacionados: `sldb graph query|neighborhood|path|similar`, `GET /graph/*` (`infraestructura.md:114`); `sldb edges show` (`infraestructura.md:92`); vecindad en UI (`ui.md:69`).
- Editar campos: `deskops edit atom` (`deskops.md:66`); `sldb docs update`, `sldb fields update/append/remove` (`infraestructura.md:31`); `POST /save` con `expected` y 409 (`infraestructura.md:51`); `kb_doc_edit` (`infraestructura.md:34`). En UI solo existe en el KB map, no en el workspace (`ui.md:63-64`).
- Vincular: `ConnectDialog` (alta de relación sobre campos de referencia, `ui.md:65`); `sldb edges init`, `RelationDoc` (`infraestructura.md:93`); `kb_edge_assert` (`infraestructura.md:97`).
- Dividir y reunir: `deskops atoms split`, `atoms merge`, `atoms delete`, `atoms reorganize` (`deskops.md:116,117,115,111`). En UI: ausente (`ui.md:88`), productor WS42.
- Materializaciones: `deskops list materializations`, `show materialization` (`deskops.md:81,92`); `MaterializationContractDoc` (`deskops.md:190`); transclusión `sldb docs compose` (`infraestructura.md:90`); `deskops drift check` incluye superficies de conocimiento (`deskops.md:129`).
- Validar contratos soportados: `deskops atoms validate` (puede crear andamiaje, `deskops.md:113,266`); `sldb stores check` (usado por `doctor`; interior no leído, `deskops.md:265`).
- Impacto: `deskops graph neighbors`, `graph missing` (`deskops.md:124-125`); `sldb edges check|unresolved` (`infraestructura.md:92`); Changes/Integrity en UI: ausente (`ui.md:80`), productor WS29.
- hueco: guardado de Markdown en bruto con revisión esperada y buffer recuperable (`infraestructura.md:33,54`); dueño sldb, productor WS20 (G_SOURCE). hueco: precondición de escritura de payload por campos; dueño sldb, productor WS45 (G_PAYLOAD_PRECONDITION). hueco: edición en el workspace con conflicto visible; dueño graph_ui, productor WS19 (WS19.1, WS19.2) y WS21 (fuente según `source_mode`).
**Error:**
- 409 por `expected` en `POST /save`; compara el payload completo, no un hash (`infraestructura.md:51,163`); la forma legacy `POST /save {doc,payload}` no verifica: última escritura gana (`infraestructura.md:53`); lote parcial responde 500 con `completed` y sin rollback (`infraestructura.md:52`); editor externo del Markdown no detectado por el guardado (`infraestructura.md:56`).
- `atoms delete` rechaza si hay referencias entrantes (`deskops.md:115`); diálogo de conflicto del KB map (`ui.md:64`).
- no definido: contrato de fallos parciales, permisos y conflicto para la UI del workspace; productor WS12.
**Nodo:** WS02, WS03, WS09, WS11, WS12 (preparación/contrato); WS13, WS14, WS19, WS21, WS24, WS42 (implementación); WS20, WS45 (precondiciones de escritura citadas arriba); WS29 (extensión de impacto/Changes; no es prerrequisito del lector ni del manual básico); WS16 (lectura), WS30 (edición).
**Gate humano:** WS16 (lectura); WS30 (edición).

## UF04 — Preparar trabajo activo

Recuperar candidato -> definir objetivo, alcance, dependencias, validación y evidencia -> localizar contexto reusable -> vincular pills/átomos y rituales -> autorizar task -> enrutamiento en Board -> identificar capa lista sin solapamiento.

Aceptación: distinguir pendiente de activo y de listo para ejecutar. No convertir automáticamente un fragmento incompleto del drawer. La fase es dependencia operativa, no categoría de negocio.

**Entrada:** candidato del drawer; objetivo, alcance, dependencias, validación y evidencia declarada; pills/átomos/rituales a vincular; Board.
**Salida:** tarea autorizada y enrutada en el Board con contexto vinculado; distinción visible entre pendiente, activo y listo para ejecutar; commit de promoción por canal autorizado externo.
**Operación:**
- Recuperar candidato y tareas: `deskops list tasks` (con `--include-repos` lee Boards de repos registrados), `show task` (`deskops.md:76,87`); `edit task` también sobre candidatas del drawer (`deskops.md:62`).
- Localizar contexto reusable: `deskops list pills`/`show pill`, `list rituals`/`show ritual`, `list atoms` (`deskops.md:77,88,78,89,80`); `sldb find` (`infraestructura.md:110`).
- Crear/vincular: `deskops add pill`, `bind pill` (`deskops.md:52,73`); `add task` (exige `closeout_evidence`; `--from-drawer`) que escribe la tarea y la agrega al Board en una transacción (`deskops.md:51,154`).
- Enrutar y leer capa: `deskops add board`/`edit board` (`deskops.md:54,65`); `deskops next` y `next_action_report` (`deskops.md:74,163`); `advance task` (`deskops.md:98`).
- Lectura en UI: `GET /api/desk/board`, `/api/desk/task` (`ui.md:67`, base parcial).
- hueco: autoría de tarea, evidencia y contexto desde la UI, enrutado en Board y capa lista sin solapamiento (`ui.md:73-75` ausente); `deskops.md` no audita un cálculo de «capa lista sin solapamiento». Dueño graph_ui, productor WS26 (WS26.1, WS26.2), sobre contrato WS12.
- hueco: vincular rituales a una tarea. `deskops bind` solo audita `bind pill` (`deskops.md:72-73`); no se afirma operación de vínculo de rituales. Dueño deskops, productor WS12.
- hueco: tablero agrupado, dependencias navegables, apertura de TaskDoc en el lector (`ui.md:67`); dueño graph_ui, productor WS22.
**Error:**
- `add task` falla sin evidencia declarada o inferible (`deskops.md:51`); `edit task`: id inmutable (`deskops.md:62`); `drawer remove` rechaza fragmentos ya referenciados por `from_drawer` (`deskops.md:45`).
- `POST /api/desk/advance` responde 409 ante revisión obsoleta de Board o tarea (`ui.md:79`).
- no definido: errores de autoría y enrutamiento para la UI; productor WS12.
**Nodo:** WS02, WS08, WS12 y G_CLOSEOUT (preparación/contrato); WS22, WS26 (WS26.1, WS26.2) (implementación); commits de promoción vía canal autorizado externo; WS30 (aceptación).
**Gate humano:** WS30.

## UF05 — Ejecutar manualmente y revisar

Abrir tarea con contexto y procedimiento -> hacer trabajo -> reunir cambios/evidencia -> comparar con contrato -> pedir corrección o completar obligaciones -> cierre vía autoridad Deskops -> revisar conocimiento durable y fase.

Aceptación: ninguna acción usa edición arbitraria de status para saltarse gates. Distinguir declarado, encontrado y verificado. Reabrir enlaces durante revisión no pierde el encargo.

**Entrada:** tarea abierta con contexto y procedimiento; cambios y evidencia reunidos; correcciones pedidas.
**Salida:** estado de la tarea con evidencia declarada, encontrada y verificada; diff comparable con el contrato; cierre ejecutado por Deskops fuera de HTTP y refresco que lo verifica; conocimiento durable y fase revisados.
**Operación:**
- Abrir tarea y siguiente paso: `deskops show task`, `next` (`deskops.md:87,74`); procedimiento: `deskops list rituals`/`show ritual` (`deskops.md:78,89`).
- Preparar corrida/registro: `deskops runtime template --task --agent` escribe un RunDoc (`deskops.md:142`); el cierre con `--run-dir` exige `board.txt`, `task.txt`, `git-status.txt` y `result-summary.md` (`deskops.md:131`).
- Verificar evidencia: `deskops closeout verify` (declarada vs references/files; informe con `declared`, `found`, `alerts`, `gates`, `findings`; `deskops.md:134,171,259`).
- Cerrar: `deskops closeout commit` (rutas `--run-dir` o `--no-run --reason`, `deskops.md:131,260`); `closeout supersede`, `closeout retire` (`deskops.md:132-133`); `advance task` sin `--to` sigue el grafo de lifecycle y llegar a `complete` no se persiste (`deskops.md:98`).
- UI actual: detalle con gates, «Evidencia declarada» y botón Avanzar; el texto dice que el cierre se gestiona desde el CLI (`ui.md:67,68,78,79`).
- hueco: diff Git por repo y tarea (`ui.md:77`; `_inspect_file_reference` no es diff); dueño graph_ui, productor WS27.1.
- hueco: evidencia encontrada y verificada en UI, apertura de soporte (`ui.md:78`); dueño graph_ui, productor WS27.2.
- hueco: `closeout verify` por UI, handoff de cierre y refresco tras cierre externo (`ui.md:79`); dueño graph_ui, productor WS28.
- hueco: reabrir enlaces sin perder el encargo (`ui.md:57`, historia/pestañas); dueño graph_ui, productor WS13.3.
- hueco: renderer de RitualDoc/StepDoc y procedimientos (`ui.md:68`); dueño graph_ui, productor WS23.
**Error:**
- `closeout verify` emite alertas y findings; exit 0 solo si ok (`deskops.md:134`); `closeout commit` exige evidencia según la ruta elegida (`deskops.md:260`); evidencia fuera del vocabulario cerrado `tests, commit, atom, materialization, document, external` (`deskops.md:259`).
- `advance task --to` fuerza status o `current_node` (`deskops.md:98`) y `edit task` cambia campos (`deskops.md:62`): la aceptación de la UF exige no usarlos para saltarse gates; la whitelist de campos protegidos la define WS12 (`dag.yaml`, nodo WS12).
- no definido: contrato de error de cierre y de handoff para la UI; productor WS12 (UI: WS28).
**Nodo:** WS02, WS08, WS12 y G_CLOSEOUT (preparación/contrato); WS13.3, WS23, WS27 (WS27.1, WS27.2), WS28 (implementación); closeout CLI/coordinador externo; WS30 (aceptación). No se promete cierre HTTP.
**Gate humano:** WS30.

## UF06 — Delegar e intervenir

Preparar bundle -> registrar intento y dispatch confirmado -> seguir ejecución -> recibir pregunta con referencias -> responder/decidir -> consultar resultado y evidencia -> revisar/corregir -> cerrar mediante workflow.

Aceptación: cada mensaje/resultado corresponde al intento correcto; completado por agente no implica aprobado. Requiere ramal Scion real y no bloquea UF01–UF05.

**Entrada:** tarea y bundle de contexto a delegar; autorización explícita del humano; preguntas del agente con referencias; decisión humana.
**Salida:** intento registrado con dispatch confirmado; mensajes y resultados vinculados al intento correcto; decisión humana registrada; resultado y evidencia para revisar; cierre por workflow Deskops. Completado por agente no implica aprobado.
**Estado:** delegación condicionada a G_SCION (`unverified`) y G_EXEC (`pending`); este borrador no la habilita ni autoriza dispatch, mensajes o acceso Scion. No bloquea UF01–UF05.
**Operación:**
- Auditadas, solo soporte local, no dispatch Scion: `deskops runtime template` (plantilla de agente y RunDoc, `deskops.md:142`), `runtime workers` (`deskops.md:140`), `runtime supervise` (bloquea sobre un agente e informa; nunca responde ni avanza tareas, `deskops.md:141`).
- UI: trazabilidad tarea-intento-mensaje, adaptador de despacho e intervención ausentes (`ui.md:82-84`); el panel de workers adyacente no se afirma que cubra el alcance (`ui.md:82`).
- hueco: preparar el bundle de contexto para delegar. `create_task_bundle` existe, pero escribe y rutea una tarea (`deskops.md:51,154`), no un bundle de delegación; el DAG no nombra uno. Dueño deskops, sin productor en el DAG.
- hueco: identidad de intento y dispatch confirmado; dueño deskops, productor WS32 (WS32.1, WS32.2).
- hueco: vincular mensajes, resultados y decisión humana al intento; dueño deskops, productor WS33 (WS33.1, WS33.2).
- hueco: exponer dispatch y respuesta autorizados; dueño deskops, productor WS34 (WS34.1, WS34.2).
- hueco: seguimiento, pregunta/respuesta e intervención en la UI; dueño graph_ui, productor WS35, WS36.
- hueco: contrato público y acceso a Scion; no auditado en `deskops.md`, `infraestructura.md` ni `ui.md`; dueño deskops, productor WS44 (gate G_SCION).
**Error:**
- no definido: fallos de dispatch, intento duplicado/no idempotente, respuesta a intento equivocado; productor WS32, WS33, WS34.
- no definido: fallo de acceso a Scion; productor WS44.
**Nodo:** WS05, WS11, WS12, WS44 y G_SCION/G_EXEC (preparación/contrato); WS32, WS33, WS34, WS35, WS36 (implementación); WS37 (aceptación); WS38 (publicación de capítulos verificados).
**Gate humano:** WS37 (requiere G_EXEC; no se ejecuta solo porque el DAG esté revisado).

## UF07 — Diagnosticar y mantener

Abrir diagnóstico -> identificar documento/ancla/relación afectada y causa -> inspeccionar soporte -> corregir o registrar trabajo -> reevaluar -> conservar procedencia.

Aceptación: se distingue error, conflicto, cambio y pérdida de soporte. Las operaciones de reparación muestran alcance; no recrean silenciosamente evidencia ausente.

**Entrada:** documento, ancla o relación sospechosa; hallazgo de un comando de diagnóstico; fallo de backend o dependencia; cambio real en el store.
**Salida:** diagnóstico que distingue error, conflicto, cambio y pérdida de soporte, con documento afectado y causa; reparación o trabajo registrado, con alcance visible; reevaluación y procedencia conservada; modo degradado que dice qué falla sin fingir vacío.
**Operación:**
- Diagnóstico: `deskops doctor` (`mutates=True`; usa `sldb stores check`), `deskops status` (alias deprecado) (`deskops.md:31-32`); `deskops drift check` (`deskops.md:129`); `deskops desk update` (informe sin `--apply`, `deskops.md:107`); `deskops graph missing` (`deskops.md:125`); `deskops atoms validate` (`deskops.md:113`).
- Enlaces y aristas: `sldb docs recover --all`, `GET /lint` (`infraestructura.md:88,91`); `sldb edges check|unresolved` (`infraestructura.md:92`); anclas: `sldb anchors check` (`infraestructura.md:94`); historia: `sldb docs history` (`infraestructura.md:60`).
- Cambios e impacto (WS29): `sldb stores check`, `deskops doctor`, `deskops drift check` y relaciones a 1 salto (`dag.yaml`, nodo WS29, scope/acceptance); en UI hay problemas por nodo (`WR._check_problems_for_node`, `ui.md:60,80`). hueco: vista Changes/Integrity (`ui.md:80`); dueño graph_ui, productor WS29.
- Modo degradado: errores de catálogo/nodo/proyección (`ui.md:60`); 503 de store no disponible (`ui.md:61`). hueco: diagnóstico de fallo CDN y reintento que conserve foco/historia (`ui.md:60`); backend caído y modelo no importable, exigidos por WS15.1 (`dag.yaml`, nodo WS15.1), sin línea de auditoría que los cubra. Dueño graph_ui, productor WS15.1.
- Inspeccionar soporte: `deskops show task`/`show atom`, `list tasks` (`deskops.md:87,91,76`); `sldb docs show` (`infraestructura.md:30`).
- Reparación por operaciones existentes, sin botón universal: `sldb edges rebuild` (`infraestructura.md:116`), `sldb anchors record` (`infraestructura.md:94`), `deskops desk update --apply`, `desk migrate`, `desk replace`, `retire` (`deskops.md:107,105,106,46`), `edit task`/`edit atom` (`deskops.md:62,66`). Registrar trabajo de corrección: `deskops add task` (`deskops.md:51`).
- Archivo no modelado no es corrupción: el universo tiene 118 archivos no modelados, p. ej. `desk/contexts/README.md` (`deskops.md:218,226`).
- hueco: criterio visible que separe error, conflicto, cambio y pérdida de soporte; no auditado; dueño graph_ui, productor WS29 (cambio) y WS15.1 (error); contrato WS11.
**Error:**
- `sldb stores check` puede escribir caché o journal: no se leyó (`deskops.md:265`); `desk update` y `atoms validate` pueden crear andamiaje (`deskops.md:266`); `anchors` requiere el extra `[code]` (`infraestructura.md:94`).
- Escritor externo no detectado por el guardado (`infraestructura.md:56`); `drift check` termina con exit 1 si hay hallazgos (`deskops.md:129`).
- no definido: errores de API y estados de red para backend ausente; productor WS11. no definido: fallos parciales de una reparación; productor WS12.
**Nodo:** WS03, WS08, WS11, WS12 (preparación/contrato); WS15 (WS15.1, WS15.2), WS29 (implementación); reparación externa documentada; WS16 (aceptación del diagnóstico).
**Gate humano:** WS16 (diagnóstico de link roto y backend ausente). WS29 es prueba técnica propia (mutación real en store temporal) y su ausencia no bloquea el manual básico; no es gate humano.

## UF08 — Cambiar de proyecto

Seguir referencia de otro desk -> resolver identidad y contexto de store -> leer destino -> volver (envío interdesk queda fuera de baseline) -> conservar proyecto origen y destino.

Aceptación: no escribir en otro desk por confusión de cwd ni copiar documentos ajenos para aparentar navegación federada.

**Entrada:** referencia de otro desk con alias o raíz explícitamente autorizados; identidad de origen y destino.
**Salida:** documento destino leído con proyecto y store visibles; retorno por la historia al origen; origen y destino conservados. Solo lectura: sin envío ni mutación en el destino.
**Operación:**
- Identidad y registro de repos: `deskops repo whoami`, `repo register`, `list repositories`, `show repository` (`deskops.md:101,100,82,93`); `deskops list tasks --include-repos` lee el Board de repos registrados (`deskops.md:76,160`).
- Resolución a otro store: `sldb stores add|list`, `sldb docs exists` (`infraestructura.md:96`).
- Lectura del destino: `sldb docs show` (`infraestructura.md:30`) y la navegación de UF01.
- hueco: lectura entre desks en la UI con aliases autorizados (`ui.md:87`: una sola raíz, sin aliases ni lectura cruzada); dueño graph_ui, productor WS41 (con WS13, WS14, WS15).
- Excluido del baseline: `deskops message send` (entrega a otro desk, `deskops.md:38`) no forma parte de UF08; sin excepción implícita a P07 (`decisiones.md` fila P07).
**Error:**
- Alias no autorizado, path escapado y store ausente deben dar error visible (`dag.yaml`, nodo WS41, acceptance); la forma del error no está definida: no definido, productor WS11.
**Nodo:** WS03, WS08, WS11 (preparación/contrato); WS41, con WS13, WS14, WS15 (implementación); WS40 (dos desks temporales); WS16 (aceptación).
**Gate humano:** WS16 (lectura). El envío cruzado está fuera de alcance.

## UF09 — Inspeccionar y cambiar un contrato de modelo

Desde un documento -> abrir Schema/clase origen -> inspeccionar campos/referencias/template -> editar draft por APIs existentes -> validar -> promover solo con autoridad y evidencia -> diagnosticar impacto. No editar modelos por payload libre ni prometer soporte no disponible. WS39 implementa el delta y valida este flujo por separado.

**Entrada:** documento activo; Schema/clase origen; cambio de campo, referencia o template en un draft del modelo.
**Salida:** contrato del modelo inspeccionado; draft editado y validado; promoción solo con autoridad y evidencia; impacto diagnosticado. No se edita por payload libre ni se promete soporte no disponible.
**Operación:**
- Inventario de modelos: `sldb models list --store .sldb` (17 modelos, `deskops.md:181`); filas por modelo (`deskops.md:185-201`); modelos no registrados: `deskops doctor`, `desk update` (`deskops.md:31,107`).
- Editor de Schema existente: `MS` (`template_edit`, `fields_add`, `fields_remove`, `validate`, `promote`), `POST /api/models/*`, `class-dialog.js`, `views/models/diagram/` (`ui.md:85`, base parcial).
- hueco: acceso al Schema/clase origen desde el panel Context del lector (`ui.md:85`: «Ausente»); dueño graph_ui, productor WS39.
- hueco: no hay comando deskops que cree o edite RoleDoc ni RuntimeProfileDoc (`deskops.md:197,199`); no se promete edición de esos modelos desde UF09; dueño deskops, sin productor en el DAG.
- Impacto: ver UF07 (`sldb edges check`, `deskops drift check`; `infraestructura.md:92`, `deskops.md:129`); hueco: Changes/impacto avanzado (`ui.md:80`), productor WS29.
**Error:**
- no definido: efectos y errores de draft/validate/promote ante autoridad faltante; productor WS12 (contrato) y WS39 (prueba); WS39 no habilita promover si la API o la autoridad falta (`dag.yaml`, nodo WS39, acceptance).
**Nodo:** WS03, WS04, WS09, WS12 (preparación/contrato); WS39 (reutiliza Schema/editar clases; requiere WS12, WS13, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT); WS29 (impacto avanzado, opcional y propuesto según evidencia); no bloquea WS31.
**Gate humano:** WS39 (prueba humana específica; G_HUMAN_MODEL).

## UF10 — Arranque y ausencia de desk

Seguir instrucciones reproducibles de instalación/arranque -> abrir ejemplo Taller -> si no hay desk, mostrar orientación e invocación init CLI con destino explícito -> refrescar tras resultado real. No ejecutar inicialización por un GET ni mutar el proyecto equivocado.

**Entrada:** instrucciones de instalación/arranque; ruta de un repo sin desk; destino explícito para inicializar; resultado real de la invocación.
**Salida:** arranque reproducible; ejemplo Taller abierto; en ausencia de desk, orientación con la invocación `deskops init <ruta>` y destino explícito; refresco tras un resultado real. Ninguna inicialización por un GET.
**Operación:**
- Inicialización por CLI: `deskops init` (crea `.sldb`, registra modelos, arma `desk/` y lifecycle; `ensure_target_directory`, `deskops.md:35`); `deskops desk install` (`deskops.md:104`); `deskops bootstrap` (puede instalar sldb con pip y crear `~/.sldb`, `deskops.md:34`).
- Estado tras iniciar: `deskops doctor` (`deskops.md:31`); lectura de nodos en UF01.
- Sin store: la ruta de nodo responde 503 «El store no está disponible.» (`ui.md:61`).
- hueco: orientación de proyecto sin desk con la invocación `deskops init <ruta>` (`ui.md:61`: grep sin resultados); dueño graph_ui, productor WS15.2.
- hueco: instrucciones reproducibles de instalación/arranque y ejemplo Taller (`ui.md:86`: sin generador ni fixture); dueño graph_ui, productor WS40.
- hueco: índices/entradas authored; dueño deskops, productor WS17 (publicación: WS43).
**Error:**
- `deskops init` exige destino de directorio resoluble (`deskops.md:35`); `bootstrap`/`init` tocan la máquina (`~/.sldb`, `deskops.md:34-35`): no se invocan desde una lectura.
- no definido: error mostrado al fallar la inicialización o el arranque; productor WS11 (lectura) y WS15.2 (orientación).
**Nodo:** WS02, WS04, WS08, WS11 (preparación/contrato); WS15 (WS15.2), WS40, WS17 (implementación); WS43 (publicación real); WS16 (aceptación).
**Gate humano:** WS16 (arranque).

## Precisiones de revisión

UF04/05 tienen handoff a Git/closeout externo; no se promete cierre HTTP. UF06 requiere WS34/36 para acciones, no solo lectura de mensajes. UF07 reparaciones se hacen por operaciones existentes documentadas, no un botón universal. UF08 inicialmente read-only; una mutación interdesk no es parte implícita de navegar. Captura/archivo no modelado no debe tratarse como corrupción. Matriz de aceptación, nodos y gates: ../cobertura.md y ../validacion-humana.md. Los pasos de intención no acreditan capacidades implementadas.

UF03: WS19 cubre campos y relaciones; WS42 cubre split/merge/tipado existentes. UF04: WS26 incluye enrutamiento y capa lista. UF08 baseline es solo lectura entre desks vía WS41; no se promete enviar ni mutar destino. UF10 usa corpus de WS40. Los gates de uso siguen validacion-humana.md, no el simple cierre de una tarea de código.

UF03 no promete generar destinos arbitrarios desde una materialización: la entrega soporta inspección/procedencia y operaciones existentes comprobadas. Generación nueva de docs/diagramas exige su contrato del repo dueño. WS43 publica navegación real tras validar el ejemplo; no basta considerar el corpus como ecosistema final.
