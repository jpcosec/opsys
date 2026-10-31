# Auditoría UI y trabajo en curso (WS04)

Fecha: 2026-10-31. Auditoría de solo lectura; el único archivo escrito en el repo es este. Los comandos están en `runs/subagents/20261031-ws04-auditoria-ui/commands.log`. Los "no comprobado" llevan su causa. Un commit prueba solo la base que cita, nunca la aceptación ampliada de un nodo.

## 1. Encabezado: repos leídos y universo

| Repo leído | HEAD completo | Líneas de `git status --short` |
|---|---|---|
| deskops (`/home/jp/proyectos/SLDB_1/deskops`) | `215bf624df27db668312af751948d6314cc1de8d` | 5 al leer (4 previas + `runs/subagents/20261031-ws04-auditoria-ui/commands.log`, creado por esta misma corrida) |
| graph_ui (`../UIs/graph_ui`) | `134a6653b8b44423cb0a58ab329383841a9e706f` | 4 |
| softfactory_spec (`/home/jp/proyectos/softfactory_spec`) | sin git (`fatal: not a git repository`) | sin git |

Universo auditado: los 35 nodos con `owner_repo: graph_ui` de `dag.yaml` (lista exacta del TaskDoc, verificada contra `dag.yaml`) más WS06, WS07, WS10 y WS11 como «solo referencia». WS04 no se mapea a sí mismo. Comprobé que ningún otro nodo de `dag.yaml` menciona `graph_ui`.

Plan leído (SHA-256 de los bytes): `desk/drawer/plans/workspace-documental/dag.yaml` `56f0161d0a0c73ae7f52d4de22231b5fddb11aea15b72f20dcd8155d55e001ad` (revision 8, status `final_plan_reviewed`, 63 entradas de tareas); `reconciliacion.md` `8b96ab2cc2d7040ab4d9d919caff7991660ad00b44601c0730fee3246515ce1a`.

Encargo aportado: no hubo documento adicional entregado al ejecutor. La delegación de `runs/subagents/20261031-ws02-04-checkpoint/activation.md` (SHA-256 `4edb27070694895cf288cd2d33c4c82a5e217aa8546d71ff3a96fd478baf9d27`) es el único registrado y no contiene requisitos de mapeo adicionales.

Leyenda de valores de mapeo (según la resolución del coordinador): **base** = capacidad ya en código, con path y commit; **delta** = fila de `reconciliacion.md` (o ticket) que la describe, aún sin cumplir; **ticket** = tarea o entrada de Board de graph_ui; **ausencia explícita** = nada de lo anterior. "parcial" = comportamiento observable citado que cumple solo parte del alcance. Se permiten combinaciones.

Abreviaturas de paths (todos en `../UIs/graph_ui`, commit observado = `git log -- <path>`):
- `WR` = `frontends/mindmap/workspace_routes.py` (a1b2b22). Símbolos en a1b2b22 (`git log -S`): `workspace_nodes`/`workspace_node`, `_build_graph_neighborhood`, `_build_code_projection`, `_inspect_file_reference`, `_check_problems_for_node`.
- `WV` = `frontends/mindmap/views/workspace/node/workspace-view.js` (a1b2b22); `WM` = `.../node/workspace.mjs` (a1b2b22): `TABS`, `filterCatalog`, `filterGraphEdges`, `formatProblems`.
- `DR` = `frontends/mindmap/deskops_routes.py` y `DV` = `frontends/mindmap/views/workflow/deskops/deskops-view.js` (ambos daa6400).
- `PS` = `frontends/mindmap/persistence.py` (git log: 9825eb4 3823dc3 2f4ef31 f739746 d2d8905 e5daa21 90b409c 761e209 c0e31e5 c63b9a3).
- `CD` = `frontends/mindmap/views/documents/map/connect-dialog.js` (087e516).
- `MS` = `frontends/mindmap/models_service.py` (e032a84 bf3dcb2 90b409c 3deed11 e107b48).
Los commits distintos de a1b2b22/f16fcd1/134a665 se listan por `git log` sobre el path citado; no se ampliaron ni leyeron (ninguna referencia actual del Board, de un ticket ni de `reconciliacion.md` apunta a ellos).

## 2. Tareas externas de graph_ui

Tarea externa = todos los archivos de `desk/tasks` de graph_ui. Entradas de Board sin archivo: ninguna (las dos entradas del Board tienen archivo); por eso no hay filas "sin archivo".

