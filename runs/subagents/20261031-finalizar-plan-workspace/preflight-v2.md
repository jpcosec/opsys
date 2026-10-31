**Reformulación breve**

- **Intención:** cerrar la planificación documental de `workspace-documental` conforme a las respuestas humanas registradas en `owner-decisions.json`, reconciliando el workspace base real con los deltas declarados, sin implementar producto.
- **Resultado esperado:** plan regenerado desde `dag.yaml`, decisiones trazadas, gates con productor/condición/evidencia/scope, ramales opcionales desacoplados, `cierre.md` authored legible sin chat, reviews baratos vigentes y evidencia de Tester independiente. `execution_authorized=false`; candidatas siguen sin ser TaskDocs ejecutables.
- **Límites:** solo plan, fichas candidatas y evidencia de este run; helpers locales solo si son imprescindibles y sin debilitar validación. No producto, no ritual oficial, no Board/cierre/commit por Executor, no cambios dirty ajenos, no recrear tasks borradas, no afirmar disponibilidad de producto ni autorizaciones no dadas.

**Ambigüedades reales que obligarían a inventar**

1. **G_CLOSEOUT / WS45:** falta precisar el umbral mínimo de prueba focalizada que permite pasar de “pendiente” a “satisfied” si los tests existentes no demuestran autoría/relación task-commit real. El Executor debe decidir con evidencia, no por conveniencia.
2. **Comando pytest:** la cadena `-k ''closeout''` aparece mal citada; requiere selección válida sin inventar cobertura. Debe registrarse comando exacto, salida, exit y commit.
3. **Primera capa preparable:** queda claro que puede ser solo WS01, pero no se fija formato de presentación; no debe convertirse en exigencia editorial.
4. **Cambios en helpers:** “solo si hace falta” necesita justificación verificable y checks semánticos; no se especifica cuáles, correcto para no prescribir de más.
5. **Concilio/Tester:** se describen roles y fuentes futuras; este revisor no acredita que existan ni que las fuentes hayan sido auditadas.

**Dry-run futuro por rol, sin ejecutar**

- **Executor:** leerá TaskDoc, `owner-decisions.json`, revisión previa, fuentes del plan, git/Board y commits/código/tests listados; comprobará `context_review.py status`; corregirá fuentes y congelará; cambiará solo plan/fichas/evidencia; actualizará decisiones P01–P09 sin firmas falsas; añadirá WS45 solo si falta prueba de G_CLOSEOUT; regenerará proyecciones; lanzará reviews afectados con procesos nuevos y stdin cerrado; guardará reformulación, ambigüedades y dry-run; entregará handoff.
- **Supervisor:** validará alcance, comparará outputs contra intención, dispondrá hallazgos con cita/razón, lanzará Tester nuevo y consultará concilio tras congelar; cerrará después.
- **Tester:** auditoría independiente de hashes, aislamiento, cobertura, refs, decisiones y dry-runs; pytest focalizado solo si se propone G_CLOSEOUT satisfied.
- **Validaciones previstas:** `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status` sin stale, revisión de todos los nodos nuevos/afectados y ninguna autorización humana/producto falsa.

No afirmo haber auditado las fuentes citadas; son trabajo futuro del Executor.
