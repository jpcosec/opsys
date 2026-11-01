REFORMULACION

PK01 es un agregado de revisión no ejecutable: no implementa ni valida producto. Propósito: fijar la base factual (brief/glosario y auditorías) y una matriz de deltas verificables para evitar duplicar código. Resultado: brief.md cubierto, auditorías de Deskops, infraestructura, UI y Scion, y reconciliacion.md con reutilización/ticket/nuevo delta, evidencia y repo dueño. Repo dueño: deskops; las auditorías leen repos externos sin cambiarlos. Límites: sin implementación, aceptación de producto, probes vivos, autorización de tareas/aristas ni supuestos de chat.

AMBIGUEDADES

Ninguna.

DRY-RUN

Hipotético, sin ejecutar. PK01 no se ejecuta: termina con sus hijos. WS01 parte del brief/glosario ya authored y verifica su cobertura; entrega brief.md como base común. Tras WS01, WS02, WS03, WS04 y WS05 pueden avanzar en paralelo: WS02 lee archivos/comandos/modelos y store local de deskops; WS03 lee sldb/pron/spec2viz; WS04 lee Board, código y sesiones de graph_ui; WS05 lee código/documentación de deskops y scion sin endpoints vivos. Salidas: auditoria/deskops.md, infraestructura.md, ui.md y scion.md; cada una cita path/símbolo, estado comprobado o «no comprobado» con causa. WS06 espera WS02–WS04 (no WS05): consume brief y las tres auditorías, y escribe reconciliacion.md con una fila por capacidad/delta, repo, clasificación, nodos, evidencia y límites; conserva la descomposición Scion ya registrada y no toca Boards. Integración: WS06 cruza auditorías, elimina duplicados y enlaza cada delta a su dueño; WS05 entrega su inventario a E y, si falta, el paquete queda incompleto pero WS06 no inventa API Scion. Validación esperada: cada fila auditada tiene ubicación y estado; cada fila C tiene dueño, clasificación y límites; los 64 nodos quedan cubiertos; no aparecen gates, firmas ni recepción ficticia. Errores: repo/store inaccesible se registra como no comprobado; falta de una auditoría impide completitud, no se sustituye.

FUTURO

WS11/WS12 convierten filas en contratos y enlazan actas; WS44 obtiene evidencia de G_SCION; WS16/WS30/WS37 validan con humanos; el receptor P01 emite actas por delta; las decisiones P01–P09 siguen siendo registro, no permiso de implementación.
