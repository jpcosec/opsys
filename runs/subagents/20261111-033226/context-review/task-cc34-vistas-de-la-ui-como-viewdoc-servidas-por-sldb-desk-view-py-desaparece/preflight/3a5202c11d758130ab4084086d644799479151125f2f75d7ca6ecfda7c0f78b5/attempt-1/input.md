FILE:desk/tasks/task-cc34-vistas-de-la-ui-como-viewdoc-servidas-por-sldb-desk-view-py-desaparece.md
---
sldb:
  by: agent
  at: '2026-11-11T03:32:05Z'
  authority: generated
  via: save_document_payload
id: task-cc34-vistas-de-la-ui-como-viewdoc-servidas-por-sldb-desk-view-py-desaparece
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/desk_view.py
- deskops/data/views/
- deskops/data/desk_declaration.yaml
- deskops/cli/commands/view.py
- deskops/runtime/
- deskops/operations.py
- deskops/domain_tree.py
- tests/
- tests/fixtures/golden/output/
- docs/deskops-ui.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC34: Vistas de la UI como ViewDoc servidas por sldb; desk_view.py desaparece

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC34 del plan deskops-como-config. Depende de CC33 (CC33a, CC33b y CC33c cerrados) y CC36 (cerrado). Gates G_GD25 y G_GD21 satisfied. Toca también graph_ui (UIs/graph_ui).

## Goal

_Describe the concrete result this task must produce._

