FILE:desk/drawer/plans/workspace-documental/context-review-guide.md
# Guía breve para revisar un nodo del plan

Esta guía va en todo input de context review. Deriva de brief.md y alcance.md; no añade requisitos de producto.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende bien como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el producto es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de IDs, aristas y gates. Las candidatas no son tareas activas: ninguna tiene ejecución autorizada.
- ROOT y PK son agrupaciones de revisión, no dependencias ni entregables. Un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una variante añade dependencias y gates a los del nodo base; nunca los quita.
- Una flecha significa prerrequisito -> dependiente.
- Un gate pendiente es intencional. No es defecto que aún no esté satisfecho.
- P01–P06/P08 son decisiones humanas registradas; P07/P09 defaults técnicos delegados. No inventes aprobación de implementación/API/uso ni permisos Scion. No vuelvas a pedir decisiones ya resueltas.
- Los gates con evaluation=per_delta requieren solo recibo del nodo/efecto concreto; el estado global resume pendientes, sin obligar aceptación conjunta de otros deltas. G_HUMAN_READ bloquea habilitar mutaciones en UI, no desarrollo/pruebas aisladas de API.
- Una dependencia futura que debe producir un contrato, API o inventario no es ambigüedad si el encargo nombra quién lo produce y qué hacer si falta.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance.

No cuentan: actas o contratos pendientes con productor, detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills), trabajo de nodos dependientes o funciones excluidas en alcance.md.

Tampoco cuentan: textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará dentro de la aceptación, ni el comportamiento ante un contrato ausente, que alcance.md resuelve en "Reglas comunes de ejecución".

Cita la frase del input que origina cada ambigüedad.

FILE:desk/drawer/plans/workspace-documental/brief.md
# Brief autosuficiente y glosario — base final de planificación

## Encargo y acuerdos explícitos del solicitante

La persona solicita un DAG que cubra el workspace documental, sus vistas/renderizaciones, manual y user-flows; el encargo actual finaliza planificación con decisiones humanas registradas. Esto autoriza corregir el plan, no implementar la UI ni modificar tareas de otras sesiones.

Extractos textuales que delimitan intención, conservados aquí para no depender del historial:

> «cada documento es simplemente un markdown ... cada vista es basicamente una renderizacion»

> «nos faltan documentos para hacer el ecosistema realmente navegable o no?»

> «ahora si estamos en la misma pagina ... como te imaginas que un humano usaria esto?»

La última respuesta siguió al paralelo con Org-mode/Obsidian/IDE: exploración, lectura y edición sobre un proyecto. No se aprobó por ello una lista específica de pantallas, permisos, backend nuevo o cierre por HTTP. La crítica a la primera pestaña Deskops invalida usar esa pestaña como especificación suficiente del producto; no borra las capacidades reutilizables de Mindmap.

## Vocabulario

- **Documento**: archivo Markdown authored, con identidad de resolución; puede tener contrato estructurado o no. Renderizado/fuente no son dos copias.
- **Nodo**: elemento del grafo; puede corresponder a documento, modelo, sección, símbolo u otro soporte. No toda entidad runtime es Markdown.
- **Vista de trabajo**: selección de contenido más forma de presentarlo en el workspace. No implica página ni archivo nuevo.
- **Renderización/representación**: transformación visible del soporte; la edición se dirige a su origen y autoridad.
- **Renderer**: pieza de la UI que materializa una representación.
- **Proyección de grafo ViewDoc**: contrato existente de spec2viz para nodos por modelo/predicado, relaciones, dirección y notación/layout. No define por sí mismo formularios, tabs o tableros.
- **Composición**: representación que reúne contenido de varios documentos; cada edición va al documento dueño de ese contenido.
- **Consulta**: selección derivada evaluada por infraestructura; no un inventario authored duplicado. No se promete modelo de consulta guardada sin prueba de WS03.
- **Foco**: elemento seleccionado por una persona, compartido entre representaciones del mismo documento; no selección compartida entre usuarios.
- **Historia de navegación**: abrir/volver y documentos abiertos. Distinta de historial Git o decisiones de workflow.
- **Disposición**: pestañas, divisiones y preferencias locales. No datos de dominio ni registro compartido por defecto.

## Términos del desk y de operación

