FILE:desk/tasks/task-ws11-cerrar-contrato-de-navegación-e-identidad.md
---
id: task-ws11-cerrar-contrato-de-navegación-e-identidad
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/borradores/vistas.md
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/reconciliacion.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- runs/subagents/20261101-ws09-vistas/result-summary.md
- runs/subagents/20261101-ws09-correccion/root-approval.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws11.md
closeout_evidence:
- commit
- document
---

# WS11: Cerrar contrato de navegación e identidad

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó WS09 y autorizó solo WS11. Trece nodos dependen de un contrato que no existe.

## Goal

_Describe the concrete result this task must produce._

Crear desk/drawer/plans/workspace-documental/contratos/navegacion.md con identidad, origen, resolución repo/store, foco, enlaces, multidesk read-only, huecos clasificados y mapa de deltas, con APIs reales verificadas.

## Scope

_State what is in scope and what is out of scope._

Un documento Markdown mantiene identidad/ruta/modelo opcional; graph/code admiten otros nodos con origen. Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos. Instancia = documento concreto que falta escribir. Vínculo = referencia o enlace que falta entre documentos existentes.

Autoriza: runs/subagents/20261101-ws09-correccion/root-approval.md. Autorización acotada: execution_authorized global sigue false. No existe contrato previo: se crea desk/drawer/plans/workspace-documental/contratos/navegacion.md.

Secciones obligatorias del contrato, en este orden:
1. Alcance y estado: qué fija, qué no, base observada (graph_ui 134a665, sldb 77bd6d00).
2. Identidad y origen: Markdown modelado frente a no modelado; ruta y modelo opcional; nodos graph y code con origen.
3. Resolución de repo y store: explícita por petición; aliases y roots autorizados; rutas seguras; sin cambiar SLDB_STORE global ni aceptar roots arbitrarios.
4. Fuente propia frente a Code referenciado.
5. Navegación, enlaces e historia.
6. Foco y correspondencias: tabla con selección origen, destino, correspondencia real, evidencia, estado. Sin mapeo no hay soporte ni prueba positiva por omisión. Si WS13.1 o el catálogo lo comprometen y falta mapeo, se registra hueco con productor o cambio de alcance explícito; nunca se elimina en silencio.
7. Errores de lectura y estados de red, incluido fallo de carga CDN, para WS15.1.
8. Lectura multidesk read-only, para WS41.
9. ViewDoc: solo grafo. Selección mínima concreta y notación para WS18 declaradas si hay evidencia; si no, declarar que su promoción se detiene.
10. Authored, derivado y preferencia local; runtime volátil no es documento compartido por defecto. Sin modelo nuevo para organizar entradas o listas derivables.
11. Huecos: tabla con hueco, clase, dueño, productor o «sin productor en el DAG». Candidaturas de vistas.md siguen como tales: genérico Markdown o modelado no implica renderer especial de FAQ, issues, roles o Specs.
12. Mapa de deltas graph_ui que requieren recepción: ID, efecto, actor P01, gate, y «sin acta registrada». G_SPEC_VIEW opcional aparte. No inventar actas. El contrato básico no espera Changes, Scion ni ViewDoc opcional.
13. Trazabilidad: cada punto de «Lo que WS11 deberá precisar» en runs/subagents/20261101-ws09-vistas/result-summary.md, resuelto o con hueco.

Clases de hueco: instancia = documento concreto que falta escribir; vínculo = referencia o enlace que falta entre documentos existentes; consulta = selección o lista derivable sin operación pública para obtenerla; API = operación pública ausente en repo dueño; renderer = representación ausente en graph_ui con datos ya disponibles. Si dos aplican, elegir la que falte primero y decirlo.

Evidencia: toda API o implementación se apoya en path:línea o símbolo verificado por lectura real en el commit citado, con el archivo abierto, además de la auditoría. Sin tablas internas, endpoints hipotéticos ni pruebas no ejecutadas. frontends/workspace/ no adoptado no es base. No confundir lo existente con lo aceptado.

Límites: lectura no espera guardado ni WS12 por el estado bloqueado de una ficha compuesta. Todo hueco de escritura se remite a WS12. No actuar en repos hermanos: solo lectura. No llamar Scion vivo ni usar credenciales. «Contrato básico revisado» = Tester independiente PASS y revisión root.

