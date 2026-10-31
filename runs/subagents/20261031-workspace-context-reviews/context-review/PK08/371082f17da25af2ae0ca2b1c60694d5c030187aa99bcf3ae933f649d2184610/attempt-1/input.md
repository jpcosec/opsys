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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:PK08
id: PK08
title: Ramal Scion opcional
scope: Probe, identidad de intento, trazabilidad, acciones, UI de delegación, validación
  real y capítulos.
acceptance: 'Agrupación de revisión, no dependencia operativa. Verdadera cuando cada
  hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito
  con responsable. Revisión vigente: `context_review` de cada hijo en dag.yaml con
  input y contrato actuales y disposición guardada, según `context_review.py status`.
  Bloqueo explícito: `context_review.status=blocked` con responsable y dependencia
  en su disposición.'
children:
- WS32
- WS33
- WS34
- WS35
- WS36
- WS37
- WS38
- WS44

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS33
id: WS33
title: Vincular mensajes, resultados y decisiones
kind: implementation
owner_repo: deskops
node_role: aggregate
children:
- WS33.1
- WS33.2
scope: Referencias Hub/proyecto/conversación/mensaje/intento y revisión humana explícita;
  dedup y procedencia. Backend documental, independiente de editor UI.
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS35
id: WS35
title: Mostrar ejecución y trazabilidad en workspace
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Lectura tarea-intento-conversación-resultados-decisión usando fuente dueña
  y referencias documentales.
acceptance: Intento correcto, enlaces origen, evidencia legible; completed no se traduce
  en aprobado/cerrado.
output_scope: frontends/mindmap/views/workspace/execution/; tests/
depends_on:
- WS33
- WS27
requires:
- G_SCION
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS36
id: WS36
title: Integrar delegación e intervención humanas
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Invocar solo adaptador autorizado para dispatch/reply y solicitud de decisión;
  revisión con actor/evidencia visible.
acceptance: Respuesta vinculada al intento y operación confirmada; ausencia de API/permisos
  visible. No autoaprobación ni simulación.
output_scope: frontends/mindmap/views/workspace/execution/; endpoints; tests/
depends_on:
- WS34
- WS35
requires:
- G_EXEC
- G_SCION
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS37
id: WS37
title: Validar delegación con agente real
kind: validation
owner_repo: graph_ui
node_role: delivery
scope: 'UF06 real: pregunta/intervención/corrección/evidencia/decisión y cierre vía
  autoridad, con actor humano.'
acceptance: G_SCION/G_EXEC y protocolo; no sustituir integración por mocks ni completed
  por aprobación. No bloquea WS31.
output_scope: runs/subagents/workspace-documental-acceptance/delegacion/
depends_on:
- WS36
- WS30
requires:
- G_EXEC
- G_SCION

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS38
id: WS38
title: Publicar capítulos verificados de delegación
kind: documentation
owner_repo: deskops
node_role: delivery
scope: Añadir instrucciones runtime y revisión trazable, con lo que funciona y fallos
  demostrados.
acceptance: Capturas y operaciones reales; mantención de contratos y autorización
  documentadas.
output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados
depends_on:
- WS37
- WS31
requires:
- G_HUMAN_DELEGATE

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS44
id: WS44
title: Comprobar y revalidar acceso público a Scion
kind: validation
owner_repo: deskops
node_role: delivery
scope: Responsable de instalación Scion, identificado por solicitante en WS07, realiza
  probe read-only de API con acceso ya autorizado; verifica capacidades/identidad
  necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar
  config o mostrar secretos. Puede repetir el probe si el inventario WS05 terminó
  sin acceso.
acceptance: G_SCION se satisface solo con respuesta pública real, identidad/fecha/capabilities
  y actor registrados. Si API o acceso no están, WS44 permanece bloqueada, no se cierra
  unverified ni se avanza WS32. Tras cambio de Hub/API/credencial, repetir y invalidar
  recibo previo.
