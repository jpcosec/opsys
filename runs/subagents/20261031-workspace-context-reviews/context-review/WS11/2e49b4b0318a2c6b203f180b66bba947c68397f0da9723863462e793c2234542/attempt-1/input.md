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
output_scope: contratos/navegacion.md; actas de aceptación de G_UI_READ y G_SPEC_VIEW
  en el repo receptor
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
  de auditoria/ui.md (WS04); error = fallo visible esperado para esa fila.
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
  hueco, sin inventarla.
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
scope: 'Implementación o delta conciliado sobre ticket workspace en draft: documento/fuente
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
  no requerir índices nuevos. Implementación o delta conciliado sobre el ticket workspace
  en draft, según acta WS11.
acceptance: 'Markdown sin modelo legible; el panel de contexto muestra identidad,
  las relaciones que declare el contrato WS11 y la ruta de origen reales; seguir un
  enlace y alternar entre texto/graph/code, en las representaciones que el catálogo
  WS09 (borradores/vistas.md) y el contrato WS11 declaren soportadas, preserva origen.
  La selección por documento/nodo fija el foco del documento abierto: seleccionar
  en Code, texto o graph actualiza ese foco y las demás representaciones del mismo
  documento lo comparten, sin abrir otra copia. No depender de conocer un ID; no crear
  otro workspace independiente. Si el acta de WS11 eligió integrar el ticket draft,
  su cierre/evidencia sustituye este delta; no suponer una base workspace ya implementada.'
output_scope: frontends/mindmap/views/workspace/document/; rutas de lectura definidas
  por el contrato WS11; tests/
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
  prueba, aparece sin cambiar código.
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
  estos índices nuevos; WS30 sí los integra.'
acceptance: Tras regenerar corpus WS40 con ejemplo/nav/, recorrer links Markdown sin
  UI; source versionado y destino temporal no son registros independientes. Verificar
  al regenerar que cada plantilla resuelve el root/store de procedencia de los dos
  desks del manifiesto WS40; no duplicar el registry de deskops.
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
acceptance: Vista portable (el mismo ViewDoc sin código específico del host) renderiza
  sobre un store real la selección declarada, coincide con ella y el ViewDoc documenta
  qué selecciona; tareas receptoras en spec2viz se promueven por dueño. Gate receptor
  G_SPEC_VIEW requerido; no modificar su repo desde este plan.
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
  state: pending
  resolver: WS07
  evidence: decisiones.md; cada decision requiere actor/fecha/resultado; no se satisface
    por archivo presente; P01 debe incluir responsables de cada repo receptor y operador
    Scion identificados por el solicitante, con actor/fecha; no se satisface por nota
    de intención.
  produced_by: WS07
G_UI_READ:
  title: Deltas de lectura aceptados en graph_ui
  state: pending
  resolver: WS11
  produced_by: WS11
  evidence: Acta de aceptación del delta definido por contrato, con identidad/fecha
    del responsable graph_ui designado explícitamente por el solicitante; task receptora
    y no solapamiento confirmados. No basta una propuesta.
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
G_SPEC_VIEW:
  title: Alcance de proyecciones aceptado en spec2viz
  state: pending
  resolver: WS11
  produced_by: WS11
  evidence: Acta de aceptación del delta definido por contrato, con identidad/fecha
    del responsable spec2viz designado explícitamente por el solicitante; task receptora
    y no solapamiento confirmados. No basta una propuesta.
  scope_nodes:
  - WS18

FILE:instruccion
Revisa el nodo WS11 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

