# deskops view: el contrato de datos de la UI de deskops

`deskops view {board,task <id>,drawer,inbox,agents} --root <repo> --format json|text`
produce las vistas que dibuja la UI de deskops (graph_ui, `frontends/desk/`).

`board` y `task` son `ViewDoc` de sldb: las semillas `deskops/data/views/board.md` y
`task.md` (viven solo en el paquete, sin `desk/views/`), trackeadas como `ViewDoc` en el
store del propio repo deskops. `deskops view` las evalúa con `sldb.api.run_view` sobre el
store del desk y `deskops.cli.commands.view.project(view, resultado, root)` proyecta el
resultado a este contrato. graph_ui lee `GET /views/<vista>` de `sldb serve` (con ETag) y
llama a la misma `project` en proceso, así que sirve exactamente el mismo JSON. `drawer`,
`inbox` y `agents` los arma el CLI (ver «Fuentes de cada campo»).

Mientras sldb no resuelva una `ViewDoc` de un store enlazado (hipótesis H9), `board` y
`task` responden solo en un desk cuyo propio store trackea las `ViewDoc` (el repo deskops);
en los demás salen con el sobre de error `Unknown view: <vista>`.

Reglas comunes:

- **Solo lectura.** Ninguna vista escribe en `desk/`, `.sldb/` ni `runs/`.
- **Una lectura por corrida.** `board` y `task` abren un `read_snapshot`: la ruta y el
  payload de cada tarea, sus transiciones, el grafo de reglas y el contexto del grafo de
  closeout se leen una vez y se comparten entre las tarjetas. El grafo no recorre `runs/`
  salvo que una materialización declare un `target_identity` allí. Es una optimización de
  lectura: el JSON y el texto no cambian (los fijan los goldens de `tests/test_view_goldens.py`).
- **Sin datos inventados.** Una referencia que no resuelve (pill, atom, tarea del Board,
  nota, línea del índice de corridas, runtime de Herdr) no aparece como dato: va a
  `errors` como `{"reference": "<id o ruta>", "cause": "<por qué>"}`; si la referencia la hace
  una tarea (una pill o un atom de la tarea), el error lleva además `"task": "<id de la tarea>"`
  para que la UI marque la tarjeta.
- `--format json` es el contrato estable; `--format text` es un resumen legible.
- Toda vista lleva `view` (nombre), `contract` (versión, hoy `1`), `root` (ruta absoluta
  del repo) y `errors`.
- Un error que impide la vista entera (no hay `desk/tasks/Board.md`, la tarea no resuelve)
  sale como el sobre de error de deskops (`{"ok": false, "error": {...}}`) con código 1.

## board

Una columna por nodo del ciclo de vida, en el orden de
`deskops/spec/workflows/task_lifecycle.yaml` (`ritual-execution`, `ritual-testing`,
`ritual-closeout`). Las tareas salen de `desk/tasks/Board.md` (el Board es la verdad).

```json
{
  "view": "board", "contract": 1, "root": "/abs/repo",
  "board": {"path": "desk/tasks/Board.md", "pills": [{"id": "pill-…", "title": "…", "source": "board"}]},
  "columns": [
    {"node": "ritual-execution", "phase": "execution", "purpose": "…", "in_lifecycle": true,
     "count": 1, "tasks": [CARD]}
  ],
  "counts": {"tasks": 1, "by_node": {"ritual-execution": 1, "ritual-testing": 0, "ritual-closeout": 0},
             "gates_holding": 1, "gates_total": 1},
  "errors": []
}
```

Una tarea cuyo `current_node` no es un nodo del ciclo de vida aparece en una columna
extra con `in_lifecycle: false` y además en `errors`.

`CARD`:

```json
{
  "id": "task-…", "title": "…", "status": "draft", "current_node": "ritual-execution",
  "task_type": "code", "path": "desk/tasks/task-….md",
  "gates": [{"relation_type": "task_activates", "target": "ritual-testing", "condition": "", "holds": true}],
  "gates_holding": 1, "gates_total": 1,
  "closeout": {
    "ok": false, "declared": ["tests", "commit"], "found": [], "summary": "…",
    "implicit_code": false, "alerts": [],
    "evidence": [{"gate": "tests", "state": "pending", "evidence": [], "findings": [{"code": "…", "message": "…"}]}]
  },
  "pills": [{"id": "pill-…", "title": "…", "source": "task|board"}],
  "atoms": [{"id": "atom-…", "title": "…"}]
}
```

- `gates` es exactamente lo que devuelve `DeskopsOperations.show_task` (transiciones que
  salen del nodo actual, con su condición sldb y si se cumple hoy).
- `closeout` resume `verify_task_closeout`: `declared`/`found` tal cual; `evidence` trae
  una entrada por compuerta (`tests`, `atom_or_materialization_link`, `commit`,
  `document`, `external`) con `state`:
  `holds` (la compuerta se cumple), `pending` (falta, y la tarea aún no está en
  `ritual-closeout`) o `failing` (falta y la tarea está en `ritual-closeout`, o el tipo
  declarado no existe en el vocabulario).
