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
- El dry-run sigue las aristas reales de `dag.yaml`. Describe orden y transferencia solo donde hay dependencia. Hermanos sin arista entre sí pueden consumir un mismo productor, pero no se entregan nada: entre ellos describe la integración conjunta. Expresiones como «en orden», «entre ellos» o «al siguiente» en las instrucciones no crean secuencia ni aristas.
- Un gate pendiente es intencional. No es defecto que aún no esté satisfecho.
- En P01–P06/P08 lo humano es el núcleo aceptado en pregunta y respuesta; sus derivaciones T-Pxx son técnicas explícitas, no firmas humanas. P07/P09 son defaults técnicos delegados. No inventes aprobación de implementación/API/uso ni permisos Scion. No vuelvas a pedir decisiones ya resueltas.
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
- **Proyección de grafo ViewDoc**: modelo de spec2viz (datos, sin ruta de store) para nodos por modelo/predicado, relaciones, dirección y notación/layout. El evaluador, las rutas de evaluación y guardado y el render viven en graph_ui, solo en modo local; el evaluador recibe el store por petición. No define por sí mismo formularios, tabs o tableros.
- **Composición**: representación que reúne contenido de varios documentos; cada edición va al documento dueño de ese contenido.
- **Consulta**: selección derivada evaluada por infraestructura; no un inventario authored duplicado. No se promete modelo de consulta guardada sin prueba de WS03.
- **Foco**: elemento seleccionado por una persona, compartido entre representaciones del mismo documento; no selección compartida entre usuarios.
- **Historia de navegación**: abrir/volver y documentos abiertos. Distinta de historial Git o decisiones de workflow.
- **Disposición**: pestañas, divisiones y preferencias locales. No datos de dominio ni registro compartido por defecto.

## Términos del desk y de operación

- **Drawer / candidato**: trabajo capturado en desk/drawer/; un candidato no es tarea hasta autorarlo con `deskops add task`. La captura directa a drawer (origen preservado, sin tarea activa, colisiones controladas) es un canal permitido pendiente del contrato WS12, que compara la API SLDB existente, su composición y un eventual wrapper Deskops; ninguno está aprobado.
- **Inbox**: mensajes entrantes en desk/inbox/; ack registra recepción, no aceptación del trabajo.
- **Protoátomo**: átomo libre con título y contenido, aún sin clasificar (`deskops atoms proto`).
- **TaskDoc / Board**: tarea modelada y su lista de enrutamiento; enrutar es añadirla al Board.
- **RitualDoc, StepDoc, lifecycle**: procedimiento, pasos y grafo de transiciones del desk.
- **Fase y capa lista**: tareas sin dependencias pendientes ni archivos solapados, según el ritual de fase.
- **Soporte / origen**: archivo o dato real que respalda una representación, y su ruta o referencia.
- **Revisión / precondición de escritura**: tres cosas distintas. (1) *Before-image por valor existente*: `expected` en `POST /save` de sldb, que compara el payload completo y responde HTTP 409 si no coincide; es una capacidad optimista real, con límites. (2) *Token publicado*: `version` / `content_hash` que sldb emite al leer un documento; hoy no se recibe en la escritura. (3) *Comparación o escritura pública con precondición compartida* entre API, CLI y UI: aún no probada. El contrato WS12 define representación, precondición, operaciones y escritores alcanzados; no se fuerza CAS en toda CLI ni un algoritmo de hash, y la frescura no se infiere por CLI. WS45 (sldb) verifica o completa esa precondición para la escritura de payload, independiente de `source_mode`.
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS37
id: WS37
title: Validar delegación con agente real
status: candidate
kind: validation
depends_on:
- WS36
- WS30
requires:
- G_EXEC
- G_SCION
owner_repo: graph_ui
output_scope: runs/subagents/workspace-documental-acceptance/delegacion/
scope: 'UF06 real: pregunta/intervención/corrección/evidencia/decisión y cierre por
  el handoff de WS28, con actor humano.'
