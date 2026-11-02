# Catálogo inicial de vistas y renderizaciones

Estado: borrador. No es una lista de páginas a implementar ni una taxonomía de modelos aprobada. WS09/WS11 deben contrastar cada caso con documentos, consultas y renderizadores existentes.

| Fuente / selección | Representaciones candidatas | Operaciones / navegación |
|---|---|---|
| Entrada ecosistema/proyecto, índice o mapa | Markdown renderizado, lista enlazada, mapa de relaciones | Abrir destinos, explicar organización; resolver origen y proyecto |
| Cualquier documento del desk | Fuente Markdown, render estructurado, campos/propiedades | Leer, comparar, editar por contrato; referencias y backlinks |
| Board y sus referencias | Lista, tablero, dependencias | Abrir tareas/contexto/rituales; operaciones de enrutamiento |
| Task y documentos vinculados | Encargo, procedimiento aplicable, evidencia/cambios | Preparar, ejecutar, validar, revisar; acciones de workflow |
| Ritual, pasos y lifecycle | Procedimiento, relaciones/transiciones | Consultar obligaciones y condiciones; edición del contrato soportado |
| Átomos/protoátomos y fuentes | Documento, agrupación/consulta, relaciones | Capturar, clasificar, vincular, dividir/reunir, consultar procedencia/materializaciones y validación soportada |
| Inbox: entradas y consulta | Lista y mensaje/documento | Leer, responder, ack y triage según contrato |
| Drawer: candidatos y mapas | Documentos, lista/consulta, relaciones | Aclarar/organizar; autoría de trabajo explícita |
| MaterializationContractDoc y soportes | Contrato, origen/destino, impacto | Navegar procedencia, verificar vigencia y validación |
| Registro de repositorios | Directorio enlazado, relaciones de desks | Abrir desk, resolver identidad, comunicación autorizada |
| Roles, runtime profiles y RunDoc | Contrato, ejecución/evidencia, conversación vinculada | Preparar/delegar y revisar; estado operativo procede del runtime |
| Resultado de búsqueda o diagnóstico | Lista/tabla, documento en contexto, subgrafo | Afinar selección, abrir origen; no duplicar contenido |

## Reglas a precisar

- ViewDoc de Spec2viz ya expresa selección de modelos/predicados, relaciones y notación; verificar qué cubre antes de extenderlo. No confundir SurfaceDoc (documentación de subsistema CLI) con definición de una pantalla.
- Un Board contiene referencias, no una segunda copia de cada tarea.
- El renderer cambia representación; las operaciones semánticas mantienen su autoridad fuera del componente visual.
- Relaciones entrantes, inventarios y resultados derivables se calculan; documentos nuevos deben aportar organización/decisión authored real.
- El mismo documento puede abrirse en dos representaciones con selección e identidad comunes. Las composiciones señalan el documento/campo dueño de cada edición.
- No es necesario representar estado volátil del runtime ni preferencias privadas como documentos compartidos; fijar ese límite explícitamente.

## Ficha de cada vista (pendiente de completar)

Propósito humano; documento/consulta origen; identidad; contrato/modelo; campos y relaciones usados; renderer existente o requerido; navegación; acciones y dueño; destino de escritura; conflictos/errores; disponibilidad actual; aceptación mediante user-flow.

## Filas que faltaban

| Soporte | Representación | Acciones/dueño |
|---|---|---|
| CrossroadDoc y namespace | Documento/árbol de dominio y relaciones | Abrir padres/hijos reales, no jerarquía por carpeta arbitraria |
| Issue Markdown sin modelo | Markdown fuente/render y lista por operaciones existentes | issue list/close por autoridad, no validarlo como TaskDoc |
| DeskFAQDoc | Documento y navegación de preguntas | Orientación, buscar y abrir; edición bajo contrato |
| StepDoc y pills | Documento/procedimiento/contexto vinculado | Consultar referencia y aplicar operación soportada |
| Código local referenciado | Code read-only y soporte del nodo | Leer archivo/rango seguro según infraestructura real; sin CST supuesto |
| SpecDoc/NotationDoc/ViewDoc | Documento y notación/gráfico soportado | Reutilizar Specs; ViewDoc solo grafo portable |
| Modelos y templates | Schema/edición de clase existente | Draft/validate/promote público, WS39 |
| Historial/diff Git | Revisión read-only junto al documento/tarea | Abrir evidencia; distinto de Changes/integridad; sin revert destructivo |

El registro estático de renderizadores/capacidades del shell puede existir en código; lo que no se hardcodea como verdad separada es el inventario y la organización de documentos/proyectos. Vocabulario de brief.md separa ViewDoc, representación, foco y consulta. La edición fuente espera WS20; una preferencia local no se convierte por defecto en documento compartido.

## Fichas por fila

Una ficha por fila de las dos tablas, F01-F12 (tabla «Fuente / selección») y F13-F20 (tabla «Filas que faltaban»), en el orden de las tablas. Los sufijos a/b separan solo un componente con evidencia o estado distinto (F11, F18, F19). Los campos son los de la TaskDoc de WS09; la sección «Ficha de cada vista» queda como la lista original.

Convención de citas. `deskops.md:N`, `infraestructura.md:N` y `ui.md:N` son líneas de `../auditoria/deskops.md`, `../auditoria/infraestructura.md` y `../auditoria/ui.md`; `user-flows.md:N` y `manual.md:N` son de este directorio; `reconciliacion.md:N`, `decisiones.md:N` y `dag.yaml:N` son de `../`. `dag.yaml` se cita para verificar IDs y alcance de nodo. «base existente» = renderer o capacidad citada en una auditoría; no prueba aceptación. Productor de contrato = WS11 o WS12; productor de implementación = nodo del DAG, o «sin productor en el DAG» con repo dueño (`owner_repo` del nodo más cercano o repo de la capacidad en la auditoría). Clases: authored = texto o estructura escrita por una persona o agente como fuente; derivado = calculado desde otras fuentes; preferencia local = estado de sesión o disposición, no documento compartido (P07, `decisiones.md:31`). Estado según `manual.md:41-49`: hoy no hay actas humanas (`manual.md:45`), así que ninguna ficha es disponible; propuesto = sin dependencia ni contrato identificado pendiente y sin evidencia completa; bloqueado = nodo del DAG o contrato WS11/WS12 pendiente que la fila necesita. Hoy las 23 fichas son bloqueado: todas dependen de un contrato o nodo pendiente, aunque tengan base existente. Lo que WS11 debe precisar se señala sin inventar mapeo (`dag.yaml:693-700`, `dag.yaml:857-859`). Nada de esta sección crea workspace, API, renderer, pasos ni capturas: reutiliza el host Mindmap y su registro (`dag.yaml:1574-1590`, `reconciliacion.md:49`).

### F01 — Entrada ecosistema/proyecto, índice o mapa

