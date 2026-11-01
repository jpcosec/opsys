FILE:desk/tasks/task-completar-productores-en-los-campos-nodo-de-ws08.md
---
id: task-completar-productores-en-los-campos-nodo-de-ws08
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/cobertura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261101-ws08-completitud/review-source.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/cobertura.md
- runs/subagents/20261101-ws08-completitud/completeness-matrix.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-completar-productores-en-ws08.md
closeout_evidence:
- commit
- document
---

# Completar productores en los campos Nodo de WS08

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root no aprobó WS08: la aceptación exige listas completas y los campos Nodo omiten productores que el propio flujo nombra.

## Goal

_Describe the concrete result this task must produce._

Que cada operación o error con productor necesario tenga ese productor en Nodo y en cobertura.md, con matriz que lo demuestre.

## Scope

_State what is in scope and what is out of scope._

Una sola pasada documental sobre desk/drawer/plans/workspace-documental/borradores/user-flows.md y desk/drawer/plans/workspace-documental/cobertura.md, con matriz runs/subagents/20261101-ws08-completitud/completeness-matrix.md. Autoriza: runs/subagents/20261101-ws08-completitud/review-source.md. No se añaden aristas, tareas ni gates: estos productores ya existen. Los textos UF y los gates humanos no cambian. Lista cerrada de cambios.

En user-flows.md, línea **Nodo:** de cada UF:
- UF03: añadir `WS29 (extensión de impacto/Changes; no es prerrequisito del lector ni del manual básico)`.
- UF05: añadir `WS13.3` y `WS23` a la implementación.
- UF06: añadir `WS44` a preparación/contrato.
- UF07: añadir `WS12` a preparación/contrato.
- UF09: añadir `WS29 (impacto avanzado, opcional y propuesto según evidencia; no bloquea WS31)`.
- UF10: añadir `WS11` a preparación/contrato.
- UF01: Nodo no cambia. WS22 es base existente citada, no productor necesario: no añadir bloqueo a WS16.

En user-flows.md, línea **Operación:**:
- UF05: `list ritual`/`show ritual` pasa a `deskops list rituals`/`show ritual` (forma auditada en deskops.md:78).
- UF05: añadir un hueco: renderer de RitualDoc/StepDoc y procedimientos (`ui.md:68`); dueño graph_ui, productor WS23.
- Ninguna otra línea cambia. WS23 no se añade al gate básico WS16 de UF01.

En cobertura.md, filas de la tabla, sin cambiar la columna Gate de aceptación salvo donde se indica:
- UF03, implementación: añadir `WS20/45 precondiciones; WS29 extensión de impacto, no prerrequisito`.
- UF05, implementación: añadir `WS13.3`, `WS23`.
- UF06, preparación: añadir `WS44`. Gate de aceptación: tras WS37 añadir `; WS38 publicación`.
- UF07, preparación: añadir `WS12`.
- UF08, implementación: añadir `WS40 corpus`.
- UF09, implementación: añadir `WS13 lector; WS29 impacto avanzado, opcional`.
- UF10, preparación: añadir `WS11`. Implementación: añadir `WS43 publicación real`.

Matriz, en runs/subagents/20261101-ws08-completitud/completeness-matrix.md: una tabla por UF, una fila por cada WS citado en Operación o Error: ID, dónde se cita, clase (productor necesario, extensión opcional, citación contextual o fuera de alcance), si está en Nodo, si está en cobertura.md. Un agregado cubre a sus hijos. No se enumeran dependencias transitivas ni IDs citados solo para decir que quedan fuera.

Si la matriz muestra otro productor necesario ausente, NO se edita: se anota en result-summary.md para el Supervisor.

No editar manual.md, decisiones.md, la guía, dag.yaml, helper, validadores ni código. Los huecos de bundle (UF06) y Corpus.rank se conservan: son honestos y no llevan productor inventado. Roles: el Executor escribe solo user-flows.md, cobertura.md, la matriz y runs/subagents/20261101-ws08-completitud/result-summary.md. No hay commits ni corrida de revisiones del Executor. Sin preguntar al solicitante. Fuera de alcance: WS09, WS11, WS12 como tareas, UI, Scion, push, suite general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Aplicar la lista cerrada. 2. Escribir la matriz leyendo las 10 UF. 3. Escribir runs/subagents/20261101-ws08-completitud/result-summary.md. 4. El Supervisor congela y entrega diff y hashes a root antes de renovar revisiones.