| Path (relativo a `../UIs/graph_ui`) | Estado observado | SHA-256 | Alcance (Scope + files) |
|---|---|---|---|
| `desk/tasks/Board.md` (42 líneas; board-graph-ui) | rutea solo 2 tareas, ambas draft; el Notes dice que `task-workspace-multiproyeccion...` está integrada y cerrada | `7ce6afbe9738587f328991e0fa2260c7b01b55acd9b36c418af0912f9d3f7e94` | Enrutar entrega graph_ui; candidatos dependientes de contratos externos en `desk/drawer/tasks/` |
| `desk/tasks/task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento.md` (70 líneas) | draft, current_node ritual-execution, depends_on task-workspace-multiproyeccion (cerrada) | `433ecb51e6dc433b8bb94d0acecc6d508793ae743eae563283aa40c5f8e24377` | Scope: solo graph_ui, endpoint de integridad e impacto, vista Changes, bloque Integrity, footer, pruebas en store temporal. files: `frontends/mindmap/serve.py`, `frontends/mindmap/views/workspace/`, `tests/test_mindmap_changes.py`, `docs/workspace-ui.md` |
| `desk/tasks/task-edicion-contextual-de-relaciones-y-campos-con-control-de-concurrencia.md` (70 líneas) | draft, current_node ritual-execution, depends_on task-workspace-multiproyeccion (cerrada) | `ea6b71f2795eb5f944c75e83ced4c2ba770e260436efae5bbc19aa82192b50c6` | Scope: solo graph_ui, endpoints de mutación de campos/relaciones con before-image, controles en Context y Document, pruebas de persistencia y 409. files: `frontends/mindmap/serve.py`, `frontends/mindmap/views/workspace/`, `tests/test_mindmap_workspace_edit.py`, `docs/workspace-ui.md` |

Observaciones: ninguno de los dos archivos de test que declaran los tickets (`tests/test_mindmap_changes.py`, `tests/test_mindmap_workspace_edit.py`) existe en graph_ui (`ls` los reporta ausentes). Ningún ticket declara estado más allá de draft. El TaskDoc cerrado `task-workspace-multiproyeccion-...` ya no existe como archivo (recibo en `reconciliacion.md`: `git show f16fcd1^:desk/tasks/...`); no se recrea.

Discrepancia observada: `../UIs/graph_ui/runs/subagents/20261031-workspace-ui/task.txt` declara `task-workspace-multiproyeccion-...` con `Status: active`, `Current node: ritual-execution`, mientras `Board.md` (Notes) y `reconciliacion.md` la dan por integrada y cerrada (a1b2b22/f16fcd1/134a665). Es un snapshot de `task.txt` de fecha no verificada; no se cambia nada en graph_ui y no se resuelve cuál es el estado vigente.

Referencia, fuera de `desk/tasks` (no son ticket por definición): candidatos de drawer en `desk/drawer/tasks/`, los tres con `status: deferred`, `files: []`, scope sin redactar (plantilla): `task-adaptador-remoto-hacia-kimun-serve.md` `73c09a1802df30106eef8ab58f1a1a1709f965d2f43aef545a82f2919e65de3a`; `task-edicion-y-anclaje-de-codigo-con-tree-sitter-e-identidad-ante-refactor.md` `7a38c0087949046175eb64246e6568732997497f681bba8f6250216e481c4acc`; `task-prueba-integral-multiagente-opsys-scion-ui.md` `332dc11e863af36e249db9ec114e88bd18a4e94530259bef4ecfead53a5819d2`.

## 3. Tabla de mapeo de nodos graph_ui

Columnas: ID | valor | path o símbolo | commit observado | nota (lo que falta o no se comprobó).

