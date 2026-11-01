REFORMULACION
Propósito: definir en `deskops` un adaptador público restringido para dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: agregado no ejecutable cuyas salidas son las de WS34.1 y WS34.2; no añade capacidad propia. Repo dueño: `deskops`. Límites: solo adaptador; no shell arbitrario ni transporte duplicado; no enviar mensajes durante planificación; depende de WS33, WS12 y sus hijos; gates G_EXEC, G_SCION y G_WRITE_CONTRACT; promoción no autorizada.

AMBIGUEDADES
Ninguna. El agregado se acepta por la aceptación de sus hijos; confirmación, timeout y autoridad del coordinador se remiten a WS34.1/WS34.2 y al contrato WS12, sin exigir que el ejecutor de WS34 invente un resultado propio.

DRY-RUN
Lecturas previstas: `dag.yaml` (WS34 y contexto de dependencias), guía, brief, alcance, decisiones, cobertura y `task-ws34.md` cuando exista. Cambios previstos: ninguno; WS34 es `aggregate` y no se ejecuta. Dependencias: WS12 (contrato), WS33 (vinculación), WS34.1/WS34.2 (hijos); gates G_EXEC, G_SCION, G_WRITE_CONTRACT. Validaciones futuras: aceptación de ambos hijos; dispatch real aceptado y otro rechazado o vencido por timeout, correlacionado con el id de intento; reply vinculado al intento correcto; timeout reportado como fallo sin confirmación; ausencia de shell/transporte duplicado; evidencia de contrato por delta.

FUTURO
WS12 produce el contrato de operaciones y autoridad; WS44 verifica Scion; el resolver externo decide G_EXEC; WS34.1/WS34.2 implementan; WS36 consume el adaptador; el responsable humano registra la aceptación por delta en el repo dueño. La promoción futura fijará TaskDoc, archivos, pruebas y evidencia; hoy no está autorizada.