## Validation

_List the checks required before this task can close._

- grep -c "^## UF" desk/drawer/plans/workspace-documental/borradores/user-flows.md
- test -s runs/subagents/20261101-ws08-completitud/completeness-matrix.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws08-completitud/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: todos los cambios de la lista aplicados y ninguno más; matriz sin productor necesario ausente; Tester independiente PASS; root comprueba la congelación; revisiones renovadas; build --check, validate --check y status en verde.

FILE:desk/drawer/plans/workspace-documental/borradores/user-flows.md
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
**Nodo:** WS02, WS03, WS09, WS11, WS12 (preparación/contrato); WS13, WS14, WS19, WS21, WS24, WS42 (implementación); WS20, WS45 (precondiciones de escritura citadas arriba); WS16 (lectura), WS30 (edición).
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
- Abrir tarea y siguiente paso: `deskops show task`, `next` (`deskops.md:87,74`); procedimiento: `list ritual`/`show ritual` (`deskops.md:78,89`).
- Preparar corrida/registro: `deskops runtime template --task --agent` escribe un RunDoc (`deskops.md:142`); el cierre con `--run-dir` exige `board.txt`, `task.txt`, `git-status.txt` y `result-summary.md` (`deskops.md:131`).
- Verificar evidencia: `deskops closeout verify` (declarada vs references/files; informe con `declared`, `found`, `alerts`, `gates`, `findings`; `deskops.md:134,171,259`).
- Cerrar: `deskops closeout commit` (rutas `--run-dir` o `--no-run --reason`, `deskops.md:131,260`); `closeout supersede`, `closeout retire` (`deskops.md:132-133`); `advance task` sin `--to` sigue el grafo de lifecycle y llegar a `complete` no se persiste (`deskops.md:98`).
- UI actual: detalle con gates, «Evidencia declarada» y botón Avanzar; el texto dice que el cierre se gestiona desde el CLI (`ui.md:67,68,78,79`).
- hueco: diff Git por repo y tarea (`ui.md:77`; `_inspect_file_reference` no es diff); dueño graph_ui, productor WS27.1.
- hueco: evidencia encontrada y verificada en UI, apertura de soporte (`ui.md:78`); dueño graph_ui, productor WS27.2.
- hueco: `closeout verify` por UI, handoff de cierre y refresco tras cierre externo (`ui.md:79`); dueño graph_ui, productor WS28.
- hueco: reabrir enlaces sin perder el encargo (`ui.md:57`, historia/pestañas); dueño graph_ui, productor WS13.3.
**Error:**
- `closeout verify` emite alertas y findings; exit 0 solo si ok (`deskops.md:134`); `closeout commit` exige evidencia según la ruta elegida (`deskops.md:260`); evidencia fuera del vocabulario cerrado `tests, commit, atom, materialization, document, external` (`deskops.md:259`).
- `advance task --to` fuerza status o `current_node` (`deskops.md:98`) y `edit task` cambia campos (`deskops.md:62`): la aceptación de la UF exige no usarlos para saltarse gates; la whitelist de campos protegidos la define WS12 (`dag.yaml`, nodo WS12).
- no definido: contrato de error de cierre y de handoff para la UI; productor WS12 (UI: WS28).
**Nodo:** WS02, WS08, WS12 y G_CLOSEOUT (preparación/contrato); WS27 (WS27.1, WS27.2), WS28 (implementación); closeout CLI/coordinador externo; WS30 (aceptación). No se promete cierre HTTP.
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
**Nodo:** WS05, WS11, WS12 y G_SCION/G_EXEC (preparación/contrato); WS32, WS33, WS34, WS35, WS36 (implementación); WS37 (aceptación); WS38 (publicación de capítulos verificados).
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
**Nodo:** WS03, WS08, WS11 (preparación/contrato); WS15 (WS15.1, WS15.2), WS29 (implementación); reparación externa documentada; WS16 (aceptación del diagnóstico).
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
**Nodo:** WS03, WS04, WS09, WS12 (preparación/contrato); WS39 (reutiliza Schema/editar clases; requiere WS12, WS13, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT); no bloquea WS31.
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
**Nodo:** WS02, WS04, WS08 (preparación/contrato); WS15 (WS15.2), WS40, WS17 (implementación); WS43 (publicación real); WS16 (aceptación).
**Gate humano:** WS16 (arranque).

