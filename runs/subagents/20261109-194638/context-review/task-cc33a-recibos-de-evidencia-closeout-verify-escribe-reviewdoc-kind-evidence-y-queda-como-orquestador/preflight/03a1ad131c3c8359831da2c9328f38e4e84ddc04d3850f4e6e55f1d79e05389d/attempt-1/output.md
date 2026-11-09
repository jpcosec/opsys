## REFORMULACION

Encargo del nodo CC33a (task.code, hijo del agregado CC33): en el repo deskops, hacer que `deskops closeout verify` ejecute los productores de hechos (git y archivos) y escriba, por cada kind verificado, un `ReviewDoc` kind `evidence` con `fact`, `value`, `verdict` accepted/rejected, reason y subject anclado al contrato de la tarea; sin duplicar recibos si el `input_sha256` no cambia. `verify_task_closeout` queda como orquestador y devuelve el mismo envelope. Límites: no cambia el gate de cierre (CC33b), no toca RuleDocs, `_add_closeout_facts`, `__closeout_evidence__`, grafo, `close_superseded/retired/with_run/resolved_by`. Superficies: `closeout_gates.py`, `closure.py`, `models/review.py`, `cli/commands/closeout.py`, `tests/`, `CHANGELOG.md`.

## AMBIGUEDADES

1. "verdict accepted o rejected" — solo se fija el rechazo de commit: "sin commit, el recibo commit queda rejected". No hay criterio de rechazo para tests, atom, materialization, document ni external; obligaría a inventar predicados por kind.
2. "value, verdict accepted o rejected" / "input_sha256 = sha256 del valor verificado (fact + value + el hash de contenido del archivo o el id de commit)" — no se define qué es `value` ni cómo se hashea en atom, materialization o external; obligaría a inventar representación y canonicalización.
3. "deskops/services/closure.py (solo la llamada a verify)" frente a "closure.py entra en files completo para verify y sus productores, no solo «la llamada a verify»" — contradicción de alcance; obligaría a inventar el límite editable.
4. "editar goal deja los recibos changed (anchor_state)" — no se nombra campo ni mecanismo de `anchor_state` en el modelo ni en el scope; obligaría a inventar su representación.
5. "por la vía de escritura de deskops sobre sldb (CC35a)" — CC35a no figura en `depends_on` (vacío) ni en `files`; obligaría a decidir si ya existe.

## DRY-RUN

Lecturas: los cinco archivos de código, `tests/test_closeout*.py`, `test_review_doc.py`, goldens. Cambios previstos: añadir `evidence` a `ReviewKind`, campos `fact`/`value` y validador en `review.py`; escribir recibos desde `verify_task_closeout` vía `_write_review`, dejando productores y envelope intactos; ajustar `closeout.py` solo si la salida lo exige; tests nuevos por caso; CHANGELOG. Dependencias: CC32/CC38 en main, CC35a, rebase si `close_resolved_by` se integra antes. Validaciones futuras: `pytest -q` por archivo con `TMPDIR=/dev/shm`, goldens sin `--update-golden`, `wc -l` antes/después, CHANGELOG.

## FUTURO

CC33b leerá los recibos y cambiará el gate; CC33c el grafo. El supervisor corre la suite completa sobre lo integrado y decide el worktree; el overlord habilita cuota; el coordinador dispone hallazgos de preflight/cold-bundle.
