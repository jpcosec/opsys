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
- **Composición**: representación que reúne contenido de varios documentos; cada edición va al documento dueño de ese contenido.
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

FILE:desk/drawer/plans/workspace-documental/borradores/vision.md
# Visión del workspace documental

Estado: borrador basado en brief.md; contrato por reconciliar en WS07. No describe funcionalidades ya entregadas ni reemplaza átomos/modelos del proyecto.

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

Dónde viven y qué contratos usan las entradas e índices; alcance real de ViewDoc; backend inicial vs ruta Kimun; representación y persistencia de selección/disposición; política de edición fuente y sincronización; autoridad y compatibilidad de acciones; latencia aceptable. Resolver con WS02–WS04/WS07/WS11/WS12, no improvisar al dibujar pantallas.

## Superficies adicionales y material existente

CrossroadDoc y namespaces organizan dominios; issues Markdown deliberadamente no modelados son legibles y operables mediante contratos existentes. FAQ y StepDoc son documentos de orientación/procedimiento. Brainstorm, Schema/edición de clases y Specs ya existen en Mindmap: inventariar y conservar/integrar sus capacidades explícitamente. Carpetas legacy (features/primitives/logbook/materializers) se clasifican por soporte actual en WS02, no por nombre ni como modelo obligatorio nuevo. KGDB no es otro servicio nuevo: la capa de grafo actual vive en sldb; no reintroducir el proyecto retirado.

Vocabulario normativo de este borrador: brief.md. Alcance: alcance.md. Propuestas de host, backend y escritura: decisiones.md (pendientes). El workspace puede enfocar nodos no documentales, pero el documento no pierde su identidad al cambiar de representación.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS01
id: WS01
title: Fijar brief y glosario autosuficientes
status: candidate
kind: planning
depends_on: []
requires: []
owner_repo: deskops
output_scope: brief.md
scope: Capturar acuerdos textuales y distinciones documento/nodo/vista/renderer/consulta/foco;
  ningún requisito remite a un chat invisible.
acceptance: Leer brief y reformular producto sin historial; acuerdos separados de
  propuestas.
estimate: S
task_file: desk/drawer/tasks/workspace-documental/task-ws01.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: deskops:desk/drawer/plans/workspace-documental/
node_role: delivery

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS02
id: WS02
title: Inventariar superficies y operaciones Deskops
kind: planning
owner_repo: deskops
node_role: delivery
scope: Modelos y Markdown no modelado; inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs;
  firmas públicas, efectos Git y cierre.
acceptance: Cada fila incluye archivo/código/operación y estado comprobado; no inferir
  modelo por carpeta.
output_scope: auditoria/deskops.md
depends_on:
- WS01
requires: []

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS03
id: WS03
title: Inventariar persistencia, consultas y notaciones
kind: planning
owner_repo: deskops
node_role: delivery
scope: 'Auditoría de solo lectura de sldb/pron/spec2viz: fuente/payload, conflictos
  y límites de locks, referencias, búsquedas y alcance real ViewDoc. Kimun solo referencia.'
acceptance: Una salida documental, sin cambios interrepo; distinguir API comprobada,
  ausencia y hueco.
output_scope: auditoria/infraestructura.md
depends_on:
- WS01
requires: []

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS04
id: WS04
title: Inventariar UI y reconciliar trabajo en curso
kind: planning
owner_repo: deskops
node_role: delivery
scope: Leer graph_ui Board, tareas y código actuales; mapear nodos de este plan a
  deltas existentes; identificar sesiones y solapamientos sin cambiar sus tareas.
acceptance: Cada tarea externa con path, estado observado, hash y alcance; reconciliar
  también SPEC externo y cualquier encargo aportado al ejecutar.
output_scope: auditoria/ui.md
depends_on:
- WS01
requires: []

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS05
id: WS05
title: Inventariar identidad y API Scion
kind: planning
owner_repo: deskops
node_role: delivery
scope: 'Leer runtime/templates/RunDoc y API pública de Scion; separar slug/agente/intento/dispatch/mensaje/conversación
  y permisos. Puede registrar observaciones de API ya disponibles sin crear un segundo
  recibo: solo el probe de WS44 es evidencia de G_SCION. Sin agentes/mensajes/config
  ni mostrar tokens. WS05 no produce G_SCION; el probe y sus reintentos son responsabilidad
  explícita de WS44, incluso si el inventario aporta observaciones.'
acceptance: No usar tablas internas como interfaz; señalar campos internos no expuestos
  y capacidades que requieren API real.
output_scope: auditoria/scion.md
depends_on:
- WS01
requires: []

FILE:instruccion
Revisa el nodo WS01 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

