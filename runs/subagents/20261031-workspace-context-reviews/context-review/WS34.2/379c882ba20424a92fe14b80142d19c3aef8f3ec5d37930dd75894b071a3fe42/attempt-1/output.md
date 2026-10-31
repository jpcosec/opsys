REFORMULACION
- Propósito: definir WS34.2 como adaptador público restringido para reply Scion, vinculado a un intento.
- Resultado: implementación en `runtime/`, `cli/commands/runtime.py` o API definida, y `tests/`, con timeout/errores y autoridad del coordinador.
- Repo dueño: `deskops`.
- Límites: no duplicar transporte, no mandar mensajes durante planificación; reply solo tras gates y contrato. Depende de WS33, WS12 y WS34.1.

AMBIGUEDADES
Ninguna.

DRY-RUN
- Lecturas previstas: guía, brief, alcance, decisiones y `dag.yaml#node:WS34.2`; al ejecutar, contrato WS12, enlaces de WS33, adaptador dispatch WS34.1 y TaskDoc de promoción.
- Cambios previstos, sin ejecutar: adaptador público de reply, ruta CLI/API según contrato, pruebas de respuesta vinculada al intento y timeout.
- Dependencias: WS33 aporta referencias mensaje/intento y decisión; WS12 fija operación, autoridad, errores y umbral; WS34.1 aporta dispatch/intento previo. Gates: `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`.
- Validaciones futuras: agente real demuestra respuesta ligada al intento correcto; timeout se reporta como fallo sin confirmación; umbral según WS12; no envío de mensajes en planificación.

FUTURO
- WS12 produce contrato técnico y umbral; WS33 produce vínculos de mensajes/resultados/decisiones; WS34.1 produce dispatch autorizado; WS44 verifica Scion; un humano resuelve `G_EXEC`.
- La promoción fijará archivos, pills, evidencias y preflight; otro nodo/humano autoriza implementación y recepción por delta.
