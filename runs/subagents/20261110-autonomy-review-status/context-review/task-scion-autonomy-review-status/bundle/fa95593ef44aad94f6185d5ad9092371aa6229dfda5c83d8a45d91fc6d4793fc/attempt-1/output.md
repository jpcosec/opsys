REFORMULACION  
Propósito: corregir la clasificación de `deskops review status` para que una disposición aceptada/rechazada vigente se reporte fielmente para el input exacto actual, evitando fallos técnicos falsos y bucles de revisión. Resultado: en `deskops/services/review.py`, `_state_for_key` debe reunir los registros de la clave; sin registros, `missing`; con registros pero ninguno cuyo `input_sha256` coincida con `_sha(input_data)`, `stale`; entre los coincidentes, prioridad existencial `accepted > rejected > pending` (estado `reviewed`) `> incomplete` (estado `technical_failure`). Conservar recibos y procedencia; añadir regresiones en `tests/test_review_command.py`; registrar el átomo por CLI antes de tocar `docs/operator-manual.md`. Repo: deskops. Límites: solo clasificación de estado, tests y documentación respaldada por átomo; sin cambios de gates, modelo ni gramática CLI; normalización y builders existentes intactos.

AMBIGUEDADES  
1. «pytest at integration»: no nombra suite ni comando; obligaría a inventar qué prueba de integración ejecutar.  
2. «Record atom-review-status-preserves-current-dispositions via CLI»: el input ya incluye ese átomo como archivo; obligaría a decidir si se crea, actualiza o solo se verifica.  
3. «actual isolated review status after accepted disposition»: no fija comando ni salida esperada; obligaría a inventar el procedimiento exacto de comprobación.

DRY-RUN  
Un ejecutor futuro leería la tarea, `deskops/services/review.py`, `tests/test_review_command.py`, el átomo citado, `docs/operator-manual.md` y `CHANGELOG.md`. Cambiaría únicamente `_state_for_key` para filtrar por SHA actual antes de aplicar la prioridad, añadiría los escenarios de regresión con los fixtures CLI aislados existentes, registraría el átomo por CLI y ajustaría la documentación. Dependencias: `_sha`, `_review_records`, `_record_key`, `ReviewDoc.input_sha256` y los fixtures de mesa aislada. Validaciones futuras: `pytest tests/test_review_command.py`, comprobación de estado tras disposición aceptada y `pytest` de integración. Sin ejecutar nada.

FUTURO  
Otro nodo o un humano debe precisar el comando de integración, confirmar la forma de registrar el átomo, ejecutar las validaciones y el closeout, y aceptar el resultado conjunto.
