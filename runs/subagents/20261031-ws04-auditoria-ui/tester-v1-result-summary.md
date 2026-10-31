# Informe de Tester — WS04 `auditoria/ui.md`

## 1. Comprobaciones obligatorias

| # | Objeto | Evidencia real leída | Resultado |
|---|---|---|---|
| 1 | 39 filas = 35 graph_ui + WS06/07/10/11 | `ui.md:50-88` (WS13 … WS42 = 35 filas; `ui.md:85-88` WS06/07/10/11 con valor «solo referencia»; `ui.md:90` «Ningún nodo se marca entregado»). Lista de 35 en `tester-facts.log` (dato del Supervisor) coincide ID a ID | PASS |
| 2 | 12 filas con base reutilizada | Ver tabla §2 | PASS (con reserva de commits) |
| 3 | 6 filas de ausencia explícita | Ver tabla §3 | FAIL |
| 4 | SHA-256 del entregable | `testing-handoff.md` y `commands.log` (última línea) y `result-summary.md` declaran `2496605c…2351`; `tester-facts.log` no contiene el hash del entregable y el Tester no puede recalcular bytes | NO VERIFICADO |
| 5a | Dos tickets comparten `serve.py`, `views/workspace/`, `docs/workspace-ui.md` | `task-vista-changes-…md:30-34`, `task-edicion-contextual-…md:30-34` | PASS |
| 5b | Tests declarados inexistentes | `ls ../UIs/graph_ui/tests` sin `test_mindmap_changes.py` ni `test_mindmap_workspace_edit.py` | PASS |
| 5c | `frontends/workspace/` sin commit; `index.html` apunta a `/app.js` ausente | `frontends/workspace/index.html:173` (`/app.js`); `find` en ese directorio: solo `index.html`, `serve.py`, `styles.css`, `__init__.py`, sin `app.js` | PASS |
| 5d | SPEC: 44 candidatas / revisión 5 vs 63 / revisión 8 | `SPEC.md:7`, `SPEC.md:57` («revisión 5: 44 candidatas»); `dag.yaml:2` (`revision: 8`); 63 entradas (dato del Supervisor) | PASS |
| 5e | Hay un enlace roto | `SPEC.md:8` enlaza `../SLDB_1/UIs/graph_ui`, que resuelve a `/home/jp/proyectos/SLDB_1/UIs/graph_ui` (existe). `conversation.md`, `conversation.html`, `mockup.html`, `../kimun`, `../SLDB_1/{deskops,sldb,scion}` existen; `edge_evidence.py` existe en `sldb/src/sldb/store/edge_index/` | **FAIL** |
| 5f | 6.1 y 6.2 abiertas en SPEC, resueltas en el plan | `SPEC.md:105-106` (ítems 1 y 2 de §6); `decisiones.md:25` (P01 extiende Mindmap), `decisiones.md:26` (P02 SLDB/pron+Deskops) | PASS |

## 2. Muestreo de 12 filas con base (contenido)

| Fila | Afirmación comprobada | Evidencia | Resultado |
|---|---|---|---|
| WS13.1 | `_build_code_projection` solo lee `files`/`references` del payload | `workspace_routes.py:431`, `:444-447` | PASS |
| WS13.2 | Catálogo al montar; «Actualizar» recarga nodo, no catálogo | `workspace-view.js:196`, `:294-296` (`loadNode`) | PASS |
| WS13.3 | `updateUrl`, `popstate`, TABS de 3 proyecciones | `workspace-view.js:71`, `:197-198`; `workspace.mjs:5-9` | PASS |
| WS14 | `filterCatalog` por id/título/modelo, filtro local | `workspace.mjs:11-22` | PASS |
| WS15.1 | `catalogError`/`nodeError`, `formatProblems`, import React desde `esm.sh` | `workspace-view.js:56`, `:65`, `:316-317`; `workspace.mjs:63`; `frontends/mindmap/index.html:7` | PASS |
| WS15.2 | `El store no está disponible.` (503) | `workspace_routes.py:105`, `:132` | PASS |
| WS19.1 | `PS.save` compara `expected` y responde 409 «cambió en SLDB» | `persistence.py:101-102` | PASS |
| WS22 | `/api/desk/board`, `/api/desk/task`, `filterTasks`/`counts`, gates | `deskops_routes.py:87-93`; `deskops-view.js:4`, `:36`, `:51-52` | PASS |
| WS23 | Gates con `holds`/`condition`, botón Avanzar, solo íconos RitualDoc/StepDoc | `deskops-view.js:51-52`; `shared/classes.mjs:15`, `:22`; `source/graph.mjs:9-13` | PASS |
| WS24 | `_build_graph_neighborhood`, 1–2 hops, `filterGraphEdges` | `workspace_routes.py:354-356` (BFS `range(1, depth+1)`); `workspace.mjs:83` | PASS |
| WS28 | `POST /api/desk/advance`, 409 por revisión, `advance_task`, texto «cierre desde el CLI» | `deskops_routes.py:94`, `:111-116`; `deskops-view.js:53` | PASS |
| WS29 | `_build_changes_projection` en `serve.py` sucio; sin `doctor`/`drift`/`stores check` | `frontends/workspace/serve.py:280`, `:178`; grep sin coincidencias de esos comandos | PASS |
| WS39 | `template_edit`/`fields_add`/`fields_remove`/`validate`/`promote` y rutas `/api/models/*` | `models_service.py:50-83`; `serve.py:390`, `:413` | PASS |

