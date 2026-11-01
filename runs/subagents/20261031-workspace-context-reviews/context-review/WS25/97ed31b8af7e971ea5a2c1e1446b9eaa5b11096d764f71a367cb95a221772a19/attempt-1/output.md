## REFORMULACION
**Propósito:** integrar en la UI la captura y el “triage” mediante operaciones autorizadas por contrato, sin confundir ack con aprobación. **Resultado:** nodo agregado no ejecutable; se cumple cuando WS25.1 y WS25.2 cumplen su aceptación, y sus dependientes siguen dependiendo de WS25. **Repo:** `graph_ui`. **Límites:** no ejecuta por sí mismo; las mutaciones de UI quedan habilitadas por `G_HUMAN_READ`; el desarrollo/pruebas aisladas de API pueden avanzar con contratos/gates técnicos; no se inventan operaciones ni canales fuera de WS12.

## AMBIGUEDADES
1. **“triage” no está definido ni tiene resultado/aceptación propia.** Cita: «Integrar captura y triage en UI». El alcance concreto dice «UI para mensaje/ack y captura interna de drawer/protoátomo», pero no aclara si “triage” comprende clasificar, enrutar, promover, cerrar o solo leer/ack/capturar. Obligaría al ejecutor a inventar operaciones de triage no cubiertas por los hijos. Debe aclararse en el nodo o retirarse del título/alcance.

## DRY-RUN
**Lecturas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y fragmentos del DAG; solo se evalúa WS25, usando WS12/WS30/gates como contexto no revisado. **Cambios previstos:** ninguno en archivos; solo este informe. **Dependencias:** WS12 (contrato), WS25.1 y WS25.2 (hijos), gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`. **Validaciones futuras:** aceptación de ambos hijos; recibos por delta de los gates; validación humana WS30. No se ejecuta nada.

## FUTURO
WS12 debe producir el contrato de operaciones/canal; WS25.1 y WS25.2 deben implementar y demostrar sus aceptaciones; el receptor P01 y WS16 producen los recibos/actas de gates; WS30 valida el recorrido manual. Nada de eso es ambigüedad de WS25 si el contrato falta: `alcance.md` ordena detenerse y registrar el hueco.
