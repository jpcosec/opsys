## REFORMULACION

**Propósito:** registrar una decisión humana explícita —aprobar o pedir corrección— sobre un intento Scion, con actor humano identificado, asociada al intento y, por él, a su tarea.
**Resultado:** un registro persistido con actor, referencia a intento y tarea, y resultado explícito; la corrección exige texto. El `completed` reportado por el agente no puede registrarse como aprobado.
**Repo:** `deskops`.
**Límites:** solo escribe la decisión mediante la operación que fije el contrato WS12; si falta, hueco con dueño. No escribe estados `completado` (Scion), `validado` ni `cerrado` (deskops). No incluye editor UI, dispatch ni tablas Scion. Depende de WS32, WS33.1, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** guía de context review; brief; alcance; decisiones; cobertura; reconciliación; nodo WS33.2, vecinos WS32/WS33/WS33.1 y gates; referencia externa Scion. Sin ejecución.

**Cambios previstos:** ninguno en esta revisión. La implementación futura quedaría acotada a `deskops:runtime/` (adaptador definido por contrato), `modelos/reportes` y `tests/`.

**Dependencias:** contrato WS12 para operación, actor y errores; identidad de intento de WS32; vinculación de WS33.1; G_SCION producido por WS44; G_WRITE_CONTRACT por delta. La promoción exige TaskDoc, archivos y preflight.

**Validaciones futuras:** registro con actor, intento y tarea; aceptación de ambos resultados; rechazo de “pedir corrección” sin texto; verificación de que `completed` del agente no equivale a aprobado; prueba contra contrato público real; revisión del gate por delta.

## FUTURO

WS12 debe emitir el contrato técnico de la operación. WS44 debe aportar la evidencia de G_SCION. WS32 fija la identidad de intento y WS33.1 vincula mensajes/resultados. La promoción del nodo fija TaskDoc, archivos y pruebas dentro de esta aceptación. El responsable humano acepta el delta en el repo receptor. WS34/WS37 probarán la intervención Scion bajo G_EXEC; no son trabajo de este nodo.
