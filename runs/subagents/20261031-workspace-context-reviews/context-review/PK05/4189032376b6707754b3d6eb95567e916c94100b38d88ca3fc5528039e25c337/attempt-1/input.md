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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:PK05
id: PK05
title: Autoría y operación manual
scope: 'Autoría manual segura, intake/trabajo y revisión/cierre por handoff verificables.
  Agrupación de entregables sin ejecución propia; dry-run hipotético describe orden/aristas
  y transferencia entre hijos: WS12 contrato por delta alimenta WS19 campos, WS20
  API fuente/G_SOURCE, WS45 precondición de payload/G_PAYLOAD_PRECONDITION y WS21
  fuente/render; WS25 captura, WS26 tareas, WS27 diff/evidencia, WS28 handoff y WS42
  conocimiento; WS30 integra pruebas humanas con entradas WS17. Orden parcial obligatorio
  de ejecución hipotética (no simultaneidad de toda la lista): WS12→WS19 y sus hijos;
  WS12→WS20; WS12→WS45→G_PAYLOAD_PRECONDITION→WS19 y sus hijos y WS21 (la arista WS12
  y el gate se suman: el guardado espera ambos); WS12→WS25 y sus hijos; WS13+WS12→WS27
  y sus hijos; WS19+WS20/G_SOURCE→WS21 editable; WS22+WS12→WS26 y sus hijos (WS26.1→WS26.2);
  WS19+WS24+WS12→WS42; WS27+WS12→WS28; todas las salidas WS17/21/22/23/24/25/26/28/42→WS30.
  Solo ejecutar en paralelo nodos ya ready con todos sus prerrequisitos satisfechos
  y sin solapamiento de archivos; WS42 NO va en paralelo con su productor WS19, WS26
  NO precede WS22.'
acceptance: precondición de escritura/conflicto/buffer/protegidos probados; guardar
  sin commit; coordinador escritor implica read-only/handoff; mostrar evidencia declarada/encontrada/verificada
  distinta; cierre confirmado por commit/Deskops. Acta WS30 cubre UF02–05 y navegación;
  uso UI espera G_HUMAN_READ, desarrollo API aislado no. Completitud sustantiva del
  paquete requiere salidas de sus hijos e integración indicada; revisiones de comprensión
  no equivalen a producto entregado. Describir validaciones futuras sin ejecutarlas;
  agrupación no autoriza tareas ni añade aristas. Para revisar este macroencargo,
  dry-run debe describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora.
children:
- WS19
- WS20
- WS21
- WS45
- WS25
- WS26
- WS27
- WS28
- WS30
- WS42
review_completion:
  protocol: ritual-context-review
  state_field: context_review
  meaning: Gate de comprensión solamente; no define resultado ni completitud sustantiva
    del paquete.
owner_repo: deskops

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
  precondición de escritura (WS45/WS12) y conflicto visible; workflow-protected fields
  no editables por este canal. Incluir alta/baja de relaciones permitidas por contrato,
  usando API real y la precondición de escritura que fije WS12; no crear semántica
  de relaciones en componente. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo
  y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta
  humana de lectura.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS19.1, WS19.2'
depends_on:
- WS12
- WS19.1
- WS19.2
requires:
- G_HUMAN_READ
- G_PAYLOAD_PRECONDITION
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
  Markdown desde browser. Conserva solo raw-source, y la precondición de escritura
  de payload por campos es un hueco separado, producido por WS45 e independiente de
  source_mode. Las pruebas de conflicto de WS20 usan la precondición de guardado raw-source
  que fije WS12 y no esperan a WS45.
acceptance: Reversible = guardar y volver a extraer conserva campos y secciones sin
  pérdida. En ambas ramas G_SOURCE exige API pública y tests de roundtrip, conflicto,
  recuperación tras fallo y campos protegidos. Si la capacidad existe, esos tests
  bastan y no se duplica código. Si falta, se implementa en sldb mediante tarea propia
  aceptada en G_SLDB_WRITE. WS20 se convierte en esa tarea propia en sldb al promoverse
  (mismo delta/recibo G_SLDB_WRITE), no crea un segundo productor. Capacidad existente
  significa que satisface todos los requisitos de esta aceptación/G_SOURCE; parcial
  se completa solo en lo faltante y se vuelve a probar todo el contrato.
