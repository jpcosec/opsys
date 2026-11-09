## REFORMULACION

Encargo del nodo CC33a (repo `deskops`): hacer que `deskops closeout verify` ejecute los productores de hechos y escriba un `ReviewDoc` `kind: evidence` por cada kind verificado (`tests`, `commit`, `atom`, `materialization`, `document`, `external`), con `fact`, `value`, `verdict` accepted/rejected y `subject` anclado al contrato de la tarea, sin duplicar recibos si el `input_sha256` no cambia. `verify_task_closeout` queda como orquestador y conserva el envelope actual. El gate de cierre no cambia hasta CC33b. Límites: solo `closeout_gates.py` (productores), `closure.py` (verify y productores), `models/review.py`, `cli/commands/closeout.py` si hace falta, tests y `CHANGELOG.md`; fuera quedan RuleDocs de cierre, borrado de `_add_closeout_facts`/`__closeout_evidence__`, grafo y `close_*`. No se commitea `desk/` ni `.sldb/`; goldens idénticos.

## AMBIGUEDADES

1. «subject anclado al contrato de la tarea» frente a «el pin llega en la primera reescritura; ver H-CC32-2: create_document no pinnea». Obliga a inventar si el primer recibo puede escribirse sin `@sha256` o si debe reescribirse de inmediato para quedar anclado.
2. «una verificación repetida sin cambios no crea recibo nuevo (mismo input_sha256)» frente a «editar goal deja los recibos changed (anchor_state)» y «input_sha256 = sha256 del valor verificado (fact + value + el hash de contenido del archivo o el id de commit)». Obliga a inventar qué cambio dispara la reescritura y si el hash debe incluir el contrato de la tarea, porque editar `goal` no altera `fact`, `value` ni el archivo/commit.
3. «como _write_review de services/review.py, sin llamar al modelo». Ese archivo no se suministra; obliga a inventar la API real de escritura, su firma y si «sin llamar al modelo» excluye la validación de `ReviewDoc`.

## DRY-RUN

Lecturas hipotéticas: `closure.py` (`verify_task_closeout`, `_closeout_link_gate`, `_skill_guard_test_evidence`, `_generated_artifact_source_finding`), `closeout_gates.py`, `models/review.py`, `cli/commands/closeout.py`, tests de closeout/review y `CHANGELOG.md`. Cambios previstos: añadir `evidence` a `ReviewKind` y `fact`/`value` opcionales con validador; escribir recibos por la vía de `_write_review`/transacción sldb; calcular `input_sha256` y buscar existente antes de escribir; invocar desde verify sin alterar el reporte. Dependencias: `_write_review` disponible, CC32/CC38 en main, CC35a. Validaciones futuras: tests nuevos por caso a7, goldens de ayuda/salida idénticos, `pytest` desde `/dev/shm` uno a uno, `wc -l` antes/después y CHANGELOG. Si cambia un golden, el ejecutor para.

## FUTURO

CC33b cambiará el gate y las reglas que leen los recibos, y retirará `_add_closeout_facts`/`__closeout_evidence__`; CC33c tocará el grafo. Un humano/coordinador debe resolver las ambigüedades 1–3 antes del despacho; el supervisor ejecutará la suite completa sobre el resultado integrado.
