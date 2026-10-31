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

FILE:desk/drawer/plans/workspace-documental/borradores/vision.md
# Visión del workspace documental

Estado: borrador basado en brief.md; base producto registrada en decisiones.md; contratos técnicos WS11/WS12 pendientes. No describe funcionalidades ya entregadas ni reemplaza átomos/modelos del proyecto.

## Propósito

Permitir a una persona entender y operar un proyecto mediante sus documentos, relaciones y procedimientos. Un IDE para el desk: explorar, abrir, leer, editar, vincular y actuar sobre el mismo material, conservando contexto.

## Unidad de trabajo

Los documentos del desk son Markdown, modelados o no; un contrato estructurado es opcional según el soporte. Fuente y renderizado conservan la identidad y procedencia. Una representación puede mostrar un documento, componer documentos referenciados o evaluar una selección: no toda vista equivale a un único archivo ni toda relación requiere un documento nuevo. Código, eventos y estado de ejecución pueden tener otros soportes; no fingir que el runtime es Markdown.

## Superficies

Inbox, drawer, boards, tareas y fases, pills, rituales/lifecycle, átomos/protoátomos, materializaciones, registro de repositorios, roles/runtimes y ejecuciones. Su navegación debe mostrar relaciones y operaciones reales, con infraestructura documental como autoridad de lectura/escritura y Deskops como autoridad del workflow.

## Interacción propuesta

Explorador, documentos abiertos en pestañas y divisiones, búsqueda y panel contextual. Seleccionar un documento permite cambiar representación y seguir enlaces sin perder historia. La organización del ecosistema procede de documentos de entrada/índice, consultas y relaciones; el shell ofrece mecanismos genéricos de navegación. Disposición y preferencia local no necesitan convertirse automáticamente en documentos compartidos.

## Criterios de producto

- Trabajar sin agentes es un recorrido completo.
- Leer Markdown permite recorrer la estructura sin depender exclusivamente de la UI.
- Cada edición tiene destino y cada composición conserva origen.
- Una condición sintáctica satisfecha no se presenta como prueba de que tests o revisión humana pasaron.
- Un error o relación rota tiene diagnóstico; no se disfraza de colección vacía.
- El usuario puede comprender las consecuencias de una acción; no necesita conocer comandos internos para operaciones soportadas.

## Decisiones abiertas

Dónde viven y qué contratos usan las entradas e índices; alcance real de ViewDoc; APIs backend real; representación local de selección/disposición acordada en P07; guardas de edición fuente y sincronización; autoridad y compatibilidad de acciones; mediciones contra objetivos aceptados P08. Resolver contratos con WS02–WS04/WS11/WS12, no improvisar al dibujar pantallas.

## Superficies adicionales y material existente

CrossroadDoc y namespaces organizan dominios; issues Markdown deliberadamente no modelados son legibles y operables mediante contratos existentes. FAQ y StepDoc son documentos de orientación/procedimiento. Brainstorm, Schema/edición de clases y Specs ya existen en Mindmap: inventariar y conservar/integrar sus capacidades explícitamente. Carpetas legacy (features/primitives/logbook/materializers) se clasifican por soporte actual en WS02, no por nombre ni como modelo obligatorio nuevo. KGDB no es otro servicio nuevo: la capa de grafo actual vive en sldb; no reintroducir el proyecto retirado.

Vocabulario normativo de este borrador: brief.md. Alcance: alcance.md. Base acordada de host, backend y escritura: decisiones.md; pendiente prueba técnica de sus guardas. El workspace puede enfocar nodos no documentales, pero el documento no pierde su identidad al cambiar de representación.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:ROOT
id: ROOT
title: Workspace documental de Deskops
scope: 'Lector temprano, autoría/operación manual y manual publicado sobre Mindmap/SLDB/Deskops;
  extensiones y Scion independientes. Agrupación de entregables sin ejecución propia;
  dry-run hipotético describe orden/aristas y transferencia entre hijos: PK01 audita
  base y reconcilia deltas; PK02 convierte decisiones registradas en flows/vistas/contratos;
  PK03 entrega y valida lector; PK04 representa navegación/trabajo/conocimiento; PK05
  habilita manual con guardas y evidencia; PK06 publica entradas/manual comprobados;
  PK07 añade Changes/modelos por separado; PK08 delegación posterior con Scion/permisos
  reales.'
