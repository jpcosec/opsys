## REFORMULACION
WS07 es un nodo de planificación, no de implementación, con repo dueño `deskops`. Su propósito es mantener trazado el registro de decisiones acordadas reutilizando `decisiones.md` y `owner-decisions.json`: respuestas humanas 0–2, mapeo P01–P09 y campos de tipo, actor, fuente y nodos/gates. El resultado esperado es un registro verificable de cada Pxx, distinguiendo lo humano de las precisiones técnicas derivadas; P07/P09 son defaults técnicos delegados, no firmas humanas. También conserva `baseline_proposal` y `parameters.source_mode=editable` condicionado a `G_SOURCE`. Límites: no repetir preguntas resueltas, no inferir aceptación de API/UI, contratos, actas ni permisos Scion, y no actualizar decisiones salvo cambio real con fuente verificable. No sustituye la cobertura de UFs ni las auditorías de WS06.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` (WS07, `parameters`, gates `G_PRODUCT`/`G_WRITE_POLICY`/`G_SOURCE`), `decisiones.md` y `owner-decisions.json`. Como `depends_on: WS06`, comprobaría que existe el producto de WS06 (`reconciliacion.md`) o registraría el hueco conforme a las reglas comunes; no lo usaría para sustituir el registro de decisiones.

Contrastaría cada P01–P09 con: tipo humano/técnico, actor, fuente exacta y nodos/gates. Verificaría que P07/P09 figuran como técnicos delegados, que `source_mode` sigue condicionado a `G_SOURCE` y que `baseline_proposal` no cambia. Si falta un campo, solo lo completaría cuando la fuente suministrada lo sostenga; si falta la fuente, se detendría y registraría el hueco, sin inventar actor ni aceptación. No se prevén cambios en `dag.yaml` salvo una nueva decisión explícita con fuente verificable; tampoco se esperan cambios en `decisiones.md` si la trazabilidad ya está completa.

Validación esperada: cada Pxx tiene los cuatro campos exigidos, las precisiones técnicas no se presentan como firmas humanas y no se infiere permiso Scion ni aprobación de implementación. Error esperado: `owner-decisions.json` ausente, Pxx sin fuente o contradicción entre fuentes → detenerse y registrar el hueco. La promoción queda no autorizada.

## FUTURO
WS08 consume las decisiones y gates registrados; WS20 produce `G_SOURCE`. Cualquier nueva decisión de producto o cambio de `baseline_proposal` corresponde a una decisión humana explícita con fuente verificable, no a este nodo. La autorización de promoción y el TaskDoc correspondiente los decide un humano.
