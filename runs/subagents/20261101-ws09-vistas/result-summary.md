# Resultado del Executor de WS09 — fichas por fila de vistas.md

Fecha: 2026-11-01. Escribí solo `desk/drawer/plans/workspace-documental/borradores/vistas.md` y este archivo.

## Fichas escritas

23 encabezados `### F..` para las 20 filas (12 + 8), en el orden de las tablas. Sufijos a/b solo donde hay evidencia o estado distinto:

- F01-F10, F12-F17, F20: una ficha cada una.
- F11a (roles y runtime profiles) y F11b (RunDoc y conversación vinculada).
- F18a (SpecDoc y NotationDoc) y F18b (ViewDoc).
- F19a (Schema y edición de clase existentes) y F19b (acceso desde el documento y promoción con autoridad).

Cada ficha lleva los 14 campos de la TaskDoc. Ninguna omitida. `grep -c "^### F"` da 23, no 20, por los sufijos que permite la disposición.

## Conteo por estado

- disponible: 0 (no hay actas, `manual.md:45`).
- bloqueado: 19 (F01-F10, F11b, F12-F17, F18b, F19b, F20).
- propuesto: 4 (F11a, F15, F18a, F19a). Motivo en cada ficha: ningún nodo del DAG ni contrato WS11/WS12 identificado necesita la fila tal como está, y la evidencia no es completa.

## Conteo por clase (fichas que contienen cada clase; las filas compuestas llevan varias)

- authored: 20 (todas salvo F12, F17, F20).
- derivado: 21 (todas salvo F11a, F11b).
- preferencia local: 15 (F01-F10, F11b, F12, F17, F18b, F19b).

## Huecos con productor

- Contrato de identidad, origen, foco, enlaces y errores de lectura: WS11 (`dag.yaml:681-711`). Casi todas las fichas.
- Contrato de escritura, whitelist, conflicto y fallos parciales: WS12 (`dag.yaml:723-783`).
- Implementación: WS13.1 (Markdown sin modelo, fuente, foco), WS13.2, WS13.3, WS14, WS15.1, WS15.2, WS17, WS18, WS19, WS20, WS21, WS22, WS23, WS24, WS25.1, WS25.2, WS26.2, WS27.1, WS27.2, WS28, WS29, WS32, WS33, WS34, WS35, WS36, WS39, WS41, WS42, WS43, WS44, WS45. IDs verificados contra `dag.yaml`.
- Sin productor en el DAG: consulta guardada y búsqueda por significado sin CLI (F12, repo sldb, `infraestructura.md:115,121`); edición de RoleDoc y RuntimeProfileDoc (F11a, repo deskops, `deskops.md:197,199`); navegación de preguntas de DeskFAQDoc (F15, repo graph_ui, `dag.yaml` solo nombra FAQ en las líneas 356 y 619).

## Lo que WS11 deberá precisar

- Identidad, ruta y modelo opcional de Markdown no modelado (entradas, drawer, issues, FAQ).
- Correspondencia real de origen entre texto, graph y code, y el foco compartido; rango dentro de un archivo (F17). No inventé mapeo.
- Selección mínima de ViewDoc y notación requerida (F18b); sin ella WS18 se detiene (`dag.yaml:1232-1235`).
- Vista Specs de Mindmap: no tiene fila en `ui.md`.
- Campos de RepositoryDoc, InboxNoteDoc, MaterializationContractDoc, PillDoc, StepDoc, DeskFAQDoc: no aparecen enumerados en las auditorías.
- Progreso de paso en un procedimiento: ningún campo o API identificado.
- Aliases y roots autorizados, y forma de los errores de lectura multidesk.
- Criterio visible que separe error, conflicto, cambio y pérdida de soporte (`user-flows.md:177`).
- Forma de los errores de API y red (backend ausente, CDN).

## Qué leí y qué no

Leí completos con Read: `vistas.md`, `user-flows.md`, `manual.md`, `decisiones.md`, `reconciliacion.md`, `auditoria/ui.md`, `auditoria/infraestructura.md`, `auditoria/deskops.md` (líneas 1-126 y 127-267, sin cortar celdas), la TaskDoc `desk/tasks/task-ws09-precisar-catálogo-de-renderizaciones.md` y `preflight-disposition.md`.

De `dag.yaml` (3330 líneas) leí por tramos: WS11 y WS12 (681-796), WS13.1 (841-891), WS17 y WS18 (1170-1257), WS22 (1488-1500), WS23 (1526-1565), WS24 (1565-1600), WS39 (2630-2660), WS41 (2722-2735) y WS42 (2745-2770). Los demás IDs y su `owner_repo` los verifiqué con `grep` de `id:` y `owner_repo:`, sin leer sus cuerpos. Hice dos `grep` adicionales sobre `dag.yaml` (FAQ/issue/pill y consulta guardada/similitud).

No leí `brief.md`, `alcance.md`, `cobertura.md`, `validacion-humana.md` ni `vision.md` completos. De `vision.md` solo vi la línea 36, por `grep`, y la cito así. Tampoco abrí código, repos hermanos ni tests: todo dato de capacidad viene de las auditorías. Las líneas de `AGENTS.md` que llegaron en el contexto no se usaron como evidencia.

## Verificación y límites

- `git show HEAD:<ruta>` contra el archivo actual con `diff`: 0 líneas borradas o cambiadas del texto original; las dos tablas y las secciones previas están intactas, y solo se añadió la sección «Fichas por fila» al final.
- No hice commits, closeout, revisiones, build, validate ni suite. No toqué `dag.yaml` ni otras fuentes. `git status` muestra `vistas.md` modificado además de cambios ajenos de otras sesiones en `desk/inbox` y `desk/drawer/tasks`.
- Una ficha no equivale a aceptación: el estado «propuesto» de F11a, F15, F18a y F19a es una lectura mía de la regla de la disposición y queda para la revisión del Supervisor.

## Ajuste del Supervisor antes de congelar

Claude Opus 5.5, pane `w3Y:p1`, sin Executor. Donde difiera de lo anterior, vale esto:

- F15: decía que ningún nodo la necesita y que `dag.yaml` solo nombra FAQ en WS02 y WS09. Es falso: WS40 crea «su FAQ Markdown» (`dag.yaml:2690`) y la línea de WS09 es 620. F15 pasa a `bloqueado`, por WS40, WS13.1 y WS11. La navegación de preguntas sigue sin productor en el DAG.
- F11b: clasificaba el estado del runtime como preferencia local; por la definición es `derivado`.

Conteo vigente: bloqueado 20, propuesto 3 (F11a, F18a, F19a), disponible 0. Clases por fichas: derivado 22, preferencia local 14, authored 20.

## Ajuste del Supervisor tras Tester v1 FAIL

Claude Opus 5.5, pane `w3Y:p1`, sin Executor. Donde difiera de lo anterior, vale esto:

- F11a, F18a y F19a pasan a `bloqueado`: sus campos nombran contratos WS11 o WS12 pendientes, y la disposición dice que eso es bloqueado. Mi conteo anterior de 3 propuesto era incorrecto.
- F18a: se quita la contradicción sobre contrato; tiene contrato de modelo, no de UI.
- F11b: la conversación no se atribuye a WS44, que es el probe de acceso; el vínculo es WS33.
- F01, F11a, F14 y F18a: WS11 no produce implementación. Renderer sin nodo pasa a «sin productor en el DAG», repo dueño graph_ui.

Conteo vigente: bloqueado 23, propuesto 0, disponible 0. Sin productor en el DAG se suman: lista de issues y renderer de roles en la UI, y vista Specs en el lector.
