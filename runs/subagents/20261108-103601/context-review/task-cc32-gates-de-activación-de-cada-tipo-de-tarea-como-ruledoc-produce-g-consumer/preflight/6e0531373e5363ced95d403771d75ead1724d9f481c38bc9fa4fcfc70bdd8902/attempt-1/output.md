## REFORMULACION
Nodo ejecutable (no agregado). Sustituir la tabla `__activation_receipts__` por RuleDocs semilla managed `on_transition` sobre ritual-execution (una por tipo, exigiendo recibos accepted/intactos y depends_on cerradas), borrar los atributos y mostrar en advance/next/show los findings de edges_blocked. Resultado: G_CONSUMER en tres pasos, reglas en desk/lifecycle/, docs y CHANGELOG; la nota a sldb la envía el coordinador. Repo: deskops sobre origin/main 7bb0f168 sin CC35a. Límites: no tocar doc_io.py ni la capa de escritura de doc_access.py; cambios mínimos en lifecycle.py, services/tasks.py y cli/commands/desk.py; nada a mano en desk/ ni en sldb; formato de desk y gramática CLI intactos; fuera CC35b-d, CC37, CC33.

## AMBIGUEDADES
1. "mientras tanto el tipo no tiene regla de activación de hijos" vs. a5 "task.aggregate no tiene RuleDoc; si lleva depends_on, se decide en el informe": ¿regla vacía o ninguna?, ¿aplica depends_on?
2. "Los chequeos ... que el inventario de CC38 asigna a CC32 pasan a RuleDoc aquí y su chequeo viejo se borra" vs. a3 "0 para CC32 ... no tiene objeto": ¿hay algún chequeo que borrar?
3. "message en español que nombra el tipo" vs. "el mensaje nombra la cláusula any(^subject: kind = "preflight" ...)": contenido exacto del mensaje.
4. "goldens de ayuda y salida idénticos" vs. "el mensaje de bloqueo lista los findings ... en lugar de las condiciones crudas": cómo no alterar goldens de salida.
5. "seeds managed ... (file: rules/<archivo>), con su include": falta el esquema YAML; obliga a inventar la forma de declaración.
6. "lista en el informe" (a9, a10, a12): no se define ruta ni formato del informe.
7. "solo si la salida de desk update lo necesita": criterio indeterminado para tocar desk.py.
8. "la vía de escritura existente de deskops ... o con sldb.api" para reproduction/goldens/owner: sin comando, no se dice qué función usar.

## DRY-RUN
Lecturas: desk_declaration.yaml, models/task_types.py y review.py, lifecycle.py, services/tasks.py, workflow/next_actions.py, cli/commands/desk.py, tests, docs/workflow-policy-reference.md, CHANGELOG y API edges de sldb. Cambios: crear deskops/data/rules/*.yaml, seeds+include, borrar `__activation_receipts__` y sus tests, mensaje de advance/next/show con findings, tests por tipo y G_CONSUMER, docs y CHANGELOG. Dependencias: CC31/CC38 en main; review CLI solo emite preflight/bundle/node. Validaciones futuras: pytest por archivo, grep vacío, dos `desk update --apply` idempotentes en copia, doctor en 6 desks, sldb rules check/explain, goldens. Nada ejecutado.

## FUTURO
El coordinador envía la nota a sldb con el hash y marca G_CONSUMER; corre los comandos de rituales listados (a12) y decide sobre task.aggregate/depends_on. El dueño decide sobre recibos sin comando (reproduction, goldens, owner) y sobre tareas de ritual-execution que quedarían bloqueadas. El supervisor corre la suite completa.
