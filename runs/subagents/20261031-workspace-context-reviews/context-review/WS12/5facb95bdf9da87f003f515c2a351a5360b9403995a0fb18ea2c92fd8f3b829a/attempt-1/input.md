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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS12
id: WS12
title: Cerrar contrato de operaciones y escritura
status: candidate
kind: planning
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY
owner_repo: deskops
output_scope: contratos/operaciones.md
scope: Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy
  coordinador, Git, workflow-protected fields, CAS/locks, fallos parciales, permisos
  y closeout fuera del servidor UI. Adapter = canal público existente (CLI/DeskopsOperations/API
  sldb) por el que la UI invoca cada operación; si no existe, se registra hueco y
  dueño, no se diseña uno aquí.
acceptance: 'G_WRITE_POLICY registrado. Publicar whitelist por operación/campo/canal/actor/revisión/Git/efectos
  y estado existente comprobado/faltante. Obtener recibo receptor y prueba solo para
  delta que se habilita: campos/intake no esperan Changes/modelos/Scion ni raw-source.
  G_WRITE_CONTRACT y G_UI_WRITE se evalúan por IDs/efecto, nunca como aceptación conjunta.
  Autoría de tareas/cierre esperan G_CLOSEOUT. Raw-source faltante tiene productor
  WS20 y G_SOURCE; recepción G_SLDB_WRITE antes de WS20, sin exigir API implementada
  para especificar contrato. Lock solo UI no coordina CLI/agentes: con otro coordinador
  escritor, read-only/handoff hasta API pública con autoridad compartida probada.'
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws12.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: deskops:desk/drawer/plans/workspace-documental/
node_role: delivery

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
acceptance: Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales;
  cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño
  antes de code. Registrar recepción lector por delta en graph_ui (actor P01, IDs,
  efecto y evidencia). El contrato básico puede cerrar sin recepción de Changes, Scion
  ni ViewDoc opcional; cada delta sigue bloqueado hasta su propio recibo. G_SPEC_VIEW
  se obtiene separadamente al preparar WS18, sin bloquear navegación base.
output_scope: contratos/navegacion.md; recibos G_UI_READ por delta; recepción G_SPEC_VIEW
  separada y opcional
depends_on:
- WS09
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
  hueco, sin inventarla.
output_scope: borradores/user-flows.md
depends_on:
- WS07
requires:
- G_PRODUCT

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS19.1
id: WS19.1
title: Editar campos con conflicto visible
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS19
scope: Edición de campos reutilizando editores y API, con revisión esperada (hash
  CAS del documento) y conflicto visible (mensaje de rechazo con el texto local conservado);
  workflow-protected fields no editables por este canal. Delta sobre workspace integrado
  a1b2b22 de edición. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y
  pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta
  humana de lectura.
acceptance: Guardar/recargar confirma dato real; una escritura obsoleta no pierde
  texto local y el conflicto se muestra como tal. Mutación restringida a desk en modo
  manual exclusivo (P03); otros modos read-only hasta contrato.
output_scope: frontends/mindmap/views/workspace/fields/; endpoints del contrato WS12
  consumidos desde graph_ui sin cambios de contrato; tests/
depends_on:
- WS12
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS19.2
id: WS19.2
title: Editar relaciones permitidas por contrato
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS19
scope: Alta/baja de relaciones permitidas por contrato, usando API real y before-image;
  no crear semántica de relaciones en el componente. G_HUMAN_READ habilita uso de
  mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates
  técnicos sin acta humana de lectura.
acceptance: Alta y baja persisten y se confirman tras recargar; una relación no permitida
  o una revisión obsoleta se rechaza con error visible.
output_scope: frontends/mindmap/views/workspace/relations/; endpoints autorizados
  por el contrato WS12; tests/
depends_on:
- WS12
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS25.1
id: WS25.1
title: Leer inbox y registrar ack o respuesta local
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS25
scope: UI para leer mensajes, ack y respuesta dentro del mismo desk mediante operaciones
  permitidas por contrato; sin envío interdesk; no confundir ack con aprobación. G_HUMAN_READ
  habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar
  con sus contratos/gates técnicos sin acta humana de lectura.
acceptance: Ack persiste tras recargar mostrando el mensaje origen; respuesta local
  solo si el contrato WS12 define esa operación, y si no se declara no disponible;
  no crea tarea implícita ni cron de triage. Permisos del contrato aplicados.
output_scope: frontends/mindmap/views/workspace/inbox/; endpoints autorizados por
  el contrato WS12; tests/
depends_on:
- WS12
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS25.2
id: WS25.2
title: Capturar en drawer o protoátomo
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS25
scope: Captura interna con destino elegido explícitamente por la persona usuaria —candidato
  de drawer o protoátomo— mediante operaciones permitidas por el contrato WS12, sin
  exigir tarea; cada destino se prueba por separado. G_HUMAN_READ habilita uso de
  mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates
  técnicos sin acta humana de lectura.