Roles: el Executor escribe solo desk/drawer/plans/workspace-documental/contratos/navegacion.md y runs/subagents/20261101-ws11-navegacion/result-summary.md. Sin commits ni revisiones. Fuera de alcance: WS12, UI, Scion, push, dag.yaml, otras fuentes, helper, validadores, suite general. Sin preguntar al solicitante.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer auditorías, vistas.md, user-flows.md, decisiones.md, reconciliacion.md y los nodos consumidores. 2. Abrir el código real citado en ../UIs/graph_ui y ../sldb. 3. Escribir el contrato. 4. Escribir runs/subagents/20261101-ws11-navegacion/result-summary.md.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/contratos/navegacion.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws11-navegacion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales citadas por auditorías WS02–04 (path/símbolo/commit y evidencia existente); cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño antes de code. Mapear recepción requerida por delta en graph_ui (actor P01, IDs y efectos); enlazar acta externa solo si el receptor ya la registró. El contrato básico puede cerrar sin recepción de Changes, Scion ni ViewDoc opcional; cada delta sigue bloqueado hasta su propio recibo. G_SPEC_VIEW se obtiene separadamente al preparar WS18, sin bloquear navegación base. WS11 cierra con contrato básico revisado, clasificación de huecos y mapa de deltas que requieren recepción; puede cerrar sin acta receptora. Recibos son producidos por solicitante P01/repo receptor al preparar cada delta, no por Executor de WS11 ni por escritura interrepo. Cada delta espera su propio recibo; contrato básico no afirma que ninguno se haya recibido. Revisiones afectadas renovadas si el helper marca alguna, build --check, validate --check y status en verde, y Tester independiente PASS antes del closeout.

FILE:desk/drawer/plans/workspace-documental/decisiones.md
# Decisiones finales de núcleo — 2026-10-31

Responsable de producto y recepción de deltas graph_ui/SLDB/spec2viz: solicitante humano de esta sesión. Fuente verificable: `runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json`, tool call `call_387acc8d34de4f35bc4bafab9263bd58`, ítems 0–2. Acepta decisiones de producto y participa en Taller; no ha aceptado implementación, contratos API ni actas de uso.

## Respuestas humanas literales

Ítem 0. Para la primera entrega, ¿confirmamos extender el Mindmap existente usando SLDB/pron y Deskops, sin migrar a Kimun, con lectura y operación manual primero y Scion como ramal posterior?

> Sí, mantener esa base y Scion después

Ítem 1. ¿Qué alcance de edición dejamos en el plan? En ambos casos: guardar no hace commit; cierre y promoción respetan el workflow Deskops; con otro coordinador escribiendo, la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado.

> Markdown editable tras probar API reversible, conflictos y campos protegidos

Ítem 2. ¿Quedas tú como responsable de producto y aceptación de deltas en graph_ui, SLDB y spec2viz, y como participante de las pruebas de uso sobre el proyecto temporal Taller? Los objetivos iniciales serían abrir/buscar ≤2 s, guardar ≤3 s y arrancar ≤10 s; Scion se designa cuando abordemos ese ramal.

> Sí, yo; acepto Taller y esos objetivos iniciales

## Registro por decisión

Todas las filas están resueltas como base de planificación; las técnicas son revisables por cambio real, sin nueva firma artificial. Fecha común 2026-10-31.