- `pills`: `effective_pills` de la tarea (`source: task`) más las pills del Board
  (`source: board`), resueltas a `PillDoc`, igual que las fusiona `deskops next`.
- `atoms`: `effective_atoms` más las referencias `atom-*`, resueltos a `AtomDoc`.

## task

```json
{
  "view": "task", "contract": 1, "root": "/abs/repo",
  "task": {
    CARD…,
    "on_board": true,
    "why": "…", "goal": "…", "scope": "…", "implementation_path": "…",
    "validation": ["…"], "done_when": "…", "references": ["…"], "files": ["…"],
    "depends_on": ["…"], "inherits_from": ["…"], "from_drawer": "", "history": ["task_activates"],
    "pills": [{"id": "…", "title": "…", "source": "task", "what": "…", "when": "…", "how_not": "…"}],
    "atoms": [{"id": "…", "title": "…", "question": "what", "answer": "…"}]
  },
  "next": {"phase": "execution", "ritual": "desk/rituals/execution.md", "next_actions": ["…"], "advance_when": ["…"]},
  "revision": "<sha256 hex>",
  "errors": []
}
```

- `validation`, `done_when` y `references` son los efectivos (con herencia).
- `next` viene de `next_action_report`; si falla, `next` es `null` y la causa va a `errors`.
- `revision` = el ETag de la vista `task` (`run_view(...)["revision"]`, GD25): cambia cuando
  cambia la tarea, el Board o una pill o un atom que la vista leyó. Es la guarda que usa
  `POST /api/desk/advance` de graph_ui: con un `revision` viejo responde 409.

## drawer

```json
{
  "view": "drawer", "contract": 1, "root": "/abs/repo", "count": 1,
  "tasks": [{
    "id": "task-…", "markdown": "<texto completo del archivo>", "title": "…", "status": "deferred",
    "excerpt": ["primeras líneas del cuerpo"], "path": "desk/drawer/tasks/task-….md",
    "command": "deskops add task --root . --from-drawer desk/drawer/tasks/task-….md --title '…'"
  }],
  "errors": []
}
```

- Archivos `desk/drawer/tasks/*.md` salvo `Board.md` y `README.md`.
- `markdown`: el archivo completo, para la vista en crudo (solo lectura).
- `excerpt`: hasta 3 líneas no vacías del cuerpo, sin encabezados ni las pistas en cursiva
  de la plantilla (`_Explain …_`).
- `status` es `null` si el archivo no es un `TaskDoc` válido (la causa va a `errors`).
- `command` es el inicio del comando para autorizar la tarea; el resto de campos
  (`--goal`, `--scope`, `--validation`, `--task-type`…) los decide quien la promueve.

## inbox

```json
{
  "view": "inbox", "contract": 1, "root": "/abs/repo", "count": 2, "open": 1,
  "notes": [{
    "id": "20261104-101500-suggestion-…", "path": "desk/inbox/….md", "kind": "suggestion",
    "title": "…", "sender": "sldb", "target": "deskops", "date": "2026-11-04T10:15:00",
    "status": "open", "acknowledged": false, "acknowledged_by": null, "acknowledged_at": null,
    "body": "…", "revision": "<sha256 de los bytes de la nota>"
  }],
  "errors": []
}
```

- Mismo orden y misma lectura del frontmatter que `deskops message list` (más nuevas
  primero); `acknowledged` es `status == "closed"`, que es lo que escribe `message ack`.
- `date` sale del sello `YYYYMMDD-HHMMSS` del nombre de archivo; sin sello, `null` y aviso.
- `body` es el campo `body` del `InboxNoteDoc`.
- `revision` = `sha256(bytes del archivo de la nota)`: la guarda de las acciones del inbox
  (Reconocer, Pasar al drawer) en la UI.

## agents

```json
{
  "view": "agents", "contract": 1, "root": "/abs/repo",
  "workers": [{"pane": "w1:p1", "kind": "claude", "name": null, "status": "idle", "cwd": "…",
               "title": "…", "workspace": "w1", "seq": 3, "focused": false}],
  "workers_error": null, "live_workers": 1,
  "runs": [{"task_id": "task-…", "run_id": null, "run_dir": null, "commit": null, "mode": "manual", "on_board": false}],
  "runs_total": 122, "runs_limit": 20,
  "errors": []
}
```

- `workers` es la forma pública de `deskops runtime workers` (Herdr, toda la máquina, no
  solo este desk). Si Herdr no responde: `workers: null`, `live_workers: null`,
  `workers_error` con la causa y una entrada en `errors`; nunca una lista vacía muda.
- `runs`: las últimas `--runs` (20 por omisión) líneas de `runs/subagents/index.jsonl`, la
  más nueva primero; `on_board` dice si la tarea sigue en el Board.