## Precisiones de revisión

UF04/05 tienen handoff a Git/closeout externo; no se promete cierre HTTP. UF06 requiere WS34/36 para acciones, no solo lectura de mensajes. UF07 reparaciones se hacen por operaciones existentes documentadas, no un botón universal. UF08 inicialmente read-only; una mutación interdesk no es parte implícita de navegar. Captura/archivo no modelado no debe tratarse como corrupción. Matriz de aceptación, nodos y gates: ../cobertura.md y ../validacion-humana.md. Los pasos de intención no acreditan capacidades implementadas.

UF03: WS19 cubre campos y relaciones; WS42 cubre split/merge/tipado existentes. UF04: WS26 incluye enrutamiento y capa lista. UF08 baseline es solo lectura entre desks vía WS41; no se promete enviar ni mutar destino. UF10 usa corpus de WS40. Los gates de uso siguen validacion-humana.md, no el simple cierre de una tarea de código.

UF03 no promete generar destinos arbitrarios desde una materialización: la entrega soporta inspección/procedencia y operaciones existentes comprobadas. Generación nueva de docs/diagramas exige su contrato del repo dueño. WS43 publica navegación real tras validar el ejemplo; no basta considerar el corpus como ecosistema final.

FILE:desk/drawer/plans/workspace-documental/cobertura.md
# Cobertura de recorridos

| Flujo | Preparación/contrato | Implementación o handoff | Gate de aceptación |
|---|---|---|---|
| UF01 conocer proyecto | WS01–04/07/08/11 | WS13/14/15; WS17 agrega índices authored | WS16 (corpus WS40), WS30 para índices, WS43 publicación real |
| UF02 captura y triage | WS02/08/12 | WS25 | WS30 |
| UF03 conocimiento | WS02/03/09/11/12 | WS13/14/19/21/24/42 | WS16 lectura; WS30 edición |
| UF04 preparar trabajo | WS02/08/12 + G_CLOSEOUT | WS22/26; commits de promoción vía canal autorizado externo | WS30 |
| UF05 revisar y cerrar | WS02/08/12 + G_CLOSEOUT | WS27/28; closeout CLI/coordinador | WS30 |
| UF06 delegar/intervenir | WS05/11/12 + G_SCION/G_EXEC | WS32–36 | WS37 |
| UF07 diagnosticar | WS03/08/11 | WS15; WS29 impacto; reparación externa documentada | WS16 diagnóstico; prueba propia WS29 |
| UF08 otro desk | WS03/08/11 | WS41 lectura multidesk, con WS13/14/15; sin envío interdesk en baseline | WS16 lectura; envío cruzado fuera de alcance |
| UF09 modelos | WS03/04/09/12 | WS39 reutiliza Schema/editar clases | Prueba humana específica WS39; no bloquea WS31 |
| UF10 arranque y proyecto sin desk | WS02/04/08 | WS15 orientación + CLI init documentado; WS40 corpus; WS17 índices | WS16 |

Las filas definen cobertura esperada, no capacidades entregadas. WS08 refina el guion sobre esta matriz; un cambio de nodos requiere actualizarla y validar referencias. Crear un desk desde browser, mover/renombrar, undo destructivo y adjuntos editables quedan explícitamente fuera en alcance.md.

FILE:runs/subagents/20261101-ws08-completitud/review-source.md
# Decisión root sobre el checkpoint WS08/WS10, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-11-01, revisión de HEAD `25f93dd0`. Autorización de trabajo documental local; no es aprobación humana.

Revisión root checkpoint WS08/WS10 HEAD25f93dd0. WS10 APROBADA documentalmente. WS08 NO aprobada aún: hay un defecto acotado de completitud del mapa de productores, no de capacidades/alcance. Fase sigue abierta; no WS09/11/12 niUI.

