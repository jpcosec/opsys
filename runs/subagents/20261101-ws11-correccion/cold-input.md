FILE:desk/tasks/task-corregir-contrato-de-navegación-de-ws11-tras-revisión-root.md
---
id: task-corregir-contrato-de-navegación-de-ws11-tras-revisión-root
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/borradores/vistas.md
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261101-ws11-correccion/review-source.md
- runs/subagents/20261101-ws11-navegacion/handoff.md
- runs/subagents/20261101-ws11-navegacion/comparison-ledger.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-001-task-closure-commit.md
files:
- desk/drawer/plans/workspace-documental/contratos/navegacion.md
- desk/drawer/plans/workspace-documental/borradores/vistas.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-contrato-ws11.md
closeout_evidence:
- commit
- document
---

# Corregir contrato de navegación de WS11 tras revisión root

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root no aprobó contratos/navegacion.md: el PASS del Tester fue focal y tres auditorías de apoyo hallaron afirmaciones que no se sostienen, además de decisiones root sobre foco, enlaces, WS18 y aliases que el contrato debe recoger.

## Goal

_Describe the concrete result this task must produce._

Corregir en una pasada contratos/navegacion.md según los puntos A a F y las cuatro decisiones root, y ajustar solo la celda necesaria de F18a en vistas.md, cotejando todas las filas C y H y las cadenas de llamada relevantes.

## Scope

_State what is in scope and what is out of scope._

Autoridad: runs/subagents/20261101-ws11-correccion/review-source.md, que se lee completo y prevalece sobre este resumen. Lista cerrada.

Superficies de escritura: desk/drawer/plans/workspace-documental/contratos/navegacion.md, una celda de F18a en desk/drawer/plans/workspace-documental/borradores/vistas.md y runs/subagents/20261101-ws11-correccion/result-summary.md.

Decisiones root que el contrato debe recoger, sin reabrirlas:
1. WS13.1 no se reduce a C1-C4. Foco interno por documento, distinguido de navegación.
2. Enlaces entre desks por composición en graph_ui dentro de WS41, sin ampliar sldb. H-16 pasa a integración/API de graph_ui de WS41.
3. WS18 sigue detenida por selección y notación mínimas; es opcional y no bloquea la base.
4. Aliases reales: configuración confiable del operador al arrancar o seleccionar despliegue. WS11 fija el contrato del input, WS41 consume y valida, WS40 da la instancia temporal. Sin configuración confiable no hay lectura cruzada. El registry da identidad y puede ser fuente designada por el operador, no autorización automática.

Correcciones:
A. Secciones 4 y 6 y H-03 a H-05b: separar datos disponibles, interacción existente y comportamiento futuro comprometido, con todas las condiciones de A sobre C1-C4, C5b, C6, C7, C8/C9, C11/C12, C14, H-05b, mismo origen y RitualDoc.steps.
B. Sección 3.3: guardias generales separadas de las específicas de referencias de TaskDoc. H-06 y enlaces: autorizar y resolver antes de cualquier lectura o recursión; composición parse_links, split_anchor y doc_status; sintaxis y tratamiento fijados.
C. Secciones 3, 5.4, 8 y H-14: retirar «doc_status no escribe»; lectura sin mutación con stores preparados y comprobación al ejecutar consumidores; store propio en WS13.1 y WS24, segundo desk en WS41.
D. Sección 7 y H-09: status conservado en el cliente como delta de WS15.1; E7 muestra la causa recibida.
E. Sección 10: authored no equivale a modelado.
F. vistas.md, F18a: solo la celda necesaria, con notation-view.js:356 y shell/registry.js:16.
Además: clave de sesión de modelado con alias además de Model:name.

Conservar: mapa de recibos por delta de la sección 12, estado de actas, opcionales sin bloquear la base, fuente propia frente a Code, identidad opcional, store explícito y estado borrador.

Cotejar todas las filas C y H, no una muestra, abriendo el código citado. Tabla por fila en result-summary.md.

No tocar: dag.yaml, helper, validadores, fuentes comunes, otros contratos, código, repos hermanos, auditorías. Sin commits, revisiones ni tests. Sin preguntar al solicitante. Una decisión de producto no cubierta se expone en result-summary.md, no se improvisa.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer review-source.md y el contrato completos. 2. Abrir cada cita de cada fila C y H y seguir las cadenas de llamada nombradas por root. 3. Aplicar A a F y las cuatro decisiones. 4. Escribir result-summary.md con resolución por punto, tabla por fila y lo no leído.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/contratos/navegacion.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261101-ws11-correccion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: A a F y las cuatro decisiones resueltas explícitamente en el contrato; todas las filas C y H cotejadas; revisión root del parche congelado antes de registrar o revisar; Tester independiente PASS sobre los puntos corregidos completos, por lectura; revisión fresca no ejecutora del contrato corregido con consumidor, en evidencia separada; WS09 renovada solo si vistas.md cambió; build --check, validate --check y status en verde.

FILE:runs/subagents/20261101-ws11-correccion/review-source.md
# Decisión root sobre el checkpoint WS11, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-11-01, revisión del closeout `65f76c46`. Autorización de trabajo documental local; no es aprobación humana. Texto copiado sin normalizar.

Revisión root del checkpoint WS11 (65f76c46): NO apruebo todavía el contrato ni activo WS12/UI. El cierre de la TaskDoc no sustituye esta revisión. Tres auditorías de apoyo leyeron todas las filas C y H y los bloques restantes, cotejando el código citado. El PASS v3 era focal sobre enumeración de archivos; no prueba el resto del contrato.

Verificación root: SHA del contrato coincide completo ca537c71d585a86032a1bf3817705f00af4904139e50534f0f5b70416b3597df; build/validate/status verdes. DAG, helper, decisiones, guía, vistas, user-flows, cobertura y manual idénticos a f3ef4cec. El contrato no es fuente de los bundles actuales: 0 stale NO equivale a contrato aceptado ni a consumidores listos. Comparé además los modelos/identity/operations de Deskops entre215bf624 y c19c6c0d: diff vacío, sin divergencia de esas fuentes.

DECISIONES ROOT sobre tus cuatro puntos:
1. NO reducir WS13.1 a C1–C4 actuales. Preservar foco interno por documento, distinguido de navegación. Hay datos reales para definir un delta futuro acotado en graph_ui; no confundir inventario actual con frontera de lo realizable. Ver corrección A debajo.
2. Resolver enlaces entre desks por composición en graph_ui dentro de WS41, usando parser/referencias reales y validación previa; NO ampliar SLDB por faltar wrapper wiki. H16 queda como integración/API graph_ui de WS41, con salvedad independiente de lectura no mutante. Ver B/C.
3. WS18 sigue detenida por selección/notación mínima no fijadas. Es opcional; no bloquea contrato básico/lector/manual y no elegir subgrafo por reflejo. No requiere nueva pregunta al humano ahora.
4. Aliases reales son configuración confiable suministrada por operador al arrancar/seleccionar despliegue, no un documento que deba generarse automáticamente. WS11 fija el contrato del input; WS41 su consumo/validación; WS40 da la instancia temporal de prueba. Sin configuración confiable no se habilita lectura cruzada. Registry da identidad y puede ser fuente designada explícitamente por operador, no autorización automática ni imposibilidad de autorizarlo por tener rutas absolutas. No inventar valores, modelo, productor o nueva decisión humana.

CORRECTIVO DOCUMENTAL ÚNICO, antes de WS12:

A) §§4/6 y H03–H05b: separar datos disponibles, interacción existente y comportamiento futuro comprometido. C1–C3 solo cambian selectedId/navegan a otro documento, no demuestran foco interno. C4 es tarjeta derivada pasiva: CodeFileView no tiene callback de selección, no interacción texto→Code existente. Definir dominio futuro de WS13.1 con procedencia real: sección y span de la misma fuente; campo/field_path; referencia de archivo identificada por documento/campo/posición/valor; arista schema con sus procedencias. WS13.3 conserva/restaura ese foco por documento. Preservar fields/references y posición antes de concatenar (H03); no atribuir archivo externo a nodo del grafo. Cada representación puede mostrar solo la correspondencia que realmente existe; no inventar highlight equivalente donde falta. Esto cabe en componentes/rutas de graph_ui ya previstos, no requiere inventar API semántica en sldb.
Condiciones: C6 owning_section es opcional (map_fields.py:22–26,43–74), no dueño garantizado ni rango exacto del campo. C7 span exacto por campo sigue sin soporte y no bloquea foco de campo/contendor. C8/C9 deben preservar multiplicidad: workspace_routes.py:384 deduplica(source,target,type,relation_doc), pudiendo colapsar distintos campos al mismo destino; no elegir arbitrariamente un campo inverso. C5b «no hay IR sin modelo» es demasiado absoluto: extract_sections(markdown) es independiente y build_document_ir_json está exportado; describir ausencia de ruta actual en graph_ui y reutilización por verificar, sin inventar modelo ni afirmar API lista para ese caso. C11/C12: foco de la referencia explícita es distinto de mapear semánticamente líneas de un archivo externo a texto/graph. C14 separar rango local de Code (archivo/revisión/líneas; :N±5 es contexto, no rango de usuario) de traslado al Markdown, que no está comprometido por F17. H05b no debe agruparlos como una única capacidad imposible. §4: «mismo origen» exige render/fuente de la misma lectura/revisión, no solo misma ruta; mantener reserva surface.text no prueba fuente íntegra. Pasos RitualDoc.steps tienen orden/posición sin StepDoc ni progreso.

