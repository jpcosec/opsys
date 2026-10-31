FILE:desk/drawer/plans/workspace-documental/context-review-guide.md
# Guía breve para revisar un nodo del plan

Esta guía va en todo input de context review. Deriva de brief.md y alcance.md; no añade requisitos de producto.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende bien como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el producto es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de IDs, aristas y gates. Las candidatas no son tareas activas: ninguna tiene ejecución autorizada.
- ROOT y PK son agrupaciones de revisión, no dependencias ni entregables. Un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una flecha significa prerrequisito -> dependiente.
- Un gate pendiente es intencional. No es defecto que aún no esté satisfecho.
- Las propuestas Pxx de decisiones.md no son decisiones humanas. No las des por aprobadas ni pidas resolverlas aquí.
- Una dependencia futura que debe producir un contrato, API o inventario no es ambigüedad si el encargo nombra quién lo produce y qué hacer si falta.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance.

No cuentan: decisiones Pxx pendientes con actor, detalles que el nodo delega a su promoción (archivos exactos, TaskDoc, pills), trabajo de nodos dependientes o funciones excluidas en alcance.md.

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
- **Proyección de grafo ViewDoc**: contrato existente de spec2viz para nodos por modelo/predicado, relaciones, dirección y notación/layout. No define por sí mismo formularios, tabs o tableros.
- **Consulta**: selección derivada evaluada por infraestructura; no un inventario authored duplicado. No se promete modelo de consulta guardada sin prueba de WS03.
- **Foco**: elemento seleccionado por una persona, compartido entre representaciones del mismo documento; no selección compartida entre usuarios.
- **Historia de navegación**: abrir/volver y documentos abiertos. Distinta de historial Git o decisiones de workflow.
- **Disposición**: pestañas, divisiones y preferencias locales. No datos de dominio ni registro compartido por defecto.

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#parameters
source_mode:
  value: pending
  allowed:
  - pending
  - editable
  - read_only
  decided_by: P04/WS07
  evidence: decisiones.md con actor humano; sincronizar valor al resolver P04

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
  y closeout fuera del servidor UI.
acceptance: 'G_WRITE_POLICY verificado; registrar capability exacta para cada acción.
  No asumir lock UI protege escritores CLI. Toda operación sin contrato queda no disponible.
  WS07 ya aprobó principios, WS12 produce whitelist final. Contrato para campos/knowledge/intake
  puede cerrar sin esperar closeout: operaciones de autoría/cierre quedan bloqueadas
  por G_CLOSEOUT hasta evidencia; no se las etiqueta disponibles. Aceptar deltas de
  escritura por graph_ui antes de cerrar; aceptar delta en sldb solo si source_mode=editable.
  Con read_only, G_SLDB_WRITE no es prerrequisito ni se anuncia como aprobado. La
  verificación del contrato clasifica APIs como existentes/comprobadas o faltantes,
  no exige implementar WS20 para cerrar WS12: la capacidad raw-source faltante se
  diseña y queda gated por G_SOURCE.'
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
  y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos.
acceptance: Resolver cada hueco como instancia/vínculo/consulta/API/renderer; si falta
  API abrir dependencia acotada del repo dueño antes de code. Sin migración Kimun
  implícita. Para cerrar, obtener aceptación del delta lector en graph_ui y de ViewDoc
  en spec2viz por responsable designado en WS07; si no hay recepción, el contrato
  queda pendiente, no se publica como cerrado. El acta receptora enumera scope_nodes
  de G_UI_READ/G_SPEC_VIEW, incluidos corpus WS40 y multidesk WS41, para no dejar
  deltas sin recepción.
output_scope: contratos/navegacion.md
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
scope: Mapear UF a operaciones de WS02/03/04; cubrir manual, captura, revisión, cambios,
  arranque, multidesk, schemas y modo degradado. UF02 responder significa dentro del
  desk/contexto autorizado local; ack local disponible según contrato. UF08 es lectura;
  envío interdesk fuera de baseline, sin excepción implícita a P07.
