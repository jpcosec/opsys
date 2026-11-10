REFORMULACION

**Resultado:** `deskops review status` debe clasificar cada clave (`task/<modo>` o `<plan>/<nodo>`) contra el SHA-256 del input exacto actual, no contra la mera existencia de recibos. Con registros de esa clave: (1) `accepted` si existe al menos un `ReviewDoc` con `verdict: accepted` e `input_sha256` actual; (2) si no, `rejected` si existe uno rechazado actual; (3) si no, `reviewed` si hay un `pending` actual; (4) si no, `technical_failure` si hay un `incomplete` actual; (5) si hay registros pero ninguno con el hash actual, `stale`; (6) sin registros, `missing`. Deben preservarse todos los recibos y el `run_dir`/provenance; no se alteran la generación de inputs, el modelo `ReviewDoc`, los gates de lifecycle ni la gramática CLI.

**Repo/archivos:** deskops. Cambios en `deskops/services/review.py` (fundamentalmente `_state_for_key`) y `tests/test_review_command.py`; nuevo átomo en `desk/atoms/workflow-model/`; reflejo en `docs/operator-manual.md` y `CHANGELOG.md`.

**Límites:** solo clasificación de estado de review, sus pruebas y documentación atom-backed. Fuera de alcance: gates de lifecycle, modelo, gramática/argumentos CLI, borrado o modificación de recibos, manifests o evidencia.

AMBIGUEDADES

Ninguna. El orden de precedencia, el filtro por hash actual, los estados resultantes y los límites están explícitos en la tarea y en el drawer.

DRY-RUN

**Lecturas:** TaskDoc, drawer, `deskops/services/review.py`, `tests/test_review_command.py`, rituales enrutados, pills, átomo destino, `docs/operator-manual.md` y `CHANGELOG.md`.

**Cambios hipotéticos:** en `_state_for_key`, calcular `current_sha`, filtrar por clave y por `input_sha256 == current_sha`, y evaluar en orden `accepted > rejected > pending > incomplete`. Si hay recibos de la clave pero ninguno con el hash actual, devolver `stale`; sin recibos, `missing`. Mantener `_review_records`, `_record_key`, `_run_one`, `_write_review`, `dispose` y `record_receipt` sin cambios de contrato. Crear el átomo con el contrato durable, reflejarlo en el manual y anotar el cambio en CHANGELOG.

**Pruebas hipotéticas:** crear tarea en desk aislado, ejecutar `review preflight` con `pi` falso, disponer `accepted`, y comprobar que `review status --format json` reporta `accepted`; añadir un rechazo o recibo viejo y verificar que no enmascara el aceptado actual; editar el input y verificar `stale`; cubrir `reviewed` con pending actual, `technical_failure` con incomplete actual y `missing` sin recibos.

**Validaciones:** `pytest tests/test_review_command.py`; estado real en desk aislado antes y después de una disposición aceptada; `pytest` en integración.

FUTURO

- Comprobar que «same existential condition as lifecycle» coincide con «al menos un recibo aceptado actual por clave»; si la regla de activación exige algo distinto, leer `desk/lifecycle/rule-activation-<type>.md` sin modificar gates.
- Confirmar que la salida CLI solo incorpora los nuevos valores de estado y que `--format json` sigue siendo estable.
- Verificar que `stale` no aparece cuando existe un estado actual `accepted`, `rejected`, `reviewed` o `technical_failure`.
- Confirmar que no se modifican recibos, `input.md`, `manifest.json` ni `receipt.json`.