B) §3.3: no aplicar guardia de referencias TaskDoc a todo lector. La tabla incluye desk/tasks, .md y excluirBoard.md (deskops_routes.py:36–40); esa regla es específica de referencias de tareas, no de FAQ/contexts/Board/fuente/explorador. Separar guardias generales y específicas para no bloquear el alcance.
H06/enlaces: reaplicar contención tras recover_links es tarde. links/recovery.py:13–14 lee destino con #anchor antes de retornar y:29–30 recursa. Analizar y autorizar/resolver destino ANTES de cualquier lectura/recursión, no usar recover_links arbitrario como resolver seguro para sanear después. En WS41 componer parse_links + split_anchor + referencia pública doc_status cuando corresponda, distinguiendo alias:Model/name o alias:ruta de los IDs GUI Model:name. Autorizar alias/root primero; operar sobre store objetivo explícitamente autorizado, validar contención también del resultado; include_linked=False, sin federación automática. doc_status cubre trackeados; no modelados usan resolución protegida de archivo de WS13.1/13.2, no un modelo falso. Fijar sintaxis y tratamiento en el contrato para que WS40/WS17 puedan authorar enlaces reales, sin inventar una API deSLDB inexistente.

C) §§3/5.4/8/H14: retirar «doc_status no escribe». doc_status.py:25 y edge_reading.py:28 llaman open_store(readonly), open_store.py:38 migra layout; readonly controla descubrimiento/fallback, no garantiza cero escrituras. load_edge_index evita rebuild pero no la migración transitiva. Para lectura sin mutaciones: stores preparados/canónicos fuera del request y comprobación real al ejecutar consumidores de que las llamadas escogidas no escriben; no migrar como efecto de leer, no asumir que el modo basta. Si no puede sostenerse con API pública, hueco con dueño y bloqueo del caso antes de implementar, no workaround de formato interno ni API inventada. El caso store propio pertenece al delta de lectura WS13.1/ruta consumida por WS24; no dejarlo huérfano por ser local. Segundo desk lo verificaWS41. No agregar tareaSLDB por reflejo: si se prueba falta de capacidad, intake explícito en repo dueño y tarea antes del workaround.

D) §7/H09: shell/api.js:5–11 descarta response.status; E2 exige mostrarlo. Tipificar/conservar status y error HTTP/red/JSON en wrappercliente como deltaWS15.1 además de renderer, sin API nuevaSLDB. E7: IR no construible/is_degraded/422 no identifican por sí solos modelo no importable (también roundtrip/lectura/otrasexcepciones); mostrar causa recibida y reservar esa etiqueta a causa corroborada. No inventar discriminante que backend no entrega.

E) §10: authored no equivale a todo documento modelado. SpecDoc/SpecNodeDoc materializados son derivados de YAML, como vistasF18a ya corregida. WS40 manifiesto generado de roots/stores/commits/documentos es evidencia derivada, aunque se versionara; plantillas/generador/definición corpus son fuente authored. No nuevo modelo por esta distinción.

F) Specs: actualizar SOLO la celda necesaria F18a de vistas.md para reflejar base existente notationView registrada (notation-view.js:356 yshell/registry.js:16). Integrarla al lector sigue candidatura sin productor; no afirmar aceptación ni inspección de todo elrenderer. Esta nueva evidencia debe matizar inventario anterior, no cambiar auditoría histórica ni fuente común.

Mantener mapa de recibosperdelta §12, estado sinactas y opcionales sin bloquear base. Los 18G_UI_READ/14G_UI_WRITE yproductores de H restantes son compatibles según cotejo. No añadir actas/aceptación a partir de código leído. Fuente propia vs Code, identidad opcional y store explícito son bases válidas; conservarlas. Para múltiplesdesks, clave de sesión de modelado debe incluir alias ademásde Model:name, sincolisiones entreidentidadeslocales iguales.

Ejecución autorizada: tarea correctivaDOCS acotada con drawer/promoción/TaskDoc/pills, preflight/cold baratos frescos, Executor y Tester independientes. Superficies: contratos/navegacion.md, ajuste puntualF18a en vistas.md, notas/registro evidencia y punteroWS09 por cambio real; no comunes/otroscontratos/código/hermanos/helper/validadores. No exige implementar endpoints o pruebasruntime en este correctivo. Congelar parche completo y enviarme diff/hash + resolución explícita de las4decisiones y puntosA–F ANTES de registrar/revisar. Cotejar TODAS lasfilas C/H y las cadenas de llamada relevantes, no otra muestra de enumeraciones. Tester posterior debe probar los puntos corregidos completos por lectura, no declarar que probó comportamiento.

También hacer revisión barata fresh no ejecutora del CONTRATO CORREGIDO + el encargo de consumidor pertinente y referencias/extractos explícitos necesarios: reformulación, ambigüedades y dry-run hipotético. Evidencia separada en el run, sin fingir que los73reviews viejos cubren este artefacto nuevo. No modificarhelper ni esquema para fabricar vigencia. Los futuros preflight/cold de consumidores deben traer el contrato real enlazado. Renovar entradasDAG realmente afectadas por vistas.md (previsiblementeWS09); 0stale del resto se informa como revisión del plan, no revisión del contrato.

No closeout ni fase hasta revisar ese parche/congelación; noWS12/UI/Scion/push. Conservar estado borrador y4dirtyajenos. Ningún punto requiere pedir permiso al humano ni recortar WS13.1 a navegaciónactual. Si aparece decisión de producto no cubierta, exponerla antes de improvisar; estas4quedan resueltas con el alcance indicado.

FILE:desk/drawer/plans/workspace-documental/contratos/navegacion.md
# Contrato de navegación e identidad del workspace documental (WS11)

Estado: borrador del Executor de WS11, 2026-11-01. No está revisado: «contrato básico revisado» exige Tester independiente PASS y revisión root. No hay actas de recepción (sección 12). `execution_authorized` global sigue en `false`; este documento no autoriza implementación, escritura en repos hermanos ni Scion.

## 0. Convenciones de cita y de estado

- Cada cita de código es `repo@commit ruta:línea` o `ruta:símbolo`, y corresponde a un archivo que el Executor abrió en el commit indicado (ver `runs/subagents/20261101-ws11-navegacion/result-summary.md` para el detalle de lo abierto). Dónde dice «auditoría» se cita `ui.md:N`, `infraestructura.md:N` o `deskops.md:N` = líneas de `auditoria/ui.md`, `auditoria/infraestructura.md`, `auditoria/deskops.md` de este directorio.
- Prefijos de ruta: `GU/` = `../UIs/graph_ui/frontends/mindmap/` (graph_ui `134a665`, árbol limpio salvo untracked); `SL/` = `../sldb/src/sldb/` (sldb `77bd6d0097f46efdec5e7eeb0e58d71d70b98be5`); `DK/` = este repo, leído en el HEAD `c19c6c0d` (las auditorías WS02 fijaron `215bf624`; solo se abrieron `deskops/models/*.py`, `deskops/identity.py` y `deskops/operations.py`, y no se compararon con `215bf624`).
- **existe** = el código leído lo muestra en ese commit. **aceptado** = tiene acta de recepción o revisión que lo diga. Hoy no hay ningún aceptado (sección 12). Toda fila de este contrato que diga «soportado» significa «existe en código»; nunca «aceptado» ni «ejecutado». No se ejecutó nada.
- `frontends/workspace/` de graph_ui (sin commit, `ui.md:158`) no es base ni se cita como evidencia.
- «No definido» siempre lleva productor o «sin productor en el DAG».

## 1. Alcance y estado

**Qué fija este contrato** (lo que WS11 debe fijar según `dag.yaml:681-711`): identidad, origen y modelo opcional de un documento Markdown; nodos graph y code con origen; resolución explícita de repo/store; fuente propia frente a Code referenciado; navegación, enlaces e historia; el dominio de correspondencias que admiten foco compartido; errores de lectura y red; lectura multidesk de solo lectura; el límite de ViewDoc; clasificación de huecos; y el mapa de deltas que requieren recepción.

**Qué no fija**: escritura, guardado, whitelist, conflictos y fallos parciales (todo hueco de escritura va a WS12, `dag.yaml:723-796`); la implementación en graph_ui; Scion; Changes; ViewDoc opcional. La lectura no espera guardado ni WS12.

**Base observada**: graph_ui `134a665` (workspace integrado a1b2b22, cierre f16fcd1, `reconciliacion.md:3`); sldb `77bd6d0097f46efdec5e7eeb0e58d71d70b98be5`. Alcance heredado: `alcance.md:5` (Entrega L), `alcance.md:27` (recepción por delta).

**Dependientes directos de WS11 en `dag.yaml`** (recomputado leyendo `depends_on`): WS12, WS13, WS13.1, WS13.2, WS13.3, WS17, WS18, WS33, WS40, WS41. Son 10; la TaskDoc decía «trece nodos» y el Supervisor lo corrigió (`preflight-disposition.md`). WS15.1 consume este contrato por texto de su aceptación (`dag.yaml:1052-1092`), pero depende de WS13, no de WS11 directamente.

**Fuera de este contrato, por diseño**: el contrato básico no espera Changes (WS29), Scion (WS32-WS36, WS44), ViewDoc opcional (WS18/G_SPEC_VIEW) ni modelos (WS39).

## 2. Identidad y origen

### 2.1 Qué existe hoy