- **Drawer / candidato**: trabajo capturado en desk/drawer/; un candidato no es tarea hasta autorarlo con `deskops add task`.
- **Inbox**: mensajes entrantes en desk/inbox/; ack registra recepción, no aceptación del trabajo.
- **Protoátomo**: átomo libre con título y contenido, aún sin clasificar (`deskops atoms proto`).
- **TaskDoc / Board**: tarea modelada y su lista de enrutamiento; enrutar es añadirla al Board.
- **RitualDoc, StepDoc, lifecycle**: procedimiento, pasos y grafo de transiciones del desk.
- **Fase y capa lista**: tareas sin dependencias pendientes ni archivos solapados, según el ritual de fase.
- **Soporte / origen**: archivo o dato real que respalda una representación, y su ruta o referencia.
- **Revisión / before-image**: hash con que una escritura prueba que partió del estado actual; si no coincide, se rechaza.
- **Modo degradado**: el backend o una dependencia falla y la UI sigue mostrando lo que puede, declarando el límite.
- **Capability**: operación concreta con su canal y efectos.
- **Handoff**: la UI prepara una acción y la deja a otro canal o actor; no equivale a hecha.
- **Intento / RunDoc / manifiesto**: una ejecución de un agente sobre una tarea, su documento y su registro canónico.

## Criterio de éxito

Una persona puede entrar, comprender un desk, navegar conocimiento/trabajo/procedimientos, editar por canales autorizados y revisar evidencia sin reconstruir rutas o relaciones de memoria. Una sesión sin agentes es válida. Agentes y trazabilidad son otro ramal, no el centro obligatorio de la UI.

## Estado de las decisiones

Ver decisiones.md. El núcleo ya está registrado en decisiones.md y owner-decisions.json. WS07 verifica/reutiliza ese registro, no vuelve a pedir firmas. La decisión de producto no acredita APIs, recepción técnica, actas de uso ni permisos Scion.

FILE:desk/drawer/plans/workspace-documental/alcance.md
# Alcance y límites de las entregas

## Entrega L — lector útil temprano

Abrir soporte real, fuente/render de lectura, foco/historia, búsqueda, links y errores honestos. Conserva las capacidades existentes de KB/Flujo/Brainstorm/Schema/Specs/Deskops cuando se integren en el host. Code local a 1–2 hops según soporte real ya en el ticket del workspace; no se promete navegación CST inexistente. WS16 valida antes de habilitar mutaciones en UI (desarrollo/pruebas aisladas API pueden avanzar con contratos técnicos); representaciones solo lectura pueden desarrollarse en paralelo.

## Entrega M — autoría y operación manual

Edición por API con revisión y fuente según variante P04, representaciones de Board/procedimiento/conocimiento, intake y autoría explícita, diff/evidencia, handoff de cierre externo y manual verificado. WS43 publica entradas del desk real después del corpus y gate manual. Captura/ack/advance no tienen por qué esperar al editor; cada acción espera solo su contrato y delta. No commits automáticos ni closeout HTTP. Privilegios y efectos definidos en WS12.

## Entrega E — Scion opcional

Registro por intento, mensajes/resultados/decisiones, API de dispatch/reply autorizada y UI de intervención con aprobación humana. No replica tablas internas ni sustituye broker. Mensajería distribuida/A2A y despliegue multiHub no se implementan aquí.

## Extensiones incluidas pero independientes

WS29: Changes/impacto comprobable del store actual. WS39: integrar capacidades existentes Schema/edición de clases. Tienen pruebas y estado propios; no se etiquetan disponibles por estar planeadas ni bloquean primer lector/manual básico.

## Fuera de alcance de esta línea base

Migrar a Kimun; desplegar infraestructura distribuida; editar otros repos remotos; colaboración multiusuario; rebases/deshacer/revert destructivos desde UI; renombrar/mover con reescritura global; editar binarios/adjuntos; exportar/publicar sitios; empaquetado offline/vendorizar todas las dependencias CDN. Para esas operaciones: lectura/diagnóstico y referencia a herramienta existente, o indicar no soportado. Abrir adjuntos referenciados solo con resolución segura si API lo soporta; no prometer editor binario.

Arranque: WS40 genera el ejemplo e instrucciones de instalación/apertura; WS16 las prueba y WS17 aporta índices; proyecto sin desk recibe orientación y handoff a init CLI. Crear desks desde UI no es requisito. El fallo CDN observado es parte de WS15 y una dependencia explícita del despliegue actual, no se oculta como offline funcional.

