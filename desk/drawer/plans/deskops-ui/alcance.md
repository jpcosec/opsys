# Alcance y estado de partida

## Qué existe hoy (verificado 2026-11-04)

**deskops** (sin servidor HTTP):
- `DeskopsOperations.list_tasks`, `show_task(id)` → `(Task, gates)` donde `gates` sale de `_lifecycle_gates` (deskops/operations.py:412-450): por transición saliente del nodo actual, la condición y si se cumple.
- `next_action_report(id)` (services/tasks.py:98): fase, ritual, pills fusionadas del Board y la tarea, `next_actions`, `advance_when`, `why`.
- `verify_task_closeout(id)` (operations.py:602): evidencia declarada (`closeout_evidence`) contra la encontrada, por tipo.
- Board: `desk/tasks/Board.md` (BoardDoc: tasks, pills, rituals). Drawer: `desk/drawer/tasks/*.md` y su Board (`ops.drawer`). Inbox: `deskops message list|read|ack` sobre `desk/inbox/*.md` (InboxNoteDoc: kind, title, body, sender/to). Pills: `desk/contexts/*.md` (PillDoc: what, why, when, where, how, how_not). Atoms: `desk/atoms/**/*.md` (AtomDoc: title, five_wh_one_plus, answer). Registro de repos: `desk/registry/repo-*.md`.
- Runtime: `deskops runtime workers --format json` (paneles de herdr), `runs/subagents/index.jsonl` (corridas y cierres).
- Ciclo de vida: nodos `ritual-execution` → `ritual-testing` → `ritual-closeout` (spec/workflows/task_lifecycle.yaml); el cierre solo por `closeout commit`.

**graph_ui**:
- `frontends/mindmap/deskops_routes.py` (`DeskRoutes`): `GET /api/desk/board`, `GET /api/desk/task?id=`, `POST /api/desk/advance` con guarda de revisión (hash de Board + tarea) e identidad validada. Se reusa.
- `frontends/workspace/` (KIMUN, :8090): explorador de nodos; `serve.py` ya compone overview, workers, runs, git. Queda como "Inspeccionar".
- `DESIGN.md`: design system oscuro (paleta, tipografía, radios 10/8/6 px, sin sombras salvo overlays, sin datos inventados, foco visible, animaciones solo transform/opacity ≤150 ms).

## Mapeo de la pantalla de Stitch a fuentes reales

| Elemento de Stitch | Fuente real hoy | Si no hay fuente |
|---|---|---|
| Columnas por etapa | `current_node` de cada tarea del Board; una columna por nodo del ciclo de vida, en el orden del spec | — |
| Checklist de gates de la tarjeta | `show_task` → gates (condición y si se cumple) más la evidencia declarada vs encontrada de `verify_task_closeout` | — |
| "n de m rituales" | conteo de los mismos gates | — |
| Pills de la tarjeta | `effective_pills` de la tarea más pills del Board, resueltas a PillDoc (título; en el panel what/when) | pill no resoluble: se muestra el id con aviso ámbar |
| Atoms | `atoms` y referencias `atom-*` de la tarea resueltos a AtomDoc (title, answer) | ídem |
| "Promover a Atom" | no hay operación | botón deshabilitado: "requiere operación de graduación (no existe)" |
| "Iniciar ejecución" | no hay dispatch | deshabilitado: "llega con runtime dispatch (fábrica E3)" |
| Avanzar | `POST /api/desk/advance` existente | — |
| Diferir a drawer | no hay operación | deshabilitado con motivo |
| Drawer: lista y vista raw | `desk/drawer/tasks/*.md` (título, status, primeras líneas) | — |
| Drawer: "Promover a Desk" | no es promoción: requiere escribir una tarea completa (`add task --from-drawer`) | se muestra el comando a copiar, no un botón que escriba |
| Inbox: lista, lectura, emisor → destino | InboxNoteDoc | — |
| Inbox: Reconocer (ack) | `deskops message ack` (operación existente) | — |
| Inbox: Pasar a drawer | `promote inbox-to-drawer-task` (operación existente) | — |
| Agentes y corridas | `runtime workers`, `runs/subagents/index.jsonl` | — |
| Métricas de cabecera ("85,7 % validado", "9 pills", "2/3 agentes") | conteos derivables: tareas por etapa, gates cumplidos/total del Board, pills enlazadas, workers vivos | solo conteos derivables; ningún porcentaje inventado |
| Hilo de conversación del inbox, firmas, prioridad, TTL, autor, versión, "hot reload" | no existe | no se dibuja |
| Gates por tipo, recibos de revisión, `anchor_state` | plan `gates-por-tipo` (GC05, GC02/GC03) y sldb GO07 | aparecen cuando existan; hasta entonces no se dibujan |

## Reglas comunes de ejecución

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk del repo dueño, con `--task-type` y `files`; preflight TaskDoc-only antes de ejecutar (una ronda, DU6).
2. Un elemento de pantalla sin fuente real no se dibuja (DU5). Si la fuente falla, la pantalla muestra el error con su causa; nunca un valor por defecto que parezca dato.
3. Escritura solo por operaciones de deskops, con confirmación explícita y la guarda de revisión que ya usa `/api/desk/advance`; ninguna ruta escribe archivos directo.
4. Solo loopback (127.0.0.1), como el resto de graph_ui.
5. Tests: deskops con pytest (vista y CLI con desks temporales reales); graph_ui con pytest de rutas y un e2e de navegador sobre un desk temporal que verifique que lo mostrado coincide con `deskops view` y que no aparece ningún texto de ejemplo de Stitch.
6. Validación en robocop2 (suite completa del repo tocado) antes de mergear.
7. Visual: comparar captura de cada pantalla con su referencia de Stitch y registrar las diferencias deliberadas en el TaskDoc.
