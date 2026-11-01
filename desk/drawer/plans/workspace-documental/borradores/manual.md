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

## Definiciones de disponibilidad (WS10)

Registradas tal como las fija la aceptación de WS10 (`../dag.yaml`, entrada WS10, campo `acceptance`).

- **Disponible**: solo versión o commit implementado, pruebas relevantes y acta humana del recorrido y pasos verificados. Hoy ningún capítulo cumple las tres condiciones: no hay actas (`../validacion-humana.md`; `auditoria/ui.md` §3, filas WS16 y WS30: «ausencia explícita», sin acta). Por eso ninguna capacidad nueva de UI queda disponible y ningún capítulo lleva esa etiqueta.
- **Propuesto**: intención sin esa evidencia.
- **Bloqueado**: dependencia o contrato identificado pendiente.

Precedencia, fijada en la preparación de esta tarea, no en la aceptación: donde `../dag.yaml` o el texto previo de este borrador ya fijan una etiqueta, se conserva y se cita (capítulo 12 Scion, capítulo 15 modelos, parte avanzada de Changes en el capítulo 14). En el resto, «bloqueado» si hay dependencia o contrato identificado pendiente; «propuesto» si no. Las etiquetas se refieren a las capacidades que describe cada capítulo, no al capítulo como texto.

Las capacidades del CLI de Deskops no se copian aquí: se remiten a `docs/operator-manual.md` (manual CLI vigente, que este borrador mantiene separado). Las pruebas y actas futuras se remiten a sus productores en `../dag.yaml` (WS30, WS31, WS38, WS39, WS40, WS43), sin anticiparlas.

## Ejemplo fijo: Taller (corpus futuro)

Ruta y productor vienen del contrato de WS10 (`../dag.yaml`, entrada WS10, campo `scope`): `graph_ui:.tmp/workspace-documental-ejemplo/`, productor WS40. Hasta que WS40 lo genere se describe como **corpus futuro**: no hay capturas ni pasos, y Taller no es producto operativo. Estado verificado en `auditoria/ui.md` §3, fila WS40: «ausencia explícita», no existe `tests/fixtures/workspace_documental/` ni script de seed. De `decisiones.md` solo consta que P08 fija «Taller temporal», con participación del solicitante; la ruta y el productor no se atribuyen a P08. Los recorridos UF01–UF10 (capítulo 17) usan este mismo ejemplo.

## Fichas por capítulo

Cada ficha: Propósito, Entradas, Salidas, Estado, Evidencia. Son esquema conceptual, no redacción del manual: no contienen pasos, capturas ni nombres de controles. «Hueco» = no se encontró en lo abierto. Rutas de auditoría relativas a `auditoria/`; `ops` = `docs/operator-manual.md`. Dueño de un hueco: productor citado en el plan, o «sin productor en el DAG».

### 1. Qué es un desk
- **Propósito**: fijar el vocabulario de documentos, conocimiento, trabajo y procedimientos.
- **Entradas**: conceptos y vocabulario acordados (sección «Qué se puede escribir ahora»); categorías del desk.
- **Salidas**: modelo mental común para los capítulos 2–16.
- **Estado**: propuesto (conceptual; sin dependencia ni contrato identificado pendiente).
- **Evidencia**: `deskops.md` «Universo auditado» y §C (categorías `desk/inbox`, `drawer`, `contexts`, `rituals`, `registry`, `roles`, `runtimes`, `tasks`, `lifecycle`); `ops` «Desk scaffold, migration, and repair» (línea 137). Hueco: sin dueño de glosario aparte de WS01 (brief); no verificado en esta tarea.

### 2. Entrar al ecosistema y conocer un proyecto
- **Propósito**: orientar a quien llega a un proyecto, con o sin desk.
- **Entradas**: ruta del proyecto; registro del ecosistema; entradas del desk (`desk/README.md` + mapa authored, P09).
- **Salidas**: proyecto identificado y punto de partida.
- **Estado**: bloqueado (orientación de proyecto sin desk: WS15.2; entradas reales: WS17/WS43).
- **Evidencia**: `ui.md` §3 fila WS15.2 (ausente orientación sin desk y el comando de `init`); `decisiones.md` P09; CLI: `deskops.md` §A1 (`repo whoami`, `repo register`, `about`, `faq`) y `ops` «Repository identity and the ecosystem registry» (109), «Orient yourself» (57), «Initialize the repository» (48). Hueco: `deskops faq` lee `docs/faq.md`, no `DeskFAQDoc` (`deskops.md` §A1 fila `faq`).