| ID | Resultado concreto | Tipo/actor/fuente | Nodos y gates |
|---|---|---|---|
| P01 | Extender Mindmap; solicitante responsable producto/aceptación de deltas graph_ui/sldb/spec2viz. Scion se designa cuando abordemos ese ramal. | Humana; solicitante; ítems 0 y 2. Precisión «operador» y «recepción técnica pendiente por delta»: Técnica derivada (T-P01) | WS04/06/07/11/12/13; G_PRODUCT; recepción técnica pendiente por delta |
| P02 | SLDB/pron + Deskops; Kimun fuera de esta línea base | Humana; solicitante; ítem 0 | WS03/06/07; G_PRODUCT |
| P03 | Con otro coordinador escribiendo, la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado | Humana; solicitante; pregunta ítem 1. Precisión «canal público, autoridad compartida CLI/agentes/UI, probado; lock solo UI no basta»: Técnica derivada (T-P03) | WS12/19/25/26/28/34/36/42; G_WRITE_POLICY/G_WRITE_CONTRACT |
| P04 | source_mode=editable; Markdown editable tras probar API reversible, conflictos y campos protegidos | Humana; solicitante; respuesta ítem 1. Precisión «con revisión» y «recuperación»: Técnica derivada (T-P04) | WS20/21/30/31; G_PRODUCT/G_SOURCE/G_SLDB_WRITE |
| P05 | Guardar no hace commit; cierre respeta el workflow Deskops | Humana; solicitante; pregunta ítem 1. Precisión «CLI/coordinador» y «refresco que verifica el resultado»: Técnica derivada (T-P05) | WS12/27/28; G_WRITE_POLICY/G_CLOSEOUT |
| P06 | Promoción y cierre respetan workflow Deskops; con otro coordinador escribiendo, la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado | Humana; solicitante; pregunta ítem 1. Precisión «preparar» y «canal completo comprobado»: Técnica derivada (T-P06) | WS12/26/28; G_WRITE_POLICY |
| P07 | Foco/historia/disposición locales; multidesk inicialmente read-only con rutas/aliases explícitos | Técnica conservadora; Executor por encargo TaskDoc v2 (actor técnico registrado); sin firma humana; fuente en T-P07 | WS11/13.3/41; G_PRODUCT |
| P08 | Taller temporal; solicitante participa. Objetivos abrir/buscar ≤2 s, guardar ≤3 s, arranque ≤10 s | Humana; solicitante; ítem 2 | WS08/16/30/40; G_PRODUCT; actas humanas aún pendientes |
| P09 | Entradas reales desk/README.md + mapa authored en deskops reutilizando registry; publicar WS43 tras validación | Técnica conservadora; Executor por encargo TaskDoc v2 (actor técnico registrado); sin firma humana; fuente en T-P09 | WS11/17/43; G_PRODUCT |

G_PRODUCT y G_WRITE_POLICY registran esta base, no funciones disponibles. G_SOURCE es producido por WS20 en sldb: contrato público de guardado raw-source con revisión esperada, extracción/validación/roundtrip, protección de campos y buffer recuperable ante conflicto/fallo. G_WRITE_CONTRACT/recepción se verifican por delta y efecto, sin aceptar modelos, Changes o Scion para habilitar campos/intake. Un recibo técnico nombra actor, IDs/alcance, fecha y commit/blob en repo dueño. Ninguna decisión autoriza dispatch, mensajes o acceso Scion; G_EXEC/G_SCION siguen pendientes. No repetir decisiones ya respondidas al promover WS07: verificar y reutilizar este registro.

## Procedencia técnica

Etiquetas: «Humana» (solo lo que dicen pregunta y respuesta de los ítems 0-2), «Técnica derivada» (precisión de planificación con fuente existente) y «Técnica sin registro histórico localizado». Las precisiones no se retiran: se separan de la afirmación humana. `preflight-input-v2.md` = `runs/subagents/20261031-finalizar-plan-workspace/preflight-input-v2.md` (commit cc8d83da), encargo técnico, no aprobación humana. «Tabla inicial» = `decisiones.md` en 35543965, propuestas con estado PENDING_OWNER y sin autor declarado. En P07/P09, «Executor por encargo TaskDoc v2» es el actor técnico registrado y responsable del default; no prueba quién inventó ni aprobó históricamente la propuesta, cuya autoría inicial sigue sin localizar. Citas a `dag.yaml` (`desk/drawer/plans/workspace-documental/`) prueban la regla vigente, no quién la decidió. Detalle por fragmento: `runs/subagents/20261031-atribucion-decisiones/attribution-map.md`.