acceptance: 'UF02: una captura persiste tras recargar en el destino elegido, con origen
  y sin tarea implícita. Permisos del contrato aplicados. Origen = referencia tipada
  al soporte del que nace la captura (ruta o mensaje), con representación fijada por
  el contrato WS12; los orígenes ruta y mensaje se registran y se muestran tras recargar.'
output_scope: frontends/mindmap/views/workspace/capture/; endpoints autorizados por
  el contrato WS12; tests/
depends_on:
- WS12
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS26.1
id: WS26.1
title: Autorar tarea, evidencia y contexto
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS26
scope: Autoría explícita desde candidato, evidencia declarada, dependencias y binding
  de contexto/pills. Candidato = archivo del drawer. G_HUMAN_READ habilita uso de
  mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates
  técnicos sin acta humana de lectura.
acceptance: 'UF04 sobre TaskDoc real: el candidato queda autorado con evidencia declarada,
  dependencias y pills de contexto vinculadas y visibles tras recargar; nunca editar
  status para avanzar. Si una operación Git no tiene contrato o dueño, la acción queda
  en handoff explícito y se declara no disponible.'
output_scope: frontends/mindmap/views/workspace/authoring/; endpoints autorizados
  por el contrato WS12; tests/
depends_on:
- WS12
- WS22
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS26.2
id: WS26.2
title: Enrutar en Board y mostrar capa lista
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS26
scope: Enrutamiento explícito en Board y representación de capa lista por dependencias/no
  solapamiento; promoción solo cuando el contrato resuelve commits previos por canal
  autorizado. Enrutar = añadir la tarea a la lista tasks del BoardDoc por operación
  pública. Capa lista = tareas sin dependencias pendientes y sin archivos solapados
  según los `files` declarados en cada TaskDoc y el ritual de fase. G_HUMAN_READ habilita
  uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con
  sus contratos/gates técnicos sin acta humana de lectura.
acceptance: Tras enrutar, `deskops show board` muestra la tarea y la UI la distingue
  de una tarea en ejecución; el canal de promoción respeta commits previos y estado
  real; la capa lista se muestra separada de tareas en ejecución y de tareas con dependencias
  pendientes o archivos solapados.
output_scope: frontends/mindmap/views/workspace/routing/; endpoints autorizados por
  el contrato WS12; tests/
depends_on:
- WS12
- WS22
- WS26.1
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS27.1
id: WS27.1
title: Mostrar diff Git por repo y tarea
kind: implementation
owner_repo: graph_ui
node_role: delivery
parent_id: WS27
scope: 'Diff Git e historial read-only junto a la TaskDoc. Base: commits listados
  en TaskDoc.references y rutas en TaskDoc.files (campos del modelo TaskDoc de deskops);
  sin commits, working tree contra HEAD limitado a esas rutas.'
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
scope: Evidencia junto a la TaskDoc. Sin modelo de comentarios nuevo.
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS32
id: WS32
title: Unificar identidad de intento y cierre Scion
kind: implementation
owner_repo: deskops
node_role: aggregate
children:
- WS32.1
- WS32.2
scope: 'Refinar el ticket de external_references.scion, sin segundo pipeline: intento
  no es slug, dispatch intent/confirmed separado, manifiesto/RunDoc/cierre consistentes
  e idempotentes.'
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS32.1, WS32.2'
depends_on:
- WS05
- WS12
- WS32.1
- WS32.2
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS32.1
id: WS32.1
title: Separar identidad de intento y dispatch
kind: implementation
owner_repo: deskops
node_role: delivery
parent_id: WS32
scope: 'Refinar el ticket de external_references.scion, sin segundo pipeline: intento
  no es slug; dispatch intent (intención registrada) y confirmed (Scion aceptó) como
  hechos separados del RunDoc; ambos se registran en el registro por intento que WS32.2
  vuelve manifiesto canónico. Confirmed = respuesta de la API pública de Scion con
  la identidad que exponga, a comprobar en WS05/WS44.'
acceptance: Dos intentos del mismo agente y un dispatch fallido (rechazo de la API
  o timeout) conservan identidades distintas, evidenciadas por ids de intento propios,
  generados por deskops antes del dispatch; cambios de RunDoc por el flujo SLDB de
  modelos (registro y edición de documento trackeado con CLI sldb), no edición ad
  hoc.
output_scope: deskops/runtime/scion.py; models/run.py; services/closure.py; tests/
depends_on:
- WS05
- WS12
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS32.2
id: WS32.2
title: Hacer idempotente manifiesto y cierre
kind: implementation
owner_repo: deskops
node_role: delivery
parent_id: WS32
scope: 'Manifiesto, RunDoc y cierre consistentes e idempotentes sobre el intento correcto
  (el identificado por el id de intento que cita el cierre, nunca por agente o slug).
  Manifiesto = registro canónico por intento que materializa RunDoc y registros de
  closeout, según el ticket de external_references.scion (campos mínimos: id de intento,
  identidad de agente, identidad de run si la API la expone, timestamps, hash de sesión,
  evidencia y commit de cierre).'
