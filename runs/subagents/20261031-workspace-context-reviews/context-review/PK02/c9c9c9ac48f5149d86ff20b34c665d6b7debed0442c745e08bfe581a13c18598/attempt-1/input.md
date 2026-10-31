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
- Las propuestas Pxx de decisiones.md no son decisiones humanas. No las des por aprobadas ni pidas resolverlas aquí.
- Una dependencia futura que debe producir un contrato, API o inventario no es ambigüedad si el encargo nombra quién lo produce y qué hacer si falta.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance.

No cuentan: decisiones Pxx pendientes con actor, detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills), trabajo de nodos dependientes o funciones excluidas en alcance.md.

Tampoco cuentan: textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará dentro de la aceptación, ni el comportamiento ante un contrato ausente, que alcance.md resuelve en "Reglas comunes de ejecución".

Cita la frase del input que origina cada ambigüedad.

FILE:desk/drawer/plans/workspace-documental/brief.md
# Brief autosuficiente y glosario — borrador para WS01/WS07

## Encargo y acuerdos explícitos del solicitante

La persona solicita un DAG que cubra el workspace documental, sus vistas/renderizaciones, manual y user-flows; ahora pide iterar con el concilio hasta pulirlo. Esto autoriza corregir el plan, no implementar la UI ni modificar tareas de otras sesiones.

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

Ver decisiones.md. Los acuerdos anteriores no resuelven automáticamente host, autoridad de escritura, fuente protegida, Git o aprobación humana. WS07 produce ese registro; no se inventa aceptación por existir este archivo.

FILE:desk/drawer/plans/workspace-documental/alcance.md
# Alcance y límites de las entregas

## Entrega L — lector útil temprano

Abrir soporte real, fuente/render de lectura, foco/historia, búsqueda, links y errores honestos. Conserva las capacidades existentes de KB/Flujo/Brainstorm/Schema/Specs/Deskops cuando se integren en el host. Code local a 1–2 hops según soporte real ya en el ticket del workspace; no se promete navegación CST inexistente. WS16 valida antes de habilitar mutaciones; representaciones solo lectura pueden desarrollarse en paralelo.

## Entrega M — autoría y operación manual

Edición por API con revisión y fuente según variante P04, representaciones de Board/procedimiento/conocimiento, intake y autoría explícita, diff/evidencia, handoff de cierre externo y manual verificado. WS43 publica entradas del desk real después del corpus y gate manual. Captura/ack/advance no tienen por qué esperar al editor; cada acción espera solo su contrato y delta. No commits automáticos ni closeout HTTP. Privilegios y efectos definidos en WS12.

## Entrega E — Scion opcional

Registro por intento, mensajes/resultados/decisiones, API de dispatch/reply autorizada y UI de intervención con aprobación humana. No replica tablas internas ni sustituye broker. Mensajería distribuida/A2A y despliegue multiHub no se implementan aquí.

## Extensiones incluidas pero independientes

WS29: Changes/impacto comprobable del store actual. WS39: integrar capacidades existentes Schema/edición de clases. Tienen pruebas y estado propios; no se etiquetan disponibles por estar planeadas ni bloquean primer lector/manual básico.

## Fuera de alcance de esta línea base

Migrar a Kimun; desplegar infraestructura distribuida; editar otros repos remotos; colaboración multiusuario; rebases/deshacer/revert destructivos desde UI; renombrar/mover con reescritura global; editar binarios/adjuntos; exportar/publicar sitios; empaquetado offline/vendorizar todas las dependencias CDN. Para esas operaciones: lectura/diagnóstico y referencia a herramienta existente, o indicar no soportado. Abrir adjuntos referenciados solo con resolución segura si API lo soporta; no prometer editor binario.

Arranque: WS40 genera el ejemplo e instrucciones de instalación/apertura; WS16 las prueba y WS17 aporta índices; proyecto sin desk recibe orientación y handoff a init CLI. Crear desks desde UI no es requisito. El fallo CDN observado es parte de WS15 y una dependencia explícita del despliegue actual, no se oculta como offline funcional.

## Reglas comunes de ejecución

Si al llegar a un nodo falta un contrato, API, dato o permiso que debía producir una dependencia: detenerse, registrar el hueco con repo dueño y no crear sustituto. La operación queda no disponible.

Las pruebas de implementación usan un store temporal real creado en el test o el corpus WS40 cuando ya exista. Las validaciones humanas usan el corpus WS40.

