**REFORMULACION**
PK01 es una agrupación de revisión, no un nodo ejecutable: termina cuando terminan sus hijos. Su resultado sustantivo es un paquete factual para deskops: brief/glosario, auditorías de superficies Deskops, persistencia/consultas/notaciones, UI/reconciliación y API Scion, más una matriz de deltas por repo dueño que evite duplicar código. Repo dueño: deskops. Límites: no implementa, no modifica Boards ni tareas ajenas, no acepta producto, no ejecuta probes vivos y WS05 no produce G_SCION.

**AMBIGUEDADES**
Ninguna.

**DRY-RUN**
Hipotéticamente, WS01 parte del brief ya cubierto: verifica hash/alcance y solo corrige brief.md si cambió una decisión; entrega brief.md como entrada común. Con esa entrada, WS02, WS03, WS04 y WS05 pueden avanzar en paralelo, pues solo dependen de WS01 y no hay aristas entre hermanos: WS02 produce `auditoria/deskops.md`; WS03, `auditoria/infraestructura.md`; WS04, `auditoria/ui.md`; WS05, `auditoria/scion.md`. WS05 queda separado: alimenta el ramal E, no WS06. WS06 consume las salidas de WS02, WS03 y WS04 —no la de WS05— e integra en `reconciliacion.md` una fila por capacidad/delta, agrupada por repo dueño, con clasificación (ya cubierto, extender ticket, nuevo delta), path/símbolo, commit observado, ticket destino, responsable y límites de evidencia; añade la atomización propuesta sin notificar ni tocar Boards. Errores esperados: fuente ausente o no comprobada se registra con causa; falta de una salida impide la integración y deja el paquete incompleto. Validación conjunta: cada fila de la matriz debe remitir a evidencia citada en las auditorías; cada nodo graph_ui debe tener correspondencia o ausencia explícita; las auditorías deben distinguir API comprobada, ausencia y hueco; y debe comprobarse que no se crearon tareas, commits ni recepciones ficticias.

**FUTURO**
WS11/WS12 consumen la matriz como fuente de contrato; el receptor P01 produce actas por delta en el repo receptor; el humano decide promoción/aceptación. WS05 alimenta el ramal E y WS44 aporta el probe de G_SCION.
