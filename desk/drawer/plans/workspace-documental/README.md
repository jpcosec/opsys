# Workspace documental — plan final documental

Revisión 9. Estado: final_plan_reviewed. Planificación final; no activación ni ejecución de producto.

## Reviews baratos

El concilio conserva APTO COMO PLAN como revisión experta; no acredita contexto cero barato. Estado por nodo (raíz, paquetes y candidatas): pending: 1, reviewed: 72. Evidencia en `runs/subagents/20261031-workspace-context-reviews/context-review/`; protocolo `ritual-context-review`. Un review vigente prueba comprensión del encargo: no promueve nodos ni satisface gates. `execution_authorized=false`.

## Jerarquía de revisión

ROOT y PK agrupan la revisión; no son dependencias. Un nodo `aggregate` no se ejecuta y termina con sus hijos.

- **PK01 Fundamentos y auditoría**: WS01, WS02, WS03, WS04, WS05, WS06
- **PK02 Decisiones y contratos**: WS07, WS08, WS09, WS10, WS11, WS12
- **PK03 Lector y descubrimiento**: WS13, WS14, WS15, WS16, WS40, WS41
- **PK04 Navegación y representaciones**: WS17, WS18, WS22, WS23, WS24
- **PK05 Autoría y operación manual**: WS19, WS20, WS21, WS45, WS25, WS26, WS27, WS28, WS30, WS42
- **PK06 Publicación básica**: WS31, WS43
- **PK07 Extensiones independientes**: WS29, WS39
- **PK08 Ramal Scion opcional**: WS32, WS33, WS34, WS35, WS36, WS37, WS38, WS44

## Entrada

- [Cierre y secuencia del plan](cierre.md): base acordada, trabajo cubierto y próximos deltas.
- [Brief y glosario](brief.md): requisitos autosuficientes, sin chat ni memoria privada necesaria.
- [Decisiones](decisiones.md): decisiones humanas registradas y defaults técnicos delegados; APIs y aceptación de uso siguen pendientes.
- [Alcance](alcance.md): lector, autoría manual, Scion opcional y exclusiones.
- [Reconciliación](reconciliacion.md): cómo integrar trabajo activo sin duplicarlo.
- [Cobertura de user-flows](cobertura.md) y [validación humana](validacion-humana.md).

Base acordada: sldb/pron + Deskops + Mindmap existentes; Kimun es referencia, no migración ni dependencia de este DAG. WS07 reutiliza el registro literal ya resuelto; no repetir decisiones sin cambio real. El plan no se apoya en decisiones que solo estén en la memoria de un agente.

## Documentos que podemos escribir ahora

[Visión](borradores/vision.md), [user-flows](borradores/user-flows.md), [catálogo de vistas](borradores/vistas.md) e [índice del manual](borradores/manual.md) tienen semilla de intención. WS01 ya fija vocabulario/fuentes con recibo documental; WS02–05 auditan; WS08–10 convierten intención en contratos contrastados. Un borrador existente no equivale a tarea cerrada, aprobación humana o función disponible.

## DAG y candidatas

[dag.yaml](dag.yaml) es la única fuente de IDs/aristas/gates/metadatos. Esta tabla, las fichas de candidatas y las proyecciones se generan. No corregir dependencias solo en README o Mermaid. Las fichas están en drawer y requieren promoción formal en su repo dueño antes de ejecución. Tamaños S/M son relativos, no promesas de horas.