## Recepción y whitelist por delta

WS11 produce contrato básico de navegación; ViewDoc spec2viz WS18 es opcional y no bloquea WS24 ni manual. WS12 produce operaciones por delta, con actor/alcance/efectos/API/pruebas. Los gates evaluation=per_delta exigen solo acta y contrato del nodo/efecto requerido; accepted_scope_nodes registra recibos verificados. Ningún recibo existe aún. No esperar aceptación de Changes, modelos o Scion para cerrar lector/campos/intake. Las actas se guardan y commitean en repo receptor; no en este plan.

## Reglas comunes de ejecución

Si al llegar a un nodo falta un contrato, API, dato o permiso que debía producir una dependencia: detenerse, registrar el hueco con repo dueño y no crear sustituto. La operación queda no disponible.

Las pruebas de implementación usan un store temporal real creado en el test o el corpus WS40 cuando ya exista. Las validaciones humanas usan el corpus WS40.

Una dependencia transitiva cuenta como prerrequisito aunque no figure en `depends_on` directo: WS11 y WS12 ya llevan detrás WS02–WS10 según el DAG.

El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide.

## Regla para cambios de alcance

Antes de promover un nodo: revisar tareas/Board del repo receptor y reconciliacion.md. La implementación puede vincular/sustituir alcance en la tarea receptora aceptada; este plan no crea una segunda ejecución concurrente. Si cambia contrato, agregar nodo atómico en dag.yaml y volver a validar/revisar las dependencias afectadas. No dar por confirmado el estado de un repo usando solo un hash viejo.

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
| P01 | Extender Mindmap; solicitante responsable producto/aceptación de deltas graph_ui/sldb/spec2viz. Operador Scion se designa después. | Humana; solicitante; ítems 0 y 2 | WS04/06/07/11/12/13; G_PRODUCT; recepción técnica pendiente por delta |
| P02 | SLDB/pron + Deskops; Kimun fuera de esta línea base | Humana; solicitante; ítem 0 | WS03/06/07; G_PRODUCT |
| P03 | Con otro coordinador escritor, UI read-only/handoff hasta canal público con autoridad compartida CLI/agentes/UI probado; lock solo UI no basta | Humana; solicitante; pregunta y respuesta ítem 1 | WS12/19/25/26/28/34/36/42; G_WRITE_POLICY/G_WRITE_CONTRACT |
| P04 | source_mode=editable; guardar Markdown solo tras API reversible con revisión, conflictos, recuperación y campos protegidos probados | Humana; solicitante; ítem 1 | WS20/21/30/31; G_PRODUCT/G_SOURCE/G_SLDB_WRITE |
| P05 | Guardar no hace commit; cierre mediante workflow CLI/coordinador y refresco verificable | Humana; solicitante; pregunta y respuesta ítem 1 | WS12/27/28; G_WRITE_POLICY/G_CLOSEOUT |
| P06 | Promoción y cierre respetan workflow Deskops; preparar/handoff hasta canal completo comprobado | Humana; solicitante; pregunta y respuesta ítem 1 | WS12/26/28; G_WRITE_POLICY |
| P07 | Foco/historia/disposición locales; multidesk inicialmente read-only con rutas/aliases explícitos | Técnica conservadora; Executor por encargo TaskDoc v2 | WS11/13.3/41; G_PRODUCT |
| P08 | Taller temporal; solicitante participa. Objetivos abrir/buscar ≤2 s, guardar ≤3 s, arranque ≤10 s | Humana; solicitante; ítem 2 | WS08/16/30/40; G_PRODUCT; actas humanas aún pendientes |
| P09 | Entradas reales desk/README.md + mapa authored en deskops reutilizando registry; publicar WS43 tras validación | Técnica conservadora; Executor por encargo TaskDoc v2 | WS11/17/43; G_PRODUCT |

G_PRODUCT y G_WRITE_POLICY registran esta base, no funciones disponibles. G_SOURCE es producido por WS20 en sldb: contrato público de guardado raw-source con revisión esperada, extracción/validación/roundtrip, protección de campos y buffer recuperable ante conflicto/fallo. G_WRITE_CONTRACT/recepción se verifican por delta y efecto, sin aceptar modelos, Changes o Scion para habilitar campos/intake. Un recibo técnico nombra actor, IDs/alcance, fecha y commit/blob en repo dueño. Ninguna decisión autoriza dispatch, mensajes o acceso Scion; G_EXEC/G_SCION siguen pendientes. No repetir decisiones ya respondidas al promover WS07: verificar y reutilizar este registro.

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

