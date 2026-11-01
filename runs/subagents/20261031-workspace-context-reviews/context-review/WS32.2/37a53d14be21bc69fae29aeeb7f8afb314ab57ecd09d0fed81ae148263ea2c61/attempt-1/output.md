REFORMULACION

Propósito: completar WS32.2 dentro de WS32, haciendo idempotente el manifiesto por intento, su RunDoc y los registros de cierre en deskops, sin contactar Scion. Resultado: manifiesto canónico local por id de intento; finalización repetida que conserva identidad/evidencia sin duplicar registros; manifiesto, RunDoc y cierre coinciden en id de intento, hash de sesión y evidencia. Repo dueño: deskops (`runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`). Límites: sin dispatch/reply ni Hub; el hash de sesión lo fijan WS05/WS12; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; la correlación real con Hub queda en WS34/37 bajo G_EXEC. Promoción no autorizada.

AMBIGUEDADES

1. «identidad de run si la API la expone» figura entre los «campos mínimos» del manifiesto. Si WS05 concluye que la API no la expone, no se dice si el campo se omite y el manifiesto sigue siendo canónico o si es hueco bloqueante; obligaría a inventar la obligatoriedad del esquema. La aceptación solo exige coincidencia en id de intento, hash de sesión y evidencia.

2. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos» no define qué operación concreta es «finalización» ni si «registros» incluye los efectos Git de `services/closure.py` (commit/amend, borrado de tarea) o solo RunDoc/manifiesto. Obligaría a inventar el alcance de la idempotencia y qué duplicados prohibir.

DRY-RUN

Lecturas: nodo, candidato drawer sha256 125b862b…, inventario WS05, contrato WS12, recibo G_CLOSEOUT, `record_scion_run`, `close_from_run`, `models/run.py` y tests. Cambios: modelo/manifiesto con id de intento, agente, run (si procede), timestamps, hash de sesión, evidencia y commit; persistencia idempotente por id de intento; cierre que reutiliza registros; pruebas con store temporal. Dependencias: registro de WS32.1 (intento/confirmado); WS05 para exposición de run; WS12 para hash y operaciones; G_SCION/G_WRITE_CONTRACT pendientes por delta. Errores: hash ausente → registrar hueco y bloquear esa coincidencia; sin red ni Hub simulado. Validación esperada: dos finalizaciones → un manifiesto/RunDoc y evidencia coincidente, sin registros nuevos. WS32 agrega: WS32.1 entrega registro e identidades; WS32.2, manifiesto canónico e idempotencia; el agregado termina cuando ambos cumplen.

FUTURO

WS05 entrega inventario de API/identidad; WS12 fija representación del hash de sesión y operaciones; WS44 produce G_SCION; WS34/37 prueban dispatch y correlación real bajo G_EXEC; un humano autoriza promoción y designa operador Scion. No son ambigüedades de este nodo.
