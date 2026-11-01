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
| WS19 e hijos / WS21 | IR/payload y hash/contexto reutilizables; ticket edición sigue draft | Guardado por campos/relaciones con precondición de escritura de payload (WS12 la define, WS45 la verifica o completa), 409/conflicto y guardas; raw-source depende WS20/G_SOURCE, sin relación con la precondición de campos |
| WS22 | deskops_routes.py lee Board/tarea/gates/next con rutas validadas | Lista/tablero/dependencias integrados al lector, mismas identidades y soporte; status no es test aprobado |
| WS23 | Lifecycle/payload navegables como documentos | Procedimiento/StepDoc/ritual con pasos/fuentes; no marcar realizado por leer |
| WS24 | Grafo entrante/saliente y hasta 2 hops; lector genérico IR/payload | Markdown no modelado, clasificación, backlinks y navegación completa; no esperar ViewDoc WS18 opcional |
| WS27 / WS27.1 | Code puede inspeccionar referencias seguras | Diff e historial Git reales acotados a tarea/repos; no son Code preview |
| WS27.2 | Task payload/gates de lifecycle | Mostrar evidencia declarada/encontrada/verificada y soporte diferenciado mediante contrato closeout público |
| WS28 | POST /api/desk/advance con revisión Board+task y lock de proceso; solo avanza lifecycle | Verify/handoff cierre externo y refresco verificable. advance no cierra; lock UI no coordina escritores CLI/agentes |
| WS29 | Problems del índice de aristas y hashes contexto | Changes sigue draft: check/doctor/drift e impacto real; no CST/Merkle Kimun |
| WS32 e hijos | Infraestructura closeout existente, candidato Scion ya capturado (WS32/33 conservan sus dependencias, incluida WS05, y sus gates) | Correlación intento/manifiesto/RunDoc e idempotencia con Scion real; no autorizados ni duplicados por este plan |

WS06 mantiene esta matriz al promover: integrar delta en ticket receptor vigente, vincular evidencia ya existente, o tarea atómica propia sin solapamiento. Nunca volver a implementar base porque el TaskDoc histórico ya no existe. Ningún nodo completo solo por commit: cada aceptación ampliada debe probarse. WS01/WS07 ya tienen contenido documental cubierto en brief/decisiones; verificar ese recibo al promover, no reescribirlo como nuevo trabajo.

Recepción: solicitante fue designado producto/aceptación graph_ui/sldb/spec2viz en ítem 2. Eso no es acta técnica. Receptor solicitante P01 registra acta por delta concreto con actor, alcance/IDs, fecha, efecto y commit/blob en su repo al preparar/promover ese delta. WS11/12 mapean esos requisitos en contratos y solo enlazan actas existentes; Executor deskops no escribe actas interrepo. G_UI_READ/G_UI_WRITE/G_SLDB_WRITE/G_SPEC_VIEW/G_WRITE_CONTRACT no exigen aceptar otros deltas. Lector/manual no esperan Changes, modelos, Scion ni spec2viz opcional.

Closeout: implementación 59244c9 y cierre 1fefa97 verificables, con Task-Id histórico; fuentes durables `deskops/services/closeout_gates.py`, `services/closure.py`, tests de evidencia declarada y lifecycle. Recibo `git show 1fefa97^:desk/tasks/task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo.md`. G_CLOSEOUT se decide con prueba focalizada actual y asociación task→commit exacta, nunca por desaparición. Autoría se refiere al registro de cierre según contrato existente, sin añadir una nueva capa de permisos. Baseline histórico reporta fallos ajenos de suite; esta tarea no arregla producto ni afirma suite global verde.

## Matriz de correspondencia WS06

Fecha: 2026-10-31. Traduce las auditorías WS02-WS04 (`auditoria/deskops.md`, `infraestructura.md`, `ui.md`, aprobadas como inventario documental en `runs/subagents/20261031-ws02-04-checkpoint/approval.md`) a capacidades y deltas por repo dueño. No es validación de runtime ni de UI: las filas se apoyan en código leído y en los límites que cada auditoría declara; no se ejecutó nada. Un commit prueba solo la base que cita, nunca el alcance ampliado de un nodo.

Lectura de la matriz.
- Una fila por capacidad o delta único. Varios nodos pueden remitir a la misma fila; los agregados (WS13, WS15, WS19, WS25, WS26, WS27, WS32, WS33, WS34) remiten por sus hijos.
- Clasificación: **ya cubierto** (capacidad observable en código, con path o símbolo y commit, sin afirmar alcance ampliado), **extender ticket** (cabe en un ticket existente, incluido un draft del Board), **nuevo delta** (no cabe; se propone atomizado) y **no adoptado** (solo `frontends/workspace/`, que se cita y no se adopta).
- El dueño de la fila es el repo donde vive el código a cambiar. Cuando difiere del `owner_repo` del nodo, la diferencia se dice en límites.
- Commit observado: el que cita la auditoría para esa fila. Si no cita uno, el HEAD auditado del repo, marcado como HEAD. Las rutas `../` son relativas a la raíz del repo deskops.
- Responsable: P01 designa al solicitante para graph_ui, sldb y spec2viz. Para deskops y para el ramal Scion la tabla de P01 no designa a nadie: «No designado en P01» es un dato de esa tabla, no un permiso nuevo que frene trabajo local autorizado por la persona usuaria. Ninguna fila registra un delta como recibido: el receptor P01 produce el acta externa en su repo al preparar cada delta, y WS11 y WS12 son fuente de contrato que solo enlaza esas actas. Esta matriz no produce firmas, gates, recepción ni permiso interrepo.
- Este documento no notifica, despacha ni modifica el Board de graph_ui. No se recrea el TaskDoc histórico de multiproyección (ver recibo arriba). Tres cosas distintas (glosario de brief.md): el before-image por valor existente `expected` con HTTP 409 (C-40), el token publicado `version`/`content_hash` (C-38) y la comparación o escritura pública con precondición compartida, aún no probada (C-41, con productor planificado WS45). La matriz no niega la capacidad optimista real ni infiere frescura por CLI.
- Serie en graph_ui: el ticket de edición (C-14) y el de Changes (C-28) comparten `frontends/mindmap/serve.py`, `frontends/mindmap/views/workspace/` y `docs/workspace-ui.md`. Se extienden uno tras otro; los deltas nuevos que escriben bajo `views/workspace/` tampoco se proponen en paralelo con ellos.


### graph_ui (`../UIs/graph_ui`, HEAD auditado `134a665`)

