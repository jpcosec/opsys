## REFORMULACION

Propósito: que el estado de revisión reporte verazmente las disposiciones aceptadas/rechazadas para el input exacto actual, evitando fallos técnicos falsos y bucles de revisión. Resultado: en `deskops/services/review.py`, `_state_for_key` recoge todos los registros de la clave; sin registros → missing; con registros pero ninguno cuyo `input_sha256` iguale `_sha(input_data)` → stale; entre coincidentes, prioridad existencial accepted > rejected > pending (state reviewed) > incomplete (technical_failure). Mantener `_sha`, normalización, builders, recibos y procedencia. Añadir escenarios de regresión en `tests/test_review_command.py` con sus fixtures CLI aisladas reales; registrar el atom vía CLI antes de tocar `docs/operator-manual.md`; actualizar CHANGELOG según `files`. Límites: solo clasificación de estado, tests y documentación respaldada por atom; sin cambios en gates de ciclo de vida, modelo ni gramática CLI. Repo: `deskops-wt-scion-autonomy`. Es un nodo ejecutable `task.code`, no un agregado; este preflight no ejecuta.

## AMBIGUEDADES

1. "Add all regression scenarios" — no enumera cuáles; obligaría a inventar la matriz completa de combinaciones.
2. "actual isolated review status after accepted disposition" — no da comando ni fixture; obligaría a inventar la invocación CLI.
3. "pytest at integration" — no identifica suite, marcador ni ruta; obligaría a inventar el comando.
4. "Record atom-review-status-preserves-current-dispositions via CLI" — no especifica subcomando ni formato; obligaría a inventar la sintaxis.
5. "CHANGELOG.md" figura en `files`, pero no se indica entrada ni formato; obligaría a inventar contenido.
6. Rationale "Not provided" y summary vacío: sin contexto de negocio; obligaría a inventar motivación si se exigiera.

## DRY-RUN

Lecturas: TaskDoc, workflow enrutado, `review.py` (`_sha`, `_state_for_key`, builders), `tests/test_review_command.py`, atom, manual, CHANGELOG. Cambios previstos: reordenar `_state_for_key` (recoger→filtrar por sha→prioridad); añadir tests; registrar atom por CLI; editar manual y CHANGELOG. Dependencias: helpers existentes, fixtures CLI de desk aislado, CLI de atoms. Validaciones futuras: `pytest tests/test_review_command.py`; estado aislado tras disposición aceptada; pytest de integración. Sin ejecutar.

## FUTURO

Otro nodo ejecuta la implementación y los tests; produce resultados de pytest, recibo del atom y evidencia de closeout. Un humano aprueba el encargo y acepta el resultado; no son ambigüedades.
