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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS11
id: WS11
title: Cerrar contrato de navegación e identidad
status: candidate
kind: planning
depends_on:
- WS09
- WS08
requires:
- G_PRODUCT
owner_repo: deskops
output_scope: contratos/navegacion.md; enlaces a recibos externos G_UI_READ por delta,
  G_SPEC_VIEW opcional
scope: Un documento Markdown mantiene identidad/ruta/modelo opcional; graph/code admiten
  otros nodos con origen. Resolución repo/store explícita, foco, enlaces/historia
  y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos. Instancia
  = documento concreto que falta escribir. Vínculo = referencia o enlace que falta
  entre documentos existentes.
acceptance: Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales;
  cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño
  antes de code. Registrar recepción lector por delta en graph_ui (actor P01, IDs,
  efecto y evidencia). El contrato básico puede cerrar sin recepción de Changes, Scion
  ni ViewDoc opcional; cada delta sigue bloqueado hasta su propio recibo. G_SPEC_VIEW
  se obtiene separadamente al preparar WS18, sin bloquear navegación base. WS11 cierra
  con contrato básico revisado, clasificación de huecos y mapa de deltas que requieren
  recepción; puede cerrar sin acta receptora. Recibos son producidos por solicitante
  P01/repo receptor al preparar cada delta, no por Executor de WS11 ni por escritura
  interrepo. Cada delta espera su propio recibo; contrato básico no afirma que ninguno
  se haya recibido.
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws11.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: deskops:desk/drawer/plans/workspace-documental/
node_role: delivery

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS09
id: WS09
title: Precisar catálogo de renderizaciones
kind: planning
owner_repo: deskops
node_role: delivery
scope: Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues,
  FAQ, Code y vistas existentes; ViewDoc es grafo, no contrato universal de UI.
acceptance: Cada fila tiene origen, contrato (o «sin contrato» si el soporte no lo
  tiene), renderer, acción/dueño, error y estado. Distinguir authored/derivado/preferencia
  local. Aplica a cada fila de las tablas de vistas.md y completa la ficha por fila.
  Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene
  de auditoria/ui.md (WS04); error = fallo visible esperado para esa fila. Filas compuestas
  admiten listas de contratos/renderers/acciones/errores y clasificación por componente
  authored/derivado/local; separar fila solo si el delta tiene evidencia/estado independiente.
  Para propuesto/bloqueado indicar error esperado condicionado a contrato/implementación,
  o no definido con productor WS11/12 si falta; nunca inventar error actual.
output_scope: borradores/vistas.md
depends_on:
- WS07
- WS10
- WS08
requires:
- G_PRODUCT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS08
id: WS08
title: Precisar user-flows y criterios observables
kind: planning
owner_repo: deskops
node_role: delivery
scope: 'Mapear UF a operaciones de WS02/03/04; cubrir manual, captura, revisión, cambios
  (UF07/WS29), arranque, multidesk, schemas y modo degradado (UF07, fallo de backend/dependencia).
  UF02 responder significa dentro del desk/contexto autorizado local; ack local: operación
  pendiente de confirmar en el contrato WS12; no se da por disponible. UF08 es lectura;
  envío interdesk fuera de baseline, sin excepción implícita a P07. Las operaciones
  vienen de auditoria/{deskops,infraestructura,ui}.md, disponibles por dependencia
  transitiva vía WS06/WS07.'
acceptance: Cada UF tiene entrada/salida, operación, error, nodo y gate humano; no
  prometer función fuera de alcance. Nodo = ID del DAG. Una operación ausente se marca
  hueco, sin inventarla. Cubrir todas UF01–UF10; operación/nodo/gate admiten listas
  completas, no elegir nodo principal. Distinguir gate humano WS16/30/37/39 de prueba
  técnica propia WS29; si no hay gate humano adicional escribir ninguno adicional.
  Delegación se documenta condicionada a G_SCION/G_EXEC, sin habilitarla.
output_scope: borradores/user-flows.md
depends_on:
- WS07
requires:
- G_PRODUCT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS12
id: WS12
title: Cerrar contrato de operaciones y escritura
kind: planning
owner_repo: deskops
node_role: delivery
scope: Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy
  coordinador, Git, workflow-protected fields, CAS/locks, fallos parciales, permisos
  y closeout fuera del servidor UI. Adapter = canal público existente (CLI/DeskopsOperations/API
  sldb) por el que la UI invoca cada operación; si no existe, se registra hueco y
  dueño, no se diseña uno aquí. Whitelist incluye campos protegidos definidos por
  modelos/lifecycle auditados WS02 (status/current_node/history/closeout_evidence
  entre otros que determine modelo), por modelo/operación; no lista universal inventada.