| Concepto | Qué hace el código | Evidencia |
|---|---|---|
| Identidad canónica de documento modelado | `Model:name`. El catálogo la arma como `f"{model_name}:{name}"`; la ruta de nodo la resuelve por `Model:name`, por `Model/name` o por nombre solo | `GU/workspace_routes.py:118`, `:251-269` (`_resolve_document`) |
| Nombre ambiguo | Un nombre presente en más de un modelo responde 400 «Identidad ambigua… Use Model:name» | `GU/workspace_routes.py:264-267`, `:299-300` |
| Guardia de identificador | Rechaza vacío, `..` en cualquier posición y prefijo `/` o `\` con 400. Es un criterio textual: también rechazaría un nombre legítimo que contenga `..` | `GU/workspace_routes.py:134-135` |
| Ruta del documento | Cada nodo del catálogo lleva `path` (`str(getattr(d,'path',''))`), el nodo lo repite y el contexto lo repite | `GU/workspace_routes.py:125`, `:237`, `:209` |
| Resolución de respaldo (documento que no valida) | Intenta `resolve_runtime_doc`; si falla, busca en `load_edge_index` y marca el nodo `is_degraded` con `degraded_reason`; solo busca frontmatter en rutas fijas bajo `desk/tasks`, `desk/contexts`, `desk/rituals`, `desk/roles`, `desk/runs`, `desk/relations` | `GU/workspace_routes.py:271-352` (candidatos `:314-322`) |
| Hash de campos y de archivo | `content_hash` = `doc_version(doc)` (hash de campos); `file_revision` = sha256 de los bytes del archivo si está dentro de `repo_root`, no es `.git` y no está ignorado por git | `GU/workspace_routes.py:173-198`; `SL/api/documents/document_serialization.py:24-32` (`doc_version`) |
| Qué es un documento en sldb | Un archivo Markdown con frontmatter y secciones, registrado en el store; el payload se extrae con el codec del modelo | `infraestructura.md:29-30` |

Esto **existe** y está **sin aceptar**. No hay en graph_ui un concepto de «proyecto» o «desk» en la identidad: el catálogo es de un solo store (sección 3).

### 2.2 Markdown modelado frente a no modelado

- **Modelado** = archivo vinculado a un modelo por `.sldb/store.yaml` (`include:`), nunca inferido por carpeta (`deskops.md:212`, «Reglas» de la sección C). Identidad: `Model:name`. Modelo: el del store. Hoy son 17 modelos (`deskops.md:181`, `deskops.md:185-201`).
- **No modelado** = Markdown del desk sin modelo (p. ej. issues, FAQ de `docs/`, candidatos del drawer, `desk/contexts/README.md`): 118 archivos en el universo auditado (`deskops.md:226`; la cifra es del HEAD `215bf624`). **No es corrupción** (`user-flows.md:176`). Los candidatos de drawer con forma de TaskDoc tampoco están modelados (`deskops.md:217`).

**Regla de identidad para un Markdown no modelado** (definición de este contrato; es lo que WS13.1/WS13.2 deben implementar, y no existe hoy):

1. Identidad = par `(repo, ruta)` donde `repo` es el alias del desk (sección 3) y `ruta` es la ruta relativa al root de ese repo, normalizada, con `/`. No lleva `Model:`.
2. El modelo es **opcional**: ausente significa «no modelado». La UI no lo infiere por carpeta ni por forma del contenido; si el store lo trackea, la identidad pasa a `Model:name` y la ruta queda como origen.
3. Un mismo archivo no puede tener dos identidades: si el store lo trackea, `Model:name` prevalece y el explorador no lo repite como no modelado.
4. Una ruta que no resuelve dentro del root del repo, que cae en `.git`, en un archivo ignorado por git o fuera del criterio de la sección 3.3 no tiene identidad: se muestra el error, no el contenido.

**Qué no existe hoy**: ninguna ruta de graph_ui entrega a la UI el texto del archivo propio de un documento (modelado o no) ni lista Markdown no modelado. Sí lo leen dos puntos internos que no exponen el texto: `read_bytes` solo para el hash de revisión (`GU/workspace_routes.py:196`) y `read_text` en la resolución de respaldo, solo para extraer el frontmatter (`GU/workspace_routes.py:326-331`). `_build_code_projection` lee solo `files`/`references` del payload (`GU/workspace_routes.py:441-451`; `ui.md:55`); `workspace_nodes` lista solo `editor_store.documents()` (`GU/workspace_routes.py:102-127`). La búsqueda `grep` de `focus` y de rutas de archivo propio no aparece en `GU/workspace_routes.py` ni en `GU/views/workspace/`. Producción: lectura de fuente propia, WS13.1; árbol y refresco, WS13.2 (huecos H-01 y H-02).

### 2.3 Nodos graph con origen

- Un nodo graph es un documento: `GU/workspace_routes.py:395-413` arma cada nodo con `id` (`Model:name`), `name`, `model_name`, `title`, `status`, `depth`. Una arista lleva `source`, `target`, `type`, `origin`, `relationDoc` (`:387-393`). El **origen de una arista** es `origin` ∈ {`relation_doc`, `schema`, `structural`} (`SL/api/edges/document_edge.py`, campo `origin`) y, para aristas `schema`, el campo del documento que la declara está en el registro de sldb (`SL/store/edge_index/declared_references.py:68`, `field=field, declared=value`), pero **`DocumentEdge` no lo expone** (`SL/api/edges/document_edge.py`, campos `id, source, target, type, origin, relation_doc`) y la ruta de graph_ui tampoco (`GU/workspace_routes.py:387-393`). Ver fila C8 de la sección 6.
- Los nodos de los extremos que no son documentos (etiquetas, modelos, campos, el store) quedan fuera de `document_edges` (`SL/api/edges/document_edges.py:18`, `:36-39`).
- El grafo es la vecindad a 1 o 2 saltos (`GU/workspace_routes.py:365-376`; `depth` solo admite 1 o 2, `:86-91`).

### 2.4 Nodos code con origen

- Un nodo code es una referencia a archivo del payload (`files` o `references`), con estados `ok`, `no_es_ruta`, `sin_repo_root`, `fuera_del_repo`, `no_existe`, `protegido`, `directorio`, `demasiado_grande`, `binario`, `error_lectura` (`GU/workspace_routes.py:481-575`). Su **origen** es la cadena original (`reference`), la ruta relativa al repo (`path`) y, si la cadena termina en `:N`, `fragment_line`, `fragment_content`, `fragment_span` (±5 líneas) (`:487-493`, `:565-571`).
- Límite de tamaño 256 KB (`GU/workspace_routes.py:19`); lenguaje por extensión, con `text` por defecto (`:20-37`, `:553`).
- Las referencias a código **no** llevan el nombre del campo de origen: `files` y `references` se concatenan antes de inspeccionarse (`:441-446`).
- Las anclas `code:<ruta>::<símbolo>` de sldb son otra capacidad (`SL/api/anchors/record_anchor.py:15`, `infraestructura.md:94`, requiere extra `[code]`); graph_ui no las consume (no aparece `anchors` en `GU/workspace_routes.py`). No hay CST supuesto (Tree-sitter diferido, `ui.md:46`).

## 3. Resolución de repo y store

### 3.1 Lo que existe

- graph_ui resuelve **un solo store por proceso**: `WorkspaceRoutes.__init__` guarda `store_path` y `repo_root = store.parent` (`GU/workspace_routes.py:68-71`, `:612-617`); el servidor lo construye una vez con `store or SLDB_STORE` (`GU/serve.py:506-515`; default `.sldb` de graph_ui, `:49`). Las rutas de Deskops resuelven una sola raíz (`DESKOPS_ROOT` absoluto o el padre del store) (`GU/deskops_routes.py:129-137`; `ui.md:87`).
- El workspace no existe en modo remote: responde 501 (`GU/serve.py:320-322`).
- La API pública de sldb **sí** recibe el store por llamada: `open_store(store, mode)` acepta un directorio `.sldb` o el alias de un enlace (`SL/api/stores/open_store.py:16-39`; `SL/api/stores/store_discovery.py:67-76`, `_resolve_store_arg`). `load_edge_index(store, include_linked=False)`, `doc_status(store, ref)`, `search(store_path, term, …)` y `document_history(store, doc_ref)` toman el store como argumento (`SL/api/edges/edge_reading.py:14`, `SL/api/stores/doc_status.py:18`, `SL/api/search.py:26`, `SL/api/documents/document_history.py:23`). No hace falta cambiar `SLDB_STORE` para leer otro store.
- **`open_store` no es solo lectura**: migra el layout si hace falta y agenda un re-chequeo por operación (`SL/api/stores/open_store.py:30-38`). Y `_resolve_store_arg` acepta cualquier ruta que sea un store (`:69-71`): **sldb no limita roots**; cualquier límite lo pone el llamador.
- Precedente en sentido contrario: `GU/views_routes.py:29-33` (`_store`) acepta del cliente cualquier directorio `.sldb` de la máquina (`store` en query o body) y las vistas pueden **escribir** ahí (`:56-66`). Eso es lo que la lectura multidesk **no** debe replicar.
- El registro de repos de deskops: `RepositoryDoc` con `name`, `id`, `path` (relativa al root del ecosistema), `status`, `description`, `tags` (`DK/deskops/models/repository.py:35-52`); `load_repository_registry` lee `desk/registry/repo-*.md`, resuelve el root y rechaza ids o roots duplicados (`DK/deskops/identity.py:65-88`); `_resolve_registered_root` acepta rutas absolutas y relativas con `..` **sin comprobar contención** (`DK/deskops/identity.py:256-262`). Hay 6 `RepositoryDoc` (`deskops.md:195,220`). `deskops list tasks --include-repos` ya lee los Boards de los repos registrados (`DK/deskops/operations.py:364-394`; `deskops.md:76`) con su propio filtro de rutas de tareas (`:1196-1210`).

### 3.2 Regla del contrato

1. **Explícita por petición.** Cada petición de lectura nombra el desk con un **alias** (cadena de un conjunto cerrado), nunca con una ruta ni con un store. El servidor traduce alias a `(root, store)` consultando el conjunto cerrado. Una petición sin alias usa el desk del proceso, y el alias que lo designa se devuelve en la respuesta.
2. **Aliases y roots autorizados: el mecanismo, no los valores.**
   - Corpus de prueba: el **manifiesto JSON de WS40** (roots, stores, commits, documentos clave; `dag.yaml:2672-2711`) es el conjunto cerrado. El manifiesto no existe todavía (hueco H-10, instancia, productor WS40).
   - Desk real: el registro `desk/registry` da **identidad** (id, path, name) pero **no autorización**, porque no impone contención (`identity.py:256-262`). Un conjunto cerrado de aliases autorizados para el desk real **no existe** y ningún nodo del DAG lo produce (H-11, instancia, sin productor en el DAG). WS41 se limita a los dos stores de WS40 (`dag.yaml:2712-2744`); la publicación real (WS43) no lo define.
   - No se inventan valores de alias ni de roots en este contrato.
3. **Sin cambiar `SLDB_STORE` global** ni abrir un store por una ruta recibida del cliente. Cada petición conserva su `(root, store)`; no hay estado compartido entre peticiones.
4. **Alias no autorizado, ruta que escapa y store ausente** dan error visible con su causa (sección 7, E-MD1 a E-MD3). El estado de un enlace de sldb (`ok` / `missing` / `not-a-store`) está en `SL/api/stores/store_links.py:15-36` y el de una referencia (`ok` / `missing` / `ambiguous` / `link-missing` / `link-broken`) en `SL/api/stores/doc_ref_status.py` y `doc_status.py:18-33`.

### 3.3 Rutas seguras: el criterio sale del código existente

Criterio mínimo, tomado de lo que ya hace `_inspect_file_reference` (`GU/workspace_routes.py:481-575`) y de las guardias vecinas:

| Criterio | Qué hace el código | Evidencia |
|---|---|---|
| Contención | Resuelve (`resolve()`, sigue symlinks) y exige `is_relative_to(repo_root)`; si no, `fuera_del_repo` | `:501-518` |
| `.git` | Cualquier parte `.git` de la ruta → `protegido` | `:521-524` |
| Ignorado por git | `git check-ignore -q` con timeout de 2 s; si falla la verificación, **falla cerrado** (`protegido`). Si el repo no tiene `.git`, no evalúa nada | `:460-479` |
| Directorio | `directorio`, no se lista | `:531-532` |
| Tamaño | Más de 256 KB → `demasiado_grande` | `:536-537` |
| Binario | Un byte nulo → `binario` | `:540-541` |
| Codificación | UTF-8 con reemplazo marcado (`utf-8-replaced`) | `:543-549` |
| URL externa | `http(s)://` → `no_es_ruta`, no se abre | `:484-485` |
| Contención del Board | La guardia de tareas exige `desk/tasks`, sufijo `.md` y nombre distinto de `Board.md` | `GU/deskops_routes.py:36-40` |