FILE:desk/drawer/plans/workspace-documental/reconciliacion.md
# Reconciliación verificada — 2026-10-31

Auditoría acotada de Board, commits y código actual; no aceptación de producto ampliado. graph_ui HEAD 134a665: Board enruta solo edición contextual y Changes, ambos draft. Workspace integrado a1b2b22, cierre f16fcd1 y actualización Board 134a665. No recrear su TaskDoc eliminado: recibo `git -C ../UIs/graph_ui show f16fcd1^:desk/tasks/task-workspace-multiproyeccion-documento-grafo-local-codigo-y-contexto.md`. Las referencias externas de dag.yaml apuntan a fuente durable actual con SHA-256; editing/Changes conservan hash actual del draft.

Fuentes inspeccionadas: `frontends/mindmap/workspace_routes.py`, `views/workspace/node/workspace-view.js`, `workspace.mjs`, `workspace.css`, `deskops_routes.py`. Base real: GET /api/workspace/nodes y /node, identidad Model:name, IR/payload, vecindad 1–2 hops, Code referenciado con límites de repo/gitignore/binario/tamaño, contexto relaciones/hash, errores por proyección. UI tiene catálogo modelado con filtro local, alternancia Document/Graph/Code, historia URL/popstate, relaciones navegables y diagnóstico. No equivale a lectura raw-source genérica o búsqueda backend.

| Nodo/delta | Reutilización comprobada | Aceptación ampliada todavía pendiente |
|---|---|---|
| WS13 / WS13.1 | Workspace integrado, IR/payload, contexto/origen, grafo/Code y selección nodo | Markdown sin modelo, fuente íntegra legible, enlaces/foco cruzado con todos los soportes y contrato WS11 |
| WS13.2 | Catálogo de documentos del store | Explorar Markdown no modelado del desk y altas dinámicas sin conocer ID |
| WS13.3 | Historia browser y tab de representación | Pestañas de documentos, divisiones simultáneas, foco por documento; no confundir TABS Document/Graph/Code con pestañas documentales |
| WS14 | filterCatalog sobre id/título/modelo ya cargado | Búsqueda texto/campos/semántica por API pública real; teclado, consulta/foco, vacío/error/degradación distintos |
| WS15 / WS15.1 | Errores catálogo/nodo/proyección y problems_report reales | Link roto, backend ausente, fallos CDN y degradación bajo guion Taller; no afirmar offline |
| WS15.2 | Errores store inexistente | Orientación proyecto sin desk y handoff init probado |
| WS19 e hijos / WS21 | IR/payload y hash/contexto reutilizables; ticket edición sigue draft | Guardado por campos/relaciones, CAS/409/conflicto y guardas; raw-source depende WS20/G_SOURCE |
| WS22 | deskops_routes.py lee Board/tarea/gates/next con rutas validadas | Lista/tablero/dependencias integrados al lector, mismas identidades y soporte; status no es test aprobado |
| WS23 | Lifecycle/payload navegables como documentos | Procedimiento/StepDoc/ritual con pasos/fuentes; no marcar realizado por leer |
| WS24 | Grafo entrante/saliente y hasta 2 hops; lector genérico IR/payload | Markdown no modelado, clasificación, backlinks y navegación completa; no esperar ViewDoc WS18 opcional |
| WS27 / WS27.1 | Code puede inspeccionar referencias seguras | Diff e historial Git reales acotados a tarea/repos; no son Code preview |
| WS27.2 | Task payload/gates de lifecycle | Mostrar evidencia declarada/encontrada/verificada y soporte diferenciado mediante contrato closeout público |
| WS28 | POST /api/desk/advance con revisión Board+task y lock de proceso; solo avanza lifecycle | Verify/handoff cierre externo y refresco verificable. advance no cierra; lock UI no coordina escritores CLI/agentes |
| WS29 | Problems del índice de aristas y hashes contexto | Changes sigue draft: check/doctor/drift e impacto real; no CST/Merkle Kimun |
| WS32 e hijos | Infraestructura closeout existente, candidato Scion ya capturado | Correlación intento/manifiesto/RunDoc e idempotencia con Scion real; no autorizados ni duplicados por este plan |

