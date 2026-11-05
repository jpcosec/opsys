REFORMULACION
Propósito: que los tipos de tarea dejen de ser cadenas sueltas y pasen a ser modelos TaskDoc con jerarquía, evidencia de cierre y receipts declarados en el tipo. Resultado: `deskops/models/task_types.py` con las subclases indicadas; registro en `MODEL_REFS` y herencia por desk; `add task --task-type` validado, default `task.code` con aviso; evidencia leída del tipo, con `--evidence` solo aditivo; migración idempotente en `desk update --apply`; fixtures, CHANGELOG y docs actualizados. Repo: `deskops`. Límites: no tocar `sldb`, no editar a mano `desk/` ni `.sldb/`, trabajar en `deskops-wt-gates`, rama `wt/gates-por-tipo`, sin push a main ni `git add -A`; fuera de alcance lo que fije `brief.md §Fuera de alcance`. Es un nodo ejecutable de código, no un agregado.

AMBIGUEDADES
1. “tabla de brief.md §Tipos” y “Fuera de alcance: brief.md §Fuera de alcance”: faltan la tabla y los límites; obliga a inventar qué evidencia/receipts corresponde a cada tipo y qué queda excluido.
2. “sintaxis de sldb GO02 (e); si la versión de sldb instalada no la lee”: no se define la sintaxis ni la versión; obliga a inventar el formato de `__contract__` y su comportamiento.
3. “tupla del vocabulario de closeout_gates.py:23” y “kinds de ReviewDoc”: no se enumera el vocabulario ni el mapeo por tipo; obliga a inventar las tuplas `__closeout_evidence__` y `__activation_receipts__`.
4. Migración: “code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code”: no cubre `debug`, `refactor`, `decision`, `aggregate` ni valores desconocidos; obliga a inventar su destino.
5. “pendiente del dueño en decisiones.md”: no se incluye la decisión; obliga a inventar si el piso de evidencia admite excepciones o solo agregados.
6. “override por encima del tipo”: no aclara si reemplaza o se une a la evidencia del tipo; obliga a inventar la semántica de cierre.
7. “Produce G_TYPES”: no se define el artefacto ni dónde materializarlo; obliga a inventar el entregable.

DRY-RUN
Lecturas: modelos, bootstrap, servicios de cierre/tareas, operaciones, CLI, workspace, tests/fixtures, docs y CHANGELOG. Cambios previstos: crear subclases; registrar en `MODEL_REFS`; validar `--task-type`; cambiar origen de evidencia; migrar tareas; actualizar hashes, docs y CHANGELOG. Dependencias: brief, sldb, `decisiones.md`, GC05/GC09 y `ReviewDoc`. Validaciones futuras: aceptación listada, `pytest tests`, grep de `TASK_TYPE_EVIDENCE`, fixtures y migración doble.

FUTURO
Deben aportarse `brief.md §Tipos`, la decisión del dueño y la capacidad/versión de sldb; GC05 fija receipts, GC09 `parent_id/children` y verificación de goldens. Un humano resuelve evidencia y migración de tipos no listados.
