FILE:desk/tasks/task-ws08-precisar-user-flows-y-criterios-observables.md
---
id: task-ws08-precisar-user-flows-y-criterios-observables
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
- desk/drawer/plans/workspace-documental/validacion-humana.md
- desk/drawer/plans/workspace-documental/cobertura.md
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- runs/subagents/20261031-atribucion-decisiones/phase-closeout.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/borradores/user-flows.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws08.md
closeout_evidence:
- commit
- document
---

# WS08: Precisar user-flows y criterios observables

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó WS07 y autorizó la capa WS08/WS10. user-flows.md es un borrador de intención sin mapa a operaciones, errores, nodos ni gates.

## Goal

_Describe the concrete result this task must produce._

Completar desk/drawer/plans/workspace-documental/borradores/user-flows.md para que UF01-UF10 tengan entrada, salida, operación, error, nodo y gate humano, con operaciones citadas de las auditorías WS02-WS04 y huecos marcados.

## Scope

_State what is in scope and what is out of scope._

Mapear UF a operaciones de WS02/03/04; cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado (UF07, fallo de backend/dependencia). UF02 responder significa dentro del desk/contexto autorizado local; ack local: operación pendiente de confirmar en el contrato WS12; no se da por disponible. UF08 es lectura; envío interdesk fuera de baseline, sin excepción implícita a P07. Las operaciones vienen de auditoria/{deskops,infraestructura,ui}.md, disponibles por dependencia transitiva vía WS06/WS07.