acceptance: Validar futuro por actas humanas WS16/30 y publicación WS43/31; extras
  solo tras sus pruebas propias, Scion tras WS37/38. Comprobar identidad/origen compartidos,
  APIs públicas, guardas/canales, manual trazado a versión y ausencia de dependencias
  opcionales sobre núcleo. Completitud sustantiva del paquete requiere salidas de
  sus hijos e integración indicada; revisiones de comprensión no equivalen a producto
  entregado. Describir validaciones futuras sin ejecutarlas; agrupación no autoriza
  tareas ni añade aristas. Para revisar este macroencargo, dry-run debe describir
  cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas, qué artefacto
  pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse a comprobar
  status/hashes/disposition. No ejecutar esos pasos ahora.
children:
- PK01
- PK02
- PK03
- PK04
- PK05
- PK06
- PK07
- PK08
review_completion:
  protocol: ritual-context-review
  state_field: context_review
  meaning: Gate de comprensión solamente; no define resultado ni completitud sustantiva
    del paquete.
owner_repo: deskops

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK01
id: PK01
title: Fundamentos y auditoría
owner_repo: deskops
children:
- WS01
- WS02
- WS03
- WS04
- WS05
- WS06
scope: 'Base factual y matriz de deltas verificables para no duplicar código. Agrupación
  de entregables sin ejecución propia; dry-run hipotético describe orden/aristas y
  transferencia entre hijos: WS01 brief cubierto alimenta auditorías independientes
  WS02 Deskops, WS03 infraestructura y WS04 UI; WS06 integra sus evidencias por delta/repo.
  WS05 inventario Scion es independiente y alimenta E.'
acceptance: Auditorías citan capacidades existentes/ausentes/huecos y repo dueño;
  matriz registra reutilización/ticket/delta pendiente con evidencia actual. Sin implícitos
  de chat, sin aceptar producto ni probes vivos. Completitud sustantiva del paquete
  requiere salidas de sus hijos e integración indicada; revisiones de comprensión
  no equivalen a producto entregado. Describir validaciones futuras sin ejecutarlas;
  agrupación no autoriza tareas ni añade aristas. Para revisar este macroencargo,
  dry-run debe describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK02
id: PK02
title: Decisiones y contratos
owner_repo: deskops
children:
- WS07
- WS08
- WS09
- WS10
- WS11
- WS12
scope: 'Contratos de producto/navegación/operaciones que permiten preparar cada delta.
  Agrupación de entregables sin ejecución propia; dry-run hipotético describe orden/aristas
  y transferencia entre hijos: WS07 reutiliza decisiones humanas dadas contra WS06;
  WS08 define UFs; WS10 fija convención manual; WS09 cataloga vistas consumiendo ambos;
  WS11 identidad/navegación y WS12 whitelist técnica por delta.'
acceptance: Pxx trazadas; cada UF tiene operaciones/errores/IDs/gates; vistas tienen
  soporte/origen; APIs y huecos con productores. Recepción técnica por delta, sin
  bloquear núcleo por extras ni suponer editable sin G_SOURCE. Completitud sustantiva
  del paquete requiere salidas de sus hijos e integración indicada; revisiones de
  comprensión no equivalen a producto entregado. Describir validaciones futuras sin
  ejecutarlas; agrupación no autoriza tareas ni añade aristas. Para revisar este macroencargo,
  dry-run debe describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK03
id: PK03
title: Lector y descubrimiento
owner_repo: deskops
children:
- WS13
- WS14
- WS15
- WS16
- WS40
- WS41
scope: 'Lector útil con descubrimiento sin ID y aceptación humana temprana. Agrupación
  de entregables sin ejecución propia; dry-run hipotético describe orden/aristas y
  transferencia entre hijos: WS11/08 habilitan WS13 e hijos, búsqueda WS14 y errores/orientación
  WS15; WS40 produce Taller real y WS41 lectura entre desks; WS16 integra guion humano.'