| ID | Valor | Path / símbolo | Commit observado | Nota |
|---|---|---|---|---|
| WS13 | base parcial + delta (fila WS13/WS13.1 de reconciliacion.md) | `WR` (`workspace_node`), `WV` (`WorkspaceView`) | a1b2b22 | Agregado. Sin ticket que lo nombre. Falta lo de sus hijos. |
| WS13.1 | base parcial + delta | `WR.workspace_node`: IR/payload del documento, contexto (`incoming_relations`, `content_hash`, `file_revision`), `_build_code_projection`; `WV`: panel Context | a1b2b22 | Ausente: Markdown sin modelo, fuente cruda íntegra, foco compartido entre representaciones. `_build_code_projection` solo lee `files`/`references` del payload, no el archivo propio del documento. Sin ticket. |
| WS13.2 | base parcial + delta | `WR.workspace_nodes` (`GET /api/workspace/nodes`), `WM.filterCatalog`, `WV.loadCatalog` | a1b2b22 | Catálogo solo de documentos del store. El catálogo se carga al montar; el único botón "Actualizar" recarga el nodo (`loadNode`), no el catálogo: refresco explícito de catálogo no observado. Ausente: Markdown no modelado del desk. Sin ticket. |
| WS13.3 | base parcial + delta | `WV.updateUrl`, handler `popstate` (`git log -S popstate` sobre el repo: a1b2b22 23ca01c 8e3138b; en `WV` solo a1b2b22), `WM.TABS` (Documento/Grafo Local/Código) | a1b2b22 | Los TABS son proyecciones, no pestañas de documentos. Ausente: pestañas por documento, divisiones, foco por documento. Sin ticket. |
| WS14 | base parcial + delta | `WM.filterCatalog` (id/título/modelo, filtro local), `WV` buscador de catálogo | a1b2b22 | Ausente: búsqueda por API (`sldb find`), estados sin resultado/error/degradado distintos, prueba de peticiones. Sin ticket. |
| WS15 | base parcial + delta (fila WS15/WS15.1) | agregado de WS15.1 y WS15.2 | a1b2b22 | Ver hijos. |
| WS15.1 | base parcial + delta | `WV` (`catalogError`, `nodeError`, errores por proyección), `WM.formatProblems`, `WR._check_problems_for_node` | a1b2b22 | Hay errores de catálogo, nodo y proyección. Ausente: diagnóstico de fallo CDN (el `index.html` de mindmap importa React desde `esm.sh`, sin manejo observado), reintento que conserve foco/historia no comprobado (no se ejecutó la UI). Sin ticket. |
| WS15.2 | base parcial + delta | `WR.workspace_node` lanza `El store no está disponible.` (503) | a1b2b22 | Ausente: orientación de proyecto sin desk y el comando `deskops init <ruta>` (grep sin resultados en `views/workspace` ni `WR`). Sin ticket. |
| WS16 | ausencia explícita | — | — | Validación humana: no hay acta ni carpeta `runs/subagents/workspace-documental-acceptance/` en graph_ui (`runs/subagents` tiene corridas de 2026-08 a 2026-10-31 (p. ej. `20261030-*`, `20261031-*`), pero ninguna es `workspace-documental-acceptance/` (`ls` con ese patrón: no existe)). |
| WS19 | ticket (draft) + delta (fila WS19/WS21) + base parcial fuera del workspace | `task-edicion-contextual-...` (draft); `PS.save` (409 por `viewRevision` y por `expected` de payload); `CD` | PS: ver leyenda; CD: 087e516 | Agregado. La edición con 409 existe solo en el KB map (`/api/save`), no en la vista workspace; los endpoints y pruebas del ticket no existen. |
| WS19.1 | ticket (draft) + delta + base parcial fuera del workspace | `PS.save`: compara `expected` contra el payload actual y responde 409 `cambió en SLDB`; `frontends/mindmap/dialogs/conflict-dialog.js` (087e516) | PS: ver leyenda | Ahí el CAS compara el payload completo, no un hash de revisión del documento; no es el contrato WS12. Ausente en workspace: campos editables, `tests/test_mindmap_workspace_edit.py`. |
| WS19.2 | ticket (draft) + delta + base parcial fuera del workspace | `CD.ConnectDialog` (alta de relación sobre campos de referencia del modelo, queda pendiente hasta guardar), `PS.save` | CD: 087e516 (`git log -S ConnectDialog`: 087e516 c63b9a3) | Ausente: baja de relación y edición desde Context/Document del workspace; no hay verificación de relación "permitida por contrato WS12". |
| WS21 | delta (fila WS19/WS21) + ausencia explícita de código | — | — | Ningún ticket habla de `source_mode`. Sin código de fuente editable en workspace. Depende de G_SOURCE/WS20 (fuera de graph_ui). |
| WS22 | base parcial + delta | `DR` (`GET /api/desk/board`, `/api/desk/task`), `DV` (lista de tareas del Board con filtro por estado y detalle con gates, `filterTasks`, `counts`) | daa6400 | Lista y detalle sí, leyendo deskops. Ausente: tablero agrupado, dependencias navegables, apertura de TaskDoc en el lector workspace, pills/átomos referenciados. Sin ticket. |
| WS23 | delta (fila WS23) + base parcial mínima | `DV` muestra gates con `holds` y condición; el payload/lifecycle de un documento es navegable en `WV` | daa6400, a1b2b22 | La vista DV tiene botón Avanzar (acción), fuera del carácter de solo lectura de WS23. Ausente: renderer de RitualDoc/StepDoc/pasos y fuentes (solo hay íconos en `shared/classes.mjs` y la gramática de referencias en `source/graph.mjs`, sin vista de procedimiento). Sin ticket. |
| WS24 | base parcial + delta | `WR._build_graph_neighborhood` (aristas entrantes/salientes, 1–2 hops), `WV` (selector de profundidad, filtro por tipo `WM.filterGraphEdges`, tarjetas que reorientan el workspace) | a1b2b22 | Ausente: Markdown no modelado, backlinks calculados con la API de grafo de sldb según auditoria/infraestructura.md (no leída por esta tarea), clasificación por tipo y tags más allá de `context.metadata.tags`. Sin ticket. |
| WS25 | ausencia explícita (agregado) | — | — | Sin código de inbox, ack ni captura en workspace. |
| WS25.1 | ausencia explícita | — | — | `grep -i inbox` en `frontends/mindmap` solo halla el ícono de `InboxNoteDoc` en `shared/classes.mjs`; no hay lectura ni ack. |
| WS25.2 | ausencia explícita (adyacente no mapeado) | — | — | Existe `quickCapturable`/`quick-create-dialog.js` (707ea86, 087e516), que crea documentos de modelos capturables en el KB map. No se afirma que cumpla captura a drawer o protoátomo: destino distinto, no comprobado. |
| WS26 | ausencia explícita (agregado) | — | — | Sin autoría de tareas ni enrutamiento Board desde UI. |
| WS26.1 | ausencia explícita | — | — | Ídem. |
| WS26.2 | ausencia explícita | — | — | Ídem. |
| WS27 | delta (fila WS27/WS27.1) — agregado | — | — | Ver hijos. |
| WS27.1 | delta + ausencia explícita de código tracked | — | — | Code preview (`WR._inspect_file_reference`) no es diff. En el árbol sucio de `frontends/workspace/serve.py` hay `_read_git_history` y `_git_status_map`; ese archivo está sin commitear (ver sección 4) y no cumple el alcance (sin referencias de TaskDoc, sin diff por repo). |
| WS27.2 | delta + base parcial | `DV`/`DR.detail`: sección "Evidencia declarada" muestra `closeout_evidence` del payload | daa6400 | Solo la parte "declarada". Ausente: encontrada y verificada (`deskops closeout verify`), abrir soporte. |
| WS28 | delta + base parcial | `DR` `POST /api/desk/advance` (revisión de Board+tarea, 409 ante revisión obsoleta, llama `advance_task`; `git log -S advance_task` en repo: 2b801f2 daa6400 6561d2e 333bb37 f241471), texto en `DV`: "El cierre se gestiona desde el CLI" | daa6400 | `advance` no es verify ni handoff de cierre. Ausente: `closeout verify` por UI y refresco tras cierre externo. |
| WS29 | ticket (draft: Changes) + delta (fila WS29) + base parcial | `task-vista-changes-...`; `WR._check_problems_for_node` y `WM.formatProblems` (problemas del índice de aristas y hashes de contexto en el panel Context) | a1b2b22 | Ausente en tracked: vista Changes, Integrity, `sldb stores check`/`deskops doctor`/`deskops drift check`; `tests/test_mindmap_changes.py` no existe. Ver el `serve.py` sucio en sección 4: tiene `_build_changes_projection` (git status + vecindad 1–2 hops) y ninguna llamada a esos tres comandos (grep de `doctor|drift|stores check` sin resultados). |
| WS30 | ausencia explícita | — | — | Validación humana; sin acta. |
| WS35 | ausencia explícita | — | — | Sin trazabilidad tarea-intento-mensaje. Adyacente no mapeado: panel de workers (`shell/workers-panel.js`, `/api/workers` en `frontends/mindmap/serve.py`), no comprobado que cubra el alcance. |
| WS36 | ausencia explícita | — | — | Sin adaptador de despacho ni UI de intervención. |
| WS37 | ausencia explícita | — | — | Candidato de drawer `task-prueba-integral-multiagente-opsys-scion-ui.md` (deferred, sin scope redactado) es el nombre afín; no es ticket y su alcance no está escrito. |
| WS39 | base parcial | `MS` (`template_edit`, `fields_add`, `fields_remove`, `validate`, `promote`; `git log -S "def promote"`: e107b48), `frontends/mindmap/dialogs/class-dialog.js` (e032a84 087e516), `views/models/diagram/` (a64a924 363fe9b be1d695 72c7cc6 0d00ab0 0cf1623 087e516 1c57de6 e107b48), rutas `POST /api/models/*` en `frontends/mindmap/serve.py` | ver paths | Editor de Schema existente en vista Schema. Ausente: acceso desde el panel Context del lector WS13. `reconciliacion.md` no tiene fila para WS39. Sin ticket. |
| WS40 | ausencia explícita | — | — | No existe `tests/fixtures/workspace_documental/` ni script de seed (`ls tests/fixtures`). `frontends/mindmap/fixtures/kb-small.json` es otro fixture, no mapea. |
| WS41 | ausencia explícita | — | — | `DeskRoutes` y `configured_routes` resuelven una única raíz (`DESKOPS_ROOT` o el padre del store); no hay aliases ni lectura entre desks. |
| WS42 | ausencia explícita | — | — | Sin operaciones split/merge/proto typing ni inspección de materializaciones en UI (`Materialization` solo aparece como ícono en `shared/classes.mjs`; `workspace_routes.py` no contiene `merge` y sus `split` son `str.split` de identificadores, no operaciones de átomos). |
| WS06 | solo referencia | — | — | Mantiene la matriz de reconciliacion.md. |
| WS07 | solo referencia | — | — | Decisiones; `decisiones.md` P01 designa al solicitante como responsable de aceptación graph_ui. |
| WS10 | solo referencia | — | — | Manual; consume esta auditoría. |
| WS11 | solo referencia | — | — | Contrato de navegación; consume rutas reales citadas aquí. |

