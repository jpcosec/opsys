REFORMULACION
Propósito: definir WS34.1 como encargo de implementación para un adaptador público restringido de dispatch, con confirmación de la API de Scion, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: adaptador en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, y pruebas en `tests/`. Repo dueño: `deskops` (`deskops:repository_root/`). Límites: no shell arbitrario, no duplicar transporte, no ejecutar en esta revisión; promoción no autorizada; contrato/API y autoridad se toman de WS12; si falta, rige la regla común de detenerse y registrar hueco.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas (sin ejecutar): nodo WS34.1, vecinos WS33/WS12, gates G_EXEC/G_SCION/G_WRITE_CONTRACT, guía, brief, alcance, decisiones y cobertura.
Cambios previstos: implementar el adaptador y sus pruebas en el repo deskops; no modificar tareas ajenas ni crear sustituto de contrato.
Dependencias: WS33 (agregado de mensajes/resultados/decisiones) y WS12; gates G_EXEC, G_SCION y G_WRITE_CONTRACT. G_SCION depende de WS44; WS12 fija whitelist/canal/efectos.
Validaciones futuras: que pasen los gates; que un agente real demuestre un dispatch aceptado y uno rechazado o vencido por timeout; que la confirmación sea la respuesta de la API de Scion; que se respete la autoridad del coordinador y no haya shell arbitrario ni transporte duplicado.

FUTURO
WS12 produce el contrato de operaciones, la API/canal y la autoridad del coordinador. WS44 produce la comprobación de G_SCION. El humano resuelve G_EXEC (autorización de ejecución/comunicaciones). WS33 aporta referencias de intento. La promoción fijará TaskDoc, archivos, pills, átomos y evidencia; la aceptación con agente real queda para ejecución autorizada.