acceptance: Abrir soporte modelado/no modelado, foco/historia/Code/grafo, búsqueda
  y errores reales; Taller incluye dos desks y repo sin desk; acta WS16 con mediciones
  P08. No depender de edición/Changes/Scion. Completitud sustantiva del paquete requiere
  salidas de sus hijos e integración indicada; revisiones de comprensión no equivalen
  a producto entregado. Describir validaciones futuras sin ejecutarlas; agrupación
  no autoriza tareas ni añade aristas. Para revisar este macroencargo, dry-run debe
  describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora. Mediciones
  P08 aquí son aperturas/búsquedas/arranque; guardado corresponde solo WS30. Grafo/Code
  existentes y su integración documental los aporta WS13.1 vía agregado WS13.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK04
id: PK04
title: Navegación y representaciones
owner_repo: deskops
children:
- WS17
- WS18
- WS22
- WS23
- WS24
scope: 'Entradas authored y representaciones navegables del desk sobre identidad común.
  Agrupación de entregables sin ejecución propia; dry-run hipotético describe orden/aristas
  y transferencia entre hijos: WS17 consume WS11/40 para índices del ejemplo; WS22
  Board y WS23 procedimientos consumen WS13/09; WS24 conocimiento reutiliza vecindad.
  WS18 ViewDoc es extensión opcional tras G_SPEC_VIEW y no bloquea WS24.'
acceptance: Abrir mismos documentos/soportes desde lista/tablero/dependencias, procedimiento
  y conocimiento; no escribir status desde renderer ni marcar pasos por lectura; índices
  siguen fuentes. ViewDoc portable prueba selección solo cuando se integra. Completitud
  sustantiva del paquete requiere salidas de sus hijos e integración indicada; revisiones
  de comprensión no equivalen a producto entregado. Describir validaciones futuras
  sin ejecutarlas; agrupación no autoriza tareas ni añade aristas. Para revisar este
  macroencargo, dry-run debe describir cómo se ejecutaría hipotéticamente el paquete
  por sus hijos/orden/aristas, qué artefacto pasa a qué hijo y cómo se probaría resultado
  integrado; NO limitarse a comprobar status/hashes/disposition. No ejecutar esos
  pasos ahora.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK05
id: PK05
title: Autoría y operación manual
owner_repo: deskops
children:
- WS19
- WS20
- WS21
- WS25
- WS26
- WS27
- WS28
- WS30
- WS42
scope: 'Autoría manual segura, intake/trabajo y revisión/cierre por handoff verificables.
  Agrupación de entregables sin ejecución propia; dry-run hipotético describe orden/aristas
  y transferencia entre hijos: WS12 contrato por delta alimenta WS19 campos, WS20
  API fuente/G_SOURCE y WS21 fuente/render; WS25 captura, WS26 tareas, WS27 diff/evidencia,
  WS28 handoff y WS42 conocimiento; WS30 integra pruebas humanas con entradas WS17.'
acceptance: CAS/conflicto/buffer/protegidos probados; guardar sin commit; coordinador
  escritor implica read-only/handoff; mostrar evidencia declarada/encontrada/verificada
  distinta; cierre confirmado por commit/Deskops. Acta WS30 cubre UF02–05 y navegación;
  uso UI espera G_HUMAN_READ, desarrollo API aislado no. Completitud sustantiva del
  paquete requiere salidas de sus hijos e integración indicada; revisiones de comprensión
  no equivalen a producto entregado. Describir validaciones futuras sin ejecutarlas;
  agrupación no autoriza tareas ni añade aristas. Para revisar este macroencargo,
  dry-run debe describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK06
