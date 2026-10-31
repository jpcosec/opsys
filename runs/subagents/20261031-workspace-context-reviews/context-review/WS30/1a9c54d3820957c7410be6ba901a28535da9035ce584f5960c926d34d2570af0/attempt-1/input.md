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

FILE:desk/drawer/plans/workspace-documental/validacion-humana.md
# Protocolo de uso y evidencia

Propuesta pendiente de P08. Participante: solicitante humano de esta sesión o persona explícitamente designada. Agente de pruebas prepara entorno y observa; no firma como usuario humano ni convierte screenshots en aprobación.

## Ejemplo reproducible

Proyecto Taller bajo graph_ui:.tmp/workspace-documental-ejemplo/, con su propio git y desk/store temporal creado por CLI real. Incluir Board, task, pill, ritual/step, átomo/protoátomo/crossroad, FAQ, issue Markdown no modelado y una referencia intencionalmente rota. Segundo desk temporal para UF08 y tercer repo temporal sin desk para UF10. Todo dato de prueba debe generarse por contratos reales cuando aplique, no mocks que sustituyan la API; sin secretos/corpus ajeno. No probar mutaciones sobre este desk de desarrollo. WS40 es el productor único del generador versionado y de los dos desks temporales. WS17 aporta solo plantillas de navegación authored bajo ejemplo/nav/; WS40 las materializa si se suministran.

## Gates por rebanada

- WS16: UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque. Encontrar un concepto desde entrada/búsqueda, abrir soporte, volver y cambiar representación con identidad; diagnosticar link roto y backend ausente. Necesita corpus WS40 y lectura multidesk WS41; no necesita edición, índices nuevos, Scion ni Changes global.
- WS30: UF02, UF03 edición, UF04, UF05. Capturar sin tarea obligatoria, preparar autoría/contexto y evidencia, provocar conflicto en dos ventanas, comparar diff real y cerrar por handoff autorizado externo. WS17 integra entradas/index authored en esta prueba; WS42 cubre operaciones de conocimiento. WS30 usa variante source_mode de P04, con fuente editable o explícitamente read-only según decisión.
- WS37: UF06 con Scion real e intervención humana; requiere G_EXEC. No se ejecuta solo porque el DAG está revisado.
- WS39: UF09 modelos; validar su prueba específica antes de etiquetar capítulo de personalización como disponible.
- WS29: UF07 impacto avanzado; prueba propia de mutaciones y soporte. Su ausencia no bloquea manual básico, que debe decirlo.

Las mutaciones de baseline requieren G_HUMAN_READ; las representaciones solo lectura pueden construirse en paralelo sin que eso implique aceptación humana.

## Evidencia y aceptación

Guardar guion, versiones/commits, corpus, comandos públicos, timestamps y resultados técnicos; grabación o capturas del recorrido; observaciones, fallos y decisión explícita del participante. La persona debe poder completar el guion sin rutas memorizadas ni instrucciones verbales correctivas del agente. Registrar ayudas solicitadas. Un fallo de recorrido bloquea el gate correspondiente y abre tarea de corrección, no solo un cambio de umbral.

Presupuestos propuestos (P08 debe confirmarlos): lectura/navegación local caliente p95 <=2 s, guardado local <=3 s; primer arranque <=10 s en corpus de ejemplo. Si una operación excede 1 s, estado de progreso visible sin afirmar éxito; registrar error/timeout. Medir al menos 20 aperturas, 10 búsquedas (WS16 y WS30) y 10 guardados (solo WS30, porque WS16 no muta) sobre corpus y tamaño documentados; no extrapolar producción. Carga grande se reporta aparte.

## Qué significa disponible

Disponible y comprobado: versión/commit implementado, pruebas relevantes verdes, recorrido correspondiente aceptado y pasos del manual verificados en esa versión. Propuesto: intención/diseño sin esa evidencia. Bloqueado: dependencia o decisión identificada impide completarlo. Una tarea cerrada o un archivo existente no prueban por sí solos la etiqueta.

## Ubicación de evidencias

Las actas de WS16/30/37/39 viven en graph_ui:runs/subagents/workspace-documental-acceptance/{lectura,manual,delegacion,modelos}/acta.md (cada caso en su subdirectorio), no en el repo de planificación. WS43 guarda publicación real en deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md. Se pueden enlazar desde este plan; no copiarlas como segundo registro. output_base y output_scope de dag.yaml son autoridad de ubicación. El corpus tiene entrada mínima generada e instrucciones en WS40; WS16 no se reduce a buscar. WS30 prueba UF01 con las entradas enriquecidas de WS17.

