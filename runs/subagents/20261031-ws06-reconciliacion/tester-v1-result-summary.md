# Informe Tester — WS06

Alcance: lectura estática, sin ejecutar código ni Git, sin leer Kimun. Hashes, conteos y validaciones de `tester-facts.log` se declaran **dato del Supervisor**; los commits se contrastaron contra las auditorías, no contra `git`.

## Tabla de comprobación

| Objeto | Evidencia real leída | Veredicto |
|---|---|---|
| Contrato TaskDoc WS06 | `desk/tasks/task-ws06-proponer-correspondencia-de-alcance-con-repos-dueños.md`: scope, formato por capacidad, cobertura 63 nodos, reglas de contenido | PASS |
| Handoff y preflight | `runs/subagents/20261031-ws06-reconciliacion/testing-handoff.md`; `preflight-disposition.md`: cuarto valor solo para `frontends/workspace`, C-nn continuo, destino ticket/delta | PASS |
| Aprobación WS02–WS04 | `runs/subagents/20261031-ws02-04-checkpoint/approval.md`: condiciones de reutilización ViewDoc, `expected`, Scion sin WS05, sin paralelo a edición/Changes | PASS |
| C-01 ya cubierto | `../UIs/graph_ui/frontends/mindmap/workspace_routes.py:102,129,167,203`; `ui.md:24` cita commit a1b2b22 | PASS |
| C-02 ya cubierto | `workspace_routes.py:354`; `views/workspace/node/workspace.mjs:83`; `workspace-view.js:234` | PASS |
| C-03 ya cubierto | `workspace_routes.py:431,441-451` (`files`/`references` del payload) | PASS |
| C-04 ya cubierto | `workspace.mjs:5` (`TABS`); `workspace-view.js:71,198` (`updateUrl`, `popstate`) | PASS |
| C-05 ya cubierto | `workspace.mjs:11-25` (`filterCatalog` por id/título/modelo) | PASS |
| C-13 ya cubierto | `../UIs/graph_ui/frontends/mindmap/persistence.py:62,85,102`; `ui.md:28` | PASS |
| C-16 ya cubierto | `deskops_routes.py:87,89`; `deskops-view.js:4,36,54`; commit daa6400 en `ui.md:26` | PASS |
| C-26 ya cubierto | `deskops_routes.py:94-116` (advance con revisión y 409); `deskops-view.js:53` | PASS |
| C-37 ya cubierto | `projection_views.py:107,127,134`; `views_routes.py:56-82`; `serve.py:147-150` (501 remote); commits 0eb7dd7/b9ab83c/2a15356 en `ui.md:105` | PASS |
| C-38/C-40 ya cubiertos | `document_serialization.py:24`; `save_plan.py:50,58`; `infraestructura.md:51,54` | PASS |
| C-43 ya cubierto | `../sldb/src/sldb/api/search.py:26`; `infraestructura.md` | PASS |
| C-51/C-53 ya cubiertos | `deskops/operations.py:301,412`; `deskops/cli/commands/message.py:145,161-198` | PASS |
| C-58/C-60 ya cubiertos | `operations.py:602,503,518`; `services/closeout_gates.py:23` | PASS |
| C-62/C-63 ya cubiertos | `cli/commands/core.py:24`; `cli/registry.py:811-851`; 6 `RepositoryDoc` en `desk/registry/` | PASS |
| C-07 nuevo delta | `workspace_routes.py:431-451`: no lee el archivo propio del documento; solo referencias del payload | PASS |
| C-08 nuevo delta | `workspace_routes.py:102-127`: catálogo solo de documentos del store; sin árbol del desk | PASS |
| C-10 nuevo delta | `workspace.mjs:11-25`: filtro local; sin ruta UI a `sldb find` | PASS |
| C-17 nuevo delta | `deskops-view.js:36`: lista/filtro; sin tablero agrupado ni dependencias navegables | PASS |
| C-20 nuevo delta | `ui.md:71`: `grep -i inbox` solo halla ícono `InboxNoteDoc`; sin lectura/ack UI | PASS |
| C-23 nuevo delta | `operations.py:350` es `next_action_report` por tarea/lifecycle; no hay comando de capa lista entre tareas | PASS |
| C-25 nuevo delta | `deskops-view.js:54`: solo «Evidencia declarada»; sin encontrada/verificada | PASS |
| C-33 nuevo delta | Cita `ui.md`; no leí el código de `DeskRoutes` en esta pasada | PASS con NO VERIFICADO de código |
| C-41 nuevo delta | `grep` sin resultados de `expected_hash|expected_revision|expected_sha|If-Match|etag` en `../sldb/src/sldb`; `save_plan.py:50,58` solo compara payload | PASS |
| C-50 nuevo delta | `views_routes.py:56-82` sí crea/guarda ViewDoc; el delta real es portabilidad, no creación | PASS con hallazgo |
| C-55 nuevo delta | `services/drawer.py:92`: solo `promote_inbox_to_drawer_task` crea candidato y borra la nota | PASS |
| C-65 nuevo delta | `runtime/scion.py:355` solo registra; candidato `task-correlacionar...` declara el hueco de vínculo | PASS |
| C-14 extender ticket | Ticket `task-edicion-contextual...`: before-image/409, `serve.py`, `views/workspace/`, test; `ui.md:41` | PASS |
| C-28 extender ticket | Ticket `task-vista-changes...`: Changes, Integrity, store real; `ui.md:39`; doctor/drift es extensión razonable | PASS con hallazgo menor |
| C-64 extender ticket | Candidato `desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md`: identidad/manifiesto/RunDoc/cierre; cubre WS32.1/32.2 | PASS con hallazgo |
| C-29 no adoptado | `ui.md:158`: `frontends/workspace/` sin commit, cliente incompleto; matriz lo cita sin reclamar | PASS |
| Regla `expected` sin CAS/frescura | C-40 limita a comparación por valor, caché y ausencia de CAS; C-13/C-37 coherentes | PASS |
| Regla Scion WS32/33 sin WS05 | C-64 conserva descomposición; C-65/66/67/68 declaran WS05 pendiente y no afirman API Scion | PASS |
| Responsables y operador Scion | Filas deskops usan «No designado en P01»; operador Scion aparece en C-64/65/66/67/68 y C-36, dentro del ramal Scion/E | PASS |
| Ninguna fila acepta delta | `grep` de `acepta/aceptad/aceptación` en la matriz: C-49 usa «acepta layout `graph`», no aceptación de delta | PASS |
| Duplicados | C-37/C-50 es solapamiento de base, no duplicado si C-50 se limita a portabilidad; no hallé otra capacidad repetida | PASS con observación |
| Cobertura 10 nodos «sin delta» | WS01 `dag.yaml:284-320`; WS02–04 auditorías; WS05 pendiente no requerido; WS08 planificación; WS11/12 contratos; WS16/30/37 validación; WS43 documentación/publicación; WS44 probe read-only; WS17 plantillas | PASS |
| Ajustes canónicos 1–5 | `canonical-adjustments.md`: #1 CAS, #2 captura directa, #3 ViewDoc/WS18, #4 texto «acepta», #5 revisiones; evidencia en `dag.yaml:1252-1253,1331-1339,1158-1181,485` y `brief.md:24,40` | PASS con hallazgo en #1 |