- **Propósito humano**: explicar propósito, superficies y trabajo actual de un proyecto sin rutas memorizadas (`user-flows.md:13`).
- **Origen**: entrada del ecosistema y entrada del desk `desk/README.md` + mapa authored (P09, `decisiones.md:33`; `user-flows.md:15`); registro `desk/registry` con 6 RepositoryDoc (`deskops.md:195,220`). Documento de la entrada del ecosistema y del mapa: no definido; productor de contrato WS11, de plantillas WS17 (`dag.yaml:1170-1198`, owner_repo deskops) y de publicación real WS43 (`dag.yaml:2792-2803`).
- **Identidad**: no definido para entrada y mapa; productor WS11 (`dag.yaml:693-694`). El repo se identifica con `deskops repo whoami` (`deskops.md:101`).
- **Contrato**: sin contrato. Ninguno de los 17 modelos registrados es de entrada o índice (`deskops.md:185-201`); P09 los define como documentos authored (`decisiones.md:33`).
- **Campos y relaciones**: enlaces `[[doc]]` y `[[doc#Sección]]` (`infraestructura.md:88`) y aristas por campo (`infraestructura.md:92`). Campos de RepositoryDoc: no leídos en las auditorías; productor WS11.
- **Renderer existente o requerido**: base existente: panel de nodo y vecindad 1-2 saltos para documentos del store (`ui.md:54-55,69`). Requerido para Markdown no modelado: ausente (`ui.md:55`), productor WS13.1 y WS13.2 (graph_ui; `dag.yaml:841,892`). Lista enlazada de entradas: no definido; contrato WS11, implementación WS13.1 y WS13.2.
- **Navegación**: abrir destinos; URL/`popstate` y tarjetas que reorientan (`ui.md:57,69`); resolver origen y proyecto lo fija WS11 (`dag.yaml:693-697`); otro desk: WS41 (`ui.md:87`).
- **Acción/dueño**: solo lectura. Dueño de las entradas authored: deskops, productor WS17.
- **Destino de escritura**: la UI no escribe. Las plantillas viven en `ejemplo/nav/` del paquete del plan (`dag.yaml:1179`).
- **Error**: condicionado a WS11 y WS13.1: proyecto no accesible o referencia rota muestra el origen y conserva la navegación (`user-flows.md:13`). Contrato de errores de API y red: no definido; productor WS11 (`user-flows.md:30`).
- **Estado**: bloqueado. Necesita el contrato WS11 y los nodos WS13.1, WS13.2 y WS17.
- **Clase**: authored (entrada y mapa); derivado (vecindad, inventario de proyectos: «inventarios... se calculan», línea 25 de este archivo); preferencia local (selección e historia, `decisiones.md:31`).
- **UF**: UF01 (`user-flows.md:9-33`); UF10 (índices authored, `user-flows.md:233`).
- **Evidencia**: `ui.md:54-57,69,87`; `deskops.md:101,185-201,195,220`; `infraestructura.md:88,92`; `user-flows.md:13-33,233`.

### F02 — Cualquier documento del desk

- **Propósito humano**: leer, comparar y editar un documento en varias representaciones sin perder la identidad; fuente y representación apuntan al mismo documento (`user-flows.md:63`).
- **Origen**: documento de cualquier modelo del store, vía payload/IR (`sldb docs show`, `GET /document/ir`; `infraestructura.md:30`); Markdown no modelado del desk (118 archivos, `deskops.md:226`).
- **Identidad**: `Model:name` para modelados (`reconciliacion.md:5`; `ui.md:54`). Para no modelados: no definido; productor WS11 (`dag.yaml:693-694`).
- **Contrato**: el modelo del documento, si existe (17 modelos, `deskops.md:185-201`). Markdown no modelado: sin contrato.
- **Campos y relaciones**: payload, `incoming_relations`, `content_hash`, `file_revision` (`ui.md:55`); `version` = `content_hash` (`infraestructura.md:51`); referencias y aristas (`infraestructura.md:88-92`). Los campos concretos son los del modelo; no se enumeran aquí.
- **Renderer existente o requerido**: base existente: WorkspaceView con Documento/Grafo Local/Código y panel Context (`ui.md:55,57`; `reconciliacion.md:5`), solo documentos del store. Fuente cruda íntegra y Markdown sin modelo: ausentes (`ui.md:55`), productor WS13.1. Campos editables y comparación: no definido; productor de contrato WS11 y WS12, de implementación WS19 (`dag.yaml:1258`).
- **Navegación**: seguir enlaces y alternar texto/graph/code preservando el origen (`dag.yaml:860-871`); foco compartido solo con correspondencia real de origen que fije WS11 (`dag.yaml:857-859`); historia URL (`ui.md:57`); pestañas y divisiones: WS13.3 (`ui.md:57`; `dag.yaml:933`).
- **Acción/dueño**: leer; editar por contrato. Cada edición señala el documento y campo dueño (línea 26 de este archivo). Whitelist por campo/modelo: WS12 (`dag.yaml:734-741`). Dueño de la operación de campos: sldb (`infraestructura.md:31`).
- **Destino de escritura**: campos: `sldb fields update` o `POST /save` (`infraestructura.md:31,51`) por el canal que fije WS12. Fuente raw: no definido; productor WS20 (sldb, `dag.yaml:1388`; `infraestructura.md:33`). En la UI actual solo el KB map guarda con 409, no el workspace (`ui.md:63-64`).
- **Error**: condicionado a WS12/WS19: el conflicto conserva la edición del usuario (`user-flows.md:63`); 409 por `expected` (`infraestructura.md:51`); la forma legacy no verifica (`infraestructura.md:53`); el editor externo no se detecta (`infraestructura.md:56`). Contrato de conflicto y fallo parcial para el workspace: no definido; productor WS12 (`user-flows.md:83`).
- **Estado**: bloqueado. Necesita WS11, WS13.1, WS19, WS20, WS21 y WS45 (`reconciliacion.md:15`).
- **Clase**: authored (documento y campos); derivado (contexto, relaciones entrantes, hashes); preferencia local (representación activa, foco, pestañas).
- **UF**: UF01, UF03 (`user-flows.md:59-85`), UF07 (inspeccionar soporte, `user-flows.md:174`), UF09 (desde un documento, `user-flows.md:206`).
- **Evidencia**: `ui.md:54-57,63-64`; `infraestructura.md:30-33,51-56`; `deskops.md:226`; `reconciliacion.md:5,15`; `user-flows.md:63,83`.

### F03 — Board y sus referencias

- **Propósito humano**: distinguir pendiente, activo y listo para ejecutar, y enrutar el trabajo (`user-flows.md:91`).
- **Origen**: BoardDoc `desk/tasks/Board.md` y los TaskDoc que referencia (`deskops.md:186,223`); en otros repos, `deskops list tasks --include-repos` (`deskops.md:76`); lectura UI: `GET /api/desk/board` (`ui.md:67`).
- **Identidad**: ruta del Board (`deskops.md:223`); identidad en el lector: no definido; productor WS11.
- **Contrato**: BoardDoc (`deskops.md:186`) y TaskDoc (`deskops.md:201`). El Board contiene referencias, no una copia de cada tarea (línea 23 de este archivo).
- **Campos y relaciones**: rutas de tareas del Board; en la tarea, `depends_on`, `files`, `closeout_evidence`, pills (`deskops.md:51,73`; `dag.yaml:1497-1501`). Capa lista sin solapamiento: ningún comando la calcula (`user-flows.md:101`); se propone derivarla en lectura (`reconciliacion.md:71`); contrato WS12.
- **Renderer existente o requerido**: base existente: vista Deskops con lista filtrada por estado y detalle con gates (`ui.md:67`, commit daa6400), fuera del lector workspace. Requerido: tablero agrupado, dependencias navegables y apertura de TaskDoc en el lector, ausentes (`ui.md:67`); productor WS22 (`dag.yaml:1488`, graph_ui).
- **Navegación**: abrir tareas, contexto y rituales; la apertura en el lector es parte de WS22 (`ui.md:67`).
- **Acción/dueño**: enrutar con `add task`, `edit board`, `advance task` (`deskops.md:51,65,98`). La UI avanza con `POST /api/desk/advance` y 409 (`ui.md:79`). Dueño: deskops; la autoría y el enrutado desde UI son WS26.2 (`ui.md:73-75`; `dag.yaml:1819`). El lock de la UI no coordina escritores CLI/agentes (`reconciliacion.md:21`).
- **Destino de escritura**: `desk/tasks/Board.md` por `add task` y `edit board` (`deskops.md:51,65`). Desde UI: no definido; productor WS12.
- **Error**: condicionado a WS12 y WS22: revisión obsoleta de Board o tarea responde 409 en `advance` (`ui.md:79`). Errores de autoría y enrutamiento para la UI: no definido; productor WS12 (`user-flows.md:107`).
- **Estado**: bloqueado. Necesita WS22, WS26.2 y el contrato WS12.
- **Clase**: authored (Board y tareas); derivado (agrupación por estado, dependencias, capa lista); preferencia local (filtro, selección).
- **UF**: UF04 (`user-flows.md:87-109`), UF01 (trabajo actual, `user-flows.md:22`), UF05 (abrir tarea, `user-flows.md:120`).
- **Evidencia**: `ui.md:67,73-75,79`; `deskops.md:51,65,73,76,98,186,201,223`; `user-flows.md:91,101,107`; `reconciliacion.md:21,71`.

