## REFORMULACION
WS32 es un agregado no ejecutable de implementación en deskops: unificar identidad de intento y cierre Scion partiendo del candidato de drawer referenciado, sin segundo pipeline. Resultado: las salidas de WS32.1 (identidad de intento y separación intent/confirmed) y WS32.2 (manifiesto/RunDoc/cierre idempotentes) aceptadas. Límites: validación local sin dispatch/reply de red ni eventos Hub inventados; la correlación real queda para WS34/37 bajo G_EXEC. Repo dueño: deskops. Gates: G_CLOSEOUT satisfecho, G_SCION sin verificar (productor WS44), G_WRITE_CONTRACT pendiente por delta (WS12). Promoción no autorizada; TaskDoc y archivos exactos quedan para promoción.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Agregado no ejecutable: no produce cambios propios. Termina cuando WS32.1 y WS32.2 cumplen su aceptación; los dependientes siguen colgando de WS32.

Lecturas: candidato `desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md` (sha256 125b862b…), `reconciliacion.md`, inventario WS05, contrato WS12, y código `deskops/runtime/scion.py`, `services/closure.py`, `models/run.py`, `tests/`.

WS32.1 consume WS05/WS12 y los recibos de G_SCION/G_WRITE_CONTRACT; crea identidad de intento persistida y registros intent/no confirmado mediante operaciones reales sobre store temporal; entrega a WS32.2 el contrato de registro/identidad y la semántica de "no confirmado". WS32.2 consume esa entrega y la especificación de sesión/hash de WS12; produce manifiesto, RunDoc y cierre idempotentes sobre el mismo id de intento; entrega evidencia a WS33 y a WS34/37.

Validación conjunta: dos IDs distintos antes de dispatch; repetición de finalización sin registros nuevos; coincidencia de id de intento, hash de sesión y evidencia entre manifiesto, RunDoc y closeout; sin red. Errores esperados: G_SCION ausente bloquea la ejecución de los hijos; falta de producto WS05/WS12 se registra como hueco y detiene; falta de artefacto/contrato de hash bloquea WS32.2 antes de promoción.

## FUTURO
WS44 produce G_SCION; WS12 publica G_WRITE_CONTRACT por delta; WS34/37 prueban Hub real y correlación bajo G_EXEC; un humano designa operador Scion y autoriza promoción/ejecución; WS06/receptor gestiona integración sin duplicar.
