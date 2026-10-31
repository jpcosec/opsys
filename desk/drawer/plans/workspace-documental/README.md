# Workspace documental — plan revisado por concilio

Revisión 5. Estado: reviewed_plan_pending_decisions. Propuesta de planificación, no activación ni ejecución de producto.

## Entrada

- [Brief y glosario](brief.md): requisitos autosuficientes, sin chat ni memoria privada necesaria.
- [Decisiones](decisiones.md): alternativas, humano responsable y evidencia requerida; pendientes explícitas.
- [Alcance](alcance.md): lector, autoría manual, Scion opcional y exclusiones.
- [Reconciliación](reconciliacion.md): cómo integrar trabajo activo sin duplicarlo.
- [Cobertura de user-flows](cobertura.md) y [validación humana](validacion-humana.md).

Baseline propuesta: sldb/pron + Deskops + Mindmap existentes; Kimun es referencia, no migración ni dependencia de este DAG. El humano resuelve las propuestas en WS07 antes de código afectado. El plan no se apoya en decisiones que solo estén en la memoria de un agente.

## Documentos que podemos escribir ahora

[Visión](borradores/vision.md), [user-flows](borradores/user-flows.md), [catálogo de vistas](borradores/vistas.md) e [índice del manual](borradores/manual.md) tienen semilla de intención. WS01 aclara vocabulario/fuentes y WS02–05 auditan; WS08–10 convierten intención en contratos contrastados. Un borrador existente no equivale a tarea cerrada, aprobación humana o función disponible.

## DAG y candidatas

[dag.yaml](dag.yaml) es la única fuente de IDs/aristas/gates/metadatos. Esta tabla, las fichas de candidatas y las proyecciones se generan. No corregir dependencias solo en README o Mermaid. Las fichas están en drawer y requieren promoción formal en su repo dueño antes de ejecución. Tamaños S/M son relativos, no promesas de horas.