### F04 — Task y documentos vinculados

- **Propósito humano**: preparar, ejecutar, validar y revisar una tarea con su encargo, procedimiento aplicable y evidencia, sin saltarse gates (`user-flows.md:115`).
- **Origen**: TaskDoc (`deskops show task`, `deskops.md:87`), con pills, rituales, `references` y `files`; evidencia con `closeout verify` (`deskops.md:134`).
- **Identidad**: TaskDoc por glob `desk/tasks/task-*.md` (`deskops.md:201`); identidad en el lector: no definido; productor WS11.
- **Contrato**: TaskDoc (`deskops.md:201`).
- **Campos y relaciones**: `closeout_evidence` declarada, `from_drawer`, pills (`deskops.md:51,73,150`); `status` y `current_node` los fija el lifecycle, y `advance --to` o `edit task` pueden forzarlos (`deskops.md:98,62`).
- **Renderer existente o requerido**: base existente: detalle con gates, «Evidencia declarada» y botón Avanzar (`ui.md:67,78,79`). Requerido y ausente: diff Git (`ui.md:77`, WS27.1), evidencia encontrada y verificada (`ui.md:78`, WS27.2), `closeout verify` por UI (`ui.md:79`, WS28), procedimiento (`ui.md:68`, WS23).
- **Navegación**: abrir soporte (`ui.md:78`); reabrir enlaces sin perder el encargo es WS13.3 (`user-flows.md:128`).
- **Acción/dueño**: avanzar por la UI existente; `closeout verify` y `closeout commit` por CLI/coordinador, sin cierre HTTP (`decisiones.md:29`; `deskops.md:131,134`). Dueño: deskops. La whitelist de campos protegidos la define WS12 (`user-flows.md:132`).
- **Destino de escritura**: TaskDoc y Board por operaciones de deskops; el cierre borra la tarea (`deskops.md:131`). Desde UI: no definido; productor WS12 y WS28.
- **Error**: condicionado a WS12/WS28: `closeout verify` emite alertas y findings, exit 0 solo si ok (`deskops.md:134`); evidencia fuera del vocabulario cerrado falla (`deskops.md:259`); 409 en `advance` (`ui.md:79`). Contrato de error de cierre y handoff para la UI: no definido; productor WS12 (`user-flows.md:133`).
- **Estado**: bloqueado. Necesita WS23, WS27.1, WS27.2, WS28 y WS12.
- **Clase**: authored (TaskDoc, evidencia declarada); derivado (gates evaluados, evidencia encontrada y verificada, diff); preferencia local (foco y pestañas).
- **UF**: UF05 (`user-flows.md:111-135`), UF04, UF06 (bundle, `user-flows.md:149`), UF07 (`user-flows.md:174`).
- **Evidencia**: `ui.md:67-68,77-79`; `deskops.md:51,62,73,87,98,131,134,150,201,259`; `decisiones.md:29`; `user-flows.md:115,128,132-133`.

### F05 — Ritual, pasos y lifecycle

- **Propósito humano**: consultar obligaciones y condiciones del procedimiento aplicable (fila de la tabla 1; `manual.md:125-129`).
- **Origen**: RitualDoc (7 en `desk/rituals`, `deskops.md:196,219`); grafo de lifecycle en `desk/lifecycle` (RelationDoc 3 y RelationTypeDoc 3, `deskops.md:193-194,224`); StepDoc: 0 documentos (`deskops.md:200`); transiciones con `show task` (`deskops.md:87`).
- **Identidad**: RitualDoc con id propio (p. ej. `ritual-phase`, `deskops.md:235`). Identidad en el lector: no definido; productor WS11.
- **Contrato**: RitualDoc, StepDoc, RelationDoc y RelationTypeDoc (`deskops.md:193-200`).
- **Campos y relaciones**: los nodos del lifecycle son RitualDocs (`deskops.md:196`); transiciones con origen, destino y condición declarados (`dag.yaml:1537-1546`). Progreso de paso: solo si WS02/WS09/WS11 identifican un campo o API real de deskops (`dag.yaml:1540-1546`); ninguno está identificado, por eso no definido; productor WS11.
- **Renderer existente o requerido**: base existente mínima: payload/lifecycle navegables como documentos y gates con `holds` y condición en la vista Deskops (`ui.md:68`). Requerido: renderer de RitualDoc/StepDoc/pasos, ausente (`ui.md:68`); productor WS23 (graph_ui, `dag.yaml:1526`).
- **Navegación**: un procedimiento abre sus documentos y soporte; no marca pasos como realizados por leerlos (`dag.yaml:1540-1546`).
- **Acción/dueño**: consultar. Edición del contrato soportado: `edit ritual` (`deskops.md:64`), dueño deskops. WS23 es solo lectura, sin controles de avance (`dag.yaml:1540-1546`); el botón Avanzar existente pertenece a la vista Deskops (`ui.md:68`).
- **Destino de escritura**: RitualDoc por `edit ritual`; `add ritual` no lo trackea en el acto (`deskops.md:53`). Desde UI: no definido; productor WS12.
- **Error**: no definido; productor de contrato WS12 y de implementación WS23. Condicionado: con 0 StepDoc el procedimiento carece de pasos que mostrar (`deskops.md:200`).
- **Estado**: bloqueado. Necesita WS23.
- **Clase**: authored (RitualDoc, StepDoc, definición del lifecycle); derivado (condición evaluada de las transiciones); preferencia local (foco).
- **UF**: UF05 (`user-flows.md:129`), UF04 (`user-flows.md:97`), UF01 (`user-flows.md:22`).
- **Evidencia**: `ui.md:68`; `deskops.md:53,64,87,193-200,219,224,235`; `dag.yaml:1526-1546`; `user-flows.md:22,97,129`.

### F06 — Átomos, protoátomos y fuentes