| ID | Capacidad o delta | Nodos DAG | Clasificación | Path o símbolo y commit observado | Ticket o delta destino | Responsable | Límites de evidencia |
|---|---|---|---|---|---|---|---|
| C-01 | Catálogo de documentos y lectura de nodo: identidad `Model:name`, IR/payload, contexto (relaciones entrantes, `content_hash`, `file_revision`) | WS13.1, WS13.2, WS23, WS24 | ya cubierto | `frontends/mindmap/workspace_routes.py`: `workspace_nodes`, `workspace_node`; `views/workspace/node/workspace-view.js` (`WorkspaceView`, panel Context). Commit a1b2b22 (integración f16fcd1; Board 134a665) | Ninguno (base reutilizable; los huecos están en C-07, C-08, C-09) | Solicitante (P01) | Solo documentos del store. No es lectura de Markdown no modelado ni de la fuente cruda. Comportamiento de runtime no ejecutado (auditoría ui.md lee código). No acredita el alcance ampliado de WS13.1, WS13.2, WS23 ni WS24 |
| C-02 | Vecindad de grafo entrante/saliente a 1–2 hops con filtro por tipo | WS13.1, WS24 | ya cubierto | `workspace_routes.py`: `_build_graph_neighborhood`; `workspace-view.js` (selector de profundidad); `workspace.mjs`: `filterGraphEdges`. Commit a1b2b22 | Ninguno | Solicitante (P01) | Sin backlinks calculados con la API de grafo de sldb (C-44), sin clasificación por tipo ni tags más allá de `context.metadata.tags`. No se ejecutó |
| C-03 | Proyección Code de referencias del documento con límites de repo, gitignore, binario y tamaño | WS13.1, WS27.1 | ya cubierto | `workspace_routes.py`: `_build_code_projection`, `_inspect_file_reference`. Commit a1b2b22 | Ninguno | Solicitante (P01) | Lee `files`/`references` del payload, no el archivo propio del documento. No es diff ni historial Git (ver C-24). No se ejecutó |
| C-04 | Alternancia Document/Graph/Code e historia de navegación por URL (`popstate`) | WS13.3 | ya cubierto | `workspace.mjs`: `TABS`; `workspace-view.js`: `updateUrl`, handler `popstate`. Commit a1b2b22 | Ninguno | Solicitante (P01) | Los `TABS` son proyecciones del mismo documento, no pestañas de documentos (C-09). Foco/historia al volver no ejecutados |
| C-05 | Filtro local del catálogo por id, título y modelo | WS13.2, WS14 | ya cubierto | `workspace.mjs`: `filterCatalog`; `workspace-view.js`: `loadCatalog` y buscador de catálogo. Commit a1b2b22 | Ninguno | Solicitante (P01) | Filtra lo ya cargado; no es búsqueda por texto/campos/semántica ni por API (C-10). El catálogo se carga al montar; el botón Actualizar recarga el nodo, no el catálogo |
| C-06 | Errores honestos de catálogo, nodo y proyección; problemas del índice de aristas y hashes de contexto; 503 «El store no está disponible» | WS15.1, WS15.2, WS29 | ya cubierto | `workspace-view.js` (`catalogError`, `nodeError`, errores por proyección); `workspace.mjs`: `formatProblems`; `workspace_routes.py`: `_check_problems_for_node` y 503 de `workspace_node`. Commit a1b2b22 | Ninguno (huecos en C-11, C-12, C-28) | Solicitante (P01) | Sin diagnóstico de CDN ni reintento que conserve foco; sin orientación de proyecto sin desk. `_check_problems_for_node` no sustituye `sldb stores check`, `deskops doctor` ni `deskops drift check`. No se ejecutó |
| C-07 | Fuente Markdown íntegra del documento (solo lectura) y foco compartido entre representaciones del mismo documento | WS13.1 | nuevo delta | Ausente en graph_ui: `_build_code_projection` no lee el archivo propio del documento (a1b2b22). Reutilizar `_inspect_file_reference` para la lectura segura | nuevo delta: lectura de fuente propia en el lector | Solicitante (P01) | Productor graph_ui, ruta de lectura que fija el contrato WS11. Markdown sin modelo se cubre en C-08. No requiere guardado (C-42 es otra fila) |
| C-08 | Explorador de documentos modelados y de Markdown no modelado del desk, con refresco explícito del catálogo | WS13.2 | nuevo delta | Ausente: el catálogo `workspace_nodes` lista solo documentos del store (a1b2b22); sin API de árbol de archivos del desk | nuevo delta: explorador de documentos y árbol del desk | Solicitante (P01) | El árbol de archivos no tiene operación existente en las auditorías; productor graph_ui, con resolución segura de rutas según WS11. No se inventa una API de sldb |
| C-09 | Pestañas de documentos, dos documentos lado a lado y foco por documento (disposición local, P07) | WS13.3 | nuevo delta | Ausente: `TABS` solo conmuta proyección (a1b2b22) | nuevo delta: pestañas y divisiones de documentos | Solicitante (P01) | Disposición como estado local, no documento compartido (P07). Comparte `views/workspace/` con C-14 y C-28: en serie |
| C-10 | Búsqueda del workspace por texto/campos sobre API pública real, con estados sin resultado, error y degradado distintos | WS14 | nuevo delta | Ausente: solo filtro local (C-05). Backend existente en sldb: C-43 | nuevo delta: búsqueda navegable sobre `sldb find` | Solicitante (P01) | Productor graph_ui (ruta/consumo); la capacidad base vive en sldb (C-43). Búsqueda semántica/ranking: `Corpus.rank` es un hueco sin CLI en sldb, no se promete. Sin prueba de peticiones |
| C-11 | Diagnóstico de fallo CDN, backend ausente, referencia rota y reintento que conserva foco/historia | WS15.1 | nuevo delta | Ausente: `index.html` de mindmap importa React desde `esm.sh` sin manejo observado (a1b2b22) | nuevo delta: errores de lectura y modo degradado | Solicitante (P01) | La detección de enlace roto puede apoyarse en C-45. No afirmar funcionamiento offline (alcance.md). Reintento no ejecutado |
| C-12 | Orientación de proyecto sin desk con ruta absoluta y comando `deskops init <ruta>`, con refresco tras init externo | WS15.2 | nuevo delta | Ausente: `grep` sin resultados en `views/workspace` ni `workspace_routes.py` (auditoría ui.md). Comando destino: C-62 | nuevo delta: orientación sin desk | Solicitante (P01) | Nunca inicializar por GET. El comando existe en deskops (C-62); lo nuevo es la pantalla |
| C-13 | Edición en el KB map: guardado con 409 por `expected` de payload, diálogo de conflicto y alta de relación (`ConnectDialog`) | WS19.1, WS19.2 | ya cubierto | `frontends/mindmap/persistence.py`: `save` (409 en líneas 85 y 102); `dialogs/conflict-dialog.js` (087e516); `views/documents/map/connect-dialog.js`: `ConnectDialog` (087e516, c63b9a3). Commits de `persistence.py` según ui.md (9825eb4 … c63b9a3) | Ninguno (base fuera del workspace) | Solicitante (P01) | Compara el payload completo, no un hash de revisión; no es el contrato WS12 (C-41). `ConnectDialog` solo agrega relaciones sobre campos de referencia; no hay baja ni verificación por contrato. No existe en la vista workspace. No se ejecutó |
| C-14 | Edición contextual de campos y relaciones con before-image y 409 dentro del workspace | WS19.1, WS19.2 | extender ticket | `desk/tasks/task-edicion-contextual-de-relaciones-y-campos-con-control-de-concurrencia.md` (draft en Board, sha256 ea6b71f2…, HEAD 134a665); sus `tests/test_mindmap_workspace_edit.py` no existen | Ticket `task-edicion-contextual-de-relaciones-y-campos-con-control-de-concurrencia` | Solicitante (P01) | Comparte `serve.py`, `views/workspace/` y `docs/workspace-ui.md` con C-28: se extienden en serie, sin ejecución paralela. Depende de C-41 (el ticket habla de before-image por valor, que existe como `expected`; la precondición compartida la trata C-41) y de los recibos del receptor P01 por delta. G_HUMAN_READ habilita solo el uso de mutaciones en UI |
| C-15 | Alternancia fuente/render con mismo origen y buffer sin guardar, según `source_mode` (P04) | WS21 | nuevo delta | Ausente: ningún ticket habla de `source_mode`; sin código de fuente editable en el workspace | nuevo delta: fuente y renderizado según `source_mode` | Solicitante (P01) | Bloqueado por G_SOURCE y C-42; sin raw-source no se prepara ni se promueve. Escribe bajo `views/workspace/`: en serie después de C-14 |
| C-16 | Lista y detalle de tareas del Board con gates y evidencia declarada (vista Deskops existente) | WS22, WS23, WS27.2 | ya cubierto | `frontends/mindmap/deskops_routes.py`: `GET /api/desk/board`, `GET /api/desk/task`; `views/workflow/deskops/deskops-view.js` (`filterTasks`, `counts`, sección «Evidencia declarada»). Commit daa6400 | Ninguno | Solicitante (P01) | Vive en la vista Deskops, no en el lector workspace. Solo evidencia declarada; sin encontrada/verificada (C-25). No se ejecutó |
| C-17 | Tablero agrupado por estado, dependencias navegables y apertura de TaskDoc/pills/átomos en el lector | WS22 | nuevo delta | Ausente (ui.md): hoy solo lista y detalle (C-16); lectura de datos vía C-51 | nuevo delta: Board como trabajo navegable | Solicitante (P01) | Sin drag-and-drop de status. Comparte `views/workspace/` con C-14 y C-28: en serie |
| C-18 | Renderer de RitualDoc/StepDoc/lifecycle como procedimiento con pasos y fuentes navegables | WS23 | nuevo delta | Ausente: solo íconos en `shared/classes.mjs` y gramática en `source/graph.mjs`; sin vista de procedimiento (ui.md) | nuevo delta: procedimiento de rituales y pasos | Solicitante (P01) | Lectura de datos: C-51. El store del desk tiene 0 documentos StepDoc (deskops.md, sección B): los pasos dependen del corpus. Transiciones solo representadas, no accionables |
| C-19 | Vista genérica de conocimiento (átomo, protoátomo, crossroad, materialización, pill), clasificación y backlinks | WS24 | nuevo delta | Ausente: Markdown no modelado y clasificación (ui.md). Base de grafo: C-02; datos: C-52, C-44 | nuevo delta: conocimiento y grafo local | Solicitante (P01) | No espera ViewDoc (C-37, C-48); la extensión es opcional y posterior a G_SPEC_VIEW |
| C-20 | Inbox en UI: leer mensajes, ack y respuesta local dentro del mismo desk | WS25.1 | nuevo delta | Ausente: `grep -i inbox` solo halla el ícono de `InboxNoteDoc` (ui.md). Operaciones existentes: C-53 | nuevo delta: inbox en workspace | Solicitante (P01) | Ruta HTTP hacia las operaciones de deskops (canal público: CLI/`DeskopsOperations`). Ack no es aprobación. Sin envío interdesk. Con otro coordinador escribiendo: lectura/handoff (P03) |
| C-21 | Captura interna en UI hacia candidato de drawer o protoátomo, con destino elegido | WS25.2 | nuevo delta | Ausente: `quick-create-dialog.js` (707ea86, 087e516) crea documentos de modelos capturables en el KB map, destino distinto, no comprobado. Operaciones: C-54, C-55 | nuevo delta: captura interna en UI | Solicitante (P01) | El nodo WS25.2 es de graph_ui, pero el canal de captura directa a drawer queda pendiente del contrato WS12 (C-55: API SLDB existente, composición o eventual wrapper Deskops, sin aprobar ninguno); cada destino se prueba por separado |
| C-22 | Autoría de tarea en UI: desde candidato, evidencia declarada, dependencias y binding de pills | WS26.1 | nuevo delta | Ausente: sin autoría de tareas desde UI (ui.md). Operaciones: C-56 | nuevo delta: autoría de tareas | Solicitante (P01) | Candidato = archivo del drawer. G_CLOSEOUT satisfecho en dag.yaml. La UI no escribe campos protegidos (status, current_node, history, closeout_evidence salvo declaración al crear) |
| C-23 | Enrutar en Board y mostrar capa lista (dependencias y no solapamiento) en UI | WS26.2 | nuevo delta | Ausente: sin enrutado desde UI (ui.md). Operación de ruta: C-57; datos de dependencias/archivos: C-51 | nuevo delta: enrutado y capa lista | Solicitante (P01) | No hay comando que calcule la capa lista en las auditorías; se propone derivarla en lectura desde `depends_on` y `files` de las tareas. Enrutar no es ejecutar |
| C-24 | Diff Git e historial de solo lectura por repo y tarea, junto al TaskDoc | WS27.1 | nuevo delta | Ausente en código versionado: la proyección Code (C-03) no es diff. C-29 tiene `_read_git_history` pero no se adopta | nuevo delta: diff Git por repo y tarea | Solicitante (P01) | Base en `TaskDoc.references` y `TaskDoc.files`. C-47 es historial por documento, no por tarea. Solo lectura |
| C-25 | Ruta de lectura que expone el informe de `closeout verify` (declarada, encontrada, gates, verificada) | WS27.2, WS28 | nuevo delta | Ausente: la vista Deskops muestra solo la evidencia declarada (C-16). Operación a exponer: C-58 | nuevo delta: informe de verificación de cierre | Solicitante (P01) | Verificada refiere al resultado del comando, no a inferencia en el renderer. G_CLOSEOUT satisfecho en dag.yaml |
| C-26 | Avance de lifecycle desde UI con revisión de Board y tarea (409 ante revisión obsoleta) y lock de proceso | WS28 | ya cubierto | `frontends/mindmap/deskops_routes.py`: `POST /api/desk/advance` que llama `advance_task`; `deskops-view.js` («El cierre se gestiona desde el CLI»). Commit daa6400 | Ninguno | Solicitante (P01) | `advance` no verifica ni cierra. El lock de la UI no coordina escritores CLI/agentes (P03). No es un canal de cierre |
| C-27 | Handoff de cierre: preparar y entregar a `deskops closeout commit` por CLI o al coordinador, sin commit ni cierre por HTTP | WS28 | nuevo delta | Ausente (ui.md). Destino del handoff: C-59 | nuevo delta: verificación y handoff de cierre | Solicitante (P01) | Handoff no equivale a cierre hecho (brief.md). Refresco verificable tras cierre externo no observado |
| C-28 | Changes e impacto comprobable: hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando | WS29 | extender ticket | `desk/tasks/task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento.md` (draft en Board, sha256 433ecb51…, HEAD 134a665); `tests/test_mindmap_changes.py` no existe. Base parcial: C-06 | Ticket `task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento` | Solicitante (P01) | Comparte `serve.py`, `views/workspace/` y `docs/workspace-ui.md` con C-14: en serie. Los tres comandos viven en C-46 y C-61; `doctor` y `drift check` amplían lo que nombra el ticket de Changes, que menciona `stores check` y el grafo; sin árbol CST/Merkle de Kimun (P02). Las pruebas usarían store temporal real |
| C-29 | `frontends/workspace/` (servidor paralelo de solo lectura, sin commit) | WS27.1, WS29 | no adoptado | Sin commit: `git ls-files frontends/workspace` devuelve 0 en 134a665; archivos sucios con sha256 en ui.md sección 4.2 | Ninguno; sin reclamo en Board ni TaskDoc | Sin reclamo (no se asigna) | Cliente incompleto: `index.html` referencia `/app.js` que no existe. Se cita lo observado (`_build_changes_projection`, `_read_git_history`) y no se adopta como base ni se reclama aquí |
| C-30 | Inspección y edición de modelos/clases en la vista Schema (`template_edit`, `fields_add`, `fields_remove`, `validate`, `promote`) | WS39 | ya cubierto | `frontends/mindmap/models_service.py` (e032a84, bf3dcb2, 90b409c, 3deed11, e107b48); `dialogs/class-dialog.js` (e032a84, 087e516); `views/models/diagram/`; rutas `POST /api/models/*` en `serve.py` | Ninguno | Solicitante (P01) | Capacidad existente en el KB map. No hay fila previa de WS39 en este documento. No se ejecutó |
| C-31 | Acceso a inspección/edición de modelos desde el panel Context del lector | WS39 | nuevo delta | Ausente: no hay acceso desde el panel Context de `WorkspaceView` (ui.md) | nuevo delta: modelos desde el contexto del documento | Solicitante (P01) | Usa draft/validate/promote de sldb ya expuestos; no reimplementa modelos. Escribe bajo `shell/dialogs.js` y `views/models/`; la parte del lector comparte `views/workspace/` (serie) |
| C-32 | Generador reproducible del corpus Taller con dos desks temporales, Markdown no modelado, Code local y referencia rota | WS40 | nuevo delta | Ausente: no existe `tests/fixtures/workspace_documental/` ni script de seed (ui.md). `frontends/mindmap/fixtures/kb-small.json` es otro fixture | nuevo delta: corpus Taller | Solicitante (P01) | Usa los CLI reales de deskops (C-62, C-56) y sldb. Las plantillas authored de WS17 son documentación (sin fila) |
| C-33 | Lectura segura entre desks con aliases/roots autorizados, sin tocar `SLDB_STORE` global | WS41 | nuevo delta | Ausente: `DeskRoutes` y `configured_routes` resuelven una sola raíz (`DESKOPS_ROOT` o el padre del store) (ui.md). Registro de repos: C-63 | nuevo delta: lectura entre desks | Solicitante (P01) | Solo lectura, sin mutaciones cruzadas (P07). Aliases y rutas los fija WS11 |
| C-34 | Operaciones de conocimiento en UI: split/merge de átomos y tipado de protoátomos con confirmación; materializaciones solo inspección | WS42 | nuevo delta | Ausente: `workspace_routes.py` no contiene operaciones de átomos (ui.md). Operaciones existentes: C-60 | nuevo delta: operaciones de conocimiento en UI | Solicitante (P01) | Whitelist de WS12; endpoints limitados a ella. Necesita C-41 o handoff mientras no exista canal con autoridad compartida (P03) |
| C-35 | Trazabilidad tarea-intento-conversación-resultados-decisión en el workspace | WS35 | nuevo delta | Ausente (ui.md). Adyacente sin comprobar: `shell/workers-panel.js` y `/api/workers` en `serve.py` | nuevo delta: ejecución y trazabilidad | Solicitante (P01) | Ramal E (opcional). Depende de C-64, C-65 y C-66; Scion no está auditado (WS05 pendiente) y no se afirma ninguna API Scion |
| C-36 | Delegación e intervención humanas en UI (dispatch/reply y decisión) | WS36 | nuevo delta | Ausente (ui.md) | nuevo delta: delegación en UI | Solicitante (P01) | Ramal E. Solo invoca los adaptadores C-67 y C-68; G_EXEC pendiente. El operador Scion se designa después |
| C-37 | ViewDoc en graph_ui: evaluador, rutas de evaluación/guardado y render (solo modo local) | WS18, WS24 | ya cubierto | `frontends/mindmap/projection_views.py`: `evaluate_view`, `list_views`, `find_view`; `views_routes.py`: `GET /api/views`, `/api/views/evaluate`, `POST /api/views/save`; `serve.py`: `_api_views`; `apps/review-workbench/src/features/graph-editor/` (render). Commits 0eb7dd7, b9ab83c, 2a15356 | Ninguno (base; reutilización primero) | Solicitante (P01) | Modo remote responde 501. `save_view` no pasa `expected`. Pruebas existentes (`tests/test_projection_views.py`, `tests/e2e_review_workbench_views.py`) no ejecutadas. El modelo vive en spec2viz (C-48). No acredita el alcance de WS18 ni de WS24 |