Checks root independientes: build0, validate0, status all current, helper13passed/1.45s.73 bundles inputbytes/contractjson/SHA/ordered_sources/outputSHA/argv/manifest/receipt completos0errores,73PIDúnicos. DAGfrente85987c4f idéntico quitando soloevidence/input_sha256. Cambiaron exactamente PK06,WS08,WS10,WS16,WS30,WS31,WS37,WS38,WS44;64sinrepetir. Fuentescoinciden con hashes dehandoff. Tres auditoríasrootlectura: UF01–05 todas105agrupacionesdecitas/107líneasúnicas, UF06–10todas68líneasúnicas y nodos/gates; WS10manual17fichas/tresauditorías/manualCLIcompleto. No runtime nihermanos ni suitegeneral.

WS10: precedencia corregida sí aplicada (Scion/modelos/Changes avanzado propuestos),17fichas completas,Tallerfuturo,no disponible ficticio,no consumo delentregableWS08. DosremisionesCLIlocalesausentesenfichas9y11 sonmenores conremisiónglobalexistente: noencargo reescritura ni invalidarWS10 porcosmética. HistoriadeTaskDoccorregidapordisposición sedeclara; futurasTaskDocsdebenentregarconsignasunívocas, no repetirlo como patrón. WS31Pxx=P01–P09,T-Pxxfuentes/precisionesnoIDsaparte: interpretaciónaceptable, conservarnotapromoción. PK06FUTUROimpreciso no cambia quedry-run G_PRODUCTyaregistrado; no requiero reintento porredacción.

DEFECTO WS08: aceptación exige listascompletas; camposNodo omitenproductoresqueelpropioflujo nombra, y cobertura.md reflejaomisiones. Corregir enunaúnicapasadadocumental:
- UF03: incluirWS29 como extensióndeimpacto/Changes yaindicada enOperación. NO volverloprerequisitodellectoro delmanualbásico.
- UF05: incluirhueco rendererRitualDoc/StepDoc/procedimientos de ui.md:68 conproductorWS23 y mapearloenNodo. WS30yaesperaWS23; no añadirseal gatebásicoWS16deUF01. AdemásNodo omiteWS13.3, citadoexplícitamente comoproductordereabrirenlacessinpérdidaenestaUF: incluirlo (oagregadoWS13claramenteentendido).
- UF06: incluirWS44,productordirectodecontrato/acceso yerrorcitadoporOperación/Error.
- UF07: incluirWS12,productordirectodelosfallosparcialesdereparación enError.
- UF09: incluirWS29comoimpactoavanzado ya citado, opcional/propuesto según evidencia, sinbloquearWS31.
- UF10: incluirWS11,productordelcontratoerrorlectura/arranque ya citado.
- UF05: operación `list ritual` corregir a `deskops list rituals`,formaauditadaen deskops.md:78. No hacefaltaprobarCLIporcambiocanónicodocmenor.
Revisar ademásUF01 dondeOperación citaWS22comobaseparcialperoNodo no: distinguirreferenciadebaseexistente deproductornecesario, noañadirautomáticamentenuevo bloqueoaUF16. Revisartodas10UF paraelmismopatrón. Agregadoscubrenhijos; no exigimos enumerartodasdependenciastransitivas ni agregarIDsmencionadossoloparaindicarfueraalcance.

Autoriza tarea correctivaDOCS acotada, capturar/promover/con commits ypreflight/coldbaratos/executor/tester conformeworkflow. Alcance coherente: user-flows.md + cobertura.md y evidencia/mappingcomparación. cobertura.md dice expresamente «un cambio de nodos requiere actualizarla»: sincronizarfilascorregidas,nodejarcontradicción a futurasTaskDocs. No añadiraristas/tareas/gatesdeproducto: estosproductoresyaexisten. Noeditar manual.md,decisiones,guía,helper/validadoresniimplementación. Mantenerroles de WS29técnico ygatehumanos intactos.