Fijado para esta tarea: conservar los textos UF01-UF10 y las precisiones; añadir bajo cada UF una tabla o lista con entrada, salida, operación, error, nodo y gate humano. Operación = lista completa con cita a auditoria/*.md. «Manual» en el alcance es la operación manual cubierta por las UF, no un entregable de manual. Si falta una operación: escribir «hueco» con repo dueño y productor, y en error «no definido» con productor, sin inventar. Gate humano = WS16, WS30, WS37 o WS39, o «ninguno adicional»; WS29 se anota como prueba técnica propia.

Autorización acotada: revisión root 2026-11-01, runs/subagents/20261031-atribucion-decisiones/root-approval-20261101.md. execution_authorized global sigue false. Reutilizar antes de editar: el texto existente no se borra ni se reescribe por estilo.

Independencia: este nodo no tiene arista con WS10 y no lee ni cita su entregable. WS07 está efectiva (runs/subagents/20261031-atribucion-decisiones/ws07-cobertura-efectiva.md). G_PRODUCT satisfecho es base de plan, no aceptación de producto, API ni UI. No reabrir decisiones P01-P09 ni preguntar al solicitante. Una capacidad se afirma solo con cita a auditoría; lo no auditado queda como hueco con dueño. Taller es corpus futuro de WS40, no producto operativo.

Roles: el Executor escribe solo desk/drawer/plans/workspace-documental/borradores/user-flows.md y runs/subagents/20261101-ws08-user-flows/result-summary.md. El Supervisor corre validaciones, commits, revisiones y closeout. Tester independiente de solo lectura. Fuera de alcance: WS09, WS11, WS12, código UI, Scion, push, dag.yaml, validadores, helper y la suite general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer desk/drawer/plans/workspace-documental/borradores/user-flows.md, validacion-humana.md, cobertura.md, decisiones.md y las auditorías. 2. Por cada UF, verificar qué ya está y añadir lo que falte. 3. Marcar huecos con dueño. 4. Escribir runs/subagents/20261101-ws08-user-flows/result-summary.md con las citas y el estado de reuso.

## Validation

_List the checks required before this task can close._

- grep -c "^## UF" desk/drawer/plans/workspace-documental/borradores/user-flows.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws08-user-flows/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Cada UF tiene entrada/salida, operación, error, nodo y gate humano; no prometer función fuera de alcance. Nodo = ID del DAG. Una operación ausente se marca hueco, sin inventarla. Cubrir todas UF01–UF10; operación/nodo/gate admiten listas completas, no elegir nodo principal. Distinguir gate humano WS16/30/37/39 de prueba técnica propia WS29; si no hay gate humano adicional escribir ninguno adicional. Delegación se documenta condicionada a G_SCION/G_EXEC, sin habilitarla. Revisiones afectadas renovadas, build --check, validate --check y status en verde, y Tester independiente PASS antes del closeout.

FILE:desk/drawer/plans/workspace-documental/borradores/user-flows.md
# User-flows del workspace

Estado: borrador de intención. Los pasos son objetivos de UX, no afirmaciones de implementación. Cada flujo requiere mapa a operaciones reales y contrato de errores en WS08/WS07.

## UF01 — Entrar a un proyecto desconocido

Abrir entrada del ecosistema -> elegir proyecto -> leer entrada del desk -> seguir enlaces a conocimiento, trabajo y procedimientos -> abrir documentos al lado -> volver sin perder selección.

Aceptación: explicar propósito, superficies y trabajo actual sin rutas memorizadas. Ante proyecto no accesible o referencia rota, mostrar origen y conservar navegación.

## UF02 — Capturar y aclarar una intención

Capturar idea interna en drawer o protoátomo según naturaleza; entrada externa en inbox -> consultar contexto -> ack local o respuesta dentro del mismo desk autorizado (sin envío interdesk) -> dar forma al material -> conservar como conocimiento o autorizar una tarea completa desde el drawer.

Aceptación: no exigir tarea ni ejecución para conservar una idea. El paso a tarea conserva procedencia; no inventa campos para suplir falta de claridad. No confundir ack con aceptación del trabajo.

## UF03 — Trabajar conocimiento

Buscar por texto/campos/significado -> abrir átomo y fuentes -> comparar con relacionados -> editar, vincular, dividir o reunir mediante operaciones públicas -> consultar materializaciones, validar contratos soportados y leer impacto.

Aceptación: fuente y representación apuntan al mismo documento; las composiciones escriben al origen correcto. El conflicto conserva la edición del usuario y permite revisar; el conocimiento no exige lanzar agentes.

## UF04 — Preparar trabajo activo

Recuperar candidato -> definir objetivo, alcance, dependencias, validación y evidencia -> localizar contexto reusable -> vincular pills/átomos y rituales -> autorizar task -> enrutamiento en Board -> identificar capa lista sin solapamiento.

Aceptación: distinguir pendiente de activo y de listo para ejecutar. No convertir automáticamente un fragmento incompleto del drawer. La fase es dependencia operativa, no categoría de negocio.

## UF05 — Ejecutar manualmente y revisar

Abrir tarea con contexto y procedimiento -> hacer trabajo -> reunir cambios/evidencia -> comparar con contrato -> pedir corrección o completar obligaciones -> cierre vía autoridad Deskops -> revisar conocimiento durable y fase.

Aceptación: ninguna acción usa edición arbitraria de status para saltarse gates. Distinguir declarado, encontrado y verificado. Reabrir enlaces durante revisión no pierde el encargo.

## UF06 — Delegar e intervenir

Preparar bundle -> registrar intento y dispatch confirmado -> seguir ejecución -> recibir pregunta con referencias -> responder/decidir -> consultar resultado y evidencia -> revisar/corregir -> cerrar mediante workflow.

Aceptación: cada mensaje/resultado corresponde al intento correcto; completado por agente no implica aprobado. Requiere ramal Scion real y no bloquea UF01–UF05.

## UF07 — Diagnosticar y mantener

Abrir diagnóstico -> identificar documento/ancla/relación afectada y causa -> inspeccionar soporte -> corregir o registrar trabajo -> reevaluar -> conservar procedencia.

Aceptación: se distingue error, conflicto, cambio y pérdida de soporte. Las operaciones de reparación muestran alcance; no recrean silenciosamente evidencia ausente.

## UF08 — Cambiar de proyecto

Seguir referencia de otro desk -> resolver identidad y contexto de store -> leer destino -> volver (envío interdesk queda fuera de baseline) -> conservar proyecto origen y destino.

Aceptación: no escribir en otro desk por confusión de cwd ni copiar documentos ajenos para aparentar navegación federada.

## UF09 — Inspeccionar y cambiar un contrato de modelo

Desde un documento -> abrir Schema/clase origen -> inspeccionar campos/referencias/template -> editar draft por APIs existentes -> validar -> promover solo con autoridad y evidencia -> diagnosticar impacto. No editar modelos por payload libre ni prometer soporte no disponible. WS39 implementa el delta y valida este flujo por separado.

## UF10 — Arranque y ausencia de desk

Seguir instrucciones reproducibles de instalación/arranque -> abrir ejemplo Taller -> si no hay desk, mostrar orientación e invocación init CLI con destino explícito -> refrescar tras resultado real. No ejecutar inicialización por un GET ni mutar el proyecto equivocado.

## Precisiones de revisión

UF04/05 tienen handoff a Git/closeout externo; no se promete cierre HTTP. UF06 requiere WS34/36 para acciones, no solo lectura de mensajes. UF07 reparaciones se hacen por operaciones existentes documentadas, no un botón universal. UF08 inicialmente read-only; una mutación interdesk no es parte implícita de navegar. Captura/archivo no modelado no debe tratarse como corrupción. Matriz de aceptación, nodos y gates: ../cobertura.md y ../validacion-humana.md. Los pasos de intención no acreditan capacidades implementadas.

UF03: WS19 cubre campos y relaciones; WS42 cubre split/merge/tipado existentes. UF04: WS26 incluye enrutamiento y capa lista. UF08 baseline es solo lectura entre desks vía WS41; no se promete enviar ni mutar destino. UF10 usa corpus de WS40. Los gates de uso siguen validacion-humana.md, no el simple cierre de una tarea de código.

UF03 no promete generar destinos arbitrarios desde una materialización: la entrega soporta inspección/procedencia y operaciones existentes comprobadas. Generación nueva de docs/diagramas exige su contrato del repo dueño. WS43 publica navegación real tras validar el ejemplo; no basta considerar el corpus como ecosistema final.

FILE:desk/drawer/plans/workspace-documental/validacion-humana.md
# Protocolo de uso y evidencia

Protocolo con base P08 aceptada el 2026-10-31 (owner-decisions.json ítem 2). Participante: solicitante humano de esta sesión; puede designar sustituto expresamente. Agente de pruebas prepara entorno y observa; no firma como usuario humano ni convierte screenshots en aprobación.

## Ejemplo reproducible

Proyecto Taller bajo graph_ui:.tmp/workspace-documental-ejemplo/, con su propio git y desk/store temporal creado por CLI real. Incluir Board, task, pill, ritual/step, átomo/protoátomo/crossroad, FAQ, issue Markdown no modelado y una referencia intencionalmente rota. Segundo desk temporal para UF08 y tercer repo temporal sin desk para UF10. Todo dato de prueba debe generarse por contratos reales cuando aplique, no mocks que sustituyan la API; sin secretos/corpus ajeno. No probar mutaciones sobre este desk de desarrollo. WS40 es el productor único del generador versionado y de los dos desks temporales. WS17 aporta solo plantillas de navegación authored bajo ejemplo/nav/; WS40 las materializa si se suministran.

## Gates por rebanada

- WS16: UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque. Encontrar un concepto desde entrada/búsqueda, abrir soporte, volver y cambiar representación con identidad; diagnosticar link roto y backend ausente. Necesita corpus WS40 y lectura multidesk WS41; no necesita edición, índices nuevos, Scion ni Changes global.
- WS30: UF02, UF03 edición, UF04, UF05. Capturar sin tarea obligatoria, preparar autoría/contexto y evidencia, provocar conflicto en dos ventanas, comparar diff real y cerrar por handoff autorizado externo. WS17 integra entradas/index authored en esta prueba; WS42 cubre operaciones de conocimiento. WS30 usa variante source_mode de P04, con fuente editable o explícitamente read-only según decisión.
- WS37: UF06 con Scion real e intervención humana; requiere G_EXEC. No se ejecuta solo porque el DAG está revisado.
- WS39: UF09 modelos; validar su prueba específica antes de etiquetar capítulo de personalización como disponible.
- WS29: UF07 impacto avanzado; prueba propia de mutaciones y soporte. Su ausencia no bloquea manual básico, que debe decirlo.

Habilitar mutaciones de baseline en UI requiere G_HUMAN_READ; desarrollo/pruebas aisladas de API no esperan ese acta humana; las representaciones solo lectura pueden construirse en paralelo sin que eso implique aceptación humana.

## Evidencia y aceptación

Guardar guion, versiones/commits, corpus, comandos públicos, timestamps y resultados técnicos; grabación o capturas del recorrido; observaciones, fallos y decisión explícita del participante. La persona debe poder completar el guion sin rutas memorizadas ni instrucciones verbales correctivas del agente. Registrar ayudas solicitadas. Un fallo de recorrido bloquea el gate correspondiente y abre tarea de corrección, no solo un cambio de umbral.

Objetivos iniciales aceptados por P08 (no mediciones obtenidas): lectura/navegación local caliente p95 <=2 s, guardado local <=3 s; primer arranque <=10 s en corpus de ejemplo. Si una operación excede 1 s, estado de progreso visible sin afirmar éxito; registrar error/timeout. Medir al menos 20 aperturas, 10 búsquedas (WS16 y WS30) y 10 guardados (solo WS30, porque WS16 no muta) sobre corpus y tamaño documentados; no extrapolar producción. Carga grande se reporta aparte.

## Qué significa disponible

Disponible y comprobado: versión/commit implementado, pruebas relevantes verdes, recorrido correspondiente aceptado y pasos del manual verificados en esa versión. Propuesto: intención/diseño sin esa evidencia. Bloqueado: dependencia o decisión identificada impide completarlo. Una tarea cerrada o un archivo existente no prueban por sí solos la etiqueta.

## Ubicación de evidencias

Las actas de WS16/30/37/39 viven en graph_ui:runs/subagents/workspace-documental-acceptance/{lectura,manual,delegacion,modelos}/acta.md (cada caso en su subdirectorio), no en el repo de planificación. WS43 guarda publicación real en deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md. Se pueden enlazar desde este plan; no copiarlas como segundo registro. output_base y output_scope de dag.yaml son autoridad de ubicación. El corpus tiene entrada mínima generada e instrucciones en WS40; WS16 no se reduce a buscar. WS30 prueba UF01 con las entradas enriquecidas de WS17.

La ubicación versionable no acredita que el acta esté versionada: incluirla explícitamente en el commit atómico de la tarea de validación del repo dueño. El recibo del gate debe enlazar ese commit y el blob de acta verificables; un archivo solo local o una captura no bastan.

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

FILE:runs/subagents/20261031-atribucion-decisiones/phase-closeout.md
# Cierre de fase, corrección de procedencia — 2026-11-01

Fase: procedencia en `decisiones.md`, tras el dictamen de WS07. Tarea cerrada: `6ac96c80`. Sin tareas activas al cerrar.

**Aprobación.** Revisión root de `fc9d6b47` y HEAD `85987c4f`: «APROBADO EL ENTREGABLE ACTUAL Y COBERTURA EFECTIVA WS07». Texto en `root-approval-20261101.md`. Verificó por su cuenta build, validate, status, 13 pruebas y los 73 bundles sin discrepancias. No aprueba suite general, runtime, API, UI ni Scion. No es aprobación humana.

**Orden real de los gates.** El closeout `6ac96c80` ocurrió sin PASS final de Tester: v4 y v5 dieron FAIL y el último cambio no tuvo Tester. El PASS focal documental del Tester root, sobre `85987c4f`, es posterior y queda como validación posterior. No se convierte el v5 en PASS.

**Validación compartida.** Ver `phase-validation.log`: build --check 0, validate --check 0, status all current, 13 pruebas del helper. Suite general: no se reabrió; sigue sin estar verde.

**WS06.** No hay registro de aprobación histórica propia; ese límite se conserva. Existe la revisión root en `runs/subagents/20261031-ajuste-canonico-ws06/review-source.md`, que verificó la matriz y pidió correcciones. La aprobación root actual ratifica la vigencia documental de la matriz corregida y permite esta dependencia. Es una ratificación actual: no se retrofecha ni afirma runtime.

**Pills.** Sin nuevas ni retiradas.

**Residuo durable.** Átomo `atom-separar-procedencia-exige-comparar-todas-las-columnas-contra-la-versión-previa`, con procedencia en el ledger.

**Trabajo capturado.** Notas de promoción en `runs/subagents/20261031-ajuste-canonico-ws06/promotion-notes.md`, adenda 2026-11-01.

**Siguiente.** Solo WS08 y WS10, sin arista entre sí. WS09, WS11, WS12 y código UI esperan checkpoint root. `execution_authorized` global sigue false.

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