| ID | Entregable | Depende de tareas | Gates adicionales | Repo dueño | Tamaño |
|---|---|---|---|---|---|
| WS01 | [Fijar brief y glosario autosuficientes](../../tasks/workspace-documental/task-ws01.md) | — | — | deskops | S |
| WS02 | [Inventariar superficies y operaciones Deskops](../../tasks/workspace-documental/task-ws02.md) | WS01 | — | deskops | M |
| WS03 | [Inventariar persistencia, consultas y notaciones](../../tasks/workspace-documental/task-ws03.md) | WS01 | — | deskops | M |
| WS04 | [Inventariar UI y reconciliar trabajo en curso](../../tasks/workspace-documental/task-ws04.md) | WS01 | — | deskops | M |
| WS05 | [Inventariar identidad y API Scion](../../tasks/workspace-documental/task-ws05.md) | WS01 | — | deskops | M |
| WS06 | [Proponer correspondencia de alcance con repos dueños](../../tasks/workspace-documental/task-ws06.md) | WS02, WS03, WS04 | — | deskops | S |
| WS07 | [Mantener registro trazado de decisiones acordadas](../../tasks/workspace-documental/task-ws07.md) | WS06 | — | deskops | M |
| WS08 | [Precisar user-flows y criterios observables](../../tasks/workspace-documental/task-ws08.md) | WS07 | G_PRODUCT | deskops | M |
| WS09 | [Precisar catálogo de renderizaciones](../../tasks/workspace-documental/task-ws09.md) | WS07, WS10, WS08 | G_PRODUCT | deskops | M |
| WS10 | [Precisar índice y convención del manual](../../tasks/workspace-documental/task-ws10.md) | WS02, WS07 | G_PRODUCT | deskops | S |
| WS11 | [Cerrar contrato de navegación e identidad](../../tasks/workspace-documental/task-ws11.md) | WS09, WS08 | G_PRODUCT | deskops | M |
| WS12 | [Cerrar contrato de operaciones y escritura](../../tasks/workspace-documental/task-ws12.md) | WS11, WS08 | G_WRITE_POLICY | deskops | M |
| WS13 | [Integrar lector workspace con historia y foco](../../tasks/workspace-documental/task-ws13.md) | WS11, WS13.1, WS13.2, WS13.3 | G_UI_READ | graph_ui | M |
| WS13.1 | [Leer documento, contexto y enlaces](../../tasks/workspace-documental/task-ws13-1.md) | WS11 | G_UI_READ | graph_ui | M |
| WS13.2 | [Explorar documentos modelados y no modelados](../../tasks/workspace-documental/task-ws13-2.md) | WS11, WS13.1 | G_UI_READ | graph_ui | S |
| WS13.3 | [Abrir documentos en pestañas y divisiones con historia](../../tasks/workspace-documental/task-ws13-3.md) | WS11, WS13.1 | G_UI_READ | graph_ui | S |
| WS14 | [Integrar búsqueda navegable del workspace](../../tasks/workspace-documental/task-ws14.md) | WS13 | G_UI_READ | graph_ui | M |
| WS15 | [Mostrar errores de lectura y modo degradado](../../tasks/workspace-documental/task-ws15.md) | WS13, WS15.1, WS15.2 | G_UI_READ | graph_ui | S |
| WS15.1 | [Mostrar errores de lectura y modo degradado](../../tasks/workspace-documental/task-ws15-1.md) | WS13 | G_UI_READ | graph_ui | S |
| WS15.2 | [Orientar proyecto sin desk](../../tasks/workspace-documental/task-ws15-2.md) | WS13 | G_UI_READ | graph_ui | S |
| WS16 | [Validar con humano lectura y descubrimiento](../../tasks/workspace-documental/task-ws16.md) | WS14, WS15, WS08, WS40, WS41 | — | graph_ui | M |
| WS17 | [Escribir entradas e índices del desk ejemplo](../../tasks/workspace-documental/task-ws17.md) | WS11, WS40 | — | deskops | S |
| WS18 | [Declarar proyecciones de grafo reutilizables](../../tasks/workspace-documental/task-ws18.md) | WS09, WS11 | G_SPEC_VIEW | spec2viz | S |
| WS19 | [Integrar edición de campos con conflicto](../../tasks/workspace-documental/task-ws19.md) | WS12, WS19.1, WS19.2 | G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS19.1 | [Editar campos con conflicto visible](../../tasks/workspace-documental/task-ws19-1.md) | WS12 | G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS19.2 | [Editar relaciones permitidas por contrato](../../tasks/workspace-documental/task-ws19-2.md) | WS12 | G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS20 | [Comprobar o completar guardado fuente reversible](../../tasks/workspace-documental/task-ws20.md) | WS12 | G_SLDB_WRITE, G_WRITE_CONTRACT | sldb | M |
| WS21 | [Integrar fuente y renderizado según source_mode](../../tasks/workspace-documental/task-ws21.md) | WS19 | G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS22 | [Renderizar Board como trabajo navegable](../../tasks/workspace-documental/task-ws22.md) | WS13, WS09 | G_UI_READ | graph_ui | M |
| WS23 | [Renderizar rituales y pasos como procedimiento](../../tasks/workspace-documental/task-ws23.md) | WS13, WS09 | G_UI_READ | graph_ui | S |
| WS24 | [Integrar conocimiento y grafo local](../../tasks/workspace-documental/task-ws24.md) | WS13, WS09 | G_UI_READ | graph_ui | M |
| WS25 | [Integrar captura y triage en UI](../../tasks/workspace-documental/task-ws25.md) | WS12, WS25.1, WS25.2 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS25.1 | [Leer inbox y registrar ack o respuesta local](../../tasks/workspace-documental/task-ws25-1.md) | WS12 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | S |
| WS25.2 | [Capturar en drawer o protoátomo](../../tasks/workspace-documental/task-ws25-2.md) | WS12 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | S |
| WS26 | [Integrar autoría y contexto de tareas](../../tasks/workspace-documental/task-ws26.md) | WS12, WS22, WS26.1, WS26.2 | G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS26.1 | [Autorar tarea, evidencia y contexto](../../tasks/workspace-documental/task-ws26-1.md) | WS12, WS22 | G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS26.2 | [Enrutar en Board y mostrar capa lista](../../tasks/workspace-documental/task-ws26-2.md) | WS12, WS22, WS26.1 | G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS27 | [Integrar revisión de cambios y evidencia](../../tasks/workspace-documental/task-ws27.md) | WS13, WS12, WS27.1, WS27.2 | G_UI_READ | graph_ui | M |
| WS27.1 | [Mostrar diff Git por repo y tarea](../../tasks/workspace-documental/task-ws27-1.md) | WS13, WS12 | G_UI_READ | graph_ui | M |
| WS27.2 | [Mostrar evidencia declarada, encontrada y verificada](../../tasks/workspace-documental/task-ws27-2.md) | WS13, WS12 | G_UI_READ | graph_ui | S |
| WS28 | [Integrar verificación y handoff de cierre](../../tasks/workspace-documental/task-ws28.md) | WS27, WS12 | G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS29 | [Integrar Changes e impacto comprobable](../../tasks/workspace-documental/task-ws29.md) | WS15, WS24 | G_UI_READ | graph_ui | M |
| WS30 | [Validar autoría y revisión manual completas](../../tasks/workspace-documental/task-ws30.md) | WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42 | — | graph_ui | M |
| WS31 | [Publicar manual documental básico probado](../../tasks/workspace-documental/task-ws31.md) | WS30, WS10, WS43 | G_HUMAN_MANUAL | deskops | M |
| WS32 | [Unificar identidad de intento y cierre Scion](../../tasks/workspace-documental/task-ws32.md) | WS05, WS12, WS32.1, WS32.2 | G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS32.1 | [Separar identidad de intento y dispatch](../../tasks/workspace-documental/task-ws32-1.md) | WS05, WS12 | G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS32.2 | [Hacer idempotente manifiesto y cierre](../../tasks/workspace-documental/task-ws32-2.md) | WS05, WS12, WS32.1 | G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS33 | [Vincular mensajes, resultados y decisiones](../../tasks/workspace-documental/task-ws33.md) | WS32, WS11, WS33.1, WS33.2 | G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS33.1 | [Vincular mensajes y resultados al intento](../../tasks/workspace-documental/task-ws33-1.md) | WS32 | G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS33.2 | [Registrar decisión humana explícita](../../tasks/workspace-documental/task-ws33-2.md) | WS32, WS33.1 | G_SCION, G_WRITE_CONTRACT | deskops | S |
| WS34 | [Exponer despacho y respuesta Scion autorizados](../../tasks/workspace-documental/task-ws34.md) | WS33, WS12, WS34.1, WS34.2 | G_EXEC, G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS34.1 | [Exponer dispatch autorizado](../../tasks/workspace-documental/task-ws34-1.md) | WS33, WS12 | G_EXEC, G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS34.2 | [Exponer respuesta autorizada](../../tasks/workspace-documental/task-ws34-2.md) | WS33, WS12, WS34.1 | G_EXEC, G_SCION, G_WRITE_CONTRACT | deskops | S |
| WS35 | [Mostrar ejecución y trazabilidad en workspace](../../tasks/workspace-documental/task-ws35.md) | WS33, WS27 | G_SCION, G_UI_READ | graph_ui | M |
| WS36 | [Integrar delegación e intervención humanas](../../tasks/workspace-documental/task-ws36.md) | WS34, WS35 | G_EXEC, G_SCION, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS37 | [Validar delegación con agente real](../../tasks/workspace-documental/task-ws37.md) | WS36, WS30 | G_EXEC, G_SCION | graph_ui | M |
| WS38 | [Publicar capítulos verificados de delegación](../../tasks/workspace-documental/task-ws38.md) | WS37, WS31 | G_HUMAN_DELEGATE | deskops | S |
| WS39 | [Integrar inspección y edición de modelos existente](../../tasks/workspace-documental/task-ws39.md) | WS12, WS13 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS40 | [Crear generador reproducible del corpus Taller](../../tasks/workspace-documental/task-ws40.md) | WS11, WS08 | G_UI_READ | graph_ui | M |
| WS41 | [Implementar lectura segura entre desks](../../tasks/workspace-documental/task-ws41.md) | WS13, WS11, WS40 | G_UI_READ | graph_ui | M |
| WS42 | [Integrar operaciones de conocimiento existentes](../../tasks/workspace-documental/task-ws42.md) | WS19, WS24, WS12 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS43 | [Publicar navegación documental del desk real](../../tasks/workspace-documental/task-ws43.md) | WS17, WS30 | G_HUMAN_MANUAL, G_PRODUCT, G_WRITE_CONTRACT | deskops | S |
| WS44 | [Comprobar y revalidar acceso público a Scion](../../tasks/workspace-documental/task-ws44.md) | WS05, WS07 | G_PRODUCT | deskops | S |
| WS45 | [Verificar o completar la precondición de escritura de payload](../../tasks/workspace-documental/task-ws45.md) | WS12 | G_SLDB_WRITE, G_WRITE_CONTRACT | sldb | M |