id: PK06
title: Publicación básica
owner_repo: deskops
children:
- WS31
- WS43
scope: 'Manual y entradas del desk real publicados sobre recorridos ya demostrados.
  Agrupación de entregables sin ejecución propia; dry-run hipotético describe orden/aristas
  y transferencia entre hijos: WS30 acta manual y WS17 entradas alimentan WS43 publicación
  real; WS31 reúne WS10, WS30 y WS43 en manual versionado con átomos y fuentes.'
acceptance: Cada instrucción enlaza acta/versión y límites; entradas desk/README.md
  y mapa authored probadas; links/provenance atom→doc verificadas. Scion/modelos/Changes
  no demostrados siguen propuestos sin bloquear manual básico. Completitud sustantiva
  del paquete requiere salidas de sus hijos e integración indicada; revisiones de
  comprensión no equivalen a producto entregado. Describir validaciones futuras sin
  ejecutarlas; agrupación no autoriza tareas ni añade aristas. Para revisar este macroencargo,
  dry-run debe describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK07
id: PK07
title: Extensiones independientes
owner_repo: deskops
children:
- WS29
- WS39
scope: 'Changes y modelos como extensiones independientes con evidencia propia. Agrupación
  de entregables sin ejecución propia; dry-run hipotético describe orden/aristas y
  transferencia entre hijos: WS29 consume lectura/vecindad WS15/24 para check/doctor/drift
  e impacto; WS39 consume contrato WS12 para inspección/edición Schema existente.
  Ninguno es prerrequisito del lector o manual básico.'
acceptance: WS29 prueba mutación real e impacto 1 hop y diagnóstico sin reparación
  automática; WS39 prueba edición/validación por API y aceptación humana propia. Manual
  etiqueta cada extra según evidencia, no presume CST/Kimun. Completitud sustantiva
  del paquete requiere salidas de sus hijos e integración indicada; revisiones de
  comprensión no equivalen a producto entregado. Describir validaciones futuras sin
  ejecutarlas; agrupación no autoriza tareas ni añade aristas. Para revisar este macroencargo,
  dry-run debe describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:PK08
id: PK08
title: Ramal Scion opcional
owner_repo: deskops
children:
- WS32
- WS33
- WS34
- WS35
- WS36
- WS37
- WS38
- WS44
scope: 'Delegación Scion posterior con intentos/trazas/intervención verificables.
  Agrupación de entregables sin ejecución propia; dry-run hipotético describe orden/aristas
  y transferencia entre hijos: WS05 inventario alimenta WS44; solo WS44 probe con
  operador/acceso designados produce G_SCION; WS32 identifica intento/cierre, WS33
  mensajes/decisiones, WS34 acciones autorizadas G_EXEC, WS35 trazas y WS36 UI; WS37
  acepta recorrido real y WS38 publica capítulo tras manual básico.'
acceptance: Intento/manifiesto/RunDoc/cierre consistentes e idempotentes, mensajes
  con procedencia/dedup, dispatch intent/confirmed separados, permisos explícitos
  y acta humana WS37. Sin acceso real ramal bloqueado; ningún permiso de núcleo se
  convierte en dispatch. No duplicar pipeline Scion. Completitud sustantiva del paquete
  requiere salidas de sus hijos e integración indicada; revisiones de comprensión
  no equivalen a producto entregado. Describir validaciones futuras sin ejecutarlas;
  agrupación no autoriza tareas ni añade aristas. Para revisar este macroencargo,
  dry-run debe describir cómo se ejecutaría hipotéticamente el paquete por sus hijos/orden/aristas,
  qué artefacto pasa a qué hijo y cómo se probaría resultado integrado; NO limitarse
  a comprobar status/hashes/disposition. No ejecutar esos pasos ahora.

FILE:instruccion
Revisa el nodo ROOT siguiendo context-review-guide.md. Para ROOT/PK, reformula el RESULTADO SUSTANTIVO del paquete y da DRY-RUN HIPOTETICO de ejecucion de hijos en orden, entradas/salidas entre ellos e integracion/validacion. No describas solo como revisar hashes/status/disposition: eso es gate de comprension, no el trabajo del paquete. No ejecutes nada. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

