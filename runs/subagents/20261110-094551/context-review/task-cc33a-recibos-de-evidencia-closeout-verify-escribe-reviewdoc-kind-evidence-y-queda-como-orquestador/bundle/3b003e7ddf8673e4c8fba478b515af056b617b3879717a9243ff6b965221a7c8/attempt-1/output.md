## REFORMULACION
Nodo CC33a (hijo del agregado CC33, plan `deskops-como-config` dag rev 4), repo **deskops**. Propósito: que `deskops closeout verify` corra los productores de hechos y escriba, por cada kind verificado, un `ReviewDoc` kind `evidence` (fact, value, verdict, subject anclado), sin duplicar recibos si la verificación se repite sin cambios; `verify_task_closeout` queda como orquestador y devuelve el mismo envelope. El gate de cierre **no** cambia (eso es CC33b). Límites: fuera RuleDocs, borrado de `_add_closeout_facts`/`__closeout_evidence__`, grafo y los `close_*`.

## AMBIGUEDADES
1. `fact` unidad: a2 lista `atom|materialization` como `Literal` separados, pero b1 dice "atom y materialization: el enlace de `_closeout_link_gate`" (un solo gate). Obliga a inventar si son **dos recibos** o uno.
2. `reason` en accepted: solo se define "reason es el texto que hoy da el gate cuando falta ese kind". El modelo exige razón también en accepted; falta su texto.
3. Orden de `value`: b2 dice "ordenado … unido con «\n»" sin criterio (¿léxico? ¿por kind?) para ids de atom/materialization.
4. Umbral de `_write_review`: "Si reusar `_write_review` exige tocar `review.py` más allá de lo mínimo" — "lo mínimo" no está definido.
5. `anchor_state` al decidir skip (c2): b4 dice que lo calcula sldb, pero no cómo lo lee `verify` al escribir (¿índice? ¿`check_doc_anchors`?).
6. Golden cambiado: a4 dice "el worker para y avisa", pero la aceptación exige goldens idénticos; no dice si parar o corregir.

## DRY-RUN
Lecturas: `closeout_gates.py`, `closure.py` (`verify_task_closeout`, `_closeout_link_gate`, `_skill_guard_test_evidence`, `_generated_artifact_source_finding`), `models/review.py`, `cli/commands/closeout.py`, `services/review.py` (`_write_review`), `services/atoms.py`, tests `test_closeout*`, `test_review_doc`, goldens. Cambios previstos: añadir `evidence` a `ReviewKind` y campos `fact`/`value` con validador; helper de recibo en `closure.py` (o `review.py`) sobre `doc_access.create_doc` + reescritura que pinnea (c1); skip por `input_sha256`+anchor (c2); productores intactos. Dependencias: CC32/CC38 en main, CC35a. Validaciones futuras: tests por caso a7, goldens help/output, `wc -l` antes/después, CHANGELOG.

## FUTURO
CC33b cambia las reglas de activación y retira `_add_closeout_facts`; CC33c migra el grafo; el supervisor corre la suite completa integrada; si `closeout resolved-by` entra antes, el worker rebasea.