- **Propósito humano**: capturar, clasificar, vincular, dividir o reunir conocimiento y consultar procedencia (`user-flows.md:61-63`).
- **Origen**: AtomDoc (145 en el índice local), ProtoAtomDoc (0) (`deskops.md:185,192`); fuentes pill, graph finding o diagrama de `atoms create` (`deskops.md:114`).
- **Identidad**: id inmutable (`deskops.md:66`); protoátomo `proto-<slug>` (`deskops.md:119`). `Model:name` en el lector: `reconciliacion.md:5`.
- **Contrato**: AtomDoc y ProtoAtomDoc (`deskops.md:185,192`).
- **Campos y relaciones**: tags y tag `domain:` (`deskops.md:119`), 5wh+ y provenance (`deskops.md:114`), referencias entrantes (`deskops.md:115`). Backlinks por API de grafo de sldb y clasificación por tipo y tags declarados (`dag.yaml:1574-1590`).
- **Renderer existente o requerido**: requerido: vista de documento genérica única registrada en `shell/registry.js`, no un renderer por clase (`dag.yaml:1574-1590`); base existente: lector genérico IR/payload (`reconciliacion.md:18`). Operaciones de dividir y reunir en UI: ausentes (`ui.md:88`), productor WS42 (`dag.yaml:2745`).
- **Navegación**: abrir átomo y fuentes, relacionados a 1-2 saltos (`ui.md:69`; `user-flows.md:71-72`).
- **Acción/dueño**: `edit atom`, `atoms split`, `merge`, `delete`, `reorganize`, `proto`, `type` (`deskops.md:66,111,115-117,119-120`); dueño deskops. Vincular: `ConnectDialog` solo en el KB map (`ui.md:65`). UI con confirmación: WS42, sobre la whitelist de WS12 (`dag.yaml:2745-2770`).
- **Destino de escritura**: archivo del átomo por deskops (muta desk y store, `deskops.md:116-117`). Desde UI: no definido; productor WS12.
- **Error**: condicionado a WS12/WS42: `atoms delete` rechaza si hay referencias entrantes (`deskops.md:115`); 409 por `expected` (`infraestructura.md:51`). Fallos parciales y permisos en el workspace: no definido; productor WS12 (`user-flows.md:83`).
- **Estado**: bloqueado. Necesita WS19, WS24, WS42 y WS12.
- **Clase**: authored (átomo, protoátomo, tags); derivado (backlinks, clasificación por árbol, vecindad); preferencia local (foco).
- **UF**: UF03, UF02 (`user-flows.md:45-46`).
- **Evidencia**: `deskops.md:66,111,114-120,185,192`; `ui.md:65,69,88`; `dag.yaml:1565-1590,2745-2770`; `user-flows.md:45-46,71-76`.

### F07 — Inbox: entradas y consulta

- **Propósito humano**: leer una nota externa, consultar contexto, acusar recibo local o responder dentro del mismo desk; el ack no es aceptación del trabajo (`user-flows.md:36,38`).
- **Origen**: InboxNoteDoc, 14 en `desk/inbox` (`deskops.md:189,216`); `message list` y `list inbox-notes` (`deskops.md:39,83`).
- **Identidad**: nombre, stem o fragmento (`message read`, `deskops.md:40`); `<ts>-<kind>-<slug>` (`deskops.md:38`). Selector en el lector: no definido; productor WS11.
- **Contrato**: InboxNoteDoc (`deskops.md:189`).
- **Campos y relaciones**: estado cerrado y `acknowledged_by/at` (`deskops.md:41`). Otros campos: no leídos en las auditorías; productor WS11.
- **Renderer existente o requerido**: ausente en la UI (solo un ícono de `InboxNoteDoc`, `ui.md:71`); productor WS25.1 (`dag.yaml:1652`). Mostrar la nota como documento: contrato de lectura WS11, implementación WS25.1.
- **Navegación**: consultar contexto con `sldb find`, `fields query`, pills (`user-flows.md:44`); más: no definido; productor WS11.
- **Acción/dueño**: leer y listar; ack local reescribe la nota y re-trackea (`deskops.md:41`) pero su uso como ack de la UF queda pendiente del contrato WS12 (`user-flows.md:49`); responder dentro del mismo desk es hueco (`user-flows.md:50`); `promote inbox-to-drawer-task` borra la nota y no está aprobado como canal (`deskops.md:43`; `user-flows.md:47`). Dueño: deskops.
- **Destino de escritura**: nota de `desk/inbox` del mismo desk (`deskops.md:41`). Desde UI: no definido; productor WS12 (UI: WS25.1).
- **Error**: condicionado a WS12/WS25.1: `message read` ambiguo = UsageError y `message ack` revierte el archivo si falla el tracking (`deskops.md:40-41`). Errores de captura, ack y respuesta expuestos a la UI: no definido; productor WS12 (`user-flows.md:55`).
- **Estado**: bloqueado. Necesita WS25.1 y WS12.
- **Clase**: authored (nota); derivado (lista ordenada por reciente, `deskops.md:39`); preferencia local (filtro, selección).
- **UF**: UF02.
- **Evidencia**: `deskops.md:38-43,83,189,216`; `ui.md:71`; `dag.yaml:1652`; `user-flows.md:36-55`.

### F08 — Drawer: candidatos y mapas

- **Propósito humano**: aclarar y organizar material sin exigir tarea ni ejecución, y autorizar una tarea completa solo explícitamente (`user-flows.md:38`).
- **Origen**: `desk/drawer/` con 119 archivos: tasks 76, plans 42 (`deskops.md:217`); candidatas con forma de TaskDoc que el store no vincula.
- **Identidad**: ruta; `resolve_drawer_source` resuelve por ruta, stem o fragmento único (`deskops.md:166`). Identidad en el lector: no definido; productor WS11.
- **Contrato**: sin contrato: las candidatas no están modeladas (`deskops.md:217`).
- **Campos y relaciones**: `from_drawer` como procedencia hacia la tarea (`deskops.md:150`).
- **Renderer existente o requerido**: no definido para el drawer; Markdown no modelado depende del lector WS13.1 y del explorador WS13.2 (`ui.md:55-56`); productor de contrato WS11.
- **Navegación**: abrir candidato y mapa; el Board del drawer es `desk/drawer/tasks/Board.md` (`deskops.md:45`). Más: no definido; productor WS11.
- **Acción/dueño**: `edit task` sobre candidatas, `add task --from-drawer`, `drawer remove` (rechaza si una tarea registra `from_drawer`) (`deskops.md:62,51,45`); dueño deskops. Captura directa a drawer: hueco, contrato WS12 y UI WS25.2 (`user-flows.md:51`; `reconciliacion.md:118`).
- **Destino de escritura**: archivos bajo `desk/drawer/tasks/` por deskops. Desde UI: no definido; productor WS12.
- **Error**: condicionado a WS12/WS25.2: `drawer remove` rechazado (`deskops.md:45`); `create_document` sobrescribe un archivo existente (`infraestructura.md:57`), por lo que las colisiones deben controlarse (`reconciliacion.md:118`).
- **Estado**: bloqueado. Necesita WS13.1/WS13.2, WS25.2 y el contrato WS12.
- **Clase**: authored (candidatos, mapas); derivado (lista o consulta de candidatos); preferencia local (filtro).
- **UF**: UF02, UF04 (`user-flows.md:93`).
- **Evidencia**: `deskops.md:45,51,62,150,166,217`; `ui.md:55-56`; `infraestructura.md:57`; `reconciliacion.md:118`; `user-flows.md:38,51,93`.

### F09 — MaterializationContractDoc y soportes

- **Propósito humano**: navegar la procedencia, verificar vigencia y validación de una materialización (`user-flows.md:76`).
- **Origen**: MaterializationContractDoc: 6 en el índice local, 8 declaradas, 2 sin indexar (`deskops.md:190,206`); `list/show materialization` (`deskops.md:81,92`).
- **Identidad**: archivo bajo `desk/materializations`; `Model:name` en el lector: no definido; productor WS11.
- **Contrato**: MaterializationContractDoc (`deskops.md:190`).
- **Campos y relaciones**: origen/destino/impacto de la tabla: los campos del modelo no se leyeron en las auditorías; no definido; productor WS11. Transclusión `sldb docs compose` (`infraestructura.md:90`).
- **Renderer existente o requerido**: inspección en UI ausente; `Materialization` solo existe como ícono (`ui.md:88`); productor WS24 (vista genérica, `dag.yaml:1574-1590`) y WS42 (inspección/validación, `dag.yaml:2745-2770`).
- **Navegación**: procedencia y soporte: no definido; productor WS11.
- **Acción/dueño**: inspección y validación por API pública SLDB, sin generar destinos arbitrarios (`dag.yaml:2745-2770`; `user-flows.md:246`); `deskops drift check` incluye superficies de conocimiento (`deskops.md:129`). Dueño: deskops (modelo) y sldb (validación).
- **Destino de escritura**: ninguno de generación; `edit materialization` por contrato (`deskops.md:67`). Desde UI: no definido; productor WS12.
- **Error**: condicionado a WS42: documento declarado pero no indexado (`deskops.md:206`); `drift check` termina con exit 1 si hay hallazgos (`deskops.md:129`).
- **Estado**: bloqueado. Necesita WS24 y WS42.
- **Clase**: authored (contrato); derivado (vigencia, drift, impacto); preferencia local (foco).
- **UF**: UF03.
- **Evidencia**: `deskops.md:67,81,92,129,190,206`; `ui.md:88`; `infraestructura.md:90`; `user-flows.md:76,246`.