acceptance: Cada UF tiene entrada/salida, operación, error, nodo y gate humano; no
  prometer función fuera de alcance.
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
scope: Delta sobre ticket draft de edición; reutilizar editores y API, revisión esperada
  y conflicto visible; workflow-protected fields no editables por este canal. Incluir
  alta/baja de relaciones permitidas por contrato, usando API real y before-image;
  no crear semántica de relaciones en componente.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS19.1, WS19.2'
depends_on:
- WS12
- WS16
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
scope: Edición de campos reutilizando editores y API, con revisión esperada y conflicto
  visible; workflow-protected fields no editables por este canal. Delta sobre ticket
  draft de edición.
acceptance: Guardar/recargar confirma dato real; una escritura obsoleta no pierde
  texto local. Mutación restringida a desk en modo manual coordinado; otros modos
  read-only hasta contrato.
output_scope: frontends/mindmap/views/workspace/fields/; endpoints si aplica; tests/
depends_on:
- WS12
- WS16
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
  no crear semántica de relaciones en el componente.
acceptance: Alta y baja persisten y se confirman tras recargar; una relación no permitida
  o una revisión obsoleta se rechaza con error visible.
output_scope: frontends/mindmap/views/workspace/relations/; endpoints si aplica; tests/
depends_on:
- WS12
- WS16
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS20
id: WS20
title: Probar o completar guardado fuente reversible
kind: implementation
owner_repo: sldb
node_role: delivery
scope: Primero verificar capacidad existente. Un documento raw-source se extrae/valida
  y guarda por API pública con revisión y preservación de campos protegidos; no sobrescribir
  Markdown desde browser.
acceptance: 'Si capacidad existe: evidencia de contrato suficiente, no código duplicado.
  Si falta: intake/tarea sldb propia y roundtrip, conflicto y recuperación reales
  antes de cerrar G_SOURCE.'
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
  permitidas por contrato; no confundir ack con aprobación.
acceptance: 'Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.
  Sus dependientes siguen dependiendo de este ID.'
output_scope: 'Agregado: salidas de WS25.1, WS25.2'
depends_on:
- WS12
- WS16
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
  permitidas por contrato; sin envío interdesk; no confundir ack con aprobación.
acceptance: Ack y respuesta local persisten tras recargar con origen visible; no crea
  tarea implícita ni cron de triage. Permisos del contrato aplicados.
output_scope: frontends/mindmap/views/workspace/inbox/; endpoints si aplica; tests/
depends_on:
- WS12
- WS16
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
scope: Captura interna de drawer/protoátomo mediante operaciones permitidas por contrato,
  sin exigir tarea.
acceptance: 'UF02: una captura persiste tras recargar con origen y sin tarea implícita.
  Permisos del contrato aplicados.'
output_scope: frontends/mindmap/views/workspace/capture/; endpoints si aplica; tests/
depends_on:
- WS12
- WS16
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
  respetar commits previos y estado real.
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
  de contexto/pills.
acceptance: UF04 sobre TaskDoc real; nunca editar status para avanzar. Si una operación
  Git no tiene contrato o dueño, la acción queda en handoff explícito y el gate humano
  no pasa hasta resolver.
output_scope: frontends/mindmap/views/workspace/authoring/; endpoints si aplica; tests/
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
  autorizado.
acceptance: Board real refleja el enrutamiento sin confundirlo con ejecución; el canal
  de promoción respeta commits previos y estado real.
output_scope: frontends/mindmap/views/workspace/routing/; endpoints si aplica; tests/
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
scope: Diff Git y artefactos de evidencia junto al encargo, historial read-only; diferenciar
  cambios de código de integridad del store.
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
scope: Diff Git e historial read-only junto al encargo; diferenciar cambios de código
  de integridad del store.
acceptance: Diff real acotado al repo y tarea (la asociación a intento se añade en
  WS35), sin execute/revert genérico.