output_scope: src/sldb/api/documents/; src/sldb/cli/serve/; tests/
depends_on:
- WS12
requires:
- G_SLDB_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS21
id: WS21
title: Integrar fuente y renderizado según source_mode
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Alternar fuente/render con mismo origen, revisión y dirty buffer; usar guardado
  fuente autorizado. Composición escribe solo origen trazable soportado. Ejecutar
  solo la variante elegida por P04; Con pending no se prepara ni se promueve este
  nodo. Al alternar con cambios sin guardar se conserva el buffer; nunca se descarta
  sin confirmación explícita de la persona usuaria; si no confirma, el buffer se conserva.
  No requiere G_SOURCE si el humano eligió fuente read_only; el guardado por campos
  exige G_PAYLOAD_PRECONDITION en ambas variantes.
acceptance: Cumplir la aceptación específica de la variante P04. En editable, G_SOURCE
  y G_WRITE_CONTRACT pasan y se prueba edición/conflicto/roundtrip. En read_only,
  fuente legible no editable y edición por campos probada; manual/WS30 no declaran
  edición fuente disponible. En ambos modos una composición, si existe en el contrato
  WS12, escribe solo en el documento dueño de cada campo; si no hay soporte, queda
  de solo lectura y se declara.
output_scope: frontends/mindmap/views/workspace/; tests/
depends_on:
- WS19
requires:
- G_PAYLOAD_PRECONDITION
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS45
id: WS45
title: Verificar o completar la precondición de escritura de payload
kind: implementation
owner_repo: sldb
node_role: delivery
scope: Productor planificado, independiente de source_mode y de raw-source (WS20 conserva
  raw-source). Distingue tres cosas, sin negar la capacidad optimista real ni inferir
  frescura por CLI; before-image por valor existente (`expected`, HTTP 409, C-40),
  token publicado (`version`/`content_hash`, C-38) y comparación o escritura pública
  con precondición compartida, aún no probada. Primero reutilizar; inventario con
  path, símbolo y commit de la capacidad existente en sldb frente al contrato WS12
  (representación de la precondición, operaciones y escritores alcanzados); luego
  pruebas reales focalizadas; código solo si al ejecutar falta capacidad, con tarea
  propia en sldb. No fuerza CAS en toda CLI ni elige un algoritmo de hash por inercia,
  y no mezcla UI ni productor condicional alguno. P03 no cambia.
acceptance: Inventario entregado y, para cada operación y escritor que el contrato
  WS12 alcance, una prueba real focalizada que muestra que una precondición obsoleta
  se rechaza sin cambios, una vigente se aplica y el rechazo es observable por el
  llamante. Si la capacidad existe, esas pruebas bastan y no se duplica código; si
  es parcial, se completa solo lo faltante y se vuelve a probar todo el contrato,
  tras recibo G_SLDB_WRITE para este delta. G_PAYLOAD_PRECONDITION se satisface solo
  con esa evidencia verificable. Este nodo es plan; no afirma que exista ni que esté
  implementado o aceptado.
output_scope: inventario y pruebas focalizadas; src/sldb/api/documents/ y src/sldb/cli/serve/
  solo si al ejecutar falta capacidad; tests/
depends_on:
- WS12
requires:
- G_SLDB_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS25
id: WS25
title: Integrar captura y triage en UI
kind: implementation
owner_repo: graph_ui
node_role: aggregate
children:
- WS25.1
- WS25.2
scope: UI para mensaje/ack y captura interna de drawer/protoátomo mediante operaciones
  permitidas por contrato; no confundir ack con aprobación. G_HUMAN_READ habilita
  uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con
  sus contratos/gates técnicos sin acta humana de lectura.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS25.1, WS25.2'