acceptance: G_SCION/G_EXEC y protocolo de validacion-humana.md (guion, acta en runs/subagents/workspace-documental-acceptance/delegacion/);
  no sustituir integración por mocks ni completed por aprobación. No bloquea WS31.
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws37.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: graph_ui:repository_root/
node_role: delivery

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS36
id: WS36
title: Integrar delegación e intervención humanas
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Invocar solo el adaptador WS34 para dispatch/reply y registrar decisiones con
  WS33.2; revisión con actor/evidencia visible.
acceptance: Respuesta vinculada al intento y operación confirmada; la revisión muestra
  actor humano y evidencia enlazada de WS33.1/WS33.2, cubierto por test; ausencia
  de API o permisos se muestra como error en la pantalla y lo cubre un test. No autoaprobación
  ni simulación.
output_scope: frontends/mindmap/views/workspace/execution/; ruta fina hacia el adaptador
  WS34 autorizada por contrato WS12; tests/
depends_on:
- WS34
- WS35
requires:
- G_EXEC
- G_SCION
- G_UI_WRITE
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
  se registra. No llamar ready a un flujo solo por tests. Acta enumera plantillas/entradas
  WS17 validadas, paths/hashes y recorridos, para que WS43 pueda trazar publicación
  real. UF03 incluye edición y navegación/lectura necesarias para comprobar origen/resultado;
  WS16 ya cubre lectura completa. Si causa de fallo no está aislada, registrar incidente
  con repo/superficie y que supervisor receptor autorice diagnóstico antes de atribuir
  nodo; no inventar causalidad ni corregir otro repo.
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS38
id: WS38
title: Publicar capítulos verificados de delegación
kind: documentation
owner_repo: deskops
node_role: delivery
scope: Añadir al manual operación de delegación y revisión trazable tal como quedó
  en WS37.
acceptance: Cada paso remite al acta de WS37 y a operaciones reales; cada acuerdo
  durable deja su átomo vinculado; los fallos registrados en esa acta se documentan;
  se indica que G_EXEC es necesario para operar. Acuerdo durable = regla de operación/autoridad/identidad
  de delegación demostrada y reusable fuera de una sesión; incidente/timestamp/resultado
  puntual queda en acta. Buscar átomos existentes de WS31 por regla; enlazar/actualizar
  el mismo cuando cubre acuerdo, crear solo si no existe regla equivalente. No atomizar
  permisos de una sola sesión.
output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados
depends_on:
- WS37
- WS31
requires:
- G_HUMAN_DELEGATE

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_EXEC:
  title: Humano autoriza ejecución y comunicaciones del escenario
  state: pending
  resolver: external
  evidence: 'deskops:desk/drawer/plans/workspace-documental/autorizaciones/scion.md:
    permiso explícito del solicitante/designee para agente/proyecto/acciones/alcance/sesión.
    Plan/review no autoriza ejecución.'
G_SCION:
  title: Scion accesible y contrato público comprobado
  state: unverified
  resolver: WS44, operador a designar al abordar ramal E
  evidence: auditoria/scion-probe.md bajo paquete del plan; actor de WS44, fecha/Hub/endpoint/identidad/capabilities
    de API pública, sin secretos. WS05 solo inventaría; WS44 permanece bloqueada hasta
    probe real y puede revalidarse.
  produced_by: WS44
G_HUMAN_DELEGATE:
  title: Persona aprueba delegación
  state: pending
  resolver: WS37
  evidence: graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md;
    actor humano/versión/guion/resultado y soportes. Guardar en repo dueño, no en
    el paquete de plan deskops.
  produced_by: WS37
  evidence_ref:
    repo: graph_ui
    path: runs/subagents/workspace-documental-acceptance/delegacion/acta.md

FILE:instruccion
Revisa el nodo WS37 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

