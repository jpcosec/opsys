## REFORMULACION
**Propósito:** revisar WS19 como encargo de planificación, no como implementación. WS19 es un `aggregate` de graph_ui que integra edición de campos y relaciones con conflicto visible, reutilizando editores/API y respetando campos protegidos por workflow.

**Resultado:** agregado no ejecutable; se cierra cuando WS19.1 y WS19.2 cumplen su aceptación. Los dependientes siguen ligados a WS19.

**Repo:** `graph_ui`; `output_scope: 'Agregado: salidas de WS19.1, WS19.2'`.

**Límites:** delta sobre ticket draft, promoción no autorizada, sin duplicado paralelo, sin semántica nueva de relaciones en el componente y sin editar campos workflow-protegidos por este canal. Depende de WS12/WS16, gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas:** guía de revisión, nodo WS19, contratos vecinos WS12/WS16, hijos WS19.1/19.2, gates, brief, alcance, decisiones, cobertura y reconciliación.

**Cambios previstos:** ninguno; esta revisión no modifica dag.yaml ni archivos del repo.

**Dependencias:** WS12 aporta contrato/whitelist; WS16 aporta gate humano de lectura; WS19.1 y WS19.2 aportan aceptación ejecutable; G_UI_WRITE requiere aceptación del delta por responsable graph_ui; G_WRITE_CONTRACT requiere contrato técnico verificado.

**Validaciones futuras:** contrato WS12 por campo/operación, aceptación humana de lectura, persistencia y recarga en hijos, rechazo visible de escritura obsoleta o relación no permitida, y no edición de campos protegidos.

## FUTURO
WS12 debe producir la whitelist, el contrato técnico y la aceptación G_UI_WRITE. WS16 debe producir G_HUMAN_READ con acta humana. WS19.1 y WS19.2 deben implementar y demostrar sus aceptaciones. WS06/WS07 y el responsable graph_ui deben confirmar integración, identidad y no solapamiento antes de despachar código. Nada de esto se resuelve en esta revisión.