Una dependencia transitiva cuenta como prerrequisito aunque no figure en `depends_on` directo: WS11 y WS12 ya llevan detrás WS02–WS10 según el DAG.

El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide.

## Regla para cambios de alcance

Antes de promover un nodo: revisar tareas/Board del repo receptor y reconciliacion.md. La implementación puede vincular/sustituir alcance en la tarea receptora aceptada; este plan no crea una segunda ejecución concurrente. Si cambia contrato, agregar nodo atómico en dag.yaml y volver a validar/revisar las dependencias afectadas. No dar por confirmado el estado de un repo usando solo un hash viejo.

FILE:desk/drawer/plans/workspace-documental/decisiones.md
# Registro de decisiones — propuestas, pendientes de confirmación WS07

Estado general: PENDING_OWNER. Actor requerido: solicitante humano de esta sesión o persona que designe explícitamente. No consta aún decisión humana sobre las propuestas de esta tabla. Una revisión del concilio no la sustituye.

| ID | Pregunta | Propuesta acotada para esta entrega | Alternativa y efecto |
|---|---|---|---|
| P01 | Host y unidad | Extender Mindmap activo; designar con identidad a responsables graph_ui/sldb/spec2viz y operador del ramal Scion (sin autorizar ejecución); foco documental conserva identidad al ver Graph/Code. Otros nodos muestran soporte y vuelven al documento cuando exista. | Otro host requiere revisar WS06/13; no copiar producto distinto en paralelo. |
| P02 | Backend | Usar sldb/pron y operaciones Deskops actualmente verificadas. Kimun solo referencia, sin migración ni dependencias M1/M2/C2 en este DAG. | Migración exige decisión y DAG propio del repo dueño; no requisito silencioso. |
| P03 | Escritura y coordinador | Baseline editable solo en desk en modo manual exclusivo; con coordinador escritor activo, UI read-only/handoff hasta canal autorizado real. No fingir lock compartido con CLI. | Canal único coordinador puede añadirse con contrato/API/validación; hoy no se supone disponible. |
| P04 | Fuente y campos | Texto fuente siempre legible; editar fuente solo tras API reversible probada y guardas de campos workflow. Guardado payload no equivale a guardado raw-source. | Fuente solo lectura permite entregar lector antes, pero WS21 no cierra como edición completa. |
| P05 | Git y cierre | Guardar no commitea automáticamente. Lectura diff/historial; closeout commit fuera de HTTP, con handoff visible y refresco que verifica resultado. | Commit desde UI requiere autoridad/transacción y tarea de diseño específica; fuera del baseline. |
| P06 | Promoción desde drawer | Preservar commits de creación/promoción exigidos por ritual. Solo ofrecer mutación cuando WS12 documente canal completo y efectos; de otro modo preparar/handoff manual, no anunciar promoción terminada. | El humano puede autorizar workflow diferente mediante cambio explícito de regla; no lo hace un renderer. |
| P07 | Contexto y federación | Foco e historial por workspace local; preferencias en estado local. Multidesk inicialmente lectura y rutas/aliases explícitos, sin mutación cruzada ni copiar documentos. | Colaboración multiusuario y escritura interdesk son posteriores, con permisos/identidad acordados. |
| P09 | Ubicación de entradas reales | Extender desk/README.md y un mapa authored del ecosistema según WS11, reutilizando registry; publicar en deskops por WS43 después del ejemplo. | Otras ubicaciones/proyectos requieren definición y tarea del repo dueño; no basta solo el demo. |
| P08 | Uso humano y alcance | Proyecto Taller temporal, participante humano y presupuestos propuestos en validacion-humana.md. | El solicitante puede designar otro ejemplo/umbrales antes de WS16. |

## Cómo se resuelve un registro

Añadir a cada Pxx: estado accepted/rejected/revised, actor humano, fecha, referencia a respuesta/acta verificable, alternativa elegida y nodos afectados. G_PRODUCT pasa solo con P01/P02/P07/P08/P09 resueltos y P04 registrado como source_mode; G_WRITE_POLICY pasa solo con principios P03–P06 aprobados; G_WRITE_CONTRACT pasa después de WS12 con la política concreta por campos/operaciones verificada. Un cambio posterior invalida los gates afectados y obliga a regenerar/revisar el plan; nunca se actualiza un estado por inferencia del agente.

## Control de huecos