## Gates externos y humanos

| Gate | Estado observado | Significado | Resolver |
|---|---|---|---|
| G_PRODUCT | satisfied | Decisiones de producto registradas por humano | WS07 |
| G_CLOSEOUT | satisfied | Contrato de evidencia de closeout estabilizado | independent tester focalizado / recibo actual del contrato |
| G_SOURCE | pending | Fuente reversible y guardas de campos probadas | WS20 |
| G_PAYLOAD_PRECONDITION | pending | Precondicion de escritura de payload verificada en sldb | WS45 |
| G_SCION | unverified | Scion accesible y contrato público comprobado | WS44, operador a designar al abordar ramal E |
| G_EXEC | pending | Humano autoriza ejecución y comunicaciones del escenario | external |
| G_HUMAN_READ | pending | Persona aprueba recorrido de lectura | WS16 |
| G_HUMAN_MANUAL | pending | Persona aprueba autoría/revisión | WS30 |
| G_HUMAN_DELEGATE | pending | Persona aprueba delegación | WS37 |
| G_WRITE_POLICY | satisfied | Política de escritura aprobada por humano | WS07 |
| G_WRITE_CONTRACT | pending | Contrato técnico de operaciones verificado | WS12 |
| G_UI_READ | pending | Deltas de lectura aceptados en graph_ui | external: solicitante P01 receptor del repo al preparar/promover el delta concreto |
| G_UI_WRITE | pending | Deltas de mutación aceptados en graph_ui | external: solicitante P01 receptor del repo al preparar/promover el delta concreto |
| G_SLDB_WRITE | pending | Alcance fuente aceptado en sldb | external: solicitante P01 receptor del repo al preparar/promover el delta concreto |
| G_SPEC_VIEW | pending | Alcance de proyecciones aceptado en spec2viz | external: solicitante P01 receptor del repo al preparar/promover el delta concreto |
| G_HUMAN_MODEL | pending | Persona valida inspección/edición de modelos | WS39 |