acceptance: 'G_WRITE_POLICY registrado. Publicar whitelist por operación/campo/canal/actor/revisión/Git/efectos
  y estado existente comprobado/faltante. Obtener recibo receptor y prueba solo para
  delta que se habilita: campos/intake no esperan Changes/modelos/Scion ni raw-source.
  G_WRITE_CONTRACT y G_UI_WRITE se evalúan por IDs/efecto, nunca como aceptación conjunta.
  Autoría de tareas/cierre esperan G_CLOSEOUT. Raw-source faltante tiene productor
  WS20 y G_SOURCE; recepción G_SLDB_WRITE antes de WS20, sin exigir API implementada
  para especificar contrato. Lock solo UI no coordina CLI/agentes: con otro coordinador
  escritor, read-only/handoff hasta API pública con autoridad compartida probada.
  WS12 solo escribe contrato y enlaces en deskops; no ejecuta mutaciones ni crea actas
  interrepo. Contrastar inventarios WS02–04 y contrato WS11, citar path/símbolo/commit
  observado; comprobado requiere evidencia real citada de API/prueba existente. Cierra
  con matriz de capacidades/efectos y huecos asignados, no requiere habilitar ninguna
  mutación. Receptor P01 en repo dueño produce acta por delta al prepararlo; G_WRITE_CONTRACT
  admite requisito de API faltante solo para el nodo productor de esa API (WS20),
  manteniendo consumidor WS21 bloqueado por G_SOURCE.'
output_scope: contratos/operaciones.md
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS13
id: WS13
title: Integrar lector workspace con historia y foco
kind: implementation
owner_repo: graph_ui
node_role: aggregate
children:
- WS13.1
- WS13.2
- WS13.3
scope: 'Implementación o delta conciliado sobre workspace integrado a1b2b22: documento/fuente
  solo lectura, contexto, enlaces, tabs/historia y selección por documento/nodo. Mantener
  Code local y rutas del host; no requerir índices nuevos. Incluir explorador de documentos
  modelados/no modelados, dos documentos lado a lado y tabs/historia. Se reutiliza
  el registro de vistas existente en shell/registry.js; organización de contenido
  procede de documentos/consultas.'
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS13.1, WS13.2, WS13.3'
depends_on:
- WS11
- WS13.1
- WS13.2
- WS13.3
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS13.1
id: WS13.1
title: Leer documento, contexto y enlaces
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS13
scope: Documento/fuente solo lectura, panel de contexto (identidad, relaciones y origen),
  enlaces y Code local con selección por documento/nodo. Mantener rutas del host;
  no requerir índices nuevos. Implementación o delta conciliado sobre el workspace
  integrado a1b2b22, según acta WS11. Foco = elemento/nodo seleccionado dentro del
  documento; documento activo identifica pestaña. Compartir foco solo donde exista
  correspondencia real de origen definida WS11; no inventar mapeo texto→código.
acceptance: 'Markdown sin modelo legible; el panel de contexto muestra identidad,
  las relaciones que declare el contrato WS11 y la ruta de origen reales; seguir un
  enlace y alternar entre texto/graph/code, en las representaciones que el catálogo
  WS09 (borradores/vistas.md) y el contrato WS11 declaren soportadas, preserva origen.
  La selección por documento/nodo fija el foco del documento abierto: seleccionar
  en Code, texto o graph actualiza ese foco y las demás representaciones del mismo
  documento lo comparten, sin abrir otra copia. No depender de conocer un ID; no crear
  otro workspace independiente.  La base a1b2b22 es punto de partida reutilizable;
  el cierre de este delta exige SU evidencia de aceptación ampliada Markdown no modelado/fuente,
  enlaces y foco. Ni cierre f16fcd1 ni commit previo sustituyen esa evidencia. Una
  copia es instancia documental con mismo origen, no cada representación.'
output_scope: frontends/mindmap/views/workspace/ (reutilizar node/workspace-view.js
  y componentes Document/Graph/Code/contexto existentes); rutas de lectura contrato
  WS11; tests/
depends_on:
- WS11
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS13.2
id: WS13.2
title: Explorar documentos modelados y no modelados
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS13
scope: Explorador sobre documentos reales del store y Markdown no modelado del desk.
  El árbol se obtiene de la API del store y del sistema de archivos del desk, según
  contrato WS11.
acceptance: Desde el explorador abrir un documento modelado y uno no modelado sin
  conocer su ID ni usar índices nuevos; al añadir un documento al store temporal de
  prueba, aparece sin cambiar código. Altas de documento modelado en store y Markdown
  no modelado en desk aparecen tras refresco explícito del catálogo sin reiniciar
  servidor ni cambiar código. Se permite reutilizar catálogo/filtro existente para
  modelados; WS11 determina API/seguridad para no modelados.
