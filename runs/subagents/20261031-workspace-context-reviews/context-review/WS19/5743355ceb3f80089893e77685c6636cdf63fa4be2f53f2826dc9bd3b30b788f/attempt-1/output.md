## REFORMULACION

**Propósito:** agregar la integración de edición de campos con conflicto visible y de relaciones permitidas, reutilizando editores, API, revisión esperada y before-image. **Resultado:** agregado no ejecutable; se completa cuando WS19.1 y WS19.2 cumplen su aceptación. **Repo:** `graph_ui`, delta sobre workspace integrado `a1b2b22`. **Límites:** no crear semántica de relaciones en el componente; no editar campos workflow-protected por este canal; no sustituir contratos de WS12; los gates pendientes no habilitan uso de mutaciones en UI.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas previstas:** nodo WS19, hijos WS19.1/WS19.2, contrato WS12 (`contratos/operaciones.md`), guía y decisiones. No se revisan los bloques edge como contratos vecinos.
- **Cambios previstos:** ninguno propio del agregado; verificará salidas de sus hijos, sin duplicar implementación ni ejecutar mutaciones.
- **Dependencias:** WS12 produce contrato/whitelist; WS19.1 y WS19.2 producen los deltas del agregado. Gates `G_WRITE_CONTRACT`, `G_UI_WRITE` y `G_HUMAN_READ` son prerrequisitos declarados.
- **Validaciones futuras:** aceptación de ambos hijos; contrato y recibo por delta concreto; prueba de guardado/recarga, conflicto visible, alta/baja persistente y rechazo de relación no permitida o revisión obsoleta. `G_HUMAN_READ` se exige antes de habilitar mutaciones en UI, no para desarrollo/pruebas aisladas de API.

## FUTURO

WS12 publicará la whitelist y el contrato técnico por operación. WS16 producirá el acta de lectura para `G_HUMAN_READ`. El receptor P01 en `graph_ui` registrará el acta de recepción por delta para `G_UI_WRITE`. WS19.1 y WS19.2 implementarán y probarán sus entregas; WS21 y WS42 consumirán el agregado. La promoción de WS19 sigue no autorizada: un humano deberá autorizarla y el TaskDoc de promoción fijará archivos, pruebas y textos dentro de la aceptación.
