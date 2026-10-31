## REFORMULACION
**Propósito:** revisar PK01 como encargo de planificación: agrupación de fundamentos y auditoría cuyos hijos directos deben tener revisión vigente o bloqueo externo con responsable. **Resultado:** una disposición de revisión, no implementación ni aceptación de producto. **Repo dueño:** deskops. **Límites:** PK01 es `aggregate` y no se ejecuta; no evalúo los bloques edge WS01–WS06 ni el producto; no ejecuto `context_review.py`; no creo sustitutos para contratos ausentes; no reabro P01–P09; no reviso tareas dependientes.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas previstas:** guía de revisión, nodo PK01, brief, alcance, decisiones, cobertura, reconciliación, IDs de hijos en `dag.yaml` y, si existieran, `disposition.md` de cada hijo. **Cambios previstos:** ninguno en código o documentos del plan; solo la disposición de esta revisión si corresponde. **Dependencias:** revisiones de WS01–WS06, hashes de input y contrato, y estado `context_review.status`. **Validaciones futuras:** coincidencia de hashes con los actuales; existencia de `disposition.md` en el intento correspondiente; admisión de `blocked` solo por causa externa, con responsable y dependencia registrados; comprobación mediante `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops.

## FUTURO
La sesión de coordinación ejecutará `context_review.py status` y guardará la disposición. Los revisores de cada hijo resolverán ambigüedades propias; un responsable externo resolverá los bloqueos admitidos. La aceptación final de PK01 depende de esas revisiones, no de una ejecución de PK01.