**No cubierto por el código existente** (por lo tanto, hueco o decisión de WS13.2/WS41, no inventado aquí):

- Una **lista de permitidos** de carpetas o extensiones: cualquier archivo de texto no ignorado dentro del repo se lee, aunque no sea del desk; las extensiones desconocidas se leen como `text` (`:553`). No hay criterio sobre archivos sensibles que no estén en `.gitignore`.
- La verificación `check-ignore` no existe fuera de un repo git (devuelve «no ignorado»): en el corpus sin repo git no protege nada.
- Condiciones de carrera entre `resolve()` y la lectura (TOCTOU): no tratadas.
- La guardia del identificador de nodo (`'..' in ident`) es textual (`:134`).
- `recover_links` de sldb resuelve `[[destino]]` también contra `Path(destino)` absoluto o relativo al directorio actual (`SL/links/resolver.py:32-37`): cualquier consumidor debe volver a aplicar la contención antes de abrir `path`.

El **criterio que este contrato fija** para toda lectura de archivo por UI: todos los de la tabla; más, para el explorador de no modelados (H-02), que el WS13.2 declare su lista de permitidos antes de implementar. No se declara hoy cuál es.

## 4. Fuente propia frente a Code referenciado

- **Fuente propia** = el archivo Markdown del documento (modelado o no). **Code referenciado** = los archivos que el documento nombra en `files`/`references`. Son cosas distintas y no se mezclan en una pestaña.
- Hoy `projections.code` es solo Code referenciado (`GU/workspace_routes.py:431-458`). La fuente propia **no tiene proyección**. `file_revision` solo hashea el archivo propio, no lo entrega (`:180-198`).
- La pestaña Documento muestra el IR (secciones) y los campos, y badges de línea `L<ini>-<fin>`; no muestra el texto crudo (`GU/views/workspace/node/workspace-view.js:41-52`, `:325-379`; `GU/shared/document-ir.mjs:11-26`).
- sldb entrega, junto al IR, `surface`: los nodos crudos del parser con su `text` y su rango de líneas (`SL/api/records/utils.py:10-19`; `SL/core/ir/document_ir.py:8-14`). `workspace_node` ya recibe ese IR (`GU/workspace_routes.py:153-161`; `SL/api/documents/document_ir_serialization.py:13`). Que `surface` reconstruya el texto íntegro **no está verificado**: no se afirma. `render_document_markdown` **no** es la fuente: renderiza el payload por la plantilla del modelo (`SL/api/documents/document_render.py:19-28`). No se encontró en `SL/cli/serve/` ni `SL/api/documents/` una operación pública que devuelva los bytes del archivo del documento (búsqueda de `raw`, `read_text`, `read_bytes` y rutas de `serve`; las lecturas del archivo del documento encontradas son internas y devuelven datos derivados, no el texto: IR y secciones en `SL/cli/serve/document_routes.py:62`, `SL/cli/serve/sections_routes.py:46` y `SL/api/documents/document_ast.py:22`; procedencia en `SL/api/documents/document_serialization.py:20`; payload anterior al guardar en `SL/api/documents/payload_save.py:54`; validación al registrar en `SL/api/documents/track_document_file.py:47,48,68`; texto previo al estampar en `SL/api/documents/provenance_stamp.py:31`). La capacidad de **guardado** raw-source no existe (`infraestructura.md:33`, productor WS20) y no se confunde con la de lectura.
- Lectura de fuente propia (modelada o no): hueco H-01, clase API (la ruta de lectura no existe en graph_ui; graph_ui puede leer el archivo con el criterio de la sección 3.3, sin pedir nada a sldb), dueño graph_ui, productor WS13.1. «Render y fuente con el mismo origen» (`dag.yaml:841-871`): la fuente y el render apuntan al mismo `(repo, ruta)` o `Model:name`; no hay dos copias.
- La edición de fuente espera WS20/WS21 y es de WS12; esta lectura no la necesita.

## 5. Navegación, enlaces e historia

### 5.1 Navegación y historia que existen

- Estado en URL: `?id=&depth=&tab=`; cada cambio de nodo, profundidad o pestaña hace `pushState` (`GU/views/workspace/node/workspace-view.js:71-86`, `:213-226`); `popstate` vuelve a leer la URL (`:88-100`, `:196-199`). Las pestañas son `document`, `graph`, `code` (`GU/views/workspace/node/workspace.mjs:5` `TABS`): son **proyecciones** del mismo documento, no pestañas de documentos.
- Seguir una relación o un nodo del grafo cambia el documento activo (`workspace-view.js:222-226`, `:419`, `:537`). El catálogo se carga al montar; «Actualizar» recarga el nodo, no el catálogo (`:102-136`, `:296`; `ui.md:56`).
- Filtro local por id, título y modelo (`workspace.mjs:11` `filterCatalog`); filtro de aristas por tipo (`:83`).
- **La URL no lleva repo ni alias**: no puede distinguir dos desks (H-12, API, graph_ui, WS41; con WS13.3 para la historia).

### 5.2 Enlaces

- Sintaxis en sldb: `[[doc]]`, `[[doc#Sección]]`, `![[doc]]` (transclusión) y `[pred:: [[doc]]]` (`SL/links/parser.py:6-7`; `infraestructura.md:88-90`). Resolución de un documento: `recover_links(doc_path, store_path)` (función importable, `SL/links/recovery.py:23-31`; no está reexportada por `sldb.api`) y `sldb docs recover`. Un destino `[[x]]` resuelve en este orden: nombre rastreado del store local, ruta relativa al documento, ruta absoluta o relativa al directorio actual (`SL/links/resolver.py:32-37`). **No hay rama de alias**: un `[[alias:x]]` no se resuelve entre stores con esta función. `recover_links` recibe una ruta de archivo, así que sirve también a un Markdown no modelado (`recovery.py:23-28`).
- La auditoría de enlaces del store (`audit_links`, `GET /lint`) informa enlaces no resueltos (`SL/links/audit.py:10`; `SL/cli/serve/lint_routes.py:25,58`).
- **graph_ui no consume `[[…]]`**: la búsqueda de `[[`, `wikilink`, `recover` y `/lint` en `GU/` no encuentra código del workspace que los use (las coincidencias son de otros módulos). Seguir un enlace de texto, hoy, no existe (H-06, API de lectura de graph_ui, WS13.1; la referencia rota la consume WS15.1).
- **Enlaces entre desks**: ver sección 8.4.
- Referencias por campo: aristas `references` y `contains` declaradas por el modelo (`SL/store/edge_index/declared_references.py:38-70`); el workspace las muestra como relaciones entrantes y salientes (`GU/workspace_routes.py:200-201`; `workspace-view.js:537`).
- Backlinks: `incoming_relations` del contexto (`GU/workspace_routes.py:200`) son las aristas entrantes de la vecindad (1 o 2 saltos), no un cálculo con la API de grafo completa (`ui.md:69`). Los backlinks por `edges_to` o `graph` no se consumen (`SL/api/edges/edge_reading.py`, `reconciliacion.md` C-44).

