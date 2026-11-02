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
| UF03 conocimiento | WS02/03/09/11/12 | WS13/14/19/21/24/42; WS20/45 precondiciones; WS29 extensión de impacto, no prerrequisito | WS16 lectura; WS30 edición |
| UF04 preparar trabajo | WS02/08/12 + G_CLOSEOUT | WS22/26; commits de promoción vía canal autorizado externo | WS30 |
| UF05 revisar y cerrar | WS02/08/12 + G_CLOSEOUT | WS13.3, WS23, WS27/28; closeout CLI/coordinador | WS30 |
| UF06 delegar/intervenir | WS05/11/12/44 + G_SCION/G_EXEC | WS32–36 | WS37; WS38 publicación |
| UF07 diagnosticar | WS03/08/11/12 | WS15; WS29 impacto; reparación externa documentada | WS16 diagnóstico; prueba propia WS29 |
| UF08 otro desk | WS03/08/11 | WS41 lectura multidesk, con WS13/14/15; WS40 corpus; sin envío interdesk en baseline | WS16 lectura; envío cruzado fuera de alcance |
| UF09 modelos | WS03/04/09/12 | WS39 reutiliza Schema/editar clases; WS13 lector; WS29 impacto avanzado, opcional | Prueba humana específica WS39; no bloquea WS31 |
| UF10 arranque y proyecto sin desk | WS02/04/08/11 | WS15 orientación + CLI init documentado; WS40 corpus; WS17 índices; WS43 publicación real | WS16 |

Las filas definen cobertura esperada, no capacidades entregadas. WS08 refina el guion sobre esta matriz; un cambio de nodos requiere actualizarla y validar referencias. Crear un desk desde browser, mover/renombrar, undo destructivo y adjuntos editables quedan explícitamente fuera en alcance.md.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS26.1
id: WS26.1
title: Autorar tarea, evidencia y contexto
status: candidate
kind: implementation
depends_on:
- WS12
- WS22
- WS47
- WS48
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_PAYLOAD_PRECONDITION
- G_UI_WRITE
- G_WRITE_CONTRACT
owner_repo: graph_ui
output_scope: frontends/mindmap/views/workspace/authoring/; endpoints autorizados
  por el contrato WS12; tests/
scope: 'Preparación del candidato en el drawer (UF04, paso preparar), con dos recorridos
  separados que el contrato WS12 (sección 4.4) distingue por la ruta y el store reales.
  Rastreado: escritura directa por update con la precondición expected (S02), guarda
  de contenido de WS47, admisión de WS48 y G_PAYLOAD_PRECONDITION; solo campos autorables
  (contenido, dependencias, files, references, tags, pills y closeout_evidence validada
  con el vocabulario cerrado existente), nunca id, status, current_node, history ni
  from_drawer. No rastreado: propuesta, handoff explícito a deskops edit task y refresco
  posterior que comprueba lo escrito, sin escritura desde HTTP, sin marcar aplicado
  por generar el comando; no disponible significa no guardar directamente desde la
  UI. Pills: reemplazo de la lista entera con la actual y la propuesta visibles, referencias
  validadas (navegación autorizada, existencia, tipo PillDoc) y conservadas salvo
  eliminación explícita. El handoff se ofrece solo si una comprobación previa confirma
  que el selector no resuelve a una tarea activa. No crea la tarea activa ni añade
  al Board (eso es WS26.2), no rastrea por reflejo, no amplía S06 ni inventa API.
  G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de
  API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.'