### 3. El workspace: explorador, selección, documentos abiertos, divisiones e historia
- **Propósito**: describir el espacio de trabajo y su estado local.
- **Entradas**: catálogo de documentos; foco e historia locales (P07).
- **Salidas**: documentos abiertos, selección, historia.
- **Estado**: bloqueado (contrato de navegación WS11; pestañas y divisiones WS13.3).
- **Evidencia**: `ui.md` §3 filas WS13, WS13.2, WS13.3: base parcial más delta; el catálogo solo cubre documentos del store y las pestañas actuales son proyecciones, no pestañas de documentos; `decisiones.md` P07. Hueco: contratos de navegación aún no existen (no está `../contratos/`); dueño WS11.

### 4. Buscar, seguir referencias y entender relaciones y procedencia
- **Propósito**: encontrar documentos, seguir enlaces y ver de dónde viene una relación.
- **Entradas**: término o filtro; documento de partida.
- **Salidas**: resultados, vecindad, enlaces entrantes y salientes.
- **Estado**: bloqueado (búsqueda por API en la UI: WS14; vecindad con grafo de sldb: WS24).
- **Evidencia**: `infraestructura.md` §3 (enlaces `[[doc]]`, aristas `references`/`contains`, anclas) y §4 (`sldb find`, `sldb graph`); `ui.md` §3 filas WS14 (filtro local, falta búsqueda por API) y WS24 (vecindad 1–2 saltos). Hueco: búsqueda por similitud sin CLI (`infraestructura.md` §4, fila corpus: «hueco»); consultas guardadas ausentes (§4); la UI no estaba contrastada con la API de grafo (`ui.md` §6).

### 5. Leer y editar: fuente Markdown, renderizaciones, campos, composiciones y conflictos
- **Propósito**: leer y modificar un documento con control de conflictos.
- **Entradas**: documento; `source_mode`; revisión esperada.
- **Salidas**: documento guardado o conflicto visible con recuperación.
- **Estado**: bloqueado (guardado de fuente WS20/G_SOURCE; edición con conflicto WS19; precondición de payload WS45).
- **Evidencia**: `infraestructura.md` §1 (guardado de Markdown en bruto con revisión: «ausente») y §2.1 (revisión esperada ausente en la API pública; verificación optimista solo en HTTP; escritor externo sin protección); §6 punto 4 (confirma P03); `ui.md` §3 filas WS19.1, WS19.2, WS21; `decisiones.md` P03, P04. Hueco: pruebas de concurrencia real no ejecutadas (`infraestructura.md` §7); catálogo de renderizaciones lo cataloga WS09, no abierto aquí.

### 6. Capturar y aclarar: inbox, drawer, protoátomos y preguntas
- **Propósito**: registrar entradas y aclararlas antes de promoverlas.
- **Entradas**: nota de inbox, candidato de drawer.
- **Salidas**: nota leída/confirmada, candidato promovido.
- **Estado**: bloqueado (UI de inbox y captura: WS25).
- **Evidencia**: `ui.md` §3 filas WS25, WS25.1, WS25.2 (ausencia explícita); CLI: `deskops.md` §A1 (`message send/list/read/ack`, `promote inbox-to-drawer-task`, `drawer remove`) y `ops` «Inbox, messages, and drawer» (303). Hueco: «proto» en el CLI solo para átomos (`atoms proto`, §A1).

### 7. Trabajar conocimiento: átomos, clasificación, relaciones y materializaciones
- **Propósito**: crear y mantener conocimiento durable.
- **Entradas**: átomo; tags; fuente de materialización.
- **Salidas**: átomos clasificados y materializaciones.
- **Estado**: bloqueado (operaciones de conocimiento en UI: WS42; grafo local: WS24).
- **Evidencia**: `ui.md` §3 filas WS42 y WS24; CLI: `deskops.md` §A1 (`atoms *`, `materialize`) y §B (`AtomDoc`, `MaterializationContractDoc`); `ops` «Atoms» (500), «Roles, materialization, and drift» (644). Hueco: 2 de 8 materializaciones sin indexar en el índice local (`deskops.md` §B, notas).

