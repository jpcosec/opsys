## REFORMULACION

**Resultado**: La tarea `task-scion-autonomy-review-status` (estado `draft`, nodo `ritual-execution`) exige que la clasificación de estado de review reporte verazmente las disposiciones aceptadas/rechazadas vigentes para el input exacto actual, evitando fallos técnicos falsos y bucles de review. El camino declarado es: en `_state_for_key`, recolectar todos los registros de la clave; sin registros ⇒ `missing`; filtrar por `input_sha256 == _sha(input_data)`; con registros pero ninguno coincidente ⇒ `stale` sin importar veredicto antiguo; entre coincidentes aplicar prioridad existencial `accepted > rejected > pending (state reviewed) > incomplete (state technical_failure)`, preservando recibos y procedencia. Se añaden escenarios de regresión en `tests/test_review_command.py` con sus fixtures CLI aisladas reales, se registra el átomo `atom-review-status-preserves-current-dispositions` vía CLI antes de tocar `docs/operator-manual.md`, y se actualiza `CHANGELOG.md`.

**Repositorio**: `deskops-wt-scion-autonomy`; superficies: `deskops/services/review.py`, `tests/test_review_command.py`, átomo indicado, `docs/operator-manual.md`, `CHANGELOG.md`. Dependencias: ninguna (`depends_on: []`).

**Límites**: solo clasificación de estado de review, sus tests y documentación respaldada por átomo; quedan fuera gates de ciclo de vida, cambios de modelo y de gramática CLI. Es hoja independiente de readiness de runtime de la fase de reparación de autonomía.

## AMBIGUEDADES

Ninguna. El contrato fija criterio de `missing`, `stale`, prioridad entre veredictos coincidentes, identidad por SHA256 de bytes exactos de `input_data`, y preservación de recibos/procedencia.

## DRY-RUN

- **Lecturas hipotéticas**: `review.py` (`_sha`, `_state_for_key`, builders/normalización), fixtures de `test_review_command.py`, átomo referenciado, manual y changelog.
- **Cambios hipotéticos**: sustituir la lógica de `_state_for_key` por recolectar→filtrar por SHA→prioridad existencial; agregar escenarios de regresión (aceptado vigente, rechazado antiguo, stale por cambio de input, pending, technical_failure); registrar átomo vía CLI; documentar contrato.
- **Validaciones hipotéticas**: `pytest tests/test_review_command.py`, estado de review real aislado tras disposición aceptada, `pytest` de integración.

## FUTURO

- Verificar que `_sha` siga usando bytes exactos de `input_data` sin alterar normalización/builders.
- Confirmar que no se modifican gates, modelo ni gramática CLI.
- Comprobar que un aceptado vigente no sea enmascarado por rechazados/recibos antiguos y que un cambio de input reporte `stale`.
- Confirmar que `pending` y `technical_failure` conservan su contrato.
- Asegurar preservación íntegra de recibos y procedencia.
- Validar que los tests usan fixtures CLI aisladas reales y que el átomo se registra vía CLI antes de editar el manual.
- Ejecutar la suite de integración y recoger evidencia de cierre.