acceptance: 'Recorrido rastreado: evidencia declarada, dependencias y pills persisten
  y son visibles tras recargar; un guardado obsoleto se rechaza con 409 sin perder
  el texto local. Recorrido no rastreado: la prueba muestra propuesta y handoff correctos,
  ninguna escritura desde HTTP y una lectura posterior que refleja la preparación
  hecha fuera de la UI; no hay prueba de guardado obsoleto para el CLI ni se marca
  aplicado por generar el comando; un botón deshabilitado no cumple. Caso con una
  tarea activa y un candidato de selector coincidente (nombre idéntico y prefijo):
  no se ofrece el comando. Evidencia vacía o incompleta queda pendiente. Nunca editar
  status; no se crea tarea activa ni ruta en el Board. Si una operación Git no tiene
  contrato o dueño, la acción queda en handoff explícito y se declara no disponible.'
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws26-1.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: graph_ui:repository_root/
node_role: delivery
parent_id: WS26

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS12
id: WS12
title: Cerrar contrato de operaciones y escritura
kind: planning
owner_repo: deskops
node_role: delivery
scope: Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy
  coordinador, Git, workflow-protected fields, precondición de escritura (before-image
  por valor, token publicado o CAS solo si el contrato lo fija)/locks, fallos parciales,
  permisos y closeout fuera del servidor UI. Adapter = canal público existente (CLI/DeskopsOperations/API
  sldb) por el que la UI invoca cada operación; si no existe, se registra hueco y
  dueño, no se diseña uno aquí. Whitelist incluye campos protegidos definidos por
  modelos/lifecycle auditados WS02 (status/current_node/history/closeout_evidence
  entre otros que determine modelo), por modelo/operación; no lista universal inventada.
acceptance: 'G_WRITE_POLICY registrado. Publicar whitelist por operación/campo/canal/actor/revisión/Git/efectos
  y estado existente comprobado/faltante. Mapear qué recibo receptor/prueba corresponde
  a cada delta; receptor P01 registra acta en su repo al preparar ese delta, no WS12:
  campos/intake no esperan Changes/modelos/Scion ni raw-source. G_WRITE_CONTRACT y
  G_UI_WRITE se evalúan por IDs/efecto, nunca como aceptación conjunta. Autoría de
  tareas/cierre esperan G_CLOSEOUT. Raw-source faltante tiene productor WS20 y G_SOURCE;
  recepción G_SLDB_WRITE antes de WS20, sin exigir API implementada para especificar
  contrato. Escritura de payload por campos: WS12 define la representación de la precondición,
  las operaciones y los escritores alcanzados, distinguiendo before-image por valor
  existente (`expected`, HTTP 409), token publicado (`version`/`content_hash`) y comparación
  o escritura pública con precondición compartida (aún no probada); no fuerza CAS
  en toda CLI ni un algoritmo, ni infiere frescura por CLI, y P03 no cambia. Su productor
  es WS45 (sldb, independiente de source_mode) y su gate G_PAYLOAD_PRECONDITION. Captura
  directa a drawer: WS12 compara API SLDB existente (`sldb.api.create_document`, DrawerService),
  composición de llamadas a esas API (no la Composición del glosario) y eventual wrapper
  Deskops, sin aprobar ninguna ni crear API o modelo por reflejo; `message send` más
  `promote` no queda aprobado (la promoción borra la nota y deja `why` apuntando a
  una ruta borrada). La captura a protoátomo entra en la whitelist con su canal o
  con su hueco y dueño. Solo si falta conducta de workflow se registra un productor
  Deskops explícito antes de WS25.2; si esa composición de llamadas cumple, se documenta
  prueba y contrato. Lock solo UI no coordina CLI/agentes: con otro coordinador escritor,
  read-only/handoff hasta API pública con autoridad compartida probada. WS12 solo
  escribe contrato y enlaces en deskops; no ejecuta mutaciones ni crea actas interrepo.
  Contrastar inventarios WS02–04 y contrato WS11, citar path/símbolo/commit observado;
  comprobado requiere evidencia real citada de API/prueba existente. Cierra con matriz
  de capacidades/efectos y huecos asignados, no requiere habilitar ninguna mutación.
  Receptor P01 en repo dueño produce acta por delta al prepararlo; G_WRITE_CONTRACT
  admite requisito de API faltante solo para el nodo productor de esa API (WS20 raw-source
  con G_SOURCE; WS45 precondición de payload con G_PAYLOAD_PRECONDITION), manteniendo
  consumidor WS21 bloqueado por G_PAYLOAD_PRECONDITION y, solo en variante editable,
  G_SOURCE. Elegir la representación de la precondición es entregable de este contrato,
  justificado por operaciones y escritores alcanzados y reutilizando lo existente;
  WS45 la verifica. «Receptor P01» aplica a graph_ui, sldb y spec2viz: en deltas de
  deskops no se crea recepción nueva y rige la autorización de trabajo local. Falta
  conducta de workflow cuando ni la API ni su composición de llamadas pueden, con
  prueba real, preservar origen, no crear tarea activa y controlar colisiones. Para
  el ramal E, este contrato asume producir, como sección por delta de WS34.1 y WS34.2,
  la política y el umbral de timeout de dispatch y reply y su clasificación observable
  (al menos aceptado, rechazado y vencido sin confirmación). La duración no se elige
  ahora: esa sección del contrato WS12 la fija al preparar esos deltas, no WS34, y
  su ausencia no impide cerrar el contrato núcleo de las Entregas L y M.'
