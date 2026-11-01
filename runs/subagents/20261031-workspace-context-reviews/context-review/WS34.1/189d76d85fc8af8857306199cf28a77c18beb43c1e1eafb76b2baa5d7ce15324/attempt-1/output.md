REFORMULACION
Propósito: definir un adaptador público restringido para despachar trabajo a Scion desde Deskops, con confirmación observada, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: dispatch autorizado, sin shell arbitrario ni transporte duplicado, correlacionado con el id de intento local previo WS32.1 y registros WS32.2, con evidencia de un dispatch aceptado y otro rechazado o vencido por timeout. Repo dueño: deskops; salidas en runtime/, cli/commands/runtime.py o la API que fije WS12, y tests/. Límites: depende de WS33 y WS12; exige G_EXEC, G_SCION y G_WRITE_CONTRACT; solo avanza con la política de timeout de este delta en WS12; si falta, se detiene y registra el hueco; esta revisión no ejecuta nada.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas previstas: nodo WS34.1; contrato WS12 para autoridad, API y timeout; salidas WS32.1/WS32.2 a través de WS33; evidencia de G_SCION/G_EXEC. Cambios previstos: adaptador de dispatch y pruebas en deskops; no UI, no shell arbitrario, no transporte nuevo. Dependencias: WS33, WS12, gates citados y política de timeout por delta. Validaciones futuras: gates pasan; agente real produce un dispatch aceptado y uno rechazado o timeout; se correlaciona con el id de intento y registros; confirmed solo con respuesta observada del Hub; la ausencia de confirmación no se convierte en éxito/fallo remoto; sin política de timeout, parada y registro de hueco.

FUTURO
WS12 fija autoridad, API y umbral/clasificación de timeout; WS32.1/WS32.2 aportan id de intento y registros; WS44 y G_SCION producen el probe; un humano resuelve G_EXEC; WS34.2 cubre reply; G_WRITE_CONTRACT verifica por delta; la promoción/TaskDoc fija archivos, pills y evidencia dentro de la aceptación.
