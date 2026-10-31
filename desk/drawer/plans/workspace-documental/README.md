# Plan: workspace documental de Deskops

Propuesta del 2026-10-31. Este paquete registra el DAG y borradores; no activa tareas ni autoriza implementaciones en repos hermanos. La UI anterior es un experimento técnico, no contrato de producto. No modifica la tarea activa de closeout ni trabajo ajeno.

## Fuentes y frontera

Esta conversación; README.md, docs/atoms.md, docs/operator-manual.md, modelos de deskops; ViewDoc/NotationDoc de spec2viz; superficie sldb y UI activa Mindmap. También se consultó /home/jp/proyectos/softfactory_spec/SPEC.md: existen candidatos de workspace, Changes, edición Kimun y correlación Scion. Los integramos como trabajo existente a precisar, no como evidencia de que ya funcionen. Kimun es una ruta de migración con dependencias externas, no un requisito para redactar o navegar Markdown hoy.

## Documentos que ya podemos escribir

| Borrador incluido | Qué fija ahora | Qué no da por resuelto |
|---|---|---|
| [Visión](borradores/vision.md) | Workspace documental, superficies y límites | Backend y contratos faltantes |
| [User-flows](borradores/user-flows.md) | Ocho recorridos humanos con aceptación | Controles y capacidades aún no implementados |
| [Vistas](borradores/vistas.md) | Fuentes, representaciones, operaciones y ficha de vista | Un renderer propio para cada tipo o nuevos modelos obligatorios |
| [Manual](borradores/manual.md) | Índice, ejemplo compartido y convención de disponibilidad | Instrucciones/capturas de una UI futura |

Los cuatro están redactados como borradores, no tareas cerradas ni docs de producto aprobados. La auditoría A1 y la reconciliación B1 establecen hechos y acuerdos; los durables pasan a átomos antes de docs. El manual CLI existente se reutiliza sin reemplazarlo por instrucciones hipotéticas.

## DAG de entregables

Fuente editable: [dag.yaml](dag.yaml). Flecha significa prerrequisito -> dependiente. Cada nodo tiene una candidata en drawer con alcance y aceptación; antes de promoción debe precisarse la lista de archivos/operaciones, pills/átomos y validación. Los IDs de este plan no son todavía IDs de tareas activas. Dependencias externas y condicionales están declaradas en YAML y candidatas; no se consideran satisfechas por existir un archivo.

| ID | Entregable | Depende de | Dueño previsto |
|---|---|---|---|
| A1 | [Auditar documentos, relaciones y capacidades existentes](../../tasks/workspace-documental/task-a1.md) | — | deskops + repos dueños |
| A2 | [Escribir visión y modelo de interacción del workspace](../../tasks/workspace-documental/task-a2.md) | — | deskops |
| A3 | [Escribir user-flows y escenarios de aceptación](../../tasks/workspace-documental/task-a3.md) | — | deskops |
| A4 | [Escribir catálogo de vistas y renderizaciones](../../tasks/workspace-documental/task-a4.md) | — | deskops + graph_ui |
| A5 | [Escribir índice y convención del manual de usuario](../../tasks/workspace-documental/task-a5.md) | — | deskops |
| B1 | [Reconciliar visión, recorridos y código](../../tasks/workspace-documental/task-b1.md) | A1, A2, A3, A4, A5 | deskops |
| B2 | [Definir contratos de navegación y autoría](../../tasks/workspace-documental/task-b2.md) | B1 | deskops + infraestructura |
| B3 | [Definir contrato de interacción y operaciones](../../tasks/workspace-documental/task-b3.md) | B1 | deskops + graph_ui |
| C1 | [Resolver contrato y clasificación de huecos documentales](../../tasks/workspace-documental/task-c1.md) | B2 | repos dueños |
| C2 | [Escribir entradas e índices navegables del ecosistema](../../tasks/workspace-documental/task-c2.md) | C1 | deskops + proyectos |
| C3 | [Escribir definiciones de vistas reutilizables](../../tasks/workspace-documental/task-c3.md) | C1, A4 | spec2viz + graph_ui |
| D1 | [Implementar workspace y navegación documental](../../tasks/workspace-documental/task-d1.md) | C2, B3 | graph_ui |
| D2 | [Integrar fuente Markdown y edición estructurada](../../tasks/workspace-documental/task-d2.md) | D1 | graph_ui + infraestructura |
| D3 | [Implementar renderizaciones sobre documentos](../../tasks/workspace-documental/task-d3.md) | D1, C3 | graph_ui |
| D4 | [Habilitar operaciones del desk desde el contexto](../../tasks/workspace-documental/task-d4.md) | D2, D3 | deskops + graph_ui |
| E1 | [Unificar identidad y registro por intento Scion](../../tasks/workspace-documental/task-e1.md) | B3 | deskops + Scion |
| E2 | [Vincular conversaciones, resultados y decisiones](../../tasks/workspace-documental/task-e2.md) | E1, D2 | Scion + deskops |
| E3 | [Proyectar ejecución y revisión en el workspace](../../tasks/workspace-documental/task-e3.md) | E2, D4 | graph_ui |
| F1 | [Integrar salud, cambios e impacto](../../tasks/workspace-documental/task-f1.md) | D2, D3 | graph_ui + infraestructura |
| G1 | [Validar recorridos humanos básicos](../../tasks/workspace-documental/task-g1.md) | D4, F1 | deskops + graph_ui |
| G2 | [Validar delegación y revisión trazable](../../tasks/workspace-documental/task-g2.md) | G1, E3 | deskops + graph_ui + Scion |
| H1 | [Publicar manual del workspace documental](../../tasks/workspace-documental/task-h1.md) | G1, A5 | deskops |
| H2 | [Completar manual de ejecución y revisión](../../tasks/workspace-documental/task-h2.md) | H1, G2 | deskops |