output_scope: contratos/operaciones.md
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS22
id: WS22
title: Renderizar Board como trabajo navegable
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Representar Board real como lista, como tablero agrupado por estado y con las
  dependencias declaradas en el TaskDoc, abriendo en el lector los mismos TaskDoc
  y sus pills/átomos referenciados. No reemplazar workflow con drag-and-drop de status.
acceptance: Las tres representaciones (lista, tablero y dependencias) abren el mismo
  TaskDoc; selección y links comunes con lector; estados y condiciones de lifecycle
  leídos de deskops (Board, lifecycle), no de dag.yaml; no duplicar tareas ni presentar
  predicado satisfecho como test aprobado.
output_scope: frontends/mindmap/views/workspace/board/; tests/
depends_on:
- WS13
- WS09
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS47
id: WS47
title: Proteger contenido no declarado en la edición por campos de /save
kind: implementation
owner_repo: sldb
node_role: delivery
scope: Productor planificado de la guarda de conservación de contenido no declarado
  (HO-07 del contrato WS12, sección 6.7), distinta de la precondición de WS45 (igualdad
  de payload por expected) y de la protección de campos del adaptador de la UI. Canal
  elegido por el contrato, la edición por campos que termina en save_document_payload
  (POST /save update y update de graph_ui local). Primero inventario con ruta, símbolo
  y commit de refuse_structural_noise y refuse_undeclared_frontmatter, que create_document
  y track_document_file ya aplican al Markdown que se crea, y de la guarda de deskops
  edit sobre el archivo previo; la guarda de este nodo inspecciona el archivo previo
  y el efecto de reescribirlo, no solo el render nuevo, y reutiliza ese criterio antes
  de crear otro. No amplía WS45, no cambia la creación, no resuelve el gap de prevalidación
  de update capturado en el inbox de sldb (si toca el mismo código, las ediciones
  van en serie) y no se sustituye con un workaround de Deskops.
acceptance: Pruebas reales focalizadas en sldb sobre el canal elegido, tras recibo
  G_SLDB_WRITE para este delta. La guarda inspecciona el archivo previo y el efecto
  de reescribirlo, no solo el render nuevo, con el criterio de la guarda de deskops
  edit y de refuse_structural_noise y refuse_undeclared_frontmatter leído en fuente,
  sin inventar otro. La aceptación declara qué pérdida detecta, qué casos no detecta
  y qué casos quedan deshabilitados; un residuo declarado no aprueba una pérdida conocida
  dentro del alcance que el nodo pretende habilitar. Un update con expected vigente
  que perdería contenido no declarado del archivo se rechaza con error observable
  y sin cambios; un update seguro, cuyo render no pierde contenido (incluido un documento
  limpio), se aplica; un expected obsoleto sigue dando 409; la creación no cambia.
  Sin merge ni restauración, y sin prometer editar todo documento con ruido. Hasta
  que pasen, WS19.1, WS19.2 y el recorrido directo de WS26.1 no habilitan la edición
  de documentos con contenido no declarado. Este nodo es plan; no afirma que exista
  ni que esté implementado o aceptado.
output_scope: inventario y pruebas focalizadas; src/sldb/api/documents/ y src/sldb/cli/serve/
  solo para la guarda; tests/