### F10 — Registro de repositorios

- **Propósito humano**: abrir otro desk, resolver su identidad y mantener origen y destino (`user-flows.md:187`).
- **Origen**: RepositoryDoc, 6 en `desk/registry` (`deskops.md:195,220`); `repo whoami` (`deskops.md:101`).
- **Identidad**: id de repo único; raíz no duplicada (`deskops.md:100`). Aliases y roots autorizados: no definido; productor WS11 (`dag.yaml:2722-2735`).
- **Contrato**: RepositoryDoc (`deskops.md:195`).
- **Campos y relaciones**: id y raíz (`deskops.md:100`); demás campos: no leídos en las auditorías; productor WS11. Relaciones de desks: no definido; productor WS11.
- **Renderer existente o requerido**: directorio enlazado: no definido; la UI resuelve una sola raíz, sin aliases ni lectura cruzada (`ui.md:87`); productor WS41 (graph_ui, `dag.yaml:2722`).
- **Navegación**: seguir una referencia a otro desk y volver por la historia (`user-flows.md:192`).
- **Acción/dueño**: lectura entre desks; `message send` queda fuera del baseline (`deskops.md:38`; `user-flows.md:198`). Dueño: deskops (registro) y graph_ui (lectura).
- **Destino de escritura**: la UI no escribe en el destino (`user-flows.md:192`); `repo register/remove` son CLI (`deskops.md:100,102`).
- **Error**: condicionado a WS41: alias no autorizado, path escapado o store ausente dan error visible (`dag.yaml:2722-2735`). Forma del error: no definido; productor WS11 (`user-flows.md:200`).
- **Estado**: bloqueado. Necesita WS41 y WS11.
- **Clase**: authored (RepositoryDoc); derivado (directorio, lista de repos); preferencia local (disposición e historia entre desks).
- **UF**: UF08 (`user-flows.md:185-202`), UF01 (elegir proyecto).
- **Evidencia**: `deskops.md:38,100-102,195,220`; `ui.md:87`; `dag.yaml:2722-2735`; `user-flows.md:187-200`.

### F11a — Roles y runtime profiles

- **Propósito humano**: leer los roles y perfiles de runtime que sirven para preparar una delegación.
- **Origen**: RoleDoc (3 en `desk/roles`) y RuntimeProfileDoc (2 en `desk/runtimes`) (`deskops.md:197,199,221-222`).
- **Identidad**: `Model:name` en el lector: no definido; productor WS11.
- **Contrato**: RoleDoc y RuntimeProfileDoc; ningún comando de deskops los crea o edita (`deskops.md:197,199`).
- **Campos y relaciones**: no leídos en las auditorías; no definido; productor WS11.
- **Renderer existente o requerido**: lector genérico de documentos del store (`reconciliacion.md:18`); renderer específico: sin productor en el DAG, repo dueño graph_ui.
- **Navegación**: no definido; productor WS11.
- **Acción/dueño**: lectura. `materialize`, `drift check` y `runtime template` los leen (`deskops.md:127,129,142`). No se promete edición desde UF09 (`user-flows.md:214`): dueño deskops, sin productor en el DAG.
- **Destino de escritura**: ninguno disponible; sin productor en el DAG, repo dueño deskops (`deskops.md:197,199`).
- **Error**: no definido; productor WS11.
- **Estado**: bloqueado. Necesita el contrato WS11 para identidad, campos y navegación en el lector.
- **Clase**: authored.
- **UF**: UF06 (solo `runtime template`, `user-flows.md:147`); UF09 como exclusión (`user-flows.md:214`).
- **Evidencia**: `deskops.md:127,129,142,197,199,221-222`; `user-flows.md:147,214`.

### F11b — RunDoc y conversación vinculada

- **Propósito humano**: seguir un intento de ejecución, su conversación y evidencia, y revisarlo; completado por agente no implica aprobado (`user-flows.md:141`).
- **Origen**: RunDoc (2 en el índice, `deskops.md:198`), escrito por `runtime template --task --agent` (`deskops.md:142`). La conversación Scion no está auditada (`user-flows.md:154`). Acceso y contrato público: no definido; productor WS44 (`dag.yaml:2842`, deskops). Vínculo de mensajes al intento: productor WS33 (`dag.yaml:2276`).
- **Identidad**: identidad de intento: no definido; productor WS32 (`user-flows.md:150`; `dag.yaml:2136`, deskops).
- **Contrato**: RunDoc; `closeout commit --run-dir` no usa RunDoc sino `run.yaml` (`deskops.md:198`).
- **Campos y relaciones**: vínculo de mensajes, resultados y decisión humana al intento: no definido; productor WS33 (`user-flows.md:151`; `dag.yaml:2276`).
- **Renderer existente o requerido**: ausente (`ui.md:82-84`); el panel de workers adyacente no se afirma que cubra el alcance (`ui.md:82`); productor WS35 (`dag.yaml:2499`, graph_ui).
- **Navegación**: conversación vinculada: no definido; productor WS33 (vínculo) y WS35 (lectura).
- **Acción/dueño**: preparar y revisar; despacho y respuesta autorizados: WS34 (`dag.yaml:2390`) y UI WS36 (`dag.yaml:2532`). `runtime supervise` nunca responde ni avanza tareas (`deskops.md:141`). Dueño: deskops. G_SCION y G_EXEC pendientes (`user-flows.md:145`). El estado operativo procede del runtime y no es documento compartido (línea 27 de este archivo).
- **Destino de escritura**: RunDoc por `runtime template` (`deskops.md:142`); resto: no definido; productor WS32, WS33, WS34.
- **Error**: no definido; productor WS32, WS33, WS34 y WS44 (`user-flows.md:156-157`).
- **Estado**: bloqueado. Necesita WS32, WS33, WS34, WS35, WS36 y WS44, y las compuertas G_SCION/G_EXEC.
- **Clase**: authored (RunDoc, decisión humana); derivado (estado operativo leído del runtime, no documento compartido).
- **UF**: UF06 (`user-flows.md:137-159`); UF05 (`user-flows.md:121`).
- **Evidencia**: `deskops.md:141-142,198`; `ui.md:82-84`; `user-flows.md:141-159`; `dag.yaml:2136,2276,2390,2499,2532,2842`.

### F12 — Resultado de búsqueda o diagnóstico

