## REFORMULACION
GC07 es un nodo `delivery` del repo deskops. Propósito: dejar de resolver la herencia de tareas recorriendo `inherits_from` en Python y obtener la clausura de ancestros desde sldb; calcular `effective_*` sobre esa lista; hacer que los ciclos no sean error; y que el cierre lea `effective_references`/`effective_atoms` en vez de los campos crudos. Resultado: `_resolve_task_payload` y `_closeout_reference_evidence` adaptados, `closeout_gates.py` leyendo efectivos, tests y CHANGELOG. Límites: `output_scope` acotado a `operations.py`, `closeout_gates.py`, `tests/` y `CHANGELOG.md`; depende de GC01 y requiere `G_SLDB_LANG`; no toca sldb ni introduce Python que supla reglas.

## AMBIGUEDADES
1. “effective_pills = pills de A ∪ B ∪ C en ese orden” frente a “el orden que sldb devuelve (hipótesis: el orden de un conjunto alcanzado por camino lo fija GO05; si no, deskops ordena por id y lo documenta)”. La aceptación no fija si “ese orden” es A→B→C, el orden de sldb o id, ni si hay deduplicación. Obliga a inventar el orden esperado del test.
2. “un ciclo deja de ser error y se documenta”. No dice dónde ni qué documentar; la aceptación solo exige que no haya `ValueError` y que desaparezca “Task inheritance cycle”. Obliga a inventar destino y contenido de esa documentación.

## DRY-RUN
Un ejecutor futuro leería `operations.py:1028-1071`, `closeout_gates.py:129,146`, los tests de herencia y los contratos GO02(b)/GO05. Cambiaría `_resolve_task_payload` por una consulta de clausura `inherits_from+`, sin duplicados y sin origen; eliminaría el error de ciclo; calcularía `effective_*` en el orden resuelto; adaptaría `_closeout_reference_evidence` y el gate de cierre a `effective_references`/`effective_atoms`; ajustaría tests y CHANGELOG. Dependencias: GC01 cerrado y `G_SLDB_LANG` satisfecho en `pyproject.toml`. Si GO04 no está, seguiría leyendo ancestros por `doc_io`. Validaría con los casos de aceptación, tests existentes, grep y ciclo.

## FUTURO
GC01 entrega los tipos registrados; sldb GO05 fija o no el orden de la clausura; el operador del desk confirma la hipótesis de orden y el lugar de documentación; GC08 alinea manual y rituales.
