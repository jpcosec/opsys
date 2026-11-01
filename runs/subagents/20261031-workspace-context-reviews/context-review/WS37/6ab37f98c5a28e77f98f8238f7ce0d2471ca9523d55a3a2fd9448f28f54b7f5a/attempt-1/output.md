## REFORMULACION
WS37 es un nodo de **validación** (no de implementación) cuyo propósito es comprobar UF06 real con un agente Scion: pregunta, intervención, corrección, evidencia y decisión humanas, y cierre mediante el handoff de WS28. El resultado es un acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/` que acredita el recorrido y alimenta `G_HUMAN_DELEGATE`. Repo dueño: **graph_ui**. Límites: no sustituir integración por mocks ni «completed» por aprobación; no bloquea WS31; `promotion: not_authorized`; exige `G_EXEC` y `G_SCION`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el protocolo `validacion-humana.md`, las decisiones P08/P01, los contratos e implementaciones de WS36, WS34, WS33 y WS28, el acta aceptada de WS30, `autorizaciones/scion.md` (`G_EXEC`), el probe de WS44 (`G_SCION`) y el corpus WS40. Antes de actuar comprobaría ambos gates: si `G_EXEC` no está firmado o `G_SCION` no está verificado por WS44, se detiene y registra el hueco con repo dueño, sin crear sustituto.

Con gates verdes: prepararía el entorno Taller, ejecutaría un intento real por el adaptador WS34 a través de WS36 —sin mocks—, plantearía una pregunta con referencias, registraría respuesta y decisión humanas, una corrección con su evidencia y cerraría por el handoff de WS28. Dependencias efectivas: WS36 y WS30; WS28 llega de forma transitiva vía WS30.

Cambios previstos: solo crear/versionar el acta y enlazar evidencia; ningún cambio de código. Validaciones: actor humano, versión/commit, guion, comandos públicos, timestamps, corpus, resultados técnicos y decisión explícita; cada mensaje/resultado vinculado al intento correcto; `completed` no equivale a aprobado. Un fallo de guion bloquea el gate y abre tarea en el nodo causante; si la causa no se aísla, incidente con repo/superficie y diagnóstico autorizado. Al final, `G_HUMAN_DELEGATE` queda con acta verificable en graph_ui. WS37 no es agregado: no tiene hijos cuyo cumplimiento recorrer.

## FUTURO
WS38 publica los capítulos usando el acta de WS37 y los átomos de WS31. Un humano designa el operador Scion y firma `G_EXEC`/`G_HUMAN_DELEGATE`; WS44 produce el probe de `G_SCION`; WS30 entrega la base manual aceptada.