- **Propósito humano**: encontrar documentos y entender qué falla o cambió, abriendo el origen sin duplicar contenido (fila de la tabla 1).
- **Origen**: búsqueda por consulta: `sldb find`, `fields query`, `sections find`, `explore` (`infraestructura.md:110-113`), `graph query` (`infraestructura.md:114`). Diagnóstico: `deskops doctor`, `drift check`, `graph missing`, `atoms validate`, `docs recover`, `edges check` (`deskops.md:31,129,125,113`; `infraestructura.md:88,92`).
- **Identidad**: resultado = documento `Model:name` (`reconciliacion.md:5`). Consulta guardada: ausente (`infraestructura.md:121`); sin productor en el DAG (no figura en `dag.yaml`), repo dueño sldb.
- **Contrato**: sin contrato de consulta de UI. ViewDoc de grafo no es contrato universal de UI (línea 22 de este archivo).
- **Campos y relaciones**: según la operación, p. ej. campos y secciones (`infraestructura.md:111-112`). Criterio que separe error, conflicto, cambio y pérdida de soporte: no auditado (`user-flows.md:177`); no definido; productor WS11 (contrato) con WS15.1 y WS29.
- **Renderer existente o requerido**: base existente: filtro local del catálogo (`ui.md:58`), vecindad (`ui.md:69`), problemas por nodo (`ui.md:60`). Ausente: búsqueda por API con estados distintos (WS14, `dag.yaml:974`) y vista Changes/Integrity (`ui.md:80`, WS29, `dag.yaml:2011`).
- **Navegación**: afinar la selección y abrir el origen.
- **Acción/dueño**: lectura. Reparación solo por operaciones existentes, sin botón universal (`user-flows.md:175`). Búsqueda por significado: hueco, `Corpus.rank` sin CLI (`infraestructura.md:115`), dueño sldb, sin productor en el DAG.
- **Destino de escritura**: ninguno de la vista. `sldb stores check` puede escribir caché o journal, no leído (`deskops.md:265`).
- **Error**: condicionado a WS14, WS15.1 y WS29: estados sin resultado, error y degradado distintos (`ui.md:58`); store no disponible 503 y errores de catálogo/nodo/proyección (`ui.md:60-61`); backend caído y fallo CDN: no definido; productor WS11 y WS15.1 (`user-flows.md:173,181`).
- **Estado**: bloqueado. Necesita WS14, WS15.1 y WS29.
- **Clase**: derivado; preferencia local (consulta y filtro activos).
- **UF**: UF03 (`user-flows.md:68-70`), UF07 (`user-flows.md:161-183`), UF01 (`user-flows.md:27-29`).
- **Evidencia**: `infraestructura.md:88,92,110-115,121`; `deskops.md:31,113,125,129,265`; `ui.md:58,60-61,69,80`; `user-flows.md:68-70,173,175,177`.

### F13 — CrossroadDoc y namespace

- **Propósito humano**: recorrer el árbol de dominios con sus padres e hijos reales (fila de la tabla 2).
- **Origen**: CrossroadDoc, 1 documento: `desk/atoms/crossroad-knowledge-management.md` (`deskops.md:187,234`); no existe la carpeta `desk/crossroads` (`deskops.md:234`); namespaces de tags en `desk/atoms/tag-namespaces.yaml` (`deskops.md:109`).
- **Identidad**: ruta de dominio; `Model:name` en el lector: no definido; productor WS11.
- **Contrato**: CrossroadDoc (`deskops.md:187`). Los namespaces están en un archivo YAML (`deskops.md:109`): sin contrato de documento.
- **Campos y relaciones**: padres exigidos al crear (`deskops.md:118`); relación padre-hijo: no definido más allá de `atoms tree` (`deskops.md:121`); productor WS11.
- **Renderer existente o requerido**: sin renderer de árbol de dominio en la UI; la vista genérica de WS24 incluye crossroads (`dag.yaml:1574-1590`).
- **Navegación**: abrir padres e hijos reales, no una jerarquía por carpeta arbitraria (tabla 2); la clasificación no se infiere por carpeta (`dag.yaml:1574-1590`).
- **Acción/dueño**: `atoms crossroad` crea; `atoms tree` y `atoms validate --all` leen (`deskops.md:118,121,113`); dueño deskops.
- **Destino de escritura**: CrossroadDoc bajo `desk/atoms` por deskops (`deskops.md:118`). Desde UI: no definido; productor WS12.
- **Error**: condicionado a WS24/WS12: crear exige padres (`deskops.md:118`); en la UI: no definido; productor WS12.
- **Estado**: bloqueado. Necesita WS24 y WS12.
- **Clase**: authored (crossroad, namespaces); derivado (árbol, validación).
- **UF**: UF02 (`user-flows.md:45`).
- **Evidencia**: `deskops.md:109,113,118,121,187,234`; `dag.yaml:1565-1590`; `user-flows.md:45`.

### F14 — Issue Markdown sin modelo

- **Propósito humano**: leer y operar issues sin tratarlos como TaskDoc (tabla 2).
- **Origen**: `issue-*.md` en `desk/issues` y `desk/drawer/issues` (`deskops.md:49`). `desk/issues` no existe; `desk/drawer/issues` existe y está vacío (`deskops.md:232`).
- **Identidad**: ruta del archivo; sin `Model:name`. Identidad en el lector: no definido; productor WS11.
- **Contrato**: sin contrato; la visión los define deliberadamente no modelados (`vision.md:36`, leída solo esa línea por búsqueda de texto).
- **Campos y relaciones**: `status` y resolución con fecha, razón y refs (`deskops.md:48`). Otros: no definido; productor WS11.
- **Renderer existente o requerido**: Markdown fuente/render sin modelo: ausente (`ui.md:55`); productor WS13.1 (`dag.yaml:860`). Lista por `issue list` en la UI: sin productor en el DAG, repo dueño graph_ui; contrato de lectura WS11.
- **Navegación**: no definido; productor WS11.
- **Acción/dueño**: `issue list` y `issue close` (`--force` reabre) por autoridad deskops (`deskops.md:48-49`; tabla 2).
- **Destino de escritura**: el archivo del issue, reescrito por `issue close` (`deskops.md:48`). Desde UI: no definido; productor WS12.
- **Error**: no definido; productor WS11. Condicionado: sin issues, la lista queda vacía (`deskops.md:232`).
- **Estado**: bloqueado. Necesita WS13.1 (Markdown sin modelo) y WS11.
- **Clase**: authored (issue); derivado (lista filtrada por status).
- **UF**: ninguna: `user-flows.md` no menciona issues (búsqueda de texto sin coincidencias).
- **Evidencia**: `deskops.md:48-49,232`; `ui.md:55`; `dag.yaml:841-871`; `user-flows.md` sin referencia.

### F15 — DeskFAQDoc

- **Propósito humano**: orientarse con preguntas y respuestas del desk, buscar y abrirlas (tabla 2).
- **Origen**: `desk/faq` existe y está vacío; DeskFAQDoc tiene 0 documentos; `deskops faq` lee `docs/faq.md`, no este modelo (`deskops.md:188,233,33`).
- **Identidad**: no definido; productor WS11.
- **Contrato**: DeskFAQDoc (`deskops.md:188`).
- **Campos y relaciones**: no leídos en las auditorías; no definido; productor WS11.
- **Renderer existente o requerido**: no definido; contrato WS11, implementación WS13.1 (el FAQ Markdown de WS40 se lee como Markdown, `dag.yaml:2690`). Navegación de preguntas: sin productor en el DAG, repo dueño graph_ui (`dag.yaml` nombra FAQ en WS02, WS09 y WS40, líneas 356, 620 y 2690; ninguno produce esa navegación).
- **Navegación**: orientación, buscar y abrir (tabla 2); no definido más allá; productor WS11.
- **Acción/dueño**: `list/show/add/edit faq-doc` (`deskops.md:59,70,84,95`); dueño deskops. Edición bajo contrato.
- **Destino de escritura**: `desk/faq/<id>.md` por `add faq-doc`, que no lo trackea en el acto (`deskops.md:59`). Desde UI: no definido; productor WS12.
- **Error**: no definido; productor WS11. Condicionado: con 0 documentos no hay orientación que mostrar, y el comando `faq` lee otra fuente (`deskops.md:233`).
- **Estado**: bloqueado. WS40 crea un FAQ Markdown en el corpus para la entrada mínima (`dag.yaml:2690`), y su lectura necesita WS40, WS13.1 y el contrato WS11.
- **Clase**: authored (preguntas); derivado (índice de preguntas, búsqueda).
- **UF**: ninguna explícita: `user-flows.md` no menciona FAQ (búsqueda de texto sin coincidencias). WS40 la usa como enlace de la entrada mínima que prueba WS16 (`dag.yaml:2690`).
- **Evidencia**: `deskops.md:33,59,70,84,95,188,233`; `dag.yaml:356,620,2690`; `user-flows.md` sin referencia.