Nodos con "delta" cuya fila de `reconciliacion.md` los nombra: WS13/13.1, 13.2, 13.3, 14, 15/15.1, 15.2, 19 e hijos, 21, 22, 23, 24, 27/27.1, 27.2, 28, 29. Nodos sin fila de reconciliación ni ticket que los nombre: WS16, WS25 (y .1/.2), WS26 (y .1/.2), WS30, WS35, WS36, WS37, WS39, WS40, WS41, WS42. Ningún nodo se marca entregado: ninguno cumple su aceptación ampliada con evidencia propia.

## 4. Sesiones y trabajo en curso

### 4.1 Paneles herdr (`herdr pane list`, lectura)

Cada fila es lo que muestra el comando; "estado" es `agent_status`. No se atribuye autoría de trabajo a ningún pane. Es coordinación, no autoridad.

| Pane | Agente | Estado | cwd | Título del terminal |
|---|---|---|---|---|
| w3Y:p1 | claude | working | `/home/jp/proyectos/SLDB_1` | fabrica-local-deskops |
| w3Y:p2 | codex (label "deskops ui") | done | `/home/jp/proyectos/SLDB_1/deskops` | Revisa y crea UI para DeskOps |
| w3Y:p4 | claude | done | `/home/jp/proyectos/SLDB_1` | DAG workspace-documental de Deskops |
| w3Y:p6 | pi | done | `/home/jp/proyectos/SLDB_1` | π - SLDB_1 |
| w3Y:p7 | agy | done | `/home/jp/proyectos/SLDB_1` | jp@johanes: ~/proyectos/SLDB_1 |
| w3Y:p8 | claude | idle | `/home/jp/proyectos/SLDB_1/deskops` | Claude Code |
| w43:p1 | claude | idle | `/home/jp/proyectos` | Herdr entre agentes de pestañas |
| w43:p2 | agy | working | `/home/jp/proyectos` | jp@johanes: ~/proyectos |
| w43:p3 | (sin agente) | unknown | `/home/jp/proyectos` (foreground `.../softfactory_spec`) | Yazi: softfactory_spec |
| w41:p2, w41:p3, w41:p9 | claude/pi/shell | unknown/done/unknown | `/home/jp/AntonIA/repos/legacy/chatbot` | fuera de los tres repos leídos |
| w44:p1, p4, p5, p7, p8 | claude/pi/agy/shell/codex | working/idle/idle/unknown/idle | `/home/jp/AntonIA/repos/legacy/mepu` | fuera de los tres repos leídos |