depends_on:
- WS12
requires:
- G_SLDB_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS48
id: WS48
title: Admitir escrituras de la UI en modo manual exclusivo
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: 'Productor común de la evidencia de modo manual exclusivo (T-P03.1, HO-03;
  contrato WS12, secciones 5 y 5.9), previo a toda mutación habilitada en la UI y
  no contenido en WS19.1, para que ack y captura no dependan de WS19.1. Un único punto
  de admisión que toda ruta de escritura de la UI, existente o nueva, consulta antes
  de invocar su canal, con una afirmación vigente suministrada fuera de la petición
  (configuración confiable del responsable del desk, cargada por este nodo y sin valores
  reales en el repo) y consultas públicas existentes para la evidencia contraria;
  no hay registro nuevo del coordinador en Deskops y el prompt de Scion no es señal
  consultable. Salidas, admitida con el texto declarado sin evidencia contraria a
  una hora, o lectura/handoff con su causa. Cubre la ruta ya en uso POST /api/desk/advance
  (el botón Avanzar de views/workflow/deskops/deskops-view.js): rechazo en el servidor
  antes de advance_task cuando falta la afirmación o la evidencia, y estado y mensaje
  del botón; se conservan revision, gates y rechazos existentes y no se crea una operación
  nueva de lifecycle. La ausencia de evidencia contraria no prueba exclusividad, y
  con otro coordinador escritor la UI queda en lectura o handoff (P03). No crea servicio
  de identidad, autenticación ni coordinación distribuida, ni lock, ni CAS universal,
  ni un 409 donde el canal no ofrece precondición. No exige G_HUMAN_READ para desarrollar
  y probar el mecanismo; la habilitación real de los consumidores sigue requiriendo
  los gates humanos correspondientes y esto no permite usar escrituras en el producto.'
acceptance: Pruebas en un store temporal. POST /api/desk/advance sin afirmación vigente
  o sin evidencia se rechaza en el servidor antes de invocar advance_task, y el botón
  Avanzar muestra su estado deshabilitado y el mensaje de la causa; con admisión,
  la ruta conserva revision, gates y rechazos existentes. Sin afirmación vigente la
  mutación queda deshabilitada y se ofrece handoff. Con evidencia contraria, o con
  la herramienta de evidencia ausente o con error, lectura o handoff con su causa
  y el buffer conservado. Con afirmación y sin evidencia contraria se admite sin afirmar
  exclusividad comprobada. Evidencia contraria tras escribir bloquea la siguiente
  escritura. Los consumidores WS19.1, WS19.2, WS21, WS25.1, WS25.2, WS26.1, WS26.2,
  WS28, WS39 y WS42 dependen de este nodo y lo usan, ninguno lo reimplementa. Acta
  P01 del delta. Este nodo es plan; no afirma que exista ni que esté implementado
  o aceptado.
output_scope: frontends/mindmap/ (módulo común de admisión de escritura; archivo exacto
  en el TaskDoc); tests/
depends_on:
- WS12
requires:
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS26
id: WS26
title: Integrar autoría y contexto de tareas
kind: implementation
owner_repo: graph_ui
node_role: aggregate
children:
- WS26.1
- WS26.2
scope: Autoría explícita desde candidato, evidencia declarada, dependencias y contexto/pill
  binding; promoción solo cuando el contrato resuelve commits previos por canal autorizado.
  Incluir enrutamiento explícito en Board y representación de capa lista por dependencias/no
  solapamiento; sin confundir Board route con ejecución. El canal de promoción debe
  respetar commits previos y estado real. G_HUMAN_READ habilita uso de mutaciones
  en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates
  técnicos sin acta humana de lectura.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS26.1, WS26.2'
depends_on:
- WS12
- WS22
- WS26.1
- WS26.2
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_PAYLOAD_PRECONDITION
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS26.2
id: WS26.2
title: Enrutar en Board y mostrar capa lista
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS26
scope: 'Enrutamiento explícito en Board y representación de capa lista por dependencias/no
  solapamiento; promoción solo cuando el contrato resuelve commits previos por canal
  autorizado. Autorizar, crear la tarea activa y enrutarla en el Board es una operación
  conjunta (W01 del contrato WS12: crea el TaskDoc y lo añade al Board), posterior
  a la preparación del candidato en WS26.1 y a la autorización de la persona; nunca
  una operación parcial ni un efecto oculto de WS26.1. Los commits previos y la promoción
  van en handoff cuando el contrato no ofrece canal. Enrutar un TaskDoc ya existente
  no tiene operación pública con precondición (HO-12). Capa lista = tareas sin dependencias
  pendientes y sin archivos solapados según los `files` declarados en cada TaskDoc
  y el ritual de fase. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y
  pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta
  humana de lectura.'