### F16 — StepDoc y pills

- **Propósito humano**: consultar una referencia o paso y su contexto vinculado, y aplicar la operación soportada (tabla 2).
- **Origen**: StepDoc, 0 documentos (`deskops.md:200`); PillDoc, 29 en `desk/contexts` (`deskops.md:191,218`).
- **Identidad**: `Model:name` en el lector: no definido; productor WS11. Id de pill inmutable en `edit` (`deskops.md:63`).
- **Contrato**: StepDoc y PillDoc (`deskops.md:191,200`).
- **Campos y relaciones**: `task.pills` agrega la ruta de la pill (`deskops.md:73`). Campos de pill y de paso: no leídos en las auditorías; no definido; productor WS11.
- **Renderer existente o requerido**: StepDoc: ausente (`ui.md:68`), productor WS23. Pills: vista genérica registrada en `shell/registry.js` (`dag.yaml:1574-1590`), productor WS24.
- **Navegación**: contexto vinculado desde la tarea o el procedimiento: no definido; productor WS11.
- **Acción/dueño**: `list/show/add/edit pill`, `bind pill`, `list/show/add/edit step` (`deskops.md:52,63,73,77,85,88,96`); dueño deskops.
- **Destino de escritura**: el documento de pill o paso, y `task.pills` por `bind pill` (`deskops.md:73`). Desde UI: no definido; productor WS12.
- **Error**: no definido; productor WS23 (pasos) y WS24 (pills). Condicionado: con 0 StepDoc no hay pasos que mostrar.
- **Estado**: bloqueado. Necesita WS23 y WS24.
- **Clase**: authored (pill, paso); derivado (pills vinculadas a una tarea, resultado de la referencia).
- **UF**: UF04 (`user-flows.md:97-98`), UF02 (`user-flows.md:44`), UF05 (renderer de StepDoc, `user-flows.md:129`).
- **Evidencia**: `deskops.md:52,63,73,77,85,88,96,191,200,218`; `ui.md:68`; `dag.yaml:1526,1565`; `user-flows.md:44,97-98,129`.

### F17 — Código local referenciado

- **Propósito humano**: ver, solo lectura, el archivo o rango que un documento referencia, junto a su soporte.
- **Origen**: `files` y `references` del payload del documento (`ui.md:55`; `reconciliacion.md:51`). Las anclas `code:<ruta>::<símbolo>` son otra capacidad (`infraestructura.md:94`).
- **Identidad**: ruta del archivo con límites de repo, gitignore, binario y tamaño (`reconciliacion.md:5,51`). Identidad de rango y correspondencia nodo-código: no definido; productor de contrato WS11 (`dag.yaml:857-859`).
- **Contrato**: sin contrato.
- **Campos y relaciones**: lee `files`/`references`, no el archivo propio del documento (`ui.md:55`). Mapeo texto-código: no definido; productor WS11; no se inventa.
- **Renderer existente o requerido**: base existente: `_build_code_projection` y `_inspect_file_reference` en la pestaña Código (`ui.md:55,77`; `reconciliacion.md:51`). Soporte de rango dentro del archivo: no leído; no definido; productor WS11. Sin CST supuesto; Tree-sitter queda diferido (`ui.md:183`).
- **Navegación**: foco compartido entre Code, texto y graph solo donde exista correspondencia real de origen definida por WS11 (`dag.yaml:857-859,865-867`); no se inventa mapeo texto-código.
- **Acción/dueño**: leer. Sin edición; el anclaje y la edición de código están en un candidato diferido (`ui.md:46`).
- **Destino de escritura**: ninguno.
- **Error**: condicionado a WS11 y WS13.1: archivo excluido por repo, gitignore, binario o tamaño (`reconciliacion.md:5`). Mensaje y forma: no definido; productor WS11.
- **Estado**: bloqueado. La base existente no basta: origen y foco necesitan el contrato WS11 y WS13.1 (`dag.yaml:841-871`).
- **Clase**: derivado (proyección del archivo referenciado); preferencia local (foco y selección).
- **UF**: ninguna lo usa de forma explícita. UF07 nombra anclas a código (`user-flows.md:171`) y UF05 la apertura de soporte (`user-flows.md:126`); no se afirma equivalencia con esta fila.
- **Evidencia**: `ui.md:46,55,77,183`; `reconciliacion.md:5,51`; `infraestructura.md:94`; `dag.yaml:841-871`; `user-flows.md:126,171`.

### F18a — SpecDoc y NotationDoc

- **Propósito humano**: leer una especificación y su notación como documento o gráfico soportado, reutilizando Specs.
- **Origen**: SpecDoc/SpecNodeDoc materializados por `spec2viz diagram sync`; la fuente es un spec YAML (`infraestructura.md:35`); NotationDoc: 8 builtin (`infraestructura.md:132`).
- **Identidad**: `Model:name`; SpecDoc con `sha256` del spec (`infraestructura.md:35`).
- **Contrato**: SpecDoc y NotationDoc registrados por `diagram sync` y `notation sync` (`infraestructura.md:100`). SurfaceDoc no es una pantalla (línea 22 de este archivo).
- **Campos y relaciones**: campo `notation` del SpecDoc, glifos y links (`infraestructura.md:100`).
- **Renderer existente o requerido**: renderers de spec2viz por CLI: 9 (`infraestructura.md:134`). La vista Specs de Mindmap la nombra la visión (`vision.md:36`, leída solo esa línea por búsqueda de texto) y no tiene fila en `ui.md`: sin productor en el DAG, repo dueño graph_ui; si entra al lector, contrato WS11.
- **Navegación**: no definido; productor WS11.
- **Acción/dueño**: reutilizar Specs; render y validación por `spec2viz`; dueño spec2viz.
- **Destino de escritura**: sync escribe por `sldb.api` (`infraestructura.md:35`). Desde UI: no definido; productor WS12.
- **Error**: no definido; productor WS11.
- **Estado**: bloqueado. Necesita el contrato WS11 para navegación y para decidir si la vista Specs entra en el lector. Tiene contrato de modelo, no de UI. WS18 solo crea ViewDoc y NotationDoc concretos (`dag.yaml:1225`).
- **Clase**: authored (spec YAML, SpecDoc, NotationDoc); derivado (render y gráfico).
- **UF**: ninguna: `user-flows.md` no menciona specs ni notaciones (búsqueda de texto sin coincidencias).
- **Evidencia**: `infraestructura.md:35,100,132,134`; `dag.yaml:1225`; `user-flows.md` sin referencia.

### F18b — ViewDoc (grafo portable)

