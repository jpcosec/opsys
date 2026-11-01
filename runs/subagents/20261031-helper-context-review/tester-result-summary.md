| Objeto | Evidencia real (leída) | Veredicto |
|---|---|---|
| 1. `technical_failure: true` ya no pasa como vigente en `stale_reviews`, con prueba | `context_review.py:159-163` (devuelve `technical_failure`), `:246-249` (solo `state != 'complete'` genera problema); test `tests/test_context_review_helper.py:99-107`, caso n=3 espera `receipt technical failure` | PASS |
| 2. Prueba de `FILE:instruccion` fija el texto y falla si cambia; cubre nodo normal, ROOT y PK; independencia de SYSTEM | Real `context_review.py:138`; texto fijado en test `:118-128` con igualdad exacta (`ROOT_CLAUSE` + `tail` independientes); normal = `tasks[0]`=WS01, ROOT = `dag.yaml:2975-2976`, PK = `packages[0]`=PK01 (`dag.yaml:3019-3020`); independencia en `:111-115` | PASS |
| 3. `receipt_state` cubre `technical_failure` con campos faltantes, con prueba | `context_review.py:159-163`; test `:56-57` compara tupla exacta `('technical_failure', faltantes)` y `:58` el caso completo | PASS |
| 4. Corrida forzada: cada intento con `retry_reason` y `retry_of` al anterior, también si el primero falla técnicamente; no auto-referencia | `context_review.py:192-202` (`prev` = último `attempt-*` existente antes de crear `out`), `:222-225` (recibo) y `:204-208` (manifest); test `:131-144` verifica attempt-2→attempt-1, attempt-3→attempt-2 y `technical_failure` en attempt-2 | PASS |
| 5. Regresión: `attempts` con dos valores, reutilización de answered sin flag, manifest propio | `context_review.py:167-177` devuelve `(failed, answered)`; `:185` reutiliza answered solo sin `reason`; `:204` escribe manifest por intento; tests `:67-71` y `:74-86` | PASS |
| 6. Aserciones que pasarían con comportamiento roto | Revisadas todas: `:52` sola sería débil pero la complementa `:70`; `:82` solo eco de la constante; `:113` solo dos subcadenas de `SYSTEM`; `:115` no cubre una copia de `SYSTEM` capturada al importar | PASS (sin enmascarar 1-5) |

Hallazgos:
- Los cinco comportamientos auditados están implementados y las pruebas los distinguen con igualdades exactas; no encontré una aserción que deje pasar 1-5 en estado roto.
- Aserciones débiles residuales: `tests/test_context_review_helper.py:82` (eco de `INSTRUCTION_VERSION`), `:113` (solo dos subcadenas de `SYSTEM`), `:115` (no detectaría `SYSTEM` capturado en constante de módulo).
- `retry_of` se calcula sobre el último `attempt-*` existente antes de crear el directorio (`context_review.py:193`), por lo que no puede apuntar a sí mismo.
- No ejecuté pytest, el helper ni git; `tester-facts.log` es dato del Supervisor y no lo usé como prueba.

RESULTADO: PASS