### sldb (`../sldb`, HEAD auditado `77bd6d0`)

| ID | Capacidad o delta | Nodos DAG | Clasificación | Path o símbolo y commit observado | Ticket o delta destino | Responsable | Límites de evidencia |
|---|---|---|---|---|---|---|---|
| C-38 | Lectura de documento: payload, IR y `version` (= `content_hash`) | WS13.1, WS19.1, WS24 | ya cubierto | `sldb/store/query.py`: `load_runtime_documents`; `sldb/api/documents/document_serialization.py` (`version`); rutas `GET /document`, `/document/ir`, `/document/segments` en `sldb/cli/serve/document_routes.py`. Commit: HEAD 77bd6d0 (la auditoría no cita otro) | Ninguno | Solicitante (P01) | La carga pasa por caché de runtime: una edición externa posterior al último barrido y que no altere los índices puede no verse hasta una nueva operación (deducción estática, no ejecutada). `/save` no lee `version` |
| C-39 | Escritura de payload con lock de store y `SAVE_LOCK` de proceso | WS19.1, WS19.2, WS21 | ya cubierto | `sldb/store/io/lock.py` (lock advisory por store); `sldb/cli/serve/save_routes.py`: `SAVE_LOCK`; `sldb/api/documents/payload_save.py`: `save_document_payload`. HEAD 77bd6d0 | Ninguno (límite de coordinación) | Solicitante (P01) | El lock cubre solo la actualización de índices; la escritura del Markdown ocurre antes y fuera de él. `SAVE_LOCK` no alcanza a otro proceso (CLI, otro `serve`). Confirma P03: lock solo de UI no basta. Por lectura, no ejecutado |
| C-40 | `expected` público por valor en `POST /save` (update/delete), con 409 | WS19.1, WS19.2, WS21 | ya cubierto | `sldb/cli/serve/save_plan.py:50,58`; `sldb/cli/serve/save_routes.py:38-43`. HEAD 77bd6d0 | Ninguno (capacidad con limitación; la precondición compartida se trata en C-41) | Solicitante (P01) | Compara el payload completo, no un hash ni una revisión; no acredita CAS compartido ni frescura para API o CLI (el payload viene de una carga sujeta a caché). La forma legacy `POST /save {doc,payload}` no verifica nada. Sin garantía entre procesos. No ejecutado |
| C-41 | Precondición de escritura de payload compartida por API, CLI y UI, con representación que fija WS12 (puede ser `expected` por valor, token `version`/`content_hash` u otra) | WS19.1, WS19.2, WS21, WS45 | nuevo delta | Existe: `expected` por valor (C-40) y `version`/`content_hash` publicado al leer (C-38). No probado: una comparación o escritura pública con precondición compartida. `save_document_payload`, `create_document`, `delete_document` y `sldb docs update` no reciben precondición; `grep` de `expected_hash`, `expected_revision`, `expected_sha`, `If-Match` y `etag` sin resultados (infraestructura.md sección 2.1) | nuevo delta: WS45 (sldb) verifica o completa la precondición de escritura de payload, independiente de `source_mode`: primero reutilizar, pruebas reales focalizadas, código solo si al ejecutarlo falta capacidad | Solicitante (P01) | WS12 define representación, precondición, operaciones y escritores alcanzados; no se fuerza CAS en toda CLI ni un algoritmo, y P03 no cambia. Un `grep` sin resultados no prueba ausencia de capacidad equivalente. WS20 conserva raw-source (C-42), que ya exige revisión y conflicto; el hueco de guardado por campos es separado y no depende del modo raw-source. Sin ticket sldb que lo contenga (tickets sldb abiertos: journal, bootstrap, jerarquía de evidencia, separación de store). Planificado: no implementado ni aceptado |
| C-42 | Guardado raw-source reversible con revisión, roundtrip, recuperación y campos protegidos | WS20, WS21 | nuevo delta | Ausente: `grep` de `raw_source` y `raw-source` en `sldb/src/sldb/api` sin resultados (infraestructura.md sección 1) | nuevo delta: guardado fuente reversible (WS20; verifica primero la capacidad existente) | Solicitante (P01) | Productor de G_SOURCE. Si WS20 halla capacidad parcial, solo se completa lo faltante. `create_document` sobre archivo existente lo sobrescribe antes de registrar (hueco: la captura a drawer, C-55, debe controlar colisiones). Recibo G_SLDB_WRITE antes de WS20 |
| C-43 | Búsqueda: `sldb find` (`--in`, `--type`, `--where`, `--regex`, `--fuzzy`), `fields query`, `sections find`, `GET /find` | WS14 | ya cubierto | `sldb/api/search.py:26`; `sldb/cli/commands/sections_find.py`; `GET /find` en `routes.py:86`. HEAD 77bd6d0 | Ninguno | Solicitante (P01) | Lectura exacta/regex/difusa, sin ranking por significado. `Corpus.rank` (`GET /corpus/rank`) es un hueco: sin CLI, 409 si no está indexado. No ejecutado |
| C-44 | Grafo y backlinks: `edges_from`, `edges_to`, `sldb graph neighborhood/query`, `GET /edges`, `GET /graph/*` | WS13.1, WS24 | ya cubierto | `sldb/store/edge_index/declared_references.py:38`; `sldb/api/graph/execute.py:13`; rutas `GET /graph/*`. HEAD 77bd6d0 | Ninguno | Solicitante (P01) | El lector de graph_ui hoy no los consume (ui.md no leyó esta auditoría). Sin consultas guardadas ni vistas de búsqueda en el store |
| C-45 | Enlaces `[[doc]]`, `[[doc#Sección]]`, predicados y auditoría de enlaces (`docs recover`, `GET /lint`) | WS13.1, WS15.1 | ya cubierto | `sldb/links/parser.py:6-7`; `sldb/links/audit.py:10`; `sldb/cli/serve/lint_routes.py:25,58`. HEAD 77bd6d0 | Ninguno | Solicitante (P01) | No ejecutado. Referencia rota en UI depende de C-11 |
| C-46 | `sldb stores check` (hallazgos de integridad del store, p. ej. «store_hash stale») | WS29 | ya cubierto | `sldb/cli/commands/store_check_report.py:35`; CLI `sldb stores check`. HEAD 77bd6d0 | Ninguno | Solicitante (P01) | deskops.md no comprobó si escribe caché o journal. No ejecutado |
| C-47 | Historia de versiones de un documento desde Git (`sldb docs history`) | WS27.1 | ya cubierto | `sldb/api/documents/document_history.py:23`. HEAD 77bd6d0 | Ninguno | Solicitante (P01) | Por documento, no por tarea ni por repo; fuera de Git devuelve vacío. No es el diff de WS27.1 |

