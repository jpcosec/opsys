## REFORMULACION
- **Propósito:** agrupar la revisión del encargo de UI que integra mensaje/ack y captura interna en drawer o protoátomo.
- **Resultado:** nodo `aggregate` no ejecutable; se considera cumplido cuando WS25.1 y WS25.2 cumplen su aceptación. Su salida es el agregado de las salidas de ambos hijos.
- **Repo dueño:** `graph_ui`.
- **Límites:** no confundir ack con aprobación; usar solo operaciones permitidas por el contrato WS12; no crear API/modelo por reflejo; las mutaciones en UI quedan sujetas a G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; el nodo no ejecuta ni sustituye a sus hijos.

## AMBIGUEDADES
ninguna

## DRY-RUN
- **Lecturas realizadas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y definición de WS25 en `dag.yaml`.
- **Cambios previstos:** ninguno; esta revisión no implementa, promueve ni modifica archivos.
- **Dependencias:** contrato WS12; salidas de WS25.1 y WS25.2; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, evaluados por delta.
- **Validaciones futuras:** comprobar aceptación de ambos hijos; verificar que el agregado enlace sus salidas; confirmar recibos por delta cuando correspondan; no habilitar mutaciones UI sin G_HUMAN_READ.

## FUTURO
WS12 produce el contrato de operaciones; WS25.1 y WS25.2 producen sus salidas y pruebas; el receptor P01 emite actas de recepción por delta; la promoción fijará TaskDoc, archivos, pruebas y evidencia; un supervisor o responsable humano decide la promoción del agregado.
