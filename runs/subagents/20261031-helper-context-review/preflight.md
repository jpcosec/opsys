REFORMULACION

Objetivo: reparar `desk/drawer/plans/workspace-documental/context_review.py` para que tenga instrucción durable, permita intento nuevo tras rechazo semántico, genere manifest y recibo propios por intento y reconozca recibos históricos incompletos sin crash. Alcance: solo ese archivo y `tests/test_context_review_helper.py`, más evidencia en `runs/subagents/20261031-helper-context-review/`. Repo: `deskops`. Límites: no tocar `validate_plan.py`, `build_plan.py`, `dag.yaml`, `brief.md`, UI, Scion ni repos hermanos; conservar `all_nodes` y `stale_reviews`; el Executor no commitea, no hace closeout y no corre `context_review.py run`. El Supervisor valida, commitea y cierra; el Tester independiente es de solo lectura. La repetición de las revisiones de WS12/WS37 queda asignada a la tarea de cierre siguiente: es tarea futura, no laguna.

AMBIGUEDADES

1. “Se expone una función que clasifica un recibo en completo, incompleto o fallo técnico, listando los campos faltantes.” No fija nombre, firma, tipo de retorno ni qué campos integran “completo”. Obligaría a inventar la API y el criterio; las pruebas dependen de ello.

2. “cuando el intento registrado en dag.yaml como evidencia tiene recibo incompleto” no define cómo localizar ese intento —campo, ruta, matching por input o número— ni el tipo exacto de elemento de `stale_reviews`. Obligaría a inventar el enlace `dag.yaml`-recibo.

3. “argv efectivo” no precisa si incluye ejecutable, flags, orden o normalización de rutas. El requisito de manifest “coherentes con argv” obliga a inventar la representación exacta.

4. “Crea un intento nuevo … attempt-n+1” y “número real de intento” no fijan base de numeración, formato ni qué ocurre sin intento previo. Obligaría a inventar la numeración.

5. “status lista exactamente WS12 y WS37” presupone que no hay otros recibos incompletos; el texto no muestra el estado completo. Si existieran, “exactamente” sería insatisfacible sin tocar datos fuera de alcance.

DRY-RUN

Un ejecutor futuro leería `context_review.py` y `validate_plan.py`; editaría solo `context_review.py` y `tests/test_context_review_helper.py`; añadiría cláusulas a `SYSTEM` e `INSTRUCTION_VERSION`; implementaría `--new-attempt` con validación de ids y razón; generaría manifest y recibo por intento; añadiría el clasificador y adaptaría `attempts()`/`stale_reviews`; escribiría pruebas con stub de `Popen`/`pi` y `RUN`/`ROOT` en `tmp_path`; ejecutaría pytest, `build_plan.py --check`, `status` y el `git diff` indicado; dejaría `result-summary.md`. No ejecutaría `run` ni commitearía. Errores esperados: el `KeyError` actual con WS12/WS37; `validate_plan.py --check` fallará por recibos incompletos; posible fallo si hay más incompletos o si `build_plan.py` consume `stale_reviews`. Resultado esperado: cuatro requisitos, pytest verde, build verde, status exactamente WS12/WS37 y Tester PASS.