### spec2viz (`../spec2viz`, HEAD auditado `10df4f0`)

| ID | Capacidad o delta | Nodos DAG | Clasificación | Path o símbolo y commit observado | Ticket o delta destino | Responsable | Límites de evidencia |
|---|---|---|---|---|---|---|---|
| C-48 | Modelo `ViewDoc` (nodos por `{model, where}`, relaciones, dirección, notación, layout) y su registro en el store | WS18, WS24 | ya cubierto | `spec2viz/sldb_models.py:348-431` (`ViewDoc`); registro `spec2viz/sldb_sync.py:33-41`; prueba `tests/test_view_doc.py` (no ejecutada). HEAD 10df4f0 | Ninguno | Solicitante (P01) | Es solo el modelo: ningún código de sldb, pron ni spec2viz lo evalúa ni lo renderiza, y el store de spec2viz tiene 0 documentos ViewDoc. El evaluador y las rutas están en graph_ui (C-37). El glosario de brief.md recoge esta división |
| C-49 | Notación y resolución de documentos con una `NotationDoc`: `notation view`, `resolve_documents`, `view_to_mermaid` | WS18 | ya cubierto | `spec2viz/notation_view.py:228-300` (`resolve_documents`); `spec2viz/renderers/view_mermaid.py:76` (`view_to_mermaid`); 8 notaciones builtin. HEAD 10df4f0 | Ninguno | Solicitante (P01) | `resolve_documents` no tiene CLI y recibe ids ya elegidos; `view_to_mermaid` solo acepta layout `graph` (lanes y grid lanzan `ValueError`). No ejecutado |
| C-50 | Autoría de ViewDoc y NotationDoc concretos (los que definan WS09/WS11) y su comprobación sobre stores reales | WS18 | nuevo delta | El ViewDoc ya se crea, evalúa y guarda en graph_ui: `frontends/mindmap/projection_views.py:107` (`evaluate_view(store, view)`), `views_routes.py:9-10,56-82` (store por petición, `POST /api/views/save`; ver C-37). ViewDoc es datos sin ruta de store. 0 documentos ViewDoc en el store de spec2viz (infraestructura.md sección 5.2). Reutilizar C-37 y C-49 para evaluar y dibujar | nuevo delta: ViewDoc y NotationDoc concretos y su comprobación sobre stores reales (WS18) | Solicitante (P01) | Delta de autoría y comprobación; no pide portabilidad genérica, ni servicio, CLI o runtime fuera de graph_ui, ni extraer o compartir el evaluador, ni evaluador nuevo. `tests/test_projection_views.py:151-156` usa dos stores (no ejecutado) y cambia filtros: no prueba el mismo payload completo. `save_view` escribe en `store.parent/sldb/views/` (carpeta del proyecto dueño del store): no prueba que `sldb/views/` pertenezca al repo sldb; con `output_base` spec2viz puede ser `spec2viz/sldb/views/`. Ruta y registro se confirman según contrato, sin cambiar de dueño por el prefijo. La selección mínima la fija WS09/WS11. G_SPEC_VIEW opcional, no bloquea WS24 ni el manual |