Si una decisión revela una API inexistente, WS11/12 deben registrar el hueco, repo dueño y dependencia nueva para el delta afectado. No crear workaround deskops ni habilitar una operación falsa. Las decisiones pendientes son trabajo planificado; no son aprobación para código.


P04 se refleja en parameters.source_mode de dag.yaml: pending bloquea WS20/21; editable habilita WS20 y exige G_SOURCE para WS21; read_only excluye WS20 de la entrega y usa la variante explícita de WS21. WS30/31 comprueban y publican exactamente el modo elegido, no una promesa de edición fuente que no existe. El responsable de cada repo receptor debe quedar identificado en P01, con aceptación de lectura/escritura registrada en WS11/12. WS06 solo propone correspondencias.

WS07 debe designar también al operador Scion de WS44; WS05 puede cerrar inventario sin acceso, pero WS44 permanece bloqueada hasta comprobar API pública y producir G_SCION para WS32.

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:PK02
id: PK02
title: Decisiones y contratos
scope: Decisiones humanas, user-flows, catálogo, índice de manual y contratos de navegación
  y operaciones.
acceptance: 'Agrupación de revisión, no dependencia operativa. Verdadera cuando cada
  hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito
  con responsable. Revisión vigente: `context_review` del hijo en dag.yaml cuyo hash
  de input y de contrato coinciden con los actuales y que tiene disposition.md guardada
  en el intento correspondiente a esos hashes; lo comprueba `python desk/drawer/plans/workspace-documental/context_review.py
  status` desde la raíz de deskops. Bloqueo explícito: `context_review.status=blocked`
  por causa externa (ajena al encargo del propio hijo), que la sesión de coordinación
  que ejecuta context_review.py registra con responsable (actor o repo que debe resolverla)
  y dependencia en esa disposition.md. Un hijo con ambigüedad de su propio encargo
  sin resolver queda pending o blocked por esa causa, y entonces esta aceptación no
  es verdadera; un bloqueo externo con responsable sí la admite.'
children:
- WS07
- WS08
- WS09
- WS10
- WS11
- WS12

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS07
id: WS07
title: Resolver decisiones de producto y escritura
kind: planning
owner_repo: deskops
node_role: delivery
scope: El humano dueño del producto confirma o corrige P01–P09 de decisiones.md, leyendo
  validacion-humana.md para P08, y `baseline_proposal` de dag.yaml (propuesta de línea
  base, no aprobación del plan completo); registrar alternativas, fecha y evidencia
  de cada decisión. Designar con identidad explícita a responsable de graph_ui, sldb
  y spec2viz para aceptar deltas; se puede designar al solicitante, no suponerlo.
  Registrar source_mode=editable o read_only en parámetros del DAG y reconsiderar
  alcance según P04 dentro de las variantes ya declaradas en dag.yaml, sin editar
  nodos aquí; un cambio de nodos sigue la regla de alcance.md. Designar explícitamente
  también al operador responsable del ramal Scion y registrar qué acceso read-only
  tiene, con identidad registrada por el solicitante en P01; no requiere configurar/ejecutar
  Scion ni concede permiso G_EXEC.
acceptance: No inventar aprobación. Gates G_PRODUCT y G_WRITE_POLICY solo pasan por
  registro explícito. Redacción de alternativas puede avanzar mientras esperan. No
  cerrar sin registro de designación de responsables graph_ui/sldb/spec2viz y operador
  Scion, con su acceso read-only, en P01 (puede ser el propio solicitante si lo confirma),
  con actor humano/fecha; P01 no equivale a autorización de ejecución.
output_scope: decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml
depends_on:
- WS06
requires: []

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
  de auditoria/ui.md (WS04); error = fallo visible esperado para esa fila.
output_scope: borradores/vistas.md
depends_on:
- WS07
- WS10
- WS08
requires:
- G_PRODUCT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS10
id: WS10
title: Precisar índice y convención del manual
kind: planning
owner_repo: deskops
node_role: delivery
scope: Índice y capítulos conceptuales, ejemplo fijo y etiqueta de disponibilidad;
  reutilizar manual CLI. Usa auditoria WS02–WS04; WS03/WS04 llegan de forma transitiva
  por WS06/WS07.
acceptance: Definiciones verificables de disponible/propuesto/bloqueado; no escribir
  pasos ni capturas ficticios.