Cada output_scope se resuelve respecto de su output_base explícito; las actas de uso viven en repo dueño. Los productores de gates también se declaran en dag.yaml, sin aristas ocultas en generador. source_mode determina la variante WS21 y si WS20 pertenece a la entrega; pending bloquea ambos. Los gates se satisfacen con el tipo de evidencia declarado, nunca por existencia del archivo. El validador comprueba referencias, ausencia de ciclos y coherencia de proyecciones; muestra por separado candidatas de preparación, bloqueos y autorización. Cero nodos tienen ejecución de producto autorizada. Las capas topológicas no son fases operativas: falta aprobar gates, no solapamiento, TaskDoc y cierre de cada fase. Las observaciones de referencias tienen hash para detectar movimiento, no para aprobar trabajo.

## Entregas y gates de uso

WS13–16 y WS40/41 dan lector con búsqueda y errores antes de edición o índices nuevos. WS40 produce corpus temporal y WS17 aporta solo plantillas de entradas authored. WS19–28, WS42 y WS30 dan autoría/revisión manual; WS31 publica su manual. WS29 (Changes) y WS39 (Schema) son extensiones con aceptación propia, no prerrequisitos del lector o manual básico. WS32–38 son el ramal de Scion con permisos de ejecución explícitos. El cierre baseline usa handoff verificado al CLI/coordinador, no commit desde HTTP.

## Reproducción y revisión

`python desk/drawer/plans/workspace-documental/build_plan.py` genera tabla/fichas/spec del diagrama. `python desk/drawer/plans/workspace-documental/validate_plan.py` verifica coherencia. `python desk/drawer/plans/workspace-documental/render_diagram.py` genera Mermaid y HTML mediante spec2viz. El modo `build_plan.py --check` no escribe y detecta proyecciones obsoletas.

[Diagrama interactivo](dag.diagram.graph.html) · [Mermaid](dag.diagram.mmd) · [Validación](validation.txt). El diagrama incluye gates como nodos; leer flechas de prerequisito a dependiente, sin confundir estado pendiente con implementación.

Revisiones independientes y resolución de hallazgos en [reviews](reviews/README.md). Los IDs antiguos A1–H2 se conservan en legacy_mapping de dag.yaml para trazabilidad, no como otro DAG activo. No se modificaron tareas ajenas ni el Board de graph_ui.