Los huecos bundleUF06 yCorpus.rank quedan documentadosHONESTAMENTE: WS08aceptaciónpermite operaciónausente comohueco. No requieren código niproductorinventado paraaprobarWS08. EnramalE resolverbundle coninventario/contrato ydueñorealantesdeconsumirlo; no equiparar create_task_bundle concontextbundle. Semántica no sepromete: WS14permitecapacidaddegradadasegúnAPIreal; noobligar aimplementarranking porsucita.

Antes degastar: prepara parcheTOTALynuevamatrizdecompletitud (operaciones/errores→productores→Nodo/cobertura, distinguiendocitascontextualesyextensiones), Testerfocal queleatodas10UF yfilasafectadas. Congelar ysuministrardiff/hashesarootANTES derenovar. Importante: cobertura.md es fuentecomúnenbundle; cambiarla probablemente invalide73, no5. Medirconhelper,noeludirinvalidación recortando/normalizandofuentes. No lanzar73hasta revisiónfocal delparche; mantengamoslas2fuentescongeladasantesllamadas. Luegoactualizarrevisionesafectadasrealmente/metadata,preservarhistoriayvalidar. No alegaPASSdelmuestreocomo160citasverificadas: root verificóelconjuntoconlímitesindicados.

Siguientepunto:parchedecompletitudlisto para comprobaciónfocal; despuésTester/closeout yrootfase. WS10seconservaaceptada,norehacerporcambiosnodependientes. NO activarWS09/11/12/UI/Scion/push; preservar4dirtyajenos. Nada requiererepreguntar alhumano decisionesyaresueltas.

FILE:desk/rituals/execution.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:19Z'
  authority: generated
  via: update_document
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 1. Confirm the current phase is explicit and that this task belongs to the ready
  dependency layer being executed.
- 1. Open the initialization gate by making the active task, task scope, touched files,
  and validation targets explicit.
- 1. Atomize the work into one coherent deliverable.
- 1. Audit code, docs, tests, and git state before changing anything.
- '1. Run cheap TaskDoc-only preflight under [ritual-context-review](context-review.md)
  in a fresh ephemeral no-tools process: restate objective, list ambiguities and give
  a detailed non-executing dry-run.'
- 1. Store that TaskDoc-only reformulation at `runs/subagents/<run-dir>/preflight.md`.
- 1. Pass the preflight only when the reformulation reproduces the task intent closely
  enough to execute without guesswork; if the subagent reports any ambiguity or misses
  the intended work, fix the TaskDoc before dispatching any Executor.
- '1. Run a separate cheap cold-bundle coverage review under [ritual-context-review](context-review.md):
  explicitly supply task, routed instructions/rituals, bound pills, linked atoms/files
  and validation. Require reformulation, ambiguities and detailed dry-run; no commands
  or source edits.'
- 1. The coordinator compares both outputs with owner intent. Fix the written brief,
  split oversized nodes and retry changed input in a new isolated process. Resolve
  cold-review findings before implementation; unresolved ambiguity blocks dispatch.
- 1. Sweep the board-routed pills and any task-local pills against the task scope,
  touched files, implementation path, and planned validation.
- 1. Bind every pill whose `when`, `where`, or `how_not` matches a plausible part
  of the task.
- 1. If a risky ambiguity is still uncovered, create or update a pill before implementation
  instead of proceeding on implicit assumptions.
- 1. Do not start implementation until the initialization gate confirms atomization,
  preflight comprehension, cold review, and pill coverage.
- 1. Implement only the changes required for the active task.
- 1. Keep scope tight and avoid unrelated fixes.
- 1. Prepare validation before calling the work complete.
- 1. Exit execution only by opening a handoff to testing that names the intended contract,
  relevant tests, and pill guardrails that must be proven.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:execution
---

# Execution ritual for active desk tasks

## Purpose

_Explain why this ritual exists._

Carry one active desk task through scoped implementation inside an explicit phase with task and pill binding, including a zero-context TaskDoc comprehension gate and a fresh-context coverage check strong enough to catch missing guardrails before implementation starts. Apply the [context-review ritual](context-review.md) as the cheap non-executing brief-quality gate; expert review, Executor work and independent Tester validation remain distinct.

## Trigger

_State when this ritual should start._

Start when a desk task becomes the current execution target.

