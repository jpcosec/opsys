| Objeto | Evidencia real | Veredicto |
|---|---|---|
| SYSTEM con instrucción durable y cláusula de agregado | `context_review.py:25-37`; test de subcadenas `tests/test_context_review_helper.py:110` | PASS |
| `FILE:instruccion` en bundle sin cambios | `context_review.py:138` vs evidencia registrada ROOT `.../ROOT/c5aaff.../attempt-1/input.md:480` y WS12 `.../attempt-2/input.md:1094` | PASS |
| Una prueba sostiene de verdad que `FILE:instruccion` no cambió | `tests/test_context_review_helper.py:108-112`: solo prueba independencia de `SYSTEM`; el hash se calcula al vuelo | FAIL |
| `--new-attempt` exige ids y razón, rechaza `--stale` | `context_review.py:261-264`; `tests/test_context_review_helper.py:87-94` | PASS |
| Sin flag reutiliza answered y no llama al proceso | `context_review.py:185`; `tests/test_context_review_helper.py:65-69` | PASS |
| Intento nuevo aunque haya answered | `context_review.py:185`; `tests/test_context_review_helper.py:72-76` | PASS |
| Manifest/recibo por intento: número, argv, versión, sha de prompt, retry | `context_review.py:198-225`; `tests/test_context_review_helper.py:79-84` | PASS |
| `retry_of` apunta al intento previo y no a sí mismo | `context_review.py:202`; `tests/test_context_review_helper.py:83` | PASS |
| `attempts` no lanza, dos valores, incompleto ni answered ni fallo | `context_review.py:167-178`; `tests/test_context_review_helper.py:49-56` | PASS |
| `receipt_state` con `technical_failure` y campos faltantes | `context_review.py:159-164` | PASS en código; caso no cubierto en test |
| `stale_reviews` reporta incompleto y usa `evidence[0]` | `context_review.py:246-247`; `tests/test_context_review_helper.py:97-105` | PASS |
| Evidencia registrada con `technical_failure: true` | `context_review.py:247`: solo compara con `incomplete` | FAIL |
| Pruebas sin proveedor | `tests/test_context_review_helper.py:33-34` | PASS |
| Aserciones débiles/vacías | `tests/test_context_review_helper.py:55,110-112` | FAIL |
| Nada rellena recibos históricos | `context_review.py:143-149,193-225`; recibo/manifest históricos de WS12 solo leídos | PASS |
| `validate_plan.py` y `build_plan.py` intactos | `validate_plan.py:18,32-34` y `build_plan.py:22` compatibles; diff solo en `tester-facts.log` | NO VERIFICADO (dato del Supervisor) |

Hallazgos:
- `stale_reviews` trata una evidencia con `technical_failure: true` como vigente: no devuelve problema, por lo que `status`/validación no fuerzan repetición. `attempts` solo la cuenta como fallo si `stdin == 'devnull'` (`context_review.py:174`).
- El test de `SYSTEM` no fija un hash ni compara el texto de `FILE:instruccion`; pasaría aunque ese bloque se alterara.
- `test_incomplete_receipt_does_not_raise_nor_answer` no cubre `technical_failure: true` con campos faltantes; el código lo clasifica bien, pero sin prueba.
- En una corrida forzada, los intentos posteriores al primero no llevan `retry_reason` ni `retry_of` (`context_review.py:202`).
- No ejecuté pytest, el helper ni git; lo relativo a intocados y a `11 passed` es dato del Supervisor.

RESULTADO: FAIL
