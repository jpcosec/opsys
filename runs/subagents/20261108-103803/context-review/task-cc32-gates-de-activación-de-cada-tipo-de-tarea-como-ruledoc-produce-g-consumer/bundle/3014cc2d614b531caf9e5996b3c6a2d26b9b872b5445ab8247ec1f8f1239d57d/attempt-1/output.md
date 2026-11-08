## REFORMULACION

**Propósito:** sustituir `__activation_receipts__` por RuleDocs semilla `managed`, `on_transition` sobre `ritual-execution`, una por tipo de fábrica, y hacer visibles sus findings. **Resultado:** reglas en `deskops/data/rules/`, seeds/include en `desk_declaration.yaml`, borrado del inventario Python, `advance`/`next`/`show` mostrando `edges_blocked` (cláusula, nodo, valor visto), tests G_CONSUMER y por tipo, CHANGELOG y doc. **Repo:** deskops, worktree `wt/cc32` sobre `origin/main` sin CC35a. **Límites:** no tocar `doc_io.py` ni la capa de escritura de `doc_access.py`; no escribir en sldb, no enviar `message send --to sldb`, no editar rituales a mano, no crear status `blocked`.

## AMBIGUEDADES

1. «goldens de ayuda y salida idénticos» (Done When) frente a b4: «solo `show_task.text` y `show_task.json` ... pueden cambiar». Obliga a inventar si los goldens de salida deben quedar idénticos o si `show_task` se actualiza por la sección de findings.
2. «`ReviewDoc.subject` queda en `__doc_anchors__` (GO07), pinneado por sldb» frente al modelo suministrado: «Until GO07 exists the installed sldb does not resolve ... stays inert». Obliga a inventar si GO07 está disponible o si `anchor_state = changed` debe simularse.

## DRY-RUN

Nodo ejecutable, no agregado. Leería TaskDoc, `desk_declaration.yaml`, `task_types.py`, `review.py`, `lifecycle.py`, `services/tasks.py`, `next_actions.py`, `desk.py`, tests, `workflow-policy-reference.md` y CHANGELOG. Crearía `rule-activation-<tipo>.md` y sus seeds/include; borraría atributos, función y tests de `__activation_receipts__`; añadiría registro de `RuleDoc` en `write_lifecycle_graph`; pasaría `document` a `edges_holding` y compondría el mensaje con findings de `edges_blocked`; añadiría helper de recibos en tests; documentaría la tabla. Depende de sldb `RuleDoc`/`edges_blocked`/GO07, del grafo CC31 y de validadores CC38. Validaría con G_CONSUMER, tests por tipo, `grep`, `rules check`/`rules explain`, `pytest` indicado, `doctor` y `desk update --apply` en 6 desks, goldens, `wc -l`, CHANGELOG y doc. Sin ejecutar nada.

## FUTURO

El coordinador rebasa CC35a y resuelve conflictos, envía la nota a sldb y marca G_CONSUMER. Un humano decide la vía para recibos `reproduction`, `goldens` y `owner`, y el campo futuro `children`. CC33/CC37 cubren cierre y consistencia; `models/task.py` queda como seguimiento.