| ID | Precisión técnica | Etiqueta | Fuente exacta | Límite |
|---|---|---|---|---|
| T-P01 | Lo que se designa en Scion es el operador; recepción técnica pendiente por delta | Técnica derivada | Operador: tabla inicial línea 7 («operador del ramal Scion»), `preflight-input-v2.md` 36; regla vigente `dag.yaml` 515, 543-544. Recepción: `preflight-input-v2.md` 131-133; regla vigente `dag.yaml` 161-167 (G_UI_READ) y 225-233 (G_SLDB_WRITE) | Sin registro histórico de quién lo decidió; el ítem 2 dice «Scion se designa», sin nombrar operador |
| T-P03 | Canal público con autoridad compartida CLI/agentes/UI, probado; lock solo UI no basta | Técnica derivada | `preflight-input-v2.md` 127-128; antecedente en tabla inicial línea 9 («canal autorizado real. No fingir lock compartido con CLI»); regla vigente `dag.yaml` 763-764 | Antecedente es propuesta sin autor; no consta aceptación humana de la precisión |
| T-P03.1 | «Modo manual exclusivo»: WS12 produce su definición operativa, las formas de comprobarla y la respuesta ante ausencia de evidencia, antes de habilitar a sus consumidores. Hoy no se fija mecanismo de lock ni de detección, y la ausencia de señal no declara exclusividad | Técnica derivada | Revisión root 2026-11-01: `runs/subagents/20261031-atribucion-decisiones/root-decision-20261101.md`, punto 3. Término en tabla inicial línea 9 («modo manual exclusivo»); regla vigente `dag.yaml` 735 (WS12, «policy coordinador») y 1327 (WS19.1) | Origen: esta revisión root, no el ítem 1. No es aprobación humana, ni API ni gate nuevos, ni cambia P03 |
| T-P04 | Guardado con revisión esperada y recuperación ante fallo/conflicto | Técnica derivada | `preflight-input-v2.md` 124-126; regla vigente `dag.yaml` 44-49 (G_SOURCE) y 1406-1408 (WS20) | «Revisión» y «recuperación» no están en la tabla inicial (línea 10) ni en el ítem 1 |
| T-P05 | Cierre por CLI/coordinador; refresco que verifica el resultado | Técnica derivada | Tabla inicial línea 11 («closeout commit fuera de HTTP, con handoff visible y refresco que verifica resultado»); regla vigente `dag.yaml` 1984-1987 y 1991-1994 (WS28: «se refresca el estado desde deskops») | Sin registro posterior que lo atribuya a una persona; el dag no dice «refresco verificable», sino que `deskops show task` y el commit de closeout confirman el cierre |
| T-P06 | Preparar/handoff manual hasta canal completo y efectos comprobados | Técnica derivada | Tabla inicial línea 12 («cuando WS12 documente canal completo y efectos; de otro modo preparar/handoff manual»); gate vigente `dag.yaml` 122-131 (G_WRITE_CONTRACT) | No se localizó en `dag.yaml` la frase «canal completo»; el gate es respaldo derivado |
| T-P07 | Foco/historia/disposición locales; multidesk inicialmente read-only con rutas/aliases explícitos | Técnica conservadora | Registro histórico: tabla inicial línea 13 («Foco e historial por workspace local ... Multidesk inicialmente lectura y rutas/aliases explícitos»); encargo: `taskdoc-frozen.md` 59 y `preflight-input.md` 32-33 («P07 local/read-only multidesk ... decisiones técnicas conservadoras ... delegadas por el encargo»), `preflight-input-v2.md` 107-110; regla vigente `dag.yaml` 541-542 (WS07), 693-695 (WS11), 945-946 (WS13.3), 1188-1196 (WS17) | Autor de la propuesta inicial no declarado; el encargo delega el default, no lo firma ningún humano |
| T-P09 | Entradas reales en desk/README.md + mapa authored en deskops, reutilizando registry; publicar WS43 tras validación | Técnica conservadora | Registro histórico: tabla inicial línea 14 («Extender desk/README.md y un mapa authored ... reutilizando registry; publicar en deskops por WS43 después del ejemplo»); encargo: `taskdoc-frozen.md` 59, `preflight-input-v2.md` 107-110; regla vigente `dag.yaml` 2804-2830 (WS43), 1185-1196 (WS17) | Autor de la propuesta inicial no declarado; «tras validación» y «entradas reales» solo con respaldo vigente en WS43 |

FILE:runs/subagents/20261101-ws09-vistas/result-summary.md
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

## Ajuste del Supervisor tras Tester v2 FAIL

F07 y F15 aún usaban WS11 como productor de implementación. Corregido: contrato WS11, implementación WS25.1 y WS13.1. El estado de ambas sigue en `bloqueado`. La premisa de mi brief de que F01 no tenía productor era incorrecta: F01 sí los tiene.

FILE:runs/subagents/20261101-ws09-correccion/root-approval.md
# Aprobación root del catálogo corregido y de WS09

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-11-01, revisión de HEAD `f3ef4cec`. Texto recibido. No es aprobación humana, ni de producto ni de suite general.

Revisión root del correctivo WS09, HEAD f3ef4cec: APROBADO EL CATÁLOGO CORREGIDO y WS09. No solicito otra corrección ni otra tanda. Puedes cerrar la fase documental correspondiente antes de continuar.

