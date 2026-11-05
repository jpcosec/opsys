FILE:desk/drawer/plans/deskops-ui/context-review-guide.md
# Guía para revisar un nodo de este plan

Va en todo input de revisión en frío. Deriva de brief.md, alcance.md y decisiones.md; no agrega requisitos.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el diseño es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de ids, aristas y gates. Ningún nodo tiene ejecución autorizada hasta que su revisión esté dispuesta.
- ROOT y PU son agrupaciones; un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una flecha `depends_on` significa prerrequisito → dependiente. Hermanos sin arista no se entregan nada entre sí.
- Un gate `pending` es intencional. Los gates `G_GC*`/`G_GO*` los producen otros planes (`gates-por-tipo` en deskops, `grafo-operable` en sldb); mientras no se cumplan, el elemento de UI correspondiente no se muestra (regla de alcance.md), y eso no es ambigüedad.
- Las decisiones DU1–DU6 de decisiones.md están tomadas.
- Las pantallas de Stitch son la referencia visual; sus datos son de ejemplo y nunca se copian.
- Los bloques `edge` son contratos de vecinos; no los revises.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance (en particular: mostrar un dato sin fuente real, o escribir sin pasar por las operaciones de deskops).

No cuentan: nombres exactos de archivos, funciones, clases CSS o tests que el TaskDoc fijará al promover; textos exactos de pantalla; detalles visuales que la pantalla de Stitch de referencia ya resuelve; trabajo de nodos dependientes; lo excluido en brief.md §Fuera de alcance.

Cita la frase del input que origina cada ambigüedad.

FILE:desk/drawer/plans/deskops-ui/brief.md
# Brief: la UI de deskops

Fecha: 2026-11-04. Repos: deskops (dueño del contrato y de la vista de datos) y graph_ui (cliente que la sirve). Estado: plan en drawer.

## Encargo

El producto es la UI de deskops: la superficie donde una persona trabaja la fábrica. Ve sus desks, las tareas por etapa del ciclo de vida, qué gate bloquea cada una, qué evidencia falta, el drawer y el inbox, y los agentes que corren; y desde ahí hace las acciones del dominio (avanzar, diferir, promover, reconocer). sldb es el sustrato que no se ve; Scion ejecuta debajo.

No es un explorador del store. El visor "KIMUN Knowledge Workspace" de graph_ui (`frontends/workspace/`, puerto 8090) responde "¿qué es este nodo?" y queda como vista secundaria de inspección.

## Lenguaje visual (lo que el dueño pidió)

Las pantallas del proyecto Stitch "Software Factory Knowledge Hub" (projects/10031397220192998154) son la referencia visual. Lo que se toma de ellas:

- **Organización por trabajo, no por almacén:** columnas por etapa del ciclo de vida; el drawer como carril aparte; el inbox como buzón entre proyectos.
- **La tarjeta cuenta en qué está la tarea:** checklist de gates con estado (cumple / pendiente / falla), conteo "n de m", contexto bajo (pills) separado de conocimiento durable (atoms).
- **Panel de la tarea seleccionada:** objetivo, gates con detalle, pills (transitorias) con su "qué" y "cuándo", atoms (durables) con su respuesta, y las acciones del dominio con su condición visible.
- **Color con significado:** verde = cumple, ámbar = pendiente, rojo = falla; el acento solo para selección.
- **Densidad tranquila:** oscuro, bordes de 1 px, mono para ids y hashes.

Lo que no se toma: ningún número, gate, porcentaje, TTL, autor, versión ni nombre de ejemplo. Regla del plan: **un elemento de pantalla sin fuente real no se dibuja**; si la fuente llega con otro plan, el elemento aparece cuando ese plan cierra.

Pantallas de referencia (archivos HTML en Stitch, versión con el design system de graph_ui aplicado):

| Pantalla | Archivo Stitch |
|---|---|
| The Desk - Active Board | projects/10031397220192998154/files/10b9fa05c4624776bdf3c0c3a9958b71 |
| The Desk - Markdown Wiki Doc | projects/10031397220192998154/files/e9c1ec6a77464258b1f45ab27d099fa7 |
| The Desk - Tareas Concurrentes & Herencia | projects/10031397220192998154/files/3c1cfa2c9f2c41258dcefbf7d95e98d0 |
| Drawers - Cajón de Esbozos & Triage | projects/10031397220192998154/files/23e743b753d440998ea42fff169165a1 |
| Inbox - Buzón Inter-Proyecto | projects/10031397220192998154/files/8bdd66211c8f4c80b2ae7e0c1e98952b |