La ubicación versionable no acredita que el acta esté versionada: incluirla explícitamente en el commit atómico de la tarea de validación del repo dueño. El recibo del gate debe enlazar ese commit y el blob de acta verificables; un archivo solo local o una captura no bastan.

FILE:desk/drawer/plans/workspace-documental/borradores/user-flows.md
# User-flows del workspace

Estado: borrador de intención. Los pasos son objetivos de UX, no afirmaciones de implementación. Cada flujo requiere mapa a operaciones reales y contrato de errores en WS08/WS07.

## UF01 — Entrar a un proyecto desconocido

Abrir entrada del ecosistema -> elegir proyecto -> leer entrada del desk -> seguir enlaces a conocimiento, trabajo y procedimientos -> abrir documentos al lado -> volver sin perder selección.

Aceptación: explicar propósito, superficies y trabajo actual sin rutas memorizadas. Ante proyecto no accesible o referencia rota, mostrar origen y conservar navegación.

## UF02 — Capturar y aclarar una intención

Capturar idea interna en drawer o protoátomo según naturaleza; entrada externa en inbox -> consultar contexto -> ack local o respuesta dentro del mismo desk autorizado (sin envío interdesk) -> dar forma al material -> conservar como conocimiento o autorizar una tarea completa desde el drawer.

Aceptación: no exigir tarea ni ejecución para conservar una idea. El paso a tarea conserva procedencia; no inventa campos para suplir falta de claridad. No confundir ack con aceptación del trabajo.

## UF03 — Trabajar conocimiento

Buscar por texto/campos/significado -> abrir átomo y fuentes -> comparar con relacionados -> editar, vincular, dividir o reunir mediante operaciones públicas -> consultar materializaciones, validar contratos soportados y leer impacto.

Aceptación: fuente y representación apuntan al mismo documento; las composiciones escriben al origen correcto. El conflicto conserva la edición del usuario y permite revisar; el conocimiento no exige lanzar agentes.

## UF04 — Preparar trabajo activo

Recuperar candidato -> definir objetivo, alcance, dependencias, validación y evidencia -> localizar contexto reusable -> vincular pills/átomos y rituales -> autorizar task -> enrutamiento en Board -> identificar capa lista sin solapamiento.

Aceptación: distinguir pendiente de activo y de listo para ejecutar. No convertir automáticamente un fragmento incompleto del drawer. La fase es dependencia operativa, no categoría de negocio.

## UF05 — Ejecutar manualmente y revisar

Abrir tarea con contexto y procedimiento -> hacer trabajo -> reunir cambios/evidencia -> comparar con contrato -> pedir corrección o completar obligaciones -> cierre vía autoridad Deskops -> revisar conocimiento durable y fase.

Aceptación: ninguna acción usa edición arbitraria de status para saltarse gates. Distinguir declarado, encontrado y verificado. Reabrir enlaces durante revisión no pierde el encargo.

## UF06 — Delegar e intervenir

Preparar bundle -> registrar intento y dispatch confirmado -> seguir ejecución -> recibir pregunta con referencias -> responder/decidir -> consultar resultado y evidencia -> revisar/corregir -> cerrar mediante workflow.

Aceptación: cada mensaje/resultado corresponde al intento correcto; completado por agente no implica aprobado. Requiere ramal Scion real y no bloquea UF01–UF05.

## UF07 — Diagnosticar y mantener

Abrir diagnóstico -> identificar documento/ancla/relación afectada y causa -> inspeccionar soporte -> corregir o registrar trabajo -> reevaluar -> conservar procedencia.

Aceptación: se distingue error, conflicto, cambio y pérdida de soporte. Las operaciones de reparación muestran alcance; no recrean silenciosamente evidencia ausente.

## UF08 — Cambiar de proyecto

Seguir referencia de otro desk -> resolver identidad y contexto de store -> leer destino -> volver (envío interdesk queda fuera de baseline) -> conservar proyecto origen y destino.

Aceptación: no escribir en otro desk por confusión de cwd ni copiar documentos ajenos para aparentar navegación federada.

## UF09 — Inspeccionar y cambiar un contrato de modelo

Desde un documento -> abrir Schema/clase origen -> inspeccionar campos/referencias/template -> editar draft por APIs existentes -> validar -> promover solo con autoridad y evidencia -> diagnosticar impacto. No editar modelos por payload libre ni prometer soporte no disponible. WS39 implementa el delta y valida este flujo por separado.

## UF10 — Arranque y ausencia de desk

Seguir instrucciones reproducibles de instalación/arranque -> abrir ejemplo Taller -> si no hay desk, mostrar orientación e invocación init CLI con destino explícito -> refrescar tras resultado real. No ejecutar inicialización por un GET ni mutar el proyecto equivocado.