### 8. Definir trabajo: alcance, dependencias, contexto y evidencia
- **Propósito**: describir una tarea con evidencia declarada.
- **Entradas**: objetivo, alcance, `closeout_evidence`, pills.
- **Salidas**: tarea ruteada en el Board.
- **Estado**: bloqueado (autoría desde UI: WS26).
- **Evidencia**: `ui.md` §3 filas WS26, WS26.1, WS26.2 (ausencia explícita); CLI: `deskops.md` §A1 (`add task`, `edit task`, `bind pill`) y §D; `ops` «Tasks» (354), «Inspect, edit, and advance a task» (385).

### 9. Organizar trabajo activo: boards y fases
- **Propósito**: ver y ordenar el trabajo activo.
- **Entradas**: Board y tareas.
- **Salidas**: vista de trabajo por estado y dependencias.
- **Estado**: bloqueado (tablero navegable: WS22).
- **Evidencia**: `ui.md` §3 fila WS22 (lista y detalle leídos de deskops; falta tablero agrupado y dependencias navegables); `deskops.md` §C2 fila «fases» (no hay `PhaseDoc` ni carpeta; las fases son concepto, ritual y pills). CLI: §A1 (`list boards`, `show board`, `next`).

### 10. Aplicar contexto y procedimientos: pills, rituales, pasos y lifecycle
- **Propósito**: aplicar procedimientos y contexto reutilizable a una tarea.
- **Entradas**: pill, ritual, paso, grafo de lifecycle.
- **Salidas**: tarea con contexto y nodo de lifecycle visibles.
- **Estado**: bloqueado (renderizado de rituales y pasos: WS23).
- **Evidencia**: `ui.md` §3 fila WS23 (no hay renderer de RitualDoc ni StepDoc); `deskops.md` §B (`PillDoc`, `RitualDoc`, `StepDoc`: 0 documentos de paso) y §A1 (`advance task`, `show task`); `ops` «Inspect the lifecycle graph» (92). Hueco: ninguno de los comandos de edición de `RoleDoc`/`RuntimeProfileDoc` existe (`deskops.md` §B).

### 11. Ejecutar manualmente; validar y revisar resultados
- **Propósito**: ejecutar a mano, validar y revisar el resultado con su evidencia.
- **Entradas**: tarea; cambios Git por repo; evidencia declarada.
- **Salidas**: resultado revisado y evidencia encontrada o verificada.
- **Estado**: bloqueado (diff y evidencia: WS27.1, WS27.2; validación humana: WS30).
- **Evidencia**: `ui.md` §3 filas WS27.1, WS27.2 (solo evidencia «declarada»), WS30 (sin acta); CLI: `deskops.md` §A1 (`closeout verify`) y §D. Hueco: el diff por repo no tiene implementación en lo versionado (`ui.md` §3, WS27.1).

### 12. Delegar, comunicarse e intervenir (ramal Scion)
- **Propósito**: delegar y vigilar trabajo en agentes.
- **Entradas**: tarea; intento; mensajes.
- **Salidas**: trazabilidad de ejecución e intervención.
- **Estado**: propuesto (fijado por este borrador, que lo deja pendiente hasta WS37, y por `../dag.yaml` WS31: «Scion … solo como capítulo marcado propuesto hasta WS38»).
- **Evidencia**: `ui.md` §3 filas WS35, WS36, WS37 (ausencia explícita); `decisiones.md` («Ninguna decisión autoriza dispatch, mensajes o acceso Scion»); CLI de runtime: `deskops.md` §A1 (`runtime status`, `runtime supervise`) y `ops` «Runtime and Herdr» (715). Hueco: la auditoría de identidad y API Scion (WS05) no se abrió; no se afirma ninguna capacidad Scion.