## Fuentes de cada campo (CC34)

`run_view` es la vista `ViewDoc` evaluada por sldb. «Agregado CLI, pendiente de sldb Hn»
es un campo que el CLI todavía arma con una operación de lectura que ya existía, porque el
modelo de `ViewDoc` no lo expresa aún; cada uno se retira cuando sldb cierre su hipótesis.

| Campo | Fuente |
|---|---|
| `view`, `contract`, `root` | constantes del CLI |
| `board.path`, `board.pills` (ids) | `run_view`, sección `board` (campos `tasks`, `pills`) |
| tareas del Board, su orden, `errors` de referencias | `run_view`, secciones `board` y `tasks` (el Board manda) |
| columnas (`node`, agrupación) | `run_view`, sección `tasks` (`group_by: current_node`) |
| `phase`, `purpose`, `in_lifecycle` de cada columna | agregado CLI, pendiente de sldb H5 (spec del ciclo de vida) |
| `CARD.id/title/status/current_node/task_type/path` | `run_view`, filas de `tasks` / `task` |
| `CARD.gates`, `gates_holding`, `gates_total` | agregado CLI, pendiente de sldb H1-H3 (`show_task`) |
| `CARD.closeout` | agregado CLI, pendiente de sldb H4 (`verify_task_closeout` sin recibos) |
| `CARD.pills`, `CARD.atoms` (títulos y detalle) | `run_view`, secciones `pills` y `atoms` |
| lista efectiva de pills y atoms; `validation`, `done_when`, `references` | agregado CLI, pendiente de sldb H6 (`resolve_task_payload`) |
| `counts` | suma del CLI sobre las tarjetas |
| `task.on_board` | `run_view`, arista `tasks` del Board |
| `task.why/goal/scope/implementation_path/files/depends_on/inherits_from/from_drawer/history` | `run_view`, fila de `task` |
| `next` | agregado CLI, pendiente de sldb H5 (`next_action_report`) |
| `revision` (task) | `run_view` (ETag de GD25) |
| `drawer.*` (`markdown`, `excerpt`, `command`...) | agregado CLI, lectura del archivo, pendiente de H7 y H10 |
| `inbox.*`, `notes[].revision` | agregado CLI, lectura del archivo, pendiente de H8 y H10 |
| `agents.*` | CLI (`deskops/runtime/desk_agents.py`): no son documentos |

## Mapeo de la pantalla de Stitch a fuentes reales

Copiado de `desk/drawer/plans/deskops-ui/alcance.md` (plan deskops-ui, 2026-11-04).

| Elemento de Stitch | Fuente real | Campo de la vista | Si no hay fuente |
|---|---|---|---|
| Columnas por etapa | `current_node` de cada tarea del Board; orden del spec | `board.columns` | — |
| Checklist de gates de la tarjeta | `show_task` → gates, más evidencia de `verify_task_closeout` | `CARD.gates`, `CARD.closeout.evidence` | — |
| "n de m rituales" | conteo de los mismos gates | `CARD.gates_holding`/`gates_total` | — |
| Pills de la tarjeta | `effective_pills` + pills del Board → `PillDoc` | `CARD.pills` (+ `what/when/how_not` en task) | id en `errors` |
| Atoms | `atoms` y referencias `atom-*` → `AtomDoc` | `CARD.atoms` (+ `answer` en task) | id en `errors` |
| "Promover a Atom" | no hay operación | — | botón deshabilitado: "requiere operación de graduación (no existe)" |
| "Iniciar ejecución" | no hay dispatch | — | deshabilitado: "llega con runtime dispatch (fábrica E3)" |
| Avanzar | `POST /api/desk/advance` de graph_ui | `task.revision` (ETag) | — |
| Diferir a drawer | no hay operación | — | deshabilitado con motivo |
| Drawer: lista y vista raw | `desk/drawer/tasks/*.md` | `drawer.tasks` | — |
| Drawer: "Promover a Desk" | `add task --from-drawer` | `drawer.tasks[].command` | se muestra el comando, no un botón |
| Inbox: lista, lectura, emisor → destino | `InboxNoteDoc` | `inbox.notes` | — |
| Inbox: Reconocer | `deskops message ack` | — (acción de UI05) | — |
| Inbox: Pasar a drawer | `promote inbox-to-drawer-task` | — (acción de UI05) | — |
| Agentes y corridas | `runtime workers`, `runs/subagents/index.jsonl` | `agents.workers`, `agents.runs` | causa en `workers_error` |
| Métricas de cabecera | conteos derivables | `board.counts`, `drawer.count`, `inbox.open`, `agents.live_workers` | ningún porcentaje inventado |
| Hilo del inbox, firmas, prioridad, TTL, autor, versión | no existe | — | no se dibuja |
| Gates por tipo, recibos, `anchor_state` | plan `gates-por-tipo`, sldb GO07 | — | no se dibuja hasta que existan |