## Resultado esperado

1. Una vista de datos en deskops (`deskops view ... --format json` y la clase que la produce) que compone lo que la UI muestra desde operaciones reales: board por etapa, tarjeta y detalle de tarea con gates y evidencia, pills y atoms resueltos, drawer, inbox, agentes y corridas. Contrato escrito en `docs/deskops-ui.md`.
2. En graph_ui, un frontend nuevo `frontends/desk/` (servidor y shell) con el design system oscuro de graph_ui, que sirve esa vista: Board, Tarea, Drawer, Inbox, Agentes; y "Inspeccionar" enlaza al visor de nodos existente.
3. Acciones del dominio solo por operaciones de deskops, con confirmación y guarda de revisión: avanzar (ya existe en graph_ui), reconocer un mensaje y pasar un mensaje del inbox al drawer. El resto de verbos se muestran deshabilitados con el motivo y el nodo que los habilita.

## Fuera de alcance

Editar Markdown o YAML en el navegador; Spec Studio y diagramas (necesita vínculos por paso en spec2viz, plan aparte); autenticación y acceso remoto (solo loopback); lanzar agentes Scion desde la UI (llega con el dispatch de la fábrica); gates por tipo y recibos (los produce `gates-por-tipo`; la UI los muestra cuando existan).

FILE:desk/drawer/plans/deskops-ui/alcance.md
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

FILE:desk/drawer/plans/deskops-ui/decisiones.md
# Decisiones registradas

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| DU1 | El producto es la UI de deskops, no un explorador del store; el visor KIMUN queda como vista secundaria de inspección. | Dueño | "¿Entiendes que el producto no es en realidad kimun si no que es la UI de deskops?" | 2026-11-04 |
| DU2 | El lenguaje visual es el de las pantallas de Stitch "Software Factory Knowledge Hub"; el design system es el de graph_ui (`DESIGN.md`), ya aplicado en Stitch. | Dueño | "si bien lo que había está técnicamente bien, no entiende el verdadero lenguaje visual que necesito… en el stitch sí se entiende"; elección de unificar hacia graph_ui | 2026-11-04 |
| DU3 | Escribir el plan y ejecutarlo. | Dueño | "si y más importante aún ejecútalo" | 2026-11-04 |
| DU4 | La lógica de qué se muestra vive en deskops (vista de datos con CLI y contrato); graph_ui es un cliente que la sirve por HTTP en loopback. deskops no gana servidor HTTP. | Asistente, conforme al plan de la fábrica del 2026-10-30 (E3: "deskops es la verdad, graph_ui solo muestra") | factory-local-first | 2026-11-04 |
| DU5 | Un elemento sin fuente real no se dibuja. Nada de datos de ejemplo, contadores inventados ni estados simulados. | Asistente, conforme a `DESIGN.md` de graph_ui ("Don't introduce mock, stub, or fabricated data") y al feedback del dueño sobre densidad | DESIGN.md; reader-density | 2026-11-04 |
| DU6 | Revisión en frío con tope: una ronda a nivel de plan y una de preflight por nodo al promover. | Dueño (tope de rondas, "8 rondas igual es excesivo") | cold-review-rounds-cap | 2026-11-04 |

FILE:desk/drawer/plans/deskops-ui/dag.yaml#node:PU01
id: PU01
title: Vista y shell
owner_repo: deskops
node_role: aggregate
children:
- UI01
- UI02
scope: UI01 escribe la vista de datos en deskops; UI02 levanta el servidor y el shell
  en graph_ui que la sirven.
acceptance: G_VIEW y G_SHELL satisfechos.