### deskops (este repo, HEAD auditado `215bf624`; la auditoría no cita otro commit por fila, salvo closeout 59244c9)

| ID | Capacidad o delta | Nodos DAG | Clasificación | Path o símbolo y commit observado | Ticket o delta destino | Responsable | Límites de evidencia |
|---|---|---|---|---|---|---|---|
| C-51 | Lectura de tareas, Board, artefactos y lifecycle: `list_tasks`, `show_task`, `next_action_report`, `list_artifacts`, `show_artifact` | WS22, WS23, WS26.1, WS26.2, WS27.2 | ya cubierto | `deskops/operations.py:301-312` (`list_tasks`), `:412-450` (`show_task`), `:350-351` (`next_action_report`), `:396-410` (`list_artifacts`), `:452-459` (`show_artifact`). HEAD 215bf624 | Ninguno | No designado en P01 | Todas de lectura (el constructor de `DeskopsOperations` escribe `.deskops.log`, ignorado por git). No ejecutadas. `StepDoc` tiene 0 documentos |
| C-52 | Lectura de conocimiento: `list/show atom/pill/materialization`, `atoms tree/validate`, `list_atoms` | WS24, WS42 | ya cubierto | `deskops/operations.py:468-475` (`list_atoms`, `validate_atoms`); `:452-459`; CLI `atoms list/show/validate/tree`. HEAD 215bf624 | Ninguno | No designado en P01 | `validate_atoms` llama `ensure_workspace` y puede crear andamiaje. 145 AtomDoc y 29 PillDoc en el índice local (derivado). No ejecutado |
| C-53 | Inbox: `message send/list/read/ack` | WS25.1 | ya cubierto | `deskops/cli/commands/message.py:145-198` (list, read, ack; escritura :181, tracking :183). HEAD 215bf624 | Ninguno | No designado en P01 | Ack reescribe la nota y re-trackea en el store; sin efecto Git. «Responder» localmente es `message send` al mismo desk: composición no probada. Interdesk fuera de WS25.1 |
| C-54 | Captura de protoátomo: `atoms proto` y `atoms type` | WS25.2 | ya cubierto | `deskops/cli/registry.py:1140-1160` (`atoms proto`, `atoms type`); servicio en `services/atoms.py`. HEAD 215bf624 | Ninguno | No designado en P01 | ProtoAtomDoc tiene 0 documentos en el índice local. No ejecutado |
| C-55 | Canal permitido de captura a drawer con origen preservado, sin tarea activa y con colisiones controladas | WS25.2 | nuevo delta | Primitivas existentes a citar: `sldb.api.documents.create_document` (`create_document(model, payload, path)`, `sldb/src/sldb/api/documents/create_document.py:22`) y `DrawerService` (`deskops/services/drawer.py:246-274`, candidato TaskDoc en `:261`). `promote inbox-to-drawer-task` parte de una nota de inbox y la borra (deskops.md A1); no hay comando Deskops especializado de captura directa, lo que no equivale a ausencia de primitiva pública | nuevo delta: contrato de captura directa a drawer (pendiente de WS12), sin crear API ni modelo por reflejo | No designado en P01 (dato de esa tabla, no un permiso que frene trabajo local) | Canal pendiente del contrato WS12, que compara API SLDB existente, composición y eventual wrapper Deskops; no se afirma canal UI completo. Por verificar: colisiones (`create_document` sobrescribe un archivo existente, mientras `promote` rechaza un destino existente), origen, lista blanca y fallo parcial. `message send` más `promote` no queda aprobado: la promoción borra la nota y `why` apunta a la ruta borrada (`drawer.py:265`), hay que probar tipos de origen y fallo parcial, y evita meter trabajo local en inbox. Un productor Deskops explícito solo si falta conducta de workflow, antes de WS25.2; si la composición cumple, se documenta prueba y contrato y no se inventa otro productor. Planificado: no implementado |
| C-56 | Autoría de tarea: `add task [--from-drawer]`, `edit task`, `bind pill`, `attach_drawer_source` | WS26.1 | ya cubierto | `deskops/operations.py:284-296` (`bind_pill_to_task`), `:344-345` (`create_task_bundle`), `:361-363` (`attach_drawer_source`); CLI `add task`, `edit task`, `bind pill`. HEAD 215bf624 | Ninguno | No designado en P01 | `add task` exige `closeout_evidence` declarado o inferido. Mutación de desk y store, sin efecto Git. No ejecutado |
| C-57 | Enrutado en Board: `add task` agrega la ruta; `edit board` sobre `tasks` | WS26.2 | ya cubierto | `deskops/services/tasks.py:80-96` (`create_task_bundle` agrega al Board en una `DocTransaction`); `deskops/operations.py:271-282` (`edit_artifact_field`). HEAD 215bf624 | Ninguno | No designado en P01 | Enrutar una tarea ya existente por `edit board` no se ejercitó en la auditoría (se deduce de `edit_artifact_field`). La capa lista no tiene comando (C-23) |
| C-58 | `deskops closeout verify` / `verify_task_closeout` (evidencia declarada, encontrada, gates, alertas) | WS27.2, WS28 | ya cubierto | `deskops/operations.py:602-723` (`verify_task_closeout`); `deskops/services/closeout_gates.py:23,120-230`. Commits 59244c9 (implementación) y 1fefa97 (cierre) | Ninguno | No designado en P01 | Lectura, exit 0/1, sin efecto Git de escritura. Prueba focalizada actual: G_CLOSEOUT en dag.yaml. No es suite global verde ni garantía de producto |
| C-59 | `deskops closeout commit` como destino del handoff | WS28 | ya cubierto | `deskops/services/closure.py:72-103,271-344,370-538`; `deskops/cli/commands/closeout.py:75-129`. HEAD 215bf624; contrato 59244c9/1fefa97 | Ninguno | No designado en P01 | Tiene efectos Git (add, rm, commit, amend) y borra la tarea: solo por CLI o coordinador (P05/P06), nunca desde HTTP |
| C-60 | Operaciones de átomos: `split_atom`, `merge_atom`, `reorganize_atoms`, `atoms split/merge` | WS42 | ya cubierto | `deskops/operations.py:503-525` (`split_atom`, `merge_atom`); `services/atoms.py:258-382`. HEAD 215bf624 | Ninguno | No designado en P01 | Mutación de desk y store, sin efecto Git. El guion de confirmación humana lo pone la UI (C-34). No ejecutado |
| C-61 | `deskops doctor` y `deskops drift check` | WS29 | ya cubierto | `deskops/cli/commands/doctor.py` (`DoctorCLI`, `mutates=True` en el registro; solo `--repair` escribe); CLI `drift check`. HEAD 215bf624 | Ninguno | No designado en P01 | No se comprobó si `sldb stores check`, que `doctor` invoca por subproceso, escribe caché o journal. No ejecutado |
| C-62 | `deskops init <ruta>` | WS15.2, WS40 | ya cubierto | `deskops/cli/commands/core.py:24-53` (`InitCLI`); `deskops/bootstrap.py:104-116`. HEAD 215bf624 | Ninguno | No designado en P01 | Muta desk, store y entorno global (`~/.sldb`, pip). La UI solo orienta; no lo invoca por GET |
| C-63 | Registro de repos: `repo register/whoami/remove`, `list repositories` | WS41 | ya cubierto | `deskops/cli/registry.py` (`repo ...`); 6 `RepositoryDoc` en `desk/registry/`. HEAD 215bf624 | Ninguno | No designado en P01 | Inventario derivable que WS43 preserva. No resuelve aliases de lectura multidesk en graph_ui (C-33) |
| C-64 | Identidad de intento, manifiesto canónico, RunDoc y cierre idempotentes (Scion RunDoc/cierre) | WS32.1, WS32.2 | nuevo delta | Candidato de drawer `desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md` (sha256 125b862b…). Base: `deskops/runtime/scion.py:355` (`record_scion_run`), `services/closure.py` (`close_from_run`). HEAD 215bf624 | nuevo delta: identidad de intento y cierre Scion, a partir del candidato del drawer `desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md` (descomposición WS32/WS32.1/WS32.2 ya registrada en dag.yaml) | No designado en P01; el operador Scion se designa al abordar el ramal E | El destino es un candidato diferido del drawer, no un ticket ni un draft del Board. WS06 puede clasificar y conservar esta descomposición sin ejecutar WS05; WS32 y WS33 conservan sus dependencias (incluida WS05) y sus gates canónicos (G_SCION, G_CLOSEOUT, G_WRITE_CONTRACT). No autorizado ni duplicado por este plan; la estabilización del closeout previa ya está en 59244c9/1fefa97. Sin dispatch ni red. El acta del receptor P01 y WS11/WS12 como fuente de contrato son las únicas vías de recepción; esta fila no añade firmas, gates ni recepción |
| C-65 | Vínculo de mensajes y resultados de Scion al intento, con deduplicación y procedencia | WS33.1 | nuevo delta | Ausente: `close_from_run` no actualiza RunDoc y no hay vínculo a conversaciones (candidato Scion citado en C-64) | nuevo delta: mensajes y resultados por intento | No designado en P01; el operador Scion se designa al abordar el ramal E | Clave de deduplicación Hub+proyecto+conversación+mensaje según dag.yaml. La API pública de Scion no está auditada (WS05 pendiente): no se afirma ningún endpoint ni campo. Ramal E |
| C-66 | Registro de decisión humana explícita (aprobar o pedir corrección) asociada al intento | WS33.2 | nuevo delta | Ausente: no hay recibo estructurado de aprobación humana en `RunDoc` (candidato Scion citado en C-64) | nuevo delta: decisión humana por intento | No designado en P01; el operador Scion se designa al abordar el ramal E | Actor identificado según el contrato WS12. Completado lo reporta Scion; validado y cerrado son estados de deskops que este delta no escribe. Ramal E |
| C-67 | Adaptador público restringido de despacho (dispatch) con confirmación, timeout y autoridad del coordinador | WS34.1 | nuevo delta | Ausente: `record_scion_run` solo registra, no despacha (candidato citado en C-64) | nuevo delta: dispatch autorizado | No designado en P01; el operador Scion se designa al abordar el ramal E | G_EXEC pendiente. Confirmación = respuesta de la API de Scion, aún no auditada. Esta matriz no autoriza ni envía nada |
| C-68 | Adaptador público restringido de respuesta (reply) vinculado al intento | WS34.2 | nuevo delta | Ausente (mismo respaldo que C-67) | nuevo delta: reply autorizado | No designado en P01; el operador Scion se designa al abordar el ramal E | G_EXEC pendiente; mismo límite de API Scion no auditada |

