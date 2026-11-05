REFORMULACION
GC10 encarga a deskops implementar la promoción nodo a nodo desde un `dag.yaml` del drawer: `add task --from-drawer <plan-dir>/dag.yaml --node <ID>` debe crear el TaskDoc con title, goal, scope, validation, done_when, files, task_type por kind, from_drawer, depends_on de prerrequisitos promovidos y parent_id del agregado del paquete creado al vuelo; guardar `promoted` y permitir que `review status <plan-dir>` cruce nodo y tarea. Repo dueño: deskops. Límites: no transfiere revisiones de nodo al TaskDoc, no toca `build_plan.py`/`validate_plan.py` ni sldb, y se ciñe al `output_scope`. Depende de GC03 y GC09.

AMBIGUEDADES
1. `"add task --from-drawer ... --node <ID> crea el TaskDoc del nodo"` y `"parent_id = la tarea task.aggregate del paquete ... creada por este mismo comando"` no excluyen promover un nodo `node_role: aggregate`; alcance dice `"nunca se promueve el agregado; se promueven los hijos"`. El ejecutor debe inventar si `--node PC03` falla, se ignora o crea tarea.
2. `"(única escritura al drawer; idempotente)"` contradice `"una segunda promoción del mismo nodo falla como duplicado"`. Hay que inventar si repetir es no-op exitoso o error; la aceptación apunta a error, el scope a idempotencia.
3. `"review status <plan-dir> muestra por nodo la tarea promovida y el estado de sus revisiones"`: `"sus"` no define si son los `ReviewDoc` de nodo con `subject_ref` anteriores, los preflight/bundle del TaskDoc promovido, o ambos. Obliga a inventar el filtro y el esquema de salida.

DRY-RUN
Lecturas: `dag.yaml` (GC10, aristas GC03/GC09/PC03, gates), brief/alcance/decisiones, `services/drawer.py`, `services/tasks.py`, `services/review.py`, registry CLI, tests y docs. Cambios previstos: parser del dag y opción `--node`, creación de TaskDoc y agregado, escritura `promoted`, status por plan, pruebas, CHANGELOG y manual. Dependencias: GC03 (review, ReviewDoc, status) y GC09 (parent_id, children, task.aggregate); los `G_SLDB_*` solo se leen como estado. Validaciones futuras: `pytest tests` y casos de aceptación en desk temporal (duplicado, prerrequisito ausente, gate pending, status). Nada se ejecuta.

FUTURO
GC03 entrega el comando review/status; GC09 entrega parent_id/children/task.aggregate; sldb cierra sus gates; el dueño autoriza ejecución y el operador del desk dispone los ReviewDoc. No son ambigüedades de GC10.
