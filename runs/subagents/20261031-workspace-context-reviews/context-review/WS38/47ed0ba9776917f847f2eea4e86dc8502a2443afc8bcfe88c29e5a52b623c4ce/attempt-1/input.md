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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS38
id: WS38
title: Publicar capítulos verificados de delegación
status: candidate
kind: documentation
depends_on:
- WS37
- WS31
requires:
- G_HUMAN_DELEGATE
owner_repo: deskops
output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados
scope: Añadir al manual operación de delegación y revisión trazable tal como quedó
  en WS37.
acceptance: Cada paso remite al acta de WS37 y a operaciones reales; los fallos registrados
  en esa acta se documentan; se indica que G_EXEC es necesario para operar.
estimate: S
task_file: desk/drawer/tasks/workspace-documental/task-ws38.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: deskops:repository_root/
node_role: delivery

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS37
id: WS37
title: Validar delegación con agente real
kind: validation
owner_repo: graph_ui
node_role: delivery
scope: 'UF06 real: pregunta/intervención/corrección/evidencia/decisión y cierre por
  el handoff de WS28, con actor humano.'
acceptance: G_SCION/G_EXEC y protocolo de validacion-humana.md (guion, acta en runs/subagents/workspace-documental-acceptance/delegacion/);
  no sustituir integración por mocks ni completed por aprobación. No bloquea WS31.
output_scope: runs/subagents/workspace-documental-acceptance/delegacion/
depends_on:
- WS36
- WS30
requires:
- G_EXEC
- G_SCION

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS31
id: WS31
title: Publicar manual documental básico probado
kind: documentation
owner_repo: deskops
node_role: delivery
scope: Publicar navegación, edición, captura, trabajo manual y revisión demostradas;
  incorporar el índice de borradores/manual.md, capturas y limitaciones a docs/workspace-user-manual.md.
acceptance: Cada instrucción remite al acta de WS30 o al acta de publicación de WS43
  de la versión publicada; un átomo por acuerdo durable ya aceptado por humano en
  decisiones.md y por cada contrato en contratos/ (navegacion.md, operaciones.md u
  otros de WS11/WS12); las propuestas Pxx pendientes no se atomizan; etiquetas, links
  y atom->doc verificados. Scion se incluye solo como capítulo marcado propuesto hasta
  WS38. Para capítulos que mencionen personalización o impacto, comprobar G_HUMAN_MODEL/WS29
  o mantener etiqueta propuesta; no bloquear manual básico por esos extras.
output_scope: docs/workspace-user-manual.md; docs/assets/workspace-user-manual/; desk/atoms/
  vinculados
depends_on:
- WS30
- WS10
- WS43
requires:
- G_HUMAN_MANUAL

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_HUMAN_DELEGATE:
  title: Persona aprueba delegación
  state: pending
  resolver: WS37
  evidence: graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md;
    actor humano/versión/guion/resultado y soportes. Guardar en repo dueño, no en
    el paquete de plan deskops.
  produced_by: WS37
  evidence_ref:
    repo: graph_ui
    path: runs/subagents/workspace-documental-acceptance/delegacion/acta.md
G_EXEC:
  title: Humano autoriza ejecución y comunicaciones del escenario
  state: pending
  resolver: external
  evidence: 'deskops:desk/drawer/plans/workspace-documental/autorizaciones/scion.md:
    permiso explícito del solicitante/designee para agente/proyecto/acciones/alcance/sesión.
    Plan/review no autoriza ejecución.'

FILE:instruccion
Revisa el nodo WS38 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