Columna «commit observado»: solo `a1b2b22`, `f16fcd1`, `134a665`, `daa6400`, `2b801f2` constan en `tester-facts.log`; `087e516`, `e032a84`, `e107b48` y la lista de `PS` no son verificables → NO VERIFICADO para esas atribuciones.

## 3. Muestreo de 6 filas de ausencia explícita

| Fila | Contraprueba buscada | Evidencia | Resultado |
|---|---|---|---|
| WS16 | Acta en `runs/subagents/workspace-documental-acceptance/` | `ls ../UIs/graph_ui/runs/subagents`: no existe esa carpeta. Pero la justificación «solo contiene corridas de agosto 2026» es falsa: hay `20260910-*`, `20261030-deskops-ui/`, `20261031-workspace-ui/` (`ui.md:58`) | **FAIL** |
| WS25.1 | `inbox` en código | Grep en `frontends/mindmap`: única coincidencia `shared/classes.mjs:18` (`InboxNoteDoc`) | PASS |
| WS26 | Rutas/tipos de autoría de tareas | Grep `create.?task|task.?create|/api/tasks` en `frontends/mindmap`: sin coincidencias | PASS |
| WS40 | `tests/fixtures/workspace_documental/` | `ls ../UIs/graph_ui/tests/fixtures`: solo `notation-*` y JSON de notation | PASS |
| WS41 | Raíz múltiple/aliases | `deskops_routes.py:129-136`: `configured_root` único vía `DESKOPS_ROOT` | PASS |
| WS42 | Operaciones split/merge | `workspace_routes.py`: 9 coincidencias de `split`, todas `str.split` (`:254`, `:259`, `:291`, `:299`, `:303`, `:328`, `:399`, `:551`, `:586`); `merge` con 0 coincidencias en ese archivo | PASS (con salvedad) |

## 4. Hallazgos

- **Falso positivo de enlace roto**: `ui.md:155` afirma que los enlaces `../SLDB_1/graph_ui` «no resuelven»; el enlace real (`SPEC.md:8`) es `../SLDB_1/UIs/graph_ui` y sí resuelve. Ningún enlace relativo del SPEC está roto.
- **WS16 (`ui.md:58`)**: «`runs/subagents` solo contiene corridas de agosto 2026» contradicho por 8 directorios posteriores, incluidos `20261030-deskops-ui/` y `20261031-workspace-ui/`.
- **WS42 (`ui.md:84`)**: atribuye coincidencias de `split`/`merge` a `workspace_routes.py`; `merge` no aparece ahí. La conclusión (sin operaciones de split/merge) se sostiene.
- **SHA-256**: coincide en handoff, `commands.log` y `result-summary.md`, pero `tester-facts.log` no lo incluye y no fue recalculado.
- Observación no usada como prueba: `runs/subagents/20261031-workspace-ui/task.txt` declara `task-workspace-multiproyeccion` en `Status: active` / `ritual-execution`, mientras `Board.md:26` y `ui.md:36` la dan por cerrada.

RESULTADO: FAIL