| ID | Entregable | Depende de tareas | Gates adicionales | Repo dueño | Tamaño |
|---|---|---|---|---|---|
| WS01 | [Fijar brief y glosario autosuficientes](../../tasks/workspace-documental/task-ws01.md) | — | — | deskops | S |
| WS02 | [Inventariar superficies y operaciones Deskops](../../tasks/workspace-documental/task-ws02.md) | WS01 | — | deskops | M |
| WS03 | [Inventariar persistencia, consultas y notaciones](../../tasks/workspace-documental/task-ws03.md) | WS01 | — | deskops | M |
| WS04 | [Inventariar UI y reconciliar trabajo en curso](../../tasks/workspace-documental/task-ws04.md) | WS01 | — | deskops | M |
| WS05 | [Inventariar identidad y API Scion](../../tasks/workspace-documental/task-ws05.md) | WS01 | — | deskops | M |
| WS06 | [Registrar acuerdos de alcance con repos dueños](../../tasks/workspace-documental/task-ws06.md) | WS02, WS03, WS04 | — | deskops | S |
| WS07 | [Resolver decisiones de producto y escritura](../../tasks/workspace-documental/task-ws07.md) | WS06 | — | deskops | M |
| WS08 | [Precisar user-flows y criterios observables](../../tasks/workspace-documental/task-ws08.md) | WS07 | G_PRODUCT | deskops | M |
| WS09 | [Precisar catálogo de renderizaciones](../../tasks/workspace-documental/task-ws09.md) | WS07 | G_PRODUCT | deskops | M |
| WS10 | [Precisar índice y convención del manual](../../tasks/workspace-documental/task-ws10.md) | WS02, WS07 | G_PRODUCT | deskops | S |
| WS11 | [Cerrar contrato de navegación e identidad](../../tasks/workspace-documental/task-ws11.md) | WS09, WS08 | G_PRODUCT | deskops | M |
| WS12 | [Cerrar contrato de operaciones y escritura](../../tasks/workspace-documental/task-ws12.md) | WS11, WS08 | G_WRITE_POLICY | deskops | M |
| WS13 | [Integrar lector workspace con historia y foco](../../tasks/workspace-documental/task-ws13.md) | WS11 | G_UI_READ | graph_ui | M |
| WS14 | [Integrar búsqueda navegable del workspace](../../tasks/workspace-documental/task-ws14.md) | WS13 | G_UI_READ | graph_ui | M |
| WS15 | [Mostrar errores de lectura y modo degradado](../../tasks/workspace-documental/task-ws15.md) | WS13 | G_UI_READ | graph_ui | S |
| WS16 | [Validar con humano lectura y descubrimiento](../../tasks/workspace-documental/task-ws16.md) | WS14, WS15, WS08, WS40, WS41 | — | graph_ui | M |
| WS17 | [Escribir entradas e índices del desk ejemplo](../../tasks/workspace-documental/task-ws17.md) | WS11, WS40 | — | deskops | S |
| WS18 | [Declarar proyecciones de grafo reutilizables](../../tasks/workspace-documental/task-ws18.md) | WS09, WS11 | G_SPEC_VIEW | spec2viz | S |
| WS19 | [Integrar edición de campos con conflicto](../../tasks/workspace-documental/task-ws19.md) | WS12, WS16 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS20 | [Probar o completar guardado fuente reversible](../../tasks/workspace-documental/task-ws20.md) | WS12 | G_SLDB_WRITE, G_WRITE_CONTRACT | sldb | M |
| WS21 | [Integrar fuente y renderizado editables](../../tasks/workspace-documental/task-ws21.md) | WS19 | G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS22 | [Renderizar Board como trabajo navegable](../../tasks/workspace-documental/task-ws22.md) | WS13, WS09 | G_UI_READ | graph_ui | M |
| WS23 | [Renderizar rituales y pasos como procedimiento](../../tasks/workspace-documental/task-ws23.md) | WS13, WS09 | G_UI_READ | graph_ui | S |
| WS24 | [Integrar conocimiento y grafo local](../../tasks/workspace-documental/task-ws24.md) | WS13, WS18 | G_UI_READ | graph_ui | M |
| WS25 | [Integrar captura y triage en UI](../../tasks/workspace-documental/task-ws25.md) | WS12, WS16 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS26 | [Integrar autoría y contexto de tareas](../../tasks/workspace-documental/task-ws26.md) | WS12, WS22 | G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS27 | [Integrar revisión de cambios y evidencia](../../tasks/workspace-documental/task-ws27.md) | WS13, WS12 | G_UI_READ | graph_ui | M |
| WS28 | [Integrar verificación y handoff de cierre](../../tasks/workspace-documental/task-ws28.md) | WS27, WS12 | G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS29 | [Integrar Changes e impacto comprobable](../../tasks/workspace-documental/task-ws29.md) | WS15, WS24 | G_UI_READ | graph_ui | M |
| WS30 | [Validar autoría y revisión manual completas](../../tasks/workspace-documental/task-ws30.md) | WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42 | — | graph_ui | M |
| WS31 | [Publicar manual documental básico probado](../../tasks/workspace-documental/task-ws31.md) | WS30, WS10, WS43 | G_HUMAN_MANUAL | deskops | M |
| WS32 | [Unificar identidad de intento y cierre Scion](../../tasks/workspace-documental/task-ws32.md) | WS05, WS12 | G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS33 | [Vincular mensajes, resultados y decisiones](../../tasks/workspace-documental/task-ws33.md) | WS32, WS11 | G_SCION | deskops | M |
| WS34 | [Exponer despacho y respuesta Scion autorizados](../../tasks/workspace-documental/task-ws34.md) | WS33, WS12 | G_EXEC, G_SCION, G_WRITE_CONTRACT | deskops | M |
| WS35 | [Mostrar ejecución y trazabilidad en workspace](../../tasks/workspace-documental/task-ws35.md) | WS33, WS27 | G_SCION, G_UI_READ | graph_ui | M |
| WS36 | [Integrar delegación e intervención humanas](../../tasks/workspace-documental/task-ws36.md) | WS34, WS35 | G_EXEC, G_SCION, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS37 | [Validar delegación con agente real](../../tasks/workspace-documental/task-ws37.md) | WS36, WS30 | G_EXEC, G_SCION | graph_ui | M |
| WS38 | [Publicar capítulos verificados de delegación](../../tasks/workspace-documental/task-ws38.md) | WS37, WS31 | G_HUMAN_DELEGATE | deskops | S |
| WS39 | [Integrar inspección y edición de modelos existente](../../tasks/workspace-documental/task-ws39.md) | WS12, WS16 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS40 | [Crear generador reproducible del corpus Taller](../../tasks/workspace-documental/task-ws40.md) | WS11, WS08 | G_UI_READ | graph_ui | M |
| WS41 | [Implementar lectura segura entre desks](../../tasks/workspace-documental/task-ws41.md) | WS13, WS11, WS40 | G_UI_READ | graph_ui | M |
| WS42 | [Integrar operaciones de conocimiento existentes](../../tasks/workspace-documental/task-ws42.md) | WS19, WS24, WS12 | G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT | graph_ui | M |
| WS43 | [Publicar navegación documental del desk real](../../tasks/workspace-documental/task-ws43.md) | WS17, WS30 | G_HUMAN_MANUAL, G_PRODUCT, G_WRITE_CONTRACT | deskops | S |
| WS44 | [Comprobar y revalidar acceso público a Scion](../../tasks/workspace-documental/task-ws44.md) | WS05, WS07 | G_PRODUCT | deskops | S |

