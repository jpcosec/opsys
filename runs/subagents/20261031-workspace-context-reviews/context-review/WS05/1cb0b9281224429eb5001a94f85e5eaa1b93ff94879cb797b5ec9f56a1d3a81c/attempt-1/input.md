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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS05
id: WS05
title: Inventariar identidad y API Scion
status: candidate
kind: planning
depends_on:
- WS01
requires: []
owner_repo: deskops
output_scope: auditoria/scion.md
scope: 'Leer runtime/templates/RunDoc y API pública de Scion (endpoints/SDK documentados
  o exportados; no tablas ni funciones internas); separar slug/agente/intento/dispatch/mensaje/conversación
  y permisos (roles, scopes y operaciones autorizadas según la API pública). Lee código
  y documentación en deskops y en el repo scion (../scion); no contacta endpoints
  vivos ni usa credenciales: solo el probe de WS44 es evidencia de G_SCION. Sin crear
  agentes, enviar mensajes ni modificar configuración; puede leer configuración sin
  secretos y no muestra tokens. WS05 no produce G_SCION; el probe y sus reintentos
  son responsabilidad explícita de WS44, incluso si el inventario aporta observaciones.'
acceptance: No usar tablas internas como interfaz; señalar los campos internos que
  no figuren en la API pública definida en el scope y capacidades que requieren API
  real; el inventario separa slug/agente/intento/dispatch/mensaje/conversación y permisos;
  marca qué capabilities requieren WS32 y WS33.
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws05.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: deskops:desk/drawer/plans/workspace-documental/
node_role: delivery
review_context_nodes:
- WS33

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS01
id: WS01
title: Fijar brief y glosario autosuficientes
kind: planning
owner_repo: deskops
node_role: delivery
scope: Brief/glosario ya authored y cubiertos por recibo covered_work. Al promover
  auditorías verificar hash/alcance; no reescribir si no cambió decisión/contrato.
  Si cambia realmente el encargo, editar solo brief.md con acuerdos textuales y vocabulario
  documento/nodo/vista/renderer/consulta/foco; sin chat invisible.
acceptance: brief.md enlaza decisiones.md como registro Pxx completo; no editar decisiones.md
  desde este nodo. Acuerdos textuales tienen actor/fuente y distinciones glosario
  legibles. Coordinator compara reformulación/dry-run de review barato aislado ritual-context-review
  con intención y explicita hallazgos/disposición; APTO no basta. Cobertura documental
  actual satisface elaboración del brief, no lifecycle cerrado ni autorización producto.
output_scope: brief.md
depends_on: []
requires: []

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
  e idempotentes. WS32.1/32.2 validan identidad/registro/idempotencia local sin dispatch/reply
  de red; estados Hub reales se prueban y correlacionan en WS34/37 bajo G_EXEC, sin
  mocks ni eventos inventados.'
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
  no es slug; dispatch intent (intención local registrada) y confirmed (solo respuesta
  Hub observada) como hechos separados del RunDoc; ambos se registran en el registro
  por intento que WS32.2 vuelve manifiesto canónico. Confirmed = respuesta de la API
  pública de Scion con la identidad que exponga, a comprobar en WS05/WS44. WS12 especifica
  contrato/ubicación del registro por intento (input de WS32.2), derivado del runtime
  real inventariado WS05; WS32.1 materializa ese registro e identidades según contrato,
  no inventa almacenamiento. Código models/run.py se cambia como código de modelo
  con registro/validación SLDB; instancias RunDoc trackeadas se crean/editan por API/CLI
  SLDB, sin ad hoc Markdown. Solo identidad/persistencia mediante operaciones locales
  reales en store temporal, SIN dispatch/reply de red ni evento Hub fingido. Registro
  local intent/no confirmado no afirma fallo/éxito de Hub.'
acceptance: Dos intentos locales generan IDs distintos antes de dispatch y registro
  intent/no confirmado mediante operaciones reales del store temporal, sin simular
  respuesta Hub ni invocar red. Ningún no confirmado se etiqueta como fallo/aceptado
  Hub sin evidencia. WS34 (con G_EXEC) y WS37 demostrarán dispatch real fallido/confirmado
  y correlación exacta al id previo; contrato de integración explícito. Código modelos
  se registra/valida SLDB y RunDoc trackeado se edita por API/CLI, no ad hoc.
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
  evidencia y commit de cierre). Idempotencia de persistencia local por operaciones
  reales del store temporal, sin dispatch/reply de red ni confirmar evento Hub no
  observado; prueba runtime con Hub y correlación es WS34/37 bajo G_EXEC.'
acceptance: Una finalización repetida sobre el mismo id de intento conserva identidad
  y evidencia sin crear registros nuevos; manifiesto, RunDoc y registros de closeout
  coinciden en id de intento, hash de sesión y evidencia. Sesión aquí = artefacto
  de sesión/log del intento que identifique inventario WS05 y contrato WS12, con campo/algoritmo
  digest y fuente exactos declarados allí. No hash de proceso/slug ni valor fabricado.
  Si no existe artefacto/contrato de hash, registrar hueco con productor WS12/WS05
  y bloquear esa coincidencia antes de promoción.
output_scope: deskops/runtime/scion.py; models/run.py; services/closure.py; tests/
depends_on:
- WS05
- WS12
- WS32.1
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS44
id: WS44
title: Comprobar y revalidar acceso público a Scion
kind: validation
owner_repo: deskops
node_role: delivery
scope: Responsable de instalación Scion, designado por solicitante al abordar ramal
  E, realiza probe read-only de API con acceso ya autorizado; verifica capacidades/identidad
  necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar
  config o mostrar secretos. Puede repetir el probe si el inventario WS05 terminó
  sin acceso. El solicitante registra en autorizaciones/scion.md qué acceso read-only
  tiene el operador; sin ese registro no se ejecuta el probe. El operador indica el
  Hub desde la configuración existente. Las capabilities mínimas son las que auditoria/scion.md
  marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene
  y registra el hueco antes del probe.
acceptance: 'G_SCION se satisface solo con respuesta pública real, identidad del operador
  (actor del probe) y Hub, fecha y capabilities registrados. Si API o acceso no están,
  WS44 permanece bloqueada, no se cierra unverified ni se avanza WS32. Tras cambio
  de Hub/API/credencial, repetir y invalidar recibo previo. Operador/acceso aún no
  designados: pendiente intencional solo de ramal E; no atribuir autorización al acuerdo
  de producto.'
output_scope: auditoria/scion-probe.md
depends_on:
- WS05
- WS07
requires:
- G_PRODUCT

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_SCION:
  title: Scion accesible y contrato público comprobado
  state: unverified
  resolver: WS44, operador a designar al abordar ramal E
  evidence: auditoria/scion-probe.md bajo paquete del plan; actor de WS44, fecha/Hub/endpoint/identidad/capabilities
    de API pública, sin secretos. WS05 solo inventaría; WS44 permanece bloqueada hasta
    probe real y puede revalidarse.
  produced_by: WS44

FILE:instruccion
Revisa el nodo WS05 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