output_scope: auditoria/scion-probe.md
depends_on:
- WS05
- WS07
requires:
- G_PRODUCT

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS12
id: WS12
title: Cerrar contrato de operaciones y escritura
kind: planning
owner_repo: deskops
node_role: delivery
scope: Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy
  coordinador, Git, workflow-protected fields, CAS/locks, fallos parciales, permisos
  y closeout fuera del servidor UI.
acceptance: 'G_WRITE_POLICY verificado; registrar capability exacta para cada acción.
  No asumir lock UI protege escritores CLI. Toda operación sin contrato queda no disponible.
  Requiere principios ya aprobados por humano en WS07 (G_WRITE_POLICY); WS12 produce
  la whitelist final. Contrato para campos/knowledge/intake puede cerrar sin esperar
  closeout: operaciones de autoría/cierre quedan bloqueadas por G_CLOSEOUT hasta evidencia;
  no se las etiqueta disponibles. Aceptar deltas de escritura por graph_ui antes de
  cerrar; aceptar delta en sldb solo si source_mode=editable. Tras WS07 source_mode
  ya no vale pending, porque G_PRODUCT exige registrarlo. Con read_only, G_SLDB_WRITE
  no es prerrequisito ni se anuncia como aprobado. La verificación del contrato clasifica
  APIs como existentes/comprobadas o faltantes, no exige implementar WS20 para cerrar
  WS12: la capacidad raw-source faltante se diseña y queda gated por G_SOURCE.'
output_scope: contratos/operaciones.md
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS30
id: WS30
title: Validar autoría y revisión manual completas
kind: validation
owner_repo: graph_ui
node_role: delivery
scope: Persona recorre UF02/03 edición/04/05; integra conocimiento y tarea en ejemplo;
  errores, teclado, dos ventanas y conflictos, con historial. Incluye explícitamente
  UF01 usando entradas authored WS17 materializadas por generador WS40, además de
  edición/operación; no limitarlo a búsqueda.
acceptance: Registro humano bajo protocolo; problemas implican tareas de corrección
  de la misma capa. No llamar ready a un flujo solo por tests.
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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS31
id: WS31
title: Publicar manual documental básico probado
kind: documentation
owner_repo: deskops
node_role: delivery
scope: Publicar navegación, edición, captura, trabajo manual y revisión demostradas;
  actualizar índice/capturas/limitaciones.
acceptance: Cada instrucción tiene evidencia vigente; etiquetas, links y atom->doc
  verificados. Scion solo capítulo marcado propuesto hasta WS38. Para capítulos que
  mencionen personalización o impacto, comprobar G_HUMAN_MODEL/WS29 o mantener etiqueta
  propuesta; no bloquear manual básico por esos extras.
output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados
depends_on:
- WS30
- WS10
- WS43
requires:
- G_HUMAN_MANUAL

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS07
id: WS07
title: Resolver decisiones de producto y escritura
kind: planning
owner_repo: deskops
node_role: delivery
scope: El humano dueño del producto confirma o corrige baseline, host, fuente/edición,
  escritura/Git/coordinador y cierre; registrar alternativas, fecha y evidencia de
  cada decisión. Designar con identidad explícita a responsable de graph_ui, sldb
  y spec2viz para aceptar deltas; se puede designar al solicitante, no suponerlo.
  Registrar source_mode=editable o read_only en parámetros del DAG y reconsiderar
  alcance según P04. Designar explícitamente también al operador responsable del ramal
  Scion, con identidad registrada por el solicitante en P01; no requiere configurar/ejecutar
  Scion ni concede permiso G_EXEC.
acceptance: No inventar aprobación. Gates G_PRODUCT y G_WRITE_POLICY solo pasan por
  registro explícito. Redacción de alternativas puede avanzar mientras esperan. No
  cerrar sin registro de designación de responsables graph_ui/sldb/spec2viz y operador
  Scion en P01 (puede ser el propio solicitante si lo confirma), con actor humano/fecha;
  P01 no equivale a autorización de ejecución.
output_scope: decisiones.md
depends_on:
- WS06
requires: []

FILE:instruccion
Revisa el nodo PK08 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

