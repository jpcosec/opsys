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

FILE:desk/drawer/plans/workspace-documental/borradores/manual.md
# Manual de usuario — estructura propuesta

Estado: índice y criterios editoriales, no manual de una UI ya implementada. Revisar en WS10. Mantener separado del manual CLI existente docs/operator-manual.md; enlazarlo para operaciones verificadas.

## Secciones

1. Qué es un desk: documentos, conocimiento, trabajo y procedimientos.
2. Entrar al ecosistema y conocer un proyecto.
3. El workspace: explorador, selección, documentos abiertos, divisiones e historia.
4. Buscar, seguir referencias y entender relaciones/procedencia.
5. Leer y editar: fuente Markdown, renderizaciones, campos, composiciones y conflictos.
6. Capturar y aclarar: inbox, drawer, protoátomos y preguntas.
7. Trabajar conocimiento: átomos, clasificación, relaciones y materializaciones.
8. Definir trabajo: alcance, dependencias, contexto y evidencia.
9. Organizar trabajo activo: boards y fases.
10. Aplicar contexto y procedimientos: pills, rituales, pasos y lifecycle.
11. Ejecutar manualmente; validar y revisar resultados.
12. Delegar, comunicarse e intervenir (ramal Scion, marcado pendiente hasta WS37).
13. Cerrar trabajo y conservar conocimiento durable.
14. Diagnosticar integridad, relaciones rotas, conflictos e impacto de cambios.
15. Personalizar modelos, vistas y configuración mediante contratos soportados.
16. Referencia de superficies, operaciones, vocabulario y límites.
17. Recorridos completos: UF01–UF10 con el mismo proyecto de ejemplo.

## Convención por capítulo

Objetivo humano -> contexto/documentos de partida -> pasos -> resultado observable -> alternativas/errores -> referencias y operaciones reales. Etiquetar cada capacidad como disponible y comprobada, propuesta o bloqueada. Capturas se obtienen del sistema real; no se usan maquetas como evidencia.

## Qué se puede escribir ahora

Conceptos y vocabulario acordados; índice; escenarios; distinción de superficies; relación entre fuente y representación; referencias al CLI vigente. Las afirmaciones de capacidades se contrastan con WS02–WS04 y los acuerdos durables se capturan en átomos antes de materializarse en docs.

## Qué espera validación

Instrucciones exactas de UI, nombres definitivos de controles, screenshots, flujos de conflictos, edición compuesta, acciones de cierre y capítulos Scion. WS31 publica el recorrido básico probado; WS38 añade delegación después de demostrarla.

## Dependencias editoriales explícitas

Brief autosuficiente: ../brief.md. Proyecto y actas humanas: ../validacion-humana.md. Cobertura por flujo: ../cobertura.md. El capítulo de modelos se marca propuesto hasta prueba WS39; Changes avanzado hasta WS29. Los capítulos manuales incluyen el handoff a terminal/coordinador y efectos Git: no prometen que todo termine con un botón. WS31 no espera Scion ni migración Kimun.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:PK06
id: PK06
title: Publicación básica
scope: 'Manual y entradas del desk real publicados sobre recorridos ya demostrados.
  Agrupación de entregables sin ejecución propia; dry-run hipotético describe orden/aristas
  y transferencia entre hijos: WS30 acta manual y WS17 entradas alimentan WS43 publicación
  real; WS31 reúne WS10, WS30 y WS43 en manual versionado con átomos y fuentes.'
acceptance: Cada instrucción enlaza acta/versión y límites; entradas desk/README.md
  y mapa authored probadas; links/provenance atom→doc verificadas. Scion/modelos/Changes
  no demostrados siguen propuestos sin bloquear manual básico. Completitud sustantiva
  del paquete requiere salidas de sus hijos e integración indicada; revisiones de
  comprensión no equivalen a producto entregado. Describir validaciones futuras sin
  ejecutarlas; agrupación no autoriza tareas ni añade aristas.
children:
- WS31
- WS43
review_completion: 'Agrupación de revisión, no dependencia operativa. Verdadera cuando
  cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito
  con responsable. Revisión vigente: `context_review` del hijo en dag.yaml cuyo hash
  de input y de contrato coinciden con los actuales y que tiene disposition.md guardada
  en el intento correspondiente a esos hashes; lo comprueba `python desk/drawer/plans/workspace-documental/context_review.py
  status` desde la raíz de deskops. Bloqueo explícito: `context_review.status=blocked`
  por causa externa (ajena al encargo del propio hijo), que la sesión de coordinación
  que ejecuta context_review.py registra con responsable (actor o repo que debe resolverla)
  y dependencia en esa disposition.md. Un hijo con ambigüedad de su propio encargo
  sin resolver queda pending o blocked por esa causa, y entonces esta aceptación no
  es verdadera; un bloqueo externo con responsable sí la admite.'