acceptance: Una finalización repetida sobre el mismo id de intento conserva identidad
  y evidencia sin crear registros nuevos; manifiesto, RunDoc y registros de closeout
  coinciden en id de intento, hash de sesión y evidencia.
output_scope: deskops/runtime/scion.py; models/run.py; services/closure.py; tests/
depends_on:
- WS05
- WS12
- WS32.1
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS34
id: WS34
title: Exponer despacho y respuesta Scion autorizados
kind: implementation
owner_repo: deskops
node_role: aggregate
children:
- WS34.1
- WS34.2
scope: Un adaptador público restringido para dispatch/reply, con confirmación, identidad
  de intento, timeout/errores y autoridad del coordinador.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS34.1, WS34.2'
depends_on:
- WS33
- WS12
- WS34.1
- WS34.2
requires:
- G_EXEC
- G_SCION
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS34.1
id: WS34.1
title: Exponer dispatch autorizado
kind: implementation
owner_repo: deskops
node_role: delivery
parent_id: WS34
scope: Adaptador público restringido para dispatch, con confirmación, identidad de
  intento, timeout/errores y autoridad del coordinador. Confirmación = respuesta de
  la API de Scion. Autoridad del coordinador según contrato WS12.
acceptance: G_SCION/G_EXEC pasan; agente real demuestra un dispatch aceptado y uno
  rechazado o vencido por timeout. No shell arbitrario ni duplicar transporte.
output_scope: runtime/; cli/commands/runtime.py o la API que fije el contrato WS12;
  tests/
depends_on:
- WS33
- WS12
requires:
- G_EXEC
- G_SCION
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS34.2
id: WS34.2
title: Exponer respuesta autorizada
kind: implementation
owner_repo: deskops
node_role: delivery
parent_id: WS34
scope: Adaptador público restringido para reply vinculado al intento, con timeout/errores
  y autoridad del coordinador.
acceptance: G_SCION/G_EXEC pasan; agente real demuestra respuesta vinculada al intento
  correcto y un timeout se reporta como fallo sin confirmación, con el umbral del
  contrato WS12. No mandar mensajes en la tarea de planificación.
output_scope: runtime/; cli/commands/runtime.py o API definida; tests/
depends_on:
- WS33
- WS12
- WS34.1
requires:
- G_EXEC
- G_SCION
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS39
id: WS39
title: Integrar inspección y edición de modelos existente
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Hacer navegables Schema/editar clases ya disponibles desde documento/contexto;
  usar draft/validate/promote de sldb. No reimplementar modelos. G_HUMAN_READ habilita
  uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con
  sus contratos/gates técnicos sin acta humana de lectura.
acceptance: UF09 inspección y mutación en store temporal real de prueba; comprobar
  los efectos y errores que declara el contrato WS12; no habilitar promover si API/autoridad
  falta. Extensión posterior al lector básico. Guardar acta de prueba humana en graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md
  con el participante que fija P08 y resultado; G_HUMAN_MODEL debe pasar antes de
  marcar disponible en el manual que publica WS31 el capítulo 15 (Personalizar modelos)
  del índice de borradores/manual.md.
output_scope: shell/dialogs.js; views/models/; tests/; runs/subagents/workspace-documental-acceptance/modelos/
depends_on:
- WS12
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS42
id: WS42
title: Integrar operaciones de conocimiento existentes
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Invocar contratos reales de atoms split/merge y proto typing cuando disponibles,
  con confirmación de la persona usuaria en la UI, que ve el origen y el efecto de
  la operación antes de ejecutar; materializaciones se inspeccionan/validan, no se
  generan destinos arbitrarios. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo
  y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta
  humana de lectura.
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_WRITE_POLICY:
  title: Política de escritura aprobada por humano
  state: satisfied
  resolver: WS07
  evidence: 'decisiones.md: P03/P04/P05/P06, actor/tipo/fuente/resultado registrados;
    no aprobación técnica ni Scion'
  produced_by: WS07
  verified_evidence: runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json;
    decisiones.md P07/P09 defaults técnicos delegados, 2026-10-31
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
G_SLDB_WRITE:
  title: Alcance fuente aceptado en sldb
  state: pending
  resolver: WS12
  produced_by: WS12
  evidence: 'Acta de recepción por delta concreto en repo receptor: actor solicitante
    humano designado P01, fecha, alcance/IDs, efecto, task receptora/no solapamiento
    y commit/blob verificable. Cada nodo usa solo su recibo; ausencia de otro delta
    no bloquea este. Estado global pendiente resume recibos, no obliga aceptación
    conjunta.'
  scope_nodes:
  - WS20
  evaluation: per_delta
  accepted_scope_nodes: []
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
G_SOURCE:
  title: Fuente reversible y guardas de campos probadas
  state: pending
  resolver: WS20
  evidence: API pública y tests roundtrip/conflicto/campos protegidos, con revisión
    de contrato
  produced_by: WS20

FILE:instruccion
Revisa el nodo WS12 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

