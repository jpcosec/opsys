## REFORMULACION
El encargo es corregir `ReviewService._state_for_key` en `deskops/services/review.py` para que el estado de review refleje la disposición real del input exacto actual. Para cada clave: reunir todos los `ReviewDoc` de esa clave; sin registros → `missing`; calcular `current_sha = _sha(input_data)` sin cambiar normalización ni builders; filtrar registros con `input_sha256 == current_sha`; si hay registros pero ninguno coincide → `stale`, sin importar veredictos antiguos. Entre los coincidentes aplicar prioridad existencial: aceptado > rechazado > pendiente (`reviewed`) > incompleto (`technical_failure`). Esto debe preservar todos los recibos y su provenance, y alinearse con la semántica lifecycle de “cualquier aceptado actual”, sin cambiar gates.

Alcance: solo clasificación de review status, sus tests y documentación respaldada por átomo. Fuera de alcance: gates de lifecycle, modelo o gramática CLI. Entregables: cambio en `review.py`; regresiones en `tests/test_review_command.py` usando sus fixtures reales de desk aislado y CLI; átomo `atom-review-status-preserves-current-dispositions` registrado vía CLI antes de tocar docs; actualización de `docs/operator-manual.md` y `CHANGELOG.md`. Resultado esperado: un accepted actual sobrevive al status y receipts rejected/stale antiguos no lo enmascaran; un cambio de input reporta `stale`; los contratos existentes de pending y technical failure se mantienen.

## AMBIGUEDADES
Ninguna. El camino de implementación fija la identidad por `_sha` del input exacto, el orden de prioridad y los estados resultantes; no hay una decisión de política pendiente que obligue a improvisar.

## DRY-RUN
Lecturas hipotéticas: `deskops/services/review.py` en `_state_for_key`, `_review_records`, `_record_key`, `status`, `_sha`, builders de input; `tests/test_review_command.py` y sus fixtures de desk aislado; átomo indicado; `docs/operator-manual.md`; `CHANGELOG.md`; Board, rituales y pills suministrados.

Cambios hipotéticos: reemplazar la lógica actual de `_state_for_key` por la secuencia registros→missing, filtrado por hash actual→stale, y prioridad accepted/rejected/pending/incomplete. No tocar `_sha`, builders, `dispose`, `record_receipt`, modelo `ReviewDoc` ni gramática CLI. Añadir escenarios de regresión: accepted actual con rejected antiguo; rejected actual; pending actual como `reviewed`; incomplete actual como `technical_failure`; input editado como `stale`; sin registros como `missing`; preservación de recibos/provenance. Crear el átomo mediante CLI antes de modificar documentación; reflejarlo en manual y changelog.

Validaciones futuras: `pytest tests/test_review_command.py`; comprobación real de `review status` en desk aislado tras disposición accepted; `pytest` de integración. Nada se ejecuta en esta revisión.

## FUTURO
Comprobaciones de implementación, no ambigüedades: verificar que no se alteran gates ni contratos lifecycle; que accepted/rejected actuales no se confunden con receipts antiguos; que `stale` aparece solo con registros sin hash actual; que pending sigue dando `reviewed` y technical failure sigue dando `technical_failure`; que se preservan recibos, run provenance y evidencia; que el átomo queda enlazado y la documentación lo materializa; que las pruebas usan CLI real sobre desk aislado y que el cierre declara la evidencia exacta.