## Precisiones de revisión

UF04/05 tienen handoff a Git/closeout externo; no se promete cierre HTTP. UF06 requiere WS34/36 para acciones, no solo lectura de mensajes. UF07 reparaciones se hacen por operaciones existentes documentadas, no un botón universal. UF08 inicialmente read-only; una mutación interdesk no es parte implícita de navegar. Captura/archivo no modelado no debe tratarse como corrupción. Matriz de aceptación, nodos y gates: ../cobertura.md y ../validacion-humana.md. Los pasos de intención no acreditan capacidades implementadas.

UF03: WS19 cubre campos y relaciones; WS42 cubre split/merge/tipado existentes. UF04: WS26 incluye enrutamiento y capa lista. UF08 baseline es solo lectura entre desks vía WS41; no se promete enviar ni mutar destino. UF10 usa corpus de WS40. Los gates de uso siguen validacion-humana.md, no el simple cierre de una tarea de código.

UF03 no promete generar destinos arbitrarios desde una materialización: la entrega soporta inspección/procedencia y operaciones existentes comprobadas. Generación nueva de docs/diagramas exige su contrato del repo dueño. WS43 publica navegación real tras validar el ejemplo; no basta considerar el corpus como ecosistema final.

FILE:desk/drawer/plans/workspace-documental/dag.yaml#node:WS30
id: WS30
title: Validar autoría y revisión manual completas
status: candidate
kind: validation
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
owner_repo: graph_ui
output_scope: runs/subagents/workspace-documental-acceptance/manual/
scope: Persona recorre UF02/03 edición/04/05; integra conocimiento y tarea en ejemplo;
  los escenarios de error, conflicto en dos ventanas y navegación por teclado del
  guion de WS08 y validacion-humana.md. Incluye explícitamente UF01 usando entradas
  authored WS17 materializadas por generador WS40, además de edición/operación; no
  limitarlo a búsqueda.
acceptance: Registro humano bajo protocolo; un fallo de guion bloquea el gate y abre
  tarea en el nodo que lo causó; una observación solo se registra. No llamar ready
  a un flujo solo por tests.
estimate: M
task_file: desk/drawer/tasks/workspace-documental/task-ws30.md
promotion: not_authorized; precise changed files/pills/atoms/evidence and task-only
  preflight required
output_base: graph_ui:repository_root/
node_role: delivery

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
  UI; source versionado y destino temporal no son registros independientes. Resolver
  dos desks y procedencia; no duplicar registry.
output_scope: ejemplo/nav/ (plantillas Markdown versionadas en el paquete del plan)
depends_on:
- WS11
- WS40
requires: []

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS21
id: WS21
title: Integrar fuente y renderizado según source_mode
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Alternar fuente/render con mismo origen, revisión y dirty buffer; usar guardado
  fuente autorizado. Composición escribe solo origen trazable soportado. Ejecutar
  solo la variante elegida por P04; Con pending no se prepara ni se promueve este
  nodo. Al alternar con cambios sin guardar se conserva el buffer; nunca se descarta
  sin confirmación explícita de la persona usuaria; si no confirma, el buffer se conserva.
  No requiere G_SOURCE si el humano eligió fuente read_only.
acceptance: Cumplir la aceptación específica de la variante P04. En editable, G_SOURCE
  y G_WRITE_CONTRACT pasan y se prueba edición/conflicto/roundtrip. En read_only,
  fuente legible no editable y edición por campos probada; manual/WS30 no declaran
  edición fuente disponible. En ambos modos una composición, si existe en el contrato
  WS12, escribe solo en el documento dueño de cada campo; si no hay soporte, queda
  de solo lectura y se declara.
output_scope: frontends/mindmap/views/workspace/; tests/
depends_on:
- WS19
requires:
- G_UI_WRITE
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS22
id: WS22
title: Renderizar Board como trabajo navegable
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Representar Board real como lista, como tablero y con dependencias, abriendo
  en el lector los mismos TaskDoc y sus pills/átomos referenciados. No reemplazar
  workflow con drag-and-drop de status.
acceptance: Selección y links comunes con lector; estados y gates leídos de deskops
  (Board, lifecycle), no de dag.yaml; no duplicar tareas ni presentar predicado satisfecho
  como test aprobado.
output_scope: frontends/mindmap/views/workspace/board/; tests/
depends_on:
- WS13
- WS09
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS23
id: WS23
title: Renderizar rituales y pasos como procedimiento
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: RitualDoc/StepDoc/lifecycle sobre referencias reales; pasos, transiciones y
  fuentes navegables. Pruebas sobre corpus WS40 o store temporal real.
