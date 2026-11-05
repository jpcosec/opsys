## REFORMULACION

GC09 es un nodo `code` de entrega en deskops (padre PC03). Propósito: dotar a `TaskDoc` de composición —`parent_id` y `children` como referencias—, `add task --parent`, alerta de `doctor`, regla de activación de `task.aggregate`, evidencia de cierre `children` y visualización en `show`/`next`. Resultado: tareas agregadas y jerarquías verificables por sldb, con cierre que exige los hijos. Límites: no toca sldb; no escribe Python que supla reglas; depende de GC01 y GC05 y requiere `G_SLDB_LANG`.

## AMBIGUEDADES

1. «Los agregados no se promueven ni se despachan: deskops advance de un agregado cuyo gate se cumple lo lleva a ritual-testing y de ahí a closeout como cualquier tarea». Contradice “no se despachan” con “como cualquier tarea”; obliga a inventar si el agregado recorre el ritual de testing o solo se cierra, y qué aceptación tiene ese paso.

2. «el ritual de testing para un agregado es la validación conjunta de la fase (phase.md)». `phase.md` no está en el input ni en `output_scope`; obliga a inventar qué validación conjunta es, quién la produce y cómo se comprueba.

3. «deskops doctor alerta cuando parent_id y children no se corresponden». El cierre borra el archivo del hijo (DC6, brief), pero el padre conserva su id en `children`; no se dice si `doctor` ignora hijos cerrados/borrados o alerta. Obliga a inventar esa regla.

## DRY-RUN

Lecturas: `models/task.py`, `models/task_types.py`, `services/tasks.py`, `services/closeout_gates.py`, `services/rules.py`, `doctor_findings.py`, `cli/registry.py`, `cli/commands/operations.py`, `closure.py:570`, fixtures de hashes y docs. Cambios previstos: campos y referencias en el modelo, transacción de `add task --parent`, regla del agregado, verificación de cierre, hallazgos de `doctor`, listados, tests y fixtures, `CHANGELOG`, `docs/workflow-policy-reference.md`. Dependencias: tipos y `__closeout_evidence__` de GC01; reglas y `edges_blocked` de GC05; versión de sldb con `G_SLDB_LANG` pinneada. Validaciones futuras: `pytest tests`, escenarios de aceptación (padre no agregado, correspondencia, bloqueo/activación, cierre fallido), `desk update --apply` idempotente, hash de contrato actualizado.

## FUTURO

GC10 consume `parent_id`/`children` y crea el agregado al promover nodos; GC11 expone esas aristas en `graph`; el dueño confirma pendientes de `decisiones.md` y dispone las revisiones; el resolver de `G_SLDB_LANG` pinnea la versión de sldb.