### Atomización propuesta

Propuesta de agrupación en tareas atómicas por repo receptor, sin crear tareas ni tocar Boards. Cada grupo se prepara y promueve con el recibo del receptor P01 correspondiente; ningún grupo existe aún como tarea.

- graph_ui, extender tickets existentes y en serie: primero C-14 (ticket de edición), después C-28 (ticket de Changes). Ninguno se duplica ni se reabre el TaskDoc histórico.
- graph_ui, lector (deltas de solo lectura sobre `views/workspace/`, en serie entre sí cuando tocan los mismos archivos): C-07, C-08, C-09, C-10, C-11, C-12; después C-17, C-18, C-19.
- graph_ui, escritura (después de C-14 y de los productores): C-15 (tras C-42), C-20, C-21, C-22, C-23, C-25, C-27, C-34.
- graph_ui, independientes del lector: C-24, C-31, C-32, C-33; ramal E: C-35, C-36.
- sldb: C-41 (WS45, precondición de escritura de payload, independiente de `source_mode`) y C-42 (WS20, raw-source) como tareas separadas, cada una con su recibo; el resto de sldb es base ya cubierta.
- spec2viz: C-50 (WS18), autoría de ViewDoc y NotationDoc concretos reutilizando C-37 y C-49; sin evaluador nuevo ni extracción del existente.
- deskops: C-55 (canal de captura a drawer, pendiente del contrato WS12; productor Deskops solo si falta conducta de workflow); ramal Scion: C-64 (candidato del drawer, ya descompuesto en WS32), luego C-65 y C-66, luego C-67 y C-68, solo al abordar el ramal E.


### Cobertura de los 64 nodos de dag.yaml

| Nodo | Fila C-nn o motivo sin delta | Tipo de nodo |
|---|---|---|
| WS01 | sin delta: planificación; brief y glosario ya authored (covered_work) | delivery |
| WS02 | sin delta: auditoría documental entregada (inventario de superficies deskops) | delivery |
| WS03 | sin delta: auditoría documental entregada (inventario de infraestructura) | delivery |
| WS04 | sin delta: auditoría documental entregada (inventario de UI) | delivery |
| WS05 | sin delta: inventario Scion pendiente; WS06 clasifica sin ejecutarlo y WS32/WS33 lo conservan como dependencia | delivery |
| WS06 | sin delta: esta matriz | delivery |
| WS07 | sin delta: registro de decisiones (decisiones.md) | delivery |
| WS08 | sin delta: planificación de user-flows (borrador) | delivery |
| WS09 | sin delta: planificación del catálogo de renderizaciones (borrador) | delivery |
| WS10 | sin delta: planificación del índice del manual (borrador) | delivery |
| WS11 | sin delta: contrato documental de navegación; consume las filas de lectura y clasifica sus huecos | delivery |
| WS12 | sin delta: contrato documental de operaciones; consume las filas de escritura y asigna sus huecos | delivery |
| WS13 | agregado, por sus hijos WS13.1, WS13.2, WS13.3: C-01, C-02, C-03, C-04, C-05, C-07, C-08, C-09, C-38, C-44, C-45 | aggregate |
| WS13.1 | C-01, C-02, C-03, C-07, C-38, C-44, C-45 | delivery |
| WS13.2 | C-01, C-05, C-08 | delivery |
| WS13.3 | C-04, C-09 | delivery |
| WS14 | C-05, C-10, C-43 | delivery |
| WS15 | agregado, por sus hijos WS15.1, WS15.2: C-06, C-11, C-12, C-45, C-62 | aggregate |
| WS15.1 | C-06, C-11, C-45 | delivery |
| WS15.2 | C-06, C-12, C-62 | delivery |
| WS16 | sin delta: validación humana (acta en graph_ui) | delivery |
| WS17 | sin delta: documentación: plantillas authored del desk ejemplo | delivery |
| WS18 | C-37, C-48, C-49, C-50 | delivery |
| WS19 | agregado, por sus hijos WS19.1, WS19.2: C-13, C-14, C-38, C-39, C-40, C-41 | aggregate |
| WS19.1 | C-13, C-14, C-38, C-39, C-40, C-41 | delivery |
| WS19.2 | C-13, C-14, C-39, C-40, C-41 | delivery |
| WS20 | C-42 | delivery |
| WS21 | C-15, C-39, C-40, C-41, C-42 | delivery |
| WS22 | C-16, C-17, C-51 | delivery |
| WS23 | C-01, C-16, C-18, C-51 | delivery |
| WS24 | C-01, C-02, C-19, C-37, C-38, C-44, C-48, C-52 | delivery |
| WS25 | agregado, por sus hijos WS25.1, WS25.2: C-20, C-21, C-53, C-54, C-55 | aggregate |
| WS25.1 | C-20, C-53 | delivery |
| WS25.2 | C-21, C-54, C-55 | delivery |
| WS26 | agregado, por sus hijos WS26.1, WS26.2: C-22, C-23, C-51, C-56, C-57 | aggregate |
| WS26.1 | C-22, C-51, C-56 | delivery |
| WS26.2 | C-23, C-51, C-57 | delivery |
| WS27 | agregado, por sus hijos WS27.1, WS27.2: C-03, C-16, C-24, C-25, C-29, C-47, C-51, C-58 | aggregate |
| WS27.1 | C-03, C-24, C-29, C-47 | delivery |
| WS27.2 | C-16, C-25, C-51, C-58 | delivery |
| WS28 | C-25, C-26, C-27, C-58, C-59 | delivery |
| WS29 | C-06, C-28, C-29, C-46, C-61 | delivery |
| WS30 | sin delta: validación humana (acta en graph_ui) | delivery |
| WS31 | sin delta: documentación del manual básico | delivery |
| WS32 | agregado, por sus hijos WS32.1, WS32.2: C-64 | aggregate |
| WS32.1 | C-64 | delivery |
| WS32.2 | C-64 | delivery |
| WS33 | agregado, por sus hijos WS33.1, WS33.2: C-65, C-66 | aggregate |
| WS33.1 | C-65 | delivery |
| WS33.2 | C-66 | delivery |
| WS34 | agregado, por sus hijos WS34.1, WS34.2: C-67, C-68 | aggregate |
| WS34.1 | C-67 | delivery |
| WS34.2 | C-68 | delivery |
| WS35 | C-35 | delivery |
| WS36 | C-36 | delivery |
| WS37 | sin delta: validación humana con agente real | delivery |
| WS38 | sin delta: documentación del manual de delegación | delivery |
| WS39 | C-30, C-31 | delivery |
| WS40 | C-32, C-62 | delivery |
| WS41 | C-33, C-63 | delivery |
| WS42 | C-34, C-52, C-60 | delivery |
| WS43 | sin delta: documentación y publicación con operaciones existentes; preserva el registro (C-63) | delivery |
| WS44 | sin delta: validación: probe read-only de Scion | delivery |
| WS45 | C-41 | delivery |