Ningún pane tiene cwd en `../UIs/graph_ui`. Ausencia de sesión en graph_ui: registrada. `activation.md` declara por su cuenta que la delegación llegó al pane `w3Y:p1` por instrucción transmitida desde `w3Y:p2`; es lo que dice ese documento, no algo comprobado aquí. Qué hace cada pane no se leyó (no se enviaron mensajes ni se leyó su contenido): no comprobado.

### 4.2 Rutas sucias por repo (sin atribución a pane ni a sesión)

deskops (`git status --short`, 5 líneas al leer):
- `M desk/inbox/20261029-122044-suggestion-declare-write-ya-conserva-los-globs-autorados.md`: sin atribución.
- `M desk/inbox/20261029-122115-suggestion-traspaso-de-sesi-n-scion-piloto-coordinador-de-deskops-en-marcha.md`: sin atribución.
- `?? desk/drawer/tasks/task-integracion-opsys-kimun-frontera-de-autoridad-y-modelos-del-desk.md`: sin atribución.
- `?? desk/inbox/20261029-213633-unclear-advance-to-superseded-no-cambia-status.md`: sin atribución.
- `?? runs/subagents/20261031-ws04-auditoria-ui/commands.log`: evidencia de esta corrida.
Ninguna se cita como evidencia de una fila; por eso no llevan hash.