## Preconditions

_List the conditions that must hold before running the ritual._

- The task exists in desk/tasks.
- The current phase or ready dependency layer is explicit.
- Dependencies are explicit.
- Required pills exist.
- The board routes the task as active.
- The active board pills are visible to the executor.
- The initialization gate is still open.
- The TaskDoc is specific enough for a fresh-context subagent to restate the work without guessing.
- Required root/package/leaf and dependency-interface reviews have passed the coordinator comparison under [ritual-context-review](context-review.md).

## Validation

_List the checks that prove the ritual was performed correctly._

- The active task is explicit.
- A cheap isolated reviewer completed TaskDoc-only preflight before Executor dispatch; provider/model/profile, exact input/hash, output and coordinator disposition are traceable under ritual-context-review.
- The preflight reformulation was stored at `runs/subagents/<run-dir>/preflight.md`.
- The preflight passed only because the subagent's reformulation reproduced the intended work and surfaced no unresolved ambiguity.
- A separate cheap isolated cold-bundle reviewer completed comprehension and guardrail coverage; expert council review does not satisfy either cheap gate.
- Required pills are named in the task.
- Cold-review ambiguities were resolved in the written contract and rerun when affected input changed; no unresolved finding was merely recorded as permission to execute.
- Each changed surface is either covered by a named pill or explicitly judged to need no pill.
- No active board pill was skipped just because it looked generic or already familiar.
- Implementation did not start before the initialization gate was satisfied.
- Changes stay within task scope.
- The work is ready for testing and has an explicit testing handoff.

## Failure Modes

_List common mistakes this ritual prevents._

- Working without an active task doc.
- Mixing unrelated concerns into one task.
- Skipping the zero-context TaskDoc comprehension gate and dispatching an Executor anyway.
- Letting the preflight pass even though the reformulation missed intent or reported ambiguity.
- Skipping the fresh-context subagent review and relying only on the primary executor's familiarity.
- Skipping pill binding when ambiguity still exists.
- Treating the task's `## Pills` list as a formality instead of a coverage checklist.
- Binding only the most obvious pill while ignoring pills implied by `when`, `where`, or `how_not`.
- Starting code changes before the initialization gate is closed.
- Handing work to closeout directly from execution without a testing gate.
- Using expert approval, a verdict token, reviewer execution, or implementation tests as a substitute for cheap non-executing comprehension.

## Completion

_Describe what completion looks like._

The implementation is complete enough to enter the testing ritual through an explicit handoff gate.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- 1. Confirm the incoming handoff includes passing evidence for the contract, validations,
  and bound pills.
- 1. Invalidate or fix stale tests if they no longer prove the intended behavior.
- 1. Run the required validation commands and confirm they pass.
- 1. Run `deskops closeout verify --task <id>` and require all reported gates to pass
  before the tool-made commit.
- '1. Check that verify reports ''esta tarea declaró X; encontré Y'' and that Y covers
  X: closeout verifies only the evidence the task declared in `closeout_evidence`
  (tests, commit, atom, materialization, document, external), and a task created without
  it is gated as code and raises an alert. Read every alert; a `.py` change on a task
  that declared no tests is not blocked, but it is never silent.'
- 1. Confirm the task satisfied each bound pill and that no matching board-routed
  pill was missed during execution.
- 1. If the task bound pills, check whether the task `references` list already points
  to an atom that captures any durable residue; tasks with no bound pills pass this
  check trivially.
- 1. If verify reports a changed file with no live atom/materialization link, route
  that gap into an explicit follow-up reference before closing.
- 1. If verify reports a rendered artifact with a sibling source but no declared `source_atoms`
  or `provenance`, fix the artifact metadata before closing.
- 1. Remove stale context docs that are no longer needed.
- '1. Leave removal and untracking to deskops closeout commit: it removes the task
  from the Board, untracks it, and deletes the bundle in the closing commit. Do not
  delete or untrack by hand first.'
- 1. If the task's subject no longer exists, close it with `deskops closeout supersede`,
  naming a reason and at least one resolvable ref, and stop here instead of running
  the closeout commit.
- 1. Close the task with `deskops closeout commit` as the one entry point and the
  mandatory final gate.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:closeout
