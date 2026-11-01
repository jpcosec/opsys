# Resultado del Executor: helper context_review

Cambios en `desk/drawer/plans/workspace-documental/context_review.py`:
- SYSTEM incorpora REFORMULACION/DRY-RUN hipotético y la cláusula de agregado o paquete; `INSTRUCTION_VERSION = 'v2-ejecucion-hipotetica'`. `FILE:instruccion` de bundle() sin cambios.
- `receipt_state(receipt)` -> (`complete`|`incomplete`|`technical_failure`, campos faltantes). `attempts()` lo usa, sigue devolviendo dos valores y no lanza; un incompleto no cuenta como answered ni como fallo.
- `review(d, node, reason='')`: con razón crea intento nuevo aunque haya answered. Manifest y recibo por intento: `instruction_version`, `system_prompt_sha256` (del argv efectivo), `retry_reason`, `retry_of` (solo primer intento forzado).
- CLI `run <ids> --new-attempt --reason <texto>`; `parser.error` sin efecto si faltan ids o razón, con --stale, o `--reason` sin flag.
- `stale_reviews` agrega `<id>: receipt incomplete` (receipt.json ausente o incompleto en evidence[0]).

Pruebas: `tests/test_context_review_helper.py`, 11 passed (Popen y `pi --version` simulados, RUN/ROOT en tmp_path).

Verificación:
- `status` lista: `WS12: receipt incomplete`, `WS37: receipt incomplete` (solo esos).
- `build_plan.py --check`: pasa.
- `validate_plan.py --check`: falla solo por `['WS12: receipt incomplete', 'WS37: receipt incomplete']`.

## Corrección tras FAIL del Tester
- `stale_reviews` reporta también `<id>: receipt technical failure` para evidencia con technical_failure verdadero.
- En corrida forzada, todos los intentos llevan `retry_reason` y `retry_of` (intento inmediatamente anterior).
- Pruebas nuevas: texto fijo de `FILE:instruccion` (normal, ROOT, PK), receipt_state con fallo técnico y campos faltantes, stale technical failure, corrida forzada con fallo y éxito. Resultado: 13 passed. `status` sigue listando solo WS12 y WS37 como receipt incomplete.