### 5.3 Historia

- **Historia de navegación** = la del navegador (arriba) y, cuando WS13.3 la entregue, la de documentos abiertos de la sesión. Es disposición local (P07, `decisiones.md:31`); no es documento compartido. «Volver sigue el orden inverso» y la restauración de foco son aceptación de WS13.3 (`dag.yaml:933-973`); no existen hoy.
- **Historial Git** = otra cosa. `document_history(store, doc_ref)` devuelve las versiones comprometidas de un documento; fuera de git devuelve vacío (`SL/api/documents/document_history.py:1-7,23`; `infraestructura.md:60`). graph_ui no lo usa en el workspace. El diff por tarea y repo es WS27.1 (H-13).

### 5.4 Efecto de lectura

`_build_graph_neighborhood` llama a `document_edges` (`GU/workspace_routes.py:356-359`), que **reconstruye el índice de aristas** bajo el lock del store y espera si está ocupado (`SL/api/edges/document_edges.py:30`; `SL/api/edges/rebuild_edges.py:17-40`). La docstring de `workspace_routes.py:3` dice «Strictly read-only»; en términos de archivos derivados no lo es por lectura del código. `load_edge_index` documenta que «Reading never rebuilds» (`SL/api/edges/edge_reading.py:14-26`). Esto importa para la sección 8 (H-14). No se ejecutó para confirmar el efecto.

## 6. Foco y correspondencias

**Dominio de la tabla**: selecciones que una persona puede hacer en un documento abierto (texto, graph, code) y el destino en otra representación **del mismo documento** o en otro documento. «Foco» = elemento seleccionado dentro de un documento (`dag.yaml:857-859`); el documento activo identifica la pestaña. **Regla**: sin mapeo no hay soporte, y ninguna fila se da por soportada por omisión. Una fila «soportado» solo indica que el código lo muestra; no está aceptada.

**Estado del foco hoy**: no hay estado de foco. En `GU/workspace_routes.py` y `GU/views/workspace/` no aparece el término `focus` (búsqueda); el único estado de selección es `selectedId` (un documento) más `depth` y `tab` (`workspace-view.js:56-61`). Lo que sigue, por tanto, es el **dominio posible** y lo que falta para cada fila.

| # | Selección origen | Destino | Correspondencia real | Evidencia | Estado |
|---|---|---|---|---|---|
| C1 | Nodo vecino en el graph | Documento activo (misma identidad `Model:name`) | El `id` del nodo del grafo es la identidad canónica del catálogo | `GU/workspace_routes.py:118`, `:395-413`; `workspace-view.js:222-226`, `:419` | soportado (existe, no aceptado) |
| C2 | Relación entrante o saliente del contexto | Documento origen o destino | Las aristas llevan `source`/`target` = `Model:name` | `GU/workspace_routes.py:200-201`, `:387-393`; `workspace-view.js:537` | soportado (existe, no aceptado) |
| C3 | Opción del catálogo | Documento activo | Mismo id | `workspace-view.js:260-264` (selector `onChange`→`handleSelectNode`) | soportado (existe, no aceptado) |
| C4 | Entrada de `files`/`references` en el texto/payload | Tarjeta Code de esa referencia | El código recorre las entradas en orden y cada tarjeta lleva `reference` (la cadena original) y `fragment_line` si hay `:N` | `GU/workspace_routes.py:441-451`, `:487-493`, `:565-571`; `workspace-view.js:15-39` | soportado en el sentido texto→Code, a nivel de entrada, por la propia tarjeta; sin estado de foco (existe, no aceptado) |
| C4b | Tarjeta Code | Campo (`files` o `references`) del documento | El campo de origen se pierde: las dos listas se concatenan antes de inspeccionarse. El IR sí tiene un nodo por campo, pero una lista es **un** nodo con toda la lista como valor (`flatten_payload` no desagrega listas) | `GU/workspace_routes.py:441-446`; `SL/api/records/flatten.py` | **no soportado**: sin mapeo. Hueco H-03 |
| C5 | Sección del texto (IR `structure`) | Rango de líneas del Markdown propio | Cada sección lleva `span.line_start/line_end`; cada nodo `surface` lleva `text` y `span` | `SL/api/records/build_ir.py:39`, `:64`; `SL/api/records/utils.py:10-19` | Datos reales en sldb y ya enviados al cliente; la UI solo los muestra como badge y no tiene vista de texto con líneas. **No soportado como foco**. Hueco H-04 (documentos modelados) |
| C5b | Sección o línea de un Markdown **no modelado** | Estructura | No hay IR sin modelo | `ui.md:55`; `GU/workspace_routes.py:151-165` (IR vía el store) | **no soportado**. Hueco H-01/H-04 |
| C6 | Campo del payload (`field_path`) | Sección que lo contiene | `owning_section` por campo | `SL/api/records/build_ir.py:68-77` (`_build_field_nodes`) | Dato real en sldb; la UI no lo usa (`irFields` no lo lee: `GU/shared/document-ir.mjs:11-17`). **No soportado como foco**. Hueco H-04 |
| C7 | Campo del payload | Rango de líneas | `_build_field_nodes` no asigna `span` a los campos; la UI ya asume líneas nulas para el frontmatter (`document-ir.mjs:18-19`) | `SL/api/records/build_ir.py:68-77` | **no soportado**: sin mapeo. Hueco H-05 |
| C8 | Campo de referencia o contención del texto | Arista del graph | sldb guarda el campo y el valor declarado en el registro de arista (`field=…, declared=…`); `DocumentEdge` y la ruta de graph_ui los omiten | `SL/store/edge_index/declared_references.py:68`; `SL/api/edges/document_edge.py`; `GU/workspace_routes.py:387-393` | **no soportado hoy**. El dato existe en `load_edge_index(...).edges[].metadata` (`SL/api/edges/edge_reading.py:14`; `SL/store/models/edge_record.py`). Hueco H-03b |
| C9 | Arista del graph | Campo del texto que la declara | Inverso de C8 | idem | **no soportado**. Hueco H-03b |
| C10 | `[[doc]]` en el texto | Documento destino | Existe `recover_links` (resuelve nombre rastreado o ruta); graph_ui no lo consume | `SL/links/parser.py:6-7`; `SL/links/resolver.py:32-37`; búsqueda en `GU/` sin consumo | **no soportado en la UI** (existe en sldb). Hueco H-06 |
| C11 | Línea o archivo en Code | Sección, campo o nodo graph | No hay mapeo. El archivo de Code no es un nodo del grafo ni se vincula a una sección | `GU/workspace_routes.py:431-458` | **no soportado**. Es el caso «seleccionar en Code actualiza el foco de texto/graph» de la aceptación de WS13.1 (`dag.yaml:841-871`). Hueco H-05b, **requiere decisión de alcance**: ver nota 6.2 |
| C12 | Línea o sección del texto | Línea de Code | No hay mapeo texto→código (prohibido inventarlo, `dag.yaml:857-859`) | — | **no soportado, declarado así**. Sin productor y sin compromiso de producirlo |
| C13 | Nodo graph de otro desk | Documento de otro desk | No existe: el workspace tiene un store y la URL no lleva repo | `GU/workspace_routes.py:68-71`; sección 3 | **no soportado hoy**. WS41 (H-12, H-10) |
| C14 | Rango de líneas dentro de un archivo Code (F17) | Rango en el texto | Hay `fragment_line` y `fragment_span` de ±5 líneas, no un rango seleccionado por la persona | `GU/workspace_routes.py:565-571` | Soporte de rango solo de entrada (`:N`); selección de rango por la persona: **no soportado**. H-05b |

### 6.1 Dominio de foco que este contrato declara soportable con lo que el código muestra

Con el código leído, lo único que se puede declarar soportado para foco compartido es **la identidad del documento** (C1-C3) y, para el Code referenciado, **la entrada de `files`/`references` ↔ su tarjeta** (C4). Es un dominio de documento y de entrada de referencia. Nada de C4b-C14 queda declarado como soportado.

### 6.2 Nota de alcance (WS13.1)

La aceptación de WS13.1 dice que «seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten» (`dag.yaml:841-871`), y su alcance admite compartir foco «solo donde exista correspondencia real de origen definida WS11». Con el dominio de 6.1, esa aceptación **no se cumple por completo con los mapeos existentes**: los mapeos de C4b-C11 son huecos con productor (H-03 a H-05b). Este contrato no elimina el comportamiento comprometido: lo registra como hueco con productor WS13.1 (cuyo `output_scope` incluye «rutas de lectura contrato WS11», `dag.yaml:841-871`). La alternativa de **acotar la aceptación de WS13.1 al dominio de 6.1** es un **cambio de alcance que decide root**, no el Executor. Mientras eso no se decida, WS13.1 no puede declararse cumplido en foco texto/code/graph.

## 7. Errores de lectura y estados de red (consumidor: WS15.1)

### 7.1 Respuestas del servidor que existen

| Código | Cuándo | Evidencia |
|---|---|---|
| 200, `ok:true` | Nodo o catálogo; la proyección puede traer su propio fallo (abajo) | `GU/workspace_routes.py:92`, `:94` |
| 400 | `id` ausente; `depth` distinto de 1 o 2; identificador con `..` o prefijo de ruta; identidad ambigua | `:84-91`, `:134-135`, `:264-267`, `:299-300` |
| 404 | Documento no encontrado; ruta de workspace desconocida | `:352`, `:96` |
| 405 | Método distinto de GET | `:74-75` |
| 500 | Error no previsto; error al cargar documentos del catálogo | `:99-100`, `:108-109` |
| 503 | `El store no está disponible.` (sin store, store inexistente o sin `editor_store`) | `:104-105`, `:131-132` |
| 501 | Workspace en modo remote | `GU/serve.py:320-322` |
| Forma | `{ok:false, error:<texto>}` con el estado HTTP | `:75`, `:98`, `:100`; `GU/serve.py:json_response` |

