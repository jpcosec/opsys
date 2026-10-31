# Informe Tester v2 — WS04 `auditoria/ui.md`

## A. Correcciones de la ronda 1

| Objeto | Evidencia real leída | Resultado |
|---|---|---|
| Enlaces / ya no se afirma enlace roto | `ui.md:157` afirma que `../kimun`, `../SLDB_1/deskops`, `../SLDB_1/sldb`, `../SLDB_1/scion`, `../SLDB_1/UIs/graph_ui`, `conversation.*` y `mockup.html` resuelven, y que «ninguno está roto»; `ls /home/jp/proyectos` muestra `kimun/` y `ls /home/jp/proyectos/SLDB_1` muestra `deskops/`, `sldb/`, `scion/`, `UIs/`. `grep "roto\|no resuelven"` solo halla `ui.md:157` | PASS |
| WS16 | `ui.md:60` ya no dice «solo agosto»: dice corridas de 2026-08 a 2026-10-31 y que no existe `workspace-documental-acceptance/`. `ls runs/subagents`: 23 entradas, de `20260820-*` a `20261031-*`, ninguna `workspace-documental-acceptance/` | PASS |
| WS42 | `ui.md:86`: «`workspace_routes.py` no contiene `merge` y sus `split` son `str.split`». `grep merge` en `workspace_routes.py`: 0 coincidencias; `split` en `:254,259,291,299,303,328,399,551,586` | PASS (ver hallazgo menor 2) |
| Atribuciones de commit | `ui.md:22-29` cita `a1b2b22/f16fcd1/134a665/daa6400/2b801f2/087e516/e032a84/e107b48`; los 8 aparecen en `tester-v2-facts.log` con asunto compatible. Los hashes de la lista `PS` y otros (`707ea86`, `c63b9a3`, `a64a924`, etc.) no están en el log | PASS con reserva: `PS` y varios paths quedan NO VERIFICADO |
| Discrepancia `task-workspace-multiproyeccion` | `ui.md:42` registra la discrepancia. Fuente: `../UIs/graph_ui/runs/subagents/20261031-workspace-ui/task.txt:3-4` (`Status: active`, `Current node: ritual-execution`); `Board.md:35` la da por «integrada y cerrada» | PASS |
| SHA-256 del entregable | `tester-v2-facts.log` (dato del Supervisor) da `8f4cc1…27e8`, igual al hash exigido; no recalculado por el Tester | PASS (dato del Supervisor) |

## B. Muestreo nuevo — 8 filas con base

| Fila | Afirmación comprobada | Evidencia real leída | Resultado |
|---|---|---|---|
| WS13 | `WR.workspace_node` y `WV.WorkspaceView`; delta en fila WS13/WS13.1 | `workspace_routes.py:129`; `views/workspace/node/workspace-view.js:54`; `reconciliacion.md:9` | PASS |
| WS15 | Agregado de WS15.1/WS15.2; delta en fila WS15/WS15.1 | `workspace-view.js:56`, `:65`; `workspace.mjs:63`; `reconciliacion.md:13` | PASS |
| WS19 | Ticket draft, `PS.save` con 409 por `viewRevision` y `expected`, `CD`; delta en fila WS19 | `task-edicion…md:3`; `persistence.py:62`, `:84-85`, `:101-102`; `connect-dialog.js:6`; `reconciliacion.md:15` | PASS |
| WS19.2 | `ConnectDialog` ofrece alta de relación sobre campos de referencia y queda pendiente hasta guardar | `connect-dialog.js:9` (`relationFields`), `:16-17` («La conexión quedará pendiente hasta guardar») | PASS (commit `c63b9a3` NO VERIFICADO) |
| WS25.2 | Existe `quickCapturable`/`quick-create-dialog.js` en el KB map, no captura a drawer | `shared/documents.mjs:27`; `quick-create-dialog.js:8`; `map-view.js:143-144` | PASS (`707ea86` NO VERIFICADO) |
| WS27.2 | Sección «Evidencia declarada» muestra `closeout_evidence` | `deskops-view.js:54`; `reconciliacion.md:20` | PASS |
| Fila `task-vista-changes…` | 70 líneas, draft, `current_node: ritual-execution`, `depends_on` multiproyección, 4 `files`, hash | `task-vista…md:3`, `:8`, `:14-22`, `:52`, `:70`; hash coincide con `tester-v2-facts.log` | PASS |
| Fila `Board.md` | 42 líneas, rutea 2 tareas draft, Notes da multiproyección por cerrada, hash | `Board.md:7-9`, `:35`, `:41-42`; hash coincide con `tester-v2-facts.log` | PASS |

## C. Muestreo nuevo — 4 filas de ausencia explícita

| Fila | Contraprueba buscada | Evidencia real leída | Resultado |
|---|---|---|---|
| WS21 | `source_mode` / fuente editable | `grep source_mode` en todo `../UIs/graph_ui`: 0 coincidencias | PASS |
| WS30 | Acta o carpeta de aceptación | `ls runs/subagents`: ninguna `*acceptance*`; `grep acceptance/workspace-documental` solo halla fixtures ajenos | PASS |
| WS35 | Trazabilidad tarea-intento-mensaje | `grep attempt/intento/task.*message` en `frontends/mindmap`: solo `workspace_routes.py:135` (escape de identificador); no hay modelo de intentos. Panel de workers existe: `shell/workers-panel.js:1` | PASS |
| WS36 | Adaptador de despacho / UI de intervención | `grep interven/adaptador/dispatch.*agent`: solo `sldb_adapter.py` (store) y `dispatch` HTTP (`workspace_routes.py:73`, `deskops_routes.py:83`) | PASS |

## D. Hallazgos

- **Menor (no FAIL):** `testing-handoff.md:6` sigue declarando el hash congelado antiguo `2496605c…2351`; el entregable corregido y `tester-v2-facts.log` dan `8f4cc1…27e8`.
- **Menor (no FAIL):** `ui.md:86` dice que los `split` de `workspace_routes.py` son «`str.split` de identificadores»; `workspace_routes.py:551` es `text.splitlines()`. La conclusión —no hay operaciones de split/merge de átomos— se mantiene.
- **NO VERIFICADO:** commits de la lista `PS` (`9825eb4`, `3823dc3`, …), `707ea86`, `c63b9a3`, `a64a924`, `363fe9b`, etc., y la existencia de `e80e8c0` como commit de deskops; no figuran en `tester-v2-facts.log`.
- Sin contradicción de fila muestreada contra su fuente.

RESULTADO: PASS