output_scope: frontends/mindmap/views/workspace/explorer/; rutas de lectura definidas
  por el contrato WS11; tests/
depends_on:
- WS11
- WS13.1
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS13.3
id: WS13.3
title: Abrir documentos en pestañas y divisiones con historia
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS13
scope: Pestañas, dos documentos lado a lado, foco e historia de navegación; disposición
  como estado local según P07, no como documento compartido. Foco es el elemento seleccionado
  dentro de un documento; origen es su soporte y ruta real. Cambiar de pestaña o división
  cambia el documento activo sin alterar el foco guardado de cada documento; volver
  restaura documento, foco y origen. Disposición por sesión de navegador; no se exige
  persistir tras recargar.
acceptance: Abrir, cambiar y cerrar pestañas; abrir dos documentos en divisiones,
  alternar el documento activo y volver conservando foco e historia. Volver sigue
  el orden inverso de navegación.
output_scope: frontends/mindmap/views/workspace/layout/; rutas de lectura definidas
  por el contrato WS11; tests/
depends_on:
- WS11
- WS13.1
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS17
id: WS17
title: Escribir entradas e índices del desk ejemplo
kind: documentation
owner_repo: deskops
node_role: delivery
scope: 'Escribir solo entradas/índices authored como plantillas versionadas bajo el
  paquete del plan; no es el productor del corpus. El generador de WS40 acepta estas
  fuentes y las materializa bajo su root temporal, sin copiar inventarios derivados
  ni escribir repos reales. Puede escribirse antes de WS16: el lector no depende de
  estos índices nuevos; WS30 sí los integra. Índice authored = texto curado y enlaces
  de entrada elegidos para recorrido, sin copiar listados completos del store que
  debe resolver consulta. Registry = desk/registry/repo-*.md existente inventariado
  WS02; enlazarlo/reutilizarlo, no duplicar otro catálogo.'
acceptance: 'Tras regenerar corpus WS40 con ejemplo/nav/, recorrer links Markdown
  sin UI; source versionado y destino temporal no son registros independientes. Verificar
  al regenerar que cada plantilla resuelve el root/store de procedencia de los dos
  desks del manifiesto WS40; no duplicar el registry de deskops. Plantillas son fuente
  única: destino temporal se regenera desde ellas, no se edita/commitea como registro
  competidor. Resolver cada link según identidad/root/store/aliases contrato WS11
  contra manifiesto WS40; conjunto de plantillas cubre ambos desks, no cada plantilla
  individual.'
output_scope: ejemplo/nav/ (plantillas Markdown versionadas en el paquete del plan)
depends_on:
- WS11
- WS40
requires: []

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS18
id: WS18
title: Declarar proyecciones de grafo reutilizables
kind: implementation
owner_repo: spec2viz
node_role: delivery
scope: ViewDoc con su NotationDoc (la notación que el ViewDoc referencia) para selecciones
  y notación ya soportadas por spec2viz; no crear UI pages declarativas ficticias.
  Selecciones concretas y notación requerida vienen de catálogo WS09 y contrato WS11,
  contrastados con capacidades WS03; si catálogo no fija selección mínima, detener
  promoción y corregir ese contrato antes de elegir una. No inventar selección aquí.
acceptance: Vista portable (el mismo ViewDoc sin código específico del host) renderiza
  sobre un store real la selección declarada, coincide con ella y el ViewDoc documenta
  qué selecciona; tareas receptoras en spec2viz se promueven por dueño. Gate receptor
  G_SPEC_VIEW requerido; este paquete documental deskops no escribe en spec2viz; la
  futura TaskDoc de WS18 se promueve y ejecuta en spec2viz por su supervisor/Executor,
  con recepción G_SPEC_VIEW para ese delta.
output_scope: sldb/views/ (rutas confirmadas por el dueño de spec2viz al promover);
  tests/
depends_on:
- WS09
- WS11
requires:
- G_SPEC_VIEW

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS33
id: WS33
title: Vincular mensajes, resultados y decisiones
kind: implementation
owner_repo: deskops
node_role: aggregate
children:
- WS33.1
- WS33.2
scope: Referencias Hub/proyecto/conversación/mensaje/intento y decisión humana explícita
  (WS33.2); dedup y procedencia. Backend documental, independiente de editor UI.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS33.1, WS33.2'