graph_ui (`git status --short`, 4 líneas):
- `?? desk/inbox/20261020-113025-suggestion-sldb-cambia-la-salida-las-alertas-dejan-de-hacer-fallar-y-nunca-son-silenciosas.md`: sin atribución.
- `?? desk/inbox/20261020-122513-suggestion-contrato-de-lectura-paquetes-uml-en-diagramas-de-clase-spec2viz-84686c3.md`: sin atribución.
- `?? desk/inbox/20261020-135650-suggestion-sldb-en-main-procedencia-por-documento-pol-tica-por-store-y-alertas-que-no-fallan.md`: sin atribución.
- `?? frontends/workspace/`: sin atribución. Citado como evidencia en WS27.1 y WS29, por eso se fija su contenido leído:

| Archivo sucio | SHA-256 |
|---|---|
| `frontends/workspace/index.html` | `11b6cf5a589c6611f390ceee2e3e0449a4a37c39c19141a69315aadfe1cb6ad6` |
| `frontends/workspace/serve.py` | `6c3b7cd63e7c14ac862af2ca9caeeff9b8376bfa3818e25c8a67cc62a3a95ada` |
| `frontends/workspace/styles.css` | `ff1df3f201b05fa315e221de9d90e20c5a7793ede025b378d51af057427ab109` |
| `frontends/workspace/__init__.py` | `861874dc0662a7d0b5915b2277222295e034fc002c94fa5ef25802aa9a39b559` |

Qué es lo observable de `frontends/workspace/` (sin commit; `git ls-files` devuelve 0): un servidor paralelo de solo lectura (`WorkspaceService`, puerto 8090 por defecto) que reutiliza `mindmap.workspace_routes` y `mindmap.deskops_routes`; añade `/api/workspace/overview`, catálogo con categorías, `sections_prose`, una proyección `changes` (git status del repo + vecindad 1–2 hops + `problems_report`), lectura de workers, runs de subagentes e historia Git. `index.html` referencia `/app.js` y el directorio no contiene `app.js` (el handler sirve solo `frontends/workspace/`), y el buscador global `global-search` no tiene handler en esos archivos: el cliente aparece incompleto. No es ticket de graph_ui: ninguno de los dos TaskDoc ni de los de deskops lista `frontends/workspace/` en `files`. No se mapea a un nodo como entregado.

### 4.3 Solapamientos