WS06 mantiene esta matriz al promover: integrar delta en ticket receptor vigente, vincular evidencia ya existente, o tarea atómica propia sin solapamiento. Nunca volver a implementar base porque el TaskDoc histórico ya no existe. Ningún nodo completo solo por commit: cada aceptación ampliada debe probarse. WS01/WS07 ya tienen contenido documental cubierto en brief/decisiones; verificar ese recibo al promover, no reescribirlo como nuevo trabajo.

Recepción: solicitante fue designado producto/aceptación graph_ui/sldb/spec2viz en ítem 2. Eso no es acta técnica. WS11/12 registran acta por delta concreto con actor, alcance/IDs, fecha, efecto y commit/blob en repo receptor. G_UI_READ/G_UI_WRITE/G_SLDB_WRITE/G_SPEC_VIEW/G_WRITE_CONTRACT no exigen aceptar otros deltas. Lector/manual no esperan Changes, modelos, Scion ni spec2viz opcional.

Closeout: implementación 59244c9 y cierre 1fefa97 verificables, con Task-Id histórico; fuentes durables `deskops/services/closeout_gates.py`, `services/closure.py`, tests de evidencia declarada y lifecycle. Recibo `git show 1fefa97^:desk/tasks/task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo.md`. G_CLOSEOUT se decide con prueba focalizada actual y asociación task→commit exacta, nunca por desaparición. Autoría se refiere al registro de cierre según contrato existente, sin añadir una nueva capa de permisos. Baseline histórico reporta fallos ajenos de suite; esta tarea no arregla producto ni afirma suite global verde.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#parameters
source_mode:
  value: editable
  allowed:
  - pending
  - editable
  - read_only
  decided_by: P04/WS07
  evidence: decisiones.md P04; owner-decisions.json respuesta1; habilitación real
    requiere G_SOURCE
  variant_rule: Una variante añade sus depends_on/requires a los del nodo base; nunca
    los quita. Listas vacías significan que no añade nada.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS21
id: WS21
title: Integrar fuente y renderizado según source_mode
status: candidate
kind: implementation
depends_on:
- WS19
requires:
- G_UI_WRITE
- G_WRITE_CONTRACT
owner_repo: graph_ui
output_scope: frontends/mindmap/views/workspace/; tests/
scope: Alternar fuente/render con mismo origen, revisión y dirty buffer; usar guardado
  fuente autorizado. Composición escribe solo origen trazable soportado. Ejecutar
  solo la variante elegida por P04; Con pending no se prepara ni se promueve este
  nodo. Al alternar con cambios sin guardar se conserva el buffer; nunca se descarta
  sin confirmación explícita de la persona usuaria; si no confirma, el buffer se conserva.
  No requiere G_SOURCE si el humano eligió fuente read_only.
acceptance: Cumplir la aceptación específica de la variante P04. En editable, G_SOURCE
  y G_WRITE_CONTRACT pasan y se prueba edición/conflicto/roundtrip. En read_only,
  fuente legible no editable y edición por campos probada; manual/WS30 no declaran
  edición fuente disponible. En ambos modos una composición, si existe en el contrato
  WS12, escribe solo en el documento dueño de cada campo; si no hay soporte, queda
  de solo lectura y se declara.
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws21.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
overlap_with: editing
integration_mode: delta_or_existing_ticket; matriz WS06 llega de forma transitiva
  por WS11/WS12; never_parallel_duplicate
variants:
- when:
    parameter: source_mode
    equals: editable
  depends_on:
  - WS20
  requires:
  - G_SOURCE
  acceptance: Fuente y render editables con API reversible y campos protegidos; roundtrip/conflicto
    real.
- when:
    parameter: source_mode
    equals: read_only
  depends_on: []
  requires: []
  acceptance: Fuente explícitamente read-only y campos editables por API. Conservar
    buffer/foco, ocultar guardado fuente; manual y WS30 etiquetan este alcance sin
    afirmar edición fuente completa.
output_base: graph_ui:repository_root/
node_role: delivery

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS19
id: WS19
title: Integrar edición de campos con conflicto
kind: implementation
owner_repo: graph_ui
node_role: aggregate
children:
- WS19.1
- WS19.2
scope: Delta sobre workspace integrado a1b2b22 de edición; reutilizar editores y API,
  revisión esperada y conflicto visible; workflow-protected fields no editables por
  este canal. Incluir alta/baja de relaciones permitidas por contrato, usando API
  real y before-image; no crear semántica de relaciones en componente. G_HUMAN_READ
  habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar
  con sus contratos/gates técnicos sin acta humana de lectura.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS19.1, WS19.2'
