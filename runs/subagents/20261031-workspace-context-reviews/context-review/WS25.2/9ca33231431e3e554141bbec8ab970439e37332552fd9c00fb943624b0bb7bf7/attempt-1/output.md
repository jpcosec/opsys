## REFORMULACION
**Propósito:** entregar captura interna en el workspace con destino elegido explícitamente: candidato de drawer o protoátomo, sin exigir crear tarea. **Resultado:** una captura persiste tras recarga en el destino elegido, conserva un origen tipado (ruta o mensaje) y no crea tarea implícita; permisos del contrato WS12 aplicados; cada destino se prueba por separado. **Repo:** `graph_ui`, salida en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. **Límites:** no implementa mensaje/ack (WS25.1); no sustituye el contrato WS12; WS25 es agregado no ejecutable; promoción no autorizada.

## AMBIGUEDADES
1. **Origen obligatorio frente a protoátomo libre.** Cita: «Origen = referencia tipada al soporte del que nace la captura (ruta o mensaje)» y, en brief.md, «Protoátomo: átomo libre con título y contenido». Obliga a inventar si un protoátomo puede capturarse sin soporte de origen, qué origen mostrar en ese caso o si debe rechazarse; la aceptación exige «con origen» sin excepción.
2. **Elección del destino.** Cita: «destino elegido explícitamente por la persona usuaria» y «persiste tras recargar en el destino elegido». No define cómo se elige ni qué ocurre si no hay elección (¿bloquear guardado, destino por defecto, recordar último?). El ejecutor tendría que inventar el comportamiento, que afecta a la aceptación.

## DRY-RUN
**Lecturas:** dag.yaml (nodo, gates, vecinos), brief.md, alcance.md, decisiones.md, cobertura.md y guía; no se suministra TaskDoc ni contrato WS12. **Cambios previstos:** ninguno; solo revisión. **Dependencias:** WS12 debe producir whitelist/capabilities y representación del origen; WS16 debe producir acta G_HUMAN_READ; G_UI_WRITE exige delta aceptado por responsable `graph_ui` designado; G_WRITE_CONTRACT pendiente. **Validaciones futuras:** persistencia tras recarga para drawer y protoátomo por separado; visualización de orígenes ruta y mensaje; ausencia de TaskDoc creado; permisos del contrato aplicados; pruebas en `tests/`.

## FUTURO
WS12 fija contrato, endpoints y representación del origen; WS16 produce la aprobación humana de lectura; el solicitante designa responsable de `graph_ui` y decide P01/P03–P06; el TaskDoc de promoción fijará archivos, textos y casos de prueba; un humano autoriza la promoción.