depends_on:
- WS12
- WS25.1
- WS25.2
requires:
- G_HUMAN_READ
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
- G_UI_WRITE
- G_WRITE_CONTRACT

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS28
id: WS28
title: Integrar verificación y handoff de cierre
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: 'Verificar con `deskops closeout verify` por el canal del contrato WS12, diagnosticar
  faltantes y ofrecer handoff explícito con evidencia: a `deskops closeout commit`
  por CLI en modo manual, o al coordinador si está activo (P03). No commit/close desde
  HTTP en baseline. G_HUMAN_READ aplica porque es una acción de escritura del baseline.
  G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de
  API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.'
acceptance: UF05 termina cuando `deskops show task` y el commit de closeout confirman
  el cierre externo y se refresca el estado desde deskops; El diagnóstico muestra
  los faltantes que reporta `deskops closeout verify`; comando o solicitud no equivalen
  a cierre. Sin terminal embebido genérico.
output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/
depends_on:
- WS27
- WS12
requires:
- G_CLOSEOUT
- G_HUMAN_READ
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS42
id: WS42
title: Integrar operaciones de conocimiento existentes
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: 'Invocar contratos reales de atoms split/merge y proto typing cuando disponibles,
  con confirmación de la persona usuaria en la UI, que ve el origen y el efecto de
  la operación antes de ejecutar; materializaciones se inspeccionan/validan, no se
  generan destinos arbitrarios. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo
  y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta
  humana de lectura. Operaciones split/merge/proto typing y la validación de materializaciones
  vienen del inventario Deskops WS02 y APIs SLDB WS03, concretadas por WS12; si faltan,
  WS12 registra productor/hueco y UI no disponible. Materializaciones: modelo MaterializationContractDoc
  de deskops/models/materialization.py registrado en el store temporal real seleccionado
  por TaskDoc (o manifiesto Taller WS40), versión/commit registrados; validar por
  API pública SLDB contra ese modelo, no renderer propio.'
acceptance: UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales,
  tras confirmación que muestra el origen y el efecto de la operación; las materializaciones
  existentes se inspeccionan y validan contra el modelo SLDB registrado en el store
  de la tarea, sin crear destinos; una materialización que no valida se muestra como
  inválida y no se ofrece para operar; cada capability no soportada se declara no
  disponible y bloquea solo el escenario de UF03 que la usa y su etiqueta de disponibilidad,
  no se simula. Cubierto por WS30.
output_scope: frontends/mindmap/views/workspace/knowledge/; endpoints limitados a
  la whitelist de WS12; tests/
depends_on:
- WS19
- WS24
- WS12
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

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
  WS02. WS43 lo reutiliza en publicación real; plantillas temporales enlazan por roots/aliases
  del manifiesto WS40, sin copiar ni depender del registry real.'
acceptance: 'Tras regenerar corpus WS40 con ejemplo/nav/, recorrer links Markdown
  sin UI; source versionado y destino temporal no son registros independientes. Verificar
  al regenerar que cada plantilla resuelve el root/store de procedencia de los dos
  desks del manifiesto WS40; no duplicar el registry de deskops; el conjunto temporal
  usa solo manifiesto WS40, no enlaces al checkout real. Plantillas son fuente única:
  destino temporal se regenera desde ellas, no se edita/commitea como registro competidor.
  Resolver cada link según identidad/root/store/aliases contrato WS11 contra manifiesto
  WS40; conjunto de plantillas cubre ambos desks, no cada plantilla individual.'
output_scope: ejemplo/nav/ (plantillas Markdown versionadas en el paquete del plan)
depends_on:
- WS11
- WS40
requires: []

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_SOURCE:
  title: Fuente reversible y guardas de campos probadas
  state: pending
  resolver: WS20
  evidence: API pública y tests roundtrip/conflicto/campos protegidos, con revisión
    de contrato
  produced_by: WS20
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

FILE:instruccion
Revisa el nodo PK05 siguiendo context-review-guide.md. Para ROOT/PK, reformula el RESULTADO SUSTANTIVO del paquete y da DRY-RUN HIPOTETICO de ejecucion de hijos en orden, entradas/salidas entre ellos e integracion/validacion. No describas solo como revisar hashes/status/disposition: eso es gate de comprension, no el trabajo del paquete. No ejecutes nada. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