FILE:desk/drawer/plans/deskops-ui/dag.yaml#edge:UI01
id: UI01
title: Vista de datos de deskops para la UI (deskops view) y su contrato
kind: code
owner_repo: deskops
node_role: delivery
parent_id: PU01
scope: 'Clase de servicio de solo lectura en deskops (deskops/services/desk_view.py)
  que compone, desde las operaciones existentes listadas en alcance.md, cinco vistas
  JSON: board (columnas por nodo del ciclo de vida en el orden del spec, cada tarjeta
  con id, título, status, current_node, gates con condición y si se cumple, conteo
  cumplidos/total, evidencia declarada y encontrada de verify_task_closeout, pills
  y atoms resueltos a título); task (lo del board más goal, scope, implementation_path,
  validation, done_when, why, references, files, depends_on, inherits_from, pills
  con what/when/how_not, atoms con answer, next_actions y advance_when de next_action_report,
  y revision = sha256 de Board + archivo de tarea como la guarda de graph_ui); drawer
  (tareas de desk/drawer/tasks con id, título, status, primeras líneas del cuerpo
  y ruta, más el comando add task --from-drawer listo para copiar); inbox (notas con
  id, kind, título, emisor, destino, fecha del nombre de archivo, estado de ack, cuerpo);
  agents (runtime workers y las últimas N corridas de runs/subagents/index.jsonl).
  Toda referencia que no resuelve aparece en una lista errors de la vista con su causa,
  nunca como dato. Subcomando deskops view {board,task <id>,drawer,inbox,agents} --root
  --format json|text registrado en cli/registry.py. Documento docs/deskops-ui.md con
  el contrato JSON de cada vista y la tabla de mapeo de alcance.md. Solo lectura:
  nada escribe.'
acceptance: 'Tests sobre desks temporales reales (deskops init + add task): board
  agrupa por current_node y cuenta gates igual que show_task; task trae los campos
  listados y la misma revision que la guarda de graph_ui; una pill o atom inexistente
  aparece en errors y no en la lista; drawer, inbox y agents devuelven lo que hay
  en disco; ninguna vista escribe (hash del árbol igual antes y después); deskops
  view --help y golden de help; docs/deskops-ui.md existe con los cinco contratos;
  suite completa verde en robocop2.'
output_scope: deskops/services/desk_view.py, deskops/cli/registry.py, deskops/cli/commands/view.py,
  tests/test_desk_view.py, tests/fixtures/golden/help/, docs/deskops-ui.md
depends_on: []
requires: []

FILE:desk/drawer/plans/deskops-ui/dag.yaml#edge:UI02
id: UI02
title: Servidor y shell de la UI de deskops en graph_ui
kind: code
owner_repo: graph_ui
node_role: delivery
parent_id: PU01
scope: 'frontends/desk/ (serve.py, index.html, app.js, styles.css): servidor en 127.0.0.1
  (puerto por defecto 8091) que expone GET /api/view/{board,task,drawer,inbox,agents}?desk=<repo>
  llamando a la vista de UI01 por Python (no por subprocess), reusa DeskRoutes para
  POST /api/desk/advance, y sirve el shell. Selector de desk entre los repos del registro
  de deskops (desk/registry/repo-*.md) que tengan desk/. Shell con el design system
  de DESIGN.md en tema oscuro por defecto: barra lateral (Board, Drawer, Inbox, Agentes,
  y "Inspeccionar" que abre el visor KIMUN en :8090 con el id), cabecera con desk
  activo y conteos derivables (tareas por etapa, drawer, inbox sin ack, workers vivos).
  Estado de error visible con causa cuando la vista falla. Sin CDN: fuentes del sistema
  o vendorizadas, como pide el plan de la fábrica.'
acceptance: 'pytest de rutas: cada /api/view/* devuelve exactamente lo que devuelve
  deskops view para el mismo desk temporal; métodos no GET rechazados salvo advance;
  escucha solo en loopback; el shell carga sin red externa (ninguna URL http(s) externa
  en index.html, styles.css ni app.js); el selector lista los desks del registro;
  captura del shell comparada con The Desk - Active Board de Stitch y diferencias
  anotadas en el TaskDoc.'
output_scope: UIs/graph_ui/frontends/desk/, UIs/graph_ui/tests/test_desk_ui_routes.py,
  UIs/graph_ui/docs/deskops-ui-client.md
depends_on:
- UI01
requires:
- G_VIEW

FILE:desk/drawer/plans/deskops-ui/dag.yaml#gates
G_VIEW:
  title: Vista de datos de deskops con contrato
  state: pending
  produced_by: UI01
  evidence: deskops view board|task|drawer|inbox|agents --format json con tests sobre
    desks temporales y docs/deskops-ui.md
G_SHELL:
  title: Shell de graph_ui sirviendo la vista
  state: pending
  produced_by: UI02
  evidence: frontends/desk/serve.py en loopback con rutas que delegan en la vista
    y shell navegable con el design system

FILE:instruccion
Revisa el nodo PU01 siguiendo context-review-guide.md. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