- **Propósito humano**: ver un subgrafo seleccionado por modelos y predicados con una notación. ViewDoc es solo grafo, no contrato universal de UI.
- **Origen**: modelo `ViewDoc` en spec2viz, 0 documentos en su store (`infraestructura.md:149-150`); evaluador, rutas y guardado en graph_ui, solo modo local (`ui.md:104-106`).
- **Identidad**: `ViewDoc:<name>`; referencia `NotationDoc:<n>` (`infraestructura.md:99,149`).
- **Contrato**: `ViewDoc` (`infraestructura.md:149`).
- **Campos y relaciones**: `nodes` (`{model, where}`), `relations`, `direction`, `notation`, `layout` (`infraestructura.md:149`). Selección mínima concreta: no fijada aquí. Debe fijarla WS11 y WS18 se detiene si falta (`dag.yaml:1232-1235`).
- **Renderer existente o requerido**: base existente: `evaluate_view`, `GET /api/views`, `POST /api/views/evaluate`, `POST /api/views/save` (`ui.md:104-105`) y el dibujo en `apps/review-workbench`, no leído (`ui.md:108`). Ningún renderer de spec2viz lo consume (`infraestructura.md:153`).
- **Navegación**: no definido; productor WS11. Su extensión al grafo del workspace es opcional y posterior a G_SPEC_VIEW (`dag.yaml:1574-1590`).
- **Acción/dueño**: evaluar y guardar vistas en graph_ui; autoría de ViewDoc y NotationDoc concretos: WS18 (`dag.yaml:1212-1244`, owner_repo spec2viz).
- **Destino de escritura**: `save_view` por la API de sldb, sin `expected` (`ui.md:105`); ruta `sldb/views/` confirmada por WS18 (`dag.yaml:1222`).
- **Error**: condicionado a WS18: en modo remote responde 501 «Las vistas solo existen en modo local» (`ui.md:106`); sin spec2viz instalado, `notation.error` lo dice (`ui.md:107`). Contrato de error de UI: no definido; productor WS11.
- **Estado**: bloqueado. Necesita WS18 (G_SPEC_VIEW) y el contrato WS11.
- **Clase**: authored (definición del ViewDoc); derivado (resultado evaluado, subgrafo); preferencia local (disposición del gráfico).
- **UF**: ninguna: `user-flows.md` no menciona ViewDoc (búsqueda de texto sin coincidencias).
- **Evidencia**: `infraestructura.md:99,149-153`; `ui.md:104-108`; `dag.yaml:1212-1244,1574-1590`; `user-flows.md` sin referencia.

### F19a — Schema y edición de clase existentes

- **Propósito humano**: inspeccionar y editar un draft de clase con las herramientas que ya existen.
- **Origen**: modelos registrados (`sldb models list`, 17, `deskops.md:181`); editor `MS`, `class-dialog.js` y `views/models/diagram/` (`ui.md:85`).
- **Identidad**: modelo o clase; en el lector: no definido; productor WS11.
- **Contrato**: sin contrato de UI documentado; operaciones `template_edit`, `fields_add`, `fields_remove`, `validate`, `promote` y `POST /api/models/*` (`ui.md:85`).
- **Campos y relaciones**: campos, referencias y template de la clase (`user-flows.md:206`).
- **Renderer existente o requerido**: base existente: vista Schema (`ui.md:85`; `reconciliacion.md:78`).
- **Navegación**: dentro de la vista Schema del KB map; acceso desde el lector: ver F19b.
- **Acción/dueño**: draft, validate y promote públicos de sldb (tabla 2); dueño sldb.
- **Destino de escritura**: el draft del modelo en el store por la API de modelos (`ui.md:85`).
- **Error**: no definido; productor WS12 (efectos y errores de draft/validate/promote, `user-flows.md:217`).
- **Estado**: bloqueado. Necesita el contrato WS12 para efectos y errores de draft, validate y promote. El capítulo 15 conserva su etiqueta propuesta, fijada por el plan (`manual.md:163`); esta ficha mide la fila. El acceso desde el lector va en F19b.
- **Clase**: authored (clase, template, draft); derivado (inventario de modelos).
- **UF**: UF09 (`user-flows.md:211-212`).
- **Evidencia**: `ui.md:85`; `deskops.md:181`; `reconciliacion.md:78`; `user-flows.md:206,211-212,217`.

### F19b — Acceso desde el documento y promoción con autoridad

- **Propósito humano**: desde un documento abrir su Schema/clase de origen, editar el draft, validar y promover solo con autoridad y evidencia (`user-flows.md:206`).
- **Origen**: panel Context del lector, que no tiene acceso al Schema (`ui.md:85`: ausente).
- **Identidad**: Schema/clase origen del documento activo: no definido; productor WS11 y WS39.
- **Contrato**: no definido; productor WS12 (autoridad, efectos y errores de promote) y WS39.
- **Campos y relaciones**: los de F19a, más la relación documento-clase de origen: no definido; productor WS11.
- **Renderer existente o requerido**: acceso desde Context ausente (`ui.md:85`); productor WS39 (graph_ui, `dag.yaml:2630-2660`).
- **Navegación**: del documento activo a su Schema/clase origen (`dag.yaml:2630-2660`).
- **Acción/dueño**: promover solo con autoridad; WS39 no habilita promover si falta la API o la autoridad (`dag.yaml:2630-2660`). RoleDoc y RuntimeProfileDoc no se editan (`deskops.md:197,199`). Dueño: sldb, con UI graph_ui.
- **Destino de escritura**: draft y promoción por API pública de sldb; no por payload libre (`user-flows.md:206`). Canal: no definido; productor WS12.
- **Error**: no definido; productor WS12 (contrato) y WS39 (prueba) (`user-flows.md:217`).
- **Estado**: bloqueado. Necesita WS39 y WS12; el capítulo 15 del manual ya es propuesto hasta la prueba humana de WS39 (`manual.md:163`).
- **Clase**: authored (draft promovido); derivado (impacto); preferencia local (foco).
- **UF**: UF09 (`user-flows.md:204-219`).
- **Evidencia**: `ui.md:85`; `deskops.md:197,199`; `dag.yaml:2630-2660`; `manual.md:163`; `user-flows.md:206,213-219`.

### F20 — Historial y diff Git

- **Propósito humano**: abrir la evidencia de cambios junto al documento o la tarea, de solo lectura (tabla 2).
- **Origen**: historia por documento con `sldb docs history` (`infraestructura.md:60`); diff por repo y tarea ausente (`ui.md:77`), a partir de `TaskDoc.references` y `files` (`reconciliacion.md:72`).
- **Identidad**: documento (historia) o tarea y repo (diff); en el lector: no definido; productor WS11.
- **Contrato**: sin contrato.
- **Campos y relaciones**: versiones comprometidas de Git (`infraestructura.md:60`); repos de la tarea: no definido; productor WS11.
- **Renderer existente o requerido**: ausente. La proyección Code no es diff (`ui.md:77`); `_read_git_history` está en `frontends/workspace/`, sin commit y no adoptado (`ui.md:77,158`; `reconciliacion.md:77`). Productor WS27.1 (`dag.yaml:1887`, graph_ui).
- **Navegación**: abrir la revisión junto al documento o la tarea; distinto de Changes e integridad, que son WS29 (tabla 2; `dag.yaml:2011`).
- **Acción/dueño**: solo lectura, sin revert destructivo (tabla 2).
- **Destino de escritura**: ninguno.
- **Error**: condicionado a WS27.1: fuera de Git, `sldb docs history` devuelve vacío (`infraestructura.md:60`). Forma del error: no definido; productor WS11.
- **Estado**: bloqueado. Necesita WS27.1.
- **Clase**: derivado.
- **UF**: UF05 (diff comparable con el contrato, `user-flows.md:118,125`), UF07 (`sldb docs history`, `user-flows.md:171`).
- **Evidencia**: `infraestructura.md:60`; `ui.md:77,158`; `reconciliacion.md:72,77`; `dag.yaml:1887,2011`; `user-flows.md:118,125,171`.