### 7.2 Fallos dentro de un 200

- `projections.document.ok=false` + `error`: el IR no se construyó (`GU/workspace_routes.py:152-164`). La UI muestra el payload y un aviso (`workspace-view.js:325-332`).
- `projections.graph.ok=false` + `error` (`:422-429`).
- `projections.code`: `ok=false` con `error` si el documento está degradado (`:432-439`); y cada archivo con `status` (`:481-575`).
- Documento degradado: `is_degraded` y `degraded_reason` en `node` y `context` (`:217-218`, `:240`, `:309-346`).
- `documents_error` si el catálogo del store no se pudo listar al resolver un nodo (`:139-145`, `:216`, `:242`).
- `content_hash_error` y `file_revision_error` (`:173-198`).
- Problemas del índice de aristas: `{ok, problems, store_problems_count, error}` (`:577-609`) y su lectura `formatProblems` en cuatro estados `clean`, `node_problems`, `store_problems`, `error` (`workspace.mjs:63-81`). No sustituye `sldb stores check`, `deskops doctor` ni `drift check` (`reconciliacion.md` C-06).

### 7.3 Cliente

`request()` lanza `Error(body.error || 'No se pudo completar la operación')` cuando la respuesta no es 2xx o `ok===false`, adjunta `error.body`, y aplica timeout de 60 s (`GU/shell/api.js:4-13`). `loadCatalog` y `loadNode` muestran `err.message` en el panel (`workspace-view.js:126-130`, `:185-189`, `:316-317`). Una caída del backend o una respuesta no-JSON llega como la excepción nativa de `fetch`/`json()`: **por lectura de `api.js` y por el comportamiento estándar de `fetch`; no se ejecutó**. No hay forma normalizada de «sin respuesta»: la persona ve el mensaje del navegador.

### 7.4 Fallo de carga CDN

`index.html` declara un `importmap` con `esm.sh` para react, react-dom, @xyflow/react, htm, dagre, elkjs y lucide, y una hoja de estilos de `esm.sh` (`GU/index.html:7-8`). Búsqueda de `onerror`, `onError` y `import(` en `index.html`, `app.js` y `shell/*.js`: sin manejo de fallo de carga (solo `try/catch` de `localStorage` e `history`). Como el árbol de módulos se resuelve por el importmap antes de que exista cualquier panel React, **un panel dentro de la aplicación no puede informar ese fallo**; el diagnóstico tiene que vivir fuera del árbol que no cargó. Eso es decisión de implementación de WS15.1; el contrato fija lo observable, no el mecanismo. El empaquetado offline está fuera de alcance (`alcance.md:21,23`); no se afirma funcionamiento sin red.

### 7.5 Estados que WS15.1 debe distinguir (observable)

| Estado | Se reconoce porque | Qué debe verse | Qué debe conservarse |
|---|---|---|---|
| E1 Sin respuesta del backend | `fetch` rechaza o vence el timeout | «Backend sin respuesta» y reintento | Pestañas, foco, historia, último nodo |
| E2 Respuesta de error | HTTP no-2xx con `{ok:false,error}` | El `error` del servidor y el código | Ídem |
| E3 Respuesta ilegible | No es JSON | Mensaje distinto de E2 | Ídem |
| E4 Éxito con fallo de proyección o documento degradado | 200 con `ok:false`/`is_degraded` | Aviso en el panel afectado; el resto sigue | Ídem |
| E5 Referencia rota | `[[x]]` no resuelto (`recover_links`/`audit_links`) o estado `no_existe`/`fuera_del_repo`/`protegido` en Code | Origen y causa | Navegación |
| E6 Documento ausente | 404 | «Documento no encontrado» + id | Historia |
| E7 Modelo no importable | `ir` no construible (`is_degraded`/422 en sldb) | Aviso de degradado | Ídem |
| E8 Fallo CDN | Módulos no cargan | Diagnóstico visible; sin prometer offline | No aplica (la app no arrancó) |
| E9 Fuente sin capacidad de edición | Límite read-only | Límite visible, **no** fallo de lectura | Ídem |

No se inventa respuesta del backend ausente: E1 y E8 se prueban simulando la ausencia, no suponiendo qué devolvería. «Reintentar» tras restaurar el backend: el botón Actualizar ya conserva `selectedId`, `tab` y `depth` porque llama `loadNode(selectedId, depth)` sin tocar el estado (`workspace-view.js:296`); el catálogo solo se carga al montar (`:196`).

### 7.6 Qué distingue «error, conflicto, cambio y pérdida de soporte»

`user-flows.md:177` pide un criterio visible. Este contrato fija solo la parte de **lectura**: error (E1-E3, E6), degradado (E4, E7), pérdida de soporte (E5, estados de Code `no_existe`/`fuera_del_repo`/`protegido`). **Conflicto** (409 de guardado, `infraestructura.md:51`) es de WS12/WS19; **cambio** (drift, staleness) es de WS29. Hueco H-15.

## 8. Lectura multidesk de solo lectura (consumidor: WS41)

### 8.1 Alcance

Solo lectura: no hay mutaciones cruzadas, ni envío (`message send` está fuera del baseline, `deskops.md:38`; `user-flows.md:198`), ni copia de documentos ajenos para aparentar navegación federada (`user-flows.md:189`). P07: multidesk inicialmente solo lectura con rutas y aliases explícitos (`decisiones.md:31`, T-P07).

### 8.2 Mecanismo (ver 3.2)

Alias cerrado → `(root, store)`; sin rutas del cliente; sin tocar `SLDB_STORE`. Cada respuesta incluye el alias del desk y el store resuelto, para que «identidad y origen sean visibles».

### 8.3 Lo que sldb ofrece para leer otro store

`open_store(alias_o_ruta)`, `load_edge_index(store, include_linked=False)`, `doc_status(store, ref)` y `search(store_path, …)` reciben el store como argumento (sección 3.1). `doc_status` no escribe (docstring `SL/api/stores/doc_status.py:1-5`) y devuelve `ok/missing/ambiguous/link-missing/link-broken`; un enlace a store (`stores add --name`) se resuelve solo si es **directo** (`SL/api/stores/doc_ref.py:1-8`). Las referencias entre stores se escriben `alias:ref` (`doc_ref.py:28-40`). `load_runtime_documents(include_linked=True)` federa los stores enlazados (`SL/store/query.py:76-102`) pero no se usa en graph_ui.

### 8.4 Cosas que **no** existen y que el contrato registra

- **Ruta de lectura por alias en graph_ui**: `WorkspaceRoutes` tiene un solo store (`workspace_routes.py:68-71`). Hueco H-12, clase API (graph_ui), productor WS41.
- **Enlace de texto entre desks**: `recover_links` no tiene rama de alias (`SL/links/resolver.py:32-37`) y `doc_status` resuelve *referencias*, no enlaces de texto. No hay operación pública de sldb que resuelva un `[[alias:ref]]`. Hueco H-16, clase API, dueño sldb, **sin productor en el DAG** (WS41 es de graph_ui y no crea API en sldb). La sintaxis con la que WS40 escribirá los enlaces authored entre los dos desks tampoco está fijada por el código leído. **Requiere decisión**: o WS41 compone `parse_links` + `doc_status` en graph_ui (composición, a verificar con prueba real al promover), o root amplía el alcance a sldb. El Executor no lo decide.
- **Lectura sin escritura derivada**: `document_edges` reconstruye índices (sección 5.4). Para leer el segundo desk sin tocar su disco la ruta debe usar `load_edge_index` («Reading never rebuilds»); `open_store` aún puede migrar el layout. Hueco H-14.
- **Conjunto autorizado para el desk real**: H-11 (sección 3.2).
- **Forma del error multidesk**: ver 8.5.

### 8.5 Errores visibles (la aceptación de WS41 los exige)

| Error | Causa | Contenido mínimo | Fuente del dato |
|---|---|---|---|
| E-MD1 Alias no autorizado | Alias fuera del conjunto cerrado | alias recibido; «no autorizado» | conjunto cerrado (sección 3.2) |
| E-MD2 Ruta escapada o root arbitrario | Parámetro con ruta, `..`, ruta absoluta o fuera del criterio 3.3 | ruta rechazada y criterio violado | `fuera_del_repo`/`protegido` (`GU/workspace_routes.py:511-529`) |
| E-MD3 Store ausente | El alias autorizado no tiene store | alias y ruta esperada | `store_links` (`missing`/`not-a-store`, `SL/api/stores/store_links.py:15-36`) o 503 (`workspace_routes.py:104`) |
| E-MD4 Documento ausente en el desk destino | `doc_status` ≠ `ok` | `status` y `detail` | `SL/api/stores/doc_ref_status.py` |

La forma JSON sigue la de 7.1 (`{ok:false,error}` + estado HTTP); el campo adicional con el alias es parte de la implementación de WS41, no se fija aquí.

### 8.6 Registro de desks

`RepositoryDoc` da `id`, `path`, `name`, `status`, `description`, `tags` (`DK/deskops/models/repository.py:35-52`). Sirve para **explicar** el directorio de desks (F10); no es autorización (3.2). `list_repo_task_routes` ya lee los Boards de repos registrados en el CLI (`DK/deskops/operations.py:364-394`); graph_ui no lo usa.