| Solapamiento | Tipo | Detalle |
|---|---|---|
| `task-vista-changes-...` vs `task-edicion-contextual-...` | Rutas en `files` de dos TaskDoc (reclamos observables) | Comparten `frontends/mindmap/serve.py`, `frontends/mindmap/views/workspace/` y `docs/workspace-ui.md`; difieren solo en el archivo de test. Ambas draft en el mismo Board, mismo átomo y misma dependencia. Ninguna tiene sesión activa nombrada en el Board. Sin dos reclamos de sesión: es solapamiento declarado entre tickets, no entre sesiones. |
| Tareas WS02/WS03/WS04 de deskops entre sí | — | `files` distintos (`auditoria/deskops.md`, `auditoria/infraestructura.md`, `auditoria/ui.md`): sin solapamiento. |
| Nodos del plan vs tickets | Contención de ruta (potencial, no solapamiento de sesión) | Los `output_scope` de WS13.1, WS14, WS19.x, WS24, WS27.x, WS29, entre otros, caen bajo `frontends/mindmap/views/workspace/`, que ya reclaman los dos tickets. Los nodos no son TaskDoc ni declaran `files`: se dice, no se afirma conflicto. WS19.x y WS29 son además la misma capacidad que cada ticket. |
| `frontends/workspace/` (sucio) vs tickets | Sin reclamo | Ningún TaskDoc lo reclama; reutiliza código bajo `frontends/mindmap/`. Solapamiento no afirmable (menos de dos reclamos observables). |
| Sesiones vs rutas sucias | Sin dos reclamos observables | No hay pane en graph_ui y ningún campo `files` reclama las rutas sucias de ninguno de los tres repos. |

Board de deskops (`desk/tasks/Board.md`): rutea WS02, WS03 y WS04 (draft). Board de graph_ui: los dos tickets draft. Candidatos sin archivo en tasks ni en Board: los tres de `desk/drawer/tasks/` de graph_ui, deferred.

## 5. SPEC externo

Archivo: `/home/jp/proyectos/softfactory_spec/SPEC.md` (106 líneas), SHA-256 `373159eaae74c75aef105091f1c92d20331a60c5e9662db30256b1bd690ee789`. Carpeta sin git. Criterio: coincidencia = el plan lo cubre; discrepancia = lo cubre distinto; ausencia = parte de la sección sin contraparte en el plan. El plan = `dag.yaml` + `reconciliacion.md`.

Observaciones de la cabecera del SPEC (antes de `## 1`): dice plan de 44 candidatas WS01–WS44, "revisión 5", commit `e80e8c0`, 15 compuertas, `execution_authorized=false`. Observado: `dag.yaml` revision 8, 63 entradas (44 WSnn más 19 subnodos), 15 gates, `execution_authorized: false`; `e80e8c0` existe como commit en deskops. Discrepancia de cifra y revisión. Enlaces relativos comprobados con `test -e` desde la carpeta del SPEC: `../kimun`, `../SLDB_1/deskops`, `../SLDB_1/sldb`, `../SLDB_1/scion`, `../SLDB_1/UIs/graph_ui`, `conversation.md`, `conversation.html` y `mockup.html` resuelven; ninguno está roto (`../SLDB_1/graph_ui`, sin `UIs/`, no es el enlace del SPEC).