depends_on:
- WS32
- WS11
- WS33.1
- WS33.2
requires:
- G_SCION

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS40
id: WS40
title: Crear generador reproducible del corpus Taller
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: 'Versionar un generador en graph_ui que usa el contrato WS11 y los CLI reales
  de deskops/sldb verificados en WS02/WS03, no servidor fake. Crear dos repos temporales
  bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas), sus stores
  y documentos, incluyendo Markdown no modelado, Code local y referencia rota. Parámetro
  opcional con la ruta de plantillas WS17: WS40 cierra sin ellas, y WS17 regenera
  con ellas después. Generar instrucciones de instalación/arranque del ejemplo y entrada
  mínima ecosistema/proyecto con enlaces al Board del desk temporal, su FAQ Markdown
  y documentos de conocimiento, todos creados dentro del corpus temporal, para que
  WS16 pruebe una entrada sin esperar índices ricos WS17. Incluir un tercer repo temporal
  sin desk para UF10 y enlaces authored entre los dos desks con desk para UF08.'
acceptance: Un comando crea/recrea entorno aislado, hace commits git reales en los
  repos temporales y nunca toca desk real; imprime un manifiesto JSON con roots, stores,
  commits y documentos clave. Es productor único de corpus para WS16/30; WS17 solo
  aporta contenido authored. Entrada mínima y README de arranque reproducibles, manifiesto
  de ubicación y segundo desk; WS17 enriquece navegación posteriormente.
output_scope: tests/fixtures/workspace_documental/; script de seed; tests/
depends_on:
- WS11
- WS08
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS41
id: WS41
title: Implementar lectura segura entre desks
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Resolver aliases/roots explícitamente autorizados en contrato WS11, usando
  APIs públicas de stores; cada request conserva proyecto/store sin cambiar global
  SLDB_STORE. Leer segundo desk y volver, sin mutaciones cruzadas.
acceptance: 'UF08 lectura sobre dos stores de WS40: identidad/origen visibles, seguir
  enlaces authored del corpus entre desks y volver por la historia; alias no autorizado,
  path escapado y store ausente dan error visible; rechazar roots arbitrarios o paths
  escapados. No afirmar federación por copiar contenido.'
output_scope: frontends/mindmap/source/; rutas de lectura por store definidas por
  contrato WS11, que llaman a APIs públicas; views/workspace/; tests/
depends_on:
- WS13
- WS11
- WS40
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_PRODUCT:
  title: Decisiones de producto registradas por humano
  state: satisfied
  resolver: WS07
  evidence: 'decisiones.md: P01/P02/P04/P07/P08/P09, actor/tipo/fuente/resultado registrados;
    no aprobación técnica ni Scion'
  produced_by: WS07
  verified_evidence: runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json;
    decisiones.md P07/P09 defaults técnicos delegados, 2026-10-31
G_UI_READ:
  title: Deltas de lectura aceptados en graph_ui
  state: pending
  resolver: 'external: solicitante P01 receptor del repo al preparar/promover el delta
    concreto'
  evidence: 'Acta de recepción por delta concreto en repo receptor: actor solicitante
    humano designado P01, fecha, alcance/IDs, efecto, task receptora/no solapamiento
    y commit/blob verificable. Cada nodo usa solo su recibo; ausencia de otro delta
    no bloquea este. Estado global pendiente resume recibos, no obliga aceptación
    conjunta. Productor del acta: receptor del repo dueño al preparar/promover ese
    delta, enlaza contrato WS11; Executor deskops solo registra el enlace, no escribe/commitea
    actas interrepo.'
  scope_nodes:
  - WS13
  - WS13.1
  - WS13.2
  - WS13.3
  - WS14
  - WS15
  - WS15.1
  - WS15.2
  - WS22
  - WS23
  - WS24
  - WS27
  - WS27.1
  - WS27.2
  - WS29
  - WS35
  - WS40
  - WS41
  evaluation: per_delta
  accepted_scope_nodes: []
  contract_source: WS11
G_SPEC_VIEW:
  title: Alcance de proyecciones aceptado en spec2viz
  state: pending
  resolver: 'external: solicitante P01 receptor del repo al preparar/promover el delta
    concreto'
  evidence: 'Acta de recepción por delta concreto en repo receptor: actor solicitante
    humano designado P01, fecha, alcance/IDs, efecto, task receptora/no solapamiento
    y commit/blob verificable. Cada nodo usa solo su recibo; ausencia de otro delta
    no bloquea este. Estado global pendiente resume recibos, no obliga aceptación
    conjunta. Productor del acta: receptor del repo dueño al preparar/promover ese
    delta, enlaza contrato WS11; Executor deskops solo registra el enlace, no escribe/commitea
    actas interrepo.'
  scope_nodes:
  - WS18
  evaluation: per_delta
  accepted_scope_nodes: []
  contract_source: WS11

FILE:instruccion
Revisa el nodo WS11 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