## 9. ViewDoc: solo grafo

- ViewDoc es un modelo de spec2viz (datos, sin ruta de store) con `nodes` (`{model, where}`), `relations`, `direction`, `notation`, `layout` (`infraestructura.md:149`; `reconciliacion.md` C-48). **No es contrato universal de UI** ni define formularios, pestañas o tableros (`brief.md:24`).
- Evaluación y rutas **existen en graph_ui, solo en modo local**: `evaluate_view(store, view)` une los documentos de cada `nodes[].model` que cumplen su `where`, filtra aristas por `relations` y `direction`, y toma `layout` de la vista o de la notación (`GU/projection_views.py:107-124`, `:41-62`); `list_views` (`:127`); rutas `GET /api/views`, `/api/views/evaluate`, `POST /api/views/save` (`GU/views_routes.py:69-87`); en modo remote responde 501 (`GU/serve.py:147-150`). `save_view` escribe en `store.parent/sldb/views/<name>.md` y no pasa `expected` (`GU/views_routes.py:56-66`). Notación: delega en `resolve_documents` de spec2viz; sin spec2viz, `notation.error` lo dice (`GU/projection_views.py:85-104`). Todo **existe**, no está aceptado, no se ejecutó.
- **Selección mínima concreta y notación para WS18**: **no hay evidencia en este paquete que fije una selección**. Ni `vistas.md` (F18b: «Selección mínima concreta: no fijada aquí»), ni `user-flows.md` (ninguna UF menciona ViewDoc), ni la reconciliación nombran qué modelos y predicados debe seleccionar un ViewDoc concreto. Las capacidades de evaluación están (arriba), pero elegir qué subgrafo ver sería inventarlo, y `dag.yaml:1212-1244` lo prohíbe («No inventar selección aquí»). **Declaración: la promoción de WS18 se detiene** hasta que un cambio de alcance o una decisión de producto, de root o del solicitante P01, fije la selección y la notación. WS18 no es prerrequisito del lector ni del manual básico (`alcance.md:27`; `dag.yaml:1565-1590`, WS24 no espera ViewDoc).
- Ruta `sldb/views/` prevista y repo de escritura: pendiente de confirmación al promover (`dag.yaml:1222-1224`); `save_view` de graph_ui escribe bajo `store.parent/sldb/views/`, que es la carpeta del proyecto dueño del store, y eso no prueba que sea del repo spec2viz (`reconciliacion.md` C-50).
- G_SPEC_VIEW: ver sección 12.

## 10. Authored, derivado y preferencia local

| Clase | Qué es | Ejemplos de este contrato |
|---|---|---|
| **Authored** | Texto o estructura escrita por persona o agente como fuente | Un Markdown no modelado; un documento modelado y sus campos; el RepositoryDoc; las entradas y el mapa de P09 (`decisiones.md:33`); el manifiesto de WS40 una vez generado |
| **Derivado** | Calculado desde otras fuentes; se regenera | Catálogo, vecindad, `incoming_relations`, backlinks, `content_hash`, `file_revision`, IR, lista de issues por estado, lista de desks, el árbol del explorador, el progreso de lectura |
| **Preferencia local** | Estado de sesión o disposición, no documento compartido (P07, `decisiones.md:31`) | Foco, pestañas, divisiones, profundidad, filtro, historia de la sesión |

Reglas:

1. **El runtime volátil no es documento compartido por defecto** (`vistas.md` reglas a precisar; `brief.md`): estado de workers, intentos y conversaciones se leen del runtime (`deskops.md:140-141`). Un RunDoc authored es otra cosa que su estado operativo.
2. **Sin modelo nuevo** para organizar entradas ni listas derivables: un índice de issues, de FAQ o de desks se calcula (consulta) o se escribe como Markdown authored con enlaces; no se crea un modelo por reflejo (`vistas.md` reglas; `dag.yaml:1170-1198`, índice authored = texto curado, no copia de listados).
3. **Preferencia local** no se persiste como documento. La disposición de WS13.3 es por sesión de navegador, sin exigir persistencia tras recargar (`dag.yaml:933-973`).
4. Las entradas y el mapa del desk (P09) son authored, en deskops, y se **publican** con WS43; el contrato de identidad no las crea (WS17 las escribe como plantillas, WS43 publica). Cuando los listados dependan de lo que ya resuelve una consulta, no se copian.

## 11. Huecos

Clases: **instancia** = documento concreto que falta escribir; **vínculo** = referencia o enlace que falta entre documentos existentes; **consulta** = selección o lista derivable sin operación pública para obtenerla; **API** = operación pública ausente en el repo dueño; **renderer** = representación ausente en graph_ui con datos ya disponibles. Cuando aplican dos, se elige la que falta primero y se dice. «Productor» = nodo de `dag.yaml`. Hueco de escritura → WS12. Una candidatura sigue siendo candidatura.

| ID | Hueco | Clase (y por qué esa) | Dueño | Productor |
|---|---|---|---|---|
| H-01 | Lectura del archivo propio de un documento (fuente íntegra + render, modelado o no), con el mismo origen | API: la ruta de lectura no existe en graph_ui (`workspace_routes.py:431-458`); falta antes que el renderer | graph_ui | WS13.1 |
| H-02 | Explorador y árbol de Markdown no modelado del desk, con refresco explícito del catálogo y lista de permitidos (3.3) | API: no hay operación de listado en graph_ui ni en sldb (`workspace_routes.py:102-127`); falta antes que el renderer | graph_ui | WS13.2 |
| H-03 | Campo de origen (`files` o `references`) de cada tarjeta Code | API: la ruta concatena y pierde el campo (`workspace_routes.py:441-446`) | graph_ui | WS13.1 |
| H-03b | Campo ↔ arista (C8/C9): el campo está en el registro de arista de sldb y la ruta de graph_ui no lo entrega | API (ruta de graph_ui); luego renderer. sldb ya tiene el dato en `load_edge_index` | graph_ui | WS13.1 (candidato; **no comprometido** literalmente: ver 6.2) |
| H-04 | Foco por sección y campo en texto (C5, C5b, C6), con la vista de texto con líneas | renderer: los datos ya llegan al cliente (IR); para no modelados, antes falta H-01 | graph_ui | WS13.1 |
| H-05 | Rango de líneas por campo (C7) | API: `_build_field_nodes` no asigna `span` | sldb | sin productor en el DAG; no comprometido |
| H-05b | Mapeo de selección en Code a texto/graph (C11) y selección de rango (C14) | API: no hay correspondencia | graph_ui | WS13.1 es productor declarado del comportamiento; **requiere decisión de alcance** (6.2): sin ella, queda sin productor identificable |
| H-06 | Seguir `[[…]]` y mostrar referencia rota desde el texto | API: graph_ui no consume `recover_links`/`audit_links` (existen en sldb, `SL/links/recovery.py:23`, `SL/links/audit.py:10`); falta antes que el renderer | graph_ui | WS13.1 (seguir enlace); WS15.1 (referencia rota) |
| H-07 | Pestañas, divisiones y foco por documento (disposición local) | renderer | graph_ui | WS13.3 |
| H-08 | Diagnóstico de fallo CDN (E8) | renderer: los «datos» (la carga fallida) viven fuera del árbol React, ver 7.4 | graph_ui | WS15.1 |
| H-09 | Estados E1-E3 distinguibles y reintento sobre catálogo | renderer: `request()` entrega los datos; la distinción visible no existe | graph_ui | WS15.1 |
| H-10 | Manifiesto de WS40 (aliases, roots, stores, commits, documentos clave) | instancia: documento concreto que falta | graph_ui | WS40 |
| H-11 | Conjunto cerrado de aliases autorizados para el desk **real** | instancia | deskops | sin productor en el DAG |
| H-12 | Ruta de lectura por alias y URL con repo/alias | API: el workspace tiene un store (`workspace_routes.py:68-71`) | graph_ui | WS41 (historia en WS13.3) |
| H-14 | Lectura multidesk sin escritura derivada (uso de `load_edge_index` en vez de `document_edges`; `open_store` puede migrar) | API: la ruta de lectura de graph_ui reconstruye índices (`workspace_routes.py:356-359`) | graph_ui | WS41 para el segundo desk; para el store propio, sin productor en el DAG |
| H-16 | Resolver un enlace de texto entre desks (`[[alias:ref]]`) | API: ausente en sldb (`resolver.py:32-37`); falta antes que cualquier vínculo en el corpus | sldb | sin productor en el DAG (WS41 es graph_ui). **Requiere decisión** (8.4) |
| H-17 | Enlaces authored entre los dos desks del corpus | vínculo (se escriben entre documentos que WS40 genera) | graph_ui | WS40; WS17 para las plantillas |
| H-13 | Diff Git por tarea y repo | renderer/API: `document_history` existe (por documento); el diff por tarea no | graph_ui | WS27.1 |
| H-15 | Criterio visible error/conflicto/cambio/pérdida de soporte (parte de lectura fijada en 7.6) | renderer | graph_ui | WS15.1 (error), WS29 (cambio); conflicto: WS12/WS19 |
| H-18 | Tablero, dependencias y apertura de TaskDoc/pills en el lector | renderer: `GET /api/desk/board` y `/task` existen (`DeskRoutes.board` y `DeskRoutes.dispatch` en `GU/deskops_routes.py`; `board` desde `:31`) | graph_ui | WS22 |
| H-19 | Procedimiento: renderer de RitualDoc/StepDoc | renderer | graph_ui | WS23 |
| H-20 | Vista genérica de conocimiento, clasificación y backlinks completos | renderer, luego consulta | graph_ui | WS24 |
| H-21 | Progreso de paso de un procedimiento | API: ningún campo en `RitualDoc`/`StepDoc` (campos en `DK/deskops/models/ritual.py:65-67`, `step.py:31-35`; búsqueda de `progress`/`done` sin resultados); WS23 declara que no se marca por leer (`dag.yaml:1540-1546`) | deskops | sin productor en el DAG; no comprometido |
| H-22 | Campo faltante de `InboxNoteDoc`, `MaterializationContractDoc`, `PillDoc`, `StepDoc`, `DeskFAQDoc`, `RepositoryDoc` | **resuelto por lectura** (ver 13, punto 5) | — | — |
| H-23 | Búsqueda con estados distintos por API | API (graph_ui consume `search`/`GET /find` de sldb: `SL/api/search.py:26`) | graph_ui | WS14 |
| H-24 | Orientación de proyecto sin desk | renderer | graph_ui | WS15.2 |
| H-25 | Captura, ack, respuesta local (inbox), autoría de tareas y edición de campos | **escritura**: remitido a WS12 | deskops / graph_ui | WS12 (contrato); WS25.x, WS26.x, WS19.x, WS21 (UI) |