acceptance: 'Tras enrutar, `deskops show board` muestra la tarea y la UI la distingue
  de una tarea en ejecución; el canal de promoción respeta commits previos y estado
  real; la capa lista se muestra separada de tareas en ejecución y de tareas con dependencias
  pendientes o archivos solapados. No implementar promoción nueva: invocar solo operación
  completa ya admitida por WS12; si falta, preparar handoff y mostrar pendiente, no
  promoción terminada. Capa lista usa rutas normalizadas/expansión de files que documente
  contrato WS12 y ritual vigente: igualdad o contención directorio implican solapamiento;
  glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar
  lista, no heurística optimista.'
output_scope: frontends/mindmap/views/workspace/routing/; endpoints autorizados por
  el contrato WS12; tests/
depends_on:
- WS12
- WS22
- WS26.1
- WS48
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_CLOSEOUT:
  title: Contrato de evidencia de closeout estabilizado
  state: satisfied
  resolver: independent tester focalizado / recibo actual del contrato
  evidence: 59244c9 implementación, 1fefa97 cierre; tests/test_closeout_declared_evidence.py
    y tests/test_lifecycle_end_to_end.py prueban evidencia declarada y relación task→commit
    Task-Id exacta/parentage/commit-amend aislado. Recibo actual en run finalizar-plan-workspace.
    No autenticación/RBAC nuevo.
  verified_evidence: 'runs/subagents/20261031-finalizar-plan-workspace/tester-closeout-contract.md;
    tester-closeout-command.json; tester-closeout-pytest.log; tester-closeout-receipts.json:
    23 passed, 3 deselected, exit0, 2026-10-31; commit bd93985; impl 59244c9/cierre1fefa97'
G_HUMAN_READ:
  title: Persona aprueba recorrido de lectura
  state: pending
  resolver: WS16
  evidence: graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md;
    actor humano/versión/guion/resultado y soportes. Guardar en repo dueño, no en
    el paquete de plan deskops.
  produced_by: WS16
  evidence_ref:
    repo: graph_ui
    path: runs/subagents/workspace-documental-acceptance/lectura/acta.md
  effect: enable_ui_use_only; no bloquea desarrollo/pruebas aisladas de API; se exige
    antes de habilitar mutaciones en UI
G_PAYLOAD_PRECONDITION:
  title: Precondicion de escritura de payload verificada en sldb
  state: pending
  resolver: WS45
  produced_by: WS45
  evidence: 'Inventario con path/simbolo/commit y pruebas reales focalizadas en sldb
    de la precondicion de escritura de payload que fije el contrato WS12 (representacion,
    operaciones, escritores alcanzados): estado previo obsoleto rechazado sin cambios
    y vigente aplicado, rechazo observable por el llamante; commit/blob verificable
    en sldb. Independiente de source_mode y de G_SOURCE. El `expected` por valor existente
    (C-40) cuenta solo si WS12 lo adopta como contrato. Planificado: no hay evidencia
    de que exista ni este aceptado.'
G_UI_WRITE:
  title: Deltas de mutación aceptados en graph_ui
  state: pending
  resolver: 'external: solicitante P01 receptor del repo al preparar/promover el delta
    concreto'
  evidence: 'Acta de recepción por delta concreto en repo receptor: actor solicitante
    humano designado P01, fecha, alcance/IDs, efecto, task receptora/no solapamiento
    y commit/blob verificable. Cada nodo usa solo su recibo; ausencia de otro delta
    no bloquea este. Estado global pendiente resume recibos, no obliga aceptación
    conjunta. Productor del acta: receptor del repo dueño al preparar/promover ese
    delta, enlaza contrato WS12; Executor deskops solo registra el enlace, no escribe/commitea
    actas interrepo.'
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
  - WS48
  evaluation: per_delta
  accepted_scope_nodes: []
  contract_source: WS12
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
  - WS33
  - WS33.1
  - WS33.2
  - WS34
  - WS34.1
  - WS34.2
  - WS36
  - WS39
  - WS42
  - WS43
  - WS45
  - WS46
  - WS47
  - WS48

FILE:instruccion
Revisa el nodo WS26.1 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