output_scope: frontends/mindmap/views/workspace/diff/; endpoints si aplica; tests/
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
scope: Artefactos de evidencia junto al encargo, sin inventar CommentDoc antes de
  contrato.
acceptance: Mostrar declarada/encontrada/verificada y abrir su soporte; una evidencia
  ausente se ve como ausente.
output_scope: frontends/mindmap/views/workspace/evidence/; endpoints si aplica; tests/
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
scope: Verificar con autoridad Deskops, diagnosticar faltantes y ofrecer handoff explícito
  a closeout CLI/coordinador con evidencia. No commit/close desde HTTP en baseline.
acceptance: UF05 termina al confirmar resultado real del cierre externo y refrescar
  estado; comando o solicitud no equivalen a cierre. Sin terminal embebido genérico.
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
scope: 'Refinar ticket existente, sin segundo pipeline: intento no es slug, dispatch
  intent/confirmed separado, manifiesto/RunDoc/cierre consistentes e idempotentes.'
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
scope: 'Refinar ticket existente, sin segundo pipeline: intento no es slug; dispatch
  intent y confirmed separados.'
acceptance: Dos intentos del mismo agente y un dispatch fallido conservan identidades
  distintas; schema mediante SLDB.
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
scope: Manifiesto, RunDoc y cierre consistentes e idempotentes sobre el intento correcto.
acceptance: G_CLOSEOUT pasa; una finalización repetida conserva identidad y evidencia
  sin duplicar.
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
  intento, timeout/errores y autoridad del coordinador.
acceptance: G_SCION/G_EXEC pasan; agente real demuestra aceptación y fallo. No shell
  arbitrario ni duplicar transporte.
output_scope: runtime/; cli/commands/runtime.py o API definida; tests/
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
  correcto. No mandar mensajes en la tarea de planificación.
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
  usar draft/validate/promote del dueño. No reimplementar modelos.
acceptance: UF09 inspección y mutación en store temporal; confirmar efectos de contrato
  y errores; no habilitar promover si API/autoridad falta. Extensión posterior al
  lector básico. Guardar acta de prueba humana en graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md
  con participante designado y resultado; G_HUMAN_MODEL debe pasar antes de marcar
  capítulo disponible.
output_scope: shell/dialogs.js; views/models/; tests/
depends_on:
- WS12
- WS16
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
  con confirmación de alcance y procedencia; materializaciones se inspeccionan/validan,
  no se generan destinos arbitrarios.
acceptance: UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales;
  cada capability no soportada se declara no disponible y bloquea ese escenario, no
  se simula. Cubierto por WS30.
output_scope: frontends/mindmap/views/workspace/knowledge/; endpoints whitelist; tests/
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
  state: pending
  resolver: WS07
  evidence: P03–P06 resueltos por humano; principios y límites, no whitelist final
    producida por WS12
  produced_by: WS07
G_WRITE_CONTRACT:
  title: Contrato técnico de operaciones verificado
  state: pending
  resolver: WS12
  produced_by: WS12
  evidence: whitelist por campo/operación, canal/actor, API/revisión/Git y efectos
    comprobados; revisión por responsable identificado
G_UI_WRITE:
  title: Deltas de mutación aceptados en graph_ui
  state: pending
  resolver: WS12
  produced_by: WS12
  evidence: Acta de aceptación del delta definido por contrato, con identidad/fecha
    del responsable graph_ui designado explícitamente por el solicitante; task receptora
    y no solapamiento confirmados. No basta una propuesta.
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
G_SLDB_WRITE:
  title: Alcance fuente aceptado en sldb
  state: pending
  resolver: WS12
  produced_by: WS12
  evidence: Acta de aceptación del delta definido por contrato, con identidad/fecha
    del responsable sldb designado explícitamente por el solicitante; task receptora
    y no solapamiento confirmados. No basta una propuesta.
  scope_nodes:
  - WS20

FILE:instruccion
Revisa el nodo WS12 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