## Orden de trabajo y gates

Primera capa candidata: A1–A5 (archivos separados y sin dependencias internas). A2–A5 tienen semilla escrita; requieren revisión. Luego B1; luego B2 y B3 en paralelo. El resto se selecciona por dependencias satisfechas y archivos sin solapamiento, no por letra o tema. Por ejemplo E1 se puede preparar tras B3 pero no ejecutar sobre cierre hasta que cierre la tarea activa que toca ese servicio. Una capa lista no equivale automáticamente a fase activa: ejecutar ritual de fase y comprobar no solapamiento en cada repo.

Entrega documental/manual básica: C2 + D1–D4 + F1 -> G1 -> H1. Ramal opcional de delegación: E1–E3 -> G2 -> H2. G1 no depende de Scion; H1 puede publicarse antes de G2. Lectura/navegación inicial D1 tampoco espera edición distribuida.

Cada tarea activa debe pasar preflight, ejecución, testing y cierre atómico. Cada fase cierra con integración y reconciliación de pills. Tests técnicos no sustituyen la comprobación del recorrido humano. No se amplía automáticamente a base de datos compartida, transporte nuevo ni despliegue distribuido.

## Reutilización y preguntas abiertas

D1 refina workspace multiproyección ya capturado; D2 refina adaptador/edición; F1 refina Changes; E1/E2 descomponen correlación Scion. Antes de promover hay que reconciliar y atomizar las candidatas originales, no ejecutar ambos tickets. El contrato Opsys–Kimun es dependencia condicional de sus adaptadores, con M1/M2/C2 comprobados en el repo dueño. No crear sustitutos en deskops para huecos de infraestructura.

B2 debe resolver dónde viven entradas e índices y si bastan contratos existentes. B3 debe resolver navegación/edición y autoridad de acciones. Las decisiones que requieren dueño se presentan como decisiones, sin usar su ausencia como permiso para inventar arquitectura.

## Diagrama y validación

- [Diagrama interactivo generado](dag.diagram.graph.html)
- [Mermaid generado](dag.diagram.mmd)
- [Spec de diagrama derivado](dag.diagram.yaml)

Regenerar: `python desk/drawer/plans/workspace-documental/render_diagram.py`, después `spec2viz diagram render desk/drawer/plans/workspace-documental/dag.diagram.yaml --renderer mermaid --out desk/drawer/plans/workspace-documental` (o `--renderer graph`). No editar las proyecciones para cambiar dependencias: editar dag.yaml y las candidatas correspondientes.

Revisión: E2 depende de E1 y del contrato B3, no de edición UI. C1 cierra clasificación y contratos, no exige modelos nuevos. D1/D4 requieren atomización antes de ejecución; los demás también deben verificarse por coherencia del entregable al promover. La captura del plan no ejecuta estos nodos ni cierra tareas del producto.

## Estado de referencias externas al validar

La especificación externa cita tickets de workspace, edición, Changes e integración Kimun que se pudieron leer al iniciar la revisión, pero sus archivos ya no estaban disponibles al validar este paquete. Se conservan sus rutas como procedencia pendiente, no como dependencias satisfechas ni tareas existentes ejecutables. A1 debe reconciliar su ubicación/estado antes de promover o duplicar trabajo. Los archivos de correlación Scion y de la tarea activa de closeout sí existen. Ver reference_status en dag.yaml. Este plan no restaura ni modifica trabajo ajeno.