---

# Closeout ritual for tracked desk tasks

## Purpose

_Explain why this ritual exists._

Close a desk task only after tests, board cleanup, store cleanup when needed, and a dedicated closing commit, while leaving shared integration, pill reconciliation, and next-phase preparation to the phase ritual. `deskops closeout commit` is the one closure entry point: it runs the closeout gates, removes the task from the Board, removes the bundle, makes exactly one commit with the route's trailers, and records the index entry. `deskops advance` does not close tasks. `deskops closeout supersede` is the only way to close a task whose subject no longer exists: it records `superseded` and the stated reason instead of pretending the work was done. `deskops closeout retire` removes a task that was already resolved before the ritual lifecycle (status resolved, closed, done or complete), naming the commit that resolved it, so legacy history leaves desk/tasks without passing through evidence gates it predates. When a closed task was never committed, the closeout first records its body in one commit (`desk: registra <task stem>`, with `Task-Id` and `Closeout-Mode: record` trailers) before the closing commit removes it, so the task's rationale, goal, scope, validation, and done-when stay in git history. The evidence that closes a task is declared when the task is created (`closeout_evidence`, set with `deskops add task --evidence` or filled from `--task-type`; owner decision of 2026-10-29), and closeout verifies exactly that: the same evidence cannot be demanded of every task. See atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly.

## Trigger

_State when this ritual should start._

Start when the implementation work for a task is complete.

## Preconditions

_List the conditions that must hold before running the ritual._

- Relevant tests pass.
- Bound pill obligations were checked during testing.
- If the task bound one or more pills, closeout reviewed whether any durable pill residue now needs an atom reference in the task `references` list.
- The testing-to-closeout handoff gate is explicit.
- Any stale context docs are ready to be removed.
- The closing change is ready to commit.
- For a superseded task, the reason states that the subject no longer exists and the ref resolves to an ancestor commit or an existing path.

## Validation

_List the checks that prove the ritual was performed correctly._

- The task is gone from desk/tasks.
- The board no longer routes the task.
- No bound pill is left unmet or unverified.
- Tasks with bound pills either reference an atom in `references` or explicitly affirm that no durable pill knowledge needed graduation.
- `deskops closeout verify --task <id>` passes before the tool-made closeout commit.
- Verify reports the evidence the task declared in `closeout_evidence` and what it found ('esta tarea declaró X; encontré Y'): resolvable test evidence when tests is declared, a resolvable ancestor commit when commit is declared, changed-file atom/materialization coverage (or a routed follow-up when coverage is not live yet) when atom or materialization is declared, an existing document when document is declared, and an http(s) URL in `references` when external is declared.
- A `.py` change on a task that did not declare tests, or a task with no `closeout_evidence` (gated as code), is reported as a visible alert and does not block closeout.
- Changed generated artifacts with a sibling source declare `source_atoms` or `provenance` so the source relation is explicit.
- The local store stays consistent after untracking.
- `deskops closeout commit` made exactly one closing commit, with the route's trailers, and recorded its index entry.
- The task was not treated as closed before the final commit gate.
- A superseded task was closed with `deskops closeout supersede`, not with a closeout commit that claims completed work.
- The superseded closing commit carries `Closeout-Mode: superseded`, `Closeout-Reason`, and `Closeout-Ref` trailers.

## Failure Modes

_List common mistakes this ritual prevents._

- Deleting the task before the closing commit exists.
- Leaving a stale tracked document in the store.
- Calling a task closed while tests still fail.
- Closing from green tests alone without checking pill coverage.
- Removing a pill-bound task without checking whether its durable residue should now point at an atom.
- Treating board cleanup or task deletion as equivalent to the final commit gate.
- Closing a task whose subject was removed as if the work had been done.
- Running `deskops closeout supersede` without a reason or a resolvable ref.
- Demanding the same evidence from every task: a docs, spec or external task is not blocked for lacking tests, and a code task cannot skip them by declaring nothing.

## Completion

_Describe what completion looks like._

The task has left the active workspace and its closure is recorded by its own git commit. If it was the last open task in the current phase, the board must still pass through phase closeout before the next phase begins.