## Gates externos y humanos

| Gate | Estado observado | Significado | Resolver |
|---|---|---|---|
| G_PRODUCT | pending | Decisiones de producto registradas por humano | WS07 |
| G_CLOSEOUT | blocked | Contrato de evidencia de closeout estabilizado | external |
| G_SOURCE | pending | Fuente reversible y guardas de campos probadas | WS20 |
| G_SCION | unverified | Scion accesible y contrato público comprobado | WS44 por operador Scion designado en WS07 |
| G_EXEC | pending | Humano autoriza ejecución y comunicaciones del escenario | external |
| G_HUMAN_READ | pending | Persona aprueba recorrido de lectura | WS16 |
| G_HUMAN_MANUAL | pending | Persona aprueba autoría/revisión | WS30 |
| G_HUMAN_DELEGATE | pending | Persona aprueba delegación | WS37 |
| G_WRITE_POLICY | pending | Política de escritura aprobada por humano | WS07 |
| G_WRITE_CONTRACT | pending | Contrato técnico de operaciones verificado | WS12 |
| G_UI_READ | pending | Deltas de lectura aceptados en graph_ui | WS11 |
| G_UI_WRITE | pending | Deltas de mutación aceptados en graph_ui | WS12 |
| G_SLDB_WRITE | pending | Alcance fuente aceptado en sldb | WS12 |
| G_SPEC_VIEW | pending | Alcance de proyecciones aceptado en spec2viz | WS11 |
| G_HUMAN_MODEL | pending | Persona valida inspección/edición de modelos | WS39 |

Cada output_scope se resuelve respecto de su output_base explícito; las actas de uso viven en repo dueño. Los productores de gates también se declaran en dag.yaml, sin aristas ocultas en generador. source_mode determina la variante WS21 y si WS20 pertenece a la entrega; pending bloquea ambos. Los gates se satisfacen con el tipo de evidencia declarado, nunca por existencia del archivo. El validador comprueba referencias, ausencia de ciclos y coherencia de proyecciones; muestra por separado candidatas de preparación, bloqueos y autorización. Cero nodos tienen ejecución de producto autorizada. Las capas topológicas no son fases operativas: falta aprobar gates, no solapamiento, TaskDoc y cierre de cada fase. Las observaciones de referencias tienen hash para detectar movimiento, no para aprobar trabajo.

## Entregas y gates de uso

WS13–16 y WS40/41 dan lector con búsqueda y errores antes de edición o índices nuevos. WS40 produce corpus temporal y WS17 aporta solo plantillas de entradas authored. WS19–28, WS42 y WS30 dan autoría/revisión manual; WS31 publica su manual. WS29 (Changes) y WS39 (Schema) son extensiones con aceptación propia, no prerrequisitos del lector o manual básico. WS32–38 son el ramal de Scion con permisos de ejecución explícitos. El cierre baseline usa handoff verificado al CLI/coordinador, no commit desde HTTP.

## Reproducción y revisión

`python desk/drawer/plans/workspace-documental/build_plan.py` genera tabla/fichas/spec del diagrama. `python desk/drawer/plans/workspace-documental/validate_plan.py` verifica coherencia. `python desk/drawer/plans/workspace-documental/render_diagram.py` genera Mermaid y HTML mediante spec2viz. El modo `build_plan.py --check` no escribe y detecta proyecciones obsoletas.

[Diagrama interactivo](dag.diagram.graph.html) · [Mermaid](dag.diagram.mmd) · [Validación](validation.txt). El diagrama incluye gates como nodos; leer flechas de prerequisito a dependiente, sin confundir estado pendiente con implementación.

Revisiones independientes y resolución de hallazgos en [reviews](reviews/README.md). Los IDs antiguos A1–H2 se conservan en legacy_mapping de dag.yaml para trazabilidad, no como otro DAG activo. No se modificaron tareas ajenas ni el Board de graph_ui.