acceptance: Un procedimiento abre sus documentos y soporte; no auto-marcar pasos como
  realizados por leerlos. El estado de un paso solo viene de deskops; esta vista no
  lo escribe.
output_scope: frontends/mindmap/views/workspace/procedure/; tests/
depends_on:
- WS13
- WS09
requires:
- G_UI_READ

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS24
id: WS24
title: Integrar conocimiento y grafo local
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: Reutilizar el gráfico actual y una vista de documento genérica única registrada
  en shell/registry.js para átomos/protoátomos/crossroads (CrossroadDoc del árbol
  de dominio)/materializaciones/pills, clasificación y vecindad; preservar Code local
  del ticket workspace en draft que identifique el acta WS11. Backlinks = relaciones
  entrantes calculadas por la API de grafo de sldb según auditoria/infraestructura.md
  (producido por WS03). Clasificación = tipo y tags. Vecindad = 1–2 hops. Code local
  = proyección Code del ticket workspace.
acceptance: Navegación ida/vuelta por fuentes y backlinks derivados; un soporte no
  modelado (Markdown sin modelo) es visible y navegable en la vista con su ruta de
  origen. No un renderer nuevo obligatorio por cada clase.
output_scope: frontends/mindmap/views/workspace/graph/; Context; tests/
depends_on:
- WS13
- WS18
requires:
- G_UI_READ

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

FILE:desk/drawer/plans/workspace-documental/dag.yaml#edge:WS28
id: WS28
title: Integrar verificación y handoff de cierre
kind: implementation
owner_repo: graph_ui
node_role: delivery
scope: 'Verificar con `deskops closeout verify` por el canal del contrato WS12, diagnosticar
  faltantes y ofrecer handoff explícito con evidencia: a `deskops closeout commit`
  por CLI en modo manual, o al coordinador si está activo (P03). No commit/close desde
  HTTP en baseline. G_HUMAN_READ aplica porque es una acción de escritura del baseline.'
acceptance: UF05 termina cuando `deskops show task` y el commit de closeout confirman
  el cierre externo y refrescar estado; comando o solicitud no equivalen a cierre.
  Sin terminal embebido genérico.
output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/
depends_on:
- WS27
- WS12
requires:
- G_CLOSEOUT
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
  con confirmación de la persona usuaria en la UI, que ve el alcance y la procedencia
  antes de ejecutar; materializaciones se inspeccionan/validan, no se generan destinos
  arbitrarios.
acceptance: UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales;
  las materializaciones existentes se inspeccionan y validan contra el modelo SLDB
  vigente, sin crear destinos; cada capability no soportada se declara no disponible
  y bloquea solo el escenario de UF03 que la usa y su etiqueta de disponibilidad,
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
  y atom->doc verificados. Scion solo capítulo marcado propuesto hasta WS38. Para
  capítulos que mencionen personalización o impacto, comprobar G_HUMAN_MODEL/WS29
  o mantener etiqueta propuesta; no bloquear manual básico por esos extras.
output_scope: docs/workspace-user-manual.md; docs/assets/workspace-user-manual/; desk/atoms/
  vinculados
depends_on:
- WS30
- WS10
- WS43
requires:
- G_HUMAN_MANUAL

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
acceptance: P09 y contrato fijan ubicación/modelo opcional. El participante que fija
  P08 recorre Markdown y UI real, links/roots verificables (root = alias/root autorizado
  por el contrato de navegación; un enlace es verificable si resuelve a un path existente
  del repo enlazado), commit por `deskops closeout commit`, acta deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md
  y commit; no publicar solo ejemplo como si fuera ecosistema real. Cada proyecto
  adicional requiere su tarea de repo y acuerdo de alcance.
output_scope: desk/README.md; mapa de ecosistema/índices según P09 y WS11; átomos
  de acuerdos durables
depends_on:
- WS17
- WS30
requires:
- G_HUMAN_MANUAL
- G_PRODUCT
- G_WRITE_CONTRACT

FILE:desk/drawer/plans/workspace-documental/dag.yaml#gates
G_HUMAN_MANUAL:
  title: Persona aprueba autoría/revisión
  state: pending
  resolver: WS30
  evidence: graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md;
    actor humano/versión/guion/resultado y soportes. Guardar en repo dueño, no en
    el paquete de plan deskops.
  produced_by: WS30
  evidence_ref:
    repo: graph_ui
    path: runs/subagents/workspace-documental-acceptance/manual/acta.md

FILE:instruccion
Revisa el nodo WS30 siguiendo context-review-guide.md. Los bloques edge son contratos de sus vecinos; no los revises. No ejecutes nada.

