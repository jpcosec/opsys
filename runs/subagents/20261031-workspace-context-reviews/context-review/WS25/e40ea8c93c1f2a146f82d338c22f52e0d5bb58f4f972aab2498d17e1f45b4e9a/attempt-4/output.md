## REFORMULACION

**Propósito:** integrar en la UI la lectura de inbox con ack/respuesta local y la captura interna en drawer o protoátomo, usando solo operaciones autorizadas por contrato y sin confundir ack con aprobación.

**Resultado:** nodo `aggregate` no ejecutable; su aceptación es el agregado de las aceptaciones de WS25.1 y WS25.2.

**Repo dueño:** `graph_ui`.

**Límites:** no envío interdesk, no tarea implícita, no cron de triage, no promoción autorizada; los dependientes siguen dependiendo de WS25.

## AMBIGUEDADES

Ninguna. El nodo delega resultado y aceptación comprobable en WS25.1/WS25.2, identifica repo, dependencias y límites. Los gates pendientes son intencionales. La ausencia de contrato operativo está cubierta por alcance.md: detenerse, registrar hueco y declarar la operación no disponible. Los detalles de archivos, pruebas y textos quedan para el TaskDoc de promoción.

## DRY-RUN

**Lecturas previstas:** guía de revisión; brief; alcance; decisiones; cobertura; nodo WS25; contratos vecinos WS12, WS16, WS25.1, WS25.2 y gates. Sin revisar otros bloques edge.

**Cambios previstos:** ninguno; esta revisión no modifica el plan ni ejecuta el nodo.

**Dependencias:** WS12 debe producir contrato de operaciones y aceptar deltas de escritura; WS16 debe aportar aprobación humana de lectura; WS25.1 y WS25.2 deben cumplir sus aceptaciones. Los gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT siguen pendientes.

**Validaciones futuras:** aceptación de cada hijo; persistencia de ack y respuesta local según contrato; captura persistente con origen y sin tarea implícita; permisos aplicados; posterior recorrido UF02/UF03 en WS30. No se valida todavía que el producto sea bueno.

## FUTURO

- WS07/WS12 resuelven contrato, actor responsable y deltas de escritura.
- Un humano produce G_HUMAN_READ mediante WS16.
- El TaskDoc de promoción fija archivos, escenarios y textos dentro de la aceptación existente.
- WS25 termina cuando terminan WS25.1 y WS25.2; WS30 podrá validar después el recorrido manual.