FILE:desk/drawer/plans/workspace-documental/dag.yaml#external_reference:workspace
workspace:
  path: ../UIs/graph_ui/frontends/mindmap/workspace_routes.py
  exists: true
  sha256: dfbf68a70f3f1394119bc9cbcdbffe9ac9237397a5fa07788152146a697f39c9
  interpretation: observed_source_not_gate_acceptance
  historical_receipt: git -C ../UIs/graph_ui show f16fcd1^:desk/tasks/task-workspace-multiproyeccion-documento-grafo-local-codigo-y-contexto.md;
    impl a1b2b22; cierre f16fcd1; Board 134a665

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS13
id: WS13
title: Integrar lector workspace con historia y foco
status: candidate
kind: implementation
depends_on:
- WS11
- WS13.1
- WS13.2
- WS13.3
requires:
- G_UI_READ
owner_repo: graph_ui
output_scope: 'Agregado: salidas de WS13.1, WS13.2, WS13.3'
scope: 'Implementación o delta conciliado sobre workspace integrado a1b2b22: documento/fuente
  solo lectura, contexto, enlaces, tabs/historia y selección por documento/nodo. Mantener
  Code local y rutas del host; no requerir índices nuevos. Incluir explorador de documentos
  modelados/no modelados, dos documentos lado a lado y tabs/historia. Se reutiliza
  el registro de vistas existente en shell/registry.js; organización de contenido
  procede de documentos/consultas.'
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws13.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
overlap_with: workspace
integration_mode: delta_or_existing_ticket; matriz WS06 llega de forma transitiva
  por WS11/WS12; never_parallel_duplicate
output_base: graph_ui:repository_root/
node_role: aggregate
children:
- WS13.1
- WS13.2
- WS13.3
reconciliation: 'reconciliacion.md: base a1b2b22/f16fcd1/134a665 reutilizable; acceptance
  de este nodo/delta pendiente, no duplicar implementación ni inferir cierre por commit'

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS11
id: WS11
title: Cerrar contrato de navegación e identidad
kind: planning
owner_repo: deskops
node_role: delivery
scope: Un documento Markdown mantiene identidad/ruta/modelo opcional; graph/code admiten
  otros nodos con origen. Resolución repo/store explícita, foco, enlaces/historia
  y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos. Instancia
  = documento concreto que falta escribir. Vínculo = referencia o enlace que falta
  entre documentos existentes.
acceptance: Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales
  citadas por auditorías WS02–04 (path/símbolo/commit y evidencia existente); cada
  hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño antes
  de code. Mapear recepción requerida por delta en graph_ui (actor P01, IDs y efectos);
  enlazar acta externa solo si el receptor ya la registró. El contrato básico puede
  cerrar sin recepción de Changes, Scion ni ViewDoc opcional; cada delta sigue bloqueado
  hasta su propio recibo. G_SPEC_VIEW se obtiene separadamente al preparar WS18, sin
  bloquear navegación base. WS11 cierra con contrato básico revisado, clasificación
  de huecos y mapa de deltas que requieren recepción; puede cerrar sin acta receptora.
  Recibos son producidos por solicitante P01/repo receptor al preparar cada delta,
  no por Executor de WS11 ni por escritura interrepo. Cada delta espera su propio
  recibo; contrato básico no afirma que ninguno se haya recibido.
output_scope: contratos/navegacion.md; enlaces a recibos externos G_UI_READ por delta,
  G_SPEC_VIEW opcional
depends_on:
- WS09
- WS08
requires:
- G_PRODUCT

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
  integrado a1b2b22, según contrato WS11 y recibo externo del delta. Foco = elemento/nodo
  seleccionado dentro del documento; documento activo identifica pestaña. Compartir
  foco solo donde exista correspondencia real de origen definida WS11; no inventar
  mapeo texto→código.
acceptance: 'Markdown sin modelo tiene render de lectura y fuente cruda íntegra legibles
  (ambas), con mismo origen; el panel de contexto muestra identidad, las relaciones
  que declare el contrato WS11 y la ruta de origen reales; seguir un enlace y alternar
  entre texto/graph/code, en las representaciones que el catálogo WS09 (borradores/vistas.md)
  y el contrato WS11 declaren soportadas, preserva origen. La selección por documento/nodo
  fija el foco del documento abierto: seleccionar en Code, texto o graph actualiza
  ese foco y las demás representaciones del mismo documento lo comparten, sin abrir
  otra copia. No depender de conocer un ID; no crear otro workspace independiente.  La
  base a1b2b22 es punto de partida reutilizable; el cierre de este delta exige SU
  evidencia de aceptación ampliada Markdown no modelado/fuente, enlaces y foco. Ni
  cierre f16fcd1 ni commit previo sustituyen esa evidencia. Una copia es instancia
  documental con mismo origen, no cada representación.'
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS14
id: WS14
title: Integrar búsqueda navegable del workspace
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: 'Texto/campos/semántica solo según API real; resultados abren el documento
  con su identidad y ruta de origen. Estados diferenciados: búsqueda sin resultados,
  error y degradación.'
acceptance: 'Usar `sldb find` o su ruta en `sldb serve`, según auditoria/infraestructura.md
  (producido por WS03) y contrato WS11; no parser propio. Con teclado: buscar, abrir
  un resultado y volver conserva consulta y foco. Sin resultados; error de backend
  (la API no responde o falla y la UI lo declara sin mostrar vacío); y búsqueda degradada
  (la API responde con capacidad parcial, p. ej. sin semántica, y la UI declara qué
  no cubre) se ven como tres estados distintos; no cargar todo grafo en cada tecla.
  Comprobar en prueba de peticiones que teclear no dispara petición de carga completa
  del grafo; no exige debounce/umbral nuevo, mecanismo se fija en TaskDoc.'
output_scope: frontends/mindmap/source/; views/workspace/; tests/
depends_on:
- WS13
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS15
id: WS15
title: Mostrar errores de lectura y modo degradado
kind: implementation
owner_repo: graph_ui
node_role: aggregate
children:
- WS15.1
- WS15.2
scope: 'Agregado: errores de lectura (WS15.1) y orientación sin desk (WS15.2).'
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS15.1, WS15.2'
depends_on:
- WS13
- WS15.1
- WS15.2
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS15.1
id: WS15.1
title: Mostrar errores de lectura y modo degradado
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS15
scope: Referencia rota, documento ausente, modelo no importable y backend caído se
  muestran en panel afectado sin borrar historial ni fingir vacío. Fuente sin permiso/capacidad
  de edición es límite read-only visible, no fallo de lectura. Fallos CDN se declaran
  límite actual sin prometer offline.
