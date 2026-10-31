## REFORMULACION
**Propósito:** fijar un encargo implementable para que manifiesto, RunDoc y cierre sean idempotentes sobre el intento correcto, sin confundirlo con agente o slug.  
**Resultado:** persistencia local repetible sobre el mismo id de intento, conservando identidad, evidencia y hash de sesión sin duplicar registros.  
**Repo:** `deskops`.  
**Límites:** solo store temporal y operaciones locales; sin dispatch/reply ni confirmar Hub; la correlación real es WS34/37 bajo G_EXEC; no inventar artefacto ni hash.

## AMBIGUEDADES
1. **Posible dependencia sobrante de G_SCION.** Cita: `requires: - G_CLOSEOUT - G_SCION - G_WRITE_CONTRACT`, frente a `sin dispatch/reply de red ni confirmar evento Hub no observado; prueba runtime con Hub y correlación es WS34/37 bajo G_EXEC`. Obligaría a decidir si G_SCION —gate de Scion accesible/probado por WS44— condiciona una prueba local de idempotencia o si es una dependencia sobrante y el nodo puede promoverse sin probe vivo.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (WS32.2, WS05, WS12, WS32.1 y gates), `external_references.scion`, `auditoria/scion.md`, `contratos/operaciones.md`, salida de WS32.1, `services/closure.py`, `models/run.py`, `runtime/scion.py` y tests.  
**Cambios previstos:** registro/manifiesto idempotente por intento y pruebas de doble finalización.  
**Dependencias:** WS05, WS12, WS32.1; G_CLOSEOUT satisfecho; G_SCION y G_WRITE_CONTRACT pendientes.  
**Validaciones futuras:** repetir finalización con el mismo id no crea registros; manifiesto, RunDoc y closeout coinciden en id, hash de sesión y evidencia; si falta artefacto/contrato de hash, registrar hueco y bloquear antes de promoción. Sin ejecutar nada.

## FUTURO
WS05 produce inventario/campos; WS12 contrato de operaciones y hash; WS32.1 registro por intento; WS44 probe de G_SCION; WS34/37 correlación real con Hub bajo G_EXEC. La promoción, el TaskDoc y la aceptación del delta corresponden a nodos posteriores y al humano.