output_scope: borradores/manual.md
depends_on:
- WS02
- WS07
requires:
- G_PRODUCT

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
acceptance: Resolver cada hueco como instancia/vínculo/consulta/API/renderer; si falta
  API abrir dependencia acotada del repo dueño antes de code. Sin migración Kimun
  implícita. Para cerrar, obtener aceptación del delta lector en graph_ui y de ViewDoc
  en spec2viz por responsable designado en WS07; si no hay recepción, el contrato
  queda pendiente, no se publica como cerrado. El acta de G_UI_READ enumera sus scope_nodes,
  incluidos corpus WS40 y multidesk WS41; el acta de G_SPEC_VIEW enumera los suyos,
  para no dejar deltas sin recepción.
output_scope: contratos/navegacion.md; actas de aceptación de G_UI_READ y G_SPEC_VIEW
  en el repo receptor
depends_on:
- WS09
- WS08
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
  dueño, no se diseña uno aquí.
acceptance: 'G_WRITE_POLICY verificado; registrar capability exacta (operación, canal,
  efectos) para cada mutación o lectura Git que usen WS19, WS20, WS21, WS25, WS26,
  WS27, WS28, WS32, WS34, WS36, WS39 y WS42. No asumir lock UI protege escritores
  CLI. Toda operación sin contrato queda no disponible. Requiere principios ya aprobados
  por humano en WS07 (G_WRITE_POLICY); WS12 produce la whitelist final. Contrato para
  campos/knowledge/intake puede cerrar sin esperar closeout: operaciones de autoría
  de tareas/cierre quedan bloqueadas por G_CLOSEOUT hasta evidencia; no se las etiqueta
  disponibles. Aceptar el delta de escritura (operaciones de la whitelist sobre los
  scope_nodes de G_UI_WRITE) por graph_ui antes de cerrar; aceptar delta en sldb solo
  si source_mode=editable. Tras WS07 source_mode ya no vale pending, porque G_PRODUCT
  exige registrarlo. Con read_only, G_SLDB_WRITE no es prerrequisito ni se anuncia
  como aprobado. La verificación del contrato clasifica APIs como existentes/comprobadas
  o faltantes, no exige implementar WS20 para cerrar WS12: la capacidad raw-source
  faltante se especifica como requisito (operación y efectos) y queda gated por G_SOURCE;
  su diseño e implementación pertenecen a WS20.'
output_scope: contratos/operaciones.md
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS06
id: WS06
title: Proponer correspondencia de alcance con repos dueños
kind: planning
owner_repo: deskops
node_role: delivery
scope: 'Una matriz por implementación: ya cubierto (capacidad observable en código
  implementado, con referencia), extender ticket existente (incluido un draft del
  Board) o nuevo delta. La fila Scion RunDoc/cierre de reconciliacion.md conserva
  el tratamiento ya registrado (descomposición en WS32/33) sin requerir WS05. Registrar
  en reconciliacion.md la atomización propuesta, sin notificar, despachar ni modificar
  el Board de graph_ui; el responsable receptor se designa en WS07 y acepta en WS11/12.'
acceptance: Matriz con una fila por delta o capacidad propuesta, agrupada por repo
  dueño, no por nodo del DAG; correspondencia ticket/delta y responsable por designar;
  no produce gates de aceptación ni aprueba deltas que aún no están definidos. WS11/12
  obtienen aceptación específica por repo receptor.
output_scope: reconciliacion.md
depends_on:
- WS02
- WS03
- WS04
requires: []

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS02
id: WS02
title: Inventariar superficies y operaciones Deskops
kind: planning
owner_repo: deskops
node_role: delivery
scope: Superficie = cada archivo, comando público o modelo registrado concreto de
  las categorías enumeradas; una fila por superficie. Modelos y Markdown no modelado;
  inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs; firmas
  públicas, efectos Git y cierre. Modelado = tiene modelo registrado en el store (`sldb
  models list`); Markdown no modelado = el resto. Firmas públicas = comandos CLI de
  deskops y métodos de DeskopsOperations. Cierre = `deskops closeout verify|commit`.
acceptance: Cada fila incluye ubicación (archivo o símbolo de código) y la operación
  expuesta (comando o método que la lee o muta, o «dato pasivo»), con estado comprobado;
  no inferir modelo por carpeta. Estado comprobado = lectura citada con archivo:línea
  o salida de comando de solo lectura; lo no comprobado se marca «no comprobado» con
  causa (ausente, inaccesible o no encontrado).
output_scope: auditoria/deskops.md
depends_on:
- WS01
requires: []

FILE:instruccion
Revisa el nodo PK02 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

