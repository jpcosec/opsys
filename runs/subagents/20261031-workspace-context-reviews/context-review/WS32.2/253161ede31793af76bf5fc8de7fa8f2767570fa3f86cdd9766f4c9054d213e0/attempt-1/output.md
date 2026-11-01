**REFORMULACION**  
Propósito: hacer idempotente el manifiesto, RunDoc y cierre sobre el intento correcto, identificado por su id y no por agente/slug. Resultado: repetir la finalización del mismo intento conserva identidad y evidencia sin crear registros nuevos, y manifiesto/RunDoc/closeout coinciden en id de intento, hash de sesión y evidencia. Repo dueño: `deskops`, con cambios previstos en `runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`. Límites: persistencia local con store temporal; sin dispatch/reply de red ni confirmación de eventos Hub; el hash de sesión depende de inventario WS05 y contrato WS12; si falta artefacto/contrato, se registra hueco y se bloquea antes de promoción.

**AMBIGUEDADES**  
ninguna.

**DRY-RUN**  
Lecturas previstas: nodo WS32.2, referencia externa `scion` con SHA-256, contratos vecinos WS05/WS12/WS32.1, gates y guía/brief/alcance/decisiones. No se ejecuta nada. Cambios previstos: manifiesto por intento, registro RunDoc, cierre idempotente y pruebas en store temporal. Dependencias: WS05 aporta inventario de identidad/API; WS12 fija representación, registro y campos de sesión; WS32.1 separa identidad de intento y dispatch; G_CLOSEOUT está satisfecho; G_SCION sigue no verificado y G_WRITE_CONTRACT pendiente por delta. Validaciones futuras: finalización repetida sobre el mismo id; ausencia de duplicados; coincidencia de id, hash y evidencia; ausencia de red/Hub simulado; bloqueo si falta contrato de hash.

**FUTURO**  
WS05/WS12 deben producir el inventario y contrato exactos del hash de sesión y del registro por intento; WS44/G_SCION y WS34/37 validarán API/Hub reales bajo G_EXEC; la promoción a TaskDoc fijará archivos, pruebas y campos precisos; el receptor pertinente decidirá la aceptación del delta.