Leí diff completo frente e4b2825c, handoff, ledger, output/disposición vigente y Tester final. Las cuatro correcciones resueltas: RitualDoc.steps inline no depende de instancias StepDoc; SpecDoc/SpecNodeDoc son derivados del YAML; destino WS18 previsto pendiente de confirmar al promover; diagnósticos conservan efectos conocidos de atoms validate. Precisiones F03/F12 acotadas a evidencia. F18a Origen soporta la clase y NotationDoc en store queda honestamente no comprobado.

Ítem11/F15: acepto el ajuste adicional como corrección de la misma clase de negación por conteo dentro del catálogo. 0 DeskFAQDoc no niega docs/faq.md ni FAQ de Taller. Está declarado, con congelación, revisión renovada y Tester de bytes finales. No añade una feature ni decisión de producto; no requería permiso humano nuevo. No dejarlo como trabajo supuestamente no autorizado ni ocultarlo.

Verificación independiente root: SHA vistas.md exacto 411b5bc7160ed635b1d2a275dd3ca9ba3c4e9585fb331ad5fee8624f9c2f4dfd; build --check0, validate --check0, status all current; helper13passed/1.39s. Recalculé73 bundles, contratos/hash/ordered_sources/outputsha/argv/recibos completos:0 discrepancias,73PID únicos. SoloWS09 cambió frente e4b2825c; DAG completo idéntico quitando evidence/input_sha256. Verificado commitcd041ea3 conTester final como ancestro de370c0f61. No atribuir al Tester verificación de365citas ni comandos/hashes globales que corrió root. No prueba de producto ni suite general verde.

Guardar esta decisión y ejecutar ritual/commit de fase: validación común, reconciliación de pills y captura de huecos que correspondan, sin convertir candidaturas del catálogo en compromisos nuevos. Mantener fuentes y contratos/gates sin reescrituras cosméticas.

Tras cierre de fase queda autorizada SOLO WS11: cerrar contrato de navegación e identidad, según su aceptación vigente, en contratos/navegacion.md y enlaces previstos. WS12 y códigoUI siguen fuera de esta autorización. Primero verificar reuso; TaskDoc precisa y commits drawer/promoción, preflight TaskDoc-only y cold-bundle baratos frescos, Executor propio y Tester independiente antes de closeout. Leer filas pertinentes de auditorías completas y verificar path/símbolo/commit real de las APIs/implementaciones existentes donde el contrato se apoye; sin tablas internas, endpoint hipotético ni afirmar pruebas no ejecutadas.

El contrato debe distinguir Markdown modelado/no modelado, identidad/origen/modelo opcional, repo/store explícitos, fuente propia vs Code referenciado, navegación/enlaces/historia y foco. Para texto/graph/Code: identificar el dominio de selecciones/correspondencias soportadas de verdad; sin mapeo, no hay soporte ni prueba positiva por omisión. Un comportamiento ya comprometido no se elimina silenciosamente: hueco y productor o cambio de alcance explícito. Conservar API real y resolver rutas seguras; no cambiar SLDB_STORE global ni aceptar roots arbitrarios.

Clasificar huecos instancia/vínculo/consulta/API/renderer con dueño y productor cuando exista, antes de código. Candidaturas sin productor siguen como tales: genérico Markdown/modelado no implica renderer especial FAQ/issues/roles/Specs implementado. ViewDoc sigue solo grafo; selección mínima concreta/notación para WS18 debe quedar declarada o su promoción se detiene. No crear modelo nuevo por reflejo para organizar entrada/lista derivable; separar authored/derivado/preferencia local. No convertir runtime volátil en documento compartido por defecto.

Mapear deltas/recepción per_delta graph_ui según contrato, sin inventar actas ni hacer que contrato básico espere Changes, Scion o ViewDoc opcional. WS11 puede cerrar sin recepción externa, pero no declara recibida ninguna; la prepara el receptor real al abordar cada delta. Lectura no debe quedar esperando guardado/WS12 por el estado bloqueado de una ficha compuesta. Todo hueco de escritura se remite a WS12, no se implementa aquí. No actuar en hermanos ni llamar Scion vivo ni usar credenciales.

Congelar contrato/enlaces antes de renovar los inputs realmente afectados; helper mide. Revisiones con comparación de contrato completo/reformulación/dry-run, Tester final y checks; checkpoint root antes de WS12/UI. No modificar helper/validadores para acomodar contratos; no suite general ni arreglos ajenos. Mantener execution_authorized global=false como planificación histórica y registrar autorización acotada. Preservar cuatro dirty ajenos, sin push. Continuar sin volver a preguntar decisiones resueltas.

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