owner_repo: deskops

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS31
id: WS31
title: Publicar manual documental básico probado
kind: documentation
owner_repo: deskops
node_role: delivery
scope: Publicar navegación, edición, captura, trabajo manual y revisión demostradas;
  incorporar el índice de borradores/manual.md, capturas y limitaciones a docs/workspace-user-manual.md.
acceptance: Cada instrucción remite al acta de WS30 o al acta de publicación de WS43
  de la versión publicada; un átomo por cada decisión Pxx humana o técnica ya registrada
  y vigente en decisiones.md y por cada contrato en contratos/ (navegacion.md, operaciones.md
  u otros de WS11/WS12); no atomizar permisos o aceptación técnica que aún no existen;
  etiquetas, links y atom->doc verificados. Scion se incluye solo como capítulo marcado
  propuesto hasta WS38. Para capítulos que mencionen personalización o impacto, comprobar
  G_HUMAN_MODEL/WS29 o mantener etiqueta propuesta; no bloquear manual básico por
  esos extras. contratos/ se resuelve en deskops:desk/drawer/plans/workspace-documental/contratos/
  según output_base WS11/12; otros contratos solo si dichos productores los inventarían
  explícitamente. Para WS29 exigir referencia a pruebas reales/recibo y commit de
  su TaskDoc de ejecución; sin ella capítulo sigue propuesto. Executor del manual
  comprueba links resolubles, etiquetas coherentes con actas/commits y atom→doc con
  fuente declarada; Tester independiente verifica esos criterios antes del cierre.
output_scope: docs/workspace-user-manual.md; docs/assets/workspace-user-manual/; desk/atoms/
  vinculados
depends_on:
- WS30
- WS10
- WS43
requires:
- G_HUMAN_MANUAL

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS43
id: WS43
title: Publicar navegación documental del desk real
kind: documentation
owner_repo: deskops
node_role: delivery
scope: 'Aplicar entradas/índices authored validados en Taller al deskops real, por
  operaciones autorizadas y preservando registry como inventario derivable. Enlazar
  repos conocidos por identidad/origen y su entrada existente; no modificar repos
  hermanos ni imponer nuevos modelos. Registrar conocimiento durable en átomos antes
  de docs. Repos a enlazar = todos los de `deskops list repositories`: enlazar no
  escribe en ellos. Escribir una entrada dentro de otro repo requiere su tarea y acuerdo
  de alcance. Contrato = contratos/navegacion.md (WS11, transitivo).'
acceptance: 'P09 y contrato fijan ubicación/modelo opcional; los acuerdos durables
  aplicados al mapa (Pxx aceptadas y contratos navegacion.md/operaciones.md de WS11/WS12)
  quedan en átomos enlazados desde él. El participante que fija P08 recorre Markdown
  y UI real, links/roots verificables (root = alias/root autorizado por el contrato
  de navegación; un enlace es verificable si resuelve a un path existente del repo
  enlazado), commit por `deskops closeout commit`, acta deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md
  y commit; no publicar solo ejemplo como si fuera ecosistema real y el mapa publicado
  corresponde a las entradas/índices validados en Taller. Escribir una entrada en
  un proyecto adicional requiere su tarea de repo y acuerdo de alcance. Regla durable
  de mapa = navegación/identidad/registry reusable P01/P02/P07/P09 vigentes (incluidos
  defaults técnicos); P03–06 solo si mapa expone operaciones, P08 remite a protocolo,
  permisos de sesión no se atomizan. Reutilizar átomo equivalente antes de crear.
  Contrastar lista paths/hashes de entradas WS17 que acta WS30 valida y registrar
  correspondencia a publicación. Repo listado sin entrada authored: enlazar registro
  existente y mostrar entrada ausente con follow-up del repo dueño; no omitir repo
  ni fabricar entrada interrepo.'
output_scope: desk/README.md; mapa de ecosistema/índices según P09 y WS11; átomos
  de acuerdos durables
depends_on:
- WS17
- WS30
requires:
- G_HUMAN_MANUAL
- G_PRODUCT
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS10
id: WS10
title: Precisar índice y convención del manual
kind: planning
owner_repo: deskops
node_role: delivery
scope: 'Índice y capítulos conceptuales, ejemplo fijo y etiqueta de disponibilidad;
  reutilizar manual CLI. Usa auditoria WS02–WS04; WS03/WS04 llegan de forma transitiva
  por WS06/WS07. Ejemplo fijo acordado P08: Taller, graph_ui:.tmp/workspace-documental-ejemplo/,
  productor WS40; hasta generarse describir como corpus futuro, sin capturas ni pasos
  inventados.'
acceptance: Definiciones verificables de disponible/propuesto/bloqueado; no escribir
  pasos ni capturas ficticios.
output_scope: borradores/manual.md
depends_on:
- WS02
- WS07
requires:
- G_PRODUCT

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

FILE:instruccion
Revisa el nodo PK06 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