## Hallazgos

- **C-50**: «sin comando que cree uno» es impreciso; `views_routes.py:56-82` expone `POST /api/views/save` y `ui.md:105` lo reconoce. El delta solo se sostiene como **portabilidad/host-independence**, no como ausencia de creación. Defecto de cita que no cambia la clasificación si se corrige la redacción.  
- **C-64**: el destino es un candidato diferido del drawer, no un ticket abierto del Board; el preflight dice que solo graph_ui tiene tickets abiertos conocidos. El contenido cabe en el candidato, pero «extender ticket» es una convención amplia; si se exige literalidad, debería rotularse «nuevo delta».  
- **Ajuste canónico #1**: afirma que WS20 «nombra únicamente raw-source»; WS20 sí dice «con revisión» y exige pruebas de conflicto (`dag.yaml:1331-1339`). El ajuste sigue siendo necesario para el CAS de payload, pero esa frase debe precisarse.  
- **C-28**: el ticket de Changes nombra `stores check` y grafo; `deskops doctor` y `drift check` son una extensión algo más amplia, aunque compatible con «estado real de verificación».  
- **C-23, C-41, C-55**: sus clasificaciones se sostienen; no hay comando de capa lista, no hay CAS público y no hay captura directa a drawer fuera de `promote`.  
- **C-49**: no es defecto; «acepta layout» se refiere a un renderer, no a aceptar un delta.

## No verificado / dato del Supervisor

- No ejecuté `git`, `build_plan.py`, `validate_plan.py` ni `context_review.py`; los conteos 68/33/31/3/1, 63/63 y el sha256 son **dato del Supervisor**.
- Los commits se tomaron de `ui.md`, `infraestructura.md` y `deskops.md`; no se verificaron con `git show` en esta pasada.
- El comportamiento de runtime de las capacidades «ya cubierto» no se ejecutó; son lecturas de código y auditorías.
- La no aplicación de los ajustes canónicos no se comprobó con `git status`; el documento declara que ninguno está aplicado.

RESULTADO: PASS