acceptance: Reutilizar lectura Markdown de WS13.1 donde siga disponible; no implementar
  otro lector ni guardado. Contrato WS11 define errores de API y estados de red sin
  respuesta, incluido fallo de carga CDN; pruebas distinguen ambos sin inventar respuesta
  del backend ausente. Reintentar backend tras restaurarlo recupera lectura conservando
  pestañas/foco/historia; fallo CDN tiene diagnóstico visible y prueba de no carga,
  sin exigir recuperación offline. Empaquetado offline fuera.
output_scope: frontends/mindmap/views/workspace/errors/; rutas de lectura definidas
  por el contrato WS11; tests/
depends_on:
- WS13
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS15.2
id: WS15.2
title: Orientar proyecto sin desk
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS15
scope: 'UF10: un proyecto sin desk muestra orientación, la ruta absoluta del proyecto
  como destino y el comando `deskops init <ruta>`; nunca inicializar por GET. Tras
  init externo real, refrescar lectura.'
acceptance: Abrir un proyecto sin desk muestra orientación y destino sin mutar nada;
  tras ejecutar init fuera de la UI, refrescar muestra el desk real.
output_scope: frontends/mindmap/views/workspace/orientation/; rutas de lectura definidas
  por el contrato WS11; tests/
depends_on:
- WS13
requires:
- G_UI_READ

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS23
id: WS23
title: Renderizar rituales y pasos como procedimiento
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: RitualDoc/StepDoc/lifecycle sobre referencias reales; pasos y fuentes navegables;
  transiciones solo representadas, no accionables. Pruebas sobre corpus WS40 o store
  temporal real.
acceptance: Un procedimiento abre sus documentos y soporte; no auto-marcar pasos como
  realizados por leerlos. Mostrar progreso/estado de paso solo si WS02/WS09/WS11 identifican
  campo/API real de deskops que lo produce; si no, pasos authored son inertes y no
  hay progreso inventado. La vista no escribe estado. Las transiciones muestran origen/destino/condición
  declarados del lifecycle, sin controles que invoquen avance ni mutaciones; prueba
  de no peticiones de escritura.
output_scope: frontends/mindmap/views/workspace/procedure/; tests/
depends_on:
- WS13
- WS09
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS24
id: WS24
title: Integrar conocimiento y grafo local
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Reutilizar el gráfico actual y una vista de documento genérica única registrada
  en shell/registry.js para átomos/protoátomos/crossroads (inventariados en WS02 y
  catalogados en WS09)/materializaciones (MaterializationContractDoc; modelo en deskops/models/materialization.py)/pills,
  clasificación y vecindad; preservar Code local existente del workspace integrado
  a1b2b22. Backlinks = relaciones entrantes calculadas por la API de grafo de sldb
  según auditoria/infraestructura.md (producido por WS03). Clasificación = tipo del
  modelo y tags del documento cuando el modelo los declare. Vecindad = hasta 2 hops.
  Code local = proyección Code del workspace integrado a1b2b22. La vecindad existente
  se reutiliza sin esperar WS18. ViewDoc de WS18 es extensión opcional y solo se conecta
  tras recepción G_SPEC_VIEW, sin bloquear navegación básica ni manual. Tags se leen
  del payload/semantic_tags públicos del documento según inventario WS03 y contrato
  WS11, sin inferirlos por carpeta. Markdown no modelado se hereda del lector WS13.1/explorador
  WS13.2 (vía WS13), no segundo lector.
acceptance: Navegación ida/vuelta por fuentes y backlinks derivados; un soporte no
  modelado (Markdown sin modelo) es visible y navegable en la vista de documento genérica
  con su ruta de origen. La vista muestra la clasificación (tipo y tags) y la vecindad
  de hasta 2 hops. No un renderer nuevo obligatorio por cada clase. Markdown no modelado
  se identifica sin modelo y sin tags declarados; no inferir clasificación ficticia.
output_scope: frontends/mindmap/views/workspace/graph/ y node/workspace-view.js (panel
  Context existente); shell/registry.js; tests/
depends_on:
- WS13
- WS09
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS27
id: WS27
title: Integrar revisión de cambios y evidencia
kind: implementation
owner_repo: graph_ui
node_role: aggregate
children:
- WS27.1
- WS27.2
scope: 'Agregado: diff (WS27.1) y evidencia (WS27.2).'
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS27.1, WS27.2'
depends_on:
- WS13
- WS12
- WS27.1
- WS27.2
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS27.1
id: WS27.1
title: Mostrar diff Git por repo y tarea
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS27
scope: 'Diff Git e historial read-only junto a la TaskDoc. Base: commits listados
  en TaskDoc.references y rutas en TaskDoc.files (campos del modelo TaskDoc de deskops);
  sin commits, working tree contra HEAD limitado a esas rutas. Historial baseline
  = commits de TaskDoc.references resolubles y ordenados por fecha de commit, limitados
  a TaskDoc.files; sin commits se declara que no hay historial referenciado y se usa
  diff working tree→HEAD. Repo/rutas se resuelven por contrato WS11 con registry/aliases,
  presentando root repo explícito; ruta sin repo resoluble queda no disponible, no
  adivinar ni escribir cruzado.'
acceptance: Diff real e historial read-only acotados al repo y tarea (la asociación
  a intento se añade en WS35), sin escribir ni revertir nada; la vista no muestra
  hallazgos de integridad del store, que son de WS29. Se muestra una sección por cada
  repo alcanzado por TaskDoc.files, con el repo declarado.
output_scope: frontends/mindmap/views/workspace/diff/; rutas de lectura definidas
  por el contrato WS11; tests/
depends_on:
- WS13
- WS12
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS27.2
id: WS27.2
title: Mostrar evidencia declarada, encontrada y verificada
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS27
scope: Evidencia junto a la TaskDoc. Sin modelo de comentarios nuevo. WS12 fija correspondencia
  por tipo de evidencia declarada TaskDoc (no inferencia por extensión en renderer),
  artefactos soporte y salida pública de closeout verify; declarada/encontrada/gates/summary
  se muestran según reporte real. Verificada refiere al resultado del gate de la TaskDoc/tipo,
  no prueba independiente del artefacto. Reporte ausente/fallo de comando es no verificable
  con error, nunca verificado.
acceptance: Mostrar declarada/encontrada/verificada y abrir su soporte; una evidencia
  ausente se ve como ausente; declarada sin artefacto, artefacto no declarado y verificación
  fallida se muestran como estados distintos, sin colapsarlos. Declarada = closeout_evidence
  de la TaskDoc; encontrada = artefactos resolubles en las references/files de la
  TaskDoc; verificada = resultado de `deskops closeout verify`. Abrir soporte = abrir
  el artefacto en el lector si es Markdown dentro del workspace; fuera de ese caso
  se muestra la ruta y se declara no soportado (alcance.md).
output_scope: frontends/mindmap/views/workspace/evidence/; rutas de lectura definidas
  por el contrato WS11; tests/
depends_on:
- WS13
- WS12
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS39
id: WS39
title: Integrar inspección y edición de modelos existente
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Hacer navegables Schema/editar clases ya disponibles desde documento/contexto;
  usar draft/validate/promote de sldb. No reimplementar modelos. G_HUMAN_READ habilita
  uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con
  sus contratos/gates técnicos sin acta humana de lectura. Contexto = panel lateral
  Context del lector WS13 (node/workspace-view.js); acceso desde documento activo
  muestra Schema/clase origen de ese documento y abre editor existente inventariado
  WS04. Probar ese punto de entrada además de mutación UF09; ruta/selector exacto
  se fija en TaskDoc. WS13 aporta el lector requerido para integración, G_HUMAN_READ
  solo habilita uso de mutaciones.
acceptance: UF09 inspección y mutación en store temporal real de prueba; comprobar
  los efectos y errores que declara el contrato WS12; no habilitar promover si API/autoridad
  falta. Extensión posterior al lector básico. Guardar acta de prueba humana en graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md
  con el participante que fija P08 y resultado; G_HUMAN_MODEL debe pasar antes de
  marcar disponible en el manual que publica WS31 el capítulo 15 (Personalizar modelos)
  del índice de borradores/manual.md.
output_scope: shell/dialogs.js; views/models/; tests/; runs/subagents/workspace-documental-acceptance/modelos/
depends_on:
- WS12
- WS13
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

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

FILE:instruccion
Revisa el nodo WS13 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