**Candidaturas sin productor** (siguen como tales, `vistas.md` sección «Candidaturas sin productor»; no son prerrequisito del lector ni compromisos): consulta guardada y búsqueda por significado sin CLI (`infraestructura.md:115,121`; dueño sldb); edición de `RoleDoc` y `RuntimeProfileDoc` (excluida por UF09; dueño deskops); navegación de preguntas de `DeskFAQDoc`; lista de issues en la UI (dueño graph_ui; `issue list` existe como CLI de deskops, `deskops.md:49`, y la UI no tiene ruta que lo llame); renderer de roles; vista Specs embebida en el lector. **Genérico Markdown o modelado no implica renderer especial** de FAQ, issues, roles o Specs. Hallazgo sobre Specs: la vista **Specs sí existe en graph_ui** como vista de primer nivel (`notationView`, `GU/views/specs/notation/notation-view.js:356`, registrada en `GU/shell/registry.js:16`); la auditoría `ui.md` no tiene fila para ella (candidatura de vistas.md). Lo que sigue sin productor es **integrarla en el lector**; la vista misma no está aceptada.

## 12. Mapa de deltas graph_ui que requieren recepción

**Regla** (`dag.yaml` gates `G_UI_READ`, `G_UI_WRITE`, `G_SLDB_WRITE`, `G_SPEC_VIEW`; `reconciliacion.md:27`; `alcance.md:27`): cada delta tiene su propio recibo; `evaluation: per_delta`; `accepted_scope_nodes: []` en todos. El **actor** que registra el acta es el solicitante designado en P01 (`decisiones.md:25`), receptor del repo dueño, al preparar o promover ese delta. El Executor de WS11 no escribe ni commitea actas interrepo y este contrato no afirma que alguna se haya recibido. «Efecto» = qué desbloquea el recibo, según el nodo. **Todas las filas: sin acta registrada** (búsqueda en graph_ui: no existe `runs/subagents/workspace-documental-acceptance/`; `ls` sin resultados).

### 12.1 Lectura: gate G_UI_READ (contrato fuente: este documento)

| ID | Efecto | Actor | Gate | Acta |
|---|---|---|---|---|
| WS13 (agregado) | Se cumple cuando WS13.1-3 cumplen; sin recibo propio | P01 | G_UI_READ | sin acta registrada |
| WS13.1 | Documento/fuente solo lectura, contexto, enlaces, foco | P01 | G_UI_READ | sin acta registrada |
| WS13.2 | Explorador de modelados y no modelados | P01 | G_UI_READ | sin acta registrada |
| WS13.3 | Pestañas, divisiones, historia | P01 | G_UI_READ | sin acta registrada |
| WS14 | Búsqueda por API pública con estados distintos | P01 | G_UI_READ | sin acta registrada |
| WS15 (agregado) / WS15.1 / WS15.2 | Errores de lectura y modo degradado (WS15.1); orientación sin desk (WS15.2) | P01 | G_UI_READ | sin acta registrada |
| WS22 | Board como trabajo navegable en el lector | P01 | G_UI_READ | sin acta registrada |
| WS23 | Procedimiento de rituales y pasos, solo lectura | P01 | G_UI_READ | sin acta registrada |
| WS24 | Vista genérica de conocimiento; no espera ViewDoc | P01 | G_UI_READ | sin acta registrada |
| WS27 (agregado) / WS27.1 / WS27.2 | Diff Git; evidencia declarada/encontrada/verificada | P01 | G_UI_READ | sin acta registrada |
| WS29 | Changes/Integrity (extensión independiente) | P01 | G_UI_READ | sin acta registrada |
| WS35 | Trazabilidad de ejecución (ramal E; además exige G_SCION) | P01 | G_UI_READ (+G_SCION) | sin acta registrada |
| WS40 | Generador del corpus Taller | P01 | G_UI_READ | sin acta registrada |
| WS41 | Lectura segura entre desks | P01 | G_UI_READ | sin acta registrada |

Los IDs son los nodos con `owner_repo: graph_ui` que declaran `G_UI_READ` en `requires` (recomputado leyendo `dag.yaml`: WS13, WS13.1, WS13.2, WS13.3, WS14, WS15, WS15.1, WS15.2, WS22, WS23, WS24, WS27, WS27.1, WS27.2, WS29, WS35, WS40, WS41), que coinciden con `scope_nodes` del gate.

### 12.2 Escritura: solo remisión a WS12

Nodos graph_ui que declaran `G_UI_WRITE` (y `G_WRITE_CONTRACT`): WS19, WS19.1, WS19.2, WS21, WS25, WS25.1, WS25.2, WS26, WS26.1, WS26.2, WS28, WS36, WS39, WS42. Sus huecos de escritura **se remiten a WS12** (H-25) y su contrato de efectos lo produce WS12 (`dag.yaml:723-796`); este contrato no define operación alguna. Receptor: P01. Gates: `G_UI_WRITE` y `G_WRITE_CONTRACT`, con `contract_source: WS12`. Sin acta registrada. En sldb, `G_SLDB_WRITE` cubre WS20 y WS45; también remitido a WS12.

### 12.3 G_SPEC_VIEW (opcional, aparte)

`G_SPEC_VIEW`: alcance WS18 (owner spec2viz), `evaluation: per_delta`, `contract_source: WS11`, receptor P01, `state: pending`, sin acta registrada. Se obtiene al preparar WS18, **no bloquea** la navegación base, ni WS24, ni el manual. La selección que WS18 necesita no está fijada (sección 9).

## 13. Trazabilidad

Cada punto de «Lo que WS11 deberá precisar» de `runs/subagents/20261101-ws09-vistas/result-summary.md`:

| # | Punto | Resolución | Dónde |
|---|---|---|---|
| 1 | Identidad, ruta y modelo opcional del Markdown no modelado (entradas, drawer, issues, FAQ) | **Resuelto como regla**: `(repo, ruta)` con modelo opcional. La implementación (lectura, explorador) es hueco con productor | 2.2; H-01, H-02 |
| 2 | Correspondencia real de origen texto/graph/code, foco compartido, rango dentro de un archivo (F17) | **Resuelto como dominio y tabla**: soportado solo C1-C4; el resto, huecos con productor; **cambio de alcance pendiente para root** respecto de WS13.1 | 6; 6.2; H-03 a H-05b |
| 3 | Selección mínima de ViewDoc y notación (F18b) | **Resuelto como declaración**: no hay evidencia; la promoción de WS18 se detiene | 9 |
| 4 | Vista Specs de Mindmap sin fila en `ui.md` | **Parcialmente resuelto**: la vista existe en graph_ui (`notationView`); integración en el lector sigue siendo candidatura sin productor | 11 (hallazgo) |
| 5 | Campos de `RepositoryDoc`, `InboxNoteDoc`, `MaterializationContractDoc`, `PillDoc`, `StepDoc`, `DeskFAQDoc` | **Resuelto por lectura de modelos** en `DK` (c19c6c0d): `RepositoryDoc` — name, id, path, status, description, tags (`models/repository.py:35-52`); `InboxNoteDoc` — kind (`unclear`/`suggestion`), sender_project, target_project, created_at, status (`open`/`closed`), acknowledged_by, acknowledged_at, title, body (`models/inbox.py:37-61`); `MaterializationContractDoc` — id, title, source_atoms, target_kind, target_identity, intent, validation, tags, provenance (`models/materialization.py:31-58`); `PillDoc` — title, id, status, summary, current_node, history, what, why, when, where, how, how_not, tags (`models/pill.py:59-77`); `StepDoc` — title, id, action, outcome, tags (`models/step.py:31-35`); `DeskFAQDoc` — title, body (`models/faq.py:19-20`). Son campos del modelo, no contrato de UI | 8.6; 13 |
| 6 | Progreso de paso en un procedimiento | **Hueco**: ningún campo ni API (búsqueda `progress`/`done` sin resultados en los modelos); WS23 no marca por leer | H-21 |
| 7 | Aliases y roots autorizados; forma de errores de lectura multidesk | **Resuelto el mecanismo**; los valores no se inventan; el conjunto del desk real es hueco sin productor | 3.2; 8; H-10, H-11, H-16 |
| 8 | Criterio visible error/conflicto/cambio/pérdida de soporte | **Parcial**: la parte de lectura se fija; conflicto y cambio quedan en WS12/WS19 y WS29 | 7.6; H-15 |
| 9 | Forma de errores de API y red (backend ausente, CDN) | **Resuelto como tabla de estados**; mecanismo CDN lo decide WS15.1 | 7 |

