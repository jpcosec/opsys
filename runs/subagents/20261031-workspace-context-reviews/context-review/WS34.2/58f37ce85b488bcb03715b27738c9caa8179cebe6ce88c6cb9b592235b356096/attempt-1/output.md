## REFORMULACION
**Propósito:** implementar un adaptador público restringido para respuesta (reply) vinculado al intento, con timeout/errores y autoridad del coordinador.  
**Resultado:** código en `runtime/`, `cli/commands/runtime.py` o la API que defina WS12, más `tests/`; aceptación mediante agente real que demuestre respuesta vinculada al intento correcto y timeout reportado como fallo sin confirmación, usando el umbral del contrato WS12.  
**Repo:** `deskops`.  
**Límites:** no mandar mensajes durante la tarea de planificación; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT; no se autoriza promoción (`not_authorized`).

## AMBIGUEDADES
Ninguna.

El canal/API queda delegado a WS12; la identidad de intento a WS33/WS32.1; los detalles de archivos, escenarios y evidencia al TaskDoc de promoción. Los gates pendientes son intencionales y no defectos. La ausencia de contrato se resuelve con la regla común: detenerse y registrar el hueco.

## DRY-RUN
**Lecturas previstas:** nodo WS34.2; vecinos WS33, WS12 y WS34.1; gates G_EXEC, G_SCION y G_WRITE_CONTRACT; guía, brief, alcance y decisiones.  
**Cambios previstos:** adaptador de reply, comando/API pública y pruebas; sin ejecución real.  
**Dependencias:** WS33 completo (agregado), contrato WS12, dispatch/identidad de intento de WS34.1, autorización externa G_EXEC y verificación Scion G_SCION.  
**Validaciones futuras:** contrato WS12 aplicado al reply; prueba con agente real; correlación respuesta-intento; timeout como fallo sin confirmación; acta/recepción por delta; preflight de TaskDoc.

## FUTURO
- **WS12** debe fijar canal público, operaciones, autoridad del coordinador, manejo de errores y umbral de timeout.
- **WS33/WS32** deben aportar referencias de mensaje, intento y decisión.
- **WS44** verifica Scion; **G_EXEC** lo autoriza un humano/designee.
- **TaskDoc de promoción** fija archivos exactos, pruebas y evidencia.
- **Receptor P01** registra el acta del delta; la aceptación de implementación no está autorizada.