### 13. Cerrar trabajo y conservar conocimiento durable
- **Propósito**: cerrar una tarea con su evidencia y dejar el conocimiento en átomos.
- **Entradas**: tarea con `closeout_evidence`; commit; átomos.
- **Salidas**: tarea cerrada (commit de closeout) y conocimiento conservado.
- **Estado**: bloqueado (verificación y handoff de cierre desde UI: WS28; P05 deja el cierre en CLI/coordinador).
- **Evidencia**: `ui.md` §3 fila WS28 (existe `advance`, no `closeout verify` ni handoff); `decisiones.md` P05, P06, T-P05; CLI: `deskops.md` §D (`closeout verify`, `closeout commit`) y §A1; `ops` «Closeout» (407). Hueco: `closeout commit` borra la tarea y su archivo (`deskops.md`, resumen, «Sorpresas» d).

### 14. Diagnosticar integridad, relaciones rotas, conflictos e impacto de cambios
- **Propósito**: detectar y entender problemas de integridad e impacto.
- **Entradas**: store; relaciones; cambios.
- **Salidas**: hallazgos de integridad y de impacto.
- **Estado**: bloqueado para diagnóstico base (errores de lectura y modo degradado: WS15). Changes avanzado: propuesto hasta WS29, fijado por este borrador («Changes avanzado hasta WS29») y por `../dag.yaml` WS31.
- **Evidencia**: `ui.md` §3 filas WS15.1 y WS29 (sin vista Changes; `tests/test_mindmap_changes.py` no existe); CLI: `deskops.md` §A1 (`doctor`, `graph missing`, `drift check`); `infraestructura.md` §3 (`sldb edges check/unresolved`). Hueco: no se comprobó si `sldb stores check` escribe cache (`deskops.md` resumen, hueco 1).

### 15. Personalizar modelos, vistas y configuración mediante contratos soportados
- **Propósito**: inspeccionar y editar modelos y vistas por contrato soportado.
- **Entradas**: modelo o clase; ViewDoc.
- **Salidas**: modelo o vista modificados y promovidos.
- **Estado**: propuesto (fijado por este borrador, «El capítulo de modelos se marca propuesto hasta prueba WS39», y por `../dag.yaml` WS39: G_HUMAN_MODEL antes de marcarlo disponible).
- **Evidencia**: `ui.md` §3 fila WS39 (base parcial: editor existente) y §3.1 (evaluador y guardado de ViewDoc solo en modo local); `infraestructura.md` §5.2 (modelo ViewDoc en spec2viz, sin evaluador en sldb, pron ni spec2viz; cero ViewDoc en el store de spec2viz) y §6 punto 1. Hueco: renderer de la vista en `apps/review-workbench` solo listado, no leído (`ui.md` §3.1); dueño WS18.

### 16. Referencia de superficies, operaciones, vocabulario y límites
- **Propósito**: consulta de superficies y operaciones reales.
- **Entradas**: contratos de navegación y operaciones; inventarios.
- **Salidas**: tabla de referencia.
- **Estado**: bloqueado (contratos `contratos/navegacion.md` y `contratos/operaciones.md` de WS11/WS12: la carpeta aún no existe).
- **Evidencia**: `deskops.md` §A1/§A2 (113 comandos, 24 métodos), §B (17 modelos); `infraestructura.md` §2 y §4; `ui.md` §3; `ops` «Verb coverage» (742). Hueco: el inventario de CLI cubre el repo deskops; el interior de `../sldb`, `../spec2viz`, `../pron` y `../scion` no se leyó en WS02 (`deskops.md` resumen, hueco 2).

### 17. Recorridos completos: UF01–UF10
- **Propósito**: recorrer de principio a fin cada flujo sobre Taller.
- **Entradas**: corpus Taller (WS40); flujos UF01–UF10 (se conservan como están en el índice).
- **Salidas**: recorridos verificados con acta humana.
- **Estado**: bloqueado (corpus WS40, validación WS30 y publicación WS31/WS43).
- **Evidencia**: `ui.md` §3 filas WS40 y WS30 (ausencia explícita); `../dag.yaml` WS31 (publicación remite a las actas de WS30/WS43). Hueco: la definición de los flujos no se leyó aquí; dueño WS08.