deskops view board|task|drawer|inbox sale de sldb.api.run_view sobre ViewDocs semilla del paquete, con el mismo JSON que hoy salvo revision; graph_ui lee esas vistas sin importar DeskView; desk_view.py y sus helpers se borran.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/desk_view.py, deskops/data/views/, deskops/data/desk_declaration.yaml, deskops/cli/commands/view.py, deskops/runtime/, deskops/operations.py, tests/, tests/fixtures/golden/output/, docs/deskops-ui.md, CHANGELOG.md; en graph_ui: frontends/desk/serve.py, frontends/mindmap/deskops_routes.py, tests/. Fuera: proveedores computed (DA1) y carpeta desk/views (DA4).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml, CC34). SCOPE: Primer paso: capturar goldens JSON de deskops view board|task|drawer|inbox sobre un desk de prueba fijo (no existen hoy en tests/fixtures/golden/output/). ViewDocs semilla (deskops/data/views/: board, task, drawer, inbox) que reproducen el contrato de docs/deskops-ui.md (CONTRACT_VERSION 1): board = sección de tareas del Board agrupadas por current_node en el orden de los RitualDoc del ciclo de vida, con transitions (holding/blocked de GO08/GO09), rules (findings de las reglas de CC32/CC33) y edges (pills, atoms); task = una tarea por {id} con sus campos y next; drawer = selector por path_glob desk/drawer/tasks/*.md; inbox = notas del inbox. Sin proveedores computed (DA1): los hechos de git del closeout llegan a la vista como recibos ReviewDoc kind evidence de CC33 que la ViewDoc lee por edges o rules; lo que no es documento ni recibo (agents de Herdr, runtime/, P4) lo agrega deskops view sobre el resultado de run_view en el CLI, y graph_ui lo pide a deskops en proceso como las acciones (DP4); ningún agregado reimplementa una regla. deskops view <x> = sldb.api.run_view + el render_text actual (se conserva en el CLI); revision del payload = ETag de GD25 (los valores cambian, la clave y su semántica de guarda optimista no). Se borran services/desk_view.py, task_revision/note_revision y los alias privados de la fachada que CC30 conservó para graph_ui. graph_ui (repo aparte, UIs/graph_ui): GET /api/view/<view> lee GET /views/<view> de sldb serve (proxy o cliente directo, con ETag) en lugar de importar DeskView; deskops_routes.py deja de usar ops._read_doc/_resolve_glob/show_task y lee la vista task; las acciones siguen por el CLI de deskops en proceso (DP4); su guarda de revisión usa el ETag. Las ViewDocs viven solo como semillas del paquete deskops, sin carpeta desk/views/ (DA4); sldb serve las encuentra por un store de deskops enlazado.

ACCEPTANCE: deskops view board|task|drawer|inbox --format json idénticos a los goldens capturados en el primer paso salvo el valor de revision; ayuda de view idéntica; GET /views/board de sldb serve sobre el desk de prueba devuelve el mismo payload; graph_ui sirve la vista board leyendo de sldb serve (test en graph_ui) y POST /api/desk/advance con un ETag viejo da 409; tests/test_desk_view.py reescrito sobre run_view y verde; grep de "desk_view\|DeskView" en deskops/ y en UIs/graph_ui/frontends vacío; deskops view board en los 6 desks responde; tiempo frío/caliente de view board sobre el desk real de deskops registrado (meta caliente < 1 s, la verifica CC52); CHANGELOG; docs/deskops-ui.md.

OUTPUT_SCOPE: deskops/services/desk_view.py (borrado), deskops/data/views/, deskops/cli/commands/view.py, deskops/runtime/ (agents en el CLI), deskops/operations.py (alias privados), tests/, tests/fixtures/golden/output/, docs/deskops-ui.md, CHANGELOG.md, UIs/graph_ui/frontends/desk/serve.py, UIs/graph_ui/frontends/mindmap/deskops_routes.py, UIs/graph_ui/tests/

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-11, coordinador del plan; base origin/main b990c49e, con CC33 y CC36 cerrados; decisiones revisables):
a1 (lo que hay hoy): deskops/services/desk_view.py (543 líneas): DeskView, CONTRACT_VERSION = 1, task_revision (:40), note_revision (:48), RUN_INDEX y los agents de herdr. graph_ui lo importa en frontends/desk/serve.py (from deskops.services.desk_view import DeskView, DeskViewError). sldb expone sldb.api.run_view y list_views (GD25).
a2 (dos repos, orden de integración): el nodo toca deskops y graph_ui. Para no romper graph_ui en ningún punto, el orden es:
1. graph_ui deja de importar DeskView y lee la vista nueva (deskops view <x> --format json en proceso, o GET /views/<x> de sldb serve con ETag). Va en una rama wt/ de graph_ui creada desde su master después de que entre la integración wt/deskops-ui.
2. deskops borra desk_view.py.
Entregas: rama wt/cc34 en deskops y rama wt/cc34-ui en graph_ui. El coordinador integra primero graph_ui y después deskops, y el CI de cada repo corre contra el main del otro. Si con eso un paso intermedio queda rojo, el worker para y avisa con la propuesta.
a3 (goldens primero): antes de cambiar nada, deskops view board|task|drawer|inbox --format json se captura en tests/fixtures/golden/output/ sobre un desk de prueba fijo (tmp_path con contenido determinista, sin fechas ni hashes variables salvo revision). Ese commit va solo. La aceptación compara contra esos goldens salvo el valor de revision.
a4 (agents y lo que no es documento): lo que no es documento ni recibo (agents de herdr, runs/subagents/index.jsonl) lo suma el CLI de deskops view sobre el resultado de run_view (DA1, DP4). No hay proveedor computed en sldb. Ningún agregado reimplementa una regla.
a5 (ETag): revision del payload = ETag de GD25. La clave revision y su guarda optimista no cambian; el valor sí. POST /api/desk/advance de graph_ui con un ETag viejo da 409 (test en graph_ui).
a6 (DA4): las ViewDoc viven solo como semillas en deskops/data/views/, sin carpeta desk/views/. sldb serve las encuentra por el store de deskops enlazado. Si no las encuentra, hipótesis y nota a sldb.
a7 (files): deskops: deskops/services/desk_view.py (borrado), deskops/data/views/, deskops/data/desk_declaration.yaml (solo si hace falta declarar las ViewDoc), deskops/cli/commands/view.py, deskops/runtime/, deskops/operations.py, tests/, tests/fixtures/golden/output/, docs/deskops-ui.md, CHANGELOG.md. graph_ui: frontends/desk/serve.py, frontends/mindmap/deskops_routes.py, tests/.
a8 (4 pasos): los de deskops (sldb stores build --store .sldb; pytest, un proceso por archivo; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh .) y todos los pasos de .github/workflows/ci.yml de graph_ui, con sus e2e. Los corre el coordinador en clones limpios.

DISPOSICIÓN DE PREFLIGHT-1 Y BUNDLE-1 (2026-11-11, coordinador del plan; decisiones revisables):
b1 (transporte de graph_ui): un solo transporte, GET /views/<vista> de sldb serve, como cliente directo con If-None-Match/ETag. Si sldb serve no responde, graph_ui devuelve 502 con el mensaje del error. No se usa la vía en proceso por CLI para leer vistas. Las acciones siguen por el CLI de deskops en proceso (DP4).
b2 (enlace del store): el store de graph_ui ya enlaza a deskops (.sldb/store.yaml: links name deskops, path ../../deskops/.sldb). Las ViewDoc semilla de deskops/data/views/ se trackean en el store del propio repo deskops (su .sldb), declaradas con `sldb stores declare --write`, nunca a mano. Así sldb serve sobre cualquier store que enlace a deskops las encuentra. Para los tests de deskops, el desk de prueba se arma igual: un store de prueba que enlaza al store de deskops.
b3 (desk_declaration.yaml): no hace falta tocarlo si b2 alcanza. Queda en files solo como reserva: si el worker lo toca, justifica en el informe por qué b2 no alcanzó.
b4 (forma de la ViewDoc): el modelo es sldb.models.notation.view_doc (GD25). Cada parte del contrato de docs/deskops-ui.md se lee como lo da el modelo: relaciones (pills, atoms) por edges y hallazgos de reglas (CC32/CC33) por rules. La forma de cada ViewDoc sale del contrato y del modelo, no se inventa. Si el modelo no expresa una parte, hipótesis y nota a sldb.
b5 (agregados del CLI): deskops view sobre run_view suma, con las mismas claves y el mismo orden que hoy, lo que no es documento: agents de herdr y runs/subagents/index.jsonl. `deskops view agents` sigue existiendo como hoy (cli/commands/view.py:28) y queda fuera de la comparación con goldens de ViewDoc.
b6 (desk de prueba determinista): una fixture de tests arma el desk en tmp_path con ids, títulos y fechas fijas (created_at por flag o por frontmatter del fixture). Antes de comparar con los goldens, el test normaliza los valores de revision y de fechas a marcadores fijos ('<revision>', '<date>'). inbox entra en los goldens con esa normalización.
b7 (alias privados): se borran los tres de deskops/operations.py:259-272 (_read_doc, _resolve_glob, _registered_repositories) y _repository_root si solo lo usa graph_ui. deskops/domain_tree.py todavía llama a uno: se cambia esa llamada a doc_access directamente (único cambio en domain_tree.py, que se suma a files). graph_ui deja de usarlos (deskops_routes.py).

DISPOSICIÓN DE PREFLIGHT-2 Y BUNDLE-2 (2026-11-11, coordinador del plan; decisiones revisables; mandan sobre a2, b1-b7 y el SCOPE donde difieren):
c1 (orden de integración; reemplaza a2): graph_ui lee las ViewDoc de deskops, así que deskops va primero. wt/cc34 en deskops trae las semillas ViewDoc, deskops view sobre run_view y el borrado de desk_view.py. wt/cc34-ui en graph_ui se verifica contra wt/cc34. El coordinador integra deskops y en seguida graph_ui. Mientras tanto, el master de graph_ui puede quedar rojo unos minutos contra deskops main; se acepta y no hay shim de compatibilidad. wt/cc34-ui parte del master de graph_ui después de que entre la integración wt/deskops-ui.
c2 (transporte, cierra el choque con DP4): graph_ui LEE las vistas por GET /views/<vista> de sldb serve (b1). Las ACCIONES (advance, acknowledge, etc.) siguen por el CLI de deskops en proceso (DP4). La frase del SCOPE "lo pide a deskops en proceso como las acciones" vale solo para los agregados de b5: agents y runs los pide graph_ui al CLI de deskops en proceso (deskops view agents --format json), no a sldb serve.
c3 (golden de task): el id es el de una tarea fija del desk de prueba de b6, invocado como `deskops view task <id> --format json`. El fixture lo define.
c4 (normalización): se normalizan solo los valores de revision y de fechas, con los marcadores de b6. Todo lo demás se compara igual. "salvo revision" del contrato se lee como revision y fechas.
c5 (6 desks): "responde" quiere decir exit 0, JSON válido con las claves del contrato y sin error. Se registra por desk en el informe.
c6 (GET /views/board): devuelve el resultado de run_view, sin los agregados del CLI de b5. El test lo compara con `deskops view board --format json` quitando esos agregados.
c7 (desk_declaration.yaml): "hace falta" quiere decir que sldb serve sobre el store de prueba enlazado no encuentra las ViewDoc con b2 solo. Si las encuentra, el archivo no se toca.
c8 (tiempo): `time deskops view board --format json` sobre el desk real de deskops, en frío (primera corrida tras borrar .sldb_cache) y en caliente (segunda corrida). Los dos valores van al informe; la meta la verifica CC52.
c9 (alias y agents):
- Inventario de usos con `grep -rn "_read_doc\|_resolve_glob\|_registered_repositories\|_repository_root" deskops/ ~/proyectos/SLDB_1/UIs/graph_ui/frontends`; se borra cada alias sin usos tras el cambio.
- agents() y la lectura de runs pasan de desk_view.py a deskops/runtime/ (agents de herdr) o a cli/commands/view.py, sin cambiar su salida.
- Mapeo campo a campo del contrato (errors, counts, closeout, next, markdown, excerpt, command...): es parte del trabajo. El informe lleva una tabla campo -> fuente (ViewDoc por edges o rules, o agregado del CLI de b5); lo que no tenga fuente en el modelo, hipótesis y nota a sldb.
- revision/ETag: cubre lo que ETag de GD25 cubre para esa vista. Si un cambio del Board ya no invalida la revision de task como hoy (sha256 de Board más tarea), se deja escrito y el test de 409 de graph_ui lo prueba con el cambio que sí la invalida.

## Validation

_List the checks required before this task can close._

- deskops view board|task|drawer|inbox --format json idénticos a los goldens capturados primero (a3), salvo revision
- GET /views/board de sldb serve sobre el desk de prueba da el mismo payload
- graph_ui sirve board leyendo la vista nueva y POST /api/desk/advance con ETag viejo da 409
- grep de desk_view y DeskView vacío en deskops/ y en graph_ui frontends
- deskops view board responde en los 6 desks; tiempo frío y caliente registrado
- 4 pasos de deskops y CI completo de graph_ui en clones limpios

## Done When

_Name the observable condition that makes the task complete._

deskops view board|task|drawer|inbox --format json idénticos a los goldens capturados en el primer paso salvo el valor de revision; ayuda de view idéntica; GET /views/board de sldb serve sobre el desk de prueba devuelve el mismo payload; graph_ui sirve la vista board leyendo de sldb serve (test en graph_ui) y POST /api/desk/advance con un ETag viejo da 409; tests/test_desk_view.py reescrito sobre run_view y verde; grep de "desk_view\|DeskView" en deskops/ y en UIs/graph_ui/frontends vacío; deskops view board en los 6 desks responde; tiempo frío/caliente de view board sobre el desk real de deskops registrado (meta caliente < 1 s, la verifica CC52); CHANGELOG; docs/deskops-ui.md.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-cc34-vistas-de-la-ui-como-viewdoc-servidas-por-sldb-desk-view-py-desaparece: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

