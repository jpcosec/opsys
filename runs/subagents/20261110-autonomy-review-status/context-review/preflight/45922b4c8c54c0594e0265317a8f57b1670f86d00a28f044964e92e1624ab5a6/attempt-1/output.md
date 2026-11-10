## REFORMULACION

**Resultado:** la tarea debe garantizar que el estado de revisión reporte de forma veraz el resultado correspondiente a la entrada exacta actual. Una disposición aceptada vigente no debe quedar ocultada por recibos rechazados o stale anteriores; si cambia la entrada, debe reportarse `stale`; sin entradas, `missing`. La clasificación indicada es: hash coincidente → `accepted` > `rejected` > `pending(reviewed)` > `incomplete(technical_failure)`; `stale` cuando solo existen otras entradas; `missing` cuando no hay ninguna.

**Repo/superficie:** `deskops/services/review.py`, `tests/test_review_command.py`, el átomo `desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md`, `docs/operator-manual.md` y `CHANGELOG.md`. Referencias declaradas: `e58ee061` y `tests/test_review_command.py`. Tarea `task.code`, estado `draft`, nodo `ritual-execution`, sin dependencias ni átomos heredados.

**Límites:** solo clasificación de estado de revisión, sus pruebas y documentación respaldada por átomo. Fuera de alcance: gates de ciclo de vida, cambios de modelo o de gramática CLI. Es una hoja independiente de runtime-readiness dentro de la fase de reparación de autonomía. Deben conservarse todos los recibos. Validación exigida: `pytest tests/test_review_command.py`; estado real de revisión en escritorio aislado tras disposición aceptada; `pytest` en integración. Cierre observable: la disposición aceptada actual sobrevive al estado, los recibos rechazados/stale antiguos no la enmascaran, el cambio de entrada reporta `stale`, y se mantienen los contratos existentes de `pending` y fallo técnico.

## AMBIGUEDADES

- **Identidad de la entrada exacta:** no se define cómo se calcula o compara el hash de entrada que separa “coincidente” de “stale”. Cita: “for the current exact input” y “stale when only other inputs”.
- **Precedencia frente a existencia:** no queda explícito si `stale` y `missing` son estados de clasificación o resultados de ausencia, ni cómo conviven con la precedencia `accepted > rejected > pending(reviewed) > incomplete(technical_failure)`. Cita: “classify matching hash accepted > rejected > pending(reviewed) > incomplete(technical_failure), stale when only other inputs, missing when none”.
- **Ubicación de las regresiones CLI:** se piden “real isolated-desk status CLI regressions”, pero no se indica si deben añadirse a `tests/test_review_command.py` o a otro archivo. Cita: “Add real isolated-desk status CLI regressions”.

## DRY-RUN

**Lecturas hipotéticas:** tarea, workflow enrutado, `review.py`, pruebas existentes, átomo fuente, manual de operador y changelog. **Cambios hipotéticos:** ajustar clasificación y conservación de recibos en `review.py`; añadir regresiones de estado CLI con escritorio aislado; actualizar átomo, documentación y changelog. **Validaciones hipotéticas:** ejecutar `pytest tests/test_review_command.py`; comprobar estado real tras aceptación; ejecutar integración. No se ejecutó ningún comando.

## FUTURO

Comprobar al implementar: que la clasificación use la entrada exacta y no mezcle recibos antiguos; que la precedencia se aplique solo a coincidencias; que `stale` y `missing` sean observables; que no se alteren gates, modelo ni gramática CLI; que las pruebas cubran aceptado, rechazado, pendiente revisado, fallo técnico, stale y missing; que átomo, manual y changelog coincidan con el comportamiento; y que la evidencia de cierre incluya los recibos conservados.