depends_on:
- WS12
- WS19.1
- WS19.2
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS20
id: WS20
title: Comprobar o completar guardado fuente reversible
kind: implementation
owner_repo: sldb
node_role: delivery
scope: Primero verificar capacidad existente. Un documento raw-source se extrae/valida
  y guarda por API pública con revisión y preservación de campos protegidos; no sobrescribir
  Markdown desde browser.
acceptance: Reversible = guardar y volver a extraer conserva campos y secciones sin
  pérdida. En ambas ramas G_SOURCE exige API pública y tests de roundtrip, conflicto,
  recuperación tras fallo y campos protegidos. Si la capacidad existe, esos tests
  bastan y no se duplica código. Si falta, se implementa en sldb mediante tarea propia
  aceptada en G_SLDB_WRITE.
output_scope: src/sldb/api/documents/; src/sldb/cli/serve/; tests/
depends_on:
- WS12
requires:
- G_SLDB_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS30
id: WS30
title: Validar autoría y revisión manual completas
kind: validation
owner_repo: graph_ui
node_role: delivery
scope: Persona recorre UF02/03 edición/04/05; integra conocimiento y tarea en ejemplo;
  los escenarios de error, conflicto en dos ventanas y navegación por teclado del
  guion de WS08 y validacion-humana.md. Incluye explícitamente UF01 usando entradas
  authored WS17 materializadas por generador WS40, además de edición/operación; no
  limitarlo a búsqueda.
acceptance: Registro humano bajo protocolo; un fallo de guion bloquea el gate y el
  responsable del repo dueño abre tarea en el nodo que lo causó; una observación solo
  se registra. No llamar ready a un flujo solo por tests.
output_scope: runs/subagents/workspace-documental-acceptance/manual/
depends_on:
- WS17
- WS21
- WS22
- WS23
- WS24
- WS25
- WS26
- WS28
- WS42
requires: []

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_UI_WRITE:
  title: Deltas de mutación aceptados en graph_ui
  state: pending
  resolver: WS12
  produced_by: WS12
  evidence: 'Acta de recepción por delta concreto en repo receptor: actor solicitante
    humano designado P01, fecha, alcance/IDs, efecto, task receptora/no solapamiento
    y commit/blob verificable. Cada nodo usa solo su recibo; ausencia de otro delta
    no bloquea este. Estado global pendiente resume recibos, no obliga aceptación
    conjunta.'
  scope_nodes:
  - WS19
  - WS19.1
  - WS19.2
  - WS21
  - WS25
  - WS25.1
  - WS25.2
  - WS26
  - WS26.1
  - WS26.2
  - WS28
  - WS36
  - WS39
  - WS42
  evaluation: per_delta
  accepted_scope_nodes: []
G_WRITE_CONTRACT:
  title: Contrato técnico de operaciones verificado
  state: pending
  resolver: WS12
  produced_by: WS12
  evidence: 'Contrato técnico WS12 por delta/operación: canal público, campos, actor,
    revisión esperada, efectos, errores y pruebas reales/API existente o productor
    si falta; commit/blob verificable y revisión responsable. accepted_scope_nodes
    solo enumera IDs cuyo contrato de efectos requerido está comprobado; no esperar
    otros deltas ni confundir acta de recepción con prueba API.'
  evaluation: per_delta
  accepted_scope_nodes: []
  scope_nodes:
  - WS19
  - WS19.1
  - WS19.2
  - WS20
  - WS21
  - WS25
  - WS25.1
  - WS25.2
  - WS26
  - WS26.1
  - WS26.2
  - WS28
  - WS32
  - WS32.1
  - WS32.2
  - WS34
  - WS34.1
  - WS34.2
  - WS36
  - WS39
  - WS42
  - WS43
G_SOURCE:
  title: Fuente reversible y guardas de campos probadas
  state: pending
  resolver: WS20
  evidence: API pública y tests roundtrip/conflicto/campos protegidos, con revisión
    de contrato
  produced_by: WS20

FILE:instruccion
Revisa el nodo WS21 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