| Sección ## de SPEC.md | Coincidencias | Discrepancias | Ausencias |
|---|---|---|---|
| `## 1. Objetivo y Principio Rector` (1.1, 1.2) | Un objeto lógico con proyecciones Documento/Grafo/Código/Cambios (`reconciliacion.md`: base real y WS13–WS29); vecindad 1–2 hops (WS24); relaciones editables (WS19.2). | El objetivo "interfaz entre el grafo de Kimun y los archivos" no es el del plan: la línea base es Mindmap + SLDB/pron + Deskops, Kimun fuera (P02). | No hay contraparte para el time slider histórico ni para "trazabilidad de corridas" como proyección del grafo (WS35 es Scion, opcional). |
| `## 2. Capas del Sistema y Fronteras de Autoridad` | Cuatro capas con dueños `sldb`, `deskops`, `scion`+`deskops`, `graph_ui`; `deskops` gobierna el flujo (plan: `owner_repo`). Concurrencia: la nota sobre múltiples escritores coincide con P03. | La capa Workspace UI cita `/documents/map` y `/workflow/deskops` como implementación; el workspace real es la vista `workspace`/`node` (id `node` en `WV`, `docs/workspace-ui.md` usa `/workspace/node`). SPEC propone coordinador único como objetivo; el plan fija P03: UI de solo lectura o handoff hasta canal con autoridad compartida probado. | Nada del plan sobre `kimun serve` (C2) ni anillos S/M/G: fuera de alcance por P02. |
| `## 3. Estado de Incertidumbres Técnicas (U01–U09)` | U06 (409 por hash en HTTP): observado `PS.save` 409 y `DR` revisión; coincide con la base. U08 (deskops autoridad de flujo): coincide con P03/G_CLOSEOUT. U09 (RunDoc): coincide con WS32/33. U04 (staleness requiere consumidor con línea base): coincide con WS29. | U06: SPEC dice "hash de revisión"; el KB map compara el payload (`expected`) y la vista deskops usa revisión de Board+tarea, no un hash de documento único. | U01–U03, U05, U07: sin contraparte directa en el plan (son internas de kernel/sldb). |
| `## 4. Mapeo del DAG Original (K/O/S/E)` | K07→WS11/12, K09→WS19–WS21, K10→WS13/22–24, K11/K13→WS19/21, K14→WS13–WS28, K15→WS19–21/28/30, S01–S02→WS05/32/33, E01→WS37: los IDs y títulos existen en `dag.yaml` con ese sentido. | K01–K06→WS02–WS05: WS02–WS04 son auditorías, WS05 es Scion, no "auditorías de kernel/Tree-sitter/Merkle". K12 (Tree-sitter): el plan lo excluye (candidato diferido en drawer). K09: "cliente C2 en `kimun serve`" no está en el plan (Kimun fuera). | K08 (sincronización grafo-archivos) y O02 (Opsys–Kimun): el plan los cubre por WS12 y por tarea drawer deskops, no por nodos propios. |
| `## 5. Brechas, Divergencias y Viabilidad Técnica` (5.1–5.4) | 5.1.2: Changes está en WS29 dependiendo de WS15 y WS24 (coincide con `dag.yaml`). 5.2: `edge_evidence.py` estampa `ref_hash` y `contract` (verificado en `sldb/src/sldb/store/edge_index/edge_evidence.py`); la línea base de evidencia no existe en graph_ui (grep de `baseline` solo halla la línea base del editor, no de evidencia). 5.3: Kimun referencia, no dependencia (P02). 5.4: UF01–UF10, manual WS31/38 existen en el plan. | 5.1.3: SPEC dice que `+ Add relation` está fuera del plan; el plan sí cubre alta/baja de relaciones permitidas por contrato (WS19.2), aunque no con el nombre ni sobre aristas sin archivo. 5.3: SPEC deja la adopción diferida a WS07; WS07 es registro de decisiones y las resuelve (P02). | 5.1.1: time slider histórico sin nodo (grep de "slider" sin resultados en el plan). 5.1.3: aristas sin archivo físico, sin contraparte. 5.2: resolución de impacto a nivel de documento (hash del `_owner`) no se menciona en WS29. |
| `## 6. Decisiones Técnicas Abiertas para Definición del Dueño` | 6.2: extender `frontends/mindmap` (WS13+) está decidido en P01. 6.1: producto = Workspace Documental de Deskops sobre sldb/pron (P01/P02). | 6.1 y 6.2 figuran como abiertas en SPEC y como resueltas en el plan (G_PRODUCT satisfied). 6.5: SPEC habla de tres TaskDoc en el Board de graph_ui; hoy el Board enruta dos (el de multiproyección está cerrado, a1b2b22/f16fcd1/134a665) y `reconciliacion.md` manda integrar deltas en el ticket vigente o en tarea atómica propia (no devolver al drawer). | 6.3 (D0, identidad estructural) y 6.4 (jerarquía de modelos de evidencia): sin nodo ni decisión en el plan. |

Nota final, temas del plan que SPEC no menciona: gates G_* (UI_READ/WRITE, SLDB_WRITE, WRITE_CONTRACT, CLOSEOUT, SOURCE, HUMAN_*), `source_mode` (P04), generador de corpus Taller (WS40) y lectura entre desks (WS41, UF08), captura/triage de inbox (WS25) y autoría de tareas con capa lista (WS26), diff/evidencia/handoff de cierre (WS27/28), sin desk (WS15.2/UF10), validaciones humanas (WS16/30/37), recepción por delta (P01), y el contrato de closeout (59244c9, 1fefa97).

## 6. No comprobado y límites

- No se ejecutó la UI ni sus pruebas (esta tarea es de lectura): comportamiento de runtime de la UI (reintentos, foco, historia al volver) no comprobado; las afirmaciones se basan en el código leído.
- No se leyeron `auditoria/deskops.md` ni `auditoria/infraestructura.md` (son de WS02/WS03): la correspondencia de WS24 con la API de grafo de sldb y de WS14 con `sldb find` queda sin contrastar.
- El contenido de los commits fuera de a1b2b22/f16fcd1/134a665 no se leyó; sus hashes se listan por `git log` sobre el path.
- Qué hace cada pane de herdr no se verificó.
